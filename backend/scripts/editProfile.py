# Port: 5100
# Routes: /editDetails (POST), /updateBookmark (POST), /updateFollowLists (POST), /updateModType (POST), /removeModType (POST)
# /updateListPrivacy (POST), /updateListItemNote (POST), /upvoteList (POST), /removeUpvote (POST)
# -----------------------------------------------------------------------------------------

import os
import s3Images
from flask import Blueprint, g, request, jsonify
from scripts import pointsHelperFunc, badge_helpers, notifications
from datetime import datetime
import re
from scripts import notifications

# Import the database manager for connection pooling
from app import db_manager

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

# -----------------------------------------------------------------------------------------
# [POST] Edit user profile
# - Update user profile with new details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/editDetails', methods=['POST'])
def editDetails():
    data = request.get_json()
    userID = data['userID']
    
    with db_manager.get_cursor() as cursor:
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

# -----------------------------------------------------------------------------------------
# [POST] Update user producer bookmark
# - Update user producer bookmark with new details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/updateProducerBookmark', methods=['POST'])
def updateProducerBookmark():
    data = request.get_json()
    userID = int(data['userID'])
    bookmark = data['bookmark']

    try:
        with db_manager.get_cursor() as cursor:
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
        return jsonify({
            "code": 500,
            "data": {
                "userID": userID,
                "bookmark": bookmark
            },
            "message": "An error occurred updating the producer lists."
        }), 500
    
# -----------------------------------------------------------------------------------------
# [POST] Update user venue bookmark
# - Update user venue bookmark with new details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/updateVenueBookmark', methods=['POST'])
def updateVenueBookmark():
    data = request.get_json()
    userID = int(data['userID'])
    bookmark = data['bookmark']

    try:
        with db_manager.get_cursor() as cursor:
            # Fetch existing venue lists for the user
            cursor.execute('SELECT "id", "listName" FROM "userVenueLists" WHERE "userId" = %s', (userID,))
            existing_lists = {row['listName']: row['id'] for row in cursor.fetchall()}

            bookmark_list_names = set(bookmark.keys())
            existing_list_names = set(existing_lists.keys())

            # Identify lists to delete
            lists_to_delete = existing_list_names - bookmark_list_names
            for listName in lists_to_delete:
                cursor.execute('DELETE FROM "userVenueLists" WHERE "userId" = %s AND "listName" = %s', (userID, listName))

            for listName, listData in bookmark.items():
                listItems = listData["listItems"]

                if listName in existing_lists:
                    list_id = existing_lists[listName]
                    cursor.execute(
                        'UPDATE "userVenueLists" SET "listDesc" = %s WHERE "id" = %s',
                        (listData["listDesc"], list_id)
                    )
                else:
                    cursor.execute(
                        'INSERT INTO "userVenueLists" ("userId", "listName", "listDesc") VALUES (%s, %s, %s) RETURNING "id"',
                        (userID, listName, listData["listDesc"],)
                    )
                    list_id = cursor.fetchone()["id"]

                # Delete existing items in the list
                cursor.execute('DELETE FROM "userVenueListItems" WHERE "listId" = %s', (list_id,))

                # Insert new venues
                for item in listItems:
                    added_date = item.get("addedDate", None)
                    if added_date:
                        cursor.execute(
                            'INSERT INTO "userVenueListItems" ("listId", "venueId", "addedDate") VALUES (%s, %s, %s)',
                            (list_id, item["venueId"], added_date)
                        )
                    else:
                        cursor.execute(
                            'INSERT INTO "userVenueListItems" ("listId", "venueId", "addedDate") VALUES (%s, %s, NOW())',
                            (list_id, item["venueId"])
                        )

        return jsonify({
            "code": 201,
            "data": {
                "userID": userID,
                "bookmark": bookmark
            }
        }), 201

    except Exception as e:
        print("Update venue bookmark error:", str(e))
        return jsonify({
            "code": 500,
            "data": {
                "userID": userID,
                "bookmark": bookmark
            },
            "message": "An error occurred updating the venue lists."
        }), 500
    
# -----------------------------------------------------------------------------------------
# [POST] Update user bookmark
# - Update user bookmark with new details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/updateBookmark', methods=['POST'])
def updateBookmark():
    data = request.get_json()
    userID = int(data['userID'])
    bookmark = data['bookmark']

    try:
        with db_manager.get_cursor() as cursor:
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
                listDesc = listData.get("listDesc", "")
                isPublic = listData.get("isPublic", True)  # Default to public if not specified

                # If list exists, use its ID; otherwise, create a new one
                if listName in existing_lists:
                    list_id = existing_lists[listName]

                    # Update existing list desc and public status
                    cursor.execute(
                        'UPDATE "usersDrinkLists" SET "listDesc" = %s, "isPublic" = %s WHERE "id" = %s',
                        (listDesc, isPublic, list_id)
                    )
                else:
                    cursor.execute(
                        'INSERT INTO "usersDrinkLists" ("userId", "listName", "listDesc", "isPublic") VALUES (%s, %s, %s, %s) RETURNING "id"',
                        (userID, listName, listDesc, isPublic)
                    )
                    list_id = cursor.fetchone()["id"]
                    num_lists_to_add_count += 1

                # Delete existing items in the list (to avoid duplicates)
                cursor.execute('DELETE FROM "usersDrinkListItems" WHERE "listId" = %s', (list_id,))

                # Insert new drinks with their addedDate and note, using NOW() if missing
                for item in listItems:
                    added_date = item.get("addedDate", None)  # Get addedDate, default to None
                    note = item.get("note", "")  # Get note, default to empty string
                    drink_id = item.get("drinkId") or item  # Handle both old format (direct ID) and new format (object with drinkId)
                    
                    if added_date:
                        cursor.execute(
                            'INSERT INTO "usersDrinkListItems" ("listId", "drinkId", "addedDate", "note") VALUES (%s, %s, %s, %s)',
                            (list_id, drink_id, added_date, note)
                        )
                    else:
                        cursor.execute(
                            'INSERT INTO "usersDrinkListItems" ("listId", "drinkId", "addedDate", "note") VALUES (%s, %s, NOW(), %s)',
                            (list_id, drink_id, note)
                        )

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

                    print(f"User {userID} earned {points_earned} points for editing the number of lists.")

                # Process PublicList badge based on net list changes
                net_list_change = num_lists_to_add_count - num_lists_to_delete_count
                if net_list_change != 0:
                    badge_result = badge_helpers.process_public_list_badge(cursor.connection, cursor, userID, net_list_change)

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

            return jsonify(response_data), 201

    except Exception as e:
        print("Update bookmark error:", str(e))
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
    data = request.get_json()

    userID = int(data['userID'])
    action = data['action']
    target = data['target']
    followerID = int(data['followerID'])

    try:
        with db_manager.get_cursor() as cursor:
            cursor.execute('SELECT "users", "producers", "venues" FROM "usersFollowLists" WHERE "userId" = %s', (userID,))
            row = cursor.fetchone()

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
                        cursor.execute(
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
                        cursor.execute(
                            'SELECT COUNT(*) FROM "latestUserFollowers" WHERE "userId" = %s',
                            (userID,)
                        )
                        count = cursor.fetchone()['count']

                        # Step 2: If already 10 followers, delete the oldest one
                        if count >= 10:
                            cursor.execute(
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
                        cursor.execute(
                            '''
                            INSERT INTO "latestUserFollowers" ("userId", "followingId")
                            VALUES (%s, %s)
                            ON CONFLICT DO NOTHING
                            ''',
                            (userID, followerID)
                        )

                        # ADD NOTIFICATION CODE HERE
                        # Get follower username (User A's name)
                        cursor.execute('SELECT "username", "photo" FROM "users" WHERE "id" = %s', (userID,))
                        follower_user = cursor.fetchone()
                        follower_username = follower_user['username'] if follower_user else "Someone"
                        follower_photo = follower_user['photo']  # User A's photo

                        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                        # Create notification for User B
                        notification_data = {
                            "userId": followerID,  # User B (person being followed)
                            "userType": "user",
                            "notiTabs": "forYou",
                            "notiType": "new_follower",
                            "image": follower_photo,  # User A's photo
                            "link": f"/profile/user/{userID}/{follower_username}",
                            "message": f"@{follower_username} followed you!",
                            "createdAt": current_time
                        }

                        #Send notification to User B
                        print("Sending notification:", notification_data)
                        notifications.add_notification_to_db(notification_data)

            if row:
                cursor.execute(
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
                cursor.execute(
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
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred updating follow list."
            }
        ), 500
    
# -----------------------------------------------------------------------------------------
# [POST] Update mod type
# - Update user mod type with new details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/updateModType', methods=['POST'])
def updateModType():
    data = request.get_json()
    print(data)
    userID = data['userID']
    newModType = data['newModType']

    try:
        with db_manager.get_cursor() as cursor:
            cursor.execute('SELECT "modType" FROM users WHERE id = %s', (userID,))
            existingModType = cursor.fetchone()

            if not existingModType:
                return jsonify(
                    {
                        "code": 404,
                        "message": "User not found."
                    }
                ), 404

            modType = existingModType['modType'] if existingModType['modType'] is not None else []
            modType.append(newModType)

            cursor.execute('UPDATE users SET "modType" = %s WHERE id = %s', (modType, userID))

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

# -----------------------------------------------------------------------------------------
# [POST] Remove mod type
# - Remove user mod type by specified drink type
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/removeModType', methods=['POST'])
def removeModType():
    data = request.get_json()
    print(data)
    userID = data['userID']
    removeModType = data['removeModType']

    try:
        with db_manager.get_cursor() as cursor:
            cursor.execute('SELECT "modType" FROM users WHERE id = %s', (userID,))
            existingModType = cursor.fetchone()

            if not existingModType:
                return jsonify(
                    {
                        "code": 404,
                        "message": "User not found."
                    }
                ), 404

            modType = existingModType['modType'] if existingModType['modType'] is not None else []
            modType.remove(removeModType)

            cursor.execute('UPDATE users SET "modType" = %s WHERE id = %s', (modType, userID))

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

@blueprint.route('/updateListPrivacy', methods=['POST'])
def update_list_privacy():
    """Update the privacy setting of a user's list"""
    data = request.get_json()
    userID = int(data['userID'])
    listName = data['listName']
    isPublic = data['isPublic']
    
    try:
        with db_manager.get_cursor() as cursor:
            # Update the list privacy setting
            cursor.execute(
                'UPDATE "usersDrinkLists" SET "isPublic" = %s, "updatedAt" = NOW() WHERE "userId" = %s AND "listName" = %s',
                (isPublic, userID, listName)
            )
            
            return jsonify({
                "code": 201,
                "data": {
                    "userID": userID,
                    "listName": listName,
                    "isPublic": isPublic
                },
                "message": "List privacy updated successfully."
            }), 201
        
    except Exception as e:
        print("Update list privacy error:", str(e))
        return jsonify({
            "code": 500,
            "message": "An error occurred updating list privacy."
        }), 500
    
@blueprint.route('/updateListItemNote', methods=['POST'])
def update_list_item_note():
    """Update note for a specific item in a list"""
    data = request.get_json()
    userID = int(data['userID'])
    listName = data['listName']
    drinkId = int(data['drinkId'])
    note = data['note']
    
    try:
        with db_manager.get_cursor() as cursor:
            
            # Get the list ID first
            cursor.execute(
                'SELECT "id" FROM "usersDrinkLists" WHERE "userId" = %s AND "listName" = %s',
                (userID, listName)
            )
            list_result = cursor.fetchone()
            
            if not list_result:
                return jsonify({
                    "code": 404,
                    "message": "List not found."
                }), 404
                
            listId = list_result['id']
            
            # Update the note for the specific item
            cursor.execute(
                'UPDATE "usersDrinkListItems" SET "note" = %s WHERE "listId" = %s AND "drinkId" = %s',
                (note, listId, drinkId)
            )
            
            return jsonify({
                "code": 201,
                "data": {
                    "listName": listName,
                    "drinkId": drinkId,
                    "note": note
                },
                "message": "Note updated successfully."
            }), 201
        
    except Exception as e:
        print("Update list item note error:", str(e))
        return jsonify({
            "code": 500,
            "message": "An error occurred updating the note."
        }), 500

@blueprint.route('/upvoteList', methods=['POST'])
def upvote_list():
    """Upvote a public list"""
    data = request.get_json()
    userID = int(data['userID'])
    listId = int(data['listId'])
    
    try:
        with db_manager.get_cursor() as cursor:
            # Check if user already upvoted this list
            cursor.execute(
                'SELECT "id" FROM "usersDrinkListUpvotes" WHERE "listId" = %s AND "userId" = %s',
                (listId, userID)
            )
            
            existing_upvote = cursor.fetchone()
            
            if existing_upvote:
                return jsonify({
                    "code": 400,
                    "message": "You have already upvoted this list."
                }), 400
            
            # Add upvote
            cursor.execute(
                'INSERT INTO "usersDrinkListUpvotes" ("listId", "userId") VALUES (%s, %s)',
                (listId, userID)
            )
            
            # Update upvote count
            cursor.execute(
                'UPDATE "usersDrinkLists" SET "upvotes" = "upvotes" + 1 WHERE "id" = %s',
                (listId,)
            )
            
            # Get updated upvote count
            cursor.execute(
                'SELECT "upvotes" FROM "usersDrinkLists" WHERE "id" = %s',
                (listId,)
            )
            
            updated_count = cursor.fetchone()['upvotes']
            
            return jsonify({
                "code": 201,
                "data": {
                    "listId": listId,
                    "upvotes": updated_count
                },
                "message": "List upvoted successfully."
            }), 201
        
    except Exception as e:
        print("Upvote list error:", str(e))
        return jsonify({
            "code": 500,
            "message": "An error occurred upvoting the list."
        }), 500
    
@blueprint.route('/removeUpvote', methods=['POST'])
def remove_upvote():
    """Remove upvote from a public list"""
    data = request.get_json()
    userID = int(data['userID'])
    listId = int(data['listId'])
    
    try:
        with db_manager.get_cursor() as cursor:
            # Check if user has upvoted this list
            cursor.execute(
                'SELECT "id" FROM "usersDrinkListUpvotes" WHERE "listId" = %s AND "userId" = %s',
                (listId, userID)
            )
            
            existing_upvote = cursor.fetchone()
            
            if not existing_upvote:
                return jsonify({
                    "code": 400,
                    "message": "You haven't upvoted this list."
                }), 400
            
            # Remove upvote
            cursor.execute(
                'DELETE FROM "usersDrinkListUpvotes" WHERE "listId" = %s AND "userId" = %s',
                (listId, userID)
            )
            
            # Update upvote count (ensure it doesn't go below 0)
            cursor.execute(
                'UPDATE "usersDrinkLists" SET "upvotes" = GREATEST("upvotes" - 1, 0) WHERE "id" = %s',
                (listId,)
            )
            
            # Get updated upvote count
            cursor.execute(
                'SELECT "upvotes" FROM "usersDrinkLists" WHERE "id" = %s',
                (listId,)
            )
            
            updated_count = cursor.fetchone()['upvotes']
            
            return jsonify({
                "code": 201,
                "data": {
                    "listId": listId,
                    "upvotes": updated_count
                },
                "message": "Upvote removed successfully."
            }), 201
        
    except Exception as e:
        print("Remove upvote error:", str(e))
        return jsonify({
            "code": 500,
            "message": "An error occurred removing the upvote."
        }), 500

# -----------------------------------------------------------------------------------------
# [POST] Create and add to festival favourites list
# - Check if "Favourites from <Venue Name>" list exists, create if needed, and add drink
# - Possible return codes: 200 (Already exists), 201 (Added), 500 (Error)
@blueprint.route('/createAndAddToFestivalFavouriteList', methods=['POST'])
def create_and_add_to_festival_favourite_list():
    """Create favourites list if needed and add drink to it"""
    data = request.get_json()
    userID = int(data['userId'])
    listName = data['listName'] 
    drinkId = int(data['drinkId'])
    
    try:
        with db_manager.get_cursor() as cursor:
            # Check if the favourites list already exists
            cursor.execute(
                'SELECT "id" FROM "usersDrinkLists" WHERE "userId" = %s AND "listName" = %s',
                (userID, listName)
            )
            
            existing_list = cursor.fetchone()
            
            if existing_list:
                list_id = existing_list['id']
                
                # Check if the drink is already in the list
                cursor.execute(
                    'SELECT "id" FROM "usersDrinkListItems" WHERE "listId" = %s AND "drinkId" = %s',
                    (list_id, drinkId)
                )
                
                existing_item = cursor.fetchone()
                
                if existing_item:
                    return jsonify({
                        "code": 200,
                        "data": {
                            "listName": listName,
                            "drinkId": drinkId,
                            "alreadyExists": True
                        },
                        "message": "Drink is already in your favourites list."
                    }), 200
                    
            else:
                # Create the favourites list
                list_desc = "Drinks you bookmarked at this event"
                cursor.execute(
                    'INSERT INTO "usersDrinkLists" ("userId", "listName", "listDesc", "isPublic") VALUES (%s, %s, %s, %s) RETURNING "id"',
                    (userID, listName, list_desc, True)  # Default to public
                )
                list_id = cursor.fetchone()["id"]
            
            # Add the drink to the list
            cursor.execute(
                'INSERT INTO "usersDrinkListItems" ("listId", "drinkId", "addedDate") VALUES (%s, %s, NOW())',
                (list_id, drinkId)
            )
            
            return jsonify({
                "code": 201,
                "data": {
                    "listName": listName,
                    "drinkId": drinkId,
                    "listId": list_id,
                    "alreadyExists": False
                },
                "message": "Drink has been added to your favourites list!"
            }), 201
        
    except Exception as e:
        print("Create and add to festival favourites error:", str(e))
        return jsonify({
            "code": 500,
            "data": {
                "userId": userID,
                "listName": listName,
                "drinkId": drinkId
            },
            "message": "An error occurred adding the drink to favourites."
        }), 500