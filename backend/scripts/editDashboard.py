import os
import pytz
import s3Images
from flask import Blueprint, g, request, jsonify
from datetime import datetime

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

# -----------------------------------------------------------------------------------------
# [POST] Edit Top 3 Category
# - Update user profile with new details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/editTop3', methods=['POST'])
def editDetails():
    conn = g.db
    data = request.get_json()
    userID = data['userID']
    cursor = conn.cursor()
    try:
        selectedGrails = data['selectedGrails']
        cursor.execute("UPDATE users SET \"grails\" = %s WHERE id = %s", (selectedGrails, userID))
        selectedUpAndComing = data['selectedUpAndComing']
        cursor.execute("UPDATE users SET \"upAndComing\" = %s WHERE id = %s", (selectedUpAndComing, userID))
        selectedGOATs = data['selectedGOATs']
        cursor.execute("UPDATE users SET \"goats\" = %s WHERE id = %s", (selectedGOATs, userID))
        
        conn.commit()
        return jsonify(
            {   
                "code": 201,
                "data": {
                    "userID": userID,
                    "grails": selectedGrails,
                    "upAndComing": selectedUpAndComing,
                    "goats": selectedGOATs
                }
            }
        ), 201

    except Exception as e:
        conn.rollback()
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": {
                    "userID": userID,
                    "grails": data['selectedGrails'],
                    "upAndComing": data['selectedUpAndComing'],
                    "goats": data['selectedGOATs']
                },
                "message": "An error occurred updating the image or drink choice."
            }
        ), 500
    
    finally:
        cursor.close()