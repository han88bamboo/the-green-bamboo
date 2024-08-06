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
    db = g.db
    listing_id=ObjectId(id)
    updatedListing = request.get_json()
    updatedListing['producerID'] = ObjectId(updatedListing['producerID'])
    
    # Duplicate listing check: Reject if listing with the same bottle name already exists in the database
    updatedListingName = updatedListing["listingName"]
    existingBottle = db.listings.find_one({"listingName": updatedListingName})
    if(existingBottle != None):
        if(existingBottle["_id"] != listing_id):
            return jsonify(
                {   
                    "code": 410,
                    "data": {
                        "listingName": updatedListingName
                    },
                    "message": "Bottle already exists."
                }
            ), 410
        else:
            # delete the old image and upload new one
            try:
                if existingBottle['photo']:
                    s3Images.deleteImageFromS3(existingBottle['photo'])
                if updatedListing['photo']:
                    updatedListing['photo'] = s3Images.uploadBase64ImageToS3(updatedListing['photo'])

            except Exception as e:
                print(str(e))
                return jsonify(
                    {
                        "code": 450,
                        "data": {
                            "_id": id
                        },
                        "message": "An error occurred updating the listing."
                    }
                ), 450
    
    # Update the listing entry with the specified id
    # updatedBottle = data.listings(**updatedListing)
    # print(updatedBottle)
    try: 
        result = db.listings.update_one(
            {"_id": listing_id},
            # {"$set": data.asdict(updatedBottle)}
            {"$set": updatedListing}

        )

        if result.matched_count > 0:
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "_id": id
                    },
                    "message": "Listing updated successfully."
                }
            ), 200
        else:
            return jsonify(
                {
                    "code": 440,
                    "data": {
                        "_id":  id
                    },
                    "message": "Listing was not updated"
                }
            ), 440
        
    # If Id is invalid
    except InvalidId:
        return jsonify(
            {
                "code": 420,
                "data": {
                    "_id": id
                },
                "message": "Invalid listing ID."
            }
        ), 420
    
    # If listing does not work
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 450,
                "data": {
                    "_id": id
                },
                "message": "An error occurred updating the listing."
            }
        ), 450

# -----------------------------------------------------------------------------------------
# [DELETE] Deletes a listing
# - Delete entry with specified id from the "listings" collection
# - Possible return codes: 201 (Deleted), 400 (Listing doesn't exist), 500 (Error during deletion)
@blueprint.route("/deleteListing/<id>", methods=['DELETE'])
def deleteListing(id):
    db = g.db
        
    # Find the listing entry with the specified id
    existingListing = db.listings.find_one({"_id": ObjectId(id)})
    if(existingListing == None):
        return jsonify(
            {   
                "code": 400,
                "data": {
                    "id": id
                },
                "message": "Listing doesn't exist."
            }
        ), 400


    # Delete the listing entry with the specified id
    try: 
        # delete image from s3 bucket
        s3Images.deleteImageFromS3(existingListing['photo'])

        # delete listing
        result = db.listings.delete_one({"_id": ObjectId(id)})

        return jsonify(
            {   
                "code": 201,
                "message": "Listing deleted successfully!"
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