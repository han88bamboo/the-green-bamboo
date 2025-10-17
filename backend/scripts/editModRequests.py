# Port: 5101
# Routes: /submitModRequest (POST), /updateModRequest (POST)

# [OLD] TO BE DELETED FOR POSTGRES:
# ------------------------------------------------------
##
# ======================================================

# [NEW] TO BE ADDED FOR POSTGRES:
# ------------------------------------------------------
##
# ======================================================

# -----------------------------------------------------------------------------------------

import os
from flask import Blueprint, g, request, jsonify
# [OLD] TO BE DELETED FOR POSTGRES:
# ------------------------------------------------------
# from bson.objectid import ObjectId (REMOVED - not needed for PostgreSQL)
# ======================================================

# Import the database manager for connection pooling
from app import db_manager

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

# -----------------------------------------------------------------------------------------
# [POST] Submit mod request
# - Submit mod request with new details
# - Possible return codes: 201 (Updated), 500 (Error during update)

@blueprint.route('/submitModRequest', methods=['POST'])
def submitModRequest():
    data = request.get_json()
    print(data)
    userID = data['userID']
    drinkType = data['drinkType']
    modDesc = data['modDesc']

# [OLD] TO BE DELETED FOR POSTGRES:
# ------------------------------------------------------
    # try: 
    #     submitReq = db.modRequests.insert_one({
    #         'userID': ObjectId(userID),
    #         'drinkType': drinkType,
    #         'modDesc': modDesc, 
    #         'reviewStatus': True
    #     })

    #     return jsonify(
    #         {   
    #             "code": 201,
    #             "data": {
    #                 "userID": userID,
    #                 "drinkType": drinkType,
    #                 "modDesc": modDesc, 
    #                 "reviewStatus": True
    #             }
    #         }
    #     ), 201
# ======================================================    
# [NEW] TO BE ADDED FOR POSTGRES:
# ------------------------------------------------------
    try: 
        with db_manager.get_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO "modRequests" ("userID", "drinkType", "modDesc", "reviewStatus")
                VALUES (%s, %s, %s, %s)
                """,
                (userID, drinkType, modDesc, True)
            )

        return jsonify(
            {   
                "code": 201,
                "data": {
                    "userID": userID,
                    "drinkType": drinkType,
                    "modDesc": modDesc, 
                    "reviewStatus": True
                }
            }
        ), 201
# ======================================================

    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": {
                    "data": {
                        "userID": userID,
                        "drinkType": drinkType,
                        "modDesc": modDesc,
                        "reviewStatus": True
                    }
                },
                "message": "An error occurred updating the mod request."
            }
        ), 500
    
# -----------------------------------------------------------------------------------------
# [POST] Update mod request status
# - Update mod request with new details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/updateModRequest', methods=['POST'])
def updateModRequest():
    data = request.get_json()
    print(data)
    requestID = data['requestID']
    reviewStatus = data['reviewStatus']


# [OLD] TO BE DELETED FOR POSTGRES:
# ------------------------------------------------------
    # try: 
    #     updateReviewStatus = db.modRequests.update_one({'_id': ObjectId(requestID)}, {'$set': {'reviewStatus': reviewStatus}})
# ======================================================
# [NEW] TO BE ADDED FOR POSTGRES:
# ------------------------------------------------------
    try:
        with db_manager.get_cursor() as cursor:
            cursor.execute(
                """
                UPDATE "modRequests"
                SET "reviewStatus" = %s
                WHERE id = %s
                """,
                (reviewStatus, requestID)
            )

# ======================================================
        return jsonify(
            {   
                "code": 201,
                "data": {
                    "requestID": requestID,
                    "reviewStatus": reviewStatus
                }
            }
        ), 201
    
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": {
                    "data": {
                        "requestID": requestID,
                        "reviewStatus": reviewStatus
                    }
                },
                "message": "An error occurred updating the mod request."
            }
        ), 500
