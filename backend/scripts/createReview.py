# Port: 5021
# Routes: /createReview (POST)
# Dataclass: reviews
# -----------------------------------------------------------------------------------------


# [OLD] TO BE DELETED FOR POSTGRES:
# ------------------------------------------------------


# ======================================================

# [NEW] TO BE ADDED FOR POSTGRES:
# ------------------------------------------------------


# ======================================================


import os
import json
import data
import s3Images
from flask import Blueprint, g, request, jsonify
from datetime import datetime
from scripts.adminFunctions import hash_password
# [OLD] TO BE DELETED FOR POSTGRES:
# ------------------------------------------------------
from bson import json_util
from bson.objectid import ObjectId
# ======================================================

# [NEW] TO BE ADDED FOR POSTGRES:
# ------------------------------------------------------
# import psycopg2
# from psycopg2.extras import RealDictCursor
# ======================================================

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

# [OLD] TO BE DELETED FOR POSTGRES:
# ------------------------------------------------------
def parse_json(data):
    return json.loads(json_util.dumps(data))
# ======================================================


# -----------------------------------------------------------------------------------------
# [OLD] TO BE DELETED FOR POSTGRES:
# -----------------------------------------------------
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
# ======================================================

# [NEW] TO BE ADDED FOR POSTGRES:
# ------------------------------------------------------
# def create_username(location_name):
#     conn = g.db  # Get the DB connection from g
#     cur = conn.cursor()

#     # Query to get all existing usernames from the venues table
#     cur.execute("SELECT username FROM venues")
#     rows = cur.fetchall()
    
#     # Convert the query result to a set of existing usernames
#     username_set = {row['username'] for row in rows}

#     location_name = location_name.replace(" ", "").lower()

#     # Check if the location name is already in use
#     if location_name not in username_set:
#         username = location_name
#     else:
#         # Generate a unique username by appending a number
#         count = sum(1 for name in username_set if name.startswith(location_name))
#         username = f"{location_name}_{count + 1}"

#     return username
# ======================================================



# -----------------------------------------------------------------------------------------
# [POST] Creates a review
# - Insert entry into the "reviews" collection. Follows reviews dataclass requirements.
# - Duplicate review check: If a review with the same userID and reviewTarget exists, reject the request
# - Possible return codes: 201 (Created), 400 (Duplicate Detected), 500 (Error during creation)

# [OLD] TO BE DELETED FOR POSTGRES:
# ------------------------------------------------------
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
 
# ======================================================
# [NEW] TO BE ADDED FOR POSTGRES:
# ------------------------------------------------------
# @blueprint.route("/createReview", methods= ['POST'])
# def createReviews():
#     rawReview = request.get_json()

    
#     rawReview['createdDate'] = datetime.strptime(rawReview['createdDate'], "%Y-%m-%dT%H:%M:%S.%fZ")# convert date to datetime object

#     # get review address
#     locationAddress=rawReview['address']
#     locationName=rawReview['location']

#     # Check if the venue already exists in the database
#     cur.execute("""
#         SELECT COUNT(*) FROM venues 
#         WHERE address = %s OR venueName = %s
#     """, (locationAddress, locationName))
#     condition_1, condition_2 = cur.fetchone()

#     # see if address is in the dictionary, if not insert a new venue
#     if locationAddress != "" :
        
#         if condition_2==0 or condition_1==0 :

#             # Create a username for the venue
#             username = create_username(locationName)
            
#             cur.execute("""
#                 INSERT INTO venues 
#                 (venueName, address, venueType, originLocation, venueDesc, menu, hashedPassword, claimStatus, openingHours, photo, updates, questionsAnswers, reservationDetails, publicHolidays, username)
#                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#             """, (
#                 rawReview["location"],
#                 locationAddress,
#                 "",
#                 "",
#                 "",
#                 [],  # Assuming you store JSON or ARRAY type in Postgres
#                 hash_password(username, "admin1234"),
#                 False,
#                 '{"Monday": ["", ""], "Tuesday": ["", ""], "Wednesday": ["", ""], "Thursday": ["", ""], "Friday": ["", ""], "Saturday": ["", ""], "Sunday": ["", ""]}',  # JSON string for openingHours
#                 "",
#                 [],
#                 [],
#                 "",
#                 "",
#                 username
#             ))
#             conn.commit()  # Commit the transaction to persist changes
 
# ======================================================           



# [OLD] TO BE DELETED FOR POSTGRES:
# ------------------------------------------------------    
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
# ======================================================

# [NEW] TO BE ADDED FOR POSTGRES:
    # ------------------------------------------------------
    # if len(rawReview['taggedUsers']) > 0:
    #     # Assuming IDs are already in a suitable format for PostgreSQL (e.g., UUIDs or strings)
    #     tagged_users = [str(id) for id in rawReview['taggedUsers']]
    #     rawReview['taggedUsers'] = tagged_users

    # if len(rawReview['flavorTag']) > 0:
    #     # Assuming IDs are already in a suitable format for PostgreSQL (e.g., UUIDs or strings)
    #     flavor_tags = [str(id['$oid']) for id in rawReview['flavorTag']]  # Only if '$oid' format is used
    #     rawReview['flavorTag'] = flavor_tags
# ======================================================


# [OLD] TO BE DELETED FOR POSTGRES:
# ------------------------------------------------------    
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
# ======================================================

# [NEW] TO BE ADDED FOR POSTGRES:
# ------------------------------------------------------    
    # # Duplicate listing check: Reject if review with the same userID and reviewTarget exists in the database
    # rawReviewBottle = rawReview["reviewTarget"]
    # rawReviewUserID = rawReview["userID"]

    # # Prepare SQL query to check for an existing review
    # query = """
    #     SELECT 1 FROM reviews 
    #     WHERE reviewTarget = %s AND userID = %s
    #     LIMIT 1
    # """

    # cur.execute(query, (rawReviewBottle, rawReviewUserID))
    # existingReview = cur.fetchone()

    # if existingReview is not None:
    #     return jsonify(
    #         {   
    #             "code": 400,
    #             "data": {
    #                 "listingName": rawReview['reviewDesc']
    #             },
    #             "message": "Review already exists."
    #         }
    #     ), 400
# ======================================================

    # Upload image into S3
    if rawReview['photo']:
        rawReview['photo'] = s3Images.uploadBase64ImageToS3(rawReview['photo'])

# [OLD] TO BE DELETED FOR POSTGRES:
# ------------------------------------------------------
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
# ======================================================

# [NEW] TO BE ADDED FOR POSTGRES:
# ------------------------------------------------------
    # # Insert new review into database
    # newReview = data.reviews(**rawReview)
    
    # try:
    #     insertResult = db.reviews.insert_one(data.asdict(newReview))
    #     insert_query = """
    #         INSERT INTO reviews (userID, reviewTarget, reviewDesc, photo, createdDate, flavorTag, taggedUsers)
    #         VALUES (%s, %s, %s, %s, %s, %s, %s)
    #         RETURNING id
    #     """
    #     cur.execute(insert_query, (
    #         newReview.userID,
    #         newReview.reviewTarget,
    #         newReview.reviewDesc,
    #         newReview.photo,
    #         newReview.createdDate,
    #         newReview.flavorTag,  # Assuming flavorTag is properly formatted
    #         newReview.taggedUsers  # Assuming taggedUsers is properly formatted
    #     ))

    #     conn.commit()        

    #     return jsonify( 
    #         {   
    #             "code": 201,
    #             "data": rawReview['reviewDesc']
    #         }
    #     ), 201
    # except Exception as e:
    #     print(str(e))
    #     g.db.rollback() 
    #     return jsonify(
    #         {
    #             "code": 500,
    #             "data": {
    #                 "listingName": rawReview['reviewDesc']
    #             },
    #             "message": "An error occurred creating the listing."
    #         }
    #     ), 500
# ======================================================