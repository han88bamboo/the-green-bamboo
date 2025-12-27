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
                    notifications.add_notification_to_db(approval_notification)

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
                    notifications.add_notification_to_db(notification_data)

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