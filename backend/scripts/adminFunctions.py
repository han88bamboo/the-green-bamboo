# Port: 5052
# Routes: /createObservationTag (POST), /updateObservationTag (PUT), /deleteObservationTag/<id> (DELETE), /updateFamilyTag (POST), /updateSubTag (PUT), /deleteFamilyTag/<id> (DELETE), /deleteSubTag/<id> (DELETE), /importListings (POST), /createFamilyTag (POST), /createSubTag (POST), /importListings (POST), /readCSV (GET)
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
from concurrent.futures import ThreadPoolExecutor

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
    conn = g.db
    cur = conn.cursor()
    rawTag = request.get_json()
    rawObservationTag = rawTag['observationTag']

    try:
        # Check if the observation tag already exists
        cur.execute('SELECT * FROM "observationTags" WHERE "observationTag" = %s', (rawObservationTag,))
        existingObservationTag = cur.fetchone()

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
        cur.execute('INSERT INTO "observationTags" ("observationTag") VALUES (%s) RETURNING "id"', (rawObservationTag,))
        newObservationTagId = cur.fetchone()
        conn.commit()

        return jsonify(
            {
                "code": 201,
                "data": newObservationTagId
            }
        ), 201

    except Exception as e:
        print(str(e))
        conn.rollback()
        return jsonify(
            {
                "code": 500,
                "data": {
                    "observationTag": rawObservationTag
                },
                "message": "An error occurred creating the observation tag."
            }
        ), 500

    finally:
        cur.close()

# -----------------------------------------------------------------------------------------
    
# [PUT] Update observation tag
# - Update observation tag with updated data
# - Possible return codes: 201 (Updated), 400(Observation tag not found), 500 (Error during update)
@blueprint.route('/updateObservationTag', methods=['PUT'])
def updateObservationTag():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()

    updates = []
    for elem in data:
        # check psql table for existing observation tag
        cur.execute('SELECT * FROM "observationTags" WHERE "id" = %s', (elem["id"],))
        existingObservationTag = cur.fetchone()

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
            cur.execute('UPDATE "observationTags" SET "observationTag" = %s WHERE "id" = %s', (update["update"]["observationTag"], update["id"]))
            conn.commit()
        return jsonify(
            {   
                "code": 201,
                "data": elem['observationTag']
            }
        ), 201

    except Exception as e:
        print(str(e))
        conn.rollback()
        return jsonify(
            {
                "code": 500,
                "data": {
                    "data": elem['observationTag']
                },
                "message": "An error occurred updating the observation tags."
            }
        ), 500

    finally:
        cur.close()
# -----------------------------------------------------------------------------------------
# [DELETE] Deletes a observationTag
# - Delete entry with specified id from the "observationTag" collection.
# - Possible return codes: 201 (Deleted), 400 (Review doesn't exist), 500 (Error during deletion)
@blueprint.route("/deleteObservationTag/<id>", methods= ['DELETE'])
def deleteObservationTag(id):
    conn = g.db
    cur = conn.cursor()

    cur.execute('SELECT * FROM "observationTags" WHERE "id" = %s', (id,))
    existingObservation = cur.fetchone()

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

    try:
        cur.execute('DELETE FROM "observationTags" WHERE "id" = %s', (id,))
        conn.commit()
        return jsonify( 
            {   
                "code": 200,
                "data": id
            }
        ), 201

    except Exception as e:
        print(str(e))
        conn.rollback()
        return jsonify(
            {
                "code": 500,
                "data": {
                    "id": id
                },
                "message": "An error occurred deleting the observation."
            }
        ), 500

    finally:
        cur.close()

# -----------------------------------------------------------------------------------------
    
# [PUT] Update family tag
# - Update flavour tag with updated family tag data
# - Possible return codes: 201 (Updated), 400(Flavour tag not found), 500 (Error during update)
@blueprint.route('/updateFamilyTag', methods=['PUT'])
def updateFamilyTag():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()

    updates = []
    try:
        for elem in data:
            cur.execute('SELECT id FROM "flavourTags" WHERE id = %s', (elem["id"],))
            existingFamilyTag = cur.fetchone()

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

            cur.execute("""
                UPDATE "flavourTags" SET "familyTag" = %s, "hexcode" = %s WHERE "id" = %s
            """, (elem["familyTag"], elem["hexcode"], elem["id"]))
            conn.commit()

            updates.append({"id": elem["id"], "familyTag": elem["familyTag"], "hexcode": elem["hexcode"]})

        return jsonify(
            {
                "code": 201,
                "data": updates
            }
        ), 201

    except Exception as e:
        print(str(e))
        conn.rollback()
        return jsonify(
            {
                "code": 500,
                "data": {
                    "familyTag": elem["familyTag"]
                },
                "message": "An error occurred updating the family tag."
            }
        ), 500

    finally:
        cur.close()
            
    
# -----------------------------------------------------------------------------------------
    
# [PUT] Update sub tag
# - Update subtag with udpated subtag info
# - Possible return codes: 201 (Updated), 400(Sub tag not found), 500 (Error during update)
@blueprint.route('/updateSubTag', methods=['PUT'])
def updateSubTag():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()

    updates = []
    try:
        for elem in data:
            # Check if the sub tag exists
            cur.execute('SELECT id FROM "subTags" WHERE "id" = %s', (elem["id"],))
            existingSubTag = cur.fetchone()

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

            cur.execute("""
                UPDATE "subTags" SET "subTag" = %s WHERE "id" = %s
            """, (elem["subTag"], elem["id"]))
            conn.commit()

            updates.append({"id": elem["id"], "subTag": elem["subTag"]})

        return jsonify(
            {
                "code": 201,
                "data": updates
            }
        ), 201

    except Exception as e:
        print(str(e))
        conn.rollback()
        return jsonify(
            {
                "code": 500,
                "data": {
                    "subTag": elem["subTag"]
                },
                "message": "An error occurred updating the sub tag."
            }
        ), 500

    finally:
        cur.close()
    
# -----------------------------------------------------------------------------------------
    
# [DELETE] Deletes a familyTag
# - Delete entry with specified id from the "flavourTags" collection.
# - Possible return codes: 201 (Deleted), 400 (family tag doesn't exist), 500 (Error during deletion)
@blueprint.route("/deleteFamilyTag/<id>", methods= ['DELETE'])
def deleteFamilyTag(id):
    conn = g.db
    cur = conn.cursor()

    try:
        cur.execute('SELECT id FROM "flavourTags" WHERE "id" = %s', (id,))
        existingFamilyTag = cur.fetchone()

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

        cur.execute('DELETE FROM "subTags" WHERE "familyTagId" = %s', (id,))
        cur.execute('DELETE FROM "flavourTags" WHERE "id" = %s', (id,))
        conn.commit()

        return jsonify(
            {
                "code": 201,
                "data": id
            }
        ), 201

    except Exception as e:
        print(str(e))
        conn.rollback()
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
    conn = g.db
    cur = conn.cursor()

    try:
        # Check if the sub tag exists
        cur.execute('SELECT id FROM "subTags" WHERE "id" = %s', (id,))
        existingSubTag = cur.fetchone()

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

        cur.execute('DELETE FROM "subTags" WHERE "id" = %s', (id,))
        conn.commit()

        return jsonify(
            {
                "code": 201,
                "data": id
            }
        ), 201

    except Exception as e:
        print(str(e))
        conn.rollback()
        return jsonify(
            {
                "code": 500,
                "data": {
                    "id": id
                },
                "message": "An error occurred deleting the sub tag."
            }
        ), 500

    finally:
        cur.close()
    
# -----------------------------------------------------------------------------------------
# [POST] Creates a flavour family tag
# - Insert entry into the "familyTags" collection. Follows flavourTag dataclass requirements.
# - Duplicate review check: If a flavourTag with the same flavourTag, reject the request
# - Possible return codes: 201 (Created), 400 (Duplicate Detected), 500 (Error during creation)
@blueprint.route("/createFamilyTag", methods= ['POST'])
def createFamilyTag():
    conn = g.db
    cur = conn.cursor()
    rawTag = request.get_json()
    rawFamily= rawTag['familyTag']

    try:
        # Duplicate listing check: Reject if a subTag with the same name exists in the database
        cur.execute('SELECT id FROM "flavourTags" WHERE "familyTag" = %s', (rawFamily,))
        existingTag = cur.fetchone()

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
        cur.execute("""
            INSERT INTO "flavourTags" ("familyTag", "hexcode") VALUES (%s, %s) RETURNING "id"
        """, (rawFamily, rawTag['hexcode']))
        newFamilyTagId = cur.fetchone()
        conn.commit()

        return jsonify(
            {
                "code": 201,
                "data": newFamilyTagId
            }
        ), 201

    except Exception as e:
        print(str(e))
        conn.rollback()
        return jsonify(
            {
                "code": 500,
                "data": {
                    "familyTag": rawFamily
                },
                "message": "An error occurred creating the family tag."
            }
        ), 500

    finally:
        cur.close()
# -----------------------------------------------------------------------------------------
# [POST] Creates a flavour sub tag
# - Insert entry into the "subTags" collection. Follows subTag dataclass requirements.
# - Duplicate review check: If a subTag with the same subTag, reject the request
# - Possible return codes: 201 (Created), 400 (Duplicate Detected), 500 (Error during creation)
@blueprint.route("/createSubTag", methods= ['POST'])
def createSubTag():
    conn = g.db
    cur = conn.cursor()
    rawTag = request.get_json()
    rawSub= rawTag['subTag']

    # Duplicate listing check: Reject if review with the same observation exists in the database
    try:
        cur.execute('SELECT id FROM "subTags" WHERE "subTag" = %s', (rawSub,))
        existingTag = cur.fetchone()

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
        cur.execute("""
            INSERT INTO "subTags" ("familyTagId", "subTag") VALUES (%s, %s) RETURNING "id"
        """, (rawTag['familyTagId'], rawSub))
        newSubTagId = cur.fetchone()
        conn.commit()

        return jsonify(
            {
                "code": 201,
                "data": newSubTagId
            }
        ), 201

    except Exception as e:
        print(str(e))
        conn.rollback()
        return jsonify(
            {
                "code": 500,
                "data": {
                    "subTag": rawSub
                },
                "message": "An error occurred creating the sub tag."
            }
        ), 500

    finally:
        cur.close()
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
    conn = g.db
    cur = conn.cursor()
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
    cur.execute('SELECT "producerName", "id" FROM "producers"')
    producers = cur.fetchall()
    producer_name_id_dict = {row['producerName']: row['id'] for row in producers}

    # Collect producer names from CSV
    csv_producers = set(row[1] for row in rows if row[1])

    # Determine new producers to insert
    new_producers = csv_producers - set(producer_name_id_dict.keys())
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
            "claimStatusCheckDate": None
        }
        for name in new_producers
    ]

    # Bulk insert new producers and fetch their IDs
    if new_producer_data:
        insert_query = """
            INSERT INTO producers (
                "producerName", "producerDesc", "originCountry", "mainDrinks", "photo", "hashedPassword",
                "claimStatus", "statusOB", "username", "producerLink", "stripeCustomerId", "claimStatusCheckDate"
            ) VALUES %s RETURNING "producerName", "id"
        """
        execute_values(cur, insert_query, [
            (
                producer["producerName"], producer["producerDesc"], producer["originCountry"],
                producer["mainDrinks"], producer["photo"], producer["hashedPassword"],
                producer["claimStatus"], producer["statusOB"], producer["username"],
                producer["producerLink"], producer["stripeCustomerId"], producer["claimStatusCheckDate"]
            )
            for producer in new_producer_data
        ])
        conn.commit()
        new_producers_with_ids = cur.fetchall()
        producer_name_id_dict.update({row["producerName"]: row["id"] for row in new_producers_with_ids})

    # Process listings and prepare for bulk insert
    listings_to_insert = []
    image_urls = []

    for row in rows:
        converted_row = []
        for data_type, value in zip(column_data_types, row):
            if data_type is float:
                value = value.replace('%', '').strip()
                converted_value = float(value) if value and value.lower() != 'n/a' else None
            else:
                converted_value = data_type(value) if value else None
            converted_row.append(converted_value)

        producer_name = converted_row[1]
        producer_id = producer_name_id_dict.get(producer_name)

        # Collect image URL for parallel upload
        image_urls.append(converted_row[12])

        listings_to_insert.append({
            'listingName': converted_row[0],
            'producerID': producer_id,
            'bottler': converted_row[2],
            'originCountry': converted_row[3],
            'drinkType': converted_row[4],
            'typeCategory': converted_row[5],
            'drinkStyle':converted_row[6], 
            'age': converted_row[7],
            'abv': converted_row[8],
            'reviewLink': converted_row[9],
            'officialDesc': converted_row[10],
            'sourceLink': converted_row[11],
            'photo': None,  # Placeholder for S3 URL
            'allowMod': True,
            'addedDate': datetime.now()
        })

    # Parallelize S3 image uploads
    def upload_image(image_url):
        return s3Images.uploadURLtoS3(image_url) if image_url else None

    with ThreadPoolExecutor() as executor:
        s3_urls = list(executor.map(upload_image, image_urls))
        print("S3 URLs:", s3_urls)

    # Update photo URLs in listings
    for listing, s3_url in zip(listings_to_insert, s3_urls):
        listing['photo'] = s3_url

    # Bulk insert listings
    listing_columns = listings_to_insert[0].keys()
    listing_query = "INSERT INTO listings ({}) VALUES %s".format(
        ', '.join(f'"{col}"' for col in listing_columns)
    )
    listing_values = [tuple(listing.values()) for listing in listings_to_insert]
    execute_values(cur, listing_query, listing_values)
    conn.commit()

    return jsonify({
        "code": 201,
        "message": f"{file.filename} has been fully uploaded!"
    }), 201


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
