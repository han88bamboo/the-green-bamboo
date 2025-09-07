# Port: 5002
# Routes: /addToCellar (POST)
# Dataclass: myCellarItems, myCellarCollections
# -----------------------------------------------------------------------------------------

import os
import json
from flask import Blueprint, g, request, jsonify
from datetime import datetime, date
from psycopg2.extras import RealDictCursor
from decimal import Decimal, InvalidOperation
import psycopg2


file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

# -----------------------------------------------------------------------------------------
# [POST] Add bottles to cellar
# - Creates master record with shared properties and individual bottle records
# - Uses listing, variant, format, volume number, and volume unit as composite key
# - Handles automatic collection creation if owner has no collections
# - Supports all owner types: user, producer, venue
# - Validates all input data and handles currency conversion
# - Possible return codes: 201 (Created), 400 (Validation Error), 404 (Not Found), 500 (Server Error)
@blueprint.route("/addToCellar", methods=['POST'])
def addToCellar():
    print("TZHBackendLog: ===========================================")
    print("TZHBackendLog: Starting addToCellar endpoint")
    
    try:
        conn = g.db
        cur = conn.cursor(cursor_factory=RealDictCursor)
        print("TZHBackendLog: Database connection established")
        
        data = request.get_json()
        print("TZHBackendLog: Raw request data received:")
        print(f"TZHBackendLog: {json.dumps(data, indent=2, default=str)}")
        print(f"TZHBackendLog: Request method: {request.method}")
        print(f"TZHBackendLog: Request headers: {dict(request.headers)}")
        print(f"TZHBackendLog: Request content type: {request.content_type}")
        
        # Validate required fields
        required_fields = ['listingId', 'ownerType', 'ownerId', 'quantity']
        print(f"TZHBackendLog: Validating required fields: {required_fields}")
        
        for field in required_fields:
            if field not in data or data[field] is None:
                error_msg = f"Missing required field: {field}"
                print(f"TZHBackendLog: Validation failed - {error_msg}")
                return jsonify({
                    "code": 400,
                    "message": error_msg
                }), 400
        
        print("TZHBackendLog: All required fields present")
        
        # Validate owner type
        print(f"TZHBackendLog: Validating ownerType: {data['ownerType']}")
        if data['ownerType'] not in ['user', 'producer', 'venue']:
            error_msg = "Invalid ownerType. Must be 'user', 'producer', or 'venue'."
            print(f"TZHBackendLog: {error_msg}")
            return jsonify({
                "code": 400,
                "message": error_msg
            }), 400
        
        print("TZHBackendLog: ownerType validation passed")
        
        # Validate quantity
        print(f"TZHBackendLog: Validating quantity: {data['quantity']}")
        try:
            quantity = int(data['quantity'])
            if quantity < 1:
                raise ValueError("Quantity must be positive")
            print(f"TZHBackendLog: Quantity validation passed: {quantity}")
        except (ValueError, TypeError) as e:
            error_msg = "Quantity must be a positive integer"
            print(f"TZHBackendLog: Quantity validation failed: {e}")
            return jsonify({
                "code": 400,
                "message": error_msg
            }), 400
        
        # Validate listing exists
        print(f"TZHBackendLog: Validating listing exists with ID: {data['listingId']}")
        cur.execute('SELECT "id", "listingName" FROM "listings" WHERE "id" = %s', (data['listingId'],))
        listing = cur.fetchone()
        if not listing:
            error_msg = f"Listing with ID {data['listingId']} not found"
            print(f"TZHBackendLog: {error_msg}")
            return jsonify({
                "code": 404,
                "message": error_msg
            }), 404
        
        print(f"TZHBackendLog: Listing found: {dict(listing)}")
        
        # Validate owner exists
        owner_table = f'"{data["ownerType"]}s"'  # users, producers, venues
        owner_id_field = '"id"'
        print(f"TZHBackendLog: Validating owner in table {owner_table} with ID: {data['ownerId']}")
        
        cur.execute(f'SELECT {owner_id_field} FROM {owner_table} WHERE {owner_id_field} = %s', (data['ownerId'],))
        owner = cur.fetchone()
        if not owner:
            error_msg = f"Owner with ID {data['ownerId']} not found in {data['ownerType']}s table"
            print(f"TZHBackendLog: {error_msg}")
            return jsonify({
                "code": 404,
                "message": error_msg
            }), 404
        
        print(f"TZHBackendLog: Owner found: {dict(owner)}")
        
        # Handle collection - get or create default collection
        collection_id = data.get('collectionId')
        print(f"TZHBackendLog: Processing collection ID: {collection_id}")
        
        if not collection_id:
            print("TZHBackendLog: No collection ID provided, finding or creating default collection")
            # Find or create default collection for this owner
            cur.execute("""
                SELECT "id" FROM "myCellarCollections" 
                WHERE "ownerID" = %s AND "ownerType" = %s AND "isDefault" = TRUE
            """, (data['ownerId'], data['ownerType']))
            
            default_collection = cur.fetchone()
            
            if not default_collection:
                print("TZHBackendLog: No default collection found, creating one")
                # Create default collection
                cur.execute("""
                    INSERT INTO "myCellarCollections" 
                    ("ownerID", "ownerType", "collectionName", "isDefault", "createdDate", "updatedDate")
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING "id"
                """, (
                    data['ownerId'], 
                    data['ownerType'], 
                    'General Collection',
                    True,
                    datetime.now(),
                    datetime.now()
                ))
                collection_id = cur.fetchone()['id']
                conn.commit()
                print(f"TZHBackendLog: Created new default collection with ID: {collection_id}")
            else:
                collection_id = default_collection['id']
                print(f"TZHBackendLog: Found existing default collection with ID: {collection_id}")
        else:
            print(f"TZHBackendLog: Validating provided collection {collection_id} belongs to owner")
            # Validate provided collection belongs to the owner
            cur.execute("""
                SELECT "id" FROM "myCellarCollections" 
                WHERE "id" = %s AND "ownerID" = %s AND "ownerType" = %s
            """, (collection_id, data['ownerId'], data['ownerType']))
            
            if not cur.fetchone():
                error_msg = "Collection does not belong to the specified owner"
                print(f"TZHBackendLog: {error_msg}")
                return jsonify({
                    "code": 400,
                    "message": error_msg
                }), 400
            print(f"TZHBackendLog: Collection validation passed for ID: {collection_id}")
        
        # Parse and validate dates
        def parse_date(date_str):
            if not date_str:
                return None
            try:
                return datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                try:
                    return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ').date()
                except ValueError:
                    return None
        
        print("TZHBackendLog: Parsing dates...")
        purchase_date = parse_date(data.get('purchaseDate'))
        delivery_date = parse_date(data.get('deliveryDate'))
        drink_onwards_date = parse_date(data.get('drinkOnwardsDate'))
        drink_by_date = parse_date(data.get('drinkByDate'))
        
        print(f"TZHBackendLog: Parsed dates - purchase: {purchase_date}, delivery: {delivery_date}, drink_onwards: {drink_onwards_date}, drink_by: {drink_by_date}")
        
        # Parse and validate prices
        def parse_price(price_str):
            if not price_str:
                return None
            try:
                return Decimal(str(price_str))
            except (InvalidOperation, TypeError, ValueError):
                return None
        
        print("TZHBackendLog: Parsing prices...")
        purchase_price = parse_price(data.get('purchasePrice'))
        current_value_estimation = parse_price(data.get('currentValueEstimation'))
        
        print(f"TZHBackendLog: Parsed prices - purchase: {purchase_price}, current_value: {current_value_estimation}")
        
        # Parse volume - store as user entered (no conversion)
        volume_number = None
        volume_unit = None
        print(f"TZHBackendLog: Parsing volume - raw volumeNumber: {data.get('volumeNumber')}")
        if data.get('volumeNumber'):  # Frontend now sends volumeNumber
            try:
                volume_number = float(data['volumeNumber'])
                volume_unit = data.get('volumeUnit', 'ml')  # Keep original unit
                print(f"TZHBackendLog: Parsed volume: {volume_number} {volume_unit}")
            except (ValueError, TypeError) as e:
                print(f"TZHBackendLog: Volume parsing failed: {e}")
                volume_number = None
                volume_unit = None
        
        # Parse variant (vintage)  
        variant = None
        print(f"TZHBackendLog: Parsing variant - raw variant: {data.get('variant')}")
        if data.get('variant'):
            try:
                variant = int(data['variant'])
                print(f"TZHBackendLog: Parsed variant: {variant}")
            except (ValueError, TypeError) as e:
                print(f"TZHBackendLog: Variant parsing failed: {e}")
                variant = None
        
        # Validate format, volume combination consistency
        format_value = data.get('format', 'Bottle')
        if not format_value:
            format_value = 'Bottle'  # Default format
        print(f"TZHBackendLog: Format value: {format_value}")
        
        # Ensure volume information is consistent
        if volume_number is not None and not volume_unit:
            error_msg = "Volume unit is required when volume number is provided"
            print(f"TZHBackendLog: {error_msg}")
            return jsonify({
                "code": 400,
                "message": error_msg
            }), 400
        
        # Check if master record already exists for this listing+variant+format+volume combination FOR THIS OWNER
        print("TZHBackendLog: Checking for existing master record...")
        print(f"TZHBackendLog: Looking for master with: listingID={data['listingId']}, variant={variant}, format={format_value}, volume={volume_number} {volume_unit} for owner {data['ownerType']} {data['ownerId']}")
        
        # First, let's debug what's actually in the database for this user (across all collections)
        cur.execute("""
            SELECT ci."id", ci."listingID", ci."variant", ci."quantityVariantID", ci."drinkFormat", 
                   ci."volumeNumber", ci."volumeUnit", ci."collectionID", cc."collectionName"
            FROM "myCellarItems" ci
            JOIN "myCellarCollections" cc ON ci."collectionID" = cc."id"
            WHERE ci."listingID" = %s 
            AND cc."ownerID" = %s 
            AND cc."ownerType" = %s
            ORDER BY ci."quantityVariantID"
        """, (data['listingId'], data['ownerId'], data['ownerType']))
        
        all_user_items = cur.fetchall()
        print(f"TZHBackendLog: All existing items for this listing across all user's collections:")
        for item in all_user_items:
            print(f"TZHBackendLog:   Item: {dict(item)}")
        
        # Now look for the specific master record across all user's collections
        cur.execute("""
            SELECT ci."id", ci."collectionID" FROM "myCellarItems" ci
            JOIN "myCellarCollections" cc ON ci."collectionID" = cc."id"
            WHERE ci."listingID" = %s 
            AND (ci."variant" = %s OR (ci."variant" IS NULL AND %s IS NULL))
            AND ci."quantityVariantID" = 1
            AND ci."drinkFormat" = %s
            AND ci."volumeNumber" = %s
            AND ci."volumeUnit" = %s
            AND cc."ownerID" = %s
            AND cc."ownerType" = %s
        """, (
            data['listingId'], 
            variant, 
            variant,  # For the NULL check
            format_value,
            volume_number,
            volume_unit,
            data['ownerId'],
            data['ownerType']
        ))
        
        master_record = cur.fetchone()
        existing_master_collection_id = None
        
        if master_record:
            existing_master_collection_id = master_record['collectionID']
            print(f"TZHBackendLog: Found existing master record with ID: {master_record['id']} in collection {existing_master_collection_id}")
            
            # Check if the master record is in a different collection than the requested one
            if existing_master_collection_id != collection_id:
                print(f"TZHBackendLog: Master record is in collection {existing_master_collection_id}, but new bottles requested for collection {collection_id}")
                print(f"TZHBackendLog: Will add bottles to the existing master's collection ({existing_master_collection_id}) to keep them grouped")
                # Use the existing master's collection to keep bottles grouped together
                collection_id = existing_master_collection_id
        
        if not master_record:
            print("TZHBackendLog: No existing master record found, creating new master record")
            # Create master record (quantityVariantID = 1) with shared properties AND first bottle's individual properties
            master_insert_data = (
                data['listingId'],
                collection_id,
                variant,
                1,  # Master record
                format_value,
                volume_number,
                volume_unit,
                drink_by_date,
                drink_onwards_date,
                current_value_estimation,
                data.get('currentValueCurrency', 'USD'),
                data.get('suggestedFoodPairing', '').strip() or None,
                # Individual properties for the first bottle (not defaults!)
                purchase_date,
                delivery_date,
                purchase_price,
                data.get('purchaseCurrency', 'USD'),
                data.get('purchaseVenueId'),
                data.get('purchasePlaceName', '').strip() or None,
                data.get('purchaseAddress', '').strip() or None,
                data.get('status', 'In Possession'),
                data.get('consumption', 'Unopened'),
                data.get('currentLocation', 'At Home'),
                data.get('subLocation', '').strip() or None,
                data.get('personalNotes', '').strip() or None,
                False,  # Not archived
                datetime.now(),
                datetime.now()
            )
            
            print(f"TZHBackendLog: Master record insert data: {master_insert_data}")
            
            cur.execute("""
                INSERT INTO "myCellarItems" (
                    "listingID", "collectionID", "variant", "quantityVariantID",
                    "drinkFormat", "volumeNumber", "volumeUnit", "drinkByDate", "drinkOnwardsDate",
                    "currentValueEstimation", "currentValueCurrency", "suggestedFoodPairing",
                    "purchaseDate", "deliveryDate", "purchasePrice", "purchaseCurrency",
                    "purchaseVenueID", "purchasePlaceName", "purchaseAddress",
                    "status", "consumption", "currentLocation", "subLocation",
                    "noteToSelf", "archiveStatus", "addedDate", "updatedDate"
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                ) RETURNING "id"
            """, master_insert_data)
            master_id = cur.fetchone()['id']
            print(f"TZHBackendLog: Created master record with ID: {master_id}")
            
            # Add master ID to created bottles list since it represents the first bottle
            created_bottle_ids = [master_id]
        else:
            master_id = master_record['id']
            print(f"TZHBackendLog: Found existing master record with ID: {master_id} in collection {collection_id}")
            
            # For existing master record, we need to create a new individual bottle record for the first bottle
            # since the existing master already represents someone else's first bottle
            created_bottle_ids = []
            
            # Update master record with new shared properties if provided
            # Note: drinkFormat, volumeNumber, volumeUnit are now part of the key and won't be updated
            update_fields = []
            update_values = []
            
            if drink_by_date is not None:
                update_fields.append('"drinkByDate" = %s')
                update_values.append(drink_by_date)
            
            if drink_onwards_date is not None:
                update_fields.append('"drinkOnwardsDate" = %s')
                update_values.append(drink_onwards_date)
            
            if current_value_estimation is not None:
                update_fields.append('"currentValueEstimation" = %s')
                update_values.append(current_value_estimation)
                update_fields.append('"currentValueCurrency" = %s')
                update_values.append(data.get('currentValueCurrency', 'USD'))
            
            if data.get('suggestedFoodPairing', '').strip():
                update_fields.append('"suggestedFoodPairing" = %s')
                update_values.append(data['suggestedFoodPairing'].strip())
            
            if update_fields:
                update_fields.append('"updatedDate" = %s')
                update_values.append(datetime.now())
                update_values.append(master_id)
                
                update_query = f"""
                    UPDATE "myCellarItems" 
                    SET {', '.join(update_fields)}
                    WHERE "id" = %s
                """
                print(f"TZHBackendLog: Updating master record with query: {update_query}")
                print(f"TZHBackendLog: Update values: {update_values}")
                cur.execute(update_query, update_values)
                print("TZHBackendLog: Master record updated")
        
        # Get next quantityVariantID for this listing+variant+format+volume combination FOR THIS OWNER
        print("TZHBackendLog: Getting next quantityVariantID...")
        cur.execute("""
            SELECT MAX(ci."quantityVariantID") as max_variant_id 
            FROM "myCellarItems" ci
            JOIN "myCellarCollections" cc ON ci."collectionID" = cc."id"
            WHERE ci."listingID" = %s 
            AND (ci."variant" = %s OR (ci."variant" IS NULL AND %s IS NULL))
            AND ci."drinkFormat" = %s
            AND ci."volumeNumber" = %s
            AND ci."volumeUnit" = %s
            AND cc."ownerID" = %s
            AND cc."ownerType" = %s
        """, (
            data['listingId'], 
            variant,
            variant,  # For the NULL check
            format_value,
            volume_number,
            volume_unit,
            data['ownerId'],
            data['ownerType']
        ))
        
        result = cur.fetchone()
        # Since we just created/found a master record (quantityVariantID = 1), 
        # individual bottles should start from 2
        max_existing_id = result['max_variant_id'] or 0
        if max_existing_id == 0:
            # This shouldn't happen since we just created a master record, but handle gracefully
            next_variant_id = 2
            print("TZHBackendLog: Warning: No existing records found, but master should exist. Starting from 2.")
        else:
            next_variant_id = max_existing_id + 1
        print(f"TZHBackendLog: Next quantityVariantID will be: {next_variant_id} (max existing: {max_existing_id})")
        
        # Create individual bottle records
        print(f"TZHBackendLog: Creating {quantity} individual bottle records...")
        
        if not master_record:
            # New master record case: master record IS the first bottle
            if quantity == 1:
                print("TZHBackendLog: Quantity is 1, only master record needed (already created)")
            else:
                # Create additional bottle records for quantities 2 and beyond
                print(f"TZHBackendLog: Creating {quantity - 1} additional individual bottle records...")
                
                for i in range(1, quantity):  # Start from 1 (second bottle) since master is first bottle
                    current_variant_id = next_variant_id + i - 1  # Adjust indexing
                    print(f"TZHBackendLog: Creating bottle {i+1}/{quantity} with quantityVariantID: {current_variant_id}")
                    
                    bottle_insert_data = (
                        data['listingId'],
                        collection_id,
                        variant,
                        current_variant_id,  # Individual bottle ID
                        purchase_date,
                        delivery_date,
                        purchase_price,
                        data.get('purchaseCurrency', 'USD'),
                        data.get('purchaseVenueId'),  # If provided
                        data.get('purchasePlaceName', '').strip() or None,
                        data.get('purchaseAddress', '').strip() or None,
                        data.get('status', 'In Possession'),
                        data.get('consumption', 'Unopened'),
                        data.get('currentLocation', 'At Home'),  # Database field: currentLocation
                        data.get('subLocation', '').strip() or None,
                        data.get('personalNotes', '').strip() or None,
                        False,  # Not archived
                        datetime.now(),
                        datetime.now()
                    )
                    
                    print(f"TZHBackendLog: Bottle {i+1} insert data: {bottle_insert_data}")
                    
                    cur.execute("""
                        INSERT INTO "myCellarItems" (
                            "listingID", "collectionID", "variant", "quantityVariantID",
                            "purchaseDate", "deliveryDate", "purchasePrice", "purchaseCurrency",
                            "purchaseVenueID", "purchasePlaceName", "purchaseAddress",
                            "status", "consumption", "currentLocation", "subLocation",
                            "noteToSelf", "archiveStatus", "addedDate", "updatedDate"
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                        ) RETURNING "id"
                    """, bottle_insert_data)
                    
                    bottle_id = cur.fetchone()['id']
                    created_bottle_ids.append(bottle_id)
                    print(f"TZHBackendLog: Created bottle {i+1} with ID: {bottle_id}")
        else:
            # Existing master record case: need to create ALL bottles as individual records
            print(f"TZHBackendLog: Master record exists, creating {quantity} individual bottle records...")
            
            for i in range(quantity):
                current_variant_id = next_variant_id + i
                print(f"TZHBackendLog: Creating bottle {i+1}/{quantity} with quantityVariantID: {current_variant_id}")
                
                bottle_insert_data = (
                    data['listingId'],
                    collection_id,
                    variant,
                    current_variant_id,  # Individual bottle ID
                    purchase_date,
                    delivery_date,
                    purchase_price,
                    data.get('purchaseCurrency', 'USD'),
                    data.get('purchaseVenueId'),  # If provided
                    data.get('purchasePlaceName', '').strip() or None,
                    data.get('purchaseAddress', '').strip() or None,
                    data.get('status', 'In Possession'),
                    data.get('consumption', 'Unopened'),
                    data.get('currentLocation', 'At Home'),  # Database field: currentLocation
                    data.get('subLocation', '').strip() or None,
                    data.get('personalNotes', '').strip() or None,
                    False,  # Not archived
                    datetime.now(),
                    datetime.now()
                )
                
                print(f"TZHBackendLog: Bottle {i+1} insert data: {bottle_insert_data}")
                
                cur.execute("""
                    INSERT INTO "myCellarItems" (
                        "listingID", "collectionID", "variant", "quantityVariantID",
                        "purchaseDate", "deliveryDate", "purchasePrice", "purchaseCurrency",
                        "purchaseVenueID", "purchasePlaceName", "purchaseAddress",
                        "status", "consumption", "currentLocation", "subLocation",
                        "noteToSelf", "archiveStatus", "addedDate", "updatedDate"
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    ) RETURNING "id"
                """, bottle_insert_data)
                
                bottle_id = cur.fetchone()['id']
                created_bottle_ids.append(bottle_id)
                print(f"TZHBackendLog: Created bottle {i+1} with ID: {bottle_id}")
        
        # Commit the transaction
        print("TZHBackendLog: Committing transaction...")
        conn.commit()
        print("TZHBackendLog: Transaction committed successfully")
        
        # Verify what was actually inserted into the database
        print("TZHBackendLog: Verifying inserted data...")
        
        # Query the master record
        cur.execute("""
            SELECT * FROM "myCellarItems" 
            WHERE "id" = %s
        """, (master_id,))
        master_data = cur.fetchone()
        print(f"TZHBackendLog: Master record in database: {dict(master_data) if master_data else 'NOT FOUND'}")
        
        # Query all individual bottle records
        for bottle_id in created_bottle_ids:
            cur.execute("""
                SELECT * FROM "myCellarItems" 
                WHERE "id" = %s
            """, (bottle_id,))
            bottle_data = cur.fetchone()
            print(f"TZHBackendLog: Bottle record {bottle_id} in database: {dict(bottle_data) if bottle_data else 'NOT FOUND'}")
        
        # Query all records for this listing+variant combination for this owner to see the full picture
        cur.execute("""
            SELECT ci."id", ci."quantityVariantID", ci."status", ci."consumption", ci."currentLocation", 
                   ci."purchasePrice", ci."drinkFormat", ci."volumeNumber", ci."volumeUnit",
                   ci."variant", ci."noteToSelf", ci."subLocation", ci."purchasePlaceName", ci."collectionID"
            FROM "myCellarItems" ci
            JOIN "myCellarCollections" cc ON ci."collectionID" = cc."id"
            WHERE ci."listingID" = %s 
            AND (ci."variant" = %s OR (ci."variant" IS NULL AND %s IS NULL))
            AND ci."drinkFormat" = %s
            AND ci."volumeNumber" = %s
            AND ci."volumeUnit" = %s
            AND cc."ownerID" = %s
            AND cc."ownerType" = %s
            ORDER BY ci."quantityVariantID"
        """, (data['listingId'], variant, variant, format_value, volume_number, volume_unit, data['ownerId'], data['ownerType']))
        all_records = cur.fetchall()
        print(f"TZHBackendLog: All records for this listing+variant:")
        for record in all_records:
            print(f"TZHBackendLog:   Record: {dict(record)}")
        
        response_data = {
            "code": 201,
            "message": f"Successfully added {quantity} bottle(s) to cellar",
            "data": {
                "masterId": master_id,
                "bottleIds": created_bottle_ids,
                "collectionId": collection_id,
                "listingId": data['listingId'],
                "listingName": listing['listingName'],
                "variant": variant,
                "drinkFormat": format_value,
                "volumeNumber": volume_number,
                "volumeUnit": volume_unit,
                "quantity": quantity,
                "addedDate": datetime.now().isoformat()
            }
        }
        
        print(f"TZHBackendLog: Preparing response: {json.dumps(response_data, indent=2, default=str)}")
        print("TZHBackendLog: Returning success response")
        print("TZHBackendLog: ===========================================")
        
        return jsonify(response_data), 201
        
    except psycopg2.Error as e:
        print(f"TZHBackendLog: Database error occurred: {str(e)}")
        print(f"TZHBackendLog: Database error type: {type(e).__name__}")
        print(f"TZHBackendLog: Database error code: {getattr(e, 'pgcode', 'N/A')}")
        print(f"TZHBackendLog: Database error detail: {getattr(e, 'pgerror', 'N/A')}")
        
        if conn:
            print("TZHBackendLog: Rolling back transaction due to database error")
            conn.rollback()
            
        print(f"TZHBackendLog: Database error in addToCellar: {str(e)}")
        print("TZHBackendLog: Returning 500 error response")
        print("TZHBackendLog: ===========================================")
        
        return jsonify({
            "code": 500,
            "message": f"Database error: {str(e)}"
        }), 500
        
    except Exception as e:
        print(f"TZHBackendLog: General exception occurred: {str(e)}")
        print(f"TZHBackendLog: Exception type: {type(e).__name__}")
        print(f"TZHBackendLog: Exception args: {e.args}")
        
        if conn:
            print("TZHBackendLog: Rolling back transaction due to general exception")
            conn.rollback()
            
        print(f"TZHBackendLog: Error in addToCellar: {str(e)}")
        print("TZHBackendLog: Returning 500 error response")
        print("TZHBackendLog: ===========================================")
        
        return jsonify({
            "code": 500,
            "message": f"Internal server error: {str(e)}"
        }), 500

# -----------------------------------------------------------------------------------------
# [GET] Get collection summary for an owner
# - Returns all collections for the specified owner with item counts
# - Useful for populating collection dropdowns in frontend
@blueprint.route("/getCollections/<ownerType>/<int:ownerID>", methods=['GET'])
def getCollections(ownerType, ownerID):
    try:
        conn = g.db
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Validate ownerType
        if ownerType not in ['user', 'producer', 'venue']:
            return jsonify({
                "code": 400,
                "message": "Invalid ownerType. Must be 'user', 'producer', or 'venue'."
            }), 400
        
        # Get collections for this owner
        cur.execute("""
            SELECT 
                cc."id",
                cc."collectionName",
                cc."isDefault",
                cc."isPublic",
                cc."createdDate",
                cc."updatedDate",
                COUNT(ci."id") as itemCount
            FROM "myCellarCollections" cc
            LEFT JOIN "myCellarItems" ci ON cc."id" = ci."collectionID" AND ci."archiveStatus" = FALSE
            WHERE cc."ownerID" = %s AND cc."ownerType" = %s
            GROUP BY cc."id"
            ORDER BY cc."isDefault" DESC, cc."collectionName"
        """, (ownerID, ownerType))
        
        collections = cur.fetchall()
        
        # Convert to list of dicts for JSON serialization
        collections_list = []
        for collection in collections:
            collections_list.append({
                "id": collection["id"],
                "collectionName": collection["collectionName"],
                "isDefault": collection["isDefault"],
                "isPublic": collection["isPublic"],
                "createdDate": collection["createdDate"].isoformat() if collection["createdDate"] else None,
                "updatedDate": collection["updatedDate"].isoformat() if collection["updatedDate"] else None,
                "itemCount": collection["itemCount"]
            })
        
        return jsonify({
            "code": 200,
            "data": {
                "collections": collections_list,
                "totalCollections": len(collections_list)
            }
        })
        
    except Exception as e:
        print(f"Error in getCollections: {str(e)}")
        return jsonify({
            "code": 500,
            "message": f"Error retrieving collections: {str(e)}"
        }), 500
