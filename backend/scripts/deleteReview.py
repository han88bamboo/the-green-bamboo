# Port: 5023
# Routes: /deleteReview/<id> (DELETE)
# -----------------------------------------------------------------------------------------

import os
import s3Images
import json
from bson import json_util
from flask import Blueprint, g, request, jsonify
from bson.objectid import ObjectId


file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

def parse_json(data):
    return json.loads(json_util.dumps(data))

# -----------------------------------------------------------------------------------------
# [DELETE] Deletes a review
# - Delete entry with specified id from the "reviews" collection.
# - Possible return codes: 201 (Deleted), 400 (Review doesn't exist), 500 (Error during deletion)
@blueprint.route("/deleteReview/<id>", methods= ['DELETE'])
def deleteReview(id):
    db = g.db

    # Find the review entry with the specified id
    existingReview = db.reviews.find_one({"_id": ObjectId(id)})
    if(existingReview == None):
        return jsonify(
            {   
                "code": 400,
                "data": {
                    "id": id
                },
                "message": "Review doesn't exist."
            }
        ), 400
    

    # Delete the review entry with the specified id
    try:
        if(existingReview['photo']):
            s3Images.deleteImageFromS3(existingReview['photo'])
        deleteResult = db.reviews.delete_one({"_id": ObjectId(id)})

        return jsonify( 
            {   
                "code": 200,
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
                "message": "An error occurred deleting the listing."
            }
        ), 500
