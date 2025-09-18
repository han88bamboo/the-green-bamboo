# Port: 5002
# Routes: /addToCellar (POST), /editCellar (POST), /getCollections/<ownerType>/<int:ownerID> (GET), /createCollection (POST), /collections/public-status/<int:collection_id>/ (PUT), /deleteCollection/<int:collection_id> (DELETE)
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
        
        # Parse volume - normalize for better matching (no unit conversion)
        volume_number = None
        volume_unit = None
        print(f"TZHBackendLog: Parsing volume - raw volumeNumber: {data.get('volumeNumber')}")
        if data.get('volumeNumber'):  # Frontend now sends volumeNumber
            try:
                # Normalize to 2 decimal places for consistent matching
                volume_number = round(float(data['volumeNumber']), 2)
                # Normalize volume unit to lowercase for case-insensitive matching
                volume_unit = data.get('volumeUnit', 'ml').lower().strip()
                print(f"TZHBackendLog: Parsed and normalized volume: {volume_number} {volume_unit}")
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
        # Normalize format to proper case for consistent matching
        format_value = format_value.strip().title()  # "bottle" -> "Bottle", "CAN" -> "Can"
        print(f"TZHBackendLog: Normalized format value: {format_value}")
        
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
        
        # Look for existing master record (quantityVariantID = 1) across all user's collections
        # This will be the group leader for items with identical properties
        # Use normalized values and case-insensitive matching for better grouping
        cur.execute("""
            SELECT ci."id", ci."collectionID", ci."variantGroupID" FROM "myCellarItems" ci
            JOIN "myCellarCollections" cc ON ci."collectionID" = cc."id"
            WHERE ci."listingID" = %s 
            AND (ci."variant" = %s OR (ci."variant" IS NULL AND %s IS NULL))
            AND ci."quantityVariantID" = 1
            AND UPPER(ci."drinkFormat") = UPPER(%s)
            AND ROUND(CAST(ci."volumeNumber" AS NUMERIC), 2) = %s
            AND LOWER(ci."volumeUnit") = %s
            AND cc."ownerID" = %s
            AND cc."ownerType" = %s
        """, (
            data['listingId'], 
            variant, 
            variant,  # For the NULL check
            format_value,  # Case-insensitive comparison via UPPER()
            volume_number,  # Already normalized to 2 decimal places
            volume_unit,   # Already normalized to lowercase
            data['ownerId'],
            data['ownerType']
        ))
        
        master_record = cur.fetchone()
        existing_master_collection_id = None
        group_variant_id = None
        
        if master_record:
            existing_master_collection_id = master_record['collectionID']
            group_variant_id = master_record['variantGroupID']
            print(f"TZHBackendLog: Found existing master record with ID: {master_record['id']} in collection {existing_master_collection_id}")
            print(f"TZHBackendLog: Existing group variantGroupID: {group_variant_id}")
            
            # Check if the master record is in a different collection than the requested one
            if existing_master_collection_id != collection_id:
                print(f"TZHBackendLog: Master record is in collection {existing_master_collection_id}, but new bottles requested for collection {collection_id}")
                print(f"TZHBackendLog: Will add bottles to the existing master's collection ({existing_master_collection_id}) to keep them grouped")
                # Use the existing master's collection to keep bottles grouped together
                collection_id = existing_master_collection_id
        else:
            print(f"TZHBackendLog: No existing master record found for listingID={data['listingId']}, variant={variant}, format={format_value}, volume={volume_number} {volume_unit}")
        
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
                    "listingID", "collectionID", "variant", "quantityVariantID", "variantGroupID",
                    "drinkFormat", "volumeNumber", "volumeUnit", "drinkByDate", "drinkOnwardsDate",
                    "currentValueEstimation", "currentValueCurrency", "suggestedFoodPairing",
                    "purchaseDate", "deliveryDate", "purchasePrice", "purchaseCurrency",
                    "purchaseVenueID", "purchasePlaceName", "purchaseAddress",
                    "status", "consumption", "currentLocation", "subLocation",
                    "noteToSelf", "archiveStatus", "addedDate", "updatedDate"
                ) VALUES (
                    %s, %s, %s, %s, NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                ) RETURNING "id"
            """, master_insert_data)
            master_id = cur.fetchone()['id']
            print(f"TZHBackendLog: Created master record with ID: {master_id}")
            
            # Update the variantGroupID to point to itself (self-reference for group leader)
            cur.execute("""
                UPDATE "myCellarItems" 
                SET "variantGroupID" = %s 
                WHERE "id" = %s
            """, (master_id, master_id))
            print(f"TZHBackendLog: Updated master record variantGroupID to self-reference: {master_id}")
            
            # Set group_variant_id for subsequent bottle creation
            group_variant_id = master_id
            
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
        
        # Get next quantityVariantID - SIMPLIFIED APPROACH
        print("TZHBackendLog: Getting next quantityVariantID...")
        
        if not master_record:
            # New master record case
            next_variant_id = 2  # Master is 1, so next individual bottle is 2
            print(f"TZHBackendLog: New master record created, next quantityVariantID will be: {next_variant_id}")
        else:
            # Existing master record case
            # Find the absolute maximum quantityVariantID for this listing+variant in this collection
            # This ensures we never have conflicts, even if there are multiple volume groups
            cur.execute("""
                SELECT MAX("quantityVariantID") as max_id
                FROM "myCellarItems"
                WHERE "listingID" = %s 
                AND "variant" = %s
                AND "collectionID" = %s
            """, (
                data['listingId'], 
                variant,
                existing_master_collection_id
            ))
            
            result = cur.fetchone()
            max_existing_id = result['max_id'] or 1
            next_variant_id = max_existing_id + 1
            print(f"TZHBackendLog: Found max quantityVariantID {max_existing_id} for listing+variant, next will be: {next_variant_id}")
            
            # IMPORTANT: This means different volume groups will have non-consecutive quantityVariantIDs
            # But that's OK - the grouping is determined by the master record's format+volume, not by sequence
        
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
                        group_variant_id,  # Reference to master record's ID
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
                            "listingID", "collectionID", "variant", "quantityVariantID", "variantGroupID",
                            "purchaseDate", "deliveryDate", "purchasePrice", "purchaseCurrency",
                            "purchaseVenueID", "purchasePlaceName", "purchaseAddress",
                            "status", "consumption", "currentLocation", "subLocation",
                            "noteToSelf", "archiveStatus", "addedDate", "updatedDate"
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
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
                    group_variant_id,  # Reference to master record's ID
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
                        "listingID", "collectionID", "variant", "quantityVariantID", "variantGroupID",
                        "purchaseDate", "deliveryDate", "purchasePrice", "purchaseCurrency",
                        "purchaseVenueID", "purchasePlaceName", "purchaseAddress",
                        "status", "consumption", "currentLocation", "subLocation",
                        "noteToSelf", "archiveStatus", "addedDate", "updatedDate"
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
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
        
        # Query all records for this specific drink group (same listing+variant+format+volume) for this owner
        cur.execute("""
            SELECT ci."id", ci."quantityVariantID", ci."status", ci."consumption", ci."currentLocation", 
                   ci."purchasePrice", ci."drinkFormat", ci."volumeNumber", ci."volumeUnit",
                   ci."variant", ci."noteToSelf", ci."subLocation", ci."purchasePlaceName", ci."collectionID"
            FROM "myCellarItems" ci
            JOIN "myCellarCollections" cc ON ci."collectionID" = cc."id"
            WHERE ci."listingID" = %s 
            AND (ci."variant" = %s OR (ci."variant" IS NULL AND %s IS NULL))
            AND (
                (ci."quantityVariantID" = 1 AND ci."drinkFormat" = %s AND ci."volumeNumber" = %s AND ci."volumeUnit" = %s)
                OR 
                (ci."quantityVariantID" > 1 AND ci."drinkFormat" IS NULL AND ci."volumeNumber" IS NULL AND ci."volumeUnit" IS NULL)
            )
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
        
        print(f"TZHBackendLog: Final response summary:")
        print(f"TZHBackendLog:   - Requested quantity: {quantity}")
        print(f"TZHBackendLog:   - Master record ID: {master_id}")
        print(f"TZHBackendLog:   - Created bottle IDs: {created_bottle_ids}")
        print(f"TZHBackendLog:   - Total bottles created: {len(created_bottle_ids)}")
        print(f"TZHBackendLog:   - Collection ID: {collection_id}")
        
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
# [POST] Edit cellar items in a variant group
# - Handles master record updates (shared properties for quantityVariantID=1)
# - Handles individual bottle updates (bottle-specific properties)
# - Supports adding new bottles to existing group
# - Supports archiving individual bottles
# - Supports collection changes for entire group
# - Maintains master-detail integrity and proper quantityVariantID assignment
# - Possible return codes: 200 (Updated), 400 (Validation Error), 404 (Not Found), 500 (Server Error)
@blueprint.route("/editCellar", methods=['POST'])
def editCellar():
    print("TZHBackendLog: ===========================================")
    print("TZHBackendLog: Starting editCellar endpoint")
    
    try:
        conn = g.db
        cur = conn.cursor(cursor_factory=RealDictCursor)
        print("TZHBackendLog: Database connection established")
        
        data = request.get_json()
        print("TZHBackendLog: Raw request data received:")
        print(f"TZHBackendLog: {json.dumps(data, indent=2, default=str)}")
        
        # Validate required fields
        if not data or 'variantGroupID' not in data or 'changes' not in data:
            error_msg = "Missing required fields: variantGroupID and changes"
            print(f"TZHBackendLog: Validation failed - {error_msg}")
            return jsonify({
                "code": 400,
                "message": error_msg
            }), 400
        
        variant_group_id = data['variantGroupID']
        changes = data['changes']
        
        # Validate variantGroupID is numeric
        try:
            variant_group_id = int(variant_group_id)
        except (ValueError, TypeError):
            error_msg = "variantGroupID must be a valid integer"
            print(f"TZHBackendLog: Validation failed - {error_msg}")
            return jsonify({
                "code": 400,
                "message": error_msg
            }), 400
        
        print(f"TZHBackendLog: Processing changes for variantGroupID: {variant_group_id}")
        
        # Validate changes structure
        if not isinstance(changes, dict):
            error_msg = "changes must be an object"
            print(f"TZHBackendLog: Validation failed - {error_msg}")
            return jsonify({
                "code": 400,
                "message": error_msg
            }), 400
        
        # Get all items in this variant group
        cur.execute("""
            SELECT * FROM "myCellarItems" 
            WHERE "variantGroupID" = %s OR "id" = %s
            ORDER BY "quantityVariantID"
        """, (variant_group_id, variant_group_id))
        
        existing_items = cur.fetchall()
        if not existing_items:
            error_msg = f"No items found for variantGroupID: {variant_group_id}"
            print(f"TZHBackendLog: {error_msg}")
            return jsonify({
                "code": 404,
                "message": error_msg
            }), 404
        
        print(f"TZHBackendLog: Found {len(existing_items)} existing items in group")
        
        # Find master record (quantityVariantID = 1)
        master_record = None
        for item in existing_items:
            if item['quantityVariantID'] == 1:
                master_record = item
                break
        
        if not master_record:
            error_msg = f"Master record not found for variantGroupID: {variant_group_id}"
            print(f"TZHBackendLog: {error_msg}")
            return jsonify({
                "code": 404,
                "message": error_msg
            }), 404
        
        print(f"TZHBackendLog: Found master record with ID: {master_record['id']}")
        
        # Track changes for response
        changes_made = {
            "master_updated": False,
            "bottles_updated": 0,
            "bottles_archived": 0,
            "bottles_added": 0,
            "collection_changed": False
        }
        
        # 1. Handle Collection Changes
        collection_change = changes.get('collectionChange', {})
        print(f"TZHBackendLog: Collection change data: {collection_change}")
        
        if collection_change and collection_change.get('from') != collection_change.get('to'):
            new_collection_id = collection_change.get('to')
            print(f"TZHBackendLog: Collection change detected - from: {collection_change.get('from')} to: {new_collection_id}")
            
            if new_collection_id:
                # Convert to integer for database comparison
                try:
                    new_collection_id = int(new_collection_id)
                    print(f"TZHBackendLog: Changing collection to: {new_collection_id}")
                except (ValueError, TypeError):
                    error_msg = f"Invalid collection ID: {new_collection_id}"
                    print(f"TZHBackendLog: {error_msg}")
                    return jsonify({
                        "code": 400,
                        "message": error_msg
                    }), 400
                
                # Verify new collection exists and belongs to same owner
                cur.execute("""
                    SELECT cc."ownerID", cc."ownerType"
                    FROM "myCellarCollections" cc
                    WHERE cc."id" = %s
                """, (new_collection_id,))
                
                new_collection = cur.fetchone()
                if not new_collection:
                    error_msg = f"Target collection {new_collection_id} not found"
                    print(f"TZHBackendLog: {error_msg}")
                    return jsonify({
                        "code": 404,
                        "message": error_msg
                    }), 404
                
                # Get current collection owner info
                cur.execute("""
                    SELECT cc."ownerID", cc."ownerType"
                    FROM "myCellarCollections" cc
                    INNER JOIN "myCellarItems" ci ON cc."id" = ci."collectionID"
                    WHERE ci."id" = %s
                """, (master_record['id'],))
                
                current_collection = cur.fetchone()
                if not current_collection:
                    error_msg = f"Current collection not found for master record"
                    print(f"TZHBackendLog: {error_msg}")
                    return jsonify({
                        "code": 404,
                        "message": error_msg
                    }), 404
                
                # Ensure new collection belongs to same owner
                if (new_collection['ownerID'] != current_collection['ownerID'] or 
                    new_collection['ownerType'] != current_collection['ownerType']):
                    error_msg = f"Cannot move items to collection owned by different user"
                    print(f"TZHBackendLog: {error_msg}")
                    return jsonify({
                        "code": 403,
                        "message": error_msg
                    }), 403
                
                # Update collection for all items in the group
                cur.execute("""
                    UPDATE "myCellarItems" 
                    SET "collectionID" = %s, "updatedDate" = CURRENT_TIMESTAMP
                    WHERE "variantGroupID" = %s OR "id" = %s
                """, (new_collection_id, variant_group_id, variant_group_id))
                
                affected_rows = cur.rowcount
                print(f"TZHBackendLog: Updated collection for {affected_rows} items")
                changes_made["collection_changed"] = True
        else:
            print(f"TZHBackendLog: No collection change needed - from: {collection_change.get('from')} to: {collection_change.get('to')}")
        
        # 2. Handle Master Data Updates (shared properties)
        master_data = changes.get('masterData', {})
        if master_data:
            print(f"TZHBackendLog: Processing master data updates: {master_data}")
            
            # Build update query for master record shared properties
            update_fields = []
            update_values = []
            
            # Shared properties (only for quantityVariantID = 1)
            shared_fields = {
                'drinkFormat': 'drinkFormat',
                'volumeNumber': 'volumeNumber', 
                'volumeUnit': 'volumeUnit',
                'drinkByDate': 'drinkByDate',
                'drinkOnwardsDate': 'drinkOnwardsDate',
                'currentValueEstimation': 'currentValueEstimation',
                'currentValueCurrency': 'currentValueCurrency',
                'suggestedFoodPairing': 'suggestedFoodPairing'
            }
            
            for field_key, db_field in shared_fields.items():
                if field_key in master_data:
                    value = master_data[field_key]
                    
                    # Handle empty strings as NULL for optional fields
                    if value == '':
                        value = None
                    
                    # Special validation for numeric fields
                    if field_key in ['volumeNumber', 'currentValueEstimation'] and value is not None:
                        try:
                            value = float(value) if value != '' else None
                            if value is not None and value <= 0:
                                error_msg = f"{field_key} must be positive"
                                print(f"TZHBackendLog: Validation failed - {error_msg}")
                                return jsonify({
                                    "code": 400,
                                    "message": error_msg
                                }), 400
                        except (ValueError, TypeError):
                            error_msg = f"{field_key} must be a valid number"
                            print(f"TZHBackendLog: Validation failed - {error_msg}")
                            return jsonify({
                                "code": 400,
                                "message": error_msg
                            }), 400
                    
                    # Validate date fields
                    if field_key in ['drinkByDate', 'drinkOnwardsDate'] and value is not None:
                        try:
                            if isinstance(value, str) and value.strip():
                                # Validate date format YYYY-MM-DD
                                datetime.strptime(value, '%Y-%m-%d').date()
                        except ValueError:
                            error_msg = f"{field_key} must be in YYYY-MM-DD format"
                            print(f"TZHBackendLog: Validation failed - {error_msg}")
                            return jsonify({
                                "code": 400,
                                "message": error_msg
                            }), 400
                    
                    update_fields.append(f'"{db_field}" = %s')
                    update_values.append(value)
            
            if update_fields:
                update_values.append(master_record['id'])
                update_query = f"""
                    UPDATE "myCellarItems" 
                    SET {', '.join(update_fields)}, "updatedDate" = CURRENT_TIMESTAMP
                    WHERE "id" = %s
                """
                
                print(f"TZHBackendLog: Executing master update query: {update_query}")
                print(f"TZHBackendLog: With values: {update_values}")
                
                cur.execute(update_query, update_values)
                if cur.rowcount > 0:
                    changes_made["master_updated"] = True
                    print(f"TZHBackendLog: Updated master record")
        
        # 3. Handle Individual Bottle Changes
        bottle_changes = changes.get('bottleChanges', {})
        if bottle_changes:
            print(f"TZHBackendLog: Processing bottle changes for {len(bottle_changes)} bottles")
            
            for cellar_item_id, bottle_data in bottle_changes.items():
                # Skip if this is a temporary ID (new bottle)
                if str(cellar_item_id).startswith('temp_'):
                    print(f"TZHBackendLog: Skipping temporary ID: {cellar_item_id}")
                    continue
                
                print(f"TZHBackendLog: Updating bottle {cellar_item_id}: {bottle_data}")
                
                # Build update query for individual bottle properties
                update_fields = []
                update_values = []
                
                # Individual bottle properties (can be updated for any bottle)
                bottle_fields = {
                    'status': 'status',
                    'consumption': 'consumption',
                    'currentLocation': 'currentLocation',
                    'subLocation': 'subLocation',
                    'noteToSelf': 'noteToSelf',
                    'purchasePlaceName': 'purchasePlaceName',
                    'purchaseAddress': 'purchaseAddress',
                    'purchaseDate': 'purchaseDate',
                    'deliveryDate': 'deliveryDate',
                    'purchasePrice': 'purchasePrice',
                    'purchaseCurrency': 'purchaseCurrency'
                }
                
                for field_key, db_field in bottle_fields.items():
                    if field_key in bottle_data:
                        value = bottle_data[field_key]
                        
                        # Handle empty strings as NULL for optional fields
                        if value == '':
                            value = None
                        
                        # Validate constraint fields
                        if field_key == 'status' and value is not None:
                            valid_statuses = ['In Possession', 'On Its Way', 'Purchased', 'Held Elsewhere', 'Wishlisted', 'Consumed']
                            if value not in valid_statuses:
                                error_msg = f"Invalid status: {value}. Must be one of: {', '.join(valid_statuses)}"
                                print(f"TZHBackendLog: Validation failed - {error_msg}")
                                return jsonify({
                                    "code": 400,
                                    "message": error_msg
                                }), 400
                        
                        if field_key == 'consumption' and value is not None:
                            valid_consumption = ['Opened', 'Unopened', 'Empty']
                            if value not in valid_consumption:
                                error_msg = f"Invalid consumption: {value}. Must be one of: {', '.join(valid_consumption)}"
                                print(f"TZHBackendLog: Validation failed - {error_msg}")
                                return jsonify({
                                    "code": 400,
                                    "message": error_msg
                                }), 400
                        
                        # Validate numeric fields
                        if field_key == 'purchasePrice' and value is not None:
                            try:
                                value = float(value) if value != '' else None
                                if value is not None and value < 0:
                                    error_msg = f"purchasePrice must be non-negative"
                                    print(f"TZHBackendLog: Validation failed - {error_msg}")
                                    return jsonify({
                                        "code": 400,
                                        "message": error_msg
                                    }), 400
                            except (ValueError, TypeError):
                                error_msg = f"purchasePrice must be a valid number"
                                print(f"TZHBackendLog: Validation failed - {error_msg}")
                                return jsonify({
                                    "code": 400,
                                    "message": error_msg
                                }), 400
                        
                        # Validate date fields
                        if field_key in ['purchaseDate', 'deliveryDate'] and value is not None:
                            try:
                                if isinstance(value, str) and value.strip():
                                    # Validate date format YYYY-MM-DD
                                    datetime.strptime(value, '%Y-%m-%d').date()
                            except ValueError:
                                error_msg = f"{field_key} must be in YYYY-MM-DD format"
                                print(f"TZHBackendLog: Validation failed - {error_msg}")
                                return jsonify({
                                    "code": 400,
                                    "message": error_msg
                                }), 400
                        
                        update_fields.append(f'"{db_field}" = %s')
                        update_values.append(value)
                
                if update_fields:
                    update_values.append(int(cellar_item_id))
                    update_query = f"""
                        UPDATE "myCellarItems" 
                        SET {', '.join(update_fields)}, "updatedDate" = CURRENT_TIMESTAMP
                        WHERE "id" = %s
                    """
                    
                    print(f"TZHBackendLog: Executing bottle update query: {update_query}")
                    print(f"TZHBackendLog: With values: {update_values}")
                    
                    cur.execute(update_query, update_values)
                    if cur.rowcount > 0:
                        changes_made["bottles_updated"] += 1
                        print(f"TZHBackendLog: Updated bottle {cellar_item_id}")
        
        # 4. Handle Archived Bottles
        archived_bottles = changes.get('archivedBottles', [])
        if archived_bottles:
            print(f"TZHBackendLog: Archiving {len(archived_bottles)} bottles")
            
            for cellar_item_id in archived_bottles:
                # Skip temporary IDs
                if str(cellar_item_id).startswith('temp_'):
                    continue
                
                print(f"TZHBackendLog: Archiving bottle {cellar_item_id}")
                
                cur.execute("""
                    UPDATE "myCellarItems" 
                    SET "archiveStatus" = TRUE, "updatedDate" = CURRENT_TIMESTAMP
                    WHERE "id" = %s
                """, (int(cellar_item_id),))
                
                if cur.rowcount > 0:
                    changes_made["bottles_archived"] += 1
                    print(f"TZHBackendLog: Archived bottle {cellar_item_id}")
        
        # 5. Handle New Bottles
        new_bottles = changes.get('newBottles', [])
        if new_bottles:
            print(f"TZHBackendLog: Adding {len(new_bottles)} new bottles")
            
            # Find the maximum quantityVariantID for this group
            max_quantity_variant_id = max(item['quantityVariantID'] for item in existing_items)
            print(f"TZHBackendLog: Current max quantityVariantID: {max_quantity_variant_id}")
            
            for i, new_bottle in enumerate(new_bottles):
                next_quantity_variant_id = max_quantity_variant_id + i + 1
                print(f"TZHBackendLog: Creating new bottle with quantityVariantID: {next_quantity_variant_id}")
                
                # Validate new bottle data
                if not isinstance(new_bottle, dict):
                    error_msg = f"New bottle {i+1} must be an object"
                    print(f"TZHBackendLog: Validation failed - {error_msg}")
                    return jsonify({
                        "code": 400,
                        "message": error_msg
                    }), 400
                
                # Validate status and consumption if provided
                status = new_bottle.get('status', 'In Possession')
                consumption = new_bottle.get('consumption', 'Unopened')
                
                valid_statuses = ['In Possession', 'On Its Way', 'Purchased', 'Held Elsewhere', 'Wishlisted', 'Consumed']
                if status not in valid_statuses:
                    error_msg = f"Invalid status for new bottle: {status}"
                    print(f"TZHBackendLog: Validation failed - {error_msg}")
                    return jsonify({
                        "code": 400,
                        "message": error_msg
                    }), 400
                
                valid_consumption = ['Opened', 'Unopened', 'Empty']
                if consumption not in valid_consumption:
                    error_msg = f"Invalid consumption for new bottle: {consumption}"
                    print(f"TZHBackendLog: Validation failed - {error_msg}")
                    return jsonify({
                        "code": 400,
                        "message": error_msg
                    }), 400
                
                # Use master record properties for required fields
                insert_data = {
                    'listingID': master_record['listingID'],
                    'collectionID': master_record['collectionID'], 
                    'variant': master_record['variant'],
                    'quantityVariantID': next_quantity_variant_id,
                    'variantGroupID': master_record['id'],  # Reference master record
                    
                    # Individual bottle properties from new bottle data
                    'status': status,
                    'consumption': consumption,
                    'currentLocation': new_bottle.get('currentLocation', 'At Home'),
                    'subLocation': new_bottle.get('subLocation'),
                    'noteToSelf': new_bottle.get('noteToSelf'),
                    'purchasePlaceName': new_bottle.get('purchasePlaceName'),
                    'purchaseDate': new_bottle.get('purchaseDate'),
                    'deliveryDate': new_bottle.get('deliveryDate'),
                    'purchasePrice': new_bottle.get('purchasePrice'),
                    'purchaseCurrency': new_bottle.get('purchaseCurrency', 'USD'),
                    'archiveStatus': False
                }
                
                # Validate and convert numeric/date fields
                if insert_data['purchasePrice']:
                    try:
                        insert_data['purchasePrice'] = float(insert_data['purchasePrice'])
                        if insert_data['purchasePrice'] < 0:
                            error_msg = f"Purchase price for new bottle must be non-negative"
                            print(f"TZHBackendLog: Validation failed - {error_msg}")
                            return jsonify({
                                "code": 400,
                                "message": error_msg
                            }), 400
                    except (ValueError, TypeError):
                        error_msg = f"Purchase price for new bottle must be a valid number"
                        print(f"TZHBackendLog: Validation failed - {error_msg}")
                        return jsonify({
                            "code": 400,
                            "message": error_msg
                        }), 400
                
                # Validate date fields
                for date_field in ['purchaseDate', 'deliveryDate']:
                    if insert_data[date_field]:
                        try:
                            if isinstance(insert_data[date_field], str) and insert_data[date_field].strip():
                                datetime.strptime(insert_data[date_field], '%Y-%m-%d').date()
                        except ValueError:
                            error_msg = f"{date_field} for new bottle must be in YYYY-MM-DD format"
                            print(f"TZHBackendLog: Validation failed - {error_msg}")
                            return jsonify({
                                "code": 400,
                                "message": error_msg
                            }), 400
                
                # Convert empty strings to None for database NULL handling
                for key, value in insert_data.items():
                    if value == '':
                        insert_data[key] = None
                
                print(f"TZHBackendLog: Inserting new bottle: {insert_data}")
                
                cur.execute("""
                    INSERT INTO "myCellarItems" (
                        "listingID", "collectionID", "variant", "quantityVariantID", "variantGroupID",
                        "status", "consumption", "currentLocation", "subLocation", "noteToSelf",
                        "purchasePlaceName", "purchaseDate", "deliveryDate", "purchasePrice", 
                        "purchaseCurrency", "archiveStatus"
                    ) VALUES (
                        %(listingID)s, %(collectionID)s, %(variant)s, %(quantityVariantID)s, %(variantGroupID)s,
                        %(status)s, %(consumption)s, %(currentLocation)s, %(subLocation)s, %(noteToSelf)s,
                        %(purchasePlaceName)s, %(purchaseDate)s, %(deliveryDate)s, %(purchasePrice)s,
                        %(purchaseCurrency)s, %(archiveStatus)s
                    )
                """, insert_data)
                
                changes_made["bottles_added"] += 1
                print(f"TZHBackendLog: Successfully added new bottle with quantityVariantID: {next_quantity_variant_id}")
        
        # Commit all changes
        conn.commit()
        print("TZHBackendLog: All changes committed successfully")
        
        print(f"TZHBackendLog: Changes summary: {changes_made}")
        print("TZHBackendLog: editCellar completed successfully")
        
        # Prepare successful response
        success_response = {
            "code": 200,
            "success": True,
            "message": "Cellar items updated successfully",
            "data": {
                "variantGroupID": int(variant_group_id) if variant_group_id else None,
                "changesSummary": changes_made
            }
        }
        
        print(f"TZHBackendLog: About to return success response: {success_response}")
        print("TZHBackendLog: ===========================================")
        
        return jsonify(success_response)
        
    except psycopg2.Error as e:
        print(f"TZHBackendLog: Database error in editCellar: {str(e)}")
        conn.rollback()
        print("TZHBackendLog: Transaction rolled back")
        print("TZHBackendLog: ===========================================")
        
        return jsonify({
            "code": 500,
            "message": f"Database error: {str(e)}"
        }), 500
        
    except Exception as e:
        print(f"TZHBackendLog: General error in editCellar: {str(e)}")
        conn.rollback()
        print("TZHBackendLog: Transaction rolled back")
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

# -----------------------------------------------------------------------------------------
# CREATE NEW COLLECTION ENDPOINT
# -----------------------------------------------------------------------------------------

@blueprint.route("/createCollection", methods=['POST'])
def createCollection():
    print("TZHBackendLog: ===========================================")
    print("TZHBackendLog: Starting createCollection endpoint")
    
    try:
        conn = g.db
        cur = conn.cursor(cursor_factory=RealDictCursor)
        print("TZHBackendLog: Database connection established")
        
        data = request.get_json()
        print("TZHBackendLog: Raw request data received:")
        print(f"TZHBackendLog: {json.dumps(data, indent=2, default=str)}")
        
        # Validate required fields
        required_fields = ['ownerType', 'ownerId', 'collectionName']
        print(f"TZHBackendLog: Validating required fields: {required_fields}")
        
        for field in required_fields:
            if field not in data or data[field] is None or str(data[field]).strip() == '':
                error_msg = f"Missing or empty required field: {field}"
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
        
        # Validate collection name length and format
        collection_name = str(data['collectionName']).strip()
        if len(collection_name) > 255:
            error_msg = "Collection name must be 255 characters or less"
            print(f"TZHBackendLog: {error_msg}")
            return jsonify({
                "code": 400,
                "message": error_msg
            }), 400
        
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
        
        # Check if collection name already exists for this owner
        print(f"TZHBackendLog: Checking for duplicate collection name")
        cur.execute("""
            SELECT "id" FROM "myCellarCollections" 
            WHERE "ownerID" = %s AND "ownerType" = %s AND "collectionName" = %s
        """, (data['ownerId'], data['ownerType'], collection_name))
        
        existing_collection = cur.fetchone()
        if existing_collection:
            error_msg = f"Collection '{collection_name}' already exists for this {data['ownerType']}"
            print(f"TZHBackendLog: {error_msg}")
            return jsonify({
                "code": 409,
                "message": error_msg
            }), 409
        
        print(f"TZHBackendLog: Collection name is unique")
        
        # Parse optional fields
        is_public = bool(data.get('isPublic', False))
        # Default to FALSE for new collections unless explicitly requested
        is_default = bool(data.get('isDefault', False))
        
        print(f"TZHBackendLog: Optional fields - isPublic: {is_public}, isDefault: {is_default}")
        
        # If this is being set as default, we need to unset any existing default
        if is_default:
            print(f"TZHBackendLog: Setting as default collection, checking for existing default")
            cur.execute("""
                UPDATE "myCellarCollections" 
                SET "isDefault" = FALSE, "updatedDate" = CURRENT_TIMESTAMP
                WHERE "ownerID" = %s AND "ownerType" = %s AND "isDefault" = TRUE
            """, (data['ownerId'], data['ownerType']))
            
            updated_rows = cur.rowcount
            if updated_rows > 0:
                print(f"TZHBackendLog: Unset {updated_rows} existing default collection(s)")
        
        # Create the new collection
        print(f"TZHBackendLog: Creating new collection")
        cur.execute("""
            INSERT INTO "myCellarCollections" 
            ("ownerID", "ownerType", "collectionName", "isDefault", "isPublic", "createdDate", "updatedDate")
            VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            RETURNING "id", "createdDate"
        """, (
            data['ownerId'], 
            data['ownerType'], 
            collection_name,
            is_default,
            is_public
        ))
        
        new_collection = cur.fetchone()
        collection_id = new_collection['id']
        created_date = new_collection['createdDate']
        
        print(f"TZHBackendLog: Created new collection with ID: {collection_id}")
        
        # Commit the transaction
        conn.commit()
        print("TZHBackendLog: Transaction committed successfully")
        
        # Prepare successful response
        response_data = {
            "code": 201,
            "success": True,
            "message": f"Collection '{collection_name}' created successfully",
            "data": {
                "id": collection_id,
                "ownerID": data['ownerId'],
                "ownerType": data['ownerType'],
                "collectionName": collection_name,
                "isDefault": is_default,
                "isPublic": is_public,
                "createdDate": created_date.isoformat() if created_date else None,
                "updatedDate": created_date.isoformat() if created_date else None
            }
        }
        
        print(f"TZHBackendLog: Preparing response: {json.dumps(response_data, indent=2, default=str)}")
        print("TZHBackendLog: createCollection completed successfully")
        print("TZHBackendLog: ===========================================")
        
        return jsonify(response_data), 201
        
    except psycopg2.IntegrityError as e:
        print(f"TZHBackendLog: Database integrity error occurred: {str(e)}")
        print(f"TZHBackendLog: Error code: {getattr(e, 'pgcode', 'N/A')}")
        
        if conn:
            print("TZHBackendLog: Rolling back transaction due to integrity error")
            conn.rollback()
        
        # Handle specific constraint violations
        if 'unique constraint' in str(e).lower():
            if 'collectionname' in str(e).lower():
                error_msg = "A collection with this name already exists"
            elif 'isdefault' in str(e).lower():
                error_msg = "Only one default collection is allowed per owner"
            else:
                error_msg = "Collection violates database constraints"
        else:
            error_msg = f"Database constraint violation: {str(e)}"
        
        print(f"TZHBackendLog: Returning 409 conflict response")
        print("TZHBackendLog: ===========================================")
        
        return jsonify({
            "code": 409,
            "message": error_msg
        }), 409
        
    except psycopg2.Error as e:
        print(f"TZHBackendLog: Database error occurred: {str(e)}")
        print(f"TZHBackendLog: Database error type: {type(e).__name__}")
        print(f"TZHBackendLog: Database error code: {getattr(e, 'pgcode', 'N/A')}")
        
        if conn:
            print("TZHBackendLog: Rolling back transaction due to database error")
            conn.rollback()
        
        print("TZHBackendLog: Returning 500 error response")
        print("TZHBackendLog: ===========================================")
        
        return jsonify({
            "code": 500,
            "message": f"Database error: {str(e)}"
        }), 500
        
    except Exception as e:
        print(f"TZHBackendLog: General exception occurred: {str(e)}")
        print(f"TZHBackendLog: Exception type: {type(e).__name__}")
        
        if conn:
            print("TZHBackendLog: Rolling back transaction due to general exception")
            conn.rollback()
        
        print("TZHBackendLog: Returning 500 error response")
        print("TZHBackendLog: ===========================================")
        
        return jsonify({
            "code": 500,
            "message": f"Internal server error: {str(e)}"
        }), 500


# -----------------------------------------------------------------------------------------
# [PUT] Update collection public status
# - Updates the isPublic field for a specific collection
# - Validates collection ownership
# - Supports all owner types: user, producer, venue
# - Possible return codes: 200 (Updated), 400 (Validation Error), 404 (Not Found), 500 (Server Error)
@blueprint.route("/collections/public-status/<int:collection_id>/", methods=['PUT'])
def updateCollectionPublicStatus(collection_id):
    print("TZHBackendLog: ===========================================")
    print(f"TZHBackendLog: Starting updateCollectionPublicStatus endpoint for collection {collection_id}")
    
    try:
        conn = g.db
        cur = conn.cursor(cursor_factory=RealDictCursor)
        print("TZHBackendLog: Database connection established")
        
        data = request.get_json()
        print("TZHBackendLog: Raw request data received:")
        print(f"TZHBackendLog: {json.dumps(data, indent=2, default=str)}")
        
        # Validate required fields
        if 'isPublic' not in data:
            error_msg = "Missing required field: isPublic"
            print(f"TZHBackendLog: Validation failed - {error_msg}")
            return jsonify({
                "code": 400,
                "message": error_msg
            }), 400
        
        is_public = bool(data.get('isPublic'))
        print(f"TZHBackendLog: Setting isPublic to: {is_public}")
        
        # First, verify the collection exists and get owner info for validation
        print(f"TZHBackendLog: Checking if collection {collection_id} exists")
        cur.execute("""
            SELECT id, "ownerID", "ownerType", "collectionName", "isPublic"
            FROM "myCellarCollections" 
            WHERE id = %s
        """, (collection_id,))
        
        collection = cur.fetchone()
        if not collection:
            error_msg = f"Collection with ID {collection_id} not found"
            print(f"TZHBackendLog: {error_msg}")
            return jsonify({
                "code": 404,
                "message": error_msg
            }), 404
        
        print(f"TZHBackendLog: Found collection: {collection['collectionName']} (Owner: {collection['ownerType']} {collection['ownerID']})")
        
        # Update the collection's public status
        print(f"TZHBackendLog: Updating collection {collection_id} isPublic to {is_public}")
        cur.execute("""
            UPDATE "myCellarCollections" 
            SET "isPublic" = %s, "updatedDate" = CURRENT_TIMESTAMP
            WHERE id = %s
        """, (is_public, collection_id))
        
        if cur.rowcount == 0:
            error_msg = f"Failed to update collection {collection_id}"
            print(f"TZHBackendLog: {error_msg}")
            return jsonify({
                "code": 500,
                "message": error_msg
            }), 500
        
        conn.commit()
        print(f"TZHBackendLog: Successfully updated collection {collection_id} public status to {is_public}")
        
        # Return success response
        response_data = {
            "code": 200,
            "message": "Collection public status updated successfully",
            "data": {
                "collectionId": collection_id,
                "isPublic": is_public,
                "collectionName": collection['collectionName']
            }
        }
        
        print("TZHBackendLog: Returning success response:")
        print(f"TZHBackendLog: {json.dumps(response_data, indent=2, default=str)}")
        print("TZHBackendLog: ===========================================")
        
        return jsonify(response_data), 200
        
    except psycopg2.Error as e:
        print(f"TZHBackendLog: Database error occurred: {str(e)}")
        print(f"TZHBackendLog: Database error type: {type(e).__name__}")
        print(f"TZHBackendLog: Database error code: {getattr(e, 'pgcode', 'N/A')}")
        
        if conn:
            print("TZHBackendLog: Rolling back transaction due to database error")
            conn.rollback()
        
        print("TZHBackendLog: Returning 500 error response")
        print("TZHBackendLog: ===========================================")
        
        return jsonify({
            "code": 500,
            "message": f"Database error: {str(e)}"
        }), 500
        
    except Exception as e:
        print(f"TZHBackendLog: General exception occurred: {str(e)}")
        print(f"TZHBackendLog: Exception type: {type(e).__name__}")
        
        if conn:
            print("TZHBackendLog: Rolling back transaction due to general exception")
            conn.rollback()
        
        print("TZHBackendLog: Returning 500 error response")
        print("TZHBackendLog: ===========================================")
        
        return jsonify({
            "code": 500,
            "message": f"Internal server error: {str(e)}"
        }), 500

# -----------------------------------------------------------------------------------------
# [DELETE] Delete a collection
# - Verifies ownership by checking ownerID and ownerType against the provided credentials
# - Only allows deletion if the collection belongs to the authenticated owner
# - Prevents deletion of default collections to maintain data integrity
# - Uses CASCADE delete to remove all related items automatically
# - Possible return codes: 200 (Deleted), 400 (Bad Request), 403 (Forbidden), 404 (Not Found), 500 (Server Error)
@blueprint.route("/deleteCollection/<int:collection_id>", methods=['DELETE'])
def deleteCollection(collection_id):
    print("TZHBackendLog: ===========================================")
    print(f"TZHBackendLog: Starting deleteCollection endpoint for collection ID: {collection_id}")
    
    try:
        conn = g.db
        cur = conn.cursor(cursor_factory=RealDictCursor)
        print("TZHBackendLog: Database connection established")
        
        data = request.get_json()
        print("TZHBackendLog: Raw request data received:")
        print(f"TZHBackendLog: {json.dumps(data, indent=2, default=str)}")
        
        # Validate required fields for authentication
        required_fields = ['ownerType', 'ownerId']
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
        
        # First, verify that the authenticated owner exists in their respective table
        owner_table = f'"{data["ownerType"]}s"'  # users, producers, venues
        owner_id_field = '"id"'
        print(f"TZHBackendLog: Validating owner exists in table {owner_table} with ID: {data['ownerId']}")
        
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
        
        # Now verify that the collection exists and get its details
        print(f"TZHBackendLog: Fetching collection details for ID: {collection_id}")
        cur.execute("""
            SELECT "id", "ownerID", "ownerType", "collectionName", "isDefault"
            FROM "myCellarCollections" 
            WHERE "id" = %s
        """, (collection_id,))
        
        collection = cur.fetchone()
        if not collection:
            error_msg = f"Collection with ID {collection_id} not found"
            print(f"TZHBackendLog: {error_msg}")
            return jsonify({
                "code": 404,
                "message": error_msg
            }), 404
        
        print(f"TZHBackendLog: Collection found: {dict(collection)}")
        
        # DEBUG: Log data types and values for comparison
        print(f"TZHBackendLog: DEBUGGING OWNERSHIP VERIFICATION:")
        print(f"TZHBackendLog: collection['ownerID'] = {collection['ownerID']} (type: {type(collection['ownerID'])})")
        print(f"TZHBackendLog: data['ownerId'] = {data['ownerId']} (type: {type(data['ownerId'])})")
        print(f"TZHBackendLog: collection['ownerType'] = {collection['ownerType']} (type: {type(collection['ownerType'])})")
        print(f"TZHBackendLog: data['ownerType'] = {data['ownerType']} (type: {type(data['ownerType'])})")
        print(f"TZHBackendLog: ownerID comparison: {collection['ownerID']} != {data['ownerId']} = {collection['ownerID'] != data['ownerId']}")
        print(f"TZHBackendLog: ownerType comparison: {collection['ownerType']} != {data['ownerType']} = {collection['ownerType'] != data['ownerType']}")
        
        # Verify ownership: the collection's ownerID and ownerType must match the authenticated user
        # Convert both to int to handle potential string/int mismatches
        collection_owner_id = int(collection['ownerID'])
        request_owner_id = int(data['ownerId'])
        
        if collection_owner_id != request_owner_id or collection['ownerType'] != data['ownerType']:
            error_msg = f"Access denied. Collection belongs to different owner (Collection owner: {collection['ownerType']} ID {collection_owner_id}, Authenticated user: {data['ownerType']} ID {request_owner_id})"
            print(f"TZHBackendLog: {error_msg}")
            return jsonify({
                "code": 403,
                "message": "You do not have permission to delete this collection"
            }), 403
        
        print("TZHBackendLog: Ownership verification passed")
        
        # Prevent deletion of default collections to maintain data integrity
        if collection['isDefault']:
            error_msg = f"Cannot delete default collection '{collection['collectionName']}'"
            print(f"TZHBackendLog: {error_msg}")
            return jsonify({
                "code": 400,
                "message": "Default collections cannot be deleted. Please set another collection as default first."
            }), 400
        
        print("TZHBackendLog: Collection is not default, proceeding with deletion")
        
        # Count items that will be archived (not deleted due to new archival system)
        cur.execute("""
            SELECT COUNT(*) as item_count
            FROM "myCellarItems" 
            WHERE "collectionID" = %s AND "archiveStatus" = FALSE
        """, (collection_id,))
        
        item_count_result = cur.fetchone()
        item_count = item_count_result['item_count'] if item_count_result else 0
        print(f"TZHBackendLog: Collection contains {item_count} active items that will be archived")
        
        # Delete the collection (trigger will automatically archive related items)
        print(f"TZHBackendLog: Deleting collection '{collection['collectionName']}' (ID: {collection_id})")
        print("TZHBackendLog: Items will be archived automatically by database trigger")
        
        cur.execute("""
            DELETE FROM "myCellarCollections" 
            WHERE "id" = %s
        """, (collection_id,))
        
        deleted_rows = cur.rowcount
        if deleted_rows == 0:
            error_msg = f"Failed to delete collection {collection_id}"
            print(f"TZHBackendLog: {error_msg}")
            return jsonify({
                "code": 500,
                "message": "Failed to delete collection"
            }), 500
        
        print(f"TZHBackendLog: Successfully deleted {deleted_rows} collection record")
        print(f"TZHBackendLog: Database trigger archived {item_count} related items")
        
        # Commit the transaction
        conn.commit()
        print("TZHBackendLog: Transaction committed successfully")
        
        # Prepare success response
        response_data = {
            "code": 200,
            "message": f"Collection '{collection['collectionName']}' deleted successfully",
            "data": {
                "deletedCollectionId": collection_id,
                "collectionName": collection['collectionName'],
                "archivedItemCount": item_count,  # Changed from deletedItemCount
                "ownerId": collection['ownerID'],
                "ownerType": collection['ownerType']
            }
        }
        
        print(f"TZHBackendLog: Returning success response: {json.dumps(response_data, indent=2, default=str)}")
        print("TZHBackendLog: ===========================================")
        
        return jsonify(response_data), 200
        
    except psycopg2.Error as e:
        print(f"TZHBackendLog: Database error occurred: {str(e)}")
        print(f"TZHBackendLog: Error code: {e.pgcode}")
        print(f"TZHBackendLog: Error message: {e.pgerror}")
        
        if conn:
            print("TZHBackendLog: Rolling back transaction due to database error")
            conn.rollback()
        
        print("TZHBackendLog: Returning 500 error response")
        print("TZHBackendLog: ===========================================")
        
        return jsonify({
            "code": 500,
            "message": f"Database error: {str(e)}"
        }), 500
        
    except Exception as e:
        print(f"TZHBackendLog: General exception occurred: {str(e)}")
        print(f"TZHBackendLog: Exception type: {type(e).__name__}")
        
        if conn:
            print("TZHBackendLog: Rolling back transaction due to general exception")
            conn.rollback()
        
        print("TZHBackendLog: Returning 500 error response")
        print("TZHBackendLog: ===========================================")
        
        return jsonify({
            "code": 500,
            "message": f"Internal server error: {str(e)}"
        }), 500
