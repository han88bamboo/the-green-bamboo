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
    image64 = data.get('image64', '')

    try:
        cur.execute('SELECT * FROM producers WHERE id = %s', (producerID,))
        existingProducer = cur.fetchone()

        if existingProducer:
            if existingProducer['photo']:
                s3Images.deleteImageFromS3(existingProducer['photo'])

            if image64:
                image64 = s3Images.uploadBase64ImageToS3(image64)

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
    db = g.db

    # fetch sent data
    data = request.get_json()
    print(data)

    # extract components of the data
    producerID = data['producerID']
    date = datetime.strptime(data['date'], "%Y-%m-%dT%H:%M:%S.%fZ")
    text = data['text']
    image64 = s3Images.uploadBase64ImageToS3(data['image64']) 

    try:
        submitReq = db.producers.update_one(
            {'_id': ObjectId(producerID)},
            {'$push': {'updates': 
                        {
                            '_id': ObjectId(),
                            'date': date,
                            'text': text,
                            'photo': image64,
                            'likes': []
                        }
                    }
            }
        )

        return jsonify( 
            {   
                "code": 201,
                "message": "Update added successfully!"
            }
        ), 201
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred creating the update!"
            }
        ), 500

# -----------------------------------------------------------------------------------------
# [POST] Send questions to producer
# - Send questions to producer
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/sendQuestions', methods=['POST'])
def sendQuestions():
    db = g.db

    # fetch sent data
    data = request.get_json()
    print(data)

    # extract components of the data
    producerID = data['producerID']
    question = data['question']
    answer = data['answer']
    date = datetime.strptime(data['date'], "%Y-%m-%dT%H:%M:%S.%fZ")
    userID = data['userID']

    try:
        submitReq = db.producers.update_one(
            {'_id': ObjectId(producerID)},
            {'$push': {'questionsAnswers': 
                        {
                            '_id': ObjectId(),
                            'question': question,
                            'answer': answer,
                            'date': date,
                            'userID': ObjectId(userID)
                        }
                    }
            }
        )

        return jsonify( 
            {   
                "code": 201,
                "message": "Question sent successfully!"
            }
        ), 201
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred sending the question!"
            }
        ), 500

# -----------------------------------------------------------------------------------------
# [POST] Send answers to questions
# - Send answers to questions
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/sendAnswers', methods=['POST'])
def sendAnswers():
    db = g.db

    # fetch sent data
    data = request.get_json()
    print(data)

    # extract components of the data
    producerID = data['producerID']
    questionsAnswersID = data['questionsAnswersID']
    answer = data['answer']

    try:
        submitReq = db.producers.update_one(
            {'_id': ObjectId(producerID), 'questionsAnswers._id': ObjectId(questionsAnswersID)},
            {'$set': {'questionsAnswers.$.answer': answer}}
        )
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
                "data": data,
                "message": "An error occurred sending the answer!"
            }
        ), 500

# -----------------------------------------------------------------------------------------
# [POST] Like updates
# - Like updates
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/likeUpdates', methods=['POST'])
def likeUpdates():
    db = g.db
    data = request.get_json()
    print(data)
    producerID = data['producerID']
    updateID = data['updateID']
    userID = data['userID']

    try: 
        likeUpdate = db.producers.update_one(
            {'_id': ObjectId(producerID), 'updates._id': ObjectId(updateID)},
            {'$push': {'updates.$.likes': ObjectId(userID)}}
        )
        return jsonify(
            {   
                "code": 201,
                "message": "Update liked successfully!"
            }
        ), 201
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred liking the update!"
            }
        ), 500

# -----------------------------------------------------------------------------------------
# [POST] Unlike updates
# - Unlike updates
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/unlikeUpdates', methods=['POST'])
def unlikeUpdates():
    db = g.db
    data = request.get_json()
    print(data)
    producerID = data['producerID']
    updateID = data['updateID']
    userID = data['userID']

    try: 
        unlikeUpdate = db.producers.update_one(
            {'_id': ObjectId(producerID), 'updates._id': ObjectId(updateID)},
            {'$pull': {'updates.$.likes': ObjectId(userID)}}
        )
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
@blueprint.route('/addProfileCount', methods=['POST'])
def addProfileCount():
    db = g.db
    data = request.get_json()
    print(data)
    producerID = data['producerID']
    viewsID = data['viewsID']

    try: 
        addProfileCount = db.producersProfileViews.update_one(
            {'_id': ObjectId(producerID), 'views._id': ObjectId(viewsID)},
            {'$inc': {'views.$.count': 1}}
        )
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
    db = g.db
    data = request.get_json()
    print(data)
    producerID = data['producerID']
    date = datetime.strptime(data['date'], "%Y-%m-%dT%H:%M:%S.%fZ")

    try: 
        addNewProfileCount = db.producersProfileViews.update_one(
            {'_id': ObjectId(producerID)},
            {'$push': {'views': 
                        {
                            '_id': ObjectId(),
                            'date': date,
                            'count': 1
                        }
                    }
            }
        )
        # If addNewProfileCount does not update any documents, create a new document
        if addNewProfileCount.matched_count == 0:
            addNewProfileCount = db.producersProfileViews.insert_one(
                {
                    '_id': ObjectId(producerID),
                    'producerID': ObjectId(producerID),
                    'views': 
                        [{
                            '_id': ObjectId(),
                            'date': date,
                            'count': 1
                        }]
                }
            )
        return jsonify(
            {   
                "code": 201,
                "message": "New profile view count updated successfully!"
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
    db = g.db

    # fetch sent data
    data = request.get_json()
    print(data)

    # extract components of the data
    producerID = data['producerID']
    updateID = data['updateID']
    update = data['update']

    # find existing update and check if photo exists, if it does, delete it from s3 bucket, then upload new image to bucket
    # Aggregation pipeline bye chatgpt
    # pipeline = [
    #     {
    #         "$match": {
    #             "_id": ObjectId(producerID),
    #             "updates._id": ObjectId(updateID)
    #         }
    #     },
    #     {
    #         "$project": {
    #             "updates": {
    #                 "$filter": {
    #                     "input": "$updates",
    #                     "as": "update",
    #                     "cond": { "$eq": ["$$update._id", ObjectId(updateID)] }
    #                 }
    #             }
    #         }
    #     }
    # ]
    # result = list(db.producers.aggregate(pipeline))
    # if result and 'updates' in result[0] and result[0]['updates']:
    #     photo = result[0]['updates'][0].get('photo', None)
    #     s3Images.deleteImageFromS3(photo)
    
    existingProducer = db.producers.find_one({"_id": ObjectId(producerID)})
    for updates in existingProducer['updates']:
        if updates['_id'] == ObjectId(updateID):
            if(updates['photo']):
                s3Images.deleteImageFromS3(updates['photo']) 
    if(data['image64']):
        image64 = s3Images.uploadBase64ImageToS3(data['image64'])
    
    try: 
        update = db.producers.update_one(
            {'_id': ObjectId(producerID), 'updates._id': ObjectId(updateID)},
            {'$set': 
                {'updates.$.text': update,
                'updates.$.photo': image64}
            }
        )

        return jsonify(
            {   
                "code": 201,
                "message": "Updated producer's update!"
            }
        ), 201
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

# [POST] Delete producer update
# - Delete a producer update with new details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/deleteUpdate', methods=['POST'])
def deleteUpdate():
    db = g.db

    # fetch sent data
    data = request.get_json()
    print(data)

    # extract components of the data
    producerID = data['producerID']
    updateID = data['updateID']

    # find update and see if photo exist, if it does delete it from s3 bucket
    existingProducer = db.producers.find_one({"_id": ObjectId(producerID)})
    for update in existingProducer['updates']:
        if update['_id'] == ObjectId(updateID):
            if(update['photo']):
                s3Images.deleteImageFromS3(update['photo']) 

    try: 
        deleteUpdate = db.producers.update_one(
            {'_id': ObjectId(producerID)},
            {'$pull': {'updates': {'_id': ObjectId(updateID)}}}
        )

        return jsonify(
            {   
                "code": 201,
                "message": "Deleted producer's update!"
            }
        ), 201
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
    db = g.db

    # fetch sent data
    data = request.get_json()
    print(data)

    # extract components of the data
    producerID = data['producerID']
    questionsAnswersID = data['questionsAnswersID']
    answer = data['answer']

    try: 
        updateQA = db.producers.update_one(
            {'_id': ObjectId(producerID), 'questionsAnswers._id': ObjectId(questionsAnswersID)},
            {'$set': {'questionsAnswers.$.answer': answer}}
        )

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
    db = g.db

    # fetch sent data
    data = request.get_json()
    print(data)

    # extract components of the data
    producerID = data['producerID']
    questionsAnswersID = data['questionsAnswersID']
    answer = data['answer']

    try: 
        deleteQA = db.producers.update_one(
            {'_id': ObjectId(producerID), 'questionsAnswers._id': ObjectId(questionsAnswersID)},
            {'$set': {'questionsAnswers.$.answer': answer}}
        )

        return jsonify(
            {   
                "code": 201,
                "message": "Deleted producer's Q&A!"
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
    # db = g.db

    # # fetch sent data
    # data = request.get_json()
    # print(data)

    # # extract components of the data
    # producerID = data['businessId']
    # claimStatus = data["claimStatus"]

    # try: 
    #     update = db.producers.update_one({'_id': ObjectId(producerID)}, 
    #                                      {'$set': {
    #                                             'claimStatus': claimStatus
    #                                         }})

    #     return jsonify(
    #         {   
    #             "code": 201,
    #             "message": "Updated claim status successfully!"
    #         }
    #     ), 201
    # except Exception as e:
    #     print(str(e))
    #     return jsonify(
    #         {
    #             "code": 500,
    #             "data": data,
    #             "message": "An error occurred updating claim status!"
    #         }
    #     ), 500

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
    db = g.db

    # fetch sent data
    data = request.get_json()
    print(data)

    # extract components of the data
    producerID = data['businessId']
    # claimStatusCheckDate = data["claimStatusCheckDate"]
    claimStatusCheckDate = datetime.strptime(data["claimStatusCheckDate"], "%Y-%m-%dT%H:%M:%S.%fZ")

    try: 
        update = db.producers.update_one({'_id': ObjectId(producerID)}, 
                                         {'$set': {
                                                'claimStatusCheckDate': claimStatusCheckDate
                                            }})

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
