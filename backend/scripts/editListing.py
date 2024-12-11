# Port: 5002
# Routes: /updateListing/<id> (PUT), /deleteListing/<id> (DELETE), /getDistance/<origins>/<destinations>/<key> (GET)
# Dataclass: listings
# -----------------------------------------------------------------------------------------

import os
import json
import s3Images
from bson import json_util
from flask import Blueprint, g, request, jsonify
from bson.objectid import ObjectId
from bson.errors import InvalidId
import pip._vendor.requests as requests

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

def parse_json(data):
    return json.loads(json_util.dumps(data))

# -----------------------------------------------------------------------------------------
# [PUT] Updates a listing
# - Update entry with specified id from the "listings" collection. Follows listings dataclass requirements.
# - Duplicate listing check: If a listing with the same name exists, reject the request
# - Possible return codes: 200 (Updated), 410 (Duplicate Detected), 420 (Invalid ID), 440 (Not Found), 450 (Error during update)
@blueprint.route("/updateListing/<id>", methods=['POST'])
def updateListing(id):
    conn = g.db
    cur = conn.cursor()

    updatedListing = request.get_json()
    updatedListing['producerID'] = int(updatedListing['producerID'])

    if 'abv' in updatedListing:
        abv_value = updatedListing['abv'].replace('%', '')
        updatedListing['abv'] = float(abv_value)

    updatedListingName = updatedListing["listingName"]

    try:
        # Check if listing with the same name exists
        cur.execute("SELECT * FROM listings WHERE \"listingName\" = %s", (updatedListingName,))
        existingBottle = cur.fetchone()

        if existingBottle is not None and existingBottle['id'] != int(id):
            return jsonify(
                {   
                    "code": 410,
                    "data": {
                        "listingName": updatedListingName
                    },
                    "message": "Bottle already exists."
                }
            ), 410
        
        # If it's an existing bottle, delete the old image from S3 and upload the new one
        if existingBottle and updatedListing.get('photo'):
            try:
                if existingBottle['photo'] is not None and existingBottle['photo'] != '':
                    s3Images.deleteImageFromS3(existingBottle['photo'])
                updatedListing['photo'] = s3Images.uploadBase64ImageToS3(updatedListing['photo'])
            except Exception as e:
                print(str(e))
                return jsonify(
                    {
                        "code": 450,
                        "data": {
                            "id": id
                        },
                        "message": "An error occurred updating the listing."
                    }
                ), 450
            
        # Update the listing
        columns = ', '.join(f'"{col}" = %s' for col in updatedListing.keys())
        sql = f'UPDATE listings SET {columns} WHERE "id" = %s'
        cur.execute(sql, list(updatedListing.values()) + [id])
        conn.commit()

        return jsonify(
            {
                "code": 200,
                "data": id,
                "message": "Listing updated successfully."
            }
        ), 200
    
    except Exception as e:
        print(str(e))
        conn.rollback()
        return jsonify(
            {
                "code": 450,
                "data": id,
                "message": "An error occurred updating the listing."
            }
        ), 450
    
    finally:
        cur.close()

# -----------------------------------------------------------------------------------------
# [POST] Updates listing moderation status
# - Update entry with specified id from the "listings" collection. Follows listings dataclass requirements.
# - Possible return codes: 200 (Updated), 420 (Invalid ID), 440 (Not Found), 450 (Error during update)
@blueprint.route("/updateListingMod/<id>", methods=['POST'])
def updateListingMod(id):
    conn = g.db
    cur = conn.cursor()

    updatedListing = request.get_json()
    allowMod = updatedListing["allowMod"]
    listingName = updatedListing["listingName"]

    try:
        cur.execute("SELECT * FROM listings WHERE \"id\" = %s", (id,))
        existingListing = cur.fetchone()

        if existingListing is None:
            return jsonify(
                {   
                    "code": 440,
                    "data": {
                        "id": id
                    },
                    "message": "Listing doesn't exist."
                }
            ), 440
        
        cur.execute('UPDATE listings SET "allowMod" = %s WHERE "id" = %s', (allowMod, id))
        conn.commit()

        return jsonify(
            {
                "code": 200,
                "data": id,
                "message": "Listing moderation status updated successfully."
            }
        ), 200
    
    except Exception as e:
        print(str(e))
        conn.rollback()
        return jsonify(
            {
                "code": 450,
                "data": id,
                "message": "An error occurred updating the listing moderation status."
            }
        ), 450
    
    finally:
        cur.close()

# -----------------------------------------------------------------------------------------
# [DELETE] Deletes a listing
# - Delete entry with specified id from the "listings" collection
# - Possible return codes: 201 (Deleted), 400 (Listing doesn't exist), 500 (Error during deletion)
@blueprint.route("/deleteListing/<id>", methods=['DELETE'])
def deleteListing(id):
    conn = g.db
    cur = conn.cursor()
    
    # Find the listing entry with the specified id
    cur.execute('SELECT * FROM listings WHERE "id" = %s', (id,))
    existingListing = cur.fetchone()

    if existingListing is None:
        return jsonify(
            {   
                "code": 400,
                "data": {
                    "id": id
                },
                "message": "Listing doesn't exist."
            }
        ), 400
    
    try:
        # Delete image from S3 bucket only if it exists
        if existingListing['photo'] is not None and existingListing['photo'] != '':
            s3Images.deleteImageFromS3(existingListing['photo'])

        # Find and delete associated reviews and votes
        cur.execute('SELECT "id" FROM reviews WHERE "reviewTarget" = %s', (id,))
        reviews = cur.fetchall()

        for review in reviews:
            review_id = review['id']

            # Delete associated votes for each review
            cur.execute('DELETE FROM "reviewsUserVotes" WHERE "reviewId" = %s', (review_id,))

        # Delete associated reviews
        cur.execute('DELETE FROM reviews WHERE "reviewTarget" = %s', (id,))

        # Delete the listing
        cur.execute('DELETE FROM listings WHERE "id" = %s', (id,))

        conn.commit()

        return jsonify(
            {   
                "code": 201,
                "message": "Listing deleted successfully!"
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
                "message": "An error occurred deleting listing!"
            }
        ), 500

# -----------------------------------------------------------------------------------------
# [GET] Get distance between two locations
# - Get distance between two locations
# - Possible return codes: 201 (Success), 500 (Error)
@blueprint.route("/getDistance/<origins>/<destinations>/<key>", methods=['GET'])
def getDistance(origins, destinations, key):
    db = g.db
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?destinations={destinations}&origins={origins}&key={key}"
    response = requests.get(url)
    data = response.json()

    if data["status"] == "OK":
        return jsonify(
            {
                "code": 201,
                "data": data
            }
        ), 201
    else:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred getting distance!"
            }
        ), 500