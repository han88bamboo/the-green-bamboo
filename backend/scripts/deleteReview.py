# Port: 5023
# Routes: /deleteReview/<id> (DELETE)
# -----------------------------------------------------------------------------------------

# [OLD] TO BE DELETED FOR POSTGRES:
# ------------------------------------------------------


# ======================================================

# [NEW] TO BE ADDED FOR POSTGRES:
# ------------------------------------------------------


# ======================================================
import os
import s3Images
import json
from flask import Blueprint, g, request, jsonify
# [OLD] TO BE DELETED FOR POSTGRES:
# ------------------------------------------------------
from bson import json_util
from bson.objectid import ObjectId
# ======================================================

# [NEW] TO BE ADDED FOR POSTGRES:
# ------------------------------------------------------
# import psycopg2
# from psycopg2.extras import RealDictCursor
# ======================================================


file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)


# [OLD] TO BE DELETED FOR POSTGRES:
# ------------------------------------------------------
def parse_json(data):
    return json.loads(json_util.dumps(data))
# ======================================================

# -----------------------------------------------------------------------------------------
# [DELETE] Deletes a review
# - Delete entry with specified id from the "reviews" collection.
# - Possible return codes: 201 (Deleted), 400 (Review doesn't exist), 500 (Error during deletion)


@blueprint.route("/deleteReview/<id>", methods= ['DELETE'])
def deleteReview(id):
    # [OLD] TO BE DELETED FOR POSTGRES:
    # ------------------------------------------------------
    db = g.db
    # ======================================================
    
    # [NEW] TO BE ADDED FOR POSTGRES:
    # ------------------------------------------------------
    # conn = g.db  # Get the DB connection from g
    # cur = conn.cursor()
    # ======================================================


# Find the review entry with the specified id
    # [OLD] TO BE DELETED FOR POSTGRES:
    # ------------------------------------------------------
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
    # ======================================================

    # [NEW] TO BE ADDED FOR POSTGRES:
    # ------------------------------------------------------
    
    # cur.execute("SELECT * FROM reviews WHERE id = %s", (id,))
    # existingReview = cur.fetchone()

    # if existingReview is None:
    #     return jsonify(
    #         {   
    #             "code": 400,
    #             "data": {
    #                 "id": id
    #             },
    #             "message": "Review doesn't exist."
    #         }
    #     ), 400

    # ======================================================

# Delete the review entry with the specified id
    # [OLD] TO BE DELETED FOR POSTGRES:
    # ------------------------------------------------------
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
    # ======================================================

    # [NEW] TO BE ADDED FOR POSTGRES:
    # ------------------------------------------------------
    # try:
    #     if(existingReview['photo']):
    #         s3Images.deleteImageFromS3(existingReview['photo'])
    #     cur.execute("DELETE FROM reviews WHERE id = %s", (id,))
    #     g.db.commit()  # Commit the transaction to make sure the deletion takes effect


    #     return jsonify( 
    #         {   
    #             "code": 200,
    #             "data": id
    #         }
    #     ), 201
    # except Exception as e:
    #     print(str(e))
    #     return jsonify(
    #         {
    #             "code": 500,
    #             "data": {
    #                 "id": id
    #             },
    #             "message": "An error occurred deleting the listing."
    #         }
    #     ), 500
    # ======================================================

