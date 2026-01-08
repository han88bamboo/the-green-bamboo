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
        
                
