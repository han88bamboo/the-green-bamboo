# Port: 5200
# Routes: /editDetails (POST), /addUpdates (POST), /sendQuestions (POST), /sendAnswers (POST), /likeUpdates (POST), /unlikeUpdates (POST), /updateProducerStatus (POST), /addProfileCount (POST), /addNewProfileCount (POST), /editUpdate (POST), /deleteUpdate (POST), /editQA (POST), /deleteQA (POST)
# -----------------------------------------------------------------------------------------

import os
import s3Images
from flask import Blueprint, g, request, jsonify
from bson.objectid import ObjectId
from datetime import datetime

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

# -----------------------------------------------------------------------------------------
# [POST] Edit producer profile
# - Update producer profile with new details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/editDetails', methods=['POST'])
def editDetails():  
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()
    print(data)

    producerID = int(data['producerID'])
    producerName = data['producerName']
    producerDesc = data['producerDesc']
    originCountry = data['originCountry']

    try:
        cur.execute('SELECT * FROM producers WHERE id = %s', (producerID,))
        existingProducer = cur.fetchone()

        if existingProducer:
            if data['image64']:
                if(existingProducer['photo']):
                    s3Images.deleteImageFromS3(existingProducer['photo'])
                image64 = s3Images.uploadBase64ImageToS3(data['image64'])
            else:
                image64 = existingProducer['photo']
            cur.execute(
                """
                UPDATE producers 
                SET 
                    "photo" = %s,
                    "producerName" = %s,
                    "producerDesc" = %s,
                    "originCountry" = %s
                WHERE id = %s
                """,
                (image64, producerName, producerDesc, originCountry, producerID)
            )
            conn.commit()

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
        
    except Exception as e:
        print(str(e))
        conn.rollback()
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred updating profile!"
            }
        ), 500
    
    finally:
        cur.close()

# -----------------------------------------------------------------------------------------
# [POST] Add updates to producer profile
# - Add updates to producer profile
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/addUpdates', methods=['POST'])
def addUpdates():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()
    print(data)

    producerID = int(data['producerID'])
    date = datetime.strptime(data['date'], "%Y-%m-%dT%H:%M:%S.%fZ")
    text = data['text']

    image64 = ''

    if data.get('image64'):
        image64 = s3Images.uploadBase64ImageToS3(data['image64'])

    try:
        cur.execute('INSERT INTO "producersUpdates" ("date", "text", "photo", "producerId") VALUES (%s, %s, %s, %s)', (date, text, image64, producerID))
        conn.commit()

        return jsonify(
            {   
                "code": 201,
                "message": "Update added successfully!"
            }
        ), 201
    
    except Exception as e:
        conn.rollback()
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred creating the update!"
            }
        ), 500
    
    finally:
        cur.close()

# -----------------------------------------------------------------------------------------
# [POST] Send questions to producer
# - Send questions to producer
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/sendQuestions', methods=['POST'])
def sendQuestions():
    conn = g.db
    cur = conn.cursor()

    data = request.get_json()
    print(data)

    producerID = int(data['producerID'])
    question = data['question']
    answer = data['answer']
    date = datetime.strptime(data['date'], "%Y-%m-%dT%H:%M:%S.%fZ")
    userID = int(data['userID'])

    try:
        cur.execute(
            """
                INSERT INTO "producersQuestionAnswers" (question, answer, date, "userId", "producerId")
                VALUES (%s, %s, %s, %s, %s)
            """,
            (question, answer, date, userID, producerID)
        )
        conn.commit()

        return jsonify(
            {
                "code": 201,
                "message": "Question sent successfully!"
            }
        ), 201
    
    except Exception as e:
        conn.rollback()
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred sending the question!"
            }
        ), 500
    
    finally:
        cur.close()

# -----------------------------------------------------------------------------------------
# [POST] Send answers to questions
# - Send answers to questions
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/sendAnswers', methods=['POST'])
def sendAnswers():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()
    print(data)

    producerID = int(data['producerID'])
    questionsAnswersID = int(data['questionsAnswersID'])
    answer = data['answer']

    try:
        cur.execute('UPDATE "producersQuestionAnswers" SET "answer" = %s WHERE "producerId" = %s AND id = %s', (answer, producerID, questionsAnswersID))
        conn.commit()

        return jsonify(
            {   
                "code": 201,
                "message": "Answer sent successfully!"
            }
        ), 201
    
    except Exception as e:
        conn.rollback()
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred sending the answer!"
            }
        ), 500
    
    finally:
        cur.close()

# -----------------------------------------------------------------------------------------
# [POST] Like updates
# - Like updates
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/likeUpdates', methods=['POST'])
def likeUpdates():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()
    print(data)

    producerID = int(data['producerID'])
    updateID = int(data['updateID'])
    userID = int(data['userID'])

    try:
        # Verify that the update exists and belongs to the producer
        cur.execute('SELECT "producerId" FROM "producersUpdates" WHERE "id" = %s', (updateID,))
        existingUpdate = cur.fetchone()

        if not existingUpdate or existingUpdate['producerId'] != producerID:
            return jsonify(
                {
                    "code": 404,
                    "message": "Update not found."
                }
            ), 404
        
        # Insert into the likes table
        cur.execute("""
            INSERT INTO "producerUpdateLikes" ("updateId", "userId")
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING
        """, (updateID, userID))
        conn.commit()

        return jsonify(
            {
                "code": 201,
                "message": "Update liked successfully!"
            }
        ), 201
    
    except Exception as e:
        conn.rollback()
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred liking the update."
            }
        ), 500
    
    finally:
        cur.close()

# -----------------------------------------------------------------------------------------
# [POST] Unlike updates
# - Unlike updates
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/unlikeUpdates', methods=['POST'])
def unlikeUpdates():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()
    print(data)

    producerID = int(data['producerID'])
    updateID = int(data['updateID'])
    userID = int(data['userID'])

    try:
        # Verify that the update exists and belongs to the producer
        cur.execute('SELECT "producerId" FROM "producersUpdates" WHERE "id" = %s', (updateID,))
        existingUpdate = cur.fetchone()

        if not existingUpdate or existingUpdate['producerId'] != producerID:
            return jsonify(
                {
                    "code": 404,
                    "message": "Update not found."
                }
            ), 404
        
        # Remove from the likes table
        cur.execute('DELETE FROM "producerUpdateLikes" WHERE "updateId" = %s AND "userId" = %s', (updateID, userID))
        conn.commit()

        return jsonify(
            {
                "code": 201,
                "message": "Update unliked successfully!"
            }
        ), 201
    
    except Exception as e:
        conn.rollback()
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred unliking the update."
            }
        ), 500

    finally:
        cur.close()
    
# -----------------------------------------------------------------------------------------
# [POST] Edit producer profile
# - Update producer profile with new details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/updateProducerStatus', methods=['POST'])
def updateProducerStatus():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()
    print(data)

    producerID = int(data['businessID'])
    producerName = data['newBusinessData']["businessName"]
    producerDesc = data['newBusinessData']["businessDesc"]
    originCountry = data['newBusinessData']["country"]
    hashedPassword = data['newBusinessData']["hashedPassword"]
    claimStatus = data['newBusinessData']["claimStatus"]

    try:
        cur.execute(
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
        conn.commit()

        return jsonify(
            {
                "code": 201,
                "message": "Updated claim status successfully!"
            }
        ), 201
    
    except Exception as e:
        conn.rollback()
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred updating claim status!"
            }
        ), 500
    
    finally:
        cur.close()


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
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()
    print(data)
    producerID = int(data['businessId'])
    viewsID = int(data['viewsId'])

    try:
        cur.execute('UPDATE "producersProfileViews" SET "count" = "count" + 1 WHERE "producerId" = %s AND id = %s', (producerID, viewsID))
        conn.commit()

        return jsonify(
            {   
                "code": 201,
                "message": "Profile view count updated successfully!"
            }
        ), 201
    
    except Exception as e:
        conn.rollback()
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred updating the profile view count."
            }
        ), 500
    
    finally:
        cur.close()

# -----------------------------------------------------------------------------------------
# [POST] Add new profile view count
# - Add new profile view count
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/addNewProfileCount', methods=['POST'])
def addNewProfileCount():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()
    print(data)
    producerID = int(data['producerID'])
    date = datetime.strptime(data['date'], "%Y-%m-%dT%H:%M:%S.%fZ")

    try:
        cur.execute('SELECT * FROM "producersProfileViews" WHERE "producerId" = %s', (producerID,))
        existingProfileView = cur.fetchone()

        if existingProfileView:
            cur.execute('UPDATE "producersProfileViews" SET "count" = "count" + 1 WHERE "producerId" = %s', (producerID,))
            conn.commit()

        else:
            cur.execute('INSERT INTO "producersProfileViews" ("date", "count", "producerId") VALUES (%s, 1, %s)', (date, producerID))
            conn.commit()

        return jsonify(
            {   
                "code": 201,
                "message": "New profile view count added successfully!"
            }
        ), 201
    
    except Exception as e:
        conn.rollback()
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred updating the new profile view count."
            }
        ), 500
    
    finally:
        cur.close()

# -----------------------------------------------------------------------------------------

# [POST] Edit producer update
# - Update a producer update with new details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/editUpdate', methods=['POST'])
def editUpdate():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()
    print(data)

    producerID = int(data['producerID'])
    updateID = int(data['updateID'])
    update = data['update']
    image64 = data.get('image64', '')

    try:
        # Find existing producer and check for the existing update
        cur.execute('SELECT * FROM "producersUpdates" WHERE "producerId" = %s AND id = %s', (producerID, updateID))
        existingUpdate = cur.fetchone()

        if existingUpdate:
            # Delete old photo from S3 if it exists
            if existingUpdate['photo']:
                s3Images.deleteImageFromS3(existingUpdate['photo'])

            # Upload new image to S3 if it exists
            if image64:
                image64 = s3Images.uploadBase64ImageToS3(image64)

            # Update the producer's update in the database
            cur.execute(
                """
                UPDATE "producersUpdates"
                SET 
                    "text" = %s,
                    "photo" = %s
                WHERE "producerId" = %s AND id = %s
                """,
                (update, image64, producerID, updateID)
            )
            conn.commit()

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
        conn.rollback()
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred updating producer's update!"
            }
        ), 500
    
    finally:
        cur.close()

# -----------------------------------------------------------------------------------------

# [POST] Delete producer update
# - Delete a producer update with new details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/deleteUpdate', methods=['POST'])
def deleteUpdate():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()
    print(data)

    producerID = int(data['producerID'])
    updateID = int(data['updateID'])

    try:
        # Find existing producer and see if photo exists, if it does delete it from S3 bucket
        cur.execute('SELECT * FROM "producersUpdates" WHERE "producerId" = %s AND id = %s', (producerID, updateID))
        existingUpdate = cur.fetchone()

        if existingUpdate:
            if existingUpdate['photo']:
                s3Images.deleteImageFromS3(existingUpdate['photo'])

            # Delete the producer's update from the database
            cur.execute('DELETE FROM "producersUpdates" WHERE "producerId" = %s AND id = %s', (producerID, updateID))
            conn.commit()

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
        conn.rollback()
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred deleting producer's update!"
            }
        ), 500
    
    finally:
        cur.close()

# -----------------------------------------------------------------------------------------

# [POST] Edit Q&A
# - Update a producer Q&A with new details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/editQA', methods=['POST'])
def editQA():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()
    print(data)

    producerID = int(data['producerID'])
    questionsAnswersID = int(data['questionsAnswersID'])
    answer = data['answer']

    try:
        cur.execute('UPDATE "producersQuestionAnswers" SET "answer" = %s WHERE "producerId" = %s AND id = %s', (answer, producerID, questionsAnswersID))
        conn.commit()

        return jsonify(
            {   
                "code": 201,
                "message": "Updated producer's Q&A!"
            }
        ), 201
    
    except Exception as e:
        conn.rollback()
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred updating producer's Q&A!"
            }
        ), 500
    
    finally:
        cur.close()

# -----------------------------------------------------------------------------------------

# [POST] Delete producer Q&A
# - Delete a producer Q&A with new details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/deleteQA', methods=['POST'])
def deleteQA():
    print("deleteQA")
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()
    print(data)

    producerID = int(data['producerID'])
    questionsAnswersID = int(data['questionsAnswersID'])

    try:
        cur.execute('DELETE FROM "producersQuestionAnswers" WHERE "producerId" = %s AND id = %s', (producerID, questionsAnswersID))
        conn.commit()

        return jsonify(
            {   
                "code": 201,
                "message": "Deleted producer's Q&A!"
            }
        ), 201
    
    except Exception as e:
        conn.rollback()
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred deleting producer's Q&A!"
            }
        ), 500
    
    finally:
        cur.close()
    

# -----------------------------------------------------------------------------------------
# [POST] Edit producer profile claim status
# - Update producer profile with new details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/updateProducerClaimStatus', methods=['POST'])
def updateProducerClaimStatus():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()
    print(data)

    producerID = int(data['businessId'])
    claimStatus = data["claimStatus"]

    try:
        cur.execute('UPDATE producers SET "claimStatus" = %s WHERE id = %s', (claimStatus, producerID))
        conn.commit()

        return jsonify(
            {   
                "code": 201,
                "message": "Updated claim status successfully!"
            }
        ), 201
    
    except Exception as e:
        conn.rollback()
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred updating claim status!"
            }
        ), 500
    
    finally:
        cur.close()
    
# -----------------------------------------------------------------------------------------
# [POST] Edit producer profile last check claim status date
# - Update producer profile with new details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/updateProducerClaimStatusCheckDate', methods=['POST'])
def updateProducerClaimStatusCheckDate():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()
    print(data)

    producerID = int(data['businessId'])
    claimStatusCheckDate = datetime.strptime(data["claimStatusCheckDate"], "%Y-%m-%dT%H:%M:%S.%fZ")

    try:
        cur.execute('UPDATE producers SET "claimStatusCheckDate" = %s WHERE id = %s', (claimStatusCheckDate, producerID))
        conn.commit()

        return jsonify(
            {   
                "code": 201,
                "message": "Updated claim status check date successfully!"
            }
        ), 201
    
    except Exception as e:
        conn.rollback()
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred updating claim status check date!"
            }
        ), 500
    
    finally:
        cur.close()
