# Port: 5300
# Routes: /editDetails (POST), /addUpdates (POST), /sendQuestions (POST), /sendAnswers (POST), /likeUpdates (POST), /unlikeUpdates (POST)
#         /editOpeningHours (POST), /editPublicHolidays (POST), /editReservationDetails (POST), /editMenu (POST)
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
# [POST] Edit venue profile
# - Update venue profile with new details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@app.route('/editDetails', methods=['POST'])
def editDetails():

    # fetch sent data
    data = request.get_json()
    print(data)

    # extract components of the data
    venueID = data['venueID']
    venueName = data['venueName']
    venueDesc = data['venueDesc']
    originLocation = data['originLocation']
    image64 = data['image64']

    try: 
        update = db.venues.update_one({'_id': ObjectId(venueID)}, 
                                        {'$set': {
                                                    'photo': image64,
                                                    'venueName': venueName,
                                                    'venueDesc': venueDesc,
                                                    'originLocation': originLocation
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
# [POST] Add updates to venue profile
# - Add updates to the venue profile
# - Possible return codes: 201 (Updated), 500 (Error during update)
@app.route('/addUpdates', methods=['POST'])
def addUpdates():

    # fetch sent data
    data = request.get_json()
    print(data)

    # extract components of the data
    venueID = data['venueID']
    date = datetime.strptime(data['date'], "%Y-%m-%dT%H:%M:%S.%fZ")
    text = data['text']
    image64 = data['image64']

    try:
        submitReq = db.venues.update_one(
            {'_id': ObjectId(venueID)},
            {'$push': {'updates': 
                        {
                            "_id": ObjectId(),
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
# [POST] Send questions to venue profile
# - Send questions to the venue profile
# - Possible return codes: 201 (Updated), 500 (Error during update)
@app.route('/sendQuestions', methods=['POST'])
def sendQuestions():

    # fetch sent data
    data = request.get_json()
    print(data)

    # extract components of the data
    venueID = data['venueID']
    question = data['question']
    answer = data['answer']
    date = datetime.strptime(data['date'], "%Y-%m-%dT%H:%M:%S.%fZ")

    try:
        submitReq = db.venues.update_one(
            {'_id': ObjectId(venueID)},
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
# [POST] Send answers to venue profile
# - Send answers to the venue profile
# - Possible return codes: 201 (Updated), 500 (Error during update)
@app.route('/sendAnswers', methods=['POST'])
def sendAnswers():

    # fetch sent data
    data = request.get_json()
    print(data)

    # extract components of the data
    venueID = data['venueID']
    questionsAnswersID = data['questionsAnswersID']
    answer = data['answer']

    try:
        submitReq = db.venues.update_one(
            {'_id': ObjectId(venueID), 'questionsAnswers._id': ObjectId(questionsAnswersID)},
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
    venueID = data['venueID']
    updateID = data['updateID']
    userID = data['userID']

    try: 
        likeUpdate = db.venues.update_one(
            {'_id': ObjectId(venueID), 'updates._id': ObjectId(updateID)},
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
    venueID = data['venueID']
    updateID = data['updateID']
    userID = data['userID']

    try: 
        unlikeUpdate = db.venues.update_one(
            {'_id': ObjectId(venueID), 'updates._id': ObjectId(updateID)},
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
                "message": "An error occurred unliking the update!"
            }
        ), 500

# -----------------------------------------------------------------------------------------
# [POST] Edit address
# - Edit address
# - Possible return codes: 201 (Updated), 500 (Error during update)
@app.route('/editAddress', methods=['POST'])
def editAddress():
    data = request.get_json()
    print(data)
    venueID = data['venueID']
    updatedAddress = data['updatedAddress']

    try: 
        editAddress = db.venues.update_one(
            {'_id': ObjectId(venueID)},
            {'$set': {'address': updatedAddress}}
        )
        return jsonify(
            {   
                "code": 201,
                "message": "Address edited successfully!"
            }
        ), 201
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred editing the address!"
            }
        ), 500

# -----------------------------------------------------------------------------------------
# [POST] Edit opening hours
# - Edit opening hours
# - Possible return codes: 201 (Updated), 500 (Error during update)
@app.route('/editOpeningHours', methods=['POST'])
def editOpeningHours():
    data = request.get_json()
    print(data)
    venueID = data['venueID']
    updatedOpeningHours = data['updatedOpeningHours']

    try: 
        editOpeningHours = db.venues.update_one(
            {'_id': ObjectId(venueID)},
            {'$set': {'openingHours': updatedOpeningHours}}
        )
        return jsonify(
            {   
                "code": 201,
                "message": "Opening hours edited successfully!"
            }
        ), 201
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred editing the opening hours!"
            }
        ), 500

# -----------------------------------------------------------------------------------------
# [POST] Edit public holidays
# - Edit public holidays
# - Possible return codes: 201 (Updated), 500 (Error during update)
@app.route('/editPublicHolidays', methods=['POST'])
def editPublicHolidays():
    data = request.get_json()
    print(data)
    venueID = data['venueID']
    updatedPublicHolidays = data['updatedPublicHolidays']

    try: 
        editOpeningHours = db.venues.update_one(
            {'_id': ObjectId(venueID)},
            {'$set': {'publicHolidays': updatedPublicHolidays}}
        )
        return jsonify(
            {   
                "code": 201,
                "message": "Public holidays details edited successfully!"
            }
        ), 201
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred editing the public holidays!"
            }
        ), 500

# -----------------------------------------------------------------------------------------
# [POST] Edit reservation details
# - Edit reservation details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@app.route('/editReservationDetails', methods=['POST'])
def editReservationDetails():
    data = request.get_json()
    print(data)
    venueID = data['venueID']
    updatedReservationDetails = data['updatedReservationDetails']

    try: 
        editOpeningHours = db.venues.update_one(
            {'_id': ObjectId(venueID)},
            {'$set': {'reservationDetails': updatedReservationDetails}}
        )
        return jsonify(
            {   
                "code": 201,
                "message": "Reservation details edited successfully!"
            }
        ), 201
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred editing the reservation details!"
            }
        ), 500

# -----------------------------------------------------------------------------------------
# [POST] Add listing to menu
# - Add listing to menu
# - Possible return codes: 201 (Updated), 500 (Error during update)
@app.route('/addListingToMenu', methods=['POST'])
def addListingToMenu():
    data = request.get_json()
    print(data)
    venueID = data['venueID']
    menuOrder = data['menuOrder']
    listingID = data['listingID']
    itemPrice = data['itemPrice']
    servingType = data['servingType']
    sectionName = data['sectionName']

    try: 
        addListing = db.venues.update_one(
            {'_id': ObjectId(venueID), 'menu.sectionName': sectionName},
            {'$push': {'menu.$.listingsID': 
                        {
                            'itemOrder': menuOrder,
                            'itemID': ObjectId(listingID),
                            'itemPrice': itemPrice,
                            'servingType': ObjectId(servingType),
                            'itemAvailability': True,
                        }
                    }
                }
        )
        return jsonify(
            {   
                "code": 201,
                "message": "Listing added to menu successfully!"
            }
        ), 201
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred adding the listing to menu!"
            }
        ), 500
# -----------------------------------------------------------------------------------------


#  -----------------------------------------------------------------------------------------
# [POST] Change Section Name 
# - Change Section Name
# - Possible return codes: 201 (Updated), 500 (Error during update)
@app.route('/editSectionName', methods=['PUT'])
def editSectionName():
    data = request.get_json()
    print(data)
    venueID = data['venueID']
    sectionOrder = data['order']
    sectionName = data['sectionName']

    try: 
        addListing = db.venues.update_one(
            {'_id': ObjectId(venueID), 'menu.order': 0},
            {'$set': {'menu.$.sectionName': sectionName}}
        )
        return jsonify(
            {   
                "code": 201,
                "message": "Section Name changed successfully!"
            }
        ), 201
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "Section Name was not changed"}
        ), 500
# -----------------------------------------------------------------------------------------
    
# -----------------------------------------------------------------------------------------
# [POST] Edit menu
# - Edit menu
# - Possible return codes: 201 (Updated), 500 (Error during update)
@app.route('/editMenu', methods=['POST'])
def editMenu():
    data = request.get_json()
    print(data)
    venueID = data['venueID']
    updatedMenu = data['updatedMenu']

    try: 
        editMenu = db.venues.update_one(
            {'_id': ObjectId(venueID)},
            {'$set': {'menu': updatedMenu}}
        )
        return jsonify(
            {   
                "code": 201,
                "message": "Menu edited successfully!"
            }
        ), 201
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred while editing the menu!"
            }
        ), 500
    
# -----------------------------------------------------------------------------------------
# [POST] Edit venue profile
# - Update producer profile with new details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@app.route('/updateVenueStatus', methods=['POST'])
def updateVenueStatus():
    # fetch sent data
    data = request.get_json()
    print(data)

    # extract components of the data
    venueID = data['businessID']
    venueName = data['newBusinessData']["businessName"]
    venueDesc = data['newBusinessData']["businessDesc"]
    originLocation = data['newBusinessData']["country"]
    hashedPassword = data['newBusinessData']["hashedPassword"]
    claimStatus = data['newBusinessData']["claimStatus"]

    try: 
        update = db.venues.update_one({'_id': ObjectId(venueID)}, 
                                         {'$set': {
                                                'venueName': venueName,
                                                'venueDesc': venueDesc,
                                                'originLocation': originLocation,
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

# [POST] Edit venue update
# - Update a venue update with new details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@app.route('/editUpdate', methods=['POST'])
def editUpdate():

    # fetch sent data
    data = request.get_json()
    print(data)

    # extract components of the data
    venueID = data['venueID']
    updateID = data['updateID']
    update = data['update']
    image64 = data['image64']

    try: 
        update = db.venues.update_one(
            {'_id': ObjectId(venueID), 'updates._id': ObjectId(updateID)},
            {'$set': 
                {'updates.$.text': update,
                'updates.$.photo': image64}
        }
        )

        return jsonify(
            {   
                "code": 201,
                "message": "Updated venue's update!"
            }
        ), 201
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred updating venue's update!"
            }
        ), 500

# -----------------------------------------------------------------------------------------

# [POST] Delete venue update
# - Delete a venue update with new details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@app.route('/deleteUpdate', methods=['POST'])
def deleteUpdate():

    # fetch sent data
    data = request.get_json()
    print(data)

    # extract components of the data
    venueID = data['venueID']
    updateID = data['updateID']

    try: 
        deleteUpdate = db.venues.update_one(
            {'_id': ObjectId(venueID)},
            {'$pull': {'updates': {'_id': ObjectId(updateID)}}}
        )

        return jsonify(
            {   
                "code": 201,
                "message": "Deleted venue's update!"
            }
        ), 201
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred deleting venue's update!"
            }
        ), 500


# -----------------------------------------------------------------------------------------

# [POST] Edit Q&A
# - Update a venue Q&A with new details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@app.route('/editQA', methods=['POST'])
def editQA():

    # fetch sent data
    data = request.get_json()
    print(data)

    # extract components of the data
    venueID = data['venueID']
    questionsAnswersID = data['questionsAnswersID']
    answer = data['answer']

    try: 
        updateQA = db.venues.update_one(
            {'_id': ObjectId(venueID), 'questionsAnswers._id': ObjectId(questionsAnswersID)},
            {'$set': {'questionsAnswers.$.answer': answer}}
        )

        return jsonify(
            {   
                "code": 201,
                "message": "Updated venue's Q&A!"
            }
        ), 201
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred updating venue's Q&A!"
            }
        ), 500

# -----------------------------------------------------------------------------------------

# [POST] Delete venue Q&A
# - Delete a venue Q&A with new details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@app.route('/deleteQA', methods=['POST'])
def deleteQA():

    # fetch sent data
    data = request.get_json()
    print(data)

    # extract components of the data
    venueID = data['venueID']
    questionsAnswersID = data['questionsAnswersID']
    answer = data['answer']

    try: 
        deleteQA = db.venues.update_one(
            {'_id': ObjectId(venueID), 'questionsAnswers._id': ObjectId(questionsAnswersID)},
            {'$set': {'questionsAnswers.$.answer': answer}}
        )

        return jsonify(
            {   
                "code": 201,
                "message": "Deleted venue's Q&A!"
            }
        ), 201
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred deleting venue's Q&A!"
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
    venueID = data['venueID']
    viewsID = data['viewsID']

    try: 
        addProfileCount = db.venuesProfileViews.update_one(
            {'_id': ObjectId(venueID), 'views._id': ObjectId(viewsID)},
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
    venueID = data['venueID']
    date = datetime.strptime(data['date'], "%Y-%m-%dT%H:%M:%S.%fZ")

    try: 
        addNewProfileCount = db.venuesProfileViews.update_one(
            {'_id': ObjectId(venueID)},
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
            addNewProfileCount = db.venuesProfileViews.insert_one(
                {
                    '_id': ObjectId(venueID),
                    'venueID': ObjectId(venueID),
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5300)