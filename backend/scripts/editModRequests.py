# Port: 5101
# Routes: /submitModRequest (POST), /updateModRequest (POST)
# -----------------------------------------------------------------------------------------

import os
from flask import Blueprint, g, request, jsonify
from bson.objectid import ObjectId

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

# -----------------------------------------------------------------------------------------
# [POST] Submit mod request
# - Submit mod request with new details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/submitModRequest', methods=['POST'])
def submitModRequest():
    db = g.db
    data = request.get_json()
    print(data)
    userID = data['userID']
    drinkType = data['drinkType']
    modDesc = data['modDesc']

    try: 
        submitReq = db.modRequests.insert_one({
            'userID': ObjectId(userID),
            'drinkType': drinkType,
            'modDesc': modDesc, 
            'reviewStatus': True
        })

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
    db = g.db
    data = request.get_json()
    print(data)
    requestID = data['requestID']
    reviewStatus = data['reviewStatus']

    try: 
        updateReviewStatus = db.modRequests.update_one({'_id': ObjectId(requestID)}, {'$set': {'reviewStatus': reviewStatus}})

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
