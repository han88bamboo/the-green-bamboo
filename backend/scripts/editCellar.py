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
# - Handles automatic collection creation if owner has no collections
# - Supports all owner types: user, producer, venue
# - Validates all input data and handles currency conversion
# - Possible return codes: 201 (Created), 400 (Validation Error), 404 (Not Found), 500 (Server Error)
@blueprint.route("/addToCellar", methods=['POST'])
def addToCellar():
    try:
        conn = g.db
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['listingId', 'ownerType', 'ownerId', 'quantity']
        for field in required_fields:
            if field not in data or data[field] is None:
                return jsonify({
                    "code": 400,
                    "message": f"Missing required field: {field}"
                }), 400
        
        # Validate owner type
        if data['ownerType'] not in ['user', 'producer', 'venue']:
            return jsonify({
                "code": 400,
                "message": "Invalid ownerType. Must be 'user', 'producer', or 'venue'."
            }), 400
        
        # Validate quantity
        try:
            quantity = int(data['quantity'])
            if quantity < 1:
                raise ValueError("Quantity must be positive")
        except (ValueError, TypeError):
            return jsonify({
                "code": 400,
                "message": "Quantity must be a positive integer"
            }), 400
        
        # Validate listing exists
        cur.execute('SELECT "id", "listingName" FROM "listings" WHERE "id" = %s', (data['listingId'],))
        listing = cur.fetchone()
        if not listing:
            return jsonify({
                "code": 404,
                "message": f"Listing with ID {data['listingId']} not found"
            }), 404
        
        # Validate owner exists
        owner_table = f'"{data["ownerType"]}s"'  # users, producers, venues
        owner_id_field = '"id"'
        
        cur.execute(f'SELECT {owner_id_field} FROM {owner_table} WHERE {owner_id_field} = %s', (data['ownerId'],))
        owner = cur.fetchone()
        if not owner:
            return jsonify({
                "code": 404,
                "message": f"Owner with ID {data['ownerId']} not found in {data['ownerType']}s table"
            }), 404
        
        # Handle collection - get or create default collection
        collection_id = data.get('collectionId')
        if not collection_id:
            # Find or create default collection for this owner
            cur.execute("""
                SELECT "id" FROM "myCellarCollections" 
                WHERE "ownerID" = %s AND "ownerType" = %s AND "isDefault" = TRUE
            """, (data['ownerId'], data['ownerType']))
            
            default_collection = cur.fetchone()
            
            if not default_collection:
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
            else:
                collection_id = default_collection['id']
        else:
            # Validate provided collection belongs to the owner
            cur.execute("""
                SELECT "id" FROM "myCellarCollections" 
                WHERE "id" = %s AND "ownerID" = %s AND "ownerType" = %s
            """, (collection_id, data['ownerId'], data['ownerType']))
            
            if not cur.fetchone():
                return jsonify({
                    "code": 400,
                    "message": "Collection does not belong to the specified owner"
                }), 400
        
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
        
        purchase_date = parse_date(data.get('purchaseDate'))
        delivery_date = parse_date(data.get('deliveryDate'))
        drink_onwards_date = parse_date(data.get('drinkOnwardsDate'))
        drink_by_date = parse_date(data.get('drinkByDate'))
        
        # Parse and validate prices
        def parse_price(price_str):
            if not price_str:
                return None
            try:
                return Decimal(str(price_str))
            except (InvalidOperation, TypeError, ValueError):
                return None
        
        purchase_price = parse_price(data.get('purchasePrice'))
        current_value_estimation = parse_price(data.get('currentValueEstimation'))
        
        # Parse volume - store as user entered (no conversion)
        volume_number = None
        volume_unit = None
        if data.get('volumeNumber'):  # Frontend now sends volumeNumber
            try:
                volume_number = float(data['volumeNumber'])
                volume_unit = data.get('volumeUnit', 'ml')  # Keep original unit
            except (ValueError, TypeError):
                volume_number = None
                volume_unit = None
        
        # Parse variant (vintage)  
        variant = None
        if data.get('variant'):
            try:
                variant = int(data['variant'])
            except (ValueError, TypeError):
                variant = None
        
        # Check if master record already exists for this listing+variant combination
        cur.execute("""
            SELECT "id" FROM "myCellarItems" 
            WHERE "listingID" = %s AND "variant" = %s AND "quantityVariantID" = 1
        """, (data['listingId'], variant))
        
        master_record = cur.fetchone()
        
        if not master_record:
            # Create master record (quantityVariantID = 1) with shared properties
            cur.execute("""
                INSERT INTO "myCellarItems" (
                    "listingID", "collectionID", "variant", "quantityVariantID",
                    "drinkFormat", "volumeNumber", "volumeUnit", "drinkByDate", "drinkOnwardsDate",
                    "currentValueEstimation", "currentValueCurrency", "suggestedFoodPairing",
                    "status", "consumption", "currentLocation", "addedDate", "updatedDate"
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                ) RETURNING "id"
            """, (
                data['listingId'],
                collection_id,
                variant,
                1,  # Master record
                data.get('format', 'Bottle'),
                volume_number,
                volume_unit,
                drink_by_date,
                drink_onwards_date,
                current_value_estimation,
                data.get('currentValueCurrency', 'USD'),
                data.get('suggestedFoodPairing', '').strip() or None,
                'In Possession',  # Default status for master record
                'Unopened',      # Default consumption for master record
                'At Home',       # Default location for master record
                datetime.now(),
                datetime.now()
            ))
            master_id = cur.fetchone()['id']
        else:
            master_id = master_record['id']
            
            # Update master record with new shared properties if provided
            update_fields = []
            update_values = []
            
            if data.get('format'):
                update_fields.append('"drinkFormat" = %s')
                update_values.append(data['format'])
            
            if volume_number is not None:
                update_fields.append('"volumeNumber" = %s')
                update_values.append(volume_number)
                update_fields.append('"volumeUnit" = %s')
                update_values.append(volume_unit)
            
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
                cur.execute(update_query, update_values)
        
        # Get next quantityVariantID for this listing+variant combination
        cur.execute("""
            SELECT MAX("quantityVariantID") as max_variant_id 
            FROM "myCellarItems" 
            WHERE "listingID" = %s AND "variant" = %s
        """, (data['listingId'], variant))
        
        result = cur.fetchone()
        next_variant_id = (result['max_variant_id'] or 0) + 1
        
        # Create individual bottle records
        created_bottle_ids = []
        
        for i in range(quantity):
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
            """, (
                data['listingId'],
                collection_id,
                variant,
                next_variant_id + i,  # Individual bottle ID
                purchase_date,
                delivery_date,
                purchase_price,
                data.get('purchaseCurrency', 'USD'),
                data.get('purchaseVenueId'),  # If provided
                data.get('purchasePlaceName', '').strip() or None,
                data.get('purchaseAddress', '').strip() or None,
                data.get('status', 'In Possession'),
                data.get('consumption', 'Unopened'),
                data.get('storageLocation', 'At Home'),
                data.get('subLocation', '').strip() or None,
                data.get('personalNotes', '').strip() or None,
                False,  # Not archived
                datetime.now(),
                datetime.now()
            ))
            
            bottle_id = cur.fetchone()['id']
            created_bottle_ids.append(bottle_id)
        
        # Commit the transaction
        conn.commit()
        
        return jsonify({
            "code": 201,
            "message": f"Successfully added {quantity} bottle(s) to cellar",
            "data": {
                "masterId": master_id,
                "bottleIds": created_bottle_ids,
                "collectionId": collection_id,
                "listingId": data['listingId'],
                "listingName": listing['listingName'],
                "variant": variant,
                "quantity": quantity,
                "addedDate": datetime.now().isoformat()
            }
        }), 201
        
    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        print(f"Database error in addToCellar: {str(e)}")
        return jsonify({
            "code": 500,
            "message": f"Database error: {str(e)}"
        }), 500
        
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error in addToCellar: {str(e)}")
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
