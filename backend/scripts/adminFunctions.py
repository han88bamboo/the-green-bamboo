# Port: 5052
# Routes: /createObservationTag (POST), /updateObservationTag (PUT), /deleteObservationTag/<id> (DELETE), 
#         /updateFamilyTag (POST), /updateSubTag (PUT), /deleteFamilyTag/<id> (DELETE), 
#         /deleteSubTag/<id> (DELETE), /importListings (POST), /createFamilyTag (POST), /createSubTag (POST), 
#         /importListings (POST), /readCSV (GET), /getProducerMergePreview (POST), /getListingMergePreview (POST), /getVenueMergePreview (POST)
#         /mergeProducers (POST), /mergeListings (POST), /mergeVenues (POST), 
#         /searchDuplicates/<entity_type> (GET), /getEntityById/<entity_type>/<int:entity_id> (GET)
# -----------------------------------------------------------------------------------------

import logging
import os
import csv
import io
import codecs
import unicodedata
import s3Images
import base64
import chardet
from psycopg2.extras import execute_values
from concurrent.futures import ThreadPoolExecutor, as_completed

from psycopg2.extras import RealDictCursor # ADDED BY SMU GROUP 3

# Import the database manager for connection pooling
from app import db_manager

from flask import Blueprint, g, request, jsonify
from datetime import datetime
from urllib.request import urlopen

logger = logging.getLogger(__name__)

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
logger.info(project_root)

# -- ========= "observationTags" =========
# CREATE TABLE "observationTags" (
#     "id" SERIAL PRIMARY KEY,
#     "observationTag" VARCHAR(255)
# );

# -----------------------------------------------------------------------------------------
# [POST] Creates an observation tag
# - Insert entry into the "observationTags" collection. Follows observationTag dataclass requirements.
# - Duplicate review check: If an observationTag with the same observationTag, reject the request
# - Possible return codes: 201 (Created), 400 (Duplicate Detected), 500 (Error during creation)
@blueprint.route("/createObservationTag", methods= ['POST'])
def createObservationTag():
    rawTag = request.get_json()
    rawObservationTag = rawTag['observationTag']

    try:
        with db_manager.get_cursor() as cursor:
            # Check if the observation tag already exists
            cursor.execute('SELECT * FROM "observationTags" WHERE "observationTag" = %s', (rawObservationTag,))
            existingObservationTag = cursor.fetchone()

            if existingObservationTag:
                return jsonify(
                    {
                        "code": 400,
                        "data": {
                            "observationTag": rawObservationTag
                        },
                        "message": "Observation tag already exists."
                    }
                ), 400

            # Insert the new observation tag
            cursor.execute('INSERT INTO "observationTags" ("observationTag") VALUES (%s) RETURNING "id"', (rawObservationTag,))
            newObservationTagId = cursor.fetchone()

        return jsonify(
            {
                "code": 201,
                "data": newObservationTagId
            }
        ), 201

    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": {
                    "observationTag": rawObservationTag
                },
                "message": "An error occurred creating the observation tag."
            }
        ), 500

# -----------------------------------------------------------------------------------------
    
# [PUT] Update observation tag
# - Update observation tag with updated data
# - Possible return codes: 201 (Updated), 400(Observation tag not found), 500 (Error during update)
@blueprint.route('/updateObservationTag', methods=['PUT'])
def updateObservationTag():
    data = request.get_json()

    # Note: Changed transaction behavior - original code had separate commits per update
    # Original: Each UPDATE had its own commit() call
    # New: All operations are in one transaction with auto-commit at the end
    with db_manager.get_cursor() as cursor:
        updates = []
        for elem in data:
            # check psql table for existing observation tag
            cursor.execute('SELECT * FROM "observationTags" WHERE "id" = %s', (elem["id"],))
            existingObservationTag = cursor.fetchone()

            if existingObservationTag == None:
                return jsonify(
                    {   
                        "code": 400,
                        "data": {
                            "id": elem["id"]
                        },
                        "message": "Observation Tag does not exist."
                    }
                ), 400

            update_dict = {"observationTag": elem["observationTag"]}
            updates.append({"id": elem["id"], "update": update_dict})

        try:
            for update in updates:
                cursor.execute('UPDATE "observationTags" SET "observationTag" = %s WHERE "id" = %s', (update["update"]["observationTag"], update["id"]))
                # Removed individual conn.commit() calls - now handled automatically by context manager
            return jsonify(
                {   
                    "code": 201,
                    "data": elem['observationTag']
                }
            ), 201

        except Exception as e:
            print(str(e))
            # Removed conn.rollback() - now handled automatically by context manager
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "data": elem['observationTag']
                    },
                    "message": "An error occurred updating the observation tags."
                }
            ), 500

        # Removed finally block with cur.close() - handled automatically by context manager
# -----------------------------------------------------------------------------------------
# [DELETE] Deletes a observationTag
# - Delete entry with specified id from the "observationTag" collection.
# - Possible return codes: 201 (Deleted), 400 (Review doesn't exist), 500 (Error during deletion)
@blueprint.route("/deleteObservationTag/<id>", methods= ['DELETE'])
def deleteObservationTag(id):
    try:
        with db_manager.get_cursor() as cursor:
            cursor.execute('SELECT * FROM "observationTags" WHERE "id" = %s', (id,))
            existingObservation = cursor.fetchone()

            if existingObservation == None:
                return jsonify(
                    {   
                        "code": 400,
                        "data": {
                            "id": id
                        },
                        "message": "Observation tag doesn't exist."
                    }
                ), 400

            cursor.execute('DELETE FROM "observationTags" WHERE "id" = %s', (id,))
            # Auto-commit handled by context manager
            
            return jsonify( 
                {   
                    "code": 200,
                    "data": id
                }
            ), 201

    except Exception as e:
        print(str(e))
        # Auto-rollback handled by context manager
        return jsonify(
            {
                "code": 500,
                "data": {
                    "id": id
                },
                "message": "An error occurred deleting the observation."
            }
        ), 500

# -----------------------------------------------------------------------------------------
    
# [PUT] Update family tag
# - Update flavour tag with updated family tag data
# - Possible return codes: 201 (Updated), 400(Flavour tag not found), 500 (Error during update)
@blueprint.route('/updateFamilyTag', methods=['PUT'])
def updateFamilyTag():
    data = request.get_json()

    updates = []
    try:
        with db_manager.get_cursor() as cursor:
            for elem in data:
                cursor.execute('SELECT id FROM "flavourTags" WHERE id = %s', (elem["id"],))
                existingFamilyTag = cursor.fetchone()

                if existingFamilyTag is None:
                    return jsonify(
                        {   
                            "code": 400,
                            "data": {
                                "familyTag": elem['familyTag']
                            },
                            "message": "Family Tag does not exist."
                        }
                    ), 400

                cursor.execute("""
                    UPDATE "flavourTags" SET "familyTag" = %s, "hexcode" = %s WHERE "id" = %s
                """, (elem["familyTag"], elem["hexcode"], elem["id"]))
                # note TRANSACTION BEHAVIOR CHANGE: Original had individual conn.commit() per update
                # New: All updates will be committed together at the end of the context manager

                updates.append({"id": elem["id"], "familyTag": elem["familyTag"], "hexcode": elem["hexcode"]})

        return jsonify(
            {
                "code": 201,
                "data": updates
            }
        ), 201

    except Exception as e:
        print(str(e))
        # CHANGE: Removed conn.rollback() - now handled automatically by context manager
        return jsonify(
            {
                "code": 500,
                "data": {
                    "familyTag": elem["familyTag"]
                },
                "message": "An error occurred updating the family tag."
            }
        ), 500

    # CHANGE: Removed finally block with cur.close() - handled automatically by context manager
            
    
# -----------------------------------------------------------------------------------------
    
# [PUT] Update sub tag
# - Update subtag with udpated subtag info
# - Possible return codes: 201 (Updated), 400(Sub tag not found), 500 (Error during update)
@blueprint.route('/updateSubTag', methods=['PUT'])
def updateSubTag():
    data = request.get_json()

    updates = []
    try:
        with db_manager.get_cursor() as cursor:
            for elem in data:
                # Check if the sub tag exists
                cursor.execute('SELECT id FROM "subTags" WHERE "id" = %s', (elem["id"],))
                existingSubTag = cursor.fetchone()

                if existingSubTag == None:
                    return jsonify(
                        {
                            "code": 400,
                            "data": {
                                "id": elem["id"]
                            },
                            "message": "Sub tag does not exist."
                        }
                    ), 400

                cursor.execute("""
                    UPDATE "subTags" SET "subTag" = %s WHERE "id" = %s
                """, (elem["subTag"], elem["id"]))

                updates.append({"id": elem["id"], "subTag": elem["subTag"]})

        return jsonify(
            {
                "code": 201,
                "data": updates
            }
        ), 201

    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": {
                    "subTag": elem["subTag"]
                },
                "message": "An error occurred updating the sub tag."
            }
        ), 500
    
# -----------------------------------------------------------------------------------------
    
# [DELETE] Deletes a familyTag
# - Delete entry with specified id from the "flavourTags" collection.
# - Possible return codes: 201 (Deleted), 400 (family tag doesn't exist), 500 (Error during deletion)
@blueprint.route("/deleteFamilyTag/<id>", methods= ['DELETE'])
def deleteFamilyTag(id):
    try:
        with db_manager.get_cursor() as cursor:
            cursor.execute('SELECT id FROM "flavourTags" WHERE "id" = %s', (id,))
            existingFamilyTag = cursor.fetchone()

            if existingFamilyTag == None:
                return jsonify(
                    {
                        "code": 400,
                        "data": {
                            "id": id
                        },
                        "message": "Family tag doesn't exist."
                    }
                ), 400

            cursor.execute('DELETE FROM "subTags" WHERE "familyTagId" = %s', (id,))
            cursor.execute('DELETE FROM "flavourTags" WHERE "id" = %s', (id,))
            # Auto-commit handled by context manager

        return jsonify(
            {
                "code": 201,
                "data": id
            }
        ), 201

    except Exception as e:
        print(str(e))
        # Auto-rollback handled by context manager
        return jsonify(
            {
                "code": 500,
                "data": {
                    "id": id
                },
                "message": "An error occurred deleting the family tag."
            }
        ), 500

# -----------------------------------------------------------------------------------------    
    
# [DELETE] Deletes a flavour subTag
# - Delete entry with specified id from the "subTags" collection.
# - Possible return codes: 201 (Deleted), 400 (Subtag doesn't exist), 500 (Error during deletion)
@blueprint.route("/deleteSubTag/<id>", methods= ['DELETE'])
def deleteSubTag(id):
    try:
        with db_manager.get_cursor() as cursor:
            # Check if the sub tag exists
            cursor.execute('SELECT id FROM "subTags" WHERE "id" = %s', (id,))
            existingSubTag = cursor.fetchone()

            if existingSubTag == None:
                return jsonify(
                    {
                        "code": 400,
                        "data": {
                            "id": id
                        },
                        "message": "Sub tag doesn't exist."
                    }
                ), 400

            cursor.execute('DELETE FROM "subTags" WHERE "id" = %s', (id,))

            return jsonify(
                {
                    "code": 201,
                    "data": id
                }
            ), 201

    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": {
                    "id": id
                },
                "message": "An error occurred deleting the sub tag."
            }
        ), 500
    
# -----------------------------------------------------------------------------------------
# [POST] Creates a flavour family tag
# - Insert entry into the "familyTags" collection. Follows flavourTag dataclass requirements.
# - Duplicate review check: If a flavourTag with the same flavourTag, reject the request
# - Possible return codes: 201 (Created), 400 (Duplicate Detected), 500 (Error during creation)
@blueprint.route("/createFamilyTag", methods= ['POST'])
def createFamilyTag():
    rawTag = request.get_json()
    rawFamily= rawTag['familyTag']

    try:
        with db_manager.get_cursor() as cursor:
            # Duplicate listing check: Reject if a subTag with the same name exists in the database
            cursor.execute('SELECT id FROM "flavourTags" WHERE "familyTag" = %s', (rawFamily,))
            existingTag = cursor.fetchone()

            if existingTag is not None:
                return jsonify(
                    {
                        "code": 400,
                        "data": {
                            "familyTag": rawFamily
                        },
                        "message": "Family tag already exists."
                    }
                ), 400

            # Insert the new family tag
            cursor.execute("""
                INSERT INTO "flavourTags" ("familyTag", "hexcode") VALUES (%s, %s) RETURNING "id"
            """, (rawFamily, rawTag['hexcode']))
            newFamilyTagId = cursor.fetchone()

        return jsonify(
            {
                "code": 201,
                "data": newFamilyTagId
            }
        ), 201

    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": {
                    "familyTag": rawFamily
                },
                "message": "An error occurred creating the family tag."
            }
        ), 500
# -----------------------------------------------------------------------------------------
# [POST] Creates a flavour sub tag
# - Insert entry into the "subTags" collection. Follows subTag dataclass requirements.
# - Duplicate review check: If a subTag with the same subTag, reject the request
# - Possible return codes: 201 (Created), 400 (Duplicate Detected), 500 (Error during creation)
@blueprint.route("/createSubTag", methods= ['POST'])
def createSubTag():
    rawTag = request.get_json()
    rawSub= rawTag['subTag']

    # Duplicate listing check: Reject if review with the same observation exists in the database
    try:
        with db_manager.get_cursor() as cursor:
            cursor.execute('SELECT id FROM "subTags" WHERE "subTag" = %s', (rawSub,))
            existingTag = cursor.fetchone()

            if existingTag:
                return jsonify(
                    {
                        "code": 400,
                        "data": {
                            "subTag": rawSub
                        },
                        "message": "Sub tag already exists."
                    }
                ), 400

            # Insert the new sub tag
            cursor.execute("""
                INSERT INTO "subTags" ("familyTagId", "subTag") VALUES (%s, %s) RETURNING "id"
            """, (rawTag['familyTagId'], rawSub))
            newSubTagId = cursor.fetchone()

        return jsonify(
            {
                "code": 201,
                "data": newSubTagId
            }
        ), 201

    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": {
                    "subTag": rawSub
                },
                "message": "An error occurred creating the sub tag."
            }
        ), 500
# -----------------------------------------------------------------------------------------
    
# To convert image URL to base64    
def image_url_to_base64(url):
    try:
        # Fetch the image from the URL
        with urlopen(url) as response:
            # Read the image data
            image_data = response.read()
            # Convert the image data to base64
            base64_str = base64.b64encode(image_data).decode('utf-8')
            return base64_str
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
# -----------------------------------------------------------------------------------------

# To hash the password
def hash_password(id, password):
    combinedString = str(id) + password
    hash = 0

    for i in range(len(combinedString)):
        char = ord(combinedString[i])
        hash = (hash << 5) - hash + char
        hash &= 0xFFFFFFFF  # Convert to 32-bit integer

    if hash & (1 << 31):  # If the highest bit is set
        hash -= 1 << 32  # Convert to a signed integer

    return hash

# -----------------------------------------------------------------------------------------

# [POST] Import listings
# - Bulk import listings
# - Possible return codes: 201 (Updated), 400(Observation tag not found), 500 (Error during update)
@blueprint.route('/importListings', methods=['POST'])
def importListings():
    try:
        with db_manager.get_cursor() as cursor:
            file = request.files['file']

            # Detect encoding of CSV file
            file_encoding = detect_encoding(file)

            # Define column data types
            column_data_types = [str, str, str, str, str, str, str, str, float, str, str, str, str]

            # Read all rows from CSV
            with io.TextIOWrapper(file, encoding=file_encoding, errors='replace') as csv_file:
                csv_data = csv.reader(csv_file)
                for _ in range(4):  # Skip header rows
                    next(csv_data)
                
                rows = list(csv_data)

            # Fetch existing producers
            cursor.execute('SELECT "producerName", "id", "isIndependentBottler" FROM "producers"')
            producers = cursor.fetchall()
            producer_name_id_dict = {row['producerName']: row['id'] for row in producers}
            
            csv_producers = set(row[1] for row in rows if row[1])
            
            # Collect bottler names from CSV (column 2) that are not "OB" or "Original Bottling"
            csv_bottlers = set(row[2] for row in rows if row[2] and row[2] not in ["OB", "Original Bottling"])
            
            # Determine new producers to insert
            new_producers = csv_producers - set(producer_name_id_dict.keys())
            
            # Determine new bottlers to insert (excluding any already in producers table)
            new_bottlers = csv_bottlers - set(producer_name_id_dict.keys())
            
            # Prepare data for new producers
            new_producer_data = [
                {
                    "producerName": name,
                    "producerDesc": "",
                    "originCountry": "",
                    "mainDrinks": [],
                    "photo": "",
                    "hashedPassword": hash_password(name, "admin1234"),
                    "claimStatus": False,
                    "statusOB": "",
                    "username": None,
                    "producerLink": "",
                    "stripeCustomerId": None,
                    "claimStatusCheckDate": None,
                    "isIndependentBottler": False
                }
                for name in new_producers
            ]
            
            # Prepare data for new bottlers (mark them as independent bottlers)
            new_bottler_data = [
                {
                    "producerName": name,
                    "producerDesc": "",
                    "originCountry": "",
                    "mainDrinks": [],
                    "photo": "",
                    "hashedPassword": hash_password(name, "admin1234"),
                    "claimStatus": False,
                    "statusOB": "",
                    "username": None,
                    "producerLink": "",
                    "stripeCustomerId": None,
                    "claimStatusCheckDate": None,
                    "isIndependentBottler": True
                }
                for name in new_bottlers
            ]
            
            # Combine new producers and bottlers for bulk insert
            all_new_profiles = new_producer_data + new_bottler_data

            # Bulk insert new producers and bottlers and fetch their IDs
            if all_new_profiles:
                insert_query = """
                    INSERT INTO producers (
                        "producerName", "producerDesc", "originCountry", "mainDrinks", "photo", "hashedPassword",
                        "claimStatus", "statusOB", "username", "producerLink", "stripeCustomerId", "claimStatusCheckDate",
                        "isIndependentBottler"
                    ) VALUES %s RETURNING "producerName", "id"
                """
                execute_values(cursor, insert_query, [
                    (
                        profile["producerName"], profile["producerDesc"], profile["originCountry"],
                        profile["mainDrinks"], profile["photo"], profile["hashedPassword"],
                        profile["claimStatus"], profile["statusOB"], profile["username"],
                        profile["producerLink"], profile["stripeCustomerId"], profile["claimStatusCheckDate"],
                        profile["isIndependentBottler"]
                    )
                    for profile in all_new_profiles
                ])
                new_profiles_with_ids = cursor.fetchall()
                producer_name_id_dict.update({row["producerName"]: row["id"] for row in new_profiles_with_ids})

            # # Fetch existing listings to avoid duplicates - TZH commented out because this duplicate detection system is faulty
            # cursor.execute('SELECT "listingName", "producerID" FROM "listings"')
            # existing_listings = {(row['listingName'], row['producerID']) for row in cursor.fetchall()}

            listings_to_insert = []
            image_urls = []

            for row in rows:
                if len(row) < len(column_data_types):
                    print(f"Skipping row with missing columns: {row}")
                    continue
                
                converted_row = []
                for i, (data_type, value) in enumerate(zip(column_data_types, row)):
                    if data_type is float:
                        value = value.replace('%', '').strip()
                        try:
                            # Handle 'NAS', 'N/A', empty strings or any other non-numeric values
                            if value and value.lower() not in ['n/a', 'na', 'nas']:
                                converted_value = float(value)
                            else:
                                converted_value = None
                        except ValueError:
                            # If conversion fails, set to None and log the error
                            print(f"Could not convert value '{value}' to float in column {i}. Setting to None.")
                            converted_value = None
                    else:
                        converted_value = data_type(value) if value else None
                    converted_row.append(converted_value)

                producer_name = converted_row[1]
                producer_id = producer_name_id_dict.get(producer_name)
                listing_name = converted_row[0]

                # tzh commented out the duplicate detection system because it was faulty
                # if (listing_name, producer_id) in existing_listings:
                #     print(f"Skipping duplicate listing: {listing_name} from {producer_name}")
                #     image_urls.append(None)  # Add None to maintain alignment with listings
                #     continue

                # Handle bottler scenarios
                bottler_name = converted_row[2]
                
                # Scenario A: Bottler is "OB" or "Original Bottling"
                if bottler_name in ["OB", "Original Bottling"]:
                    bottler_id = None
                    bottler_name = "OB"
                # Scenario B: Any other bottler
                else:
                    # Get the bottler ID from the producers dictionary (it will be there now 
                    # whether it was pre-existing or newly created)
                    bottler_id = producer_name_id_dict.get(bottler_name) if bottler_name else None

                image_urls.append(converted_row[12])

                listings_to_insert.append({
                    'listingName': converted_row[0],
                    'producerID': producer_id,
                    'bottler': bottler_name,
                    'bottlerID': bottler_id,
                    'originCountry': converted_row[3],
                    'drinkType': converted_row[4],
                    'typeCategory': converted_row[5],
                    'drinkStyle': converted_row[6],
                    'age': converted_row[7],
                    'abv': converted_row[8],
                    'reviewLink': converted_row[9],
                    'officialDesc': converted_row[10],
                    'sourceLink': converted_row[11],
                    'photo': None,
                    'allowMod': True,
                    'addedDate': datetime.now()
                })

            # FIXED: Parallelize S3 image uploads while maintaining order
            def upload_image_with_index(indexed_data):
                index, image_url = indexed_data
                s3_url = s3Images.uploadURLtoS3(image_url) if image_url else None
                return index, s3_url

            # Create indexed data to maintain order
            indexed_image_urls = list(enumerate(image_urls))
            s3_urls = [None] * len(image_urls)

            with ThreadPoolExecutor() as executor:
                # Submit all tasks
                future_to_index = {
                    executor.submit(upload_image_with_index, indexed_data): indexed_data[0] 
                    for indexed_data in indexed_image_urls
                }
                
                # Process completed tasks and maintain order
                for future in as_completed(future_to_index):
                    index, s3_url = future.result()
                    s3_urls[index] = s3_url

            print("S3 URLs:", s3_urls)

            # Update photo URLs in listings
            for listing, s3_url in zip(listings_to_insert, s3_urls):
                listing['photo'] = s3_url

            print(f"Total rows in CSV: {len(rows)}")
            print(f"Total listings prepared for insertion: {len(listings_to_insert)}")
            print(f"Skipped duplicate listings: {len(rows) - len(listings_to_insert)}")

            # Bulk insert listings - now excluding the 'id' column and using RETURNING
            if listings_to_insert:
                # Make sure we're not trying to specify the 'id' field
                for listing in listings_to_insert:
                    if 'id' in listing:
                        del listing['id']
                
                listing_columns = listings_to_insert[0].keys()
                listing_query = "INSERT INTO listings ({}) VALUES %s RETURNING id".format(
                    ', '.join(f'"{col}"' for col in listing_columns)
                )
                listing_values = [tuple(listing.values()) for listing in listings_to_insert]
                execute_values(cursor, listing_query, listing_values)
                inserted_ids = cursor.fetchall()  # Get all returned IDs
                print(f"Inserted IDs: {inserted_ids}")
                
                # Update the sequence to ensure future inserts don't conflict
                cursor.execute("SELECT setval('listings_id_seq', COALESCE((SELECT MAX(id) FROM listings), 1), true)")
                
                print(f"Successfully inserted {len(listings_to_insert)} listings")

            return jsonify({
                "code": 201,
                "message": f"{file.filename} has been fully uploaded!"
            }), 201
    
    except Exception as e:
        print(f"Error in importListings: {str(e)}")
        return jsonify({
            "code": 500,
            "message": f"Error uploading file: {str(e)}"
        }), 500


    # # for loop for each observation tag and update
    # updates = []
    # for elem in data:

    #     existingObservationTag = db.observationTags.find_one({'_id': ObjectId(elem["_id"]["$oid"])})

    #     if(existingObservationTag == None):
    #         return jsonify(
    #             {   
    #                 "code": 400,
    #                 "data": {
    #                     "observationTag": elem['observationTag']
    #                 },
    #                 "message": "Observation Tag does not exist."
    #             }
    #         ), 400

    #     tag_key, tag_value = list(elem.items())[1]
    #     tag_dict = {"$set":{tag_key: tag_value}}
    #     updates.append({"filter": {"_id": ObjectId(elem["_id"]["$oid"])}, "update": tag_dict})


    # try: 
    #     for update in updates:
    #         filter_criteria = update["filter"]
    #         update_data = update["update"]
    #         db.observationTags.update_many(filter_criteria, update_data)
    #     return jsonify(
    #         {   
    #             "code": 201,
    #             "data": elem['observationTag']
    #         }
    #     ), 201
    # except Exception as e:
    #     print(str(e))
    #     return jsonify(
    #         {
    #             "code": 500,
    #             "data": {
    #                 "data": elem['observationTag']
    #             },
    #             "message": "An error occurred updating the observation tags."
    #         }
    #     ), 500

# -----------------------------------------------------------------------------------------
@blueprint.route('/readCSV', methods=['GET'])
def readCSV():
    data_path = os.path.join(project_root, "scripts", "listingsFormat.csv")
    logger.info(data_path)

    with codecs.open(data_path, 'r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        data = [row for row in reader]
    return jsonify(
        {
            "code": 201,
            "data": data
        }), 201
# -----------------------------------------------------------------------------------------
# This function is to convert non utf-8 encoded files to utf-8 files
def detect_encoding(file):
    raw_data = file.read()

    # Detect encoding using chardet
    detected_encoding = chardet.detect(raw_data)['encoding']
    print(f">detecting encoding...")

    # # if(detected_encoding== 'ascii' or detected_encoding == 'utf-8'):
    # #     return file

    # if(detected_encoding== 'ascii' or detected_encoding == 'utf-8'):
    #     print(f">detected either ascii or utf-8")
    #     return file

    # Decode the raw data using the detected encoding
    # text = raw_data.decode(detected_encoding)
    # print(f">Decode the raw data using the detected encoding")
    
    # Normalize text (optional step depending on use case)
    # normalized_text = normalize_unicode(text)

    # Create a new in-memory file with UTF-8 encoding
    # output_file = io.BytesIO()
    # output_file.write(normalized_text.encode('utf-8'))
    # output_file.seek(0)  # Reset the pointer to the start of the file
    file.seek(0)  # Reset the pointer to the start of the file
    print("done detecting")
    return detected_encoding
    
# This function is to normalise the data in the rows
# def normalize_unicode(text):
#     return unicodedata.normalize('NFKC', str(text)) if text else text


# [POST] Update system settings
# - Update a system setting value in the database
# - Possible return codes: 200 (Updated), 404 (Setting not found), 500 (Error during update)
@blueprint.route("/updateSystemSetting", methods=['POST'])
def updateSystemSetting():
    try:
        with db_manager.get_cursor() as cursor:
            data = request.get_json()
            setting_name = data.get('settingName')
            setting_value = data.get('settingValue')
            
            if not setting_name or setting_value is None:
                return jsonify({
                    "code": 400,
                    "message": "Missing required fields: settingName and settingValue."
                }), 400
                
            # Update the setting value and timestamp
            cursor.execute(
                'UPDATE "systemSettings" SET "settingValue" = %s, "lastUpdated" = CURRENT_TIMESTAMP WHERE "settingName" = %s',
                (setting_value, setting_name)
            )
            
            if cursor.rowcount == 0:
                return jsonify({
                    "code": 404,
                    "message": f"System setting '{setting_name}' not found."
                }), 404
                
            return jsonify({
                "code": 200,
                "message": "System setting updated successfully."
            })
        
    except Exception as e:
        print(f"Error updating system setting: {str(e)}")
        return jsonify({
            "code": 500,
            "message": f"An error occurred while updating the system setting: {str(e)}"
        }), 500

# ==================== PRODUCERS MERGE ====================

# [POST] Get producer merge preview
# - Get preview data for merging producers
@blueprint.route('/getProducerMergePreview', methods=['POST'])
def get_producer_merge_preview():
    """Get preview data for merging producers"""
    
    try:
        with db_manager.get_cursor() as cursor:
            data = request.get_json()
            master_id = data.get('masterId')
            duplicate_ids = data.get('duplicateIds', [])
            
            if not master_id or not duplicate_ids:
                return jsonify({"code": 400, "message": "Missing required fields"}), 400
            
            # Get all producer records
            all_ids = [master_id] + duplicate_ids
            cursor.execute('''
                SELECT id, "producerName", "producerDesc", "originCountry", 
                       "isIndependentBottler", "yearFounded", "activeStatus",
                       "owner", "location", "website", "claimStatus"
                FROM producers 
                WHERE id = ANY(%s)
                ORDER BY id = %s DESC
            ''', (all_ids, master_id))
            
            producers = []
            rows = cursor.fetchall()
            for row in rows:
                if hasattr(row, 'keys'):  # RealDictRow
                    producers.append({
                        'id': row['id'],
                        'producerName': row['producerName'],
                        'producerDesc': row['producerDesc'],
                        'originCountry': row['originCountry'],
                        'isIndependentBottler': row['isIndependentBottler'],
                        'yearFounded': row['yearFounded'],
                        'activeStatus': row['activeStatus'],
                        'owner': row['owner'],
                        'location': row['location'],
                        'website': row['website'],
                        'claimStatus': row['claimStatus']
                    })
                else:  # Tuple
                    producers.append({
                        'id': row[0],
                        'producerName': row[1],
                        'producerDesc': row[2],
                        'originCountry': row[3],
                        'isIndependentBottler': row[4],
                        'yearFounded': row[5],
                        'activeStatus': row[6],
                        'owner': row[7],
                        'location': row[8],
                        'website': row[9],
                        'claimStatus': row[10]
                    })
            
            # Helper function for safe counts
            def safe_count(query, pid):
                cursor.execute(query, (pid,))
                row = cursor.fetchone()
                if not row:
                    return 0
                # Handle both RealDictRow and tuple
                if hasattr(row, 'keys'):
                    return row['count']
                else:
                    return row[0]
            
            # Get related data counts
            related_counts = {}
            for pid in all_ids:
                counts = {
                    'listings': safe_count('SELECT COUNT(*) FROM listings WHERE "producerID" = %s', pid),
                    'bottlerListings': safe_count('SELECT COUNT(*) FROM listings WHERE "bottlerID" = %s', pid),
                    'reviews': safe_count('SELECT COUNT(*) FROM "producerReviews" WHERE "producerID" = %s', pid),
                    'qa': safe_count('SELECT COUNT(*) FROM "producersQuestionAnswers" WHERE "producerId" = %s', pid),
                    'updates': safe_count('SELECT COUNT(*) FROM "producersUpdates" WHERE "producerId" = %s', pid)
                }
                
                # Special case for followers (different query pattern)
                cursor.execute('''
                    SELECT COUNT(*) FROM "usersFollowLists" 
                    WHERE %s::text = ANY(producers)
                ''', (str(pid),))
                row = cursor.fetchone()
                if hasattr(row, 'keys'):
                    counts['followers'] = row['count']
                else:
                    counts['followers'] = row[0] if row else 0
                
                related_counts[pid] = counts
        
        return jsonify({
            "code": 200,
            "data": {
                "producers": producers,
                "relatedCounts": related_counts,
                "totalAffected": {
                    "listings": sum(c['listings'] for c in related_counts.values()),
                    "bottlerListings": sum(c['bottlerListings'] for c in related_counts.values()),
                    "reviews": sum(c['reviews'] for c in related_counts.values()),
                    "qa": sum(c['qa'] for c in related_counts.values()),
                    "updates": sum(c['updates'] for c in related_counts.values()),
                    "followers": sum(c['followers'] for c in related_counts.values())
                }
            }
        }), 200
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        logger.error(f"Error getting producer merge preview: {str(e)}")
        return jsonify({"code": 500, "message": str(e)}), 500

# [POST] Merge producers
# - Merge duplicate producers into a master producer
@blueprint.route('/mergeProducers', methods=['POST'])
def merge_producers():
    """Merge duplicate producers into a master producer"""
    
    try:
        data = request.get_json()
        master_id = data.get('masterId')
        duplicate_ids = data.get('duplicateIds', [])
        
        if not master_id or not duplicate_ids:
            return jsonify({"code": 400, "message": "Missing required fields"}), 400
        
        with db_manager.get_cursor() as cursor:
            # Update all foreign key references
            for dup_id in duplicate_ids:
                # Update listings where producer
                cursor.execute('''
                    UPDATE listings SET "producerID" = %s 
                    WHERE "producerID" = %s
                ''', (master_id, dup_id))
                
                # Update listings where bottler
                cursor.execute('''
                    UPDATE listings SET "bottlerID" = %s 
                    WHERE "bottlerID" = %s
                ''', (master_id, dup_id))
                
                # Update producer reviews
                cursor.execute('''
                    UPDATE "producerReviews" SET "producerID" = %s 
                    WHERE "producerID" = %s
                ''', (master_id, dup_id))
                
                # Update Q&A
                cursor.execute('''
                    UPDATE "producersQuestionAnswers" SET "producerId" = %s 
                    WHERE "producerId" = %s
                ''', (master_id, dup_id))
                
                # Update producer updates
                cursor.execute('''
                    UPDATE "producersUpdates" SET "producerId" = %s 
                    WHERE "producerId" = %s
                ''', (master_id, dup_id))
                
                # Update opening hours
                cursor.execute('''
                    UPDATE "producersOpeningHours" SET "producerId" = %s 
                    WHERE "producerId" = %s
                ''', (master_id, dup_id))
                
                # Update profile views
                cursor.execute('''
                    UPDATE "producersProfileViews" SET "producerId" = %s 
                    WHERE "producerId" = %s
                ''', (master_id, dup_id))
                
                # Update text sections
                cursor.execute('''
                    UPDATE "producerTextSections" SET "producerId" = %s 
                    WHERE "producerId" = %s
                ''', (master_id, dup_id))
                
                # Update user follow lists (stored as text array)
                cursor.execute('''
                    UPDATE "usersFollowLists" 
                    SET producers = array_replace(producers, %s::text, %s::text)
                    WHERE %s::text = ANY(producers)
                ''', (str(dup_id), str(master_id), str(dup_id)))
                
                # Update user producer list items
                cursor.execute('''
                    UPDATE "userProducerListItems" SET "producerId" = %s 
                    WHERE "producerId" = %s
                ''', (master_id, dup_id))
                
                # Update request listings
                cursor.execute('''
                    UPDATE "requestListings" SET "producerID" = %s 
                    WHERE "producerID" = %s
                ''', (master_id, dup_id))
                
                cursor.execute('''
                    UPDATE "requestListings" SET "bottlerID" = %s 
                    WHERE "bottlerID" = %s
                ''', (master_id, dup_id))
            
            # Delete duplicate producers
            cursor.execute('''
                DELETE FROM producers WHERE id = ANY(%s)
            ''', (duplicate_ids,))
        
        return jsonify({
            "code": 200,
            "message": f"Successfully merged {len(duplicate_ids)} producers into producer ID {master_id}"
        }), 200
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        logger.error(f"Error merging producers: {str(e)}")
        return jsonify({"code": 500, "message": str(e)}), 500


# ==================== LISTING MERGE ====================

# [POST] Get listing merge preview
# - Get preview data for merging listings
@blueprint.route('/getListingMergePreview', methods=['POST'])
def get_listing_merge_preview():
    """Get preview data for merging listings"""
    
    try:
        with db_manager.get_cursor() as cursor:
            data = request.get_json()
            master_id = data.get('masterId')
            duplicate_ids = data.get('duplicateIds', [])
            
            if not master_id or not duplicate_ids:
                return jsonify({"code": 400, "message": "Missing required fields"}), 400
            
            # Collect all IDs to check
            all_ids = [master_id] + duplicate_ids

            # Get all listing records
            cursor.execute('''
                SELECT l.id, l."listingName", p."producerName", l."drinkType", 
                       l."typeCategory", l.abv, l."originCountry", l."officialDesc"
                FROM listings l
                LEFT JOIN producers p ON l."producerID" = p.id
                WHERE l.id = ANY(%s)
                ORDER BY l.id = %s DESC
            ''', (all_ids, master_id))
            
            listings = []
            rows = cursor.fetchall()
            for row in rows:
                if hasattr(row, 'keys'):  # RealDictRow
                    listings.append({
                        'id': row['id'],
                        'listingName': row['listingName'],
                        'producerName': row['producerName'],
                        'drinkType': row['drinkType'],
                        'typeCategory': row['typeCategory'],
                        'abv': row['abv'],
                        'originCountry': row['originCountry'],
                        'officialDesc': row['officialDesc']
                    })
                else:  # Tuple fallback
                    listings.append({
                        'id': row[0],
                        'listingName': row[1],
                        'producerName': row[2],
                        'drinkType': row[3],
                        'typeCategory': row[4],
                        'abv': row[5],
                        'originCountry': row[6],
                        'officialDesc': row[7]
                    })
            
            # Helper function for safe counts
            def safe_count(query, lid):
                cursor.execute(query, (lid,))
                row = cursor.fetchone()
                if not row:
                    return 0
                # Handle both RealDictRow and tuple
                if hasattr(row, 'keys'):
                    return row['count']
                else:
                    return row[0]
            
            # Get related data counts
            related_counts = {}
            for lid in all_ids:
                counts = {
                    'reviews': safe_count('SELECT COUNT(*) FROM reviews WHERE "reviewTarget" = %s', lid),
                    'menuItems': safe_count('SELECT COUNT(*) FROM "menuItems" WHERE "itemID" = %s', lid),
                    'userLists': safe_count('SELECT COUNT(*) FROM "usersDrinkListItems" WHERE "drinkId" = %s', lid),
                    'cellarItems': safe_count('SELECT COUNT(*) FROM "myCellarItems" WHERE "listingID" = %s', lid),
                    'comments': safe_count('SELECT COUNT(*) FROM "listingsComments" WHERE "listingId" = %s', lid),
                    'likes': safe_count('SELECT COUNT(*) FROM "listingsLikes" WHERE "listingId" = %s', lid)
                }
                related_counts[lid] = counts
            
            # Totals across all IDs
            total_affected = {
                "reviews": sum(c['reviews'] for c in related_counts.values()),
                "menuItems": sum(c['menuItems'] for c in related_counts.values()),
                "userLists": sum(c['userLists'] for c in related_counts.values()),
                "cellarItems": sum(c['cellarItems'] for c in related_counts.values()),
                "comments": sum(c['comments'] for c in related_counts.values()),
                "likes": sum(c['likes'] for c in related_counts.values())
            }
            
            return jsonify({
                "code": 200,
                "data": {
                    "listings": listings,
                    "relatedCounts": related_counts,
                    "totalAffected": total_affected
                }
            }), 200
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        logger.error(f"Error getting listing merge preview: {str(e)}")
        return jsonify({"code": 500, "message": str(e)}), 500

# [POST] Merge listings
# - Merge duplicate listings into a master listing
@blueprint.route('/mergeListings', methods=['POST'])
def merge_listings():
    """Merge duplicate listings into a master listing"""
    
    try:
        data = request.get_json()
        master_id = data.get('masterId')
        duplicate_ids = data.get('duplicateIds', [])
        
        if not master_id or not duplicate_ids:
            return jsonify({"code": 400, "message": "Missing required fields"}), 400
        
        with db_manager.get_cursor() as cursor:
            # Update all foreign key references
            for dup_id in duplicate_ids:
                # Update reviews
                cursor.execute('''
                    UPDATE reviews SET "reviewTarget" = %s 
                    WHERE "reviewTarget" = %s
                ''', (master_id, dup_id))
                
                # Update menu items
                cursor.execute('''
                    UPDATE "menuItems" SET "itemID" = %s 
                    WHERE "itemID" = %s
                ''', (master_id, dup_id))
                
                # Update user drink list items (check for duplicates first)
                cursor.execute('''
                    DELETE FROM "usersDrinkListItems" 
                    WHERE "drinkId" = %s 
                    AND "listId" IN (
                        SELECT "listId" FROM "usersDrinkListItems" 
                        WHERE "drinkId" = %s
                    )
                ''', (dup_id, master_id))
                
                cursor.execute('''
                    UPDATE "usersDrinkListItems" SET "drinkId" = %s 
                    WHERE "drinkId" = %s
                ''', (master_id, dup_id))
                
                # Update my cellar items
                cursor.execute('''
                    UPDATE "myCellarItems" SET "listingID" = %s 
                    WHERE "listingID" = %s
                ''', (master_id, dup_id))
                
                # Update listings comments
                cursor.execute('''
                    UPDATE "listingsComments" SET "listingId" = %s 
                    WHERE "listingId" = %s
                ''', (master_id, dup_id))
                
                # Update listings likes (remove duplicates first)
                cursor.execute('''
                    DELETE FROM "listingsLikes" 
                    WHERE "listingId" = %s 
                    AND ("userId", "userType") IN (
                        SELECT "userId", "userType" FROM "listingsLikes" 
                        WHERE "listingId" = %s
                    )
                ''', (dup_id, master_id))
                
                cursor.execute('''
                    UPDATE "listingsLikes" SET "listingId" = %s 
                    WHERE "listingId" = %s
                ''', (master_id, dup_id))
                
                # Update user leaderboard
                cursor.execute('''
                    DELETE FROM "userLeaderboard" 
                    WHERE "listing_id" = %s 
                    AND ("user_id", "category") IN (
                        SELECT "user_id", "category" FROM "userLeaderboard" 
                        WHERE "listing_id" = %s
                    )
                ''', (dup_id, master_id))
                
                cursor.execute('''
                    UPDATE "userLeaderboard" SET "listing_id" = %s 
                    WHERE "listing_id" = %s
                ''', (master_id, dup_id))
                
                # Update request inaccuracy
                cursor.execute('''
                    UPDATE "requestInaccuracy" SET "listingId" = %s 
                    WHERE "listingId" = %s
                ''', (master_id, dup_id))
                
                # Update request edits
                cursor.execute('''
                    UPDATE "requestEdits" SET "listingID" = %s 
                    WHERE "listingID" = %s
                ''', (master_id, dup_id))
            
            # Delete duplicate listings
            cursor.execute('''
                DELETE FROM listings WHERE id = ANY(%s)
            ''', (duplicate_ids,))
        
        return jsonify({
            "code": 200,
            "message": f"Successfully merged {len(duplicate_ids)} listings into listing ID {master_id}"
        }), 200
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        logger.error(f"Error merging listings: {str(e)}")
        return jsonify({"code": 500, "message": str(e)}), 500


# ==================== VENUE MERGE ====================

# [POST] Get venue merge preview
# - Get preview data for merging venues
@blueprint.route('/getVenueMergePreview', methods=['POST'])
def get_venue_merge_preview():
    """Get preview data for merging venues"""
    
    try:
        data = request.get_json()
        master_id = data.get('masterId')
        duplicate_ids = data.get('duplicateIds', [])
        
        if not master_id or not duplicate_ids:
            return jsonify({"code": 400, "message": "Missing required fields"}), 400
        
        with db_manager.get_cursor() as cursor:
            # Get all venue records
            all_ids = [master_id] + duplicate_ids
            cursor.execute('''
                SELECT id, "venueName", address, "venueType", "originLocation",
                       "yearOpened", website, "claimStatus"
                FROM venues 
                WHERE id = ANY(%s)
                ORDER BY id = %s DESC
            ''', (all_ids, master_id))
            
            venues = []
            rows = cursor.fetchall()
            for row in rows:
                if hasattr(row, 'keys'):  # RealDictRow
                    venues.append({
                        'id': row['id'],
                        'venueName': row['venueName'],
                        'address': row['address'],
                        'venueType': row['venueType'],
                        'originLocation': row['originLocation'],
                        'yearOpened': row['yearOpened'],
                        'website': row['website'],
                        'claimStatus': row['claimStatus']
                    })
                else:  # Tuple
                    venues.append({
                        'id': row[0],
                        'venueName': row[1],
                        'address': row[2],
                        'venueType': row[3],
                        'originLocation': row[4],
                        'yearOpened': row[5],
                        'website': row[6],
                        'claimStatus': row[7]
                    })
            
            # Helper function for safe counts
            def safe_count(query, vid):
                cursor.execute(query, (vid,))
                row = cursor.fetchone()
                if not row:
                    return 0
                # Handle both RealDictRow and tuple
                if hasattr(row, 'keys'):
                    return row['count']
                else:
                    return row[0]
            
            # Get related data counts
            related_counts = {}
            for vid in all_ids:
                counts = {
                    'menuSections': safe_count('SELECT COUNT(*) FROM "venuesMenu" WHERE "venueId" = %s', vid),
                    'reviews': safe_count('SELECT COUNT(*) FROM "venueReviews" WHERE "venueID" = %s', vid),
                    'qa': safe_count('SELECT COUNT(*) FROM "venuesQuestionAnswers" WHERE "venueId" = %s', vid),
                    'updates': safe_count('SELECT COUNT(*) FROM "venuesUpdates" WHERE "venueId" = %s', vid),
                    'events': safe_count('SELECT COUNT(*) FROM events WHERE "eventOwnerID" = %s AND "eventOwnerType" = \'venue\'', vid)
                }
                
                # Special case for followers (different query pattern)
                cursor.execute('''
                    SELECT COUNT(*) FROM "usersFollowLists" 
                    WHERE %s::text = ANY(venues)
                ''', (str(vid),))
                row = cursor.fetchone()
                if hasattr(row, 'keys'):
                    counts['followers'] = row['count']
                else:
                    counts['followers'] = row[0] if row else 0
                
                related_counts[vid] = counts
        
        return jsonify({
            "code": 200,
            "data": {
                "venues": venues,
                "relatedCounts": related_counts,
                "totalAffected": {
                    "menuSections": sum(c['menuSections'] for c in related_counts.values()),
                    "reviews": sum(c['reviews'] for c in related_counts.values()),
                    "qa": sum(c['qa'] for c in related_counts.values()),
                    "updates": sum(c['updates'] for c in related_counts.values()),
                    "events": sum(c['events'] for c in related_counts.values()),
                    "followers": sum(c['followers'] for c in related_counts.values())
                }
            }
        }), 200
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        logger.error(f"Error getting venue merge preview: {str(e)}")
        return jsonify({"code": 500, "message": str(e)}), 500

# [POST] Merge venues
# - Merge duplicate venues into a master venue
@blueprint.route('/mergeVenues', methods=['POST'])
def merge_venues():
    """Merge duplicate venues into a master venue"""
    
    try:
        data = request.get_json()
        master_id = data.get('masterId')
        duplicate_ids = data.get('duplicateIds', [])
        
        if not master_id or not duplicate_ids:
            return jsonify({"code": 400, "message": "Missing required fields"}), 400
        
        with db_manager.get_cursor() as cursor:
            # Update all foreign key references
            for dup_id in duplicate_ids:
                # HANDLE UNIQUE CONSTRAINT TABLES FIRST
                
                # Handle venuesOpeningHours (unique constraint on venueId)
                # Check if master already has opening hours
                cursor.execute('SELECT id FROM "venuesOpeningHours" WHERE "venueId" = %s', (master_id,))
                master_has_hours = cursor.fetchone()
                
                if master_has_hours:
                    # Delete duplicate's opening hours since master already has them
                    cursor.execute('DELETE FROM "venuesOpeningHours" WHERE "venueId" = %s', (dup_id,))
                else:
                    # Move duplicate's opening hours to master
                    cursor.execute('''
                        UPDATE "venuesOpeningHours" SET "venueId" = %s 
                        WHERE "venueId" = %s
                    ''', (master_id, dup_id))
                
                # Handle venueAmenities (unique constraint on venueId)
                # Check if master already has amenities
                cursor.execute('SELECT id FROM "venueAmenities" WHERE "venueId" = %s', (master_id,))
                master_has_amenities = cursor.fetchone()
                
                if master_has_amenities:
                    # Delete duplicate's amenities since master already has them
                    cursor.execute('DELETE FROM "venueAmenities" WHERE "venueId" = %s', (dup_id,))
                else:
                    # Move duplicate's amenities to master
                    cursor.execute('''
                        UPDATE "venueAmenities" SET "venueId" = %s 
                        WHERE "venueId" = %s
                    ''', (master_id, dup_id))
                
                # HANDLE REGULAR TABLES
                
                # Update venue menus and their items (preserve hierarchy)
                cursor.execute('''
                    UPDATE "venuesMenu" SET "venueId" = %s 
                    WHERE "venueId" = %s
                ''', (master_id, dup_id))
                
                # Update venue reviews
                cursor.execute('''
                    UPDATE "venueReviews" SET "venueID" = %s 
                    WHERE "venueID" = %s
                ''', (master_id, dup_id))
                
                # Update venue review comments
                cursor.execute('''
                    UPDATE "venueReviewsComments" 
                    SET "reviewId" = subquery.new_review_id
                    FROM (
                        SELECT vrc.id, vr_new.id as new_review_id
                        FROM "venueReviewsComments" vrc
                        JOIN "venueReviews" vr_old ON vrc."reviewId" = vr_old.id
                        JOIN "venueReviews" vr_new ON vr_old."userID" = vr_new."userID" 
                            AND vr_old."createdDate" = vr_new."createdDate"
                            AND vr_new."venueID" = %s
                        WHERE vr_old."venueID" = %s
                    ) AS subquery
                    WHERE "venueReviewsComments".id = subquery.id
                ''', (master_id, dup_id))
                
                # Update Q&A
                cursor.execute('''
                    UPDATE "venuesQuestionAnswers" SET "venueId" = %s 
                    WHERE "venueId" = %s
                ''', (master_id, dup_id))
                
                # Update venue updates
                cursor.execute('''
                    UPDATE "venuesUpdates" SET "venueId" = %s 
                    WHERE "venueId" = %s
                ''', (master_id, dup_id))
                
                # Update venue update comments
                cursor.execute('''
                    UPDATE "venueUpdateComments" 
                    SET "venueUpdateId" = subquery.new_update_id
                    FROM (
                        SELECT vuc.id, vu_new.id as new_update_id
                        FROM "venueUpdateComments" vuc
                        JOIN "venuesUpdates" vu_old ON vuc."venueUpdateId" = vu_old.id
                        JOIN "venuesUpdates" vu_new ON vu_old.date = vu_new.date 
                            AND vu_old.text = vu_new.text
                            AND vu_new."venueId" = %s
                        WHERE vu_old."venueId" = %s
                    ) AS subquery
                    WHERE "venueUpdateComments".id = subquery.id
                ''', (master_id, dup_id))
                
                # Update profile views
                cursor.execute('''
                    UPDATE "venuesProfileViews" SET "venueId" = %s 
                    WHERE "venueId" = %s
                ''', (master_id, dup_id))
                
                # Update reviews location reference
                cursor.execute('''
                    UPDATE reviews SET location = %s 
                    WHERE location = %s
                ''', (master_id, dup_id))
                
                # Update events
                cursor.execute('''
                    UPDATE events SET "eventOwnerID" = %s 
                    WHERE "eventOwnerID" = %s AND "eventOwnerType" = 'venue'
                ''', (master_id, dup_id))
                
                # Update event attendees for venue events
                cursor.execute('''
                    UPDATE "eventAttendees" 
                    SET "eventID" = e_new."id"
                    FROM events e_old
                    JOIN events e_new ON e_old."eventName" = e_new."eventName" 
                        AND e_old."eventStartDate" = e_new."eventStartDate"
                        AND e_new."eventOwnerID" = %s
                    WHERE "eventAttendees"."eventID" = e_old.id
                        AND e_old."eventOwnerID" = %s
                        AND e_old."eventOwnerType" = 'venue'
                ''', (master_id, dup_id))
                
                # Update clubs created by venues
                cursor.execute('''
                    UPDATE clubs 
                    SET "createdByID" = %s 
                    WHERE "createdByID" = %s AND "createdByType" = 'venues'
                ''', (master_id, dup_id))
                
                # Update club members for venue accounts
                cursor.execute('''
                    UPDATE "clubMembers" 
                    SET "userID" = %s 
                    WHERE "userID" = %s AND "userType" = 'venues'
                ''', (master_id, dup_id))
                
                # Update notifications for venues
                cursor.execute('''
                    UPDATE notifications 
                    SET "userId" = %s 
                    WHERE "userId" = %s AND "userType" = 'venue'
                ''', (master_id, dup_id))
                
                # Update user follow lists (stored as text array)
                cursor.execute('''
                    UPDATE "usersFollowLists" 
                    SET venues = array_replace(venues, %s::text, %s::text)
                    WHERE %s::text = ANY(venues)
                ''', (str(dup_id), str(master_id), str(dup_id)))
                
                # Update user venue list items (handle duplicates)
                cursor.execute('''
                    DELETE FROM "userVenueListItems" 
                    WHERE "venueId" = %s 
                    AND "listId" IN (
                        SELECT "listId" FROM "userVenueListItems" 
                        WHERE "venueId" = %s
                    )
                ''', (dup_id, master_id))
                
                cursor.execute('''
                    UPDATE "userVenueListItems" SET "venueId" = %s 
                    WHERE "venueId" = %s
                ''', (master_id, dup_id))
                
                # Update request inaccuracy
                cursor.execute('''
                    UPDATE "requestInaccuracy" SET "venueId" = %s 
                    WHERE "venueId" = %s
                ''', (master_id, dup_id))
                
                # Update my cellar items purchase venue
                cursor.execute('''
                    UPDATE "myCellarItems" SET "purchaseVenueID" = %s 
                    WHERE "purchaseVenueID" = %s
                ''', (master_id, dup_id))
                
                # Update request listings
                cursor.execute('''
                    UPDATE "requestListings" SET "venueID" = %s 
                    WHERE "venueID" = %s
                ''', (master_id, dup_id))
                
                # Update tokens table
                cursor.execute('''
                    UPDATE tokens SET "venueId" = %s 
                    WHERE "venueId" = %s
                ''', (master_id, dup_id))
                
                # Update userFestivalTastedList
                cursor.execute('''
                    UPDATE "userFestivalTastedList" SET "venueId" = %s 
                    WHERE "venueId" = %s
                ''', (master_id, dup_id))
                
                # Update points recorder
                cursor.execute('''
                    UPDATE "pointsRecorder" 
                    SET "userID" = %s 
                    WHERE "userID" = %s AND "userType" = 'venues'
                ''', (master_id, dup_id))
            
            # Delete duplicate venues
            cursor.execute('''
                DELETE FROM venues WHERE id = ANY(%s)
            ''', (duplicate_ids,))
            
            # Auto-commit happens when context manager exits successfully
        
        return jsonify({
            "code": 200,
            "message": f"Successfully merged {len(duplicate_ids)} venues into venue ID {master_id}"
        }), 200
        
    except Exception as e:
        # Auto-rollback is handled automatically by the context manager on exception
        import traceback
        traceback.print_exc()
        logger.error(f"Error merging venues: {str(e)}")
        return jsonify({"code": 500, "message": str(e)}), 500

# ==================== SEARCH ENDPOINTS ====================

# [GET] Search for potential duplicates
# - Search by entity type (producers, listings, venues) and search term
@blueprint.route('/searchDuplicates/<entity_type>', methods=['GET'])
def search_duplicates(entity_type):
    """Search for potential duplicates by entity type and search term"""
    
    try:
        search_term = request.args.get('q', '').strip()
        if not search_term:
            return jsonify({"code": 400, "message": "Search term required"}), 400
        
        results = []
        
        # Check if search term is a URL and extract ID
        import re
        url_patterns = {
            'producers': r'/profile/producer/(\d+)/',
            'listings': r'/listing/view/(\d+)/',
            'venues': r'/profile/venue/(\d+)/'
        }
        
        # Try to extract ID from URL if it matches the pattern
        extracted_id = None
        if entity_type in url_patterns:
            match = re.search(url_patterns[entity_type], search_term)
            if match:
                extracted_id = int(match.group(1))
        
        with db_manager.get_cursor() as cursor:
            if entity_type == 'producers':
                if extracted_id:
                    # Direct ID search from URL
                    cursor.execute('''
                        SELECT id, "producerName", "originCountry", "yearFounded"
                        FROM producers 
                        WHERE id = %s
                    ''', (extracted_id,))
                else:
                    # Regular name search
                    cursor.execute('''
                        SELECT id, "producerName", "originCountry", "yearFounded"
                        FROM producers 
                        WHERE LOWER("producerName") LIKE LOWER(%s)
                        ORDER BY "producerName"
                        LIMIT 50
                    ''', (f'%{search_term}%',))
                
                rows = cursor.fetchall()
                for row in rows:
                    # Handle both RealDictRow and tuple formats
                    if hasattr(row, 'keys'):  # RealDictRow
                        results.append({
                            'id': row['id'],
                            'name': row['producerName'],
                            'country': row['originCountry'],
                            'year': row['yearFounded']
                        })
                    else:  # Tuple
                        results.append({
                            'id': row[0],
                            'name': row[1],
                            'country': row[2],
                            'year': row[3]
                        })
                    
            elif entity_type == 'listings':
                if extracted_id:
                    # Direct ID search from URL
                    cursor.execute('''
                        SELECT l.id, l."listingName", p."producerName", l."drinkType", l."typeCategory"
                        FROM listings l
                        LEFT JOIN producers p ON l."producerID" = p.id
                        WHERE l.id = %s
                    ''', (extracted_id,))
                else:
                    # Regular name search
                    cursor.execute('''
                        SELECT l.id, l."listingName", p."producerName", l."drinkType", l."typeCategory"
                        FROM listings l
                        LEFT JOIN producers p ON l."producerID" = p.id
                        WHERE LOWER(l."listingName") LIKE LOWER(%s)
                        ORDER BY l."listingName"
                        LIMIT 50
                    ''', (f'%{search_term}%',))
                
                rows = cursor.fetchall()
                for row in rows:
                    # Handle both RealDictRow and tuple formats
                    if hasattr(row, 'keys'):  # RealDictRow
                        results.append({
                            'id': row['id'],
                            'name': row['listingName'],
                            'producer': row['producerName'],
                            'type': row['drinkType'],
                            'category': row['typeCategory']
                        })
                    else:  # Tuple
                        results.append({
                            'id': row[0],
                            'name': row[1],
                            'producer': row[2],
                            'type': row[3],
                            'category': row[4]
                        })
                    
            elif entity_type == 'venues':
                if extracted_id:
                    # Direct ID search from URL
                    cursor.execute('''
                        SELECT id, "venueName", address, "venueType"
                        FROM venues 
                        WHERE id = %s
                    ''', (extracted_id,))
                else:
                    # Regular name search
                    cursor.execute('''
                        SELECT id, "venueName", address, "venueType"
                        FROM venues 
                        WHERE LOWER("venueName") LIKE LOWER(%s)
                        ORDER BY "venueName"
                        LIMIT 50
                    ''', (f'%{search_term}%',))
                
                rows = cursor.fetchall()
                for row in rows:
                    # Handle both RealDictRow and tuple formats
                    if hasattr(row, 'keys'):  # RealDictRow
                        results.append({
                            'id': row['id'],
                            'name': row['venueName'],
                            'address': row['address'],
                            'type': row['venueType']
                        })
                    else:  # Tuple
                        results.append({
                            'id': row[0],
                            'name': row[1],
                            'address': row[2],
                            'type': row[3]
                        })
            else:
                return jsonify({"code": 400, "message": "Invalid entity type"}), 400
        
        return jsonify({
            "code": 200,
            "data": results
        }), 200
        
    except Exception as e:
        logger.error(f"Error searching duplicates: {str(e)}")
        return jsonify({"code": 500, "message": str(e)}), 500


# [GET] Get entity by ID
# - Fetch a specific entity's details by its ID
@blueprint.route('/getEntityById/<entity_type>/<int:entity_id>', methods=['GET'])
def get_entity_by_id(entity_type, entity_id):
    """Get a specific entity by its ID"""
    conn = g.db
    cursor = conn.cursor()
    
    try:
        result = None
        
        if entity_type == 'producers':
            cursor.execute('''
                SELECT id, "producerName", "originCountry", "yearFounded"
                FROM producers 
                WHERE id = %s
            ''', (entity_id,))
            
            row = cursor.fetchone()
            if row:
                if hasattr(row, 'keys'):
                    result = {
                        'id': row['id'],
                        'name': row['producerName'],
                        'country': row['originCountry'],
                        'year': row['yearFounded']
                    }
                else:
                    result = {
                        'id': row[0],
                        'name': row[1],
                        'country': row[2],
                        'year': row[3]
                    }
                    
        elif entity_type == 'listings':
            cursor.execute('''
                SELECT l.id, l."listingName", p."producerName", l."drinkType", l."typeCategory"
                FROM listings l
                LEFT JOIN producers p ON l."producerID" = p.id
                WHERE l.id = %s
            ''', (entity_id,))
            
            row = cursor.fetchone()
            if row:
                if hasattr(row, 'keys'):
                    result = {
                        'id': row['id'],
                        'name': row['listingName'],
                        'producer': row['producerName'],
                        'type': row['drinkType'],
                        'category': row['typeCategory']
                    }
                else:
                    result = {
                        'id': row[0],
                        'name': row[1],
                        'producer': row[2],
                        'type': row[3],
                        'category': row[4]
                    }
                    
        elif entity_type == 'venues':
            cursor.execute('''
                SELECT id, "venueName", address, "venueType"
                FROM venues 
                WHERE id = %s
            ''', (entity_id,))
            
            row = cursor.fetchone()
            if row:
                if hasattr(row, 'keys'):
                    result = {
                        'id': row['id'],
                        'name': row['venueName'],
                        'address': row['address'],
                        'type': row['venueType']
                    }
                else:
                    result = {
                        'id': row[0],
                        'name': row[1],
                        'address': row[2],
                        'type': row[3]
                    }
        
        if result:
            return jsonify({"code": 200, "data": result}), 200
        else:
            return jsonify({"code": 404, "message": "Entity not found"}), 404
            
    except Exception as e:
        logger.error(f"Error getting entity by ID: {str(e)}")
        return jsonify({"code": 500, "message": str(e)}), 500
    finally:
        cursor.close()