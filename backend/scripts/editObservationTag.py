# Port: 5051
# Routes: /updateObservationTag (PUT)
# -----------------------------------------------------------------------------------------

import os
from flask import Blueprint, g, request, jsonify
from bson.objectid import ObjectId

# Import the database manager for connection pooling
from app import db_manager

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

# -----------------------------------------------------------------------------------------
    
# [PUT] Update review
# - Update review with review metrics
# - Possible return codes: 201 (Updated), 400(Observation tag not found), 500 (Error during update)
@blueprint.route('/updateObservationTag', methods=['PUT'])
def updateObservationTag():
    with db_manager.get_cursor() as cursor:
        data = request.get_json()
        # for loop for each observation tag and update
        updates = []
        for elem in data:

            # 🚨 Converting MongoDB find_one to PostgreSQL SELECT
            cursor.execute('SELECT * FROM "observationTags" WHERE "id" = %s', (elem["_id"]["$oid"],))
            existingObservationTag = cursor.fetchone()

            if(existingObservationTag == None):
                return jsonify(
                    {   
                        "code": 400,
                        "data": {
                            "observationTag": elem['observationTag']
                        },
                        "message": "Observation Tag does not exist."
                    }
                ), 400

            tag_key, tag_value = list(elem.items())[1]
            # 🚨 Converting MongoDB update format to PostgreSQL UPDATE
            updates.append({"id": elem["_id"]["$oid"], "column": tag_key, "value": tag_value})


        try: 
            for update in updates:
                # 🚨 Converting MongoDB update_many to PostgreSQL UPDATE
                update_query = f'UPDATE "observationTags" SET "{update["column"]}" = %s WHERE "id" = %s'
                cursor.execute(update_query, (update["value"], update["id"]))
            return jsonify(
                {   
                    "code": 201,
                    "data": elem['observationTag']
                }
            ), 201
        except Exception as e:
            print(str(e))
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "data": elem['observationTag']
                    },
                    "message": "An error occurred updating the observation tags."
                }
            ), 500
