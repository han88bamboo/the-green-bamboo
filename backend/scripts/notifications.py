# Routes: 
#   /readNotifications [DELETE]
# -----------------------------------------------------------------------------------------

import os
from flask import Blueprint, g, jsonify, request
from psycopg2 import sql

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

# -----------------------------------------------------------------------------------------
# Helper function 
def add_notification_to_db(data):
    """
    Expects `data` to contain these keys (matching exactly the column names):
      - userId    [int]
      - userType  [str]
      - notiTabs  [str]
      - notiType  [str]
      - image     [str] (optional)
      - link      [str] (optional)
      - message   [str]
    We no longer pass `createdAt` explicitly, so the DB DEFAULT CURRENT_TIMESTAMP is used.
    """
    conn = g.db
    cursor = conn.cursor()

    try:
        cursor.execute(
            '''
            INSERT INTO "notifications"
                ("userId", "userType", "notiTabs", "notiType", "image", "link", "message")
            VALUES (%s,      %s,        %s,        %s,        %s,      %s,      %s)
            ''',
            (
                data.get('userId'),
                data.get('userType'),
                data.get('notiTabs'),
                data.get('notiType'),
                data.get('image'),   # may be None
                data.get('link'),    # may be None
                data.get('message')
            )
        )
        conn.commit()
        return True

    except Exception as e:
        # Log the actual exception for debugging
        print("add_notification_to_db error:", str(e))
        conn.rollback()
        return False

    finally:
        cursor.close()

# -----------------------------------------------------------------------------------------

# [DELETE] /readNotifications
# PURPOSE: Remove record from notifications table if user has read the notification
@blueprint.route('/readNotification', methods=['DELETE'])
def readNotification():
    """
    DELETE a notification by its ID. Used to mark it as read/remove it.
    """
    conn = g.db
    cur = conn.cursor()

    notification = request.get_json()
    notif_id = notification.get('id')
    notiType = notification.get('notiType')
    link = notification.get('link')
    
    
    try:
        if notiType == 'news':
            # If it's a news notification, we delete it from the "notifications" table
            cur.execute(
                'UPDATE "notifications" SET "read" = TRUE WHERE "id" = %s AND "notiType" = %s AND "link" = %s',
                (notif_id, notiType, link)
            )
        else:
            cur.execute(
                'DELETE FROM "notifications" WHERE id = %s',
                (notif_id,)
            )
        conn.commit()
        return jsonify({'success': True}), 200

    except Exception as e:
        print("Error deleting notification:", str(e))
        return jsonify({
            'success': False,
            'message': 'Error deleting notification.'
        }), 500

    finally:
        cur.close()

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

    conn = g.db
    cur = conn.cursor()
    try:
        for art in articles:
            title = art.get('title')
            link = art.get('link')
            image = art.get('image')  # may be None
            read = art.get('read')  
            published = art.get('published')  # optional, not used here

            if not title or not link or read == True:
                continue  # skip invalid entries
            

            # 1) Check existence by (userId, userType, link)
            cur.execute(
                '''
                SELECT id
                  FROM "notifications"
                 WHERE "userId" = %s
                   AND "userType" = %s
                   AND "link" = %s
                ''',
                (user_id, user_type, link)
            )
            row = cur.fetchone()
            

            if row:
                # 2a) If exists, UPDATE the message/image/createdAt
                notif_id = row['id']

                cur.execute(
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
                cur.execute(
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

        conn.commit()
        return jsonify({'success': True}), 200

    except Exception as e:
        print("Error in upsert_news_notifications:", str(e))
        conn.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

    finally:
        cur.close()        