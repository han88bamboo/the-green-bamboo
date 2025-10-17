# Files which adds or deducts points
# club.py / createReview.py / deleteReview.py / editProducerProfile.py / editVenueProfile.py


# Routes: 
#   [pointSystemRules] 
#   /getPointSystemRules (GET), 
#   /createPointSystemRule (POST), 
#   /updatePointSystemRule/<id> (PUT), 
#   /deletePointSystemRule/<id> (DELETE)
# 
#   [pointsRecorder]
#   /getPointsForUser/<id>/<userType> (GET), 
#   /createPointsForUser (POST)
# -----------------------------------------------------------------------------------------

import os
from flask import Blueprint, g, jsonify, request
from scripts import pointsHelperFunc, badge_helpers
from psycopg2.extras import RealDictCursor # ADDED BY SMU GROUP 3

# Import the database manager for connection pooling
from app import db_manager



file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)


# -----------------------------------------------------------------------------------------
# [GET] /getPointSystemRules
@blueprint.route('/getPointSystemRules', methods=['GET'])
def getPointSystemRules():

    with db_manager.get_cursor() as cursor:
        cursor.execute('SELECT * FROM "pointSystemRules"')
        rules = cursor.fetchall()

        if not rules:
            return jsonify({"message": "No point system rules found"}), 404

        return jsonify(rules), 200


# -----------------------------------------------------------------------------------------
# [POST] /createPointSystemRule
@blueprint.route('/createPointSystemRule', methods=['POST'])
def createPointSystemRule():

    data = request.json

    # Check if all required fields are present
    if 'rule_name' not in data or 'rule_desc' not in data or 'rule_category' not in data or 'proof_points' not in data:
        return jsonify({"message": "Missing required fields"}), 400
    
    # Check if user is admin
    if data['userType'] != 'admin':
        return jsonify({"message": "Unauthorized"}), 401
    
    try:
        with db_manager.get_cursor() as cursor:
            # Check if rule already exists (rule_name)
            cursor.execute('SELECT * FROM "pointSystemRules" WHERE "ruleName" ILIKE %s', (data['rule_name'],))

            if cursor.fetchone():
                return jsonify({"message": "Point system rule already exists"}), 409
            
            # Create point system rule
            cursor.execute('INSERT INTO "pointSystemRules" ("ruleName", "ruleDesc", "ruleCategory", "proofPoints") VALUES (%s, %s, %s, %s)', (data['rule_name'], data['rule_desc'], data['rule_category'], data['proof_points']))

        return jsonify({"message": "Point system rule created"}), 201
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500


# -----------------------------------------------------------------------------------------
# [PUT] /updatePointSystemRule/<id>
@blueprint.route('/updatePointSystemRule', methods=['PUT'])
def updatePointSystemRule():

    data = request.json

    # Check if all required fields are present
    if 'ruleId' not in data or 'rule_name' not in data or 'rule_desc' not in data or 'rule_category' not in data or 'proof_points' not in data:
        return jsonify({"message": "Missing required fields"}), 400
    
    # Check if user is admin
    if data['userType'] != 'admin':
        return jsonify({"message": "Unauthorized"}), 401
    
    try:
        with db_manager.get_cursor() as cursor:
            # Check if rule exists
            cursor.execute('SELECT * FROM "pointSystemRules" WHERE id = %s', (data['ruleId'],))

            if not cursor.fetchone():
                return jsonify({"message": "Point system rule not found"}), 404
            
            # Update point system rule
            cursor.execute('UPDATE "pointSystemRules" SET "ruleName" = %s, "ruleDesc" = %s, "ruleCategory" = %s, "proofPoints" = %s WHERE id = %s', (data['rule_name'], data['rule_desc'], data['rule_category'], data['proof_points'], data['ruleId']))

        return jsonify({"message": "Point system rule updated"}), 201
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500


# -----------------------------------------------------------------------------------------
# [DELETE] /deletePointSystemRule/<id>
@blueprint.route('/deletePointSystemRule', methods=['DELETE'])
def deletePointSystemRule():

    data = request.json

    if 'ruleId' not in data:
        return jsonify({"message": "Missing required fields"}), 400

    # Check if user is admin
    if data['userType'] != 'admin':
        return jsonify({"message": "Unauthorized"}), 401
    
    with db_manager.get_cursor() as cursor:
        # Check if rule exists
        cursor.execute('SELECT * FROM "pointSystemRules" WHERE id = %s', (data['ruleId'],))

        if not cursor.fetchone():
            return jsonify({"message": "Point system rule not found"}), 404
        
        # Delete point system rule
        cursor.execute('DELETE FROM "pointSystemRules" WHERE id = %s', (data['ruleId'],))

    return jsonify({"message": "Point system rule deleted"}), 200


# -----------------------------------------------------------------------------------------
# [GET] /getPointsForUser/<id>/<userType>
@blueprint.route('/getPointsForUser/<id>/<userType>', methods=['GET'])
def getPointsForUser(id, userType):

    with db_manager.get_cursor() as cursor:
        # Get points for user
        cursor.execute('SELECT * FROM "pointsRecorder" WHERE "userID" = %s AND "userType" = %s', (id, userType,))
        user_points = cursor.fetchone()

        if not user_points:
            return jsonify({"message": "User points not found"}), 404

        
        # Get total points for user
        total_points = pointsHelperFunc.get_current_proof_points(id)

        # Get max points
        cursor.execute('SELECT "proofPoints" FROM "pointSystemRules" WHERE id = 1')
        max_points = cursor.fetchone()['proofPoints']

    return jsonify({
        'totalPoints': total_points,
        'maxPoints': max_points,
    }), 200


# -----------------------------------------------------------------------------------------
# [POST] /createPointsForUser
@blueprint.route('/createPointsForUser', methods=['POST'])
def createPointsForUser():

    data = request.json

    # Check if all required fields are present
    if 'user_id' not in data or 'user_type' not in data:
        return jsonify({"message": "Missing required fields, user id and user type must be provided."}), 400
        

    try: 
        with db_manager.get_cursor() as cursor:
            # Check if user already has points
            cursor.execute('SELECT * FROM "pointsRecorder" WHERE "userID" = %s AND "userType" = %s', (data['user_id'], data['user_type'],))

            if cursor.fetchone():
                return jsonify({"message": "User already has points"}), 409
            
            # Create points for user
            cursor.execute('INSERT INTO "pointsRecorder" ("userID", "userType", "points") VALUES (%s, %s, 0)', (data['user_id'], data['user_type'],))

        return jsonify({"message": "User points created"}), 201
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500

    
