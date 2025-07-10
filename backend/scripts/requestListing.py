# Port: 5011
# Routes: /requestListing (POST), /requestListingModify/<requestID> (POST), /requestEdits (POST), /requestEditsModify/<requestID> (POST), /requestInaccuracy (POST), /requestReviewStatus/<requestID> (POST)
# Dataclass: RequestListings
# -----------------------------------------------------------------------------------------

import os
import json
import pytz
import s3Images
from bson import json_util
from flask import Blueprint, g, request, jsonify
from datetime import datetime
from scripts import pointsHelperFunc, badge_helpers, notifications
import re

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

def parse_json(data):
    return json.loads(json_util.dumps(data))

# -----------------------------------------------------------------------------------------
# [POST] Request for listing creation
# - Insert entry into the "requestListings" collection. Follows requestListings dataclass requirements.
# - Duplicate listing check: If a listing with the same name exists, reject the request
# - Possible return codes: 201 (Created), 400 (Duplicate Detected), 500 (Error during creation)
@blueprint.route("/requestListing", methods= ['POST'])
def requestListing():
    conn = g.db
    cursor = conn.cursor()
    rawRequest = request.get_json()

    rawRequestName = rawRequest["listingName"]
    cursor.execute('SELECT id FROM listings WHERE "listingName" = %s', (rawRequestName,))
    existingBottle = cursor.fetchone()

    if existingBottle is not None:
        return jsonify(
            {
                "code": 400,
                "data": {
                    "listingName": rawRequestName
                },
                "message": "Bottle with the same name already exists."
            }
        ), 400

    if rawRequest['photo']:
        base64_string = re.sub(r'^data:image\/[a-zA-Z]+;base64,', '', rawRequest['photo'])
        rawRequest['photo'] = s3Images.uploadBase64ImageToS3(base64_string)

    # Handle nullable foreign keys
    producerId = rawRequest.get('producerID') or None
    userId = rawRequest.get('userID') or None
    bottler_id = rawRequest.get('bottlerID') or None

    try:
        cursor.execute("""
            INSERT INTO "requestListings" (
                "listingName", bottler, "drinkType", "sourceLink", "brandRelation", 
                "reviewStatus", "userID", photo, "originCountry", "producerID", 
                "producerNew", "typeCategory", abv, age, "reviewLink", "drinkStyle", "bottlerID"
            ) VALUES (%s, %s, %s, %s, %s, 
                      %s, %s, %s, %s, %s, 
                      %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
        """, (
            rawRequestName,
            rawRequest['bottler'],
            rawRequest['drinkType'],
            rawRequest['sourceLink'],
            rawRequest['brandRelation'],
            rawRequest['reviewStatus'],
            userId,
            rawRequest['photo'],
            rawRequest['originCountry'],
            producerId,
            rawRequest['producerNew'],
            rawRequest['typeCategory'],
            rawRequest['abv'],
            rawRequest['age'],
            rawRequest['reviewLink'],
            rawRequest.get('drinkStyle', ''),
            bottler_id
        ))

        conn.commit()
        newRequestId = cursor.fetchone()

        if newRequestId is None:
            raise Exception("Failed to retrieve the new request ID after insert.")

        return jsonify(
            {
                "code": 201,
                "data": {
                    "listingName": rawRequestName,
                    "requestId": newRequestId
                }
            }
        ), 201

    except Exception as e:
        conn.rollback()
        print(f"Error: {str(e)}")
        return jsonify(
            {
                "code": 500,
                "data": {
                    "listingName": rawRequestName
                },
                "message": "An error occurred while submitting the request."
            }
        ), 500
    
    finally:
        cursor.close()

# -----------------------------------------------------------------------------------------
# [POST] Edit submitted request for listing creation
# - Update entry with specified id from the "requestListings" collection. Follows requestListings dataclass requirements.
# - Duplicate listing check: If a listing with the same name exists, reject the request
# - Possible return codes: 201 (Updated), 400 (Duplicate Detected), 500 (Error during update)
@blueprint.route("/requestListingModify/<string:requestID>", methods= ['POST'])
def requestListingModify(requestID):
    conn = g.db
    cursor = conn.cursor()
    rawRequest = request.get_json()

    rawRequestName = rawRequest["listingName"]
    cursor.execute('SELECT id FROM listings WHERE "listingName" = %s', (rawRequestName,))
    existingBottle = cursor.fetchone()

    if existingBottle is not None:
        return jsonify(
            {
                "code": 400,
                "data": {
                    "listingName": rawRequestName
                },
                "message": "Bottle with the same name already exists."
            }
        ), 400
        

    # If rawRequest has photo, check if existingRequest has photo, delete if found, else upload image to s3 and save image in db
    if rawRequest['photo']:
        cursor.execute('SELECT photo FROM "requestListings" WHERE id = %s', (requestID,))
        existingRequest = cursor.fetchone()

        if existingRequest:
            s3Images.deleteImageFromS3(existingRequest)
        if rawRequest['photo']:
            base64_string = re.sub(r'^data:image\/[a-zA-Z]+;base64,', '', rawRequest['photo'])
            rawRequest['photo'] = s3Images.uploadBase64ImageToS3(base64_string)

    producerId = rawRequest.get('producerID') or None
    userId = rawRequest.get('userID') or None

    try:
        cursor.execute("""
            UPDATE "requestListings"
            SET "listingName" = %s, bottler = %s, "drinkType" = %s, "sourceLink" = %s, "brandRelation" = %s, 
                "reviewStatus" = %s, "userID" = %s, photo = %s, "originCountry" = %s, "producerID" = %s, 
                "producerNew" = %s, "typeCategory" = %s, abv = %s, age = %s, "reviewLink" = %s
            WHERE id = %s;
        """, (
            rawRequestName,
            rawRequest['bottler'],
            rawRequest['drinkType'],
            rawRequest['sourceLink'],
            rawRequest['brandRelation'],
            rawRequest['reviewStatus'],
            userId,
            rawRequest['photo'],
            rawRequest['originCountry'],
            producerId,
            rawRequest['producerNew'],
            rawRequest['typeCategory'],
            rawRequest['abv'],
            rawRequest['age'],
            rawRequest['reviewLink'],
            requestID
        ))

        conn.commit()

        return jsonify(
            {
                "code": 201,
                "data": {
                    "listingName": rawRequestName,
                    "requestId": requestID
                }
            }
        ), 201

    except Exception as e:
        conn.rollback()
        print(f"Error: {str(e)}")
        return jsonify(
            {
                "code": 500,
                "data": {
                    "listingName": rawRequestName
                },
                "message": "An error occurred while submitting the request."
            }
        ), 500

# -----------------------------------------------------------------------------------------
# [POST] Request for listing modification
# - Insert entry into the "requestEdits" collection. Follows requestEdits dataclass requirements.
# - Possible return codes: 201 (Created), 400 (Invalid Listing), 500 (Error during creation)
@blueprint.route("/requestEdits", methods= ['POST'])
def requestEdits():
    conn = g.db
    cur = conn.cursor()
    rawRequest = request.get_json()

    rawListingID = int(rawRequest["listingID"])

    cur.execute('SELECT * FROM listings WHERE "id" = %s', (rawListingID,))
    existingListing = cur.fetchone()

    if existingListing is None:
        return jsonify(
            {
                "code": 400,
                "data": {
                    "listingID": rawListingID
                },
                "message": "Linked listing is not valid!"
            }
        ), 400
    
    newRequest = {
        "editDesc": rawRequest["editDesc"],
        "listingID": rawListingID,
        "userID": int(rawRequest["userID"]),
        "brandRelation": rawRequest["brandRelation"],
        "reviewStatus": rawRequest["reviewStatus"],
        "duplicateLink": rawRequest.get("duplicateLink", ''),
        "sourceLink": rawRequest.get("sourceLink", '')
    }
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        # Insert new edit request into the database
        columns = ', '.join(f'"{key}"' for key in newRequest.keys())
        placeholders = ', '.join(['%s'] * len(newRequest))
        sql = f'INSERT INTO "requestEdits" ({columns}) VALUES ({placeholders})'
        
        cur.execute(sql, list(newRequest.values()))
        conn.commit()

        # Build and insert notification for the producer who owns this listing

        producerId = existingListing["producerID"]
        listingName = existingListing["listingName"]

        cur.execute('SELECT username FROM users WHERE id = %s', (newRequest["userID"],))
        userRow = cur.fetchone()
        userUsername = userRow["username"] if userRow else "Someone"

        notification_data = {
            "userId": producerId,
            "userType": "producer",
            "notiTabs": "forYou",
            "notiType": "edit_request",
            "image": None,
            "link": f"/request/view",  # adjust this to the actual front-end route if needed
            "message": f"@{userUsername} requested an edit for {listingName}",
            "createdAt": current_time,
        }

        notifications.add_notification_to_db(notification_data)

        return jsonify(
            {
                "code": 201,
                "data": rawListingID
            }
        ), 201
    
    except Exception as e:
        print(str(e))
        conn.rollback()
        return jsonify(
            {
                "code": 500,
                "data": {
                    "listingID": rawListingID
                },
                "message": "An error occurred while submitting the request."
            }
        ), 500

    finally:
        cur.close()

# -----------------------------------------------------------------------------------------
# [POST] Edit submitted request for listing modification
# - Update entry with specified id from the "requestEdits" collection. Follows requestEdits dataclass requirements.
# - Possible return codes: 201 (Updated), 400 (Invalid Listing), 500 (Error during update)
@blueprint.route("/requestEditsModify/<string:requestID>", methods= ['POST'])
def requestEditsModify(requestID):
    conn = g.db
    cur = conn.cursor()
    rawRequest = request.get_json()

    rawListingID = int(rawRequest["listingID"])

    cur.execute('SELECT * FROM listings WHERE "id" = %s', (rawListingID,))
    existingListing = cur.fetchone()

    if existingListing is None:
        return jsonify(
            {
                "code": 400,
                "data": {
                    "listingID": rawListingID
                },
                "message": "Linked listing is not valid!"
            }
        ), 400
    
    newRequest = {
        "editDesc": rawRequest["editDesc"],
        "listingID": rawListingID,
        "userID": int(rawRequest["userID"]),
        "brandRelation": rawRequest["brandRelation"],
        "reviewStatus": rawRequest["reviewStatus"],
        "duplicateLink": rawRequest.get("duplicateLink", ''),
        "sourceLink": rawRequest.get("sourceLink", '')
    }

    try:
        # Insert new edit request into the database
        columns = ', '.join(f'"{key}"' for key in newRequest.keys())
        placeholders = ', '.join(['%s'] * len(newRequest))
        sql = f'UPDATE "requestEdits" SET ({columns}) = ({placeholders}) WHERE id = %s'
        
        cur.execute(sql, list(newRequest.values()) + [requestID])
        conn.commit()

        return jsonify(
            {
                "code": 201,
                "data": rawListingID
            }
        ), 201
    
    except Exception as e:
        print(str(e))
        conn.rollback()
        return jsonify(
            {
                "code": 500,
                "data": {
                    "listingID": rawListingID
                },
                "message": "An error occurred while submitting the request."
            }
        ), 500
    
    finally:
        cur.close()
    
# -----------------------------------------------------------------------------------------
# [POST] Request for listing modification in venue menu
# - Insert entry into the "requestInaccurate" collection. Follows requestInaccuracy dataclass requirements.
# - Possible return codes: 201 (Created), 400 (Duplicate request), 500 (Error during creation)
@blueprint.route("/requestInaccuracy", methods= ['POST'])
def requestInaccuracy():
    conn = g.db
    cur = conn.cursor()
    rawRequest = request.get_json()

    rawListingID = int(rawRequest["listingID"])
    rawVenueID = int(rawRequest["venueID"])
    rawUserID = int(rawRequest["userID"])

    # Check if inaccuracy request is already submitted for the same bottle for a venue
    cur.execute("""
        SELECT * FROM "requestInaccuracy"
        WHERE "listingId" = %s AND "venueId" = %s AND "userId" = %s;
    """, (rawListingID, rawVenueID, rawUserID))
    existingListing = cur.fetchone()

    if existingListing is not None:
        return jsonify(
            {
                "code": 400,
                "data": {
                    "listingID": rawListingID
                },
                "message": "Duplicate request for inaccuracy!"
            }
        ), 400
    
    # Prepare new request
    reportDate = datetime.now(pytz.timezone('Etc/GMT-8'))
    inaccurateReason = rawRequest.get("inaccurateReason", "")

    try:
        cur.execute(
            """
                INSERT INTO "requestInaccuracy" ("listingId", "userId", "venueId", "reportDate", "inaccurateReason", "reviewStatus")
                VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (rawListingID, rawUserID, rawVenueID, reportDate, inaccurateReason, False)
        )
        conn.commit()

        return jsonify(
            {
                "code": 201,
                "data": rawListingID
            }
        ), 201
    
    except Exception as e:
        print(str(e))
        conn.rollback()
        return jsonify(
            {
                "code": 500,
                "data": {
                    "listingID": rawListingID
                },
                "message": "An error occurred while submitting the request."
            }
        ), 500
    
    finally:
        cur.close()

# -----------------------------------------------------------------------------------------
# [POST] Edit review status of a submitted request
# - Update entry with specified id from the specified collection.
# - Possible return codes: 201 (Updated), 500 (Error during update)

@blueprint.route("/requestReviewStatus/<string:requestID>", methods= ['POST'])
def requestReviewStatus(requestID):
    conn = g.db
    cur = conn.cursor()

    updateRequest = request.get_json()
    targetCollection = updateRequest["targetCollection"]
    status = updateRequest["reviewStatus"]
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        if targetCollection == "requestInaccuracy":
            print(f"Handling requestInaccuracy for requestID: {requestID}")

        cur.execute(
            f'UPDATE "{targetCollection}" SET "reviewStatus" = %s WHERE id = %s;',
            (status, requestID)
        )

        # Get the userID from the requestID
        cur.execute(
            f'SELECT "userID" FROM "{targetCollection}" WHERE id = %s;',
            (requestID,)
        )
        userID_result = cur.fetchone()
        
        if not userID_result:
            raise Exception(f"No user ID found for request ID {requestID}")
            
        user_id = userID_result['userID']
        
        # Check if user has reached maximum proof points
        if pointsHelperFunc.check_max_proof_points(user_id):
            return jsonify(
                {
                    "code": 201,
                    "data": requestID
                }
            ), 201

        # Initialize variables
        proofPoints = None
        badge_result = None

        # Process based on the target collection and status
        if targetCollection == "requestListings" and status == True:
            cur.execute(
                'SELECT "proofPoints" FROM "pointSystemRules" WHERE id = 12;'
            )
            proofPoints = cur.fetchone()
            
            badge_result = badge_helpers.process_new_drink_badge(conn, cur, user_id)

        elif targetCollection == "requestEdits" and status == True:
            # Get the proof points for successful edit suggestions
            cur.execute(
                'SELECT "proofPoints" FROM "pointSystemRules" WHERE id = 13;'
            )
            proofPoints = cur.fetchone()
            
            # Process the "Brew-tiful Mind" badge for edit suggestions
            badge_result = badge_helpers.process_new_drink_badge(conn, cur, user_id)
        
        # Update user's proof points if applicable
        if proofPoints is not None:
            # Update the user's proof points
            cur.execute(
                'UPDATE "pointsRecorder" SET "currentPoints" = "currentPoints" + %s WHERE "userID" = %s AND "userType" = %s;',
                (proofPoints['proofPoints'], user_id, 'user')
            )
            conn.commit()

        cur.execute('SELECT username FROM users WHERE id = %s', (user_id,))
        user_row = cur.fetchone()
        if user_row:
            # Get the username of the user
            user_username = user_row['username'] if user_row else "Someone"
            
        # Notify if badge earned
        if badge_result:
            notification_data = {
                "userId":   user_id,
                "userType": "user",
                "notiTabs": "forYou",
                "notiType": "badge_earned",
                "image":    None,
                "link":     f"/profile/user/{user_id}/{user_username}",
                "message":  f"Congratulations! You earned a badge: {badge_result['badgeName']}.",
                "createdAt": current_time,
            }
            print("Adding notification for badge earned:", notification_data)
            notifications.add_notification_to_db(notification_data)        

        # Prepare the response
        response_data = {
            "code": 201,
            "data": requestID,
            "proofPointsAdded": proofPoints['proofPoints'] if proofPoints else 0,
        }
        
        if badge_result:
            response_data["badgeAwarded"] = badge_result
        
        return jsonify(response_data), 201
    
    except Exception as e:
        conn.rollback()
        print(f"Error: {str(e)}")
        return jsonify(
            {
                "code": 500,
                "data": {
                    "requestID": requestID
                },
                "message": "An error occurred while updating the review status."
            }
        ), 500
    
    finally:
        cur.close()