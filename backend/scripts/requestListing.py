# Port: 5011
# Routes: /requestListing (POST), /requestListingModify/<requestID> (POST), /requestEdits (POST), /requestEditsModify/<requestID> (POST), /requestInaccuracy (POST), /requestReviewStatus/<requestID> (POST)
# Dataclass: RequestListings
# -----------------------------------------------------------------------------------------

import os
import json
import pytz
import s3Images
from flask import Blueprint, g, request, jsonify
from datetime import datetime, timedelta
from scripts import pointsHelperFunc, badge_helpers, notifications
import re

# Import the database manager for connection pooling
from app import db_manager

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

# -----------------------------------------------------------------------------------------
# [POST] Request for listing creation
# - Insert entry into the "requestListings" collection. Follows requestListings dataclass requirements.
# - Duplicate listing check: If a listing with the same name exists, reject the request
# - Possible return codes: 201 (Created), 400 (Duplicate Detected), 500 (Error during creation)
@blueprint.route("/requestListing", methods= ['POST'])
def requestListing():
    rawRequest = request.get_json()

    with db_manager.get_cursor() as cursor:
        # Check current system setting for auto approval
        cursor.execute('SELECT "settingValue" FROM "systemSettings" WHERE "settingName" = %s', ('autoListingApproval',))
        auto_approve = cursor.fetchone()
        auto_approve = auto_approve and auto_approve['settingValue'].lower() == 'true'

        rawRequestName = rawRequest["listingName"]
        # commented out duplicate check - as consistent with listing submission by admin
        # cursor.execute('SELECT id FROM listings WHERE "listingName" = %s', (rawRequestName,))
        # existingBottle = cursor.fetchone()

        # if existingBottle is not None:
        #     return jsonify(
        #         {
        #             "code": 400,
        #             "data": {
        #                 "listingName": rawRequestName
        #             },
        #             "message": "Bottle with the same name already exists."
        #         }
        #     ), 400

        try:
            if rawRequest['photo'] and rawRequest['photo'] != "":
                base64_string = re.sub(r'^data:image\/[a-zA-Z]+;base64,', '', rawRequest['photo'])
                rawRequest['photo'] = s3Images.uploadBase64ImageToS3(base64_string)
            else:
                rawRequest['photo'] = "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739"
        except Exception as e:
            print(f"Warning: Failed to process image: {str(e)}")
            rawRequest['photo'] = "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739"
        
        # Handle varietyTags field - ensure it's a PostgreSQL array or NULL
        if 'varietyTags' in rawRequest:
            if rawRequest['varietyTags'] is None or rawRequest['varietyTags'] == "" or rawRequest['varietyTags'] == []:
                rawRequest['varietyTags'] = None
            elif isinstance(rawRequest['varietyTags'], list):
                # It's already a list, keep it as is (will be converted to PostgreSQL array)
                pass
            elif isinstance(rawRequest['varietyTags'], str):
                # If it's a string, try to parse it as JSON array
                try:
                    rawRequest['varietyTags'] = json.loads(rawRequest['varietyTags'])
                except:
                    # If parsing fails, set to NULL
                    rawRequest['varietyTags'] = None
            else:
                rawRequest['varietyTags'] = None
        else:
            rawRequest['varietyTags'] = None
        
        # Handle nullable foreign keys
        producerId = rawRequest.get('producerID') or None
        userId = rawRequest.get('userID') or None
        bottler_id = rawRequest.get('bottlerID') or None
        
        # Determine submitter type from frontend
        submitter_type = rawRequest.get('submitterType', 'user')  # Default to 'user' for backwards compatibility
        
        # For venues submitting requests, store venue ID separately
        venue_id = None
        if submitter_type == 'venue':
            venue_id = userId  # Frontend sends venue ID in userID field
            userId = None      # Clear userId to avoid FK violation

        try:
            cursor.execute("""
                INSERT INTO "requestListings" (
                    "listingName", bottler, "drinkType", "sourceLink", "brandRelation", 
                    "reviewStatus", "userID", photo, "originCountry", "producerID", 
                    "bottlerID", "producerNew", "typeCategory", abv, age, "reviewLink", "drinkStyle", "officialDesc",
                    "submitterType", "venueID", "varietyTags"
                ) VALUES (%s, %s, %s, %s, %s, 
                          %s, %s, %s, %s, %s, 
                          %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id;
            """, (
                rawRequestName,
                rawRequest['bottler'],
                rawRequest['drinkType'],
                rawRequest['sourceLink'],
                rawRequest['brandRelation'],
                True if auto_approve else rawRequest['reviewStatus'],
                userId,  # Will be None for venue submissions
                rawRequest['photo'],
                rawRequest['originCountry'],
                producerId,
                bottler_id,
                rawRequest['producerNew'],
                rawRequest['typeCategory'],
                rawRequest['abv'],
                rawRequest['age'],
                rawRequest['reviewLink'],
                rawRequest.get('drinkStyle', ''),
                rawRequest.get('officialDesc', ''),
                submitter_type,
                venue_id,
                rawRequest.get('varietyTags', None)
            ))

            newRequestId = cursor.fetchone()
            
            # Auto-approve and create listing if setting is enabled
            # This section automatically creates a listing when auto-approval is enabled
            # It replicates the flow found in createListing.py to ensure consistency
            if auto_approve:
                # Create a new listing in the listings table
                current_time = datetime.now(pytz.timezone('Etc/GMT-8'))
                # Convert abv from string to float if necessary
                abv_converted = None
                if rawRequest['abv']:
                    try:
                        abv_value = str(rawRequest['abv']).replace('%', '')  # Remove the '%' sign
                        abv_converted = float(abv_value)
                    except (ValueError, TypeError):
                        print(f"Warning: Could not convert ABV value '{rawRequest['abv']}' to float")
                
                cursor.execute("""
                    INSERT INTO "listings" (
                        "listingName", "bottler", "drinkType", "sourceLink", 
                        "producerID", "bottlerID", "originCountry", "typeCategory", 
                        "abv", "age", "reviewLink", "drinkStyle", "officialDesc", 
                        "allowMod", "addedDate", "photo", "varietyTags"
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id;
                """, (
                    rawRequestName,
                    rawRequest['bottler'],
                    rawRequest['drinkType'],
                    rawRequest['sourceLink'],
                    producerId,
                    bottler_id,
                    rawRequest['originCountry'],
                    rawRequest['typeCategory'],
                    abv_converted,
                    rawRequest['age'],
                    rawRequest['reviewLink'],
                    rawRequest.get('drinkStyle', ''),
                    rawRequest.get('officialDesc', ''),
                    True,  # allowMod
                    current_time,
                    rawRequest['photo'],
                    rawRequest.get('varietyTags', None)
                ))
                
                listing_id = cursor.fetchone()['id']
                
                # Create notification for the submitter
                if submitter_type == 'venue' and venue_id:
                    # Venue submitter notification
                    # Create a URL-safe slug
                    slug = re.sub(r'[^a-z0-9]+', '', rawRequestName.lower())
                    
                    # Insert notification for venue
                    notification_data = {
                        "userId": venue_id,
                        "userType": "venue",
                        "notiTabs": "forYou",
                        "notiType": "approvedListing",
                        "image": rawRequest.get('photo'),
                        "link": f"/listing/view/{listing_id}/{slug}",
                        "message": f"Your listing request '{rawRequestName}' has been approved and is now live!",
                        "createdAt": current_time,
                    }
                    
                    notifications.add_notification_to_db(notification_data)
                    
                elif userId and submitter_type == 'user':
                    # Original user submitter logic
                    # Create a URL-safe slug
                    slug = re.sub(r'[^a-z0-9]+', '', rawRequestName.lower())
                    
                    # Insert notification
                    notification_data = {
                        "userId": userId,
                        "userType": "user",
                        "notiTabs": "forYou",
                        "notiType": "approvedListing",
                        "image": rawRequest.get('photo'),
                        "link": f"/listing/view/{listing_id}/{slug}",
                        "message": f"Your listing request '{rawRequestName}' has been approved and is now live!",
                        "createdAt": current_time,
                    }
                    
                    notifications.add_notification_to_db(notification_data)
                    
                    # Process any reward points or badges for users only
                    if pointsHelperFunc.check_max_proof_points(userId) is False:
                        # Add proof points for successful listing creation
                        cursor.execute(
                            'SELECT "proofPoints" FROM "pointSystemRules" WHERE id = 12;'
                        )
                        proof_points = cursor.fetchone()
                        if proof_points:
                            cursor.execute(
                                'UPDATE "pointsRecorder" SET "currentPoints" = "currentPoints" + %s WHERE "userID" = %s AND "userType" = %s;',
                                (proof_points['proofPoints'], userId, 'user')
                            )
                        
                        # 🚨 Note: badge_helpers.process_new_drink_badge still receives cursor parameter for compatibility
                        badge_result = badge_helpers.process_new_drink_badge(cursor.connection, cursor, userId)
                        if badge_result:
                            badge_notification = {
                                "userId": userId,
                                "userType": "user",
                                "notiTabs": "forYou",
                                "notiType": "badge_earned",
                                "image": None,
                                "link": f"/profile/user/{userId}",
                                "message": f"Congratulations! You earned a badge: {badge_result['badgeName']}.",
                                "createdAt": current_time,
                            }
                            notifications.add_notification_to_db(badge_notification)
                
                # Notify producer followers about the new listing
                if producerId:
                    # Check if this is the first listing in 24 hours for this producer
                    cutoff = datetime.now(pytz.timezone('Etc/GMT-8')) - timedelta(hours=24)
                    
                    cursor.execute(
                        'SELECT COUNT(*) FROM "listings" '
                        'WHERE "producerID" = %s AND "addedDate" >= %s',
                        (producerId, cutoff)
                    )
                    recent_count_row = cursor.fetchone()
                    recent_count = recent_count_row['count'] if recent_count_row else 0
                    print(f"Recent count: {recent_count}")

                    cursor.execute(
                        'SELECT "producerName" FROM "producers" WHERE id = %s',
                        (producerId,)
                    )
                    producer_row = cursor.fetchone()
                    producer_name = producer_row['producerName'] if producer_row else "A producer"

                    if recent_count <= 2:
                        # Build a URL-safe slug
                        slug = re.sub(r'[^a-z0-9]+', '', rawRequestName.lower())

                        # Fetch all users who follow this producer
                        cursor.execute(
                            'SELECT "userId" FROM "usersFollowLists" '
                            'WHERE %s::text = ANY("producers")',
                            (str(producerId),)
                        )
                        followers = [row['userId'] for row in cursor.fetchall()]

                        # Send notifications to followers
                        for uid in followers:
                            notification_data = {
                                "userId": uid,
                                "userType": "user",
                                "notiTabs": "venues & producers",
                                "notiType": "newDrink",
                                "image": rawRequest.get('photo'),
                                "link": f"/listing/view/{listing_id}/{slug}",
                                "message": f"{producer_name} added a new drink: {rawRequestName}",
                                "createdAt": current_time,
                            }
                            notifications.add_notification_to_db(notification_data)
            if newRequestId is None:
                raise Exception("Failed to retrieve the new request ID after insert.")

            return jsonify(
                {
                    "code": 201,
                    "data": {
                        "listingName": rawRequestName,
                        "requestId": newRequestId['id'],
                        "listingId": listing_id if auto_approve else None,
                        "autoApproved": auto_approve
                    }
                }
            ), 201

        except Exception as e:
            print(f"Error: {str(e)}")
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "listingName": rawRequestName
                    },
                    "message": "An error occurred while submitting the request."
                }
            ), 500


# -----------------------------------------------------------------------------------------
# [POST] Bulk Request for listing creation (formType='req')
# - Insert multiple entries into the "requestListings" collection
# - Each item is processed individually with isolated transaction rollback on failure
# - If auto-approval is enabled, listings are created immediately
# - Proof points and badges awarded once per bulk submission (not per item)
# - Supports both user and venue submitters
# - Possible return codes: 201 (Created - partial or full success), 400 (Validation Error), 500 (Server Error)
@blueprint.route("/requestListingBulk", methods=['POST'])
def requestListingsBulk():
    """
    Bulk endpoint for listing requests (formType='req').
    Accepts an array of items and processes each individually.
    Failed items are rolled back individually without affecting other items.
    """
    raw_request = request.get_json()
    
    # Expect 'items' array in the request body
    items = raw_request.get('items', [])
    
    if not items:
        return jsonify({
            "code": 400,
            "data": {
                "totalSubmitted": 0,
                "successCount": 0,
                "failCount": 0,
                "results": []
            },
            "message": "No items provided for bulk submission."
        }), 400
    
    # Track results for each item
    results = []
    success_count = 0
    fail_count = 0
    first_successful_user_id = None  # Track for proof points/badges (awarded once per bulk)
    first_successful_submitter_type = None
    
    # Check auto-approval setting once (applies to all items)
    with db_manager.get_cursor() as cursor:
        cursor.execute('SELECT "settingValue" FROM "systemSettings" WHERE "settingName" = %s', ('autoListingApproval',))
        auto_approve_row = cursor.fetchone()
        auto_approve = auto_approve_row and auto_approve_row['settingValue'].lower() == 'true'
    
    # Process each item individually
    for index, item in enumerate(items):
        item_result = process_single_bulk_request_item(index, item, auto_approve)
        results.append(item_result)
        
        if item_result['success']:
            success_count += 1
            # Track first successful user for proof points/badges (only users, not venues)
            if first_successful_user_id is None and item_result.get('submitterType') == 'user' and item_result.get('userID'):
                first_successful_user_id = item_result['userID']
                first_successful_submitter_type = 'user'
        else:
            fail_count += 1
    
    # Award proof points per successful item (only for user submitters)
    points_awarded = 0
    badge_awarded = None
    
    if success_count > 0 and first_successful_user_id and first_successful_submitter_type == 'user':
        try:
            with db_manager.get_cursor() as cursor:
                # Check if user has reached maximum proof points
                if not pointsHelperFunc.check_max_proof_points(first_successful_user_id):
                    # Get proof points for listing request (rule id = 12)
                    cursor.execute('SELECT "proofPoints" FROM "pointSystemRules" WHERE id = 12;')
                    proof_points_row = cursor.fetchone()
                    
                    if proof_points_row:
                        # Award 3 points per successful item
                        points_per_item = proof_points_row['proofPoints']
                        points_awarded = points_per_item * success_count
                        cursor.execute(
                            'UPDATE "pointsRecorder" SET "currentPoints" = "currentPoints" + %s WHERE "userID" = %s AND "userType" = %s;',
                            (points_awarded, first_successful_user_id, 'user')
                        )
                    
                    # Process badge (only once per bulk)
                    badge_result = badge_helpers.process_new_drink_badge(cursor.connection, cursor, first_successful_user_id)
                    if badge_result:
                        badge_awarded = badge_result
                        current_time = datetime.now(pytz.timezone('Etc/GMT-8'))
                        
                        # Get username for notification link
                        cursor.execute('SELECT username FROM users WHERE id = %s', (first_successful_user_id,))
                        user_row = cursor.fetchone()
                        user_username = user_row['username'] if user_row else ""
                        
                        badge_notification = {
                            "userId": first_successful_user_id,
                            "userType": "user",
                            "notiTabs": "forYou",
                            "notiType": "badge_earned",
                            "image": None,
                            "link": f"/profile/user/{first_successful_user_id}/{user_username}",
                            "message": f"Congratulations! You earned a badge: {badge_result['badgeName']}.",
                            "createdAt": current_time,
                        }
                        notifications.add_notification_to_db(badge_notification)
        except Exception as e:
            print(f"Warning: Failed to award proof points/badges for bulk submission: {str(e)}")
    
    # Determine response code
    response_code = 201 if success_count > 0 else 500
    
    return jsonify({
        "code": response_code,
        "data": {
            "totalSubmitted": len(items),
            "successCount": success_count,
            "failCount": fail_count,
            "autoApprovalEnabled": auto_approve,
            "pointsAwarded": points_awarded,
            "badgeAwarded": badge_awarded,
            "results": results
        },
        "message": f"Bulk submission complete. {success_count} succeeded, {fail_count} failed."
    }), response_code


def validate_bulk_request_item(index, item):
    """
    Validate a single item in the bulk request submission.
    Returns (is_valid, error_message, sanitized_item).
    """
    errors = []
    
    # Required field: listingName
    listing_name = item.get('listingName', '').strip() if item.get('listingName') else ''
    if not listing_name:
        errors.append("Listing name is required")
    
    # Required field: drinkType
    drink_type = item.get('drinkType', '').strip() if item.get('drinkType') else ''
    if not drink_type:
        errors.append("Drink type is required")
    
    # Required field: originCountry
    origin_country = item.get('originCountry', '').strip() if item.get('originCountry') else ''
    if not origin_country:
        errors.append("Origin country is required")
    
    # Either producerID or producerNew must be provided
    producer_id = item.get('producerID')
    producer_new = item.get('producerNew', '').strip() if item.get('producerNew') else ''
    if not producer_id and not producer_new:
        errors.append("Either producer ID or new producer name is required")
    
    if errors:
        return False, f"Item {index + 1}: {'; '.join(errors)}", None
    
    # Sanitize and prepare item data
    sanitized = {
        'listingName': listing_name,
        'drinkType': drink_type,
        'originCountry': origin_country,
        'producerID': producer_id if producer_id else None,
        'producerNew': producer_new,
        'bottler': item.get('bottler', '').strip() if item.get('bottler') else '',
        'bottlerID': item.get('bottlerID') if item.get('bottlerID') else None,
        'sourceLink': item.get('sourceLink', '').strip() if item.get('sourceLink') else '',
        'brandRelation': item.get('brandRelation', '').strip() if item.get('brandRelation') else '',
        'reviewStatus': item.get('reviewStatus', False),
        'userID': item.get('userID'),
        'photo': item.get('photo', ''),
        'typeCategory': item.get('typeCategory', '').strip() if item.get('typeCategory') else '',
        'abv': item.get('abv', '').strip() if item.get('abv') else '',
        'age': item.get('age', '').strip() if item.get('age') else '',
        'reviewLink': item.get('reviewLink', '').strip() if item.get('reviewLink') else '',
        'drinkStyle': item.get('drinkStyle', '').strip() if item.get('drinkStyle') else '',
        'officialDesc': item.get('officialDesc', '').strip() if item.get('officialDesc') else '',
        'submitterType': item.get('submitterType', 'user'),
        'varietyTags': item.get('varietyTags', None),
    }
    
    return True, None, sanitized


def optimize_bulk_request_image(base64_string):
    """
    Placeholder for future image optimization.
    Will implement:
    - Resize to max 800x600 while maintaining aspect ratio
    - Compress to 80% JPEG quality
    - Validate max file size (10MB)
    
    For now, just strips the data URL prefix and returns the base64 string.
    """
    # TODO: Implement actual image optimization using PIL/Pillow
    # from PIL import Image
    # import io
    # import base64
    #
    # # Decode base64 to image
    # image_data = base64.b64decode(base64_string)
    # image = Image.open(io.BytesIO(image_data))
    #
    # # Calculate new dimensions maintaining aspect ratio
    # max_width, max_height = 800, 600
    # width, height = image.size
    # scale = min(max_width / width, max_height / height, 1)
    # new_width = int(width * scale)
    # new_height = int(height * scale)
    #
    # # Resize if needed
    # if scale < 1:
    #     image = image.resize((new_width, new_height), Image.LANCZOS)
    #
    # # Convert to JPEG with 80% quality
    # output = io.BytesIO()
    # image.convert('RGB').save(output, format='JPEG', quality=80, optimize=True)
    # optimized_base64 = base64.b64encode(output.getvalue()).decode('utf-8')
    #
    # return optimized_base64
    
    # For now, just return the string as-is (optimization handled on frontend)
    return base64_string


def process_single_bulk_request_item(index, item, auto_approve):
    """
    Process a single item in the bulk request submission.
    Each item has its own transaction - if it fails, only this item is rolled back.
    Returns a detailed result dictionary.
    """
    # Validate the item first
    is_valid, error_message, sanitized_item = validate_bulk_request_item(index, item)
    
    if not is_valid:
        return {
            "index": index,
            "success": False,
            "error": error_message,
            "listingName": item.get('listingName', ''),
            "producerID": item.get('producerID'),
            "producerNew": item.get('producerNew', ''),
            "drinkType": item.get('drinkType', ''),
            "originCountry": item.get('originCountry', ''),
            "typeCategory": item.get('typeCategory', ''),
            "abv": item.get('abv', ''),
            "age": item.get('age', ''),
            "bottler": item.get('bottler', ''),
            "bottlerID": item.get('bottlerID'),
            "sourceLink": item.get('sourceLink', ''),
            "reviewLink": item.get('reviewLink', ''),
            "drinkStyle": item.get('drinkStyle', ''),
            "officialDesc": item.get('officialDesc', ''),
            "brandRelation": item.get('brandRelation', ''),
            "varietyTags": item.get('varietyTags'),
            "hasPhoto": bool(item.get('photo')),
            "submitterType": item.get('submitterType', 'user'),
            "userID": item.get('userID'),
            "requestId": None,
            "listingId": None,
            "autoApproved": False
        }
    
    # Duplicate check (commented out as per requirement - consistent with single item endpoint)
    # with db_manager.get_cursor() as cursor:
    #     cursor.execute('SELECT id FROM listings WHERE "listingName" = %s', (sanitized_item['listingName'],))
    #     existing_bottle = cursor.fetchone()
    #     if existing_bottle:
    #         return {
    #             "index": index,
    #             "success": False,
    #             "error": f"Item {index + 1}: A listing with this name already exists.",
    #             "listingName": sanitized_item['listingName'],
    #             "producerID": sanitized_item['producerID'],
    #             "producerNew": sanitized_item['producerNew'],
    #             "drinkType": sanitized_item['drinkType'],
    #             "originCountry": sanitized_item['originCountry'],
    #             "typeCategory": sanitized_item['typeCategory'],
    #             "abv": sanitized_item['abv'],
    #             "age": sanitized_item['age'],
    #             "bottler": sanitized_item['bottler'],
    #             "bottlerID": sanitized_item['bottlerID'],
    #             "sourceLink": sanitized_item['sourceLink'],
    #             "reviewLink": sanitized_item['reviewLink'],
    #             "drinkStyle": sanitized_item['drinkStyle'],
    #             "officialDesc": sanitized_item['officialDesc'],
    #             "brandRelation": sanitized_item['brandRelation'],
    #             "varietyTags": sanitized_item['varietyTags'],
    #             "hasPhoto": bool(sanitized_item['photo']),
    #             "submitterType": sanitized_item['submitterType'],
    #             "userID": sanitized_item['userID'],
    #             "requestId": None,
    #             "listingId": None,
    #             "autoApproved": False
    #         }
    
    # Process the item with its own transaction
    try:
        with db_manager.get_cursor() as cursor:
            # Process photo (sequential - one at a time)
            photo_url = "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739"
            if sanitized_item['photo'] and sanitized_item['photo'].strip():
                try:
                    # Strip data URL prefix if present
                    base64_string = re.sub(r'^data:image\/[a-zA-Z]+;base64,', '', sanitized_item['photo'])
                    # Apply optimization placeholder (for future implementation)
                    optimized_base64 = optimize_bulk_request_image(base64_string)
                    # Upload to S3
                    photo_url = s3Images.uploadBase64ImageToS3(optimized_base64)
                except Exception as e:
                    print(f"Warning: Failed to process image for item {index + 1}: {str(e)}")
                    # Keep default image on failure
            
            # Handle varietyTags field - ensure it's a PostgreSQL array or NULL
            variety_tags = sanitized_item.get('varietyTags')
            if variety_tags is None or variety_tags == "" or variety_tags == []:
                variety_tags = None
            elif isinstance(variety_tags, str):
                try:
                    variety_tags = json.loads(variety_tags)
                except:
                    variety_tags = None
            elif not isinstance(variety_tags, list):
                variety_tags = None
            
            # Handle nullable foreign keys
            producer_id = sanitized_item.get('producerID') or None
            user_id = sanitized_item.get('userID') or None
            bottler_id = sanitized_item.get('bottlerID') or None
            
            # Determine submitter type
            submitter_type = sanitized_item.get('submitterType', 'user')
            
            # For venues submitting requests, store venue ID separately
            venue_id = None
            if submitter_type == 'venue':
                venue_id = user_id  # Frontend sends venue ID in userID field
                user_id = None      # Clear userId to avoid FK violation
            
            # Insert into requestListings
            cursor.execute("""
                INSERT INTO "requestListings" (
                    "listingName", bottler, "drinkType", "sourceLink", "brandRelation", 
                    "reviewStatus", "userID", photo, "originCountry", "producerID", 
                    "bottlerID", "producerNew", "typeCategory", abv, age, "reviewLink", "drinkStyle", "officialDesc",
                    "submitterType", "venueID", "varietyTags"
                ) VALUES (%s, %s, %s, %s, %s, 
                          %s, %s, %s, %s, %s, 
                          %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id;
            """, (
                sanitized_item['listingName'],
                sanitized_item['bottler'],
                sanitized_item['drinkType'],
                sanitized_item['sourceLink'],
                sanitized_item['brandRelation'],
                True if auto_approve else sanitized_item['reviewStatus'],
                user_id,
                photo_url,
                sanitized_item['originCountry'],
                producer_id,
                bottler_id,
                sanitized_item['producerNew'],
                sanitized_item['typeCategory'],
                sanitized_item['abv'],
                sanitized_item['age'],
                sanitized_item['reviewLink'],
                sanitized_item['drinkStyle'],
                sanitized_item['officialDesc'],
                submitter_type,
                venue_id,
                variety_tags
            ))
            
            new_request_id = cursor.fetchone()['id']
            listing_id = None
            
            # Auto-approval: Create listing immediately if setting is enabled
            if auto_approve:
                current_time = datetime.now(pytz.timezone('Etc/GMT-8'))
                
                # Convert abv from string to float if necessary
                abv_converted = None
                if sanitized_item['abv']:
                    try:
                        abv_value = str(sanitized_item['abv']).replace('%', '')
                        abv_converted = float(abv_value)
                    except (ValueError, TypeError):
                        print(f"Warning: Could not convert ABV value '{sanitized_item['abv']}' to float")
                
                # Create listing in listings table
                cursor.execute("""
                    INSERT INTO "listings" (
                        "listingName", "bottler", "drinkType", "sourceLink", 
                        "producerID", "bottlerID", "originCountry", "typeCategory", 
                        "abv", "age", "reviewLink", "drinkStyle", "officialDesc", 
                        "allowMod", "addedDate", "photo", "varietyTags"
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id;
                """, (
                    sanitized_item['listingName'],
                    sanitized_item['bottler'],
                    sanitized_item['drinkType'],
                    sanitized_item['sourceLink'],
                    producer_id,
                    bottler_id,
                    sanitized_item['originCountry'],
                    sanitized_item['typeCategory'],
                    abv_converted,
                    sanitized_item['age'],
                    sanitized_item['reviewLink'],
                    sanitized_item['drinkStyle'],
                    sanitized_item['officialDesc'],
                    True,  # allowMod
                    current_time,
                    photo_url,
                    variety_tags
                ))
                
                listing_id = cursor.fetchone()['id']
                
                # =====================================================
                # NOTIFICATIONS FOR AUTO-APPROVED BULK ITEMS
                # Commented out for bulk - revisit later for performance optimization
                # Consider batching notifications or using async processing
                # =====================================================
                
                # # Notify submitter about approval
                # slug = re.sub(r'[^a-z0-9]+', '', sanitized_item['listingName'].lower())
                # 
                # if submitter_type == 'venue' and venue_id:
                #     # Venue submitter notification
                #     notification_data = {
                #         "userId": venue_id,
                #         "userType": "venue",
                #         "notiTabs": "forYou",
                #         "notiType": "approvedListing",
                #         "image": photo_url,
                #         "link": f"/listing/view/{listing_id}/{slug}",
                #         "message": f"Your listing request '{sanitized_item['listingName']}' has been approved and is now live!",
                #         "createdAt": current_time,
                #     }
                #     notifications.add_notification_to_db(notification_data)
                # 
                # elif user_id and submitter_type == 'user':
                #     # User submitter notification
                #     notification_data = {
                #         "userId": user_id,
                #         "userType": "user",
                #         "notiTabs": "forYou",
                #         "notiType": "approvedListing",
                #         "image": photo_url,
                #         "link": f"/listing/view/{listing_id}/{slug}",
                #         "message": f"Your listing request '{sanitized_item['listingName']}' has been approved and is now live!",
                #         "createdAt": current_time,
                #     }
                #     notifications.add_notification_to_db(notification_data)
                
                # =====================================================
                # PRODUCER FOLLOWER NOTIFICATIONS
                # Commented out for bulk - revisit later
                # Consider batching by producer to avoid duplicate notifications
                # =====================================================
                
                # if producer_id:
                #     # Check if this is the first listing in 24 hours for this producer
                #     cutoff = datetime.now(pytz.timezone('Etc/GMT-8')) - timedelta(hours=24)
                #     
                #     cursor.execute(
                #         'SELECT COUNT(*) FROM "listings" '
                #         'WHERE "producerID" = %s AND "addedDate" >= %s',
                #         (producer_id, cutoff)
                #     )
                #     recent_count_row = cursor.fetchone()
                #     recent_count = recent_count_row['count'] if recent_count_row else 0
                #     
                #     if recent_count <= 2:
                #         cursor.execute(
                #             'SELECT "producerName" FROM "producers" WHERE id = %s',
                #             (producer_id,)
                #         )
                #         producer_row = cursor.fetchone()
                #         producer_name = producer_row['producerName'] if producer_row else "A producer"
                #         
                #         slug = re.sub(r'[^a-z0-9]+', '', sanitized_item['listingName'].lower())
                #         
                #         # Fetch all users who follow this producer
                #         cursor.execute(
                #             'SELECT "userId" FROM "usersFollowLists" '
                #             'WHERE %s::text = ANY("producers")',
                #             (str(producer_id),)
                #         )
                #         followers = [row['userId'] for row in cursor.fetchall()]
                #         
                #         # Send notifications to followers
                #         for uid in followers:
                #             notification_data = {
                #                 "userId": uid,
                #                 "userType": "user",
                #                 "notiTabs": "venues & producers",
                #                 "notiType": "newDrink",
                #                 "image": photo_url,
                #                 "link": f"/listing/view/{listing_id}/{slug}",
                #                 "message": f"{producer_name} added a new drink: {sanitized_item['listingName']}",
                #                 "createdAt": current_time,
                #             }
                #             notifications.add_notification_to_db(notification_data)
            
            # Return success result with all details
            return {
                "index": index,
                "success": True,
                "error": None,
                "listingName": sanitized_item['listingName'],
                "producerID": producer_id,
                "producerNew": sanitized_item['producerNew'],
                "drinkType": sanitized_item['drinkType'],
                "originCountry": sanitized_item['originCountry'],
                "typeCategory": sanitized_item['typeCategory'],
                "abv": sanitized_item['abv'],
                "age": sanitized_item['age'],
                "bottler": sanitized_item['bottler'],
                "bottlerID": bottler_id,
                "sourceLink": sanitized_item['sourceLink'],
                "reviewLink": sanitized_item['reviewLink'],
                "drinkStyle": sanitized_item['drinkStyle'],
                "officialDesc": sanitized_item['officialDesc'],
                "brandRelation": sanitized_item['brandRelation'],
                "varietyTags": variety_tags,
                "photo": photo_url,
                "hasPhoto": photo_url != "https://cdn.shopify.com/s/files/1/0353/9510/9003/files/defaultDrinkImage.png?v=1750084739",
                "submitterType": submitter_type,
                "userID": user_id if submitter_type == 'user' else None,
                "venueID": venue_id if submitter_type == 'venue' else None,
                "requestId": new_request_id,
                "listingId": listing_id,
                "autoApproved": auto_approve and listing_id is not None
            }
    
    except Exception as e:
        print(f"Error processing bulk request item {index + 1}: {str(e)}")
        return {
            "index": index,
            "success": False,
            "error": f"Item {index + 1}: {str(e)}",
            "listingName": item.get('listingName', ''),
            "producerID": item.get('producerID'),
            "producerNew": item.get('producerNew', ''),
            "drinkType": item.get('drinkType', ''),
            "originCountry": item.get('originCountry', ''),
            "typeCategory": item.get('typeCategory', ''),
            "abv": item.get('abv', ''),
            "age": item.get('age', ''),
            "bottler": item.get('bottler', ''),
            "bottlerID": item.get('bottlerID'),
            "sourceLink": item.get('sourceLink', ''),
            "reviewLink": item.get('reviewLink', ''),
            "drinkStyle": item.get('drinkStyle', ''),
            "officialDesc": item.get('officialDesc', ''),
            "brandRelation": item.get('brandRelation', ''),
            "varietyTags": item.get('varietyTags'),
            "hasPhoto": bool(item.get('photo')),
            "submitterType": item.get('submitterType', 'user'),
            "userID": item.get('userID'),
            "requestId": None,
            "listingId": None,
            "autoApproved": False
        }


# -----------------------------------------------------------------------------------------
# [POST] Edit submitted request for listing creation
# - Update entry with specified id from the "requestListings" collection. Follows requestListings dataclass requirements.
# - Duplicate listing check: If a listing with the same name exists, reject the request
# - Possible return codes: 201 (Updated), 400 (Duplicate Detected), 500 (Error during update)
@blueprint.route("/requestListingModify/<string:requestID>", methods= ['POST'])
def requestListingModify(requestID):
    rawRequest = request.get_json()
    
    # Ensure all required fields are present in rawRequest, set to None if missing
    required_fields = [
        "listingName", "bottler", "drinkType", "sourceLink", "brandRelation",
        "reviewStatus", "userID", "photo", "originCountry", "producerID",
        "bottlerID", "producerNew", "typeCategory", "abv", "age", "reviewLink",
        "drinkStyle", "officialDesc"
    ]
    for field in required_fields:
        if field not in rawRequest:
            rawRequest[field] = None

    rawRequestName = rawRequest["listingName"]
    # cursor.execute('SELECT id FROM listings WHERE "listingName" = %s', (rawRequestName,))
    # existingBottle = cursor.fetchone()

    # if existingBottle is not None:
    #     return jsonify(
    #         {
    #             "code": 400,
    #             "data": {
    #                 "listingName": rawRequestName
    #             },
    #             "message": "Bottle with the same name already exists."
    #         }
    #     ), 400
        

    with db_manager.get_cursor() as cursor:
        # If rawRequest has photo, check if existingRequest has photo, delete if found, else upload image to s3 and save image in db
        if rawRequest['photo']:
            cursor.execute('SELECT photo FROM "requestListings" WHERE id = %s', (requestID,))
            existingRequest = cursor.fetchone()

            if existingRequest and existingRequest['photo'] and existingRequest['photo'].strip():
                try:
                    s3Images.deleteImageFromS3(existingRequest['photo'])
                except Exception as e:
                    print(f"Warning: Failed to delete existing image from S3: {str(e)}")
            if rawRequest['photo']:
                base64_string = re.sub(r'^data:image\/[a-zA-Z]+;base64,', '', rawRequest['photo'])
                rawRequest['photo'] = s3Images.uploadBase64ImageToS3(base64_string)

        producerId = rawRequest.get('producerID') or None
        userId = rawRequest.get('userID') or None
        bottler_id = rawRequest.get('bottlerID') or None
        
        # Determine submitter type from frontend
        submitter_type = rawRequest.get('submitterType', 'user')  # Default to 'user' for backwards compatibility
        
        # For venues submitting requests, store venue ID separately
        venue_id = None
        if submitter_type == 'venue':
            venue_id = userId  # Frontend sends venue ID in userID field
            userId = None      # Clear userId to avoid FK violation
        
        try:
            cursor.execute("""
                UPDATE "requestListings"
                SET "listingName" = %s, bottler = %s, "drinkType" = %s, "sourceLink" = %s, "brandRelation" = %s, 
                    "reviewStatus" = %s, "userID" = %s, photo = %s, "originCountry" = %s, "producerID" = %s, 
                    "bottlerID" = %s, "producerNew" = %s, "typeCategory" = %s, abv = %s, age = %s, "reviewLink" = %s, "drinkStyle" = %s, "officialDesc" = %s,
                    "submitterType" = %s, "venueID" = %s, "varietyTags" = %s
                WHERE id = %s;
            """, (
                rawRequestName,
                rawRequest['bottler'],
                rawRequest['drinkType'],
                rawRequest['sourceLink'],
                rawRequest['brandRelation'],
                rawRequest['reviewStatus'],
                userId,  # Will be None for venue submissions
                rawRequest['photo'],
                rawRequest['originCountry'],
                producerId,
                bottler_id,
                rawRequest['producerNew'],
                rawRequest['typeCategory'],
                rawRequest['abv'],
                rawRequest['age'],
                rawRequest['reviewLink'],
                rawRequest.get('drinkStyle', ''),
                rawRequest.get('officialDesc', ''),
                submitter_type,
                venue_id,
                rawRequest.get('varietyTags', None),
                requestID
            ))

            return jsonify(
                {
                    "code": 201,
                    "data": {
                        "listingName": rawRequestName,
                        "requestId": requestID
                    }
                }
            ), 201

        except Exception as e:
            print(f"Error: {str(e)}")
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "listingName": rawRequestName
                    },
                    "message": "An error occurred while submitting the request."
                }
            ), 500

# -----------------------------------------------------------------------------------------
# [POST] Request for listing modification
# - Insert entry into the "requestEdits" collection. Follows requestEdits dataclass requirements.
# - Possible return codes: 201 (Created), 400 (Invalid Listing), 500 (Error during creation)
@blueprint.route("/requestEdits", methods= ['POST'])
def requestEdits():
    rawRequest = request.get_json()

    rawListingID = int(rawRequest["listingID"])

    with db_manager.get_cursor() as cursor:
        cursor.execute('SELECT * FROM listings WHERE "id" = %s', (rawListingID,))
        existingListing = cursor.fetchone()

        if existingListing is None:
            return jsonify(
                {
                    "code": 400,
                    "data": {
                        "listingID": rawListingID
                    },
                    "message": "Linked listing is not valid!"
                }
            ), 400
        
        newRequest = {
            "editDesc": rawRequest["editDesc"],
            "listingID": rawListingID,
            "userID": int(rawRequest["userID"]),
            "brandRelation": rawRequest["brandRelation"],
            "reviewStatus": rawRequest["reviewStatus"],
            "duplicateLink": rawRequest.get("duplicateLink", ''),
            "sourceLink": rawRequest.get("sourceLink", '')
        }
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            # Insert new edit request into the database
            columns = ', '.join(f'"{key}"' for key in newRequest.keys())
            placeholders = ', '.join(['%s'] * len(newRequest))
            sql = f'INSERT INTO "requestEdits" ({columns}) VALUES ({placeholders})'
            
            cursor.execute(sql, list(newRequest.values()))

            # Build and insert notification for the producer who owns this listing

            producerId = existingListing["producerID"]
            listingName = existingListing["listingName"]

            cursor.execute('SELECT username FROM users WHERE id = %s', (newRequest["userID"],))
            userRow = cursor.fetchone()
            userUsername = userRow["username"] if userRow else "Someone"

            notification_data = {
                "userId": producerId,
                "userType": "producer",
                "notiTabs": "forYou",
                "notiType": "edit_request",
                "image": None,
                "link": f"/request/view",  # adjust this to the actual front-end route if needed
                "message": f"@{userUsername} requested an edit for {listingName}",
                "createdAt": current_time,
            }

            notifications.add_notification_to_db(notification_data)

            return jsonify(
                {
                    "code": 201,
                    "data": rawListingID
                }
            ), 201
        
        except Exception as e:
            print(str(e))
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "listingID": rawListingID
                    },
                    "message": "An error occurred while submitting the request."
                }
            ), 500

# -----------------------------------------------------------------------------------------
# [POST] Edit submitted request for listing modification
# - Update entry with specified id from the "requestEdits" collection. Follows requestEdits dataclass requirements.
# - Possible return codes: 201 (Updated), 400 (Invalid Listing), 500 (Error during update)
@blueprint.route("/requestEditsModify/<string:requestID>", methods= ['POST'])
def requestEditsModify(requestID):
    rawRequest = request.get_json()

    rawListingID = int(rawRequest["listingID"])

    with db_manager.get_cursor() as cursor:
        cursor.execute('SELECT * FROM listings WHERE "id" = %s', (rawListingID,))
        existingListing = cursor.fetchone()

        if existingListing is None:
            return jsonify(
                {
                    "code": 400,
                    "data": {
                        "listingID": rawListingID
                    },
                    "message": "Linked listing is not valid!"
                }
            ), 400
        
        newRequest = {
            "editDesc": rawRequest["editDesc"],
            "listingID": rawListingID,
            "userID": int(rawRequest["userID"]),
            "brandRelation": rawRequest["brandRelation"],
            "reviewStatus": rawRequest["reviewStatus"],
            "duplicateLink": rawRequest.get("duplicateLink", ''),
            "sourceLink": rawRequest.get("sourceLink", '')
        }

        try:
            # Insert new edit request into the database
            columns = ', '.join(f'"{key}"' for key in newRequest.keys())
            placeholders = ', '.join(['%s'] * len(newRequest))
            sql = f'UPDATE "requestEdits" SET ({columns}) = ({placeholders}) WHERE id = %s'
            
            cursor.execute(sql, list(newRequest.values()) + [requestID])

            return jsonify(
                {
                    "code": 201,
                    "data": rawListingID
                }
            ), 201
        
        except Exception as e:
            print(str(e))
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "listingID": rawListingID
                    },
                    "message": "An error occurred while submitting the request."
                }
            ), 500
    
# -----------------------------------------------------------------------------------------
# [POST] Request for listing modification in venue menu
# - Insert entry into the "requestInaccurate" collection. Follows requestInaccuracy dataclass requirements.
# - Possible return codes: 201 (Created), 400 (Duplicate request), 500 (Error during creation)
@blueprint.route("/requestInaccuracy", methods= ['POST'])
def requestInaccuracy():
    rawRequest = request.get_json()

    rawListingID = int(rawRequest["listingID"])
    rawVenueID = int(rawRequest["venueID"])
    rawUserID = int(rawRequest["userID"])

    with db_manager.get_cursor() as cursor:
        # Check if inaccuracy request is already submitted for the same bottle for a venue
        cursor.execute("""
            SELECT * FROM "requestInaccuracy"
            WHERE "listingId" = %s AND "venueId" = %s AND "userId" = %s;
        """, (rawListingID, rawVenueID, rawUserID))
        existingListing = cursor.fetchone()

        if existingListing is not None:
            return jsonify(
                {
                    "code": 400,
                    "data": {
                        "listingID": rawListingID
                    },
                    "message": "Duplicate request for inaccuracy!"
                }
            ), 400
        
        # Prepare new request
        reportDate = datetime.now(pytz.timezone('Etc/GMT-8'))
        inaccurateReason = rawRequest.get("inaccurateReason", "")

        try:
            cursor.execute(
                """
                    INSERT INTO "requestInaccuracy" ("listingId", "userId", "venueId", "reportDate", "inaccurateReason", "reviewStatus")
                    VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (rawListingID, rawUserID, rawVenueID, reportDate, inaccurateReason, False)
            )

            return jsonify(
                {
                    "code": 201,
                    "data": rawListingID
                }
            ), 201
        
        except Exception as e:
            print(str(e))
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "listingID": rawListingID
                    },
                    "message": "An error occurred while submitting the request."
                }
            ), 500

# -----------------------------------------------------------------------------------------
# [POST] Edit review status of a submitted request
# - Update entry with specified id from the specified collection.
# - Possible return codes: 201 (Updated), 500 (Error during update)

@blueprint.route("/requestReviewStatus/<string:requestID>", methods= ['POST'])
def requestReviewStatus(requestID):
    updateRequest = request.get_json()
    targetCollection = updateRequest["targetCollection"]
    status = updateRequest["reviewStatus"]
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        with db_manager.get_cursor() as cursor:
            if targetCollection == "requestInaccuracy":
                print(f"Handling requestInaccuracy for requestID: {requestID}")

            cursor.execute(
                f'UPDATE "{targetCollection}" SET "reviewStatus" = %s WHERE id = %s;',
                (status, requestID)
            )

            # Get the userID from the requestID
            cursor.execute(
                f'SELECT "userID" FROM "{targetCollection}" WHERE id = %s;',
                (requestID,)
            )
            userID_result = cursor.fetchone()
            
            if not userID_result:
                raise Exception(f"No user ID found for request ID {requestID}")
                
            user_id = userID_result['userID']
            
            # Check if user has reached maximum proof points
            if pointsHelperFunc.check_max_proof_points(user_id):
                return jsonify(
                    {
                        "code": 201,
                        "data": requestID
                    }
                ), 201

            # Initialize variables
            proofPoints = None
            badge_result = None

            # Process based on the target collection and status
            if targetCollection == "requestListings" and status == True:
                cursor.execute(
                    'SELECT "proofPoints" FROM "pointSystemRules" WHERE id = 12;'
                )
                proofPoints = cursor.fetchone()
                
                badge_result = badge_helpers.process_new_drink_badge(cursor.connection, cursor, user_id)

            elif targetCollection == "requestEdits" and status == True:
                # Get the proof points for successful edit suggestions
                cursor.execute(
                    'SELECT "proofPoints" FROM "pointSystemRules" WHERE id = 13;'
                )
                proofPoints = cursor.fetchone()
                
                # Process the "Brew-tiful Mind" badge for edit suggestions
                badge_result = badge_helpers.process_new_drink_badge(cursor.connection, cursor, user_id)
            
            # Update user's proof points if applicable
            if proofPoints is not None:
                # Update the user's proof points
                cursor.execute(
                    'UPDATE "pointsRecorder" SET "currentPoints" = "currentPoints" + %s WHERE "userID" = %s AND "userType" = %s;',
                    (proofPoints['proofPoints'], user_id, 'user')
                )

            cursor.execute('SELECT username FROM users WHERE id = %s', (user_id,))
            user_row = cursor.fetchone()
            if user_row:
                # Get the username of the user
                user_username = user_row['username'] if user_row else "Someone"
                
            # Notify if badge earned
            if badge_result:
                notification_data = {
                    "userId":   user_id,
                    "userType": "user",
                    "notiTabs": "forYou",
                    "notiType": "badge_earned",
                    "image":    None,
                    "link":     f"/profile/user/{user_id}/{user_username}",
                    "message":  f"Congratulations! You earned a badge: {badge_result['badgeName']}.",
                    "createdAt": current_time,
                }
                print("Adding notification for badge earned:", notification_data)
                notifications.add_notification_to_db(notification_data)        

            # Prepare the response
            response_data = {
                "code": 201,
                "data": requestID,
                "proofPointsAdded": proofPoints['proofPoints'] if proofPoints else 0,
            }
            
            if badge_result:
                response_data["badgeAwarded"] = badge_result
            
            return jsonify(response_data), 201
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify(
            {
                "code": 500,
                "data": {
                    "requestID": requestID
                },
                "message": "An error occurred while updating the review status."
            }
        ), 500