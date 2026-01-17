# Port: 5002
# Routes: /updateListing/<id> (PUT), /deleteListing/<id> (DELETE), /getDistance/<origins>/<destinations>/<key> (GET)
# Dataclass: listings
# -----------------------------------------------------------------------------------------

import os
import json
import s3Images
from flask import Blueprint, g, request, jsonify
import pip._vendor.requests as requests
import re

# Import the database manager for connection pooling
from app import db_manager

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

# -----------------------------------------------------------------------------------------
# [PUT] Updates a listing
# - Update entry with specified id from the "listings" collection. Follows listings dataclass requirements.
# - Duplicate listing check: If a listing with the same name exists, reject the request
# - Possible return codes: 200 (Updated), 410 (Duplicate Detected), 420 (Invalid ID), 440 (Not Found), 450 (Error during update)
@blueprint.route("/updateListing/<id>", methods=['POST'])
def updateListing(id):
    updatedListing = request.get_json()
    updatedListing['producerID'] = int(updatedListing['producerID'])

    if 'bottlerID' in updatedListing and updatedListing['bottlerID'] == '':
        updatedListing['bottlerID'] = None
    elif 'bottlerID' in updatedListing and updatedListing['bottlerID']:
        updatedListing['bottlerID'] = int(updatedListing['bottlerID'])

    # Convert abv from string to float if necessary
    if 'abv' in updatedListing:
        abv_value = updatedListing['abv'].replace('%', '')  # Remove the '%' sign
        if abv_value.strip():  # Check if the string is not empty
            updatedListing['abv'] = float(abv_value)
        else:
            # Handle empty ABV - set to NULL in database
            updatedListing['abv'] = None
    
    # Handle tags field - ensure it's a string or NULL
    if 'tags' in updatedListing:
        if updatedListing['tags'] is None or updatedListing['tags'].strip() == "":
            updatedListing['tags'] = None
        else:
            # Ensure tags is a string (it should already be trimmed from frontend)
            updatedListing['tags'] = str(updatedListing['tags'])
    
    # Handle order field - ensure it's an integer or NULL
    if 'order' in updatedListing:
        if updatedListing['order'] is None or updatedListing['order'] == "":
            updatedListing['order'] = None
        else:
            try:
                updatedListing['order'] = int(updatedListing['order'])
            except (ValueError, TypeError):
                updatedListing['order'] = None

    # Handle varietyTags field - ensure it's a PostgreSQL array or NULL
    if 'varietyTags' in updatedListing:
        if updatedListing['varietyTags'] is None or updatedListing['varietyTags'] == "" or updatedListing['varietyTags'] == []:
            updatedListing['varietyTags'] = None
        elif isinstance(updatedListing['varietyTags'], list):
            # It's already a list, keep it as is (will be converted to PostgreSQL array)
            pass
        elif isinstance(updatedListing['varietyTags'], str):
            # If it's a string, try to parse it as JSON array
            try:
                import json
                updatedListing['varietyTags'] = json.loads(updatedListing['varietyTags'])
            except:
                # If parsing fails, set to NULL
                updatedListing['varietyTags'] = None
        else:
            updatedListing['varietyTags'] = None

    updatedListingName = updatedListing["listingName"]

    with db_manager.get_cursor() as cursor:
        # Check if listing with the same name exists
        cursor.execute("SELECT * FROM listings WHERE \"listingName\" = %s", (updatedListingName,))
        existingBottle = cursor.fetchone()

        # if existingBottle is not None and existingBottle['id'] != int(id):
        #     return jsonify(
        #         {   
        #             "code": 410,
        #             "data": {
        #                 "listingName": updatedListingName
        #             },
        #             "message": "Bottle already exists."
        #         }
        #     ), 410
        
        # If it's an existing bottle, delete the old image from S3 and upload the new one
        if existingBottle and updatedListing.get('photo'):
            try:
                # Upload new image if it's base64, otherwise keep as is
                import re
                if updatedListing['photo'].startswith('data:image'):
                    base64_string = re.sub(r'^data:image\/[a-zA-Z]+;base64,', '', updatedListing['photo'])
                    updatedListing['photo'] = s3Images.uploadBase64ImageToS3(base64_string)
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
        cursor.execute(sql, list(updatedListing.values()) + [id])

        return jsonify(
            {
                "code": 200,
                "data": id,
                "message": "Listing updated successfully."
            }
        ), 200

# -----------------------------------------------------------------------------------------
# [POST] Updates listing moderation status
# - Update entry with specified id from the "listings" collection. Follows listings dataclass requirements.
# - Possible return codes: 200 (Updated), 420 (Invalid ID), 440 (Not Found), 450 (Error during update)
@blueprint.route("/updateListingMod/<id>", methods=['POST'])
def updateListingMod(id):
    updatedListing = request.get_json()
    allowMod = updatedListing["allowMod"]
    listingName = updatedListing["listingName"]

    try:
        with db_manager.get_cursor() as cursor:
            cursor.execute("SELECT * FROM listings WHERE \"id\" = %s", (id,))
            existingListing = cursor.fetchone()

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
            
            cursor.execute('UPDATE listings SET "allowMod" = %s WHERE "id" = %s', (allowMod, id))

            return jsonify(
                {
                    "code": 200,
                    "data": id,
                    "message": "Listing moderation status updated successfully."
                }
            ), 200
    
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 450,
                "data": id,
                "message": "An error occurred updating the listing moderation status."
            }
        ), 450

# -----------------------------------------------------------------------------------------
# [DELETE] Deletes a listing
# - Delete entry with specified id from the "listings" collection
# - Possible return codes: 201 (Deleted), 400 (Listing doesn't exist), 500 (Error during deletion)
@blueprint.route("/deleteListing/<id>", methods=['DELETE'])
def deleteListing(id):
    with db_manager.get_cursor(commit=False) as cursor:
        
        # Find the listing entry with the specified id
        cursor.execute('SELECT * FROM listings WHERE "id" = %s', (id,))
        existingListing = cursor.fetchone()

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
            # Try to delete image from S3 bucket - non-blocking (continue even if it fails)
            if existingListing['photo'] is not None and existingListing['photo'] != '':
                try:
                    s3Images.deleteImageFromS3(existingListing['photo'])
                except Exception as s3_error:
                    # Log but don't fail - orphaned S3 images can be cleaned up later
                    print(f"Warning: Failed to delete S3 image for listing {id}: {str(s3_error)}")

            # Find and delete associated reviews and votes
            cursor.execute('SELECT "id" FROM reviews WHERE "reviewTarget" = %s', (id,))
            reviews = cursor.fetchall()

            for review in reviews:
                review_id = review['id']

                # Delete associated votes for each review
                cursor.execute('DELETE FROM "reviewsUserVotes" WHERE "reviewId" = %s', (review_id,))

            # Delete associated reviews
            cursor.execute('DELETE FROM reviews WHERE "reviewTarget" = %s', (id,))

            # Delete the listing
            cursor.execute('DELETE FROM listings WHERE "id" = %s', (id,))

            cursor.connection.commit()

            return jsonify(
                {   
                    "code": 201,
                    "message": "Listing deleted successfully!"
                }
            ), 201
        
        except Exception as e:
            import traceback
            print(f"Error deleting listing {id}: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            cursor.connection.rollback()
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "id": id,
                        "error": str(e)
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