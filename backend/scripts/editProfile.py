# Port: 5100
# Routes: /editDetails (POST), /updateBookmark (POST), /updateFollowLists (POST), /updateModType (POST), /removeModType (POST)
# -----------------------------------------------------------------------------------------

import os
import s3Images
from flask import Blueprint, g, request, jsonify
from scripts import pointsHelperFunc, badge_helpers, notifications
from datetime import datetime
import re

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

# -----------------------------------------------------------------------------------------
# [POST] Edit user profile
# - Update user profile with new details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/editDetails', methods=['POST'])
def editDetails():
    conn = g.db
    data = request.get_json()
    userID = data['userID']
    cursor = conn.cursor()
    try:
        if 'image64' in data:
            cursor.execute("SELECT photo FROM users WHERE id = %s", (userID,))
            existingUser = cursor.fetchone()
            if existingUser and existingUser['photo']:
                s3Images.deleteImageFromS3(existingUser['photo'])
            base64_string = re.sub(r'^data:image\/[a-zA-Z]+;base64,', '', data['image64'])
            image64 = s3Images.uploadBase64ImageToS3(base64_string)

            cursor.execute("UPDATE users SET photo = %s WHERE id = %s", (image64, userID))
        drinkChoice = data['drinkChoice']
        cursor.execute("UPDATE users SET \"choiceDrinks\" = %s WHERE id = %s", (drinkChoice, userID))
        # retrieve the updated flavour tags from frontend -- ADDED IN BY  SMU GROUP 3
        flavourTag = data['flavourTag']
        # update the database with the new flavour tags -- ADDED IN BY  SMU GROUP 3
        cursor.execute("UPDATE users SET \"choiceFlavours\" = %s WHERE id = %s", (flavourTag, userID))
        
        # retrieve the updated obeservation tags from frontend -- ADDED IN BY  SMU GROUP 3
        observationTags = data['observationTags']
        # update the database with the new observation tags -- ADDED IN BY  SMU GROUP 3
        cursor.execute("UPDATE users SET \"preferences\" = %s WHERE id = %s", (observationTags, userID))
        
        conn.commit()
        return jsonify(
            {   
                "code": 201,
                "data": {
                    "userID": userID,
                    "drinkChoice": drinkChoice,
                    "flavourTag": flavourTag,
                    "observationTags": observationTags
                }
            }
        ), 201

    except Exception as e:
        conn.rollback()
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": {
                    "userID": userID,
                    "drinkChoice": data["drinkChoice"],
                    "flavourTag": data["flavourTag"],
                    "observationTags": data["observationTags"]
                },
                "message": "An error occurred updating the image or drink choice."
            }
        ), 500
    
    finally:
        cursor.close()

# -----------------------------------------------------------------------------------------
# [POST] Update user producer bookmark
# - Update user producer bookmark with new details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/updateProducerBookmark', methods=['POST'])
def updateProducerBookmark():
    conn = g.db
    data = request.get_json()
    userID = int(data['userID'])
    bookmark = data['bookmark']

    try:
        cursor = conn.cursor()

        # Fetch existing producer lists for the user
        cursor.execute('SELECT "id", "listName" FROM "userProducerLists" WHERE "userId" = %s', (userID,))
        existing_lists = {row['listName']: row['id'] for row in cursor.fetchall()}

        bookmark_list_names = set(bookmark.keys())
        existing_list_names = set(existing_lists.keys())

        # Identify lists to delete (if not in new bookmark)
        lists_to_delete = existing_list_names - bookmark_list_names
        for listName in lists_to_delete:
            cursor.execute('DELETE FROM "userProducerLists" WHERE "userId" = %s AND "listName" = %s', (userID, listName))

        for listName, listData in bookmark.items():
            listItems = listData["listItems"]

            # If list exists, use its ID; otherwise, create a new one
            if listName in existing_lists:
                list_id = existing_lists[listName]

                # Update existing list desc
                cursor.execute(
                    'UPDATE "userProducerLists" SET "listDesc" = %s WHERE "id" = %s',
                    (listData["listDesc"], list_id)
                )
            else:
                cursor.execute(
                    'INSERT INTO "userProducerLists" ("userId", "listName", "listDesc") VALUES (%s, %s, %s) RETURNING "id"',
                    (userID, listName, listData["listDesc"],)
                )
                list_id = cursor.fetchone()["id"]

            # Delete existing items in the list (to avoid duplicates)
            cursor.execute('DELETE FROM "userProducerListItems" WHERE "listId" = %s', (list_id,))

            # Insert new producers with their addedDate, using NOW() if missing
            for item in listItems:
                added_date = item.get("addedDate", None)  # Get addedDate, default to None
                if added_date:
                    cursor.execute(
                        'INSERT INTO "userProducerListItems" ("listId", "producerId", "addedDate") VALUES (%s, %s, %s)',
                        (list_id, item["producerId"], added_date)
                    )
                else:
                    cursor.execute(
                        'INSERT INTO "userProducerListItems" ("listId", "producerId", "addedDate") VALUES (%s, %s, NOW())',
                        (list_id, item["producerId"])
                    )

        conn.commit()
        cursor.close()
        return jsonify(
            {
                "code": 201,
                "data": {
                    "userID": userID,
                    "bookmark": bookmark
                }
            }
        ), 201

    except Exception as e:
        print("Update producer bookmark error:", str(e))
        conn.rollback()
        return jsonify({
            "code": 500,
            "data": {
                "userID": userID,
                "bookmark": bookmark
            },
            "message": "An error occurred updating the producer lists."
        }), 500
    
# -----------------------------------------------------------------------------------------
# [POST] Update user bookmark
# - Update user bookmark with new details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/updateBookmark', methods=['POST'])
def updateBookmark():
    conn = g.db
    data = request.get_json()
    userID = int(data['userID'])
    bookmark = data['bookmark']

    try:
        cursor = conn.cursor()

        # Fetch existing drink lists for the user
        cursor.execute('SELECT "id", "listName" FROM "usersDrinkLists" WHERE "userId" = %s', (userID,))
        existing_lists = {row['listName']: row['id'] for row in cursor.fetchall()}

        bookmark_list_names = set(bookmark.keys())
        existing_list_names = set(existing_lists.keys())

        # Counter to track the number of lists to delete
        num_lists_to_delete_count = 0

        # Counter to track the number of lists to add
        num_lists_to_add_count = 0

        # Identify lists to delete (if not in new bookmark)
        lists_to_delete = existing_list_names - bookmark_list_names
        for listName in lists_to_delete:
            cursor.execute('DELETE FROM "usersDrinkLists" WHERE "userId" = %s AND "listName" = %s', (userID, listName))
            num_lists_to_delete_count += 1

        for listName, listData in bookmark.items():
            listItems = listData["listItems"]

            # If list exists, use its ID; otherwise, create a new one
            if listName in existing_lists:
                list_id = existing_lists[listName]

                # Update existing list desc
                cursor.execute(
                    'UPDATE "usersDrinkLists" SET "listDesc" = %s WHERE "id" = %s',
                    (listData["listDesc"], list_id)
                )
            else:
                cursor.execute(
                    'INSERT INTO "usersDrinkLists" ("userId", "listName", "listDesc") VALUES (%s, %s, %s) RETURNING "id"',
                    (userID, listName, listData["listDesc"],)
                )
                list_id = cursor.fetchone()["id"]
                num_lists_to_add_count += 1

            # Delete existing items in the list (to avoid duplicates)
            cursor.execute('DELETE FROM "usersDrinkListItems" WHERE "listId" = %s', (list_id,))

            # Insert new drinks with their addedDate, using NOW() if missing
            for item in listItems:
                added_date = item.get("addedDate", None)  # Get addedDate, default to None
                if added_date:
                    cursor.execute(
                        'INSERT INTO "usersDrinkListItems" ("listId", "drinkId", "addedDate") VALUES (%s, %s, %s)',
                        (list_id, item["drinkId"], added_date)
                    )
                else:
                    cursor.execute(
                        'INSERT INTO "usersDrinkListItems" ("listId", "drinkId", "addedDate") VALUES (%s, %s, NOW())',
                        (list_id, item["drinkId"])
                    )

        conn.commit()

        # Initialize variables for points and badge processing
        points_earned = 0
        badge_result = None

        # Update proofPoints and process badges
        if (num_lists_to_delete_count > 0 or num_lists_to_add_count > 0) and (num_lists_to_delete_count - num_lists_to_add_count) != 0:
            
            # Get the proofPoints for creating a new list
            cursor.execute('SELECT "proofPoints" FROM "pointSystemRules" WHERE "id" = 14')
            proofPoints = cursor.fetchone()

            if proofPoints:
                # Calculate net points earned
                points_earned = (num_lists_to_add_count - num_lists_to_delete_count) * proofPoints['proofPoints']

                # Only award points if positive and user hasn't reached max
                if points_earned > 0:
                    if pointsHelperFunc.check_max_proof_points(userID):
                        return jsonify({
                            "code": 201,
                            "data": {
                                "userID": userID,
                                "bookmark": bookmark
                            },
                            "message": "Max points reached."
                        }), 201

                # Update user points (can be positive or negative)
                cursor.execute('UPDATE "pointsRecorder" SET "currentPoints" = "currentPoints" + %s WHERE "userID" = %s AND "userType" = %s', 
                               (points_earned, userID, 'user'))
                conn.commit()

                print(f"User {userID} earned {points_earned} points for editing the number of lists.")
            
            # Process PublicList badge based on net list changes
            net_list_change = num_lists_to_add_count - num_lists_to_delete_count
            if net_list_change != 0:
                badge_result = badge_helpers.process_public_list_badge(conn, cursor, userID, net_list_change)

        cursor.execute('SELECT username FROM users WHERE id = %s', (userID,))
        user_row = cursor.fetchone()
        if user_row:
            # Get the username of the user
            user_username = user_row['username'] if user_row else "Someone"
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
        # Notify if badge earned
        if badge_result:
            notification_data = {
                "userId":   userID,
                "userType": "user",
                "notiTabs": "forYou",
                "notiType": "badge_earned",
                "image":    None,
                "link":     f"/profile/user/{userID}/{user_username}",
                "message":  f"Congratulations! You earned a badge: {badge_result['badgeName']}.",
                "createdAt": current_time
            }
            print("Notification data:", notification_data)
            notifications.add_notification_to_db(notification_data)

        # Prepare the response
        response_data = {
            "code": 201,
            "data": {
                "userID": userID,
                "bookmark": bookmark
            }
        }
        
        if points_earned != 0:
            response_data["pointsEarned"] = points_earned
            
        if badge_result:
            response_data["badgeAwarded"] = badge_result

        cursor.close()
        return jsonify(response_data), 201

    except Exception as e:
        print("Update bookmark error:", str(e))
        conn.rollback()
        return jsonify({
            "code": 500,
            "data": {
                "userID": userID,
                "bookmark": bookmark
            },
            "message": "An error occurred updating the drink lists."
        }), 500

# -----------------------------------------------------------------------------------------
# [POST] Update follow lists
# - Update user follow lists with new details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/updateFollowLists', methods=['POST'])
def updateFollowList():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()

    userID = int(data['userID'])
    action = data['action']
    target = data['target']
    followerID = int(data['followerID'])

    try:
        cur.execute('SELECT "users", "producers", "venues" FROM "usersFollowLists" WHERE "userId" = %s', (userID,))
        row = cur.fetchone()

        if row:
            follow_list = {
                "users": row['users'],
                "producers": row['producers'],
                "venues": row['venues']
            }
        else:
            follow_list = {
                "users": [],
                "producers": [],
                "venues": []
            }

        if target not in ['users', 'producers', 'venues']:
            return jsonify({"code": 400, "message": "Invalid target."}), 400

        target_list = follow_list[target]

        if action == "unfollow":
            if str(followerID) in target_list:
                target_list.remove(str(followerID))

                # Remove the follower from latestUserFollowers table
                if target == 'users':
                    cur.execute(
                        'DELETE FROM "latestUserFollowers" WHERE "userId" = %s AND "followingId" = %s',
                        (userID, followerID)
                    )
        else:
            if str(followerID) not in target_list:
                target_list.append(str(followerID))

                # Add the follower to latestUserFollowers table
                if target == 'users':
                    # Ensure we do not exceed 10 followers
                    # Step 1: Check follower count
                    cur.execute(
                        'SELECT COUNT(*) FROM "latestUserFollowers" WHERE "userId" = %s',
                        (userID,)
                    )
                    count = cur.fetchone()['count']

                    # Step 2: If already 10 followers, delete the oldest one
                    if count >= 10:
                        cur.execute(
                            '''
                            WITH to_delete AS (
                                SELECT id FROM "latestUserFollowers"
                                WHERE "userId" = %s
                                ORDER BY "followDate" ASC
                                LIMIT 1
                            )
                            DELETE FROM "latestUserFollowers" WHERE id IN (SELECT id FROM to_delete)
                            ''',
                            (userID,)
                        )

                    # Step 3: Insert new follower (optional conflict resolution)
                    cur.execute(
                        '''
                        INSERT INTO "latestUserFollowers" ("userId", "followingId")
                        VALUES (%s, %s)
                        ON CONFLICT DO NOTHING
                        ''',
                        (userID, followerID)
                    )

        if row:
            cur.execute(
                """
                UPDATE "usersFollowLists"
                SET 
                    "users" = %s,
                    "producers" = %s,
                    "venues" = %s
                WHERE "userId" = %s
                """,
                (
                    follow_list['users'],
                    follow_list['producers'],
                    follow_list['venues'],
                    userID
                )
            )
        else:
            cur.execute(
                """
                INSERT INTO "usersFollowLists" ("userId", "users", "producers", "venues")
                VALUES (%s, %s, %s, %s)
                """,
                (
                    userID,
                    follow_list['users'],
                    follow_list['producers'],
                    follow_list['venues']
                )
            )
        
        conn.commit()

        return jsonify(
            {
                "code": 201,
                "data": {
                    "userID": userID,
                    "action": action,
                    "target": target,
                    "followerID": followerID
                },
                "message": f"{action.capitalize()}d successfully!"
            }
        ), 201
    except Exception as e:
        print(str(e))
        conn.rollback()
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred updating follow list."
            }
        ), 500
    finally:
        cur.close()
    
# -----------------------------------------------------------------------------------------
# [POST] Update mod type
# - Update user mod type with new details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/updateModType', methods=['POST'])
def updateModType():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()
    print(data)
    userID = data['userID']
    newModType = data['newModType']

    try:
        cur.execute('SELECT "modType" FROM users WHERE id = %s', (userID,))
        existingModType = cur.fetchone()

        if not existingModType:
            return jsonify(
                {
                    "code": 404,
                    "message": "User not found."
                }
            ), 404

        modType = existingModType['modType'] if existingModType['modType'] is not None else []
        modType.append(newModType)

        cur.execute('UPDATE users SET "modType" = %s WHERE id = %s', (modType, userID))
        conn.commit()
        cur.close()

        return jsonify(
            {   
                "code": 201,
                "data": {
                    "userID": userID,
                    "newModType": newModType
                }
            }
        ), 201

    except Exception as e:
        conn.rollback()
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": {
                    "userID": userID,
                    "newModType": newModType
                },
                "message": "An error occurred updating mod type."
            }
        ), 500

    finally:
        cur.close()

# -----------------------------------------------------------------------------------------
# [POST] Remove mod type
# - Remove user mod type by specified drink type
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/removeModType', methods=['POST'])
def removeModType():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()
    print(data)
    userID = data['userID']
    removeModType = data['removeModType']

    try:
        cur.execute('SELECT "modType" FROM users WHERE id = %s', (userID,))
        existingModType = cur.fetchone()

        if not existingModType:
            return jsonify(
                {
                    "code": 404,
                    "message": "User not found."
                }
            ), 404

        modType = existingModType['modType'] if existingModType['modType'] is not None else []
        modType.remove(removeModType)

        cur.execute('UPDATE users SET "modType" = %s WHERE id = %s', (modType, userID))
        conn.commit()
        cur.close()

        return jsonify(
            {   
                "code": 201,
                "data": {
                    "userID": userID,
                    "removeModType": removeModType
                }
            }
        ), 201

    except Exception as e:
        conn.rollback()
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": {
                    "userID": userID,
                    "removeModType": removeModType
                },
                "message": "An error occurred updating mod type."
            }
        ), 500

    finally:
        cur.close()
