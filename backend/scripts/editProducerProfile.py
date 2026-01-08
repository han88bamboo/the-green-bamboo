# Port: 5200
# Routes: /editDetails (POST), /addUpdates (POST), /sendQuestions (POST), /sendAnswers (POST), /likeUpdates (POST), /unlikeUpdates (POST), /updateProducerStatus (POST), /addProfileCount (POST), /addNewProfileCount (POST), /editUpdate (POST), /editAddress (POST), /editOpeningHours (POST), /deleteUpdate (POST), /editQA (POST), /deleteQA (POST)
# -----------------------------------------------------------------------------------------

import os
import s3Images
from flask import Blueprint, g, request, jsonify
from datetime import datetime
from scripts import pointsHelperFunc, badge_helpers, notifications
import re

# Import the database manager for connection pooling
from app import db_manager

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

# -----------------------------------------------------------------------------------------
# [POST] Edit producer profile
# - Update producer profile with new details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/editDetails', methods=['POST'])
def editDetails():  
    data = request.get_json()
    print(data)

    producerID = int(data['producerID'])
    producerName = data['producerName']
    producerDesc = data['producerDesc']
    isIndependentBottler = data['isIndependentBottler']
    originCountry = data['originCountry']
    yearFounded = data.get('yearFounded', None)
    activeStatus = data.get('activeStatus', None)
    owner = data.get('owner', None)
    location = data['location']
    openForTours = data.get('openForTours', False)
    website = data.get('website', None)

    with db_manager.get_cursor() as cursor:
        cursor.execute('SELECT * FROM producers WHERE id = %s', (producerID,))
        existingProducer = cursor.fetchone()

        if existingProducer:
            if data['image64']:
                if(existingProducer['photo']):
                    s3Images.deleteImageFromS3(existingProducer['photo'])

                base64_string = re.sub(r'^data:image\/[a-zA-Z]+;base64,', '', data['image64'])
                image64 = s3Images.uploadBase64ImageToS3(base64_string)
            else:
                image64 = existingProducer['photo']
            cursor.execute(
                """
                UPDATE producers 
                SET 
                    "photo" = %s,
                    "producerName" = %s,
                    "producerDesc" = %s,
                    "isIndependentBottler" = %s,
                    "originCountry" = %s,
                    "yearFounded" = %s,
                    "activeStatus" = %s,
                    "owner" = %s,
                    "location" = %s,
                    "openForTours" = %s,
                    "website" = %s
                WHERE id = %s
                """,
                (image64, producerName, producerDesc, isIndependentBottler, originCountry, yearFounded, activeStatus, owner, location, openForTours, website, producerID)
            )

            return jsonify(
                {
                    "code": 201,
                    "message": "Updated profile successfully!"
                }
            ), 201
        
        else:
            return jsonify(
                {
                    "code": 404,
                    "message": "Producer not found."
                }
            ), 404

# -----------------------------------------------------------------------------------------
# [POST] Add updates to producer profile
# - Add updates to producer profile
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/addUpdates', methods=['POST'])
def addUpdates():
    data = request.get_json()
    print(data)

    producerID = int(data['producerID'])
    date = datetime.strptime(data['date'], "%Y-%m-%dT%H:%M:%S.%fZ")
    text = data['text']

    image64 = ''

    if data.get('image64'):
        base64_string = re.sub(r'^data:image\/[a-zA-Z]+;base64,', '', data['image64'])
        image64 = s3Images.uploadBase64ImageToS3(base64_string)

    with db_manager.get_cursor() as cursor:
        cursor.execute('INSERT INTO "producersUpdates" ("date", "text", "photo", "producerId") VALUES (%s, %s, %s, %s)', (date, text, image64, producerID))

        # Fetch producer name
        cursor.execute('SELECT "producerName" FROM producers WHERE id = %s', (producerID,))
        producer_row = cursor.fetchone()
        producerName = producer_row['producerName'] if producer_row else "This producer"

        # Notify all users who follow this producer
        cursor.execute(
            'SELECT "userId" FROM "usersFollowLists" WHERE %s = ANY("producers")',
            (str(producerID),)
        )
        followers = cursor.fetchall()

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        for row in followers:
            notification_data = {
                "userId":   row['userId'],
                "userType": "user",
                "notiTabs": "venues & producers",
                "notiType": "producer_update",
                "image":    image64 or None,
                "link":     f"/profile/producer/{producerID}/{producerName}",
                "message":  f"{producerName} posted a new announcement.",
                "createdAt": current_time
            }
            print("Sending notification:", notification_data)
            try:
                notifications.add_notification_to_db(notification_data, cursor)
            except Exception as notif_error:
                print(f"Failed to send producer update notification: {notif_error}")

        return jsonify(
            {   
                "code": 201,
                "message": "Update added successfully!"
            }
        ), 201

# -----------------------------------------------------------------------------------------
# [POST] Send questions to producer
# - Send questions to producer
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/sendQuestions', methods=['POST'])
def sendQuestions():
    data = request.get_json()
    print(data)

    producerID = int(data['producerID'])
    question = data['question']
    answer = data['answer']
    date = datetime.strptime(data['date'], "%Y-%m-%dT%H:%M:%S.%fZ")
    userID = int(data['userID'])

    try:
        with db_manager.get_cursor() as cursor:
            cursor.execute(
                """
                    INSERT INTO "producersQuestionAnswers" (question, answer, date, "userId", "producerId")
                    VALUES (%s, %s, %s, %s, %s)
                """,
                (question, answer, date, userID, producerID)
            )

            # Send a notification to the producer
            # Fetch the asking user's username
            cursor.execute('SELECT username FROM users WHERE id = %s', (userID,))
            user_row = cursor.fetchone()
            user_username = user_row['username'] if user_row else "Someone"

            # # Fetch the producer's username
            # cursor.execute('SELECT username FROM producers WHERE id = %s', (producerID,))
            # producer_row = cursor.fetchone()
            # producer_username = producer_row['username'] if producer_row else ""

            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            notification_data = {
                "userId":   producerID,
                "userType": "producer",
                "notiTabs": "forYou",
                "notiType": "producer_question",
                "image":    None,
                "link":     f"/Producers/ProducersQA/{producerID}",
                "message":  f"@{user_username} asked you a question",
                "createdAt": current_time
            }
            try:
                notifications.add_notification_to_db(notification_data, cursor)
            except Exception as notif_error:
                print(f"Failed to send producer question notification: {notif_error}")

            # Initialize variables for points and badge processing
            points_earned = 0
            badge_result = None

            # Award points to user for asking a question
            if not pointsHelperFunc.check_max_proof_points(userID):
                # Get points for asking a question
                cursor.execute('SELECT "proofPoints" FROM "pointSystemRules" WHERE id = %s', (15,))
                points_rule = cursor.fetchone()
                
                if points_rule:
                    points_earned = points_rule['proofPoints']
                    
                    # Update user's points
                    cursor.execute(
                        'UPDATE "pointsRecorder" SET "currentPoints" = "currentPoints" + %s WHERE "userID" = %s',
                        (points_earned, userID)
                    )
                    
                    print(f"{points_earned} points awarded to user {userID} for asking a question")
                
                # Process the Question badge
                badge_result = badge_helpers.process_question_badge(cursor.connection, cursor, userID)
            
            # If badge earned, send notification
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
                print("Sending badge notification:", notification_data)
                try:
                    notifications.add_notification_to_db(notification_data, cursor)
                except Exception as notif_error:
                    print(f"Failed to send badge notification: {notif_error}")
            
            # Prepare the response
            response_data = {
                "code": 201,
                "message": "Question sent successfully!"
            }
            
            if points_earned > 0:
                response_data["pointsEarned"] = points_earned
                
            if badge_result:
                response_data["badgeAwarded"] = badge_result
                
            return jsonify(response_data), 201
    
    except Exception as e:
        print(str(e))
        return jsonify({
            "code": 500,
            "data": data,
            "message": "An error occurred sending the question!"
        }), 500

# -----------------------------------------------------------------------------------------
# [POST] Send answers to questions
# - Send answers to questions
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/sendAnswers', methods=['POST'])
def sendAnswers():
    data = request.get_json()
    print(data)

    producerID = int(data['producerID'])
    questionsAnswersID = int(data['questionsAnswersID'])
    answer = data['answer']

    try:
        with db_manager.get_cursor() as cursor:
            cursor.execute('UPDATE "producersQuestionAnswers" SET "answer" = %s WHERE "producerId" = %s AND id = %s', (answer, producerID, questionsAnswersID))

            # Fetch the original asker
            cursor.execute(
                'SELECT "userId" FROM "producersQuestionAnswers" WHERE id = %s',
                (questionsAnswersID,)
            )
            asker_row = cursor.fetchone()
            asker_id = asker_row['userId'] if asker_row else None

            # Fetch producer's username for the notification message
            cursor.execute(
                'SELECT username FROM producers WHERE id = %s',
                (producerID,)
            )
            producer_row = cursor.fetchone()
            producer_username = producer_row['username'] if producer_row else ''

            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Send notification back to the user who asked
            if asker_id:
                notification_data = {
                    "userId":   asker_id,
                    "userType": "user",
                    "notiTabs": "venues & producers",
                    "notiType": "producer_answer",
                    "image":    None,
                    "link":     f"/profile/producer/{producerID}/{producer_username}",
                    "message":  f"@{producer_username} answered your question",
                    "createdAt": current_time
                }
                print("Sending answer notification:", notification_data)
                try:
                    notifications.add_notification_to_db(notification_data, cursor)
                except Exception as notif_error:
                    print(f"Failed to send answer notification: {notif_error}")

            return jsonify(
                {   
                    "code": 201,
                    "message": "Answer sent successfully!"
                }
            ), 201
    
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred sending the answer!"
            }
        ), 500

# -----------------------------------------------------------------------------------------
# [POST] Like updates
# - Like updates
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/likeUpdates', methods=['POST'])
def likeUpdates():
    data = request.get_json()
    print(data)

    producerID = int(data['producerID'])
    updateID = int(data['updateID'])
    userID = int(data['userID'])
    userType = data['userType']

    with db_manager.get_cursor() as cursor:
        # Verify that the update exists and belongs to the producer
        cursor.execute('SELECT "producerId" FROM "producersUpdates" WHERE "id" = %s', (updateID,))
        existingUpdate = cursor.fetchone()

        if not existingUpdate or existingUpdate['producerId'] != producerID:
            return jsonify(
                {
                    "code": 404,
                    "message": "Update not found."
                }
            ), 404
        
        # Insert into the likes table
        cursor.execute("""
            INSERT INTO "producerUpdateLikes" ("updateId", "userId", "userType")
            VALUES (%s, %s, %s)
        """, (updateID, userID, userType))

        return jsonify(
            {
                "code": 201,
                "message": "Update liked successfully!"
            }
        ), 201

# -----------------------------------------------------------------------------------------
# [POST] Unlike updates
# - Unlike updates
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/unlikeUpdates', methods=['POST'])
def unlikeUpdates():
    data = request.get_json()
    print(data)

    producerID = int(data['producerID'])
    updateID = int(data['updateID'])
    userID = int(data['userID'])
    userType = data['userType']

    try:
        with db_manager.get_cursor() as cursor:
            # Verify that the update exists and belongs to the producer
            cursor.execute('SELECT "producerId" FROM "producersUpdates" WHERE "id" = %s', (updateID,))
            existingUpdate = cursor.fetchone()

            if not existingUpdate or existingUpdate['producerId'] != producerID:
                return jsonify(
                    {
                        "code": 404,
                        "message": "Update not found."
                    }
                ), 404
            
            # Remove from the likes table
            cursor.execute('DELETE FROM "producerUpdateLikes" WHERE "updateId" = %s AND "userId" = %s AND "userType" = %s', (updateID, userID, userType))

        return jsonify(
            {
                "code": 201,
                "message": "Update unliked successfully!"
            }
        ), 201
    
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred unliking the update."
            }
        ), 500
    
# -----------------------------------------------------------------------------------------
# [POST] Edit producer profile
# - Update producer profile with new details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/updateProducerStatus', methods=['POST'])
def updateProducerStatus():
    data = request.get_json()
    print(data)

    producerID = int(data['businessID'])
    producerName = data['newBusinessData']["businessName"]
    producerDesc = data['newBusinessData']["businessDesc"]
    originCountry = data['newBusinessData']["originCountry"]
    image = data['newBusinessData']["photo"]
    hashedPassword = data['newBusinessData']["hashedPassword"]
    claimStatus = data['newBusinessData']["claimStatus"]

    try:
        with db_manager.get_cursor() as cursor:
            cursor.execute(
                """
                    UPDATE producers
                    SET
                        "producerName" = %s,
                        "producerDesc" = %s,
                        "originCountry" = %s,
                        "hashedPassword" = %s,
                        "claimStatus" = %s
                    WHERE id = %s
                """,
                (producerName, producerDesc, originCountry, hashedPassword, claimStatus, producerID)
            )

            # Find all users who follow this producer
            cursor.execute(
                '''
                SELECT "userId"
                FROM "usersFollowLists"
                WHERE %s = ANY("producers")
                ''',
                (str(producerID),)
            )
            followers = cursor.fetchall()

            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Send each of them a notification
            for row in followers:
                notification_data = {
                "userId":   row['userId'],        # the follower’s user ID
                "userType": "user",
                "notiTabs":"venues & producers",
                "notiType":"status_update",
                "image":   image,
                "link":    f"/profile/producer/{producerID}/{producerName}",
                "message": f"{producerName} updated their status.",
                "createdAt": current_time
                }
                print("Sending notification:", notification_data)
                try:
                    notifications.add_notification_to_db(notification_data, cursor)
                except Exception as notif_error:
                    print(f"Failed to send status update notification: {notif_error}")

        return jsonify({
            "code": 201,
            "message": "Updated claim status successfully!"
        }), 201
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            "code": 500,
            "data": data,
            "message": "An error occurred updating claim status!"
        }), 500


# -----------------------------------------------------------------------------------------
# [POST] Add profile view count
# - Add profile view count
# - Possible return codes: 201 (Updated), 500 (Error during update)
# -- ========= "producersProfileViews" =========
# CREATE TABLE "producersProfileViews" (
#     "id" SERIAL PRIMARY KEY,
#     "date" TIMESTAMP, 
#     "count" INTEGER, -- do i need this?
#     "producerId" INTEGER REFERENCES "producers"("id") ON DELETE SET NULL -- [!] reference "producers" FK
#     -- "views" INTEGER REFERENCES "producersProfileViewsViews"("id") ON DELETE SET NULL  -- [!] reference "producersProfileViewsViews" FK
# );
@blueprint.route('/addProfileCount', methods=['POST'])
def addProfileCount():
    data = request.get_json()
    producerID = int(data['businessId'])
    viewsID = int(data['viewsId'])

    try:
        with db_manager.get_cursor() as cursor:
            cursor.execute('UPDATE "producersProfileViews" SET "count" = "count" + 1 WHERE "producerId" = %s AND id = %s', (producerID, viewsID))

        return jsonify(
            {   
                "code": 201,
                "message": "Profile view count updated successfully!"
            }
        ), 201
    
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred updating the profile view count."
            }
        ), 500

# -----------------------------------------------------------------------------------------
# [POST] Add new profile view count
# - Add new profile view count
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/addNewProfileCount', methods=['POST'])
def addNewProfileCount():
    data = request.get_json()
    print(data)
    producerID = int(data['producerID'])
    date = datetime.strptime(data['date'], "%Y-%m-%dT%H:%M:%S.%fZ")

    try:
        with db_manager.get_cursor() as cursor:
            cursor.execute('SELECT * FROM "producersProfileViews" WHERE "producerId" = %s', (producerID,))
            existingProfileView = cursor.fetchone()

            if existingProfileView:
                cursor.execute('UPDATE "producersProfileViews" SET "count" = "count" + 1 WHERE "producerId" = %s', (producerID,))

            else:
                cursor.execute('INSERT INTO "producersProfileViews" ("date", "count", "producerId") VALUES (%s, 1, %s)', (date, producerID))

        return jsonify(
            {   
                "code": 201,
                "message": "New profile view count added successfully!"
            }
        ), 201
    
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred updating the new profile view count."
            }
        ), 500

# -----------------------------------------------------------------------------------------

# [POST] Edit producer update
# - Update a producer update with new details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/editUpdate', methods=['POST'])
def editUpdate():
    data = request.get_json()
    print(data)

    producerID = int(data['producerID'])
    updateID = int(data['updateID'])
    update = data['update']
    image64 = data.get('image64', '')

    try:
        with db_manager.get_cursor() as cursor:
            # Find existing producer and check for the existing update
            cursor.execute('SELECT * FROM "producersUpdates" WHERE "producerId" = %s AND id = %s', (producerID, updateID))
            existingUpdate = cursor.fetchone()

            if existingUpdate:
                # Delete old photo from S3 if it exists
                if existingUpdate['photo']:
                    s3Images.deleteImageFromS3(existingUpdate['photo'])

                # Upload new image to S3 if it exists
                if image64:
                    base64_string = re.sub(r'^data:image\/[a-zA-Z]+;base64,', '', image64)
                    image64 = s3Images.uploadBase64ImageToS3(base64_string)

                # Update the producer's update in the database
                cursor.execute(
                    """
                    UPDATE "producersUpdates"
                    SET 
                        "text" = %s,
                        "photo" = %s
                    WHERE "producerId" = %s AND id = %s
                    """,
                    (update, image64, producerID, updateID)
                )

                return jsonify(
                    {
                        "code": 201,
                        "message": "Updated producer's update!"
                    }
                ), 201
            else:
                return jsonify(
                    {
                        "code": 404,
                        "message": "Update not found."
                    }
                ), 404
        
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred updating producer's update!"
            }
        ), 500

# -----------------------------------------------------------------------------------------

# [POST] Edit address
# - Edit address
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/editAddress', methods=['POST'])
def editAddress():
    data = request.get_json()
    print(data)

    producerID = int(data['producerID'])
    updatedLocation = data['updatedLocation']

    try:
        with db_manager.get_cursor() as cursor:
            cursor.execute("""
                UPDATE producers
                SET "location" = %s
                WHERE "id" = %s
            """, (updatedLocation, producerID))

        return jsonify(
            {
                "code": 201,
                "message": "Updated address successfully!"
            }
        ), 201

    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred updating address!"
            }
        ), 500

# -----------------------------------------------------------------------------------------

# [POST] Edit opening hours
# - Edit opening hours
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/editOpeningHours', methods=['POST'])
def editOpeningHours():
    data = request.get_json()
    print(data)

    producerID = int(data['producerID'])
    updatedOpeningHours = data['updatedOpeningHours']

    # Prepare the updated opening hours for insertion
    opening_hours = (
        updatedOpeningHours.get('Monday', []),
        updatedOpeningHours.get('Tuesday', []),
        updatedOpeningHours.get('Wednesday', []),
        updatedOpeningHours.get('Thursday', []),
        updatedOpeningHours.get('Friday', []),
        updatedOpeningHours.get('Saturday', []),
        updatedOpeningHours.get('Sunday', [])
    )

    try:
        with db_manager.get_cursor() as cursor:
            # Check if opening hours entry already exists
            cursor.execute('SELECT id FROM "producersOpeningHours" WHERE "producerId" = %s', (producerID,))
            existing_entry = cursor.fetchone()

            if existing_entry:
                cursor.execute("""
                    UPDATE "producersOpeningHours" 
                    SET "Monday" = %s, "Tuesday" = %s, "Wednesday" = %s, 
                        "Thursday" = %s, "Friday" = %s, "Saturday" = %s, 
                        "Sunday" = %s 
                    WHERE "producerId" = %s
                """, (*opening_hours, producerID))

            else:
                cursor.execute(
                    """
                        INSERT INTO "producersOpeningHours" ("Monday", "Tuesday", "Wednesday", 
                        "Thursday", "Friday", "Saturday", "Sunday", "producerId") 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (*opening_hours, producerID)
                )

        return jsonify(
            {
                "code": 201,
                "message": "Updated opening hours successfully!"
            }
        ), 201
    
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred updating opening hours!"
            }
        ), 500

# -----------------------------------------------------------------------------------------

# [POST] Delete producer update
# - Delete a producer update with new details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/deleteUpdate', methods=['POST'])
def deleteUpdate():
    data = request.get_json()
    print(data)

    producerID = int(data['producerID'])
    updateID = int(data['updateID'])

    try:
        with db_manager.get_cursor() as cursor:
            # Find existing producer and see if photo exists, if it does delete it from S3 bucket
            cursor.execute('SELECT * FROM "producersUpdates" WHERE "producerId" = %s AND id = %s', (producerID, updateID))
            existingUpdate = cursor.fetchone()

            if existingUpdate:
                if existingUpdate['photo']:
                    s3Images.deleteImageFromS3(existingUpdate['photo'])

                # Delete the producer's update from the database
                cursor.execute('DELETE FROM "producersUpdates" WHERE "producerId" = %s AND id = %s', (producerID, updateID))

                return jsonify(
                    {
                        "code": 201,
                        "message": "Deleted producer's update!"
                    }
                ), 201
            
            else:
                return jsonify(
                    {
                        "code": 404,
                        "message": "Update not found."
                    }
                ), 404
        
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred deleting producer's update!"
            }
        ), 500

# -----------------------------------------------------------------------------------------

# [POST] Edit Q&A
# - Update a producer Q&A with new details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/editQA', methods=['POST'])
def editQA():
    data = request.get_json()
    print(data)

    producerID = int(data['producerID'])
    questionsAnswersID = int(data['questionsAnswersID'])
    answer = data['answer']

    try:
        with db_manager.get_cursor() as cursor:
            cursor.execute('UPDATE "producersQuestionAnswers" SET "answer" = %s WHERE "producerId" = %s AND id = %s', (answer, producerID, questionsAnswersID))

            return jsonify(
                {   
                    "code": 201,
                    "message": "Updated producer's Q&A!"
                }
            ), 201
    
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred updating producer's Q&A!"
            }
        ), 500

# -----------------------------------------------------------------------------------------

# [POST] Delete producer Q&A
# - Delete a producer Q&A with new details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/deleteQA', methods=['POST'])
def deleteQA():
    print("deleteQA")
    data = request.get_json()
    print(data)

    producerID = int(data['producerID'])
    questionsAnswersID = int(data['questionsAnswersID'])

    try:
        with db_manager.get_cursor() as cursor:
            # Get user id from the question
            cursor.execute('SELECT "userId" FROM "producersQuestionAnswers" WHERE "producerId" = %s AND id = %s', (producerID, questionsAnswersID,))
            userID = cursor.fetchone()
            
            cursor.execute('DELETE FROM "producersQuestionAnswers" WHERE "producerId" = %s AND id = %s', (producerID, questionsAnswersID))

            # Deduct points from user for deleting a question
             
            # get points for asking a question
            cursor.execute('SELECT "proofPoints", "ruleName" FROM "pointSystemRules" WHERE id = %s', (15,))
            points = cursor.fetchone()

            # Update user's points
            cursor.execute('UPDATE "pointsRecorder" SET "currentPoints" = "currentPoints" - %s WHERE "userID" = %s', (points['proofPoints'], userID['userId'],))

            print(f"Points deducted from user {userID} for deleting a question")
            
            return jsonify(
                {   
                    "code": 201,
                    "message": "Deleted producer's Q&A!",
                     "pointsDeducted": points['proofPoints'],
                     "rule": points['ruleName']
                }
            ), 201
    
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred deleting producer's Q&A!"
            }
        ), 500
    

# -----------------------------------------------------------------------------------------
# [POST] Edit producer profile claim status
# - Update producer profile with new details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/updateProducerClaimStatus', methods=['POST'])
def updateProducerClaimStatus():
    data = request.get_json()
    print(data)

    producerID = int(data['businessId'])
    claimStatus = data["claimStatus"]

    try:
        with db_manager.get_cursor() as cursor:
            cursor.execute('UPDATE producers SET "claimStatus" = %s WHERE id = %s', (claimStatus, producerID))

            return jsonify(
                {   
                    "code": 201,
                    "message": "Updated claim status successfully!"
                }
            ), 201
    
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred updating claim status!"
            }
        ), 500
    
# -----------------------------------------------------------------------------------------
# [POST] Edit producer profile last check claim status date
# - Update producer profile with new details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/updateProducerClaimStatusCheckDate', methods=['POST'])
def updateProducerClaimStatusCheckDate():
    data = request.get_json()
    print(data)

    producerID = int(data['businessId'])
    claimStatusCheckDate = datetime.strptime(data["claimStatusCheckDate"], "%Y-%m-%dT%H:%M:%S.%fZ")

    try:
        with db_manager.get_cursor() as cursor:
            cursor.execute('UPDATE producers SET "claimStatusCheckDate" = %s WHERE id = %s', (claimStatusCheckDate, producerID))

            return jsonify(
                {   
                    "code": 201,
                    "message": "Updated claim status check date successfully!"
                }
            ), 201
    
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred updating claim status check date!"
            }
        ), 500