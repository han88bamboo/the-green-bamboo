# Port: 5000
# Routes: /editTop3 (POST)
# -----------------------------------------------------------------------------------------

import os
from flask import Blueprint, g, jsonify, request
from psycopg2.extras import RealDictCursor

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

# [POST] Update user's Grails, Up & Coming, and GOATs selections
@blueprint.route("/editTop3", methods=['POST'])
def editTop3():
    """
    Update a user's Grails, Up & Coming, and GOATs drink selections.
    
    Request body should include:
    - userID: User ID
    - selectedGrails: Array of drink names for Grails section
    - selectedUpAndComing: Array of drink names for Up & Coming section
    - selectedGOATs: Array of drink names for GOATs section
    
    Returns:
    - 201: User's selections updated successfully
    - 400: Missing user ID
    - 404: User not found
    - 500: Server error
    """
    conn = g.db
    
    try:
        data = request.json
        user_id = data.get('userID')
        selected_grails = data.get('selectedGrails', [])
        selected_up_and_coming = data.get('selectedUpAndComing', [])
        selected_goats = data.get('selectedGOATs', [])
        
        if not user_id:
            return jsonify({"code": 400, "message": "User ID is required"}), 400
        
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            # Check if user exists
            cursor.execute('SELECT * FROM "users" WHERE "id" = %s', (user_id,))
            user = cursor.fetchone()
            
            if not user:
                return jsonify({"code": 404, "message": "User not found"}), 404
            
            # Update the user's selections
            cursor.execute('''
                UPDATE "users" 
                SET "grails" = %s, 
                    "upAndComing" = %s, 
                    "goats" = %s
                WHERE "id" = %s
            ''', (selected_grails, selected_up_and_coming, selected_goats, user_id))
            
            conn.commit()
            
            return jsonify({"code": 201, "message": "User selections updated successfully"}), 201
            
    except Exception as e:
        print(str(e))
        return jsonify({"code": 500, "message": "An error occurred updating user selections."}), 500