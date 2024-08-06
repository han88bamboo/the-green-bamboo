# Port: 5021
# Routes: /createReview (POST)
# Dataclass: reviews
# -----------------------------------------------------------------------------------------

import os
import json
import data
import s3Images
from bson import json_util
from flask import Blueprint, g, request, jsonify
from bson.objectid import ObjectId
from datetime import datetime

from scripts.adminFunctions import hash_password

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

def parse_json(data):
    return json.loads(json_util.dumps(data))


# -----------------------------------------------------------------------------------------
def create_username(location_name):
    # Remove any spaces and convert to lowercase
    # Get a dict of all usernames 
    db = g.db
    username_dict={}
    for doc in db.venues.find({}):
        username_dict[doc["username"]]=doc["_id"]

    
    location_name = location_name.replace(" ", "").lower()
    
    # Check if the location name is empty
    if username_dict.get(location_name) is None :
        username = location_name
    
    else:
        # If the location name already exists, add a number to the end of the location name
        # Find the maximum number
        count = 0
        for key in username_dict.keys():
            if key.startswith(location_name):
                count += 1
                
        
        # Increment the number by 1
        id= count + 1
        username = location_name +"_"+ str(id)
    
    return username


# -----------------------------------------------------------------------------------------
# [POST] Creates a review
# - Insert entry into the "reviews" collection. Follows reviews dataclass requirements.
# - Duplicate review check: If a review with the same userID and reviewTarget exists, reject the request
# - Possible return codes: 201 (Created), 400 (Duplicate Detected), 500 (Error during creation)
@blueprint.route("/createReview", methods= ['POST'])
def createReviews():
    db = g.db
    rawReview = request.get_json()
    rawReview['reviewTarget'] = ObjectId(rawReview['reviewTarget'])  # Convert reviewTarget to ObjectId
    rawReview['userID'] = ObjectId(rawReview['userID'])  # Convert userID to ObjectId
    rawReview['createdDate'] = datetime.strptime(rawReview['createdDate'], "%Y-%m-%dT%H:%M:%S.%fZ")# convert date to datetime object

    # get review address
    locationAddress=rawReview['address']
    locationName=rawReview['location']

    
    # create a dictionary of addresses from venue documents and store thier ids
    
    condition_1= db.venues.count_documents({ "address": locationAddress })
    condition_2= db.venues.count_documents({ "venueName": locationName })
    

    # see if address is in the dictionary, if not insert a new venue
    if locationAddress != "" :
        
        if condition_2==0 or condition_1==0 :

            # Create a username for the venue
            username = create_username(locationName)
            
            venue_to_insert = {
                "venueName": rawReview["location"],
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
            
            
    if len(rawReview['taggedUsers']) >0:
        temp_tag_id =[]
        for id in rawReview['taggedUsers']:
            temp_tag_id.append(ObjectId(id))
        rawReview['taggedUsers'] = temp_tag_id
    if len(rawReview['flavorTag']) >0:
        temp_flavour_tag =[]
        for id in rawReview['flavorTag']:
            temp_flavour_tag.append(ObjectId(id['$oid']))
        rawReview['flavorTag'] = temp_flavour_tag

    # Duplicate listing check: Reject if review with the same userID and reviewTarget exists in the database
    rawReviewBottle = rawReview["reviewTarget"]
    rawReviewUserID = rawReview["userID"]
    existingReview = db.reviews.find_one({"reviewTarget": rawReviewBottle, "userID": rawReviewUserID})
    if(existingReview != None):
        return jsonify(
            {   
                "code": 400,
                "data": {
                    "listingName": rawReview['reviewDesc']
                },
                "message": "Review already exists."
            }
        ), 400
    
    # Upload image into S3
    if rawReview['photo']:
        rawReview['photo'] = s3Images.uploadBase64ImageToS3(rawReview['photo'])

    # Insert new review into database
    newReview = data.reviews(**rawReview)
    try:
        insertResult = db.reviews.insert_one(data.asdict(newReview))

        return jsonify( 
            {   
                "code": 201,
                "data": rawReview['reviewDesc']
            }
        ), 201
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": {
                    "listingName": rawReview['reviewDesc']
                },
                "message": "An error occurred creating the listing."
            }
        ), 500
