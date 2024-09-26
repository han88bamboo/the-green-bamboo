# Port: 5100
# Routes: /editDetails (POST), /updateBookmark (POST), /updateFollowLists (POST), /updateModType (POST), /removeModType (POST)
# -----------------------------------------------------------------------------------------

import os
import pytz
import s3Images
from flask import Blueprint, g, request, jsonify
from bson.objectid import ObjectId
from datetime import datetime

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
    # print(data['image64'])
    userID = data['userID']
    cursor = conn.cursor()
    try:
        if 'image64' in data:
            cursor.execute("SELECT photo FROM users WHERE id = %s", (userID,))
            existingUser = cursor.fetchone()
            if existingUser:
                s3Images.deleteImageFromS3(existingUser['photo'])

            image64 = s3Images.uploadBase64ImageToS3(data['image64'])

            cursor.execute("UPDATE users SET photo = %s WHERE id = %s", (image64, userID))
        drinkChoice = data['drinkChoice']
        cursor.execute("UPDATE users SET \"choiceDrinks\" = %s WHERE id = %s", (drinkChoice, userID))

        conn.commit()
        return jsonify(
            {   
                "code": 201,
                "data": {
                    "userID": userID,
                    "drinkChoice": drinkChoice
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
                    "drinkChoice": drinkChoice
                },
                "message": "An error occurred updating the image or drink choice."
            }
        ), 500
    
    finally:
        cursor.close()
    
# -----------------------------------------------------------------------------------------
# [POST] Update user bookmark
# - Update user bookmark with new details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/updateBookmark', methods=['POST'])
def updateBookmark():
    conn = g.db
    data = request.get_json()
    print(data)
    userID = data['userID']
    bookmark = data['bookmark']

    try:
        cursor = conn.cursor()
        for listName in bookmark:
            listDesc = bookmark[listName]["listDesc"]
            listItems = bookmark[listName]["listItems"]

            query = """
                INSERT INTO "usersDrinkLists" ("userId", "listName", "drinks")
                VALUES (%s, %s, %s)
                ON CONFLICT ("userId", "listName") DO UPDATE
                SET "drinks" = EXCLUDED."drinks";
            """
            cursor.execute(query, (userID, listName, listItems))
        
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
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": {
                    "data": {
                        "userID": userID,
                        "bookmark": bookmark
                    }
                },
                "message": "An error occurred updating the drink lists."
            }
        ), 500

# -----------------------------------------------------------------------------------------
# [POST] Update follow lists
# - Update user follow lists with new details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/updateFollowLists', methods=['POST'])
def updateFollowList():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()
    print(data)

    userID = int(data['userID'])
    action = data['action']
    target = data['target']
    followerID = data['followerID']

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
            if followerID in target_list:
                target_list.remove(followerID)
        else:
            if followerID not in target_list:
                target_list.append(followerID)

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
