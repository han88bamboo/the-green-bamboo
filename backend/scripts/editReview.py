# Port: 5022
# Routes: /voteReview (POST), /updateReview/<id> (PUT), /voteProducerReview (POST), /updateProducerReview/<id> (PUT)
# -----------------------------------------------------------------------------------------

import os
import s3Images
from flask import Blueprint, g, request, jsonify
from bson.objectid import ObjectId
from datetime import datetime
import json

from scripts.adminFunctions import hash_password
from scripts.createReview import create_username

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

# -----------------------------------------------------------------------------------------
# [POST] Vote review
# - Update review with new votes
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/voteReview', methods=['POST'])
def voteReview():
    conn = g.db
    data = request.get_json()

    review_id = data['reviewID']
    user_id = data['userID']
    action = data['action']
    current_time = data.get('voteDate', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    with conn.cursor() as cur:
        try:
            cur.execute("SELECT id, upvotes, downvotes FROM \"reviewsUserVotes\" WHERE \"reviewId\" = %s", (review_id,))
            result = cur.fetchone()

            upvotes = result['upvotes'] if result else []
            downvotes = result['downvotes'] if result else []

            # Convert JSONB to Python lists
            upvotes = json.loads(upvotes) if isinstance(upvotes, str) else upvotes
            downvotes = json.loads(downvotes) if isinstance(downvotes, str) else downvotes

            if action == "upvote":
                upvotes.append({"userId": user_id, "date": current_time})
                downvotes = [vote for vote in downvotes if vote['userId'] != user_id]

            elif action == "downvote":
                downvotes.append({"userId": user_id, "date": current_time})
                upvotes = [vote for vote in upvotes if vote['userId'] != user_id]

            elif action == "unupvote":
                upvotes = [vote for vote in upvotes if vote['userId'] != user_id]

            elif action == "undownvote":
                downvotes = [vote for vote in downvotes if vote['userId'] != user_id]

            if result:
                cur.execute("""
                    UPDATE "reviewsUserVotes"
                    SET upvotes = %s, downvotes = %s
                    WHERE id = %s;
                """, (json.dumps(upvotes), json.dumps(downvotes), result['id']))
            else:
                cur.execute("""
                    INSERT INTO "reviewsUserVotes" ("reviewId", upvotes, downvotes)
                    VALUES (%s, %s, %s);
                """, (review_id, json.dumps(upvotes), json.dumps(downvotes)))

            conn.commit()

            return jsonify({
                "code": 201,
                "data": {
                    "upvotes": upvotes,
                    "downvotes": downvotes
                }
            }), 201

        except Exception as e:
            print(str(e))
            conn.rollback()
            return jsonify({
                "code": 500,
                "message": "An error occurred updating the votes.",
                "details": str(e)
            }), 500

# -----------------------------------------------------------------------------------------
    
# [PUT] Update review
# - Update review with review metrics
# - Possible return codes: 200 (Updated), 400(Review not found), 500 (Error during update)
@blueprint.route('/updateReview/<id>', methods=['PUT'])
def updateReview(id):
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()

    # Parse the date from the request body
    try:
        created_date = datetime.strptime(data.get('createdDate', ''), "%a, %d %b %Y %H:%M:%S %Z")
    except ValueError:
        return jsonify({
            "code": 400,
            "message": "Invalid date format."
        }), 400

    # Check if review exists
    cur.execute("""
        SELECT * FROM "reviews" WHERE "id" = %s
    """, (id,))
    existing_review = cur.fetchone()

    if existing_review is None:
        return jsonify({
            "code": 400,
            "data": {
                "reviewDesc": data.get('reviewDesc', '')
            },
            "message": "Review does not exist."
        }), 400
    
    # Get proof points from pointSystemRules (id 2 to 6)
    cur.execute("""SELECT * FROM "pointSystemRules" WHERE "id" BETWEEN 2 AND 6""")
    point_system_rules = cur.fetchall()

    # Check the difference between the new review and the existing review
    remove_component = []
    added_component = []
    # [1] Check if text review was removed
    if not data.get('reviewDesc') and existing_review['reviewDesc']:
        remove_component.append(2)
    elif data.get('reviewDesc') and not existing_review['reviewDesc']:
        added_component.append(2)

    # [2] Check if extensive review was removed or added
    if not data.get('reviewType') and existing_review['reviewType']:
        remove_component.append(3)
    elif data.get('reviewType') and not existing_review['reviewType']:
        added_component.append(3)

    # [3] Check if photo was removed or added
    if not data.get('photo') and existing_review['photo']:
        remove_component.append(4)
    elif data.get('photo') and not existing_review['photo']:
        added_component.append(4)

    # [4] Check if location was removed or added
    if not data.get('location') and existing_review['location']:
        remove_component.append(5)
    elif data.get('location') and not existing_review['location']:
        added_component.append(5)

    # [5] Check if tagged users were removed or added
    if not data.get('taggedUsers') and existing_review['taggedUsers']:
        remove_component.append(6)
    elif data.get('taggedUsers') and not existing_review['taggedUsers']:
        added_component.append(6)

    # Insert or find the venue
    venue_id = None
    location_name = data.get('location')
    address = data.get('address')

    if location_name and address:
        cur.execute("""
            SELECT "id" FROM "venues" WHERE "venueName" = %s AND "address" = %s
        """, (location_name, address))
        venue_id = cur.fetchone()['id'] if cur.rowcount > 0 else None

        if not venue_id:
            username = create_username(location_name)
            insert_venue_sql = """INSERT INTO venues ("venueName", "address", "venueType", "originLocation", "venueDesc",
                                  "hashedPassword", "claimStatus", photo, "reservationDetails", username)
                                  VALUES (%s, %s, '', '', '', %s, FALSE, '', '', %s) RETURNING id"""
            hashed_password = 'hashed_password'  # Replace with actual password hashing logic
            cur.execute(insert_venue_sql, (location_name, address, hashed_password, username))
            venue_id = cur.fetchone()['id'] if cur.rowcount > 0 else None
            print("Venue ID: ", venue_id)
            conn.commit()

    # Update review photo
    if existing_review['photo']:
        s3Images.deleteImageFromS3(existing_review['photo'])
    if data['photo']:
        data['photo'] = s3Images.uploadBase64ImageToS3(data['photo'])

    tagged_users = data.get('taggedUsers', [])
    flavour_tags = data.get('flavourTag', [])
    observation_tags = data.get('observationTag', [])

    update_review_sql = """
        UPDATE "reviews"
        SET "userID" = %s, "reviewTarget" = %s, "rating" = %s, "reviewDesc" = %s, "reviewType" = %s, "createdDate" = %s,
            "language" = %s, "finish" = %s, "willRecommend" = %s, "wouldBuyAgain" = %s, "taggedUsers" = %s, "flavourTag" = %s,
            "photo" = %s, "colour" = %s, "aroma" = %s, "taste" = %s, "observationTag" = %s, "location" = %s, "address" = %s
        WHERE "id" = %s
    """

    review_values = (
        data.get('userID'), data.get('reviewTarget'), float(data.get('rating', 0.0)), data.get('reviewDesc'),
        data.get('reviewType'), created_date,
        data.get('language'), data.get('finish'), data.get('willRecommend', False), data.get('wouldBuyAgain', False),
        tagged_users, flavour_tags, data.get('photo'), data.get('colour'), data.get('aroma'), data.get('taste'),
        observation_tags, venue_id, address, id
    )

    try:
        cur.execute(update_review_sql, review_values)
        conn.commit()

        # Update user points 
        modify_point = 0
        if remove_component or added_component:
            for rule in point_system_rules:
                if rule['id'] in remove_component:
                    modify_point -= rule['points']
                elif rule['id'] in added_component:
                    modify_point += rule['points']

            cur.execute("""
                UPDATE "pointsRecorder"
                SET "currentPoints" = "currentPoints" + %s
                WHERE "id" = %s
            """, (modify_point, data.get('userID')))
            conn.commit()

        return jsonify({
            "code": 200,
            "data": data.get('reviewDesc', '')
        }), 200

    except Exception as e:
        print(str(e))
        return jsonify({
            "code": 500,
            "data": {
                "reviewDesc": data.get('reviewDesc', '')
            },
            "message": "An error occurred updating the review."
        }), 500
    
# -----------------------------------------------------------------------------------------

# [POST] Vote producer review
# - Update producer review with new votes
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/voteProducerReview', methods=['POST'])
def voteProducerReview():
    conn = g.db
    data = request.get_json()

    review_id = data['reviewID']
    user_votes = data['userVotes']
    action = data['action']

    with conn.cursor() as cur:
        try:
            cur.execute("SELECT id, upvotes, downvotes FROM \"producerReviewsUserVotes\" WHERE \"reviewId\" = %s", (review_id,))
            result = cur.fetchone()
            print("Result: ", result)

            if result:
                cur.execute("""
                    UPDATE "producerReviewsUserVotes"
                    SET upvotes = %s, downvotes = %s
                    WHERE id = %s;
                """, (user_votes['upvotes'], user_votes['downvotes'], result['id']))

            else:
                cur.execute("""
                    INSERT INTO "producerReviewsUserVotes" ("reviewId", upvotes, downvotes)
                    VALUES (%s, %s, %s);
                """, (review_id, user_votes['upvotes'], user_votes['downvotes']))

            conn.commit()

            return jsonify({
                "code": 201,
                "data": {
                    "upvotes": current_upvotes if 'current_upvotes' in locals() else user_votes['upvotes'],
                    "downvotes": current_downvotes if 'current_downvotes' in locals() else user_votes['downvotes']
                }
            }), 201
        
        except Exception as e:
            print(str(e))
            conn.rollback()
            return jsonify({
                "code": 500,
                "message": "An error occurred updating the votes.",
                "details": str(e)
            }), 500
        
# -----------------------------------------------------------------------------------------

# [PUT] Update producer review
# - Update producer review with review metrics
# - Possible return codes: 200 (Updated), 400(Review not found), 500 (Error during update)
@blueprint.route('/updateProducerReview/<id>', methods=['PUT'])
def updateProducerReview(id):
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()

    try:
        created_date = datetime.strptime(data.get('createdDate', ''), "%a, %d %b %Y %H:%M:%S %Z")
    except ValueError:
        return jsonify({"code": 400, "message": "Invalid date format."}), 400

    # Check if review exists
    cur.execute("""SELECT EXISTS(SELECT 1 FROM "producerReviews" WHERE id = %s)""", (id,))

    if not cur.fetchone()['exists']:
        return jsonify({"code": 400, "message": "Review does not exist."}), 400
    
    cur.execute("""SELECT photos FROM "producerReviews" WHERE id = %s""", (id,))
    old_photos = cur.fetchone()['photos'] or []
    
    from threading import Thread
    def async_delete_images(photo_list):
        for photo in photo_list:
            s3Images.deleteImageFromS3(photo)

    Thread(target=async_delete_images, args=(old_photos,)).start()


    new_photos = [s3Images.uploadBase64ImageToS3(photo) for photo in data.get('photos', []) if photo]

    update_review_sql = """
        UPDATE "producerReviews"
        SET "userID" = %s, "producerID" = %s, "rating" = %s, "reviewDesc" = %s, "createdDate" = %s, "photos" = %s
        WHERE "id" = %s
    """
    
    review_values = (
        data.get('userID'), data.get('producerID'), float(data.get('rating', 0.0)), data.get('reviewDesc'),
        created_date, new_photos, id
    )

    # Get the existing review 
    cur.execute("""SELECT * FROM "producerReviews" WHERE id = %s""", (id,))
    existing_review = cur.fetchone()

    # Get proof points from pointSystemRules (id 2 and 4)
    cur.execute("""SELECT * FROM "pointSystemRules" WHERE "id" IN (2, 4)""")
    point_system_rules = cur.fetchall()

    # Check the difference between the new review and the existing review
    remove_component = []
    added_component = []

    # [1] Check if text review was removed
    if not data.get('reviewDesc') and existing_review['reviewDesc']:
        remove_component.append(2)
    elif data.get('reviewDesc') and not existing_review['reviewDesc']:
        added_component.append(2)

    # [2] Check if photo was removed or added  
    if not data.get('photos') and existing_review['photos']:
        remove_component.append(4)
    elif data.get('photos') and not existing_review['photos']:
        added_component.append(4)

    try:
        cur.execute(update_review_sql, review_values)
        conn.commit()

        # Update user points
        modify_point = 0
        if remove_component or added_component:
            for rule in point_system_rules:
                if rule['id'] in remove_component:
                    modify_point -= rule['points']
                elif rule['id'] in added_component:
                    modify_point += rule['points']

            cur.execute("""
                UPDATE "pointsRecorder"
                SET "currentPoints" = "currentPoints" + %s
                WHERE "id" = %s
            """, (modify_point, data.get('userID')))
            conn.commit()

        return jsonify({"code": 200, "data": data.get('reviewDesc', '')}), 200

    except Exception as e:
        print(str(e))
        return jsonify({"code": 500, "message": "An error occurred updating the review."}), 500