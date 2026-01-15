# Routes: 
#   /readNotifications [DELETE]
# -----------------------------------------------------------------------------------------

import os
from flask import Blueprint, g, jsonify, request
from psycopg2 import sql
from psycopg2.extras import RealDictCursor # ADDED BY SMU GROUP 3

# Import the database manager for connection pooling
from app import db_manager


file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

# -----------------------------------------------------------------------------------------
# Helper function 
def add_notification_to_db(data, cursor=None):
    """
    Expects `data` to contain these keys (matching exactly the column names):
      - userId    [int]
      - userType  [str]
      - notiTabs  [str]
      - notiType  [str]
      - image     [str] 
      - link      [str] 
      - message   [str]
      - createdAt [int] 
      - read      [bool] 
    We no longer pass `createdAt` explicitly, so the DB DEFAULT CURRENT_TIMESTAMP is used.
    
    Args:
      - data: dict with notification fields
      - cursor: optional database cursor. If provided, uses existing cursor (shares connection).
                If None, creates its own connection (standalone mode).
    """
    try:
        if cursor is not None:
            # Use existing cursor - shares the connection with caller (no new connection checkout)
            cursor.execute(
                '''
                INSERT INTO "notifications"
                    ("userId", "userType", "notiTabs", "notiType", "image", "link", "message", "createdAt", "read")
                VALUES (%s,      %s,        %s,        %s,        %s,      %s,      %s, %s, %s)
                ''',
                (
                    data.get('userId'),
                    data.get('userType'),
                    data.get('notiTabs'),
                    data.get('notiType'),
                    data.get('image'),   # may be None
                    data.get('link'),    # may be None
                    data.get('message'),
                    data.get('createdAt'),  
                    data.get('read', False)
                )
            )
        else:
            # Standalone mode - create own connection (backwards compatible)
            with db_manager.get_cursor() as own_cursor:
                own_cursor.execute(
                    '''
                    INSERT INTO "notifications"
                        ("userId", "userType", "notiTabs", "notiType", "image", "link", "message", "createdAt", "read")
                    VALUES (%s,      %s,        %s,        %s,        %s,      %s,      %s, %s, %s)
                    ''',
                    (
                        data.get('userId'),
                        data.get('userType'),
                        data.get('notiTabs'),
                        data.get('notiType'),
                        data.get('image'),   # may be None
                        data.get('link'),    # may be None
                        data.get('message'),
                        data.get('createdAt'),  
                        data.get('read', False)
                    )
                )
        return True

    except Exception as e:
        # Log the actual exception for debugging
        print("add_notification_to_db error:", str(e))
        return False


# -----------------------------------------------------------------------------------------
# Helper function to notify topic/newsletter subscribers when a new story is published
# -----------------------------------------------------------------------------------------
def _slugify_for_url(name):
    """Convert a name to a URL-safe slug (lowercase, spaces to hyphens)."""
    import re
    if not name:
        return ""
    # Convert to lowercase, replace spaces with hyphens, remove non-alphanumeric except hyphens
    slug = name.lower().strip()
    slug = re.sub(r'\s+', '-', slug)  # Replace spaces with hyphens
    slug = re.sub(r'[^a-z0-9\-]', '', slug)  # Remove non-alphanumeric except hyphens
    slug = re.sub(r'-+', '-', slug)  # Collapse multiple hyphens
    return slug.strip('-')


def notify_story_subscribers(cursor, story_id, story_title, topic_id=None, newsletter_id=None, topic_name=None, newsletter_name=None):
    """
    Sends notifications to subscribers of a topic and/or newsletter when a new story is published.
    Combines notifications for users subscribed to both topic AND newsletter to avoid duplicates.
    
    Args:
        cursor: Database cursor
        story_id: ID of the published story
        story_title: Title of the story
        topic_id: ID of the topic (optional)
        newsletter_id: ID of the newsletter (optional)
        topic_name: Name of the topic (optional, fetched if not provided)
        newsletter_name: Name of the newsletter (optional, fetched if not provided)
    
    Notification behavior:
        - Users subscribed to topic only: "New Story in [Topic]: [Story Title]"
        - Users subscribed to newsletter only: "New Story in [Newsletter]: [Story Title]"
        - Users subscribed to both: "New Story in [Topic] and [Newsletter]: [Story Title]"
    """
    from datetime import datetime
    
    if not topic_id and not newsletter_id:
        return  # No subscribers to notify
    
    try:
        current_time = datetime.now().isoformat()
        
        # Fetch topic name if not provided
        if topic_id and not topic_name:
            cursor.execute('SELECT "topicName" FROM "topics" WHERE id = %s', (topic_id,))
            topic_row = cursor.fetchone()
            if topic_row:
                topic_name = topic_row['topicName']
        
        # Fetch newsletter name if not provided
        if newsletter_id and not newsletter_name:
            cursor.execute('SELECT "newsletterName" FROM "newsletters" WHERE id = %s', (newsletter_id,))
            newsletter_row = cursor.fetchone()
            if newsletter_row:
                newsletter_name = newsletter_row['newsletterName']
        
        # Collect all subscribers with their subscription types
        topic_subscribers = set()  # (userID, userType) tuples
        newsletter_subscribers = set()  # (userID, userType) tuples
        
        # Get topic subscribers
        if topic_id:
            cursor.execute('''
                SELECT "userID", "userType" 
                FROM "topicSubscribers" 
                WHERE "topicID" = %s
            ''', (topic_id,))
            topic_subscribers = {(row['userID'], row['userType']) for row in cursor.fetchall()}
        
        # Get newsletter subscribers (active ones only)
        if newsletter_id:
            cursor.execute('''
                SELECT "patronUserID", "patronUserType" 
                FROM "newsletterPatrons" 
                WHERE "newsletterID" = %s AND "subscriptionStatus" = 'active'
            ''', (newsletter_id,))
            newsletter_subscribers = {(row['patronUserID'], row['patronUserType']) for row in cursor.fetchall()}
        
        # Determine link destination
        # Priority: newsletter page if newsletter_id exists, else topic page
        # URL format: /stories/newsletters/:ID/:name or /stories/topics/:ID/:name
        if newsletter_id and newsletter_name:
            newsletter_slug = _slugify_for_url(newsletter_name)
            link = f"/stories/newsletters/{newsletter_id}/{newsletter_slug}"
        elif topic_id and topic_name:
            topic_slug = _slugify_for_url(topic_name)
            link = f"/stories/topics/{topic_id}/{topic_slug}"
        else:
            link = None
        
        # Find users in both (for combined notification)
        both_subscribers = topic_subscribers & newsletter_subscribers
        topic_only = topic_subscribers - both_subscribers
        newsletter_only = newsletter_subscribers - both_subscribers
        
        notifications_sent = 0
        
        # Send combined notifications (subscribed to both)
        for user_id, user_type in both_subscribers:
            message = f"New Story in {topic_name} and {newsletter_name}: {story_title}"
            notification_data = {
                "userId": user_id,
                "userType": user_type,
                "notiTabs": "forYou",
                "notiType": "story_new",
                "image": None,
                "link": link,
                "message": message,
                "createdAt": current_time,
                "read": False
            }
            if add_notification_to_db(notification_data, cursor):
                notifications_sent += 1
        
        # Send topic-only notifications
        for user_id, user_type in topic_only:
            message = f"New Story in {topic_name}: {story_title}"
            topic_slug = _slugify_for_url(topic_name)
            notification_data = {
                "userId": user_id,
                "userType": user_type,
                "notiTabs": "forYou",
                "notiType": "topic_new_story",
                "image": None,
                "link": f"/stories/topics/{topic_id}/{topic_slug}",
                "message": message,
                "createdAt": current_time,
                "read": False
            }
            if add_notification_to_db(notification_data, cursor):
                notifications_sent += 1
        
        # Send newsletter-only notifications
        for user_id, user_type in newsletter_only:
            message = f"New Story in {newsletter_name}: {story_title}"
            newsletter_slug = _slugify_for_url(newsletter_name)
            notification_data = {
                "userId": user_id,
                "userType": user_type,
                "notiTabs": "forYou",
                "notiType": "newsletter_new_story",
                "image": None,
                "link": f"/stories/newsletters/{newsletter_id}/{newsletter_slug}",
                "message": message,
                "createdAt": current_time,
                "read": False
            }
            if add_notification_to_db(notification_data, cursor):
                notifications_sent += 1
        
        print(f"notify_story_subscribers: Sent {notifications_sent} notifications for story {story_id}")
        return notifications_sent
        
    except Exception as e:
        print(f"notify_story_subscribers error: {str(e)}")
        return 0


# Helper function to get the list of users who follow a specific producer or venue
def get_followers(user_id, user_type):
    """
    Returns a list of user IDs who follow the specified producer or venue.
    Expects:
        - user_id: ID of the producer or venue
        - user_type: Type of the user (e.g., 'producers', 'venues')
    """
    try:
        with db_manager.get_cursor() as cursor:
            if user_type == 'producers':
                cursor.execute(
                    '''
                    SELECT "userId"
                    FROM "usersFollowLists"
                    WHERE %s IN ANY("producers")
                    ''',
                    (user_id,)
                )

            elif user_type == 'venues':
                cursor.execute(
                    '''
                    SELECT "userId"
                    FROM "usersFollowLists"
                    WHERE %s IN ANY("venues")
                    ''',
                    (user_id,)
                )
            else:
                print("Invalid user_type:", user_type)
                return []

            followers = cursor.fetchall()
            return [row['userId'] for row in followers]

    except Exception as e:
        print("get_followers error:", str(e))
        return []

# -----------------------------------------------------------------------------------------

# [DELETE] /readNotifications
# PURPOSE: Remove record from notifications table if user has read the notification
@blueprint.route('/readNotification', methods=['DELETE'])
def readNotification():
    """
    DELETE a notification by its ID. Used to mark it as read/remove it.
    """
    notification = request.get_json()
    notif_id = notification.get('id')
    notiType = notification.get('notiType')
    link = notification.get('link')
    
    try:
        with db_manager.get_cursor() as cursor:
            if notiType == 'news':
                # If it's a news notification, we delete it from the "notifications" table
                cursor.execute(
                    'UPDATE "notifications" SET "read" = TRUE WHERE "id" = %s AND "notiType" = %s AND "link" = %s',
                    (notif_id, notiType, link)
                )
            else:
                cursor.execute(
                    'DELETE FROM "notifications" WHERE id = %s',
                    (notif_id,)
                )
        
        return jsonify({'success': True}), 200

    except Exception as e:
        print("Error deleting notification:", str(e))
        return jsonify({
            'success': False,
            'message': 'Error deleting notification.'
        }), 500

# [POST] /notifications/markAllRead
# PURPOSE: Mark all notifications as read
@blueprint.route('/markAllRead', methods=['POST'])
def mark_all_read():
    data = request.get_json()
    user_id = data.get('userId')
    user_type = data.get('userType')
    try:
        with db_manager.get_cursor() as cursor:
            cursor.execute(
                'UPDATE "notifications" '
                'SET "read" = TRUE '
                'WHERE "userId" = %s AND "userType" = %s',
                (user_id, user_type)
            )
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print("Error marking all notifications read:", e)
        return jsonify({"status": "error", "message": str(e)}), 500


# [POST] /addOrUpdateNewsNotification
# PURPOSE: Add a new notification or update an existing one if it already exists        
@blueprint.route('/insertNews', methods=['POST'])
def upsert_news_notifications():
    """
    Expects JSON payload:
      {
        "userId": <int>,
        "userType": <str>,
        "articles": [
          {
            "title": <str>,
            "link": <str>,
            "image": <str>            # optional
          },
          ...
        ]
      }
    """
    data = request.get_json()
    user_id = data.get('userId')
    user_type = data.get('userType')
    articles = data.get('articles', [])

    if not user_id or not user_type or not isinstance(articles, list):
        return jsonify({'success': False, 'error': 'Missing userId, userType, or invalid articles format.'}), 400

    try:
        with db_manager.get_cursor() as cursor:
            for art in articles:
                title = art.get('title')
                link = art.get('link')
                image = art.get('image')  # may be None
                read = art.get('read')  
                published = art.get('published')  # optional, not used here

                if not title or not link or read == True:
                    continue  # skip invalid entries
                

                # 1) Check existence by (userId, userType, link)
                cursor.execute(
                    '''
                    SELECT id
                      FROM "notifications"
                     WHERE "userId" = %s
                       AND "userType" = %s
                       AND "link" = %s
                    ''',
                    (user_id, user_type, link)
                )
                row = cursor.fetchone()
                

                if row:
                    # 2a) If exists, UPDATE the message/image/createdAt
                    notif_id = row['id']

                    cursor.execute(
                        '''
                        UPDATE "notifications"
                           SET "message"   = %s,
                               "image"     = %s,
                               "createdAt" = to_timestamp(%s::double precision / 1000.0)
                         WHERE "id" = %s
                        ''',
                        (title, image, published, notif_id)
                    )

                else:

                    # 2b) If not exists, INSERT a new record
                    cursor.execute(
                        '''
                        INSERT INTO "notifications"
                          ("userId", "userType", "notiTabs", "notiType", "image", "link", "message", "createdAt", "read")
                        VALUES
                          (%s,       %s,         %s,        %s,         %s,      %s,     %s, to_timestamp(%s::double precision / 1000.0), %s)
                        ''',
                        (
                            user_id,
                            user_type,
                            'news',     # notiTabs = 'news'
                            'news',     # notiType = 'news'
                            image,
                            link,
                            title,
                            published,
                            'false'
                        )
                    )

        return jsonify({'success': True}), 200

    except Exception as e:
        print("Error in upsert_news_notifications:", str(e))
        return jsonify({'success': False, 'error': str(e)}), 500
        
                
