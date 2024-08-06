# Port: 5022
# Routes: /voteReview (POST), /updateReview/<id> (PUT)
# -----------------------------------------------------------------------------------------

import os
import s3Images
from flask import Blueprint, g, request, jsonify
from bson.objectid import ObjectId
from datetime import datetime

from scripts.adminFunctions import hash_password
from scripts.createReview import create_username

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

# -----------------------------------------------------------------------------------------
# [POST] Vote review
# - Update review with new votes
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/voteReview', methods=['POST'])
def voteReview():
    db = g.db
    data = request.get_json()
    print(data)
    reviewID = data['reviewID']
    userVotes = data['userVotes']

    for voteType in userVotes:
        votes = userVotes[voteType]
        for vote in votes:
            if isinstance(vote["userID"], str):
                vote["userID"] = ObjectId(vote["userID"])
            if isinstance(vote["date"], str):
                vote["date"] = datetime.strptime(vote["date"], "%Y-%m-%dT%H:%M:%S.%fZ")

    try: 
        voteReview = db.reviews.update_one({'_id': ObjectId(reviewID['$oid'])}, {'$set': {'userVotes': userVotes}})

        return jsonify(
            {   
                "code": 201,
                "data": userVotes
            }
        ), 201
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": {
                    "data": userVotes
                },
                "message": "An error occurred updating the image."
            }
        ), 500

# -----------------------------------------------------------------------------------------
    
# [PUT] Update review
# - Update review with review metrics
# - Possible return codes: 200 (Updated), 400(Review not found), 500 (Error during update)
@blueprint.route('/updateReview/<id>', methods=['PUT'])
def updateReview(id):
    db = g.db
    reviewID= ObjectId(id)
    data = request.get_json()
    existingReview = db.reviews.find_one({'_id': ObjectId(id)})
    data['reviewTarget'] = ObjectId(data['reviewTarget'])  # Convert reviewTarget to ObjectId
    data['userID'] = ObjectId(data['userID'])  # Convert userID to ObjectId

    # get review address
    locationAddress=data['address']
    locationName=data['location']

    
    # create a dictionary of addresses from venue documents and store thier ids
    
    condition_1= db.venues.count_documents({ "address": locationAddress })
    condition_2= db.venues.count_documents({ "venueName": locationName })

    # see if address is in the dictionary, if not insert a new venue
    if locationAddress != "": 
        if condition_2==0 or condition_1==0 :

            # Create a username for the venue
            username = create_username(locationName)

            venue_to_insert = {
                "venueName": data["location"],
                "address": locationAddress,
                "venueType": "",
                "originLocation": "",
                "venueDesc": "",
                "menu": [],
                "hashedPassword": hash_password(username,"admin1234"),
                "claimStatus": False,
                "openingHours": {
                "Monday": [
                    "",
                    ""
                ],
                "Tuesday": [
                    "",
                    ""
                ],
                "Wednesday": [
                    "",
                    ""
                ],
                "Thursday": [
                    "",
                    ""
                ],
                "Friday": [
                    "",
                    ""
                ],
                "Saturday": [
                    "",
                    ""
                ],
                "Sunday": [
                    "",
                    ""
                ]
                },
                "photo": "",
                "updates": [],
                "questionsAnswers": [],
                "reservationDetails": "",
                "publicHolidays": "",
                "username": username
            }

            db.venues.insert_one(venue_to_insert)
            

    if len(data['taggedUsers']) >0:
        temp_tag_id =[]
        for userId in data['taggedUsers']:
            temp_tag_id.append(ObjectId(userId))
        data['taggedUsers'] = temp_tag_id
    if len(data['flavorTag']) >0:
        temp_flavour_tag =[]
        for flavour_id in data['flavorTag']:
            temp_flavour_tag.append(ObjectId(flavour_id['$oid']))
        data['flavorTag'] = temp_flavour_tag

    if(existingReview == None):
        return jsonify(
            {   
                "code": 400,
                "data": {
                    "listingName": data['reviewDesc']
                },
                "message": "Review does not exist."
            }
        ), 400

    try: 
        # check if photo url exists, delete and reupload new one, else do nothing
        if existingReview['photo']:
            s3Images.deleteImageFromS3(existingReview['photo'])
        if data['photo']:
            data['photo'] = s3Images.uploadBase64ImageToS3(data['photo'])

        voteReview = db.reviews.update_one({'_id': reviewID}, {'$set': data})
        return jsonify(
            {   
                "code": 200,
                "data": data['reviewDesc']
            }
        ), 201
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": {
                    "data": data['reviewDesc']
                },
                "message": "An error occurred updating the review."
            }
        ), 500
