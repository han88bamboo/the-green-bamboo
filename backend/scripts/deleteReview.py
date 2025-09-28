# Port: 5023
# Routes: /deleteReview/<id> (DELETE), /deleteProducerReview/<id> (DELETE) , /deleteVenueReview/<id> (DELETE)
# -----------------------------------------------------------------------------------------

# [OLD] TO BE DELETED FOR POSTGRES:
# ------------------------------------------------------


# ======================================================

# [NEW] TO BE ADDED FOR POSTGRES:
# ------------------------------------------------------


# ======================================================
import os
import s3Images
import json
from flask import Blueprint, g, request, jsonify
# [OLD] TO BE DELETED FOR POSTGRES:
# ------------------------------------------------------
from bson import json_util
from bson.objectid import ObjectId
# ======================================================

# [NEW] TO BE ADDED FOR POSTGRES:
# ------------------------------------------------------
# import psycopg2
# from psycopg2.extras import RealDictCursor
# ======================================================


file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)


# [OLD] TO BE DELETED FOR POSTGRES:
# ------------------------------------------------------
def parse_json(data):
    return json.loads(json_util.dumps(data))
# ======================================================

# -----------------------------------------------------------------------------------------
# [DELETE] Deletes a review
# - Delete entry with specified id from the "reviews" collection.
# - Possible return codes: 201 (Deleted), 400 (Review doesn't exist), 500 (Error during deletion)


@blueprint.route("/deleteReview/<id>", methods=['DELETE'])
def deleteReview(id):
    conn = g.db
    cur = conn.cursor()

    cur.execute("SELECT * FROM reviews WHERE id = %s", (id,))
    existingReview = cur.fetchone()

    if existingReview is None:
        return jsonify(
            {   
                "code": 400,
                "data": {
                    "id": id
                },
                "message": "Review doesn't exist."
            }
        ), 400
    
    # Get review details
    user_id = existingReview['userID']
    review_target = existingReview['reviewTarget']
    
    # Get the total points earned for the review
    rule_points_id = []

    # Review text
    if (existingReview['reviewDesc'] != None or existingReview['reviewDesc'] != ''):
        rule_points_id.append(2)

    # Extended review: color, aroma, taste, finish
    is_extensive_review = False
    if (existingReview['finish'] != None or existingReview['colour'] != None or existingReview['aroma'] != None or existingReview['taste'] != None) and \
        (existingReview['finish'] != '' or existingReview['colour'] != '' or existingReview['aroma'] != '' or existingReview['taste'] != ''):
        rule_points_id.append(3)
        is_extensive_review = True

    # Attach image
    has_photo = False
    if (existingReview['photo'] != None and existingReview['photo'] != ''):
        rule_points_id.append(4)
        has_photo = True

    # Tag location
    has_location = False
    if (existingReview['location'] != None and existingReview['location'] != ''):
        rule_points_id.append(5)
        has_location = True

    # Tag friends
    has_tagged_friends = False
    if existingReview['taggedUsers']:
        rule_points_id.append(6)
        has_tagged_friends = True

    # Get total proof points earned
    cur.execute('SELECT SUM("proofPoints") FROM "pointSystemRules" WHERE id IN %s', (tuple(rule_points_id),))
    total_points = cur.fetchone()['sum']

    try:
        # Get listing information for badge recalculation
        cur.execute("""
            SELECT "drinkType", "typeCategory", "originCountry" 
            FROM "listings" 
            WHERE id = %s
        """, (review_target,))
        
        listing_info = cur.fetchone()

        badge_triggers = []
        affected_badge_ids = []
        
        if listing_info:
            drink_type = listing_info['drinkType']
            type_category = listing_info['typeCategory']
            origin_country = listing_info['originCountry']

            if origin_country:
                badge_triggers.append({
                    'actionType': 'Review',
                    'mappingType': 'Country',
                    'primaryValue': origin_country,
                    'secondaryValue': None
                })
            
            if drink_type:
                badge_triggers.append({
                    'actionType': 'Review',
                    'mappingType': 'DrinkType',
                    'primaryValue': drink_type,
                    'secondaryValue': None
                })
            
            if drink_type and type_category:
                badge_triggers.append({
                    'actionType': 'Review',
                    'mappingType': 'Category',
                    'primaryValue': drink_type,
                    'secondaryValue': type_category
                })
            
            # Action badge triggers
            if is_extensive_review:
                badge_triggers.append({
                    'actionType': 'ExtensiveReview',
                    'mappingType': 'Action',
                    'primaryValue': 'ExtensiveReview',
                    'secondaryValue': None
                })
                
            if has_photo:
                badge_triggers.append({
                    'actionType': 'PhotoAttached',
                    'mappingType': 'Action', 
                    'primaryValue': 'PhotoAttached',
                    'secondaryValue': None
                })
                
            if has_location:
                badge_triggers.append({
                    'actionType': 'LocationTagged',
                    'mappingType': 'Action',
                    'primaryValue': 'LocationTagged',
                    'secondaryValue': None
                })
                
            if has_tagged_friends:
                badge_triggers.append({
                    'actionType': 'FriendTagged',
                    'mappingType': 'Action',
                    'primaryValue': 'FriendTagged',
                    'secondaryValue': None
                })
            
            # Find all badge IDs affected by this review
            for trigger in badge_triggers:
                action_type = trigger['actionType']
                mapping_type = trigger['mappingType']
                primary_value = trigger['primaryValue']
                secondary_value = trigger.get('secondaryValue')
                
                if mapping_type == 'Action':
                    # For action badges, we check relatedEntity
                    cur.execute("""
                        SELECT id FROM "badges" 
                        WHERE "badgeType" = 'Action' AND "relatedEntity" = %s
                    """, (primary_value,))
                else:
                    # For other badges, we check the mappings table
                    if secondary_value:
                        # Category badge (with secondary value)
                        cur.execute("""
                            SELECT b.id FROM "badges" b
                            JOIN "badgeMappings" bm ON b.id = bm."badgeId"
                            WHERE bm."mappingType" = %s 
                            AND LOWER(bm."primaryValue") = LOWER(%s) 
                            AND LOWER(bm."secondaryValue") = LOWER(%s)
                        """, (mapping_type, primary_value, secondary_value))
                    else:
                        # Country or DrinkType badge (no secondary value)
                        cur.execute("""
                            SELECT b.id FROM "badges" b
                            JOIN "badgeMappings" bm ON b.id = bm."badgeId"
                            WHERE bm."mappingType" = %s 
                            AND LOWER(bm."primaryValue") = LOWER(%s) 
                            AND (bm."secondaryValue" IS NULL OR bm."secondaryValue" = '')
                        """, (mapping_type, primary_value))
                
                badge_rows = cur.fetchall()
                for row in badge_rows:
                    affected_badge_ids.append({
                        'badgeId': row['id'],
                        'actionType': action_type,
                        'mappingType': mapping_type,
                        'primaryValue': primary_value,
                        'secondaryValue': secondary_value
                    })

        # If there's a photo, delete it from S3
        if(existingReview['photo']):
            s3Images.deleteImageFromS3(existingReview['photo'])

        # Delete associated votes
        cur.execute("DELETE FROM \"reviewsUserVotes\" WHERE \"reviewId\" = %s", (id,))

        # Delete the review - we need to do this NOW before counting remaining reviews
        cur.execute("DELETE FROM reviews WHERE id = %s", (id,))
        
        # Commit this deletion immediately to ensure it's reflected in our count queries
        conn.commit()

        # Update user points
        if total_points:
            cur.execute('UPDATE "pointsRecorder" SET "currentPoints" = "currentPoints" - %s WHERE "userID" = %s AND "userType" = %s', 
                       (total_points, user_id, 'user',))
            conn.commit()

        # ======== BADGE RECALCULATION ========
        badges_affected = []
        
        for badge_info in affected_badge_ids:
            badge_id = badge_info['badgeId']
            action_type = badge_info['actionType']
            mapping_type = badge_info['mappingType']
            primary_value = badge_info['primaryValue']
            secondary_value = badge_info.get('secondaryValue')
            
            # Get current badge status
            cur.execute("""
                SELECT "currentLevel", "currentProgress"
                FROM "userBadges"
                WHERE "userId" = %s AND "badgeId" = %s
            """, (user_id, badge_id))
            
            user_badge = cur.fetchone()
            
            if user_badge:
                current_level = user_badge['currentLevel']
                current_progress = user_badge['currentProgress']
                
                total_actions = 0 
                
                if action_type == 'Review':
                    # For Review badges (Country, DrinkType, Category)
                    if mapping_type == 'Country':
                        cur.execute("""
                            SELECT COUNT(*) as total FROM reviews r
                            JOIN listings l ON r."reviewTarget" = l.id
                            WHERE r."userID" = %s AND LOWER(l."originCountry") = LOWER(%s)
                        """, (user_id, primary_value))
                    elif mapping_type == 'DrinkType':
                        cur.execute("""
                            SELECT COUNT(*) as total FROM reviews r
                            JOIN listings l ON r."reviewTarget" = l.id
                            WHERE r."userID" = %s AND LOWER(l."drinkType") = LOWER(%s)
                        """, (user_id, primary_value))
                    elif mapping_type == 'Category':
                        cur.execute("""
                            SELECT COUNT(*) as total FROM reviews r
                            JOIN listings l ON r."reviewTarget" = l.id
                            WHERE r."userID" = %s AND LOWER(l."drinkType") = LOWER(%s) AND LOWER(l."typeCategory") = LOWER(%s)
                        """, (user_id, primary_value, secondary_value))
                else:
                    # For action badges, count reviews with specific features
                    if action_type == 'ExtensiveReview':
                        cur.execute("""
                            SELECT COUNT(*) as total FROM reviews
                            WHERE "userID" = %s AND 
                            ((finish IS NOT NULL AND finish != '') OR 
                             (colour IS NOT NULL AND colour != '') OR 
                             (aroma IS NOT NULL AND aroma != '') OR 
                             (taste IS NOT NULL AND taste != ''))
                        """, (user_id,))
                    elif action_type == 'PhotoAttached':
                        cur.execute("""
                            SELECT COUNT(*) as total FROM reviews
                            WHERE "userID" = %s AND photo IS NOT NULL AND photo != ''
                        """, (user_id,))
                    elif action_type == 'LocationTagged':
                        cur.execute("""
                            SELECT COUNT(*) as total FROM reviews
                            WHERE "userID" = %s AND location IS NOT NULL
                        """, (user_id,))
                    elif action_type == 'FriendTagged':
                        cur.execute("""
                            SELECT COUNT(*) as total FROM reviews
                            WHERE "userID" = %s AND "taggedUsers" IS NOT NULL AND "taggedUsers" != '{}'
                        """, (user_id,))
                
                result = cur.fetchone()
                total_actions = result['total'] if result else 0
                
                print(f"Badge ID {badge_id}: Total remaining actions = {total_actions}")
                
                if total_actions == 0:
                    cur.execute("""
                        DELETE FROM "userBadges"
                        WHERE "userId" = %s AND "badgeId" = %s
                    """, (user_id, badge_id))
                    
                    badges_affected.append({
                        'badgeId': badge_id,
                        'removed': True
                    })
                    continue 

                if current_progress > 0:
                    # just reduce progress by 1
                    cur.execute("""
                        UPDATE "userBadges"
                        SET "currentProgress" = "currentProgress" - 1,
                            "lastUpdated" = CURRENT_TIMESTAMP
                        WHERE "userId" = %s AND "badgeId" = %s
                    """, (user_id, badge_id))
                    
                    badges_affected.append({
                        'badgeId': badge_id,
                        'levelChange': 0,
                        'newProgress': current_progress - 1
                    })
                else:
                    if current_level > 1:
                        # Calculate the correct level based on total actions
                        new_level = 1
                        accumulated_actions = 0
                        
                        cur.execute("""
                            SELECT "levelStart", "levelEnd", "actionsRequired"
                            FROM "badgeRules"
                            WHERE "actionType" = %s
                            ORDER BY "levelStart"
                        """, (action_type,))
                        
                        rules = cur.fetchall()
                        
                        for rule in rules:
                            level_start = rule['levelStart']
                            level_end = rule['levelEnd']
                            actions_required = rule['actionsRequired']
                            
                            for level in range(level_start, level_end + 1):
                                if accumulated_actions + actions_required > total_actions:
                                    new_level = level - 1 if level > 1 else 1
                                    break
                                accumulated_actions += actions_required
                            
                            if accumulated_actions >= total_actions:
                                break
                            
                        if accumulated_actions < total_actions and rules:
                            last_rule = rules[-1]
                            new_level = last_rule['levelEnd']
                        
                        # Update the badge level if it changed
                        if new_level < current_level:
                            remaining_actions = total_actions
                            new_progress = 0
                            
                            for rule in rules:
                                level_start = rule['levelStart']
                                level_end = rule['levelEnd']
                                actions_required = rule['actionsRequired']
                                
                                if new_level >= level_start and new_level <= level_end:
                                    for level in range(level_start, new_level):
                                        if remaining_actions >= actions_required:
                                            remaining_actions -= actions_required
                                        else:
                                            remaining_actions = 0
                                            break
                                    
                                    new_progress = remaining_actions
                                    break
                                else:
                                    levels_in_range = level_end - level_start + 1
                                    actions_in_range = levels_in_range * actions_required
                                    if remaining_actions >= actions_in_range:
                                        remaining_actions -= actions_in_range
                                    else:
                                        levels_complete = remaining_actions // actions_required
                                        new_level = level_start + levels_complete
                                        new_progress = remaining_actions % actions_required
                                        break
                            
                            cur.execute("""
                                UPDATE "userBadges"
                                SET "currentLevel" = %s,
                                    "currentProgress" = %s,
                                    "lastUpdated" = CURRENT_TIMESTAMP
                                WHERE "userId" = %s AND "badgeId" = %s
                            """, (new_level, new_progress, user_id, badge_id))
                            
                            badges_affected.append({
                                'badgeId': badge_id,
                                'levelChange': new_level - current_level,
                                'newLevel': new_level,
                                'newProgress': new_progress
                            })
                        else:
                            # Update to indicate the review was removed
                            badges_affected.append({
                                'badgeId': badge_id,
                                'levelChange': 0,
                                'newProgress': 0
                            })

        conn.commit()

        return jsonify(
            {   
                "code": 200,
                "data": id,
                "deductedPoints": total_points,
                "badgesAffected": badges_affected
            }
        ), 200

    except Exception as e:
        print(str(e))
        conn.rollback()
        return jsonify(
            {
                "code": 500,
                "data": {
                    "id": id
                },
                "message": "An error occurred deleting the review.",
                "error": str(e)
            }
        ), 500
    
# -----------------------------------------------------------------------------------------
# [DELETE] Deletes a producer review
# - Delete entry with specified id from the "producerReviews" collection.
# - Possible return codes: 201 (Deleted), 400 (Review doesn't exist), 500 (Error during deletion)
@blueprint.route("/deleteProducerReview/<id>", methods=['DELETE'])
def deleteProducerReview(id):
    conn = g.db
    cur = conn.cursor()

    cur.execute("""SELECT EXISTS(SELECT 1 FROM "producerReviews" WHERE id = %s)""", (id,))
    exists = cur.fetchone()['exists']

    if not exists:
        return jsonify(
            {   
                "code": 400,
                "data": {"id": id},
                "message": "Review doesn't exist."
            }
        ), 400

    try:
        # Fetch the points for simple review
        cur.execute('SELECT "proofPoints" FROM "pointSystemRules" WHERE id = 2')
        points = cur.fetchone()['proofPoints']

        # Fetch only the photos instead of the entire review
        cur.execute("""SELECT "userID", photos FROM "producerReviews" WHERE id = %s""", (id,))
        results = cur.fetchone()
        photos = results['photos']
        userID = results['userID']

        if photos:

            # Get points for image upload
            cur.execute('SELECT "proofPoints" FROM "pointSystemRules" WHERE id = 4')
            points += cur.fetchone()['proofPoints']

            from threading import Thread
            def async_delete_images(photo_list):
                for photo in photo_list:
                    s3Images.deleteImageFromS3(photo)

            Thread(target=async_delete_images, args=(photos,)).start()

        cur.execute("DELETE FROM \"producerReviewsUserVotes\" WHERE \"reviewId\" = %s", (id,))
        cur.execute("DELETE FROM \"producerReviews\" WHERE id = %s RETURNING id", (id,))
        
        conn.commit()

        # Update user points
        cur.execute('UPDATE "pointsRecorder" SET "currentPoints" = "currentPoints" - %s WHERE "userID" = %s AND "userType" = %s', (points, userID, 'user',))
        conn.commit()

        print(f"Deducted {points} points from user {userID} for deleting review {id}.")

        return jsonify({"code": 200, "data": id}), 200

    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": {"id": id},
                "message": "An error occurred deleting the listing."
            }
        ), 500
    
# -----------------------------------------------------------------------------------------
# [DELETE] Deletes a venue review
# - Delete entry with specified id from the "venueReviews" collection.
# - Possible return codes: 200 (Deleted), 400 (Review doesn't exist), 500 (Error during deletion)
@blueprint.route("/deleteVenueReview/<id>", methods=['DELETE'])
def deleteVenueReview(id):
    conn = g.db
    cur = conn.cursor()

    cur.execute("""SELECT EXISTS(SELECT 1 FROM "venueReviews" WHERE id = %s)""", (id,))
    exists = cur.fetchone()['exists']

    if not exists:
        return jsonify(
            {
                "code": 400,
                "data": {"id": id},
                "message": "Review doesn't exist."
            }
        ), 400

    try:
        # Fetch only the photos instead of the entire review
        cur.execute("""SELECT photos FROM "venueReviews" WHERE id = %s""", (id,))
        photos = cur.fetchone()['photos']

        if photos:
            from threading import Thread
            def async_delete_images(photo_list):
                for photo in photo_list:
                    s3Images.deleteImageFromS3(photo)
            Thread(target=async_delete_images, args=(photos,)).start()

        cur.execute("DELETE FROM \"venueReviewsUserVotes\" WHERE \"reviewId\" = %s", (id,))
        cur.execute("DELETE FROM \"venueReviews\" WHERE id = %s RETURNING id", (id,))

        conn.commit()

        return jsonify({"code": 200, "data": id}), 200

    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": {"id": id},
                "message": "An error occurred deleting the review."
            }
        ), 500
