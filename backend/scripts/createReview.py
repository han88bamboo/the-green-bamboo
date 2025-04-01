# Port: 5021
# Routes: /createReview (POST), /createProducerReview (POST)
# Dataclass: reviews, producerReviews
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
# def create_username(location_name):
#     # Remove any spaces and convert to lowercase
#     # Get a dict of all usernames 
#     db = g.db
#     username_dict={}
#     for doc in db.venues.find({}):
#         username_dict[doc["username"]]=doc["_id"]

    
#     location_name = location_name.replace(" ", "").lower()
    
#     # Check if the location name is empty
#     if username_dict.get(location_name) is None :
#         username = location_name
    
#     else:
#         # If the location name already exists, add a number to the end of the location name
#         # Find the maximum number
#         count = 0
#         for key in username_dict.keys():
#             if key.startswith(location_name):
#                 count += 1
                
        
#         # Increment the number by 1
#         id= count + 1
#         username = location_name +"_"+ str(id)
    
#     return username
# ======================================================

# [NEW] TO BE ADDED FOR POSTGRES:
# ------------------------------------------------------
def create_username(location_name):
    conn = g.db
    cur = conn.cursor()

    location_name = location_name.replace(" ", "").lower()

    cur.execute("""
        SELECT id FROM "venues" WHERE "username" LIKE %s
    """, (f"{location_name}%",))

    existing_usernames = cur.fetchall()

    if not existing_usernames:
        return location_name
    else:
        max_suffix = max([int(name[0].split('_')[-1]) for name in existing_usernames if '_' in name[0]], default=0)
        return f"{location_name}_{max_suffix + 1}"
        
# ======================================================



# -----------------------------------------------------------------------------------------
# [POST] Creates a review
# - Insert entry into the "reviews" collection. Follows reviews dataclass requirements.
# - Duplicate review check: If a review with the same userID and reviewTarget exists, reject the request
# - Possible return codes: 201 (Created), 400 (Duplicate Detected), 500 (Error during creation)

# [OLD] TO BE DELETED FOR POSTGRES:
# ------------------------------------------------------
# @blueprint.route("/createReview", methods= ['POST'])
# def createReviews():
#     db = g.db
#     rawReview = request.get_json()
#     rawReview['reviewTarget'] = ObjectId(rawReview['reviewTarget'])  # Convert reviewTarget to ObjectId
#     rawReview['userID'] = ObjectId(rawReview['userID'])  # Convert userID to ObjectId
#     rawReview['createdDate'] = datetime.strptime(rawReview['createdDate'], "%Y-%m-%dT%H:%M:%S.%fZ")# convert date to datetime object

#     # get review address
#     locationAddress=rawReview['address']
#     locationName=rawReview['location']

    
#     # create a dictionary of addresses from venue documents and store thier ids
    
#     condition_1= db.venues.count_documents({ "address": locationAddress })
#     condition_2= db.venues.count_documents({ "venueName": locationName })
    

#     # see if address is in the dictionary, if not insert a new venue
#     if locationAddress != "" :
        
#         if condition_2==0 or condition_1==0 :

#             # Create a username for the venue
#             username = create_username(locationName)
            
#             venue_to_insert = {
#                 "venueName": rawReview["location"],
#                 "address": locationAddress,
#                 "venueType": "",
#                 "originLocation": "",
#                 "venueDesc": "",
#                 "menu": [],
#                 "hashedPassword": hash_password(username,"admin1234"),
#                 "claimStatus": False,
#                 "openingHours": {
#                 "Monday": [
#                     "",
#                     ""
#                 ],
#                 "Tuesday": [
#                     "",
#                     ""
#                 ],
#                 "Wednesday": [
#                     "",
#                     ""
#                 ],
#                 "Thursday": [
#                     "",
#                     ""
#                 ],
#                 "Friday": [
#                     "",
#                     ""
#                 ],
#                 "Saturday": [
#                     "",
#                     ""
#                 ],
#                 "Sunday": [
#                     "",
#                     ""
#                 ]
#                 },
#                 "photo": "",
#                 "updates": [],
#                 "questionsAnswers": [],
#                 "reservationDetails": "",
#                 "publicHolidays": "",
#                 "username": username
#             }

#             db.venues.insert_one(venue_to_insert)
 
# ======================================================
# [NEW] TO BE ADDED FOR POSTGRES:
# ------------------------------------------------------
@blueprint.route("/createReview", methods= ['POST'])
def createReviews():
    raw_review = request.get_json()
    conn = g.db
    cur = conn.cursor()

    review_target = int(raw_review['reviewTarget'])
    user_id = int(raw_review['userID'])
    created_date = datetime.strptime(raw_review['createdDate'], "%Y-%m-%dT%H:%M:%S.%fZ")

    # Checking for duplicate review
    cur.execute("""
        SELECT * FROM "reviews" WHERE "reviewTarget" = %s AND "userID" = %s
    """, (review_target, user_id))

    if cur.fetchone() is not None:
        return jsonify({
            "code": 400,
            "data": {
                "listingName": raw_review['reviewDesc']
            },
            "message": "Review already exists."
        }), 400

    tagged_users = raw_review.get('taggedUsers', [])
    flavour_tags = raw_review.get('flavourTag', [])
    observation_tags = raw_review.get('observationTag', [])

    will_recommend = raw_review.get('willRecommend')
    would_buy_again = raw_review.get('wouldBuyAgain')

    if will_recommend is None:
        will_recommend = None
    else:
        will_recommend = bool(will_recommend == 'true')

    if would_buy_again is None:
        would_buy_again = None
    else:
        would_buy_again = bool(would_buy_again == 'true')

    # Insert new venue if necessary
    venue_id = None
    if raw_review.get('location') and raw_review.get('address'):
        location_name = raw_review['location']
        address = raw_review['address']
        cur.execute("""SELECT id FROM venues WHERE "venueName" = %s AND "address" = %s""", (location_name, address))
        venue_id = cur.fetchone()['id'] if cur.rowcount > 0 else None
        if not venue_id:
            username = create_username(location_name)
            insert_venue_sql = """INSERT INTO venues ("venueName", "address", "venueType", "originLocation", "venueDesc",
                                  "hashedPassword", "claimStatus", photo, "reservationDetails", username)
                                  VALUES (%s, %s, '', '', '', %s, FALSE, '', '', %s) RETURNING id"""
            hashed_password = 'hashed_password'
            cur.execute(insert_venue_sql, (location_name, address, hashed_password, username))
            venue_id = cur.fetchone()['id'] if cur.rowcount > 0 else None
            print(venue_id)
            conn.commit()

    # Upload image into S3
    if raw_review['photo']:
        raw_review['photo'] = s3Images.uploadBase64ImageToS3(raw_review['photo'])


    # Prepare the insert SQL for reviews
    insert_review_sql = """INSERT INTO reviews ("userID", "reviewTarget", "rating", "reviewDesc", "reviewType", "createdDate", 
                          language, finish, "willRecommend", "wouldBuyAgain", "taggedUsers", "flavourTag", photo, colour, 
                          aroma, taste, "observationTag", location, address)
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    review_values = (user_id, review_target, float(raw_review['rating']), raw_review['reviewDesc'], raw_review['reviewType'],
                     created_date, raw_review['language'], raw_review['finish'], will_recommend,
                     would_buy_again, tagged_users, flavour_tags, raw_review['photo'],
                     raw_review['colour'], raw_review['aroma'], raw_review['taste'],
                     observation_tags, venue_id, raw_review['address'])

    try:
        cur.execute(insert_review_sql, review_values)
        conn.commit()

        # Calculate proof points earned 
        rule_fulfiled_id = []

        # Basic review: Simple text 
        if (raw_review['reviewDesc'] != None):
            rule_fulfiled_id.append(2)
        
        # Extended review: color, aroma, taste, finish
        if (raw_review['finish'] != None or raw_review['colour'] != None or raw_review['aroma'] != None or raw_review['taste'] != None):
            rule_fulfiled_id.append(3)

        # Attach image
        if (raw_review['photo'] != None):
            rule_fulfiled_id.append(4)

        # Tag location
        if (venue_id != None):
            rule_fulfiled_id.append(5)

        # Tag friends
        if (tagged_users != []):
            rule_fulfiled_id.append(6)

        # Get total proof points earned 
        cur.execute('SELECT SUM("proofPoints") FROM "pointSystemRules" WHERE id IN %s', (tuple(rule_fulfiled_id),))
        total_points = cur.fetchone()['sum']

        # Update user points
        if total_points:
            cur.execute('UPDATE "pointsRecorder" SET "currentPoints" = "currentPoints" + %s WHERE id = %s AND "userType" = %s', (total_points, user_id, 'user',))
            conn.commit()

        return jsonify({
            "code": 201,
            "data": raw_review['reviewDesc'],
            "proofPointsEarned": total_points
        }), 201
    except Exception as e:
        print(str(e))
        return jsonify({
            "code": 500,
            "data": {
                "listingName": raw_review['reviewDesc']
            },
            "message": "An error occurred creating the listing."
        }), 500
# ======================================================

# [POST] Creates a producer tour review
@blueprint.route("/createProducerReview", methods=['POST'])
def createProducerReviews():
    raw_review = request.get_json()
    conn = g.db
    cur = conn.cursor()

    producer_id = int(raw_review['producerID'])
    user_id = int(raw_review['userID'])
    created_date = datetime.strptime(raw_review['createdDate'], "%Y-%m-%dT%H:%M:%S.%fZ")

    # Check for duplicate review using EXISTS
    cur.execute("""SELECT EXISTS(SELECT 1 FROM "producerReviews" WHERE "producerID" = %s AND "userID" = %s)""",
                (producer_id, user_id))
    if cur.fetchone()['exists']:
        return jsonify({"code": 400, "message": "Review already exists."}), 400

    # Upload images & store their returned URLs
    photos = [s3Images.uploadBase64ImageToS3(photo) for photo in raw_review.get('photos', []) if photo]

    insert_review_sql = """
        INSERT INTO "producerReviews" ("userID", "producerID", "rating", "reviewDesc", "createdDate", "photos") 
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    review_values = (user_id, producer_id, float(raw_review['rating']), raw_review['reviewDesc'], created_date, photos)

    try:
        cur.execute(insert_review_sql, review_values)
        conn.commit()

        total_points = 0
        # Get the proof points for simple text review
        if raw_review['reviewDesc']:
            cur.execute("""SELECT "proofPoints" FROM "pointSystemRules" WHERE id = 2""")
            total_points += cur.fetchone()['proofPoints']

        # Check if photo was provided
        if photos:
            cur.execute("""SELECT "proofPoints" FROM "pointSystemRules" WHERE id = 4""")
            total_points += cur.fetchone()['proofPoints']

        # Update user points
        cur.execute('UPDATE "pointsRecorder" SET "currentPoints" = "currentPoints" + %s WHERE id = %s AND "userType" = %s', (total_points, user_id, 'user',))
        conn.commit()

        return jsonify({"code": 201, "data": raw_review['reviewDesc']}), 201

    except Exception as e:
        print(str(e))
        return jsonify({"code": 500, "message": "An error occurred creating the review."}), 500