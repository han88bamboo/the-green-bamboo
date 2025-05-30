# Routes: 
#   /readNotifications [DELETE]
# -----------------------------------------------------------------------------------------

import os
from flask import Blueprint, g, jsonify, request


file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

# -----------------------------------------------------------------------------------------
# Helper function 
def add_notification_to_db(data):
    # Date should include 
    # user_id [int],
    # user_type [str],
    # notification_type [str], "for you", "venues and producers", "news"
    # related_id [int], e.g., review id, comment id, club id, event id, qna id, etc.
    # followers [list of int], e.g., [1, 2, 3] for user ids
    # image [str], e.g., "https://example.com/image.jpg"
    # link [str],
    # message [str],

    conn = g.db
    cursor = conn.cursor()

    try:
        # If no followers
        cursor.execute(
            'INSERT INTO "notifications" ("userId", "userType", "notiType", "relatedId", followers, image, link, message) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
            (data['user_id'], data['user_type'], data['notification_type'], data['related_id'],
             data['followers'], data['image'], data['link'], data['message'])
        )
        conn.commit()
        return True
    except Exception as e:
        return False

# -----------------------------------------------------------------------------------------

# [DELETE] /readNotifications
# PURPOSE: Remove record from notifications table if user has read the notification
@blueprint.route('/readNotifications', methods=['DELETE'])
def read_notifications():
    data = request.get_json()

    if not data or 'user_id' not in data or 'notification_id' not in data:
        return jsonify({'error': 'Invalid request'}), 400

    conn = g.db
    cursor = conn.cursor()

    try:
        cursor.execute(
            'DELETE FROM "notifications" WHERE "userId" = %s AND "id" = %s',
            (data['user_id'], data['notification_id'])
        )
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({'message': 'No notification found for the given user.'}), 404

        return jsonify({'message': 'Notification marked as read.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
