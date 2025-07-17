# Port: 5001
# Routes: /createListing (POST)
# Dataclass: listings
# -----------------------------------------------------------------------------------------

import os
import json
import pytz
import re
import s3Images
from flask import Blueprint, g, request, jsonify
from datetime import datetime, timedelta
from scripts import notifications
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
# [POST] Creates a listing
# - Insert entry into the "listings" collection. Follows listings dataclass requirements.
# - Duplicate listing check: If a listing with the same name exists, reject the request
# - Possible return codes: 201 (Created), 400 (Duplicate Detected), 500 (Error during creation)
# @blueprint.route("/createListing", methods= ['POST'])
# def createListings():
    # db = g.db
    # rawBottle = request.get_json()
    # Add current datetime to the listing
    # rawBottle['addedDate'] = datetime.now(pytz.timezone('Etc/GMT-8'))
    # rawBottle["allowMod"] = True
# [OLD] TO BE DELETED FOR POSTGRES:
# ------------------------------------------------------    
    # rawBottle['producerID'] = ObjectId(rawBottle['producerID'])
# ======================================================
    # Duplicate listing check: Reject if listing with the same bottle name already exists in the database
    # rawBottleName = rawBottle["listingName"]

# [OLD] TO BE DELETED FOR POSTGRES:
# ------------------------------------------------------    
    # existingBottle = db.listings.find_one({"listingName": rawBottleName})
    # if(existingBottle != None):
    #     return jsonify(
    #         {   
    #             "code": 400,
    #             "data": {
    #                 "listingName": rawBottleName
    #             },
    #             "message": "Bottle already exists."
    #         }
    #     ), 400
# ======================================================    
# [NEW] TO BE ADDED FOR POSTGRES:
# ------------------------------------------------------
    # # Execute the SQL query to check for duplicates
    # cursor = db.cursor()
    # cursor.execute("SELECT * FROM listings WHERE listingName = %s", (rawBottleName,))
    # existingBottle = cursor.fetchone()
    
    # if existingBottle is not None:
    #     return jsonify(
    #         {   
    #             "code": 400,
    #             "data": {
    #                 "listingName": rawBottleName
    #             },
    #             "message": "Bottle already exists."
    #         }
    #     ), 400
# ======================================================

    # Upload image into s3 bucket and retrieve url
    # rawBottle['photo'] = s3Images.uploadBase64ImageToS3(rawBottle['photo'])
# [OLD] TO BE DELETED FOR POSTGRES:
# ------------------------------------------------------      
    # Insert new listing into database
    # newBottle = data.listings(**rawBottle)
# ======================================================
# [NEW] TO BE ADDED FOR POSTGRES:
# ------------------------------------------------------
    # # Insert new listing into database
    # columns = ', '.join(rawBottle.keys())
    # placeholders = ', '.join(['%s'] * len(rawBottle))
    # sql = f"INSERT INTO listings ({columns}) VALUES ({placeholders})"
    # cursor.execute(sql, list(rawBottle.values()))
    # db.commit()
# ======================================================
    # try:
# [OLD] TO BE DELETED FOR POSTGRES:
# ------------------------------------------------------             
        # insertResult = db.listings.insert_one(data.asdict(newBottle))
# ======================================================
# [NEW] TO BE ADDED FOR POSTGRES:
# ------------------------------------------------------
        # columns = ', '.join(rawBottle.keys())
        # placeholders = ', '.join(['%s'] * len(rawBottle))
        # sql = f"INSERT INTO listings ({columns}) VALUES ({placeholders})"
        # cursor.execute(sql, list(rawBottle.values()))
        # db.commit()  # Commit the transaction
# ======================================================        
    #     return jsonify( 
    #         {   
    #             "code": 201,
    #             "data": rawBottleName
    #         }
    #     ), 201
    # except Exception as e:
    #     print(str(e))
    #     return jsonify(
    #         {
    #             "code": 500,
    #             "data": {
    #                 "listingName": rawBottleName
    #             },
    #             "message": "An error occurred creating the listing."
    #         }
    #     ), 500
# ======================================================

# -----------------------------------------------------------------------------------------
# [POST] Creates a listing
# - Insert entry into the "listings" collection. Follows listings dataclass requirements.
# - Duplicate listing check: If a listing with the same name exists, reject the request
# - Possible return codes: 201 (Created), 400 (Duplicate Detected), 500 (Error during creation)
@blueprint.route("/createListing", methods=['POST'])
def createListings():
    conn = g.db
    cur = conn.cursor()

    rawBottle = request.get_json()
    rawBottle['addedDate'] = datetime.now(pytz.timezone('Etc/GMT-8'))
    rawBottle["allowMod"] = True
    rawBottle['producerID'] = int(rawBottle['producerID'])
    rawBottle['bottlerID'] = int(rawBottle['bottlerID']) if rawBottle['bottlerID'] != "" else None
    rawBottleName = rawBottle["listingName"]
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print("data received:", rawBottle)

    try:
        # Check for duplicate listing
        cur.execute('SELECT * FROM listings WHERE "listingName" = %s', (rawBottleName,))
        existingBottle = cur.fetchone()

        if existingBottle is not None:
            return jsonify(
                {   
                    "code": 400,
                    "data": {
                        "listingName": rawBottleName
                    },
                    "message": "Bottle already exists."
                }
            ), 400
        
        # Convert abv from string to float if necessary
        if 'abv' in rawBottle:
            abv_value = rawBottle['abv'].replace('%', '')  # Remove the '%' sign
            rawBottle['abv'] = float(abv_value)

        # uploading as base64 image
        if rawBottle['photo'] is not None and rawBottle['photo'] != "":
            base64_string = re.sub(r'^data:image\/[a-zA-Z]+;base64,', '', rawBottle['photo'])
            rawBottle['photo'] = s3Images.uploadBase64ImageToS3(base64_string)
        else:
            rawBottle['photo'] = "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739"

        columns = ', '.join(f'"{col}"' for col in rawBottle.keys())
        placeholders = ', '.join(['%s'] * len(rawBottle))
        sql = f"INSERT INTO listings ({columns}) VALUES ({placeholders}) RETURNING id"
        
        cur.execute(sql, list(rawBottle.values()))
        new_id = cur.fetchone()['id']

        # NEW: Send approval notification to the original submitter
        # First, find the original request from requestListings table
        cur.execute(
            'SELECT "userID" FROM "requestListings" WHERE "listingName" = %s',
            (rawBottleName,)
        )
        original_request = cur.fetchone()
        
        if original_request and original_request['userID']:
            submitter_id = original_request['userID']
            
            # Build URL slug for the approved listing
            slug = re.sub(r'[^a-z0-9]+', '', rawBottleName.lower())
            
            # Create approval notification
            approval_notification = {
                "userId": submitter_id,
                "userType": "user",  # Could be "user", "producer", or "venue" - you may want to store this in requestListings
                "notiTabs": "forYou",
                "notiType": "approvedListing",
                "image": rawBottle.get('photo'),
                "link": f"/listing/view/{new_id}/{slug}",
                "message": f"Your listing request '{rawBottleName}' has been approved and is now live!",
                "createdAt": current_time,
            }
            
            print("Sending approval notification:", approval_notification)
            notifications.add_notification_to_db(approval_notification)

        # Existing notification logic for followers
        cutoff = datetime.now(pytz.timezone('Etc/GMT-8')) - timedelta(hours=24)
        
        cur.execute(
            'SELECT COUNT(*) FROM "listings" '
            'WHERE "producerID" = %s AND "addedDate" >= %s',
            (rawBottle['producerID'], cutoff)
        )
        recent_count = cur.fetchone()['count']
        print(f"Recent count: {recent_count}")

        cur.execute(
            'SELECT "producerName" FROM "producers" WHERE id = %s',
            (rawBottle['producerID'],)
        )
        producerName = cur.fetchone()['producerName']

        if recent_count <= 2:
            # build a URL-safe slug: lowercase, alphanumeric only
            slug = re.sub(r'[^a-z0-9]+', '', rawBottleName.lower())

            # fetch all users who follow this producer
            cur.execute(
                'SELECT "userId" FROM "usersFollowLists" '
                'WHERE %s::text = ANY("producers")',
                (str(rawBottle['producerID']),)
            )
            print("hello6")
            followers = [row['userId'] for row in cur.fetchall()]
            

            # insert notifications
            for uid in followers:
                notification_data = {
                    "userId":   uid,
                    "userType": "user",
                    "notiTabs": "venues & producers",
                    "notiType": "newDrink",
                    "image":    rawBottle.get('photo'),
                    "link":     f"/listing/view/{new_id}/{slug}",
                    "message":  f"{producerName} added a new drink: {rawBottleName}",
                    "createdAt": current_time,
                }
                print("Sending notification:", notification_data)
                notifications.add_notification_to_db(notification_data)
        
        
        conn.commit()

        return jsonify(
            {   
                "code": 201,
                "data": {
                    "listingName": rawBottleName,
                    "id": new_id
                }
            }
        ), 201
    
    except Exception as e:
        print(str(e))
        conn.rollback()
        return jsonify(
            {
                "code": 500,
                "data": {
                    "listingName": rawBottleName
                },
                "message": "An error occurred creating the listing."
            }
        ), 500
    
    finally:
        cur.close()

# ======================================================
# Optimize + simple rework (code not tested.)
# two foreseeable issues that may or may not cause issues in the future
# 1. EDGE CASE - uploading data here might hurt the performance, wait needs to be done for images(if user uploads raw images)
# suggestion - move the upload with s3 presigned URL, action can be done through f/e when user upload the image hence api just needs to receove the URL
# 2. db connection, for scalability ThreadedConnectionPool should be utilized
# ------------------------------------------------------
# ======================================================
# Exception class
# ------------------------------------------------------
# class CreteListingError(Exception):
#     pass 

# ======================================================
# logic layer
# # ------------------------------------------------------
# def create_db_listing(listing_data):
#     db = g.db
#     try: 
#         # with is to ensure the proper connection closure when 
#         # query is done 
#         with db.cursor() as cursor:
#             # fetch only necessary columns limits to only 1
#             select_query = "SELECT listingName FROM listings WHERE listingName = %s LIMIT 1"
#             cursor.execute(select_query, (listing_data["listingName"],))
#             # listing exist in db
#             if cursor.fetchone():
#                 raise ValueError(f"Bottle already exists.")

#             # upload to s3 and 
#             listing_data['photo'] = s3Images.uploadBase64ImageToS3(listing_data['photo'])

#             # insert new listing data into postgresql
#             columns = ', '.join(rawBottle.keys())
#             placeholders = ', '.join(['%s'] * len(rawBottle))
#             insert_sql = f"INSERT INTO listings ({columns}) VALUES ({placeholders}) RETURNING id"
#             cursor.execute(insert_sql, list(listing_data.values()))
#             new_id = cursor.fetchone()['id']
#             db.commit()

#             return { "id": new_id, "listingName": listing_data["listingName"]}
#     except Exception as e: 
#         db.rollback()
#         raise CreteListingError(f"Error creating listing: {str(e)}") from e
    
# ======================================================
# base Route
# ------------------------------------------------------
# @blueprint.route("/createListing", methods= ['POST'])
# def createListings():
#     try:
#         listing_data = request.get_json()
#         # Add current datetime to the listing
#         listing_data['addedDate'] = datetime.now(pytz.timezone('Etc/GMT-8'))
#         listing_data["allowMod"] = True

#         result = create_db_listing(listing_data)

#         return jsonify({
#             "code": 201,
#             "data": result["listingName"]
#         }), 201

#     except ValueError as ve:
#         return jsonify({
#             "code": 400,
#             "message": str(ve)
#         }), 400
#     except CreteListingError as cle: 
#         return jsonify({
#             "code": 500,
#             "message": "An error occured while creating the listing."
#         }), 500
#     except Exception as e: 
#         return jsonify({
#             "code": 500,
#             "message": f"An error occurred: {str(e)}"
#         }), 500