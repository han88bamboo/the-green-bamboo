# Port: 5001
# Routes: /createListing (POST), /createListingBulk (POST), /stageListingsFromCSV (POST),
#         /getStagedListings (GET), /updateStagedListing/<id> (PUT), /deleteStagedListing/<id> (DELETE),
#         /commitStagedListings (POST)
# Dataclass: listings
# -----------------------------------------------------------------------------------------

import os
import json
import pytz
import re
import csv
import io
import chardet
import s3Images
from flask import Blueprint, g, request, jsonify
from datetime import datetime, timedelta
from scripts import notifications
from scripts.getData import detect_duplicates_batch, fuzzy_match_producer_batch
from concurrent.futures import ThreadPoolExecutor, as_completed
from psycopg2.extras import execute_values
# Import the database manager for connection pooling
from app import db_manager
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
# Helper: Update specific fields of an existing listing (used by CSV import and bulk submit
# when a user confirms a duplicate and opts to update individual fields).
# -----------------------------------------------------------------------------------------
LISTING_UPDATABLE_FIELDS = {
    'officialDesc', 'sourceLink', 'reviewLink', 'photo',
    'drinkType', 'typeCategory', 'drinkStyle', 'originCountry',
    'age', 'abv', 'tags', 'varietyTags'
}

def update_existing_listing(cursor, listing_id, field_values, fields_to_update):
    """
    Update specific fields of an existing listing.
    Only updates fields explicitly listed in fields_to_update and present in LISTING_UPDATABLE_FIELDS.

    Args:
        cursor: DB cursor
        listing_id: ID of the existing listing to update
        field_values: dict with field values (from staged row or form payload)
        fields_to_update: list of field names the user opted to update
    Returns:
        True if any fields were updated, False otherwise
    """
    updates = {}
    for field in fields_to_update:
        if field not in LISTING_UPDATABLE_FIELDS:
            continue
        value = field_values.get(field)
        if value is not None and str(value).strip() != '':
            updates[field] = value

    if not updates:
        return False

    set_clause = ', '.join(f'"{k}" = %s' for k in updates.keys())
    cursor.execute(
        f'UPDATE "listings" SET {set_clause} WHERE "id" = %s',
        list(updates.values()) + [listing_id]
    )
    return True

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
    rawBottle = request.get_json()
    rawBottle['addedDate'] = datetime.now(pytz.timezone('Etc/GMT-8'))
    rawBottle["allowMod"] = True
    rawBottle['producerID'] = int(rawBottle['producerID'])
    rawBottle['bottlerID'] = int(rawBottle['bottlerID']) if rawBottle['bottlerID'] != "" else None
    rawBottleName = rawBottle["listingName"]
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print("data received:", rawBottle)

    try:
        with db_manager.get_cursor() as cursor:
            # Check for duplicate listing (commented out by charsiucharlie 15 Nov 2025)
            # cursor.execute('SELECT * FROM listings WHERE "listingName" = %s', (rawBottleName,))
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
            
            # Convert abv from string to float if necessary
            if 'abv' in rawBottle:
                abv_value = rawBottle['abv'].replace('%', '')  # Remove the '%' sign
                if abv_value.strip():  # Check if the string is not empty
                    rawBottle['abv'] = float(abv_value)
                else:
                    # Handle empty ABV - set to NULL in database
                    rawBottle['abv'] = None
            
            # Handle tags field - ensure it's a string or NULL
            if 'tags' in rawBottle:
                if rawBottle['tags'] is None or rawBottle['tags'].strip() == "":
                    rawBottle['tags'] = None
                else:
                    # Ensure tags is a string (it should already be trimmed from frontend)
                    rawBottle['tags'] = str(rawBottle['tags'])
            
            # Handle order field - ensure it's an integer or NULL
            if 'order' in rawBottle:
                if rawBottle['order'] is None or rawBottle['order'] == "":
                    rawBottle['order'] = None
                else:
                    try:
                        rawBottle['order'] = int(rawBottle['order'])
                    except (ValueError, TypeError):
                        rawBottle['order'] = None

            # Handle varietyTags field - ensure it's a PostgreSQL array or NULL
            if 'varietyTags' in rawBottle:
                if rawBottle['varietyTags'] is None or rawBottle['varietyTags'] == "" or rawBottle['varietyTags'] == []:
                    rawBottle['varietyTags'] = None
                elif isinstance(rawBottle['varietyTags'], list):
                    # It's already a list, keep it as is (will be converted to PostgreSQL array)
                    pass
                elif isinstance(rawBottle['varietyTags'], str):
                    # If it's a string, try to parse it as JSON array
                    try:
                        import json
                        rawBottle['varietyTags'] = json.loads(rawBottle['varietyTags'])
                    except:
                        # If parsing fails, set to NULL
                        rawBottle['varietyTags'] = None
                else:
                    rawBottle['varietyTags'] = None
            else:
                rawBottle['varietyTags'] = None

            # uploading as base64 image
            if rawBottle['photo'] is not None and rawBottle['photo'] != "":
                base64_string = re.sub(r'^data:image\/[a-zA-Z]+;base64,', '', rawBottle['photo'])
                rawBottle['photo'] = s3Images.uploadBase64ImageToS3(base64_string)
            else:
                rawBottle['photo'] = "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739"

            columns = ', '.join(f'"{col}"' for col in rawBottle.keys())
            placeholders = ', '.join(['%s'] * len(rawBottle))
            sql = f"INSERT INTO listings ({columns}) VALUES ({placeholders}) RETURNING id"
            
            cursor.execute(sql, list(rawBottle.values()))
            new_id = cursor.fetchone()['id']

            # NEW: Send approval notification to the original submitter
            # First, find the original request from requestListings table
            cursor.execute(
                'SELECT "userID", "venueID", "submitterType" FROM "requestListings" WHERE "listingName" = %s',
                (rawBottleName,)
            )
            original_request = cursor.fetchone()
            
            if original_request:
                submitter_type = original_request.get('submitterType', 'user')
                
                # Determine the actual submitter ID and type
                if submitter_type == 'venue' and original_request['venueID']:
                    submitter_id = original_request['venueID']
                    submitter_user_type = 'venue'
                elif submitter_type == 'user' and original_request['userID']:
                    submitter_id = original_request['userID']
                    submitter_user_type = 'user'
                else:
                    submitter_id = None
                    submitter_user_type = None
                
                if submitter_id:
                    # Build URL slug for the approved listing
                    slug = re.sub(r'[^a-z0-9]+', '', rawBottleName.lower())
                    
                    # Create approval notification with correct user type
                    approval_notification = {
                        "userId": submitter_id,
                        "userType": submitter_user_type,  # Now correctly set based on actual submitter
                        "notiTabs": "forYou",
                        "notiType": "approvedListing",
                        "image": rawBottle.get('photo'),
                        "link": f"/listing/view/{new_id}/{slug}",
                        "message": f"Your listing request '{rawBottleName}' has been approved and is now live!",
                        "createdAt": current_time,
                    }
                    
                    print("Sending approval notification:", approval_notification)
                    try:
                        notifications.add_notification_to_db(approval_notification, cursor)
                    except Exception as notif_error:
                        print(f"Failed to send approval notification: {notif_error}")

            # Existing notification logic for followers
            cutoff = datetime.now(pytz.timezone('Etc/GMT-8')) - timedelta(hours=24)
            
            cursor.execute(
                'SELECT COUNT(*) FROM "listings" '
                'WHERE "producerID" = %s AND "addedDate" >= %s',
                (rawBottle['producerID'], cutoff)
            )
            recent_count = cursor.fetchone()['count']
            print(f"Recent count: {recent_count}")

            cursor.execute(
                'SELECT "producerName" FROM "producers" WHERE id = %s',
                (rawBottle['producerID'],)
            )
            producerName = cursor.fetchone()['producerName']

            if recent_count <= 2:
                # build a URL-safe slug: lowercase, alphanumeric only
                slug = re.sub(r'[^a-z0-9]+', '', rawBottleName.lower())

                # fetch all users who follow this producer
                cursor.execute(
                    'SELECT "userId" FROM "usersFollowLists" '
                    'WHERE %s::text = ANY("producers")',
                    (str(rawBottle['producerID']),)
                )
                print("hello6")
                followers = [row['userId'] for row in cursor.fetchall()]
                

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
                    try:
                        notifications.add_notification_to_db(notification_data, cursor)
                    except Exception as notif_error:
                        print(f"Failed to send follower notification: {notif_error}")

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
        return jsonify(
            {
                "code": 500,
                "data": {
                    "listingName": rawBottleName
                },
                "message": "An error occurred creating the listing."
            }
        ), 500

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


# -----------------------------------------------------------------------------------------
# [POST] Creates multiple listings in bulk (for power users / admins)
# - Insert multiple entries into the "listings" collection
# - Each item is processed individually with its own transaction
# - Failed items are rolled back individually without affecting other items
# - Returns detailed results for each item (success/failure with details)
# - Possible return codes: 201 (At least one created), 400 (All failed validation), 500 (Server error)
# -----------------------------------------------------------------------------------------
@blueprint.route("/createListingBulk", methods=['POST'])
def createListingsBulk():
    """
    Bulk create listings endpoint for power users.
    
    Expected payload format:
    {
        "listings": [
            {
                "sourceLink": "string",
                "listingName": "string",
                "officialDesc": "string",
                "reviewLink": "string",
                "bottler": "string",
                "originCountry": "string",
                "abv": "string (e.g., '43%')",
                "age": "string",
                "producerID": int,
                "bottlerID": int or "",
                "photo": "base64 string or empty",
                "drinkType": "string",
                "typeCategory": "string",
                "drinkStyle": "string",
                "tags": "string (e.g., '#tag1, #tag2')",
                "order": int or null,
                "varietyTags": ["string"] or null
            },
            ...
        ]
    }
    
    Returns:
    {
        "code": 201,
        "data": {
            "totalSubmitted": int,
            "successCount": int,
            "failCount": int,
            "results": [
                {
                    "index": int,
                    "success": bool,
                    "listingId": int (if success),
                    "listingName": "string",
                    "producerID": int,
                    "drinkType": "string",
                    "typeCategory": "string",
                    "originCountry": "string",
                    "abv": "string",
                    "age": "string",
                    "error": "string" (if failed)
                },
                ...
            ]
        }
    }
    """
    try:
        payload = request.get_json()
        
        # Validate payload structure
        if not payload or 'listings' not in payload:
            return jsonify({
                "code": 400,
                "message": "Invalid payload. Expected { listings: [...] }"
            }), 400
        
        listings = payload['listings']
        
        if not isinstance(listings, list) or len(listings) == 0:
            return jsonify({
                "code": 400,
                "message": "Listings array is empty or invalid."
            }), 400
        
        if len(listings) > 20:
            return jsonify({
                "code": 400,
                "message": "Maximum 20 listings allowed per bulk submission."
            }), 400
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        results = []
        success_count = 0
        fail_count = 0
        
        # Process each listing individually
        for index, raw_item in enumerate(listings):
            # Check if this is an update to an existing listing (confirmed duplicate)
            update_listing_id = raw_item.get('updateExistingListingId')
            if update_listing_id:
                try:
                    fields_to_update = raw_item.get('fieldsToUpdate', [])
                    with db_manager.get_cursor() as cursor:
                        updated = update_existing_listing(cursor, int(update_listing_id), raw_item, fields_to_update)
                    item_result = {
                        'index': raw_item.get('originalIndex', index),
                        'success': True,
                        'updated': True,
                        'listingId': int(update_listing_id),
                        'listingName': raw_item.get('listingName', ''),
                        'fieldsUpdated': fields_to_update if updated else []
                    }
                except Exception as e:
                    item_result = {
                        'index': raw_item.get('originalIndex', index),
                        'success': False,
                        'error': f"Failed to update existing listing: {str(e)}"
                    }
                results.append(item_result)
                if item_result['success']:
                    success_count += 1
                else:
                    fail_count += 1
                continue

            item_result = process_single_bulk_item(index, raw_item, current_time)
            results.append(item_result)

            if item_result['success']:
                success_count += 1
            else:
                fail_count += 1
        
        # Determine overall response code
        if success_count == 0:
            response_code = 400
            message = "All listings failed to create."
        else:
            response_code = 201
            message = f"Bulk submission complete. {success_count} succeeded, {fail_count} failed."
        
        return jsonify({
            "code": response_code,
            "message": message,
            "data": {
                "totalSubmitted": len(listings),
                "successCount": success_count,
                "failCount": fail_count,
                "results": results
            }
        }), response_code
        
    except Exception as e:
        print(f"Bulk listing creation error: {str(e)}")
        return jsonify({
            "code": 500,
            "message": f"Server error during bulk creation: {str(e)}"
        }), 500


def process_single_bulk_item(index, raw_item, current_time):
    """
    Process a single item in the bulk submission.
    Each item has its own transaction - failures are rolled back individually.
    
    Args:
        index: The index of this item in the bulk array (0-based)
        raw_item: The raw item data from the request
        current_time: Current timestamp string for notifications
    
    Returns:
        dict with success status and details
    """
    listing_name = raw_item.get('listingName', f'Item {index + 1}')
    
    # Build base result with all item details (for tracking purposes)
    base_result = {
        "index": index,
        "listingName": listing_name,
        "producerID": raw_item.get('producerID'),
        "drinkType": raw_item.get('drinkType', ''),
        "typeCategory": raw_item.get('typeCategory', ''),
        "originCountry": raw_item.get('originCountry', ''),
        "abv": raw_item.get('abv', ''),
        "age": raw_item.get('age', ''),
        "bottler": raw_item.get('bottler', ''),
        "tags": raw_item.get('tags', ''),
        "order": raw_item.get('order'),
    }
    
    try:
        # ============ VALIDATION ============
        validation_error = validate_bulk_item(raw_item, index)
        if validation_error:
            return {
                **base_result,
                "success": False,
                "error": validation_error
            }
        
        # ============ PREPARE DATA ============
        processed_item = prepare_bulk_item_data(raw_item)
        
        # ============ DATABASE INSERT (with individual transaction) ============
        with db_manager.get_cursor() as cursor:
            
            # ------------------------------------------------------------------
            # [DUPLICATE CHECK - COMMENTED OUT FOR NOW]
            # Uncomment to enable duplicate listing detection
            # ------------------------------------------------------------------
            # cursor.execute('SELECT id FROM listings WHERE "listingName" = %s', (processed_item['listingName'],))
            # existing = cursor.fetchone()
            # if existing:
            #     return {
            #         **base_result,
            #         "success": False,
            #         "error": f"Duplicate listing: '{processed_item['listingName']}' already exists (ID: {existing['id']})"
            #     }
            # ------------------------------------------------------------------
            
            # Build and execute INSERT query
            columns = ', '.join(f'"{col}"' for col in processed_item.keys())
            placeholders = ', '.join(['%s'] * len(processed_item))
            sql = f"INSERT INTO listings ({columns}) VALUES ({placeholders}) RETURNING id"
            
            cursor.execute(sql, list(processed_item.values()))
            new_id = cursor.fetchone()['id']
            
            # ------------------------------------------------------------------
            # [PLACEHOLDER: PRODUCER FOLLOWER NOTIFICATIONS]
            # TODO: Implement producer follower notifications for bulk items
            # 
            # Logic from single-item endpoint:
            # 1. Check if producer has had <= 2 listings in last 24 hours (rate limit)
            # 2. If yes, fetch all users who follow this producer
            # 3. For each follower, create a "newDrink" notification
            # 
            # For bulk: Consider aggregating notifications (e.g., "Producer X added 5 new drinks")
            # instead of sending individual notifications for each item
            # 
            # Example implementation:
            # cutoff = datetime.now(pytz.timezone('Etc/GMT-8')) - timedelta(hours=24)
            # cursor.execute(
            #     'SELECT COUNT(*) FROM "listings" WHERE "producerID" = %s AND "addedDate" >= %s',
            #     (processed_item['producerID'], cutoff)
            # )
            # recent_count = cursor.fetchone()['count']
            # 
            # if recent_count <= 2:
            #     cursor.execute(
            #         'SELECT "userId" FROM "usersFollowLists" WHERE %s::text = ANY("producers")',
            #         (str(processed_item['producerID']),)
            #     )
            #     followers = [row['userId'] for row in cursor.fetchall()]
            #     
            #     slug = re.sub(r'[^a-z0-9]+', '', listing_name.lower())
            #     for uid in followers:
            #         notification_data = {
            #             "userId": uid,
            #             "userType": "user",
            #             "notiTabs": "venues & producers",
            #             "notiType": "newDrink",
            #             "image": processed_item.get('photo'),
            #             "link": f"/listing/view/{new_id}/{slug}",
            #             "message": f"{producer_name} added a new drink: {listing_name}",
            #             "createdAt": current_time,
            #         }
            #         notifications.add_notification_to_db(notification_data)
            # ------------------------------------------------------------------
            
            # ------------------------------------------------------------------
            # [PLACEHOLDER: APPROVAL NOTIFICATIONS]
            # TODO: If bulk items are linked to request IDs in the future,
            # implement approval notification logic here
            # 
            # For now, bulk submissions skip approval notifications since they
            # are not typically linked to user request submissions
            # ------------------------------------------------------------------
            
            return {
                **base_result,
                "success": True,
                "listingId": new_id
            }
            
    except Exception as e:
        # Any exception means this item's transaction is rolled back
        print(f"Bulk item {index} error: {str(e)}")
        return {
            **base_result,
            "success": False,
            "error": str(e)
        }


def validate_bulk_item(raw_item, index):
    """
    Validate a single bulk item before processing.
    
    Args:
        raw_item: The raw item data
        index: Item index for error messages
    
    Returns:
        Error message string if validation fails, None if valid
    """
    prefix = f"Item {index + 1}: "
    
    # Required field: listingName
    if not raw_item.get('listingName') or not str(raw_item.get('listingName', '')).strip():
        return f"{prefix}Listing name is required."
    
    # Required field: producerID
    if not raw_item.get('producerID'):
        return f"{prefix}Producer ID is required."
    
    # Required field: drinkType
    if not raw_item.get('drinkType') or not str(raw_item.get('drinkType', '')).strip():
        return f"{prefix}Drink type is required."
    
    # Required field: originCountry
    if not raw_item.get('originCountry') or not str(raw_item.get('originCountry', '')).strip():
        return f"{prefix}Country of origin is required."
    
    # Validate producerID is numeric
    try:
        int(raw_item.get('producerID'))
    except (ValueError, TypeError):
        return f"{prefix}Producer ID must be a valid integer."
    
    # Validate bottlerID if provided (must be numeric or empty)
    bottler_id = raw_item.get('bottlerID')
    if bottler_id and bottler_id != "":
        try:
            int(bottler_id)
        except (ValueError, TypeError):
            return f"{prefix}Bottler ID must be a valid integer or empty."
    
    # Validate order if provided (must be integer >= -1)
    order = raw_item.get('order')
    if order is not None and order != "":
        try:
            order_int = int(order)
            if order_int < -1:
                return f"{prefix}Order must be an integer >= -1."
        except (ValueError, TypeError):
            return f"{prefix}Order must be a valid integer."
    
    # Validate tags format if provided
    tags = raw_item.get('tags')
    if tags and str(tags).strip():
        tags_str = str(tags).strip()
        tag_list = [t.strip() for t in tags_str.split(',')]
        for tag in tag_list:
            if not tag.startswith('#'):
                return f"{prefix}Tags must start with # (invalid: '{tag}')."
            content = tag[1:]
            if not content or not content.isalnum():
                return f"{prefix}Tags must contain only letters/numbers after # (invalid: '{tag}')."
    
    return None  # Validation passed


def prepare_bulk_item_data(raw_item):
    """
    Prepare and sanitize a single bulk item for database insertion.
    Mirrors the data preparation logic from the single createListing endpoint.
    
    Args:
        raw_item: The raw item data from request
    
    Returns:
        dict: Processed item ready for database insertion
    """
    processed = {}
    
    # Add system fields
    processed['addedDate'] = datetime.now(pytz.timezone('Etc/GMT-8'))
    processed['allowMod'] = True
    
    # Process producerID (required, already validated)
    processed['producerID'] = int(raw_item['producerID'])
    
    # Process bottlerID (optional)
    bottler_id = raw_item.get('bottlerID')
    processed['bottlerID'] = int(bottler_id) if bottler_id and bottler_id != "" else None
    
    # Process string fields
    processed['listingName'] = str(raw_item.get('listingName', '')).strip()
    processed['sourceLink'] = str(raw_item.get('sourceLink', '')).strip()
    processed['officialDesc'] = str(raw_item.get('officialDesc', '')).strip()
    processed['reviewLink'] = str(raw_item.get('reviewLink', '')).strip()
    processed['originCountry'] = str(raw_item.get('originCountry', '')).strip()
    processed['drinkType'] = str(raw_item.get('drinkType', '')).strip()
    processed['typeCategory'] = str(raw_item.get('typeCategory', '')).strip()
    processed['drinkStyle'] = str(raw_item.get('drinkStyle', '')).strip()
    
    # Process bottler (with "Original Bottling" default already handled by frontend)
    processed['bottler'] = str(raw_item.get('bottler', '')).strip()
    
    # Process ABV (remove % sign and convert to float)
    abv_value = raw_item.get('abv', '')
    if abv_value:
        abv_str = str(abv_value).replace('%', '').strip()
        if abv_str:
            try:
                processed['abv'] = float(abv_str)
            except ValueError:
                processed['abv'] = None
        else:
            processed['abv'] = None
    else:
        processed['abv'] = None
    
    # Process age
    age_value = raw_item.get('age', '')
    processed['age'] = str(age_value).strip() if age_value else None
    
    # Process tags (ensure string or NULL)
    tags = raw_item.get('tags')
    if tags and str(tags).strip():
        processed['tags'] = str(tags).strip()
    else:
        processed['tags'] = None
    
    # Process order (ensure integer or NULL)
    order = raw_item.get('order')
    if order is not None and order != "":
        try:
            processed['order'] = int(order)
        except (ValueError, TypeError):
            processed['order'] = None
    else:
        processed['order'] = None
    
    # Process varietyTags (ensure PostgreSQL array or NULL)
    variety_tags = raw_item.get('varietyTags')
    if variety_tags is None or variety_tags == "" or variety_tags == []:
        processed['varietyTags'] = None
    elif isinstance(variety_tags, list):
        processed['varietyTags'] = variety_tags
    elif isinstance(variety_tags, str):
        try:
            parsed = json.loads(variety_tags)
            processed['varietyTags'] = parsed if isinstance(parsed, list) else None
        except:
            processed['varietyTags'] = None
    else:
        processed['varietyTags'] = None
    
    # ------------------------------------------------------------------
    # PROCESS PHOTO
    # ------------------------------------------------------------------
    # 
    # [PLACEHOLDER: IMAGE DOWNSCALING / OPTIMIZATION]
    # TODO: Implement image optimization before S3 upload
    # 
    # Future implementation should:
    # 1. Validate file type (JPEG, PNG, GIF, WebP only)
    # 2. Validate file size (max 10MB before processing)
    # 3. Scale down to max dimensions 800x600 pixels
    # 4. Maintain aspect ratio when scaling
    # 5. Enable high-quality image smoothing
    # 6. Compress to 80% JPEG quality
    # 7. Return optimized base64 data URL
    # 
    # Example placeholder function signature:
    # def optimize_image_for_upload(base64_string):
    #     """
    #     Optimize image for S3 upload.
    #     
    #     Args:
    #         base64_string: Raw base64 image data (with or without data URL prefix)
    #     
    #     Returns:
    #         str: Optimized base64 string ready for S3 upload
    #     
    #     Specifications:
    #         - Accepted formats: JPEG, PNG, GIF, WebP
    #         - Max input size: 10MB
    #         - Max output dimensions: 800x600 pixels
    #         - Output format: JPEG at 80% quality
    #         - Maintains aspect ratio
    #         - High-quality image smoothing enabled
    #     """
    #     # Import required libraries (PIL/Pillow)
    #     # from PIL import Image
    #     # import io
    #     # 
    #     # # Decode base64
    #     # # Validate file type and size
    #     # # Calculate scaled dimensions maintaining aspect ratio
    #     # # Resize with high-quality resampling (Image.LANCZOS)
    #     # # Compress to JPEG at 80% quality
    #     # # Return optimized base64
    #     pass
    # 
    # Usage:
    # photo_data = raw_item.get('photo')
    # if photo_data and photo_data.strip():
    #     optimized_photo = optimize_image_for_upload(photo_data)
    #     processed['photo'] = s3Images.uploadBase64ImageToS3(optimized_photo)
    # ------------------------------------------------------------------
    
    photo_data = raw_item.get('photo')
    if photo_data and str(photo_data).strip():
        # Strip data URL prefix if present
        base64_string = re.sub(r'^data:image\/[a-zA-Z]+;base64,', '', str(photo_data))
        processed['photo'] = s3Images.uploadBase64ImageToS3(base64_string)
    else:
        # Default image
        processed['photo'] = "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739"
    
    return processed


# ==================== STAGING IMPORTS HELPER FUNCTIONS ====================

def detect_csv_encoding(file):
    """Detect the encoding of a CSV file using chardet."""
    raw_data = file.read()
    detected_encoding = chardet.detect(raw_data)['encoding']
    print(f">detecting encoding: {detected_encoding}")
    file.seek(0)  # Reset the pointer to the start of the file
    return detected_encoding


def hash_password_for_producer(id, password):
    """Hash password for new producer creation (same as adminFunctions.py)."""
    combinedString = str(id) + password
    hash_val = 0
    for i in range(len(combinedString)):
        char = ord(combinedString[i])
        hash_val = (hash_val << 5) - hash_val + char
        hash_val &= 0xFFFFFFFF  # Convert to 32-bit integer
    if hash_val & (1 << 31):  # If the highest bit is set
        hash_val -= 1 << 32  # Convert to a signed integer
    return hash_val


# ==================== STAGING LISTINGS ENDPOINTS ====================

# -----------------------------------------------------------------------------------------
# [POST] Stage listings from CSV for review before final import
# - Parse CSV file and store in tempListingsForImport table
# - Does NOT create producers or insert into listings table yet
# - Uploads images to S3 immediately
# - Possible return codes: 201 (Staged), 400 (Invalid CSV), 500 (Error)
@blueprint.route('/stageListingsFromCSV', methods=['POST'])
def stageListingsFromCSV():
    try:
        # Get submitter info from form data
        submitter_id = request.form.get('submitterID')
        submitter_type = request.form.get('submitterType')
        
        if not submitter_id or not submitter_type:
            return jsonify({
                "code": 400,
                "message": "Missing required fields: submitterID and submitterType"
            }), 400
        
        if submitter_type not in ['user', 'producer', 'venue']:
            return jsonify({
                "code": 400,
                "message": "submitterType must be 'user', 'producer', or 'venue'"
            }), 400
        
        submitter_id = int(submitter_id)
        
        # Get the uploaded file
        if 'file' not in request.files:
            return jsonify({
                "code": 400,
                "message": "No file provided"
            }), 400
        
        file = request.files['file']
        
        if not file.filename.endswith('.csv'):
            return jsonify({
                "code": 400,
                "message": "File must be a CSV file"
            }), 400
        
        with db_manager.get_cursor() as cursor:
            # Detect encoding of CSV file
            file_encoding = detect_csv_encoding(file)
            
            # Define column data types (same as importListings)
            # Column order: listingName, producer, bottler, originCountry, drinkType, 
            #               typeCategory, drinkStyle, age, abv, reviewLink, officialDesc, sourceLink, photo
            column_data_types = [str, str, str, str, str, str, str, str, float, str, str, str, str]
            
            # Read all rows from CSV
            with io.TextIOWrapper(file, encoding=file_encoding, errors='replace') as csv_file:
                csv_data = csv.reader(csv_file)
                # Skip first 4 header rows (same as importListings)
                for _ in range(4):
                    try:
                        next(csv_data)
                    except StopIteration:
                        break
                rows = list(csv_data)
            
            if not rows:
                return jsonify({
                    "code": 400,
                    "message": "CSV file is empty or has no data rows"
                }), 400
            
            # Fetch existing producers to check if they exist
            cursor.execute('SELECT "producerName", "id", "isIndependentBottler" FROM "producers"')
            producers = cursor.fetchall()
            producer_name_id_dict = {row['producerName']: row['id'] for row in producers}
            producer_ib_dict = {row['producerName']: row.get('isIndependentBottler', False) for row in producers}
            
            staged_listings = []
            validation_errors = []
            image_urls = []
            row_numbers = []
            
            # Collect producer names for fuzzy matching
            producer_names_for_fuzzy = []
            bottler_names_for_fuzzy = []
            
            for row_index, row in enumerate(rows):
                row_number = row_index + 5  # Account for 4 skipped header rows + 1-based indexing
                
                # Skip empty rows
                if not row or all(cell.strip() == '' for cell in row):
                    continue
                
                # Validate row has enough columns
                if len(row) < len(column_data_types):
                    validation_errors.append({
                        "rowNumber": row_number,
                        "error": f"Row has {len(row)} columns, expected {len(column_data_types)}"
                    })
                    continue
                
                # Convert row data to appropriate types
                converted_row = []
                row_validation_error = None
                
                for i, (data_type, value) in enumerate(zip(column_data_types, row)):
                    if data_type is float:
                        value = value.replace('%', '').strip() if value else ''
                        try:
                            if value and value.lower() not in ['n/a', 'na', 'nas', '']:
                                converted_value = float(value)
                            else:
                                converted_value = None
                        except ValueError:
                            converted_value = None
                    else:
                        converted_value = data_type(value.strip()) if value and value.strip() else None
                    converted_row.append(converted_value)
                
                # Extract fields
                listing_name = converted_row[0]
                producer_name = converted_row[1]
                bottler_name = converted_row[2]
                origin_country = converted_row[3]
                drink_type = converted_row[4]
                type_category = converted_row[5]
                drink_style = converted_row[6]
                age = converted_row[7]
                abv = converted_row[8]
                review_link = converted_row[9]
                official_desc = converted_row[10]
                source_link = converted_row[11]
                photo_url = converted_row[12]
                
                # Validate required fields
                if not listing_name:
                    validation_errors.append({
                        "rowNumber": row_number,
                        "error": "Missing listing name (column 1)"
                    })
                    continue
                
                if not producer_name:
                    validation_errors.append({
                        "rowNumber": row_number,
                        "error": "Missing producer name (column 2)"
                    })
                    continue
                
                # Check if producer exists (exact match first)
                producer_id = producer_name_id_dict.get(producer_name)
                
                # Track producer names that don't have exact match for fuzzy matching later
                if not producer_id and producer_name:
                    producer_names_for_fuzzy.append(producer_name)
                
                # Handle bottler scenarios
                if bottler_name in ["OB", "Original Bottling", None, ""]:
                    bottler_id = None
                    bottler_name_display = "OB" if bottler_name in ["OB", "Original Bottling"] else None
                else:
                    bottler_id = producer_name_id_dict.get(bottler_name)
                    bottler_name_display = bottler_name
                    # Track bottler names that don't have exact match for fuzzy matching
                    if not bottler_id and bottler_name:
                        bottler_names_for_fuzzy.append(bottler_name)
                
                # Store image URL for later S3 upload
                image_urls.append(photo_url)
                row_numbers.append(row_number)
                
                staged_listings.append({
                    'listingName': listing_name,
                    'producerID': producer_id,
                    'producerName': producer_name,
                    'producerFuzzyMatched': False,  # Will be updated after fuzzy matching
                    'producerMatchedName': None,     # Will be updated after fuzzy matching
                    'producerMatchSimilarity': None, # Will be updated after fuzzy matching
                    'bottler': bottler_name_display,
                    'bottlerID': bottler_id,
                    'bottlerName': bottler_name if bottler_name not in ["OB", "Original Bottling", None, ""] else None,
                    'bottlerFuzzyMatched': False,    # Will be updated after fuzzy matching
                    'bottlerMatchedName': None,      # Will be updated after fuzzy matching
                    'bottlerMatchSimilarity': None,  # Will be updated after fuzzy matching
                    'originCountry': origin_country,
                    'drinkType': drink_type,
                    'typeCategory': type_category,
                    'drinkStyle': drink_style,
                    'age': str(age) if age else None,
                    'abv': abv,
                    'reviewLink': review_link,
                    'officialDesc': official_desc,
                    'sourceLink': source_link,
                    'photo': None,  # Will be updated after S3 upload
                    'allowMod': True,
                    'addedDate': None,  # Will be set when committed to listings
                    'submitterID': submitter_id,
                    'submitterType': submitter_type,
                    'rowNumber': row_number,
                    'validationErrors': None
                })
            
            if not staged_listings:
                return jsonify({
                    "code": 400,
                    "message": "No valid rows found in CSV",
                    "validationErrors": validation_errors
                }), 400
            
            # ====== STEP: Fuzzy match producers and bottlers that didn't have exact matches ======
            # Combine producer and bottler names for batch fuzzy matching
            all_names_for_fuzzy = list(set(producer_names_for_fuzzy + bottler_names_for_fuzzy))
            
            if all_names_for_fuzzy:
                print(f"Fuzzy matching {len(all_names_for_fuzzy)} producer/bottler names...")
                fuzzy_results = fuzzy_match_producer_batch(all_names_for_fuzzy, threshold=98, request_id=g.request_id if hasattr(g, 'request_id') else 'csv-staging')
                
                # Update staged listings with fuzzy match results
                for listing in staged_listings:
                    # Handle producer fuzzy match
                    producer_name = listing.get('producerName')
                    if producer_name and not listing.get('producerID'):
                        fuzzy_match = fuzzy_results.get(producer_name, {})
                        if fuzzy_match.get('matched'):
                            listing['producerID'] = fuzzy_match['producerID']
                            listing['producerFuzzyMatched'] = True
                            listing['producerMatchedName'] = fuzzy_match['matchedName']
                            listing['producerMatchSimilarity'] = fuzzy_match['similarity']
                            print(f"  Producer '{producer_name}' -> '{fuzzy_match['matchedName']}' ({fuzzy_match['similarity']}%)")
                    
                    # Handle bottler fuzzy match
                    bottler_name = listing.get('bottlerName')
                    if bottler_name and not listing.get('bottlerID'):
                        fuzzy_match = fuzzy_results.get(bottler_name, {})
                        if fuzzy_match.get('matched'):
                            listing['bottlerID'] = fuzzy_match['producerID']
                            listing['bottlerFuzzyMatched'] = True
                            listing['bottlerMatchedName'] = fuzzy_match['matchedName']
                            listing['bottlerMatchSimilarity'] = fuzzy_match['similarity']
                            print(f"  Bottler '{bottler_name}' -> '{fuzzy_match['matchedName']}' ({fuzzy_match['similarity']}%)")
                
                # Count fuzzy matches
                producer_fuzzy_count = sum(1 for l in staged_listings if l.get('producerFuzzyMatched'))
                bottler_fuzzy_count = sum(1 for l in staged_listings if l.get('bottlerFuzzyMatched'))
                print(f"Fuzzy matched {producer_fuzzy_count} producers and {bottler_fuzzy_count} bottlers")
            
            # Parallelize S3 image uploads while maintaining order
            DEFAULT_IMAGE_URL = "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739"

            def convert_google_drive_url(url):
                """
                Detects Google Drive share/view URLs and rewrites them to direct
                lh3.googleusercontent.com image links, which return the actual image
                bytes (for publicly shared files). Returns the original URL unchanged
                if it is not a recognised Google Drive pattern.
                Supported patterns:
                  - /file/d/FILE_ID/view?usp=sharing
                  - /file/d/FILE_ID/view?usp=drive_link
                  - /file/d/FILE_ID/view  (no query params)
                  - /open?id=FILE_ID
                  - /uc?id=FILE_ID
                """
                if 'drive.google.com' not in url:
                    return url
                # Pattern 1: /file/d/FILE_ID/...
                match = re.search(r'drive\.google\.com/file/d/([a-zA-Z0-9_-]+)', url)
                if match:
                    return f'https://lh3.googleusercontent.com/d/{match.group(1)}'
                # Pattern 2: /open?id=FILE_ID or /uc?id=FILE_ID
                match = re.search(r'drive\.google\.com/(?:open|uc)\?(?:.*&)?id=([a-zA-Z0-9_-]+)', url)
                if match:
                    return f'https://lh3.googleusercontent.com/d/{match.group(1)}'
                return url

            def upload_image_with_index(indexed_data):
                index, image_url = indexed_data
                if image_url and image_url.strip():
                    try:
                        transformed_url = convert_google_drive_url(image_url)
                        was_gdrive = (transformed_url != image_url)
                        s3_url = s3Images.uploadURLtoS3(transformed_url)
                        # uploadURLtoS3 returns its input URL unchanged on failure.
                        # If we transformed a GDrive URL and upload still failed
                        # (e.g. file is private), fall back to default image.
                        if was_gdrive and s3_url == transformed_url:
                            print(f"GDrive image not accessible (private?): {image_url}")
                            return index, DEFAULT_IMAGE_URL
                        return index, s3_url
                    except Exception as e:
                        print(f"Error uploading image from URL {image_url}: {str(e)}")
                        return index, DEFAULT_IMAGE_URL
                return index, DEFAULT_IMAGE_URL
            
            # Create indexed data to maintain order
            indexed_image_urls = list(enumerate(image_urls))
            s3_urls = [None] * len(image_urls)
            
            with ThreadPoolExecutor() as executor:
                future_to_index = {
                    executor.submit(upload_image_with_index, indexed_data): indexed_data[0]
                    for indexed_data in indexed_image_urls
                }
                for future in as_completed(future_to_index):
                    index, s3_url = future.result()
                    s3_urls[index] = s3_url
            
            print(f"S3 URLs for staging: {s3_urls}")
            
            # Update photo URLs in staged listings
            for listing, s3_url in zip(staged_listings, s3_urls):
                listing['photo'] = s3_url
            
            # Bulk insert into tempListingsForImport
            if staged_listings:
                insert_columns = [
                    "listingName", "producerID", "producerName", "bottler", "bottlerID", 
                    "bottlerName", "originCountry", "drinkType", "typeCategory", "drinkStyle",
                    "age", "abv", "reviewLink", "officialDesc", "sourceLink", "photo",
                    "allowMod", "addedDate", "submitterID", "submitterType", "rowNumber", "validationErrors"
                ]
                
                insert_query = """
                    INSERT INTO "tempListingsForImport" ({}) VALUES %s RETURNING id
                """.format(', '.join(f'"{col}"' for col in insert_columns))
                
                insert_values = [
                    (
                        listing['listingName'],
                        listing['producerID'],
                        listing['producerName'],
                        listing['bottler'],
                        listing['bottlerID'],
                        listing['bottlerName'],
                        listing['originCountry'],
                        listing['drinkType'],
                        listing['typeCategory'],
                        listing['drinkStyle'],
                        listing['age'],
                        listing['abv'],
                        listing['reviewLink'],
                        listing['officialDesc'],
                        listing['sourceLink'],
                        listing['photo'],
                        listing['allowMod'],
                        listing['addedDate'],
                        listing['submitterID'],
                        listing['submitterType'],
                        listing['rowNumber'],
                        listing['validationErrors']
                    )
                    for listing in staged_listings
                ]
                
                inserted_rows = execute_values(cursor, insert_query, insert_values, fetch=True)
                inserted_ids = [row['id'] for row in inserted_rows]
                
                # Add IDs to staged listings for response
                for listing, inserted_id in zip(staged_listings, inserted_ids):
                    listing['id'] = inserted_id
                
                print(f"Successfully staged {len(staged_listings)} listings")
            
            # ====== STEP: Detect duplicates for staged listings ======
            # Prepare listings in the format expected by detect_duplicates_batch
            listings_for_duplicate_check = [
                {
                    'id': listing['id'],
                    'listingName': listing['listingName'],
                    'producerId': listing.get('producerID', ''),
                    'producerName': listing.get('producerName', ''),
                    'drinkType': listing.get('drinkType', ''),
                    'originCountry': listing.get('originCountry', ''),
                    'bottlerId': listing.get('bottlerID', ''),
                    'bottlerName': listing.get('bottlerName', ''),
                    'age': listing.get('age', ''),
                    'abv': listing.get('abv')
                }
                for listing in staged_listings
            ]
            
            # Call duplicate detection (uses default threshold from detect_duplicates_batch)
            duplicate_results = detect_duplicates_batch(listings_for_duplicate_check)
            
            # Build a map of stagedListingId -> duplicate info for easy lookup
            duplicate_matches = {}
            for result in duplicate_results.get('results', []):
                duplicate_matches[result['stagedListingId']] = {
                    'isDuplicate': result['isDuplicate'],
                    'matches': result['matches']
                }
            
            # Add isDuplicate flag to each staged listing
            for listing in staged_listings:
                dup_info = duplicate_matches.get(listing['id'], {})
                listing['isDuplicate'] = dup_info.get('isDuplicate', False)
            
            print(f"Duplicate check complete: {duplicate_results.get('totalDuplicates', 0)} potential duplicates found")
            
            # Prepare response with staged listings, validation errors, and duplicate info
            response_data = {
                "staged": staged_listings,
                "stagedCount": len(staged_listings),
                "validationErrors": validation_errors,
                "errorCount": len(validation_errors),
                "duplicateMatches": duplicate_matches,
                "totalDuplicates": duplicate_results.get('totalDuplicates', 0)
            }
            
            return jsonify({
                "code": 201,
                "message": f"Successfully staged {len(staged_listings)} listings for review",
                "data": response_data
            }), 201
    
    except Exception as e:
        print(f"Error in stageListingsFromCSV: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "code": 500,
            "message": f"Error staging listings: {str(e)}"
        }), 500


# -----------------------------------------------------------------------------------------
# [GET] Get staged listings for a specific submitter
# - Fetch all staged listings from tempListingsForImport for the given submitter
# - Possible return codes: 200 (Success), 500 (Error)
@blueprint.route('/getStagedListings', methods=['GET'])
def getStagedListings():
    try:
        submitter_id = request.args.get('submitterID')
        submitter_type = request.args.get('submitterType')
        
        if not submitter_id or not submitter_type:
            return jsonify({
                "code": 400,
                "message": "Missing required query parameters: submitterID and submitterType"
            }), 400
        
        submitter_id = int(submitter_id)
        
        with db_manager.get_cursor() as cursor:
            cursor.execute('''
                SELECT * FROM "tempListingsForImport"
                WHERE "submitterID" = %s AND "submitterType" = %s
                ORDER BY "stagedAt" DESC, "rowNumber" ASC
            ''', (submitter_id, submitter_type))
            
            staged_listings = cursor.fetchall()
            
            # Convert to list of dicts
            listings_list = []
            for row in staged_listings:
                listings_list.append({
                    'id': row['id'],
                    'listingName': row['listingName'],
                    'producerID': row['producerID'],
                    'producerName': row['producerName'],
                    'bottler': row['bottler'],
                    'bottlerID': row['bottlerID'],
                    'bottlerName': row['bottlerName'],
                    'originCountry': row['originCountry'],
                    'drinkType': row['drinkType'],
                    'typeCategory': row['typeCategory'],
                    'drinkStyle': row['drinkStyle'],
                    'age': row['age'],
                    'abv': row['abv'],
                    'reviewLink': row['reviewLink'],
                    'officialDesc': row['officialDesc'],
                    'sourceLink': row['sourceLink'],
                    'photo': row['photo'],
                    'stagedAt': row['stagedAt'].isoformat() if row['stagedAt'] else None,
                    'rowNumber': row['rowNumber'],
                    'validationErrors': row['validationErrors']
                })
        
        return jsonify({
            "code": 200,
            "data": listings_list,
            "count": len(listings_list)
        }), 200
    
    except Exception as e:
        print(f"Error in getStagedListings: {str(e)}")
        return jsonify({
            "code": 500,
            "message": f"Error fetching staged listings: {str(e)}"
        }), 500


# -----------------------------------------------------------------------------------------
# [PUT] Update a single staged listing
# - Update a staged listing in tempListingsForImport
# - Possible return codes: 200 (Updated), 404 (Not found), 500 (Error)
@blueprint.route('/updateStagedListing/<int:id>', methods=['PUT'])
def updateStagedListing(id):
    try:
        data = request.get_json()
        
        with db_manager.get_cursor() as cursor:
            # Check if the staged listing exists
            cursor.execute('SELECT id FROM "tempListingsForImport" WHERE id = %s', (id,))
            existing = cursor.fetchone()
            
            if not existing:
                return jsonify({
                    "code": 404,
                    "message": f"Staged listing with ID {id} not found"
                }), 404
            
            # Build update query dynamically based on provided fields
            allowed_fields = [
                'listingName', 'producerID', 'producerName', 'bottler', 'bottlerID',
                'bottlerName', 'originCountry', 'drinkType', 'typeCategory', 'drinkStyle',
                'age', 'abv', 'reviewLink', 'officialDesc', 'sourceLink', 'photo'
            ]
            
            update_parts = []
            update_values = []
            
            for field in allowed_fields:
                if field in data:
                    update_parts.append(f'"{field}" = %s')
                    update_values.append(data[field])
            
            if not update_parts:
                return jsonify({
                    "code": 400,
                    "message": "No valid fields to update"
                }), 400
            
            update_values.append(id)  # For WHERE clause
            
            update_query = f'''
                UPDATE "tempListingsForImport"
                SET {', '.join(update_parts)}
                WHERE id = %s
            '''
            
            cursor.execute(update_query, update_values)
        
        return jsonify({
            "code": 200,
            "message": f"Staged listing {id} updated successfully"
        }), 200
    
    except Exception as e:
        print(f"Error in updateStagedListing: {str(e)}")
        return jsonify({
            "code": 500,
            "message": f"Error updating staged listing: {str(e)}"
        }), 500


# -----------------------------------------------------------------------------------------
# [DELETE] Delete a single staged listing
# - Remove a staged listing from tempListingsForImport
# - Possible return codes: 200 (Deleted), 404 (Not found), 500 (Error)
@blueprint.route('/deleteStagedListing/<int:id>', methods=['DELETE'])
def deleteStagedListing(id):
    try:
        with db_manager.get_cursor() as cursor:
            # Check if the staged listing exists
            cursor.execute('SELECT id FROM "tempListingsForImport" WHERE id = %s', (id,))
            existing = cursor.fetchone()
            
            if not existing:
                return jsonify({
                    "code": 404,
                    "message": f"Staged listing with ID {id} not found"
                }), 404
            
            cursor.execute('DELETE FROM "tempListingsForImport" WHERE id = %s', (id,))
        
        return jsonify({
            "code": 200,
            "message": f"Staged listing {id} deleted successfully"
        }), 200
    
    except Exception as e:
        print(f"Error in deleteStagedListing: {str(e)}")
        return jsonify({
            "code": 500,
            "message": f"Error deleting staged listing: {str(e)}"
        }), 500


# -----------------------------------------------------------------------------------------
# [POST] Commit selected staged listings to the listings table
# - Move selected staged listings to listings table
# - Create new producers/bottlers if they don't exist
# - Delete committed listings from tempListingsForImport
# - Possible return codes: 201 (Committed), 400 (Invalid), 500 (Error)
@blueprint.route('/commitStagedListings', methods=['POST'])
def commitStagedListings():
    try:
        data = request.get_json()
        staged_ids = data.get('stagedIds', [])
        update_existing = data.get('updateExistingListings', [])

        if not staged_ids and not update_existing:
            return jsonify({
                "code": 400,
                "message": "No staged listing IDs or update requests provided"
            }), 400

        with db_manager.get_cursor() as cursor:
            listings_to_insert = []
            created_listings_map = []
            new_producers_to_create = set()
            new_bottlers_to_create = set()

            # ====== PART 1: Create new listings from staged IDs ======
            if staged_ids:
                # Fetch the staged listings
                cursor.execute('''
                    SELECT * FROM "tempListingsForImport"
                    WHERE id = ANY(%s)
                ''', (staged_ids,))

                staged_listings = cursor.fetchall()

                if not staged_listings and not update_existing:
                    return jsonify({
                        "code": 404,
                        "message": "No staged listings found with the provided IDs"
                    }), 404

                if staged_listings:
                    # Fetch existing producers
                    cursor.execute('SELECT "producerName", "id", "isIndependentBottler" FROM "producers"')
                    producers = cursor.fetchall()
                    producer_name_id_dict = {row['producerName']: row['id'] for row in producers}

                    # Collect all producer and bottler names that need to be created
                    for listing in staged_listings:
                        producer_name = listing['producerName']
                        if producer_name and producer_name not in producer_name_id_dict:
                            new_producers_to_create.add(producer_name)

                        bottler_name = listing['bottlerName']
                        if bottler_name and bottler_name not in producer_name_id_dict and bottler_name not in new_producers_to_create:
                            new_bottlers_to_create.add(bottler_name)

                    # Create new producers
                    if new_producers_to_create:
                        new_producer_data = [
                            (
                                name, "", "", [], "", hash_password_for_producer(name, "admin1234"),
                                False, "", None, "", None, None, False
                            )
                            for name in new_producers_to_create
                        ]

                        insert_query = """
                            INSERT INTO producers (
                                "producerName", "producerDesc", "originCountry", "mainDrinks", "photo", "hashedPassword",
                                "claimStatus", "statusOB", "username", "producerLink", "stripeCustomerId", "claimStatusCheckDate",
                                "isIndependentBottler"
                            ) VALUES %s RETURNING "producerName", "id"
                        """
                        new_producers_with_ids = execute_values(cursor, insert_query, new_producer_data, fetch=True)
                        producer_name_id_dict.update({row["producerName"]: row["id"] for row in new_producers_with_ids})
                        print(f"Created {len(new_producers_with_ids)} new producers")

                    # Create new bottlers (as independent bottlers)
                    if new_bottlers_to_create:
                        new_bottler_data = [
                            (
                                name, "", "", [], "", hash_password_for_producer(name, "admin1234"),
                                False, "", None, "", None, None, True  # isIndependentBottler = True
                            )
                            for name in new_bottlers_to_create
                        ]

                        insert_query = """
                            INSERT INTO producers (
                                "producerName", "producerDesc", "originCountry", "mainDrinks", "photo", "hashedPassword",
                                "claimStatus", "statusOB", "username", "producerLink", "stripeCustomerId", "claimStatusCheckDate",
                                "isIndependentBottler"
                            ) VALUES %s RETURNING "producerName", "id"
                        """
                        new_bottlers_with_ids = execute_values(cursor, insert_query, new_bottler_data, fetch=True)
                        producer_name_id_dict.update({row["producerName"]: row["id"] for row in new_bottlers_with_ids})
                        print(f"Created {len(new_bottlers_with_ids)} new bottlers")

                    # Prepare listings for insertion into listings table
                    staged_id_order = []  # Track order of staged IDs for mapping back
                    current_time = datetime.now(pytz.timezone('Etc/GMT-8'))

                    for listing in staged_listings:
                        staged_id_order.append(listing['id'])  # Store the staged ID
                        producer_name = listing['producerName']
                        producer_id = producer_name_id_dict.get(producer_name)

                        bottler_name = listing['bottlerName']
                        if bottler_name:
                            bottler_id = producer_name_id_dict.get(bottler_name)
                        else:
                            bottler_id = None

                        listings_to_insert.append({
                            'listingName': listing['listingName'],
                            'producerID': producer_id,
                            'bottler': listing['bottler'],
                            'bottlerID': bottler_id,
                            'originCountry': listing['originCountry'],
                            'drinkType': listing['drinkType'],
                            'typeCategory': listing['typeCategory'],
                            'drinkStyle': listing['drinkStyle'],
                            'age': listing['age'],
                            'abv': listing['abv'],
                            'reviewLink': listing['reviewLink'],
                            'officialDesc': listing['officialDesc'],
                            'sourceLink': listing['sourceLink'],
                            'photo': listing['photo'],
                            'allowMod': True,
                            'addedDate': current_time
                        })

                    # Bulk insert into listings table
                    if listings_to_insert:
                        listing_columns = listings_to_insert[0].keys()
                        listing_query = """
                            INSERT INTO listings ({}) VALUES %s RETURNING id, "listingName"
                        """.format(', '.join(f'"{col}"' for col in listing_columns))

                        listing_values = [tuple(listing.values()) for listing in listings_to_insert]
                        inserted_listings = execute_values(cursor, listing_query, listing_values, fetch=True)

                        # Map staged IDs to new listing IDs (order is preserved)
                        for idx, inserted in enumerate(inserted_listings):
                            created_listings_map.append({
                                'stagedId': staged_id_order[idx],
                                'listingId': inserted['id'],
                                'listingName': inserted['listingName']
                            })

                        # Update the sequence to ensure future inserts don't conflict
                        cursor.execute("SELECT setval('listings_id_seq', COALESCE((SELECT MAX(id) FROM listings), 1), true)")

                        print(f"Successfully committed {len(inserted_listings)} listings to database")

                    # Delete committed listings from tempListingsForImport
                    cursor.execute('''
                        DELETE FROM "tempListingsForImport"
                        WHERE id = ANY(%s)
                    ''', (staged_ids,))

                    print(f"Deleted {len(staged_ids)} staged listings after commit")

            # ====== PART 2: Update existing listings for confirmed duplicates ======
            updated_existing_count = 0

            if update_existing:
                # Each item: { stagedId, linkedListingId, fieldsToUpdate: [...] }
                update_staged_ids = [item['stagedId'] for item in update_existing]

                cursor.execute('''
                    SELECT * FROM "tempListingsForImport"
                    WHERE id = ANY(%s)
                ''', (update_staged_ids,))
                staged_for_update = {row['id']: row for row in cursor.fetchall()}

                for item in update_existing:
                    staged = staged_for_update.get(item['stagedId'])
                    if not staged:
                        continue

                    fields_to_update = item.get('fieldsToUpdate', [])
                    if update_existing_listing(cursor, item['linkedListingId'], dict(staged), fields_to_update):
                        updated_existing_count += 1

                print(f"Updated {updated_existing_count} existing listings from confirmed duplicates")

        return jsonify({
            "code": 201,
            "message": f"Successfully committed {len(listings_to_insert)} listings",
            "data": {
                "committedCount": len(listings_to_insert),
                "newProducersCreated": len(new_producers_to_create),
                "newBottlersCreated": len(new_bottlers_to_create),
                "createdListings": created_listings_map,
                "updatedExistingCount": updated_existing_count
            }
        }), 201
    
    except Exception as e:
        print(f"Error in commitStagedListings: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "code": 500,
            "message": f"Error committing staged listings: {str(e)}"
        }), 500