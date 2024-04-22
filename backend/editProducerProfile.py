# Port: 5200
# Routes: /editDetails (POST), /addUpdates (POST), /sendQuestions (POST), /sendAnswers (POST), /likeUpdates (POST), /unlikeUpdates (POST)
# -----------------------------------------------------------------------------------------

import bson
import json
from bson import json_util
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS

from bson.objectid import ObjectId

from gridfs import GridFS
import os
from datetime import datetime

from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)  # Allow all requests

load_dotenv()
app.config["MONGO_URI"] = os.getenv('MONGO_DB_URL')
db = PyMongo(app).db

mongo = PyMongo(app)
fs = GridFS(mongo.db)

# -----------------------------------------------------------------------------------------
# [POST] Edit producer profile
# - Update producer profile with new details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@app.route('/editDetails', methods=['POST'])
def editDetails():

    # fetch sent data
    data = request.get_json()
    print(data)

    # extract components of the data
    producerID = data['producerID']
    image64 = data['image64']
    producerName = data['producerName']
    producerDesc = data['producerDesc']
    originCountry = data['originCountry']

    try: 
        update = db.producers.update_one({'_id': ObjectId(producerID)}, 
                                        {'$set': {
                                                    'photo': image64,
                                                    'producerName': producerName,
                                                    'producerDesc': producerDesc,
                                                    'originCountry': originCountry
                                                    }
                                            })

        return jsonify(
            {   
                "code": 201,
                "message": "Updated profile successfully!"
            }
        ), 201
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred updating profile!"
            }
        ), 500

# -----------------------------------------------------------------------------------------
# [POST] Add updates to producer profile
# - Add updates to producer profile
# - Possible return codes: 201 (Updated), 500 (Error during update)
@app.route('/addUpdates', methods=['POST'])
def addUpdates():

    # fetch sent data
    data = request.get_json()
    print(data)

    # extract components of the data
    producerID = data['producerID']
    date = datetime.strptime(data['date'], "%Y-%m-%dT%H:%M:%S.%fZ")
    text = data['text']
    image64 = data['image64']

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
@app.route('/sendQuestions', methods=['POST'])
def sendQuestions():

    # fetch sent data
    data = request.get_json()
    print(data)

    # extract components of the data
    producerID = data['producerID']
    question = data['question']
    answer = data['answer']
    date = datetime.strptime(data['date'], "%Y-%m-%dT%H:%M:%S.%fZ")

    try:
        submitReq = db.producers.update_one(
            {'_id': ObjectId(producerID)},
            {'$push': {'questionsAnswers': 
                        {
                            '_id': ObjectId(),
                            'question': question,
                            'answer': answer,
                            'date': date,
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
@app.route('/sendAnswers', methods=['POST'])
def sendAnswers():

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
@app.route('/likeUpdates', methods=['POST'])
def likeUpdates():
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
@app.route('/unlikeUpdates', methods=['POST'])
def unlikeUpdates():
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
@app.route('/updateProducerStatus', methods=['POST'])
def updateProducerStatus():

    # fetch sent data
    data = request.get_json()
    print(data)

    # extract components of the data
    producerID = data['businessID']
    producerName = data['newBusinessData']["businessName"]
    producerDesc = data['newBusinessData']["businessDesc"]
    originCountry = data['newBusinessData']["country"]
    hashedPassword = data['newBusinessData']["hashedPassword"]
    claimStatus = data['newBusinessData']["claimStatus"]

    try: 
        update = db.producers.update_one({'_id': ObjectId(producerID)}, 
                                         {'$set': {
                                                'producerName': producerName,
                                                'producerDesc': producerDesc,
                                                'originCountry': originCountry,
                                                'hashedPassword': hashedPassword,
                                                'claimStatus': claimStatus
                                            }})

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
# [POST] Add profile view count
# - Add profile view count
# - Possible return codes: 201 (Updated), 500 (Error during update)
@app.route('/addProfileCount', methods=['POST'])
def addProfileCount():
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
@app.route('/addNewProfileCount', methods=['POST'])
def addNewProfileCount():
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
@app.route('/editUpdate', methods=['POST'])
def editUpdate():

    # fetch sent data
    data = request.get_json()
    print(data)

    # extract components of the data
    producerID = data['producerID']
    updateID = data['updateID']
    update = data['update']
    image64 = data['image64']

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
@app.route('/deleteUpdate', methods=['POST'])
def deleteUpdate():

    # fetch sent data
    data = request.get_json()
    print(data)

    # extract components of the data
    producerID = data['producerID']
    updateID = data['updateID']

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
@app.route('/editQA', methods=['POST'])
def editQA():

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
@app.route('/deleteQA', methods=['POST'])
def deleteQA():

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5200)