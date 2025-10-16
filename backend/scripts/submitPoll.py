"""
Poll Response Submission Endpoint
Handles user responses to polls for all three question types:
1. multiple_choice_single_selection
2. multiple_choice_multi_selection  
3. rating_scale
"""

from flask import request, jsonify, g, Blueprint
from psycopg2.extras import RealDictCursor
import traceback
from datetime import datetime

# Import the database manager for connection pooling
from app import db_manager

# Create a Blueprint for poll submission
blueprint = Blueprint('submitPoll', __name__)

@blueprint.route('/submitResponse', methods=['POST'])
def submit_poll_response():
    """Submit a user's response to a poll"""
    
    try:
        # Get request data
        data = request.get_json()
        
        # Validate required fields
        if not data or 'pollId' not in data or 'respondentId' not in data:
            return jsonify({
                "code": 400,
                "message": "Missing required fields: pollId and respondentId are required."
            }), 400
        
        poll_id = data.get('pollId')
        respondent_id = data.get('respondentId')
        selected_option_ids = data.get('selectedOptionIds')
        rating_value = data.get('ratingValue')
        
        # Validate that exactly one of selectedOptionIds or ratingValue is provided
        if (selected_option_ids is None and rating_value is None) or \
           (selected_option_ids is not None and rating_value is not None):
            return jsonify({
                "code": 400,
                "message": "Either selectedOptionIds or ratingValue must be provided, but not both."
            }), 400
        
        with db_manager.get_cursor() as cursor:
            # First, get the poll details to validate the question type and status
            cursor.execute('''
                SELECT 
                    "id", 
                    "questionType", 
                    "isActive", 
                    "isVisible",
                    "expiresAt",
                    "creatorId",
                    "creatorType"
                FROM "pollQuestions" 
                WHERE "id" = %s
            ''', (poll_id,))
            
            poll = cursor.fetchone()
            
            if not poll:
                return jsonify({
                    "code": 404,
                    "message": "Poll not found."
                }), 404
            
            # Check if poll is active and visible
            if not poll['isActive']:
                return jsonify({
                    "code": 400,
                    "message": "This poll is no longer accepting responses."
                }), 400
            
            if not poll['isVisible']:
                return jsonify({
                    "code": 400,
                    "message": "This poll is not currently visible."
                }), 400
            
            # Check if poll has expired
            if poll['expiresAt'] and poll['expiresAt'] <= datetime.now():
                return jsonify({
                    "code": 400,
                    "message": "This poll has expired and is no longer accepting responses."
                }), 400
            
            # Validate the respondent exists and is a regular user
            cursor.execute('SELECT "id" FROM "users" WHERE "id" = %s', (respondent_id,))
            user = cursor.fetchone()
            
            if not user:
                return jsonify({
                    "code": 404,
                    "message": "User not found."
                }), 404
            
            # Check if user has already responded to this poll
            cursor.execute('''
                SELECT "id" FROM "pollResponses" 
                WHERE "pollId" = %s AND "respondentId" = %s
            ''', (poll_id, respondent_id))
            
            existing_response = cursor.fetchone()
            
            if existing_response:
                return jsonify({
                    "code": 400,
                    "message": "You have already responded to this poll."
                }), 400
            
            # Validate response data based on question type
            if poll['questionType'] in ['multiple_choice_single_selection', 'multiple_choice_multi_selection']:
                # Multiple choice questions require selectedOptionIds
                if selected_option_ids is None or not isinstance(selected_option_ids, list) or len(selected_option_ids) == 0:
                    return jsonify({
                        "code": 400,
                        "message": "selectedOptionIds must be a non-empty array for multiple choice questions."
                    }), 400
                
                # For single selection, ensure only one option is selected
                if poll['questionType'] == 'multiple_choice_single_selection' and len(selected_option_ids) != 1:
                    return jsonify({
                        "code": 400,
                        "message": "Single selection questions must have exactly one option selected."
                    }), 400
                
                # Validate that all selected option IDs exist for this poll
                format_strings = ','.join(['%s'] * len(selected_option_ids))
                cursor.execute(f'''
                    SELECT "id" FROM "pollOptions" 
                    WHERE "pollId" = %s AND "id" IN ({format_strings})
                ''', [poll_id] + selected_option_ids)
                
                valid_options = cursor.fetchall()
                
                if len(valid_options) != len(selected_option_ids):
                    return jsonify({
                        "code": 400,
                        "message": "One or more selected options are invalid for this poll."
                    }), 400
            
            elif poll['questionType'] == 'rating_scale':
                # Rating scale questions require ratingValue
                if rating_value is None:
                    return jsonify({
                        "code": 400,
                        "message": "ratingValue is required for rating scale questions."
                    }), 400
                
            else:
                return jsonify({
                    "code": 400,
                    "message": f"Unsupported question type: {poll['questionType']}"
                }), 400
            
            # Insert the poll response
            cursor.execute('''
                INSERT INTO "pollResponses" 
                ("pollId", "respondentId", "selectedOptionIds", "ratingValue")
                VALUES (%s, %s, %s, %s)
                RETURNING "id"
            ''', (poll_id, respondent_id, selected_option_ids, rating_value))
            
            response_record = cursor.fetchone()
            response_id = response_record['id']
            
            # Prepare response data
            response_data = {
                "id": response_id,
                "pollId": poll_id,
                "respondentId": respondent_id,
                "selectedOptionIds": selected_option_ids,
                "ratingValue": rating_value,
                "createdAt": datetime.now().isoformat()
            }
            
            return jsonify({
                "code": 200,
                "message": "Poll response submitted successfully.",
                "data": response_data
            }), 200
        
    except Exception as e:
        print("Submit poll response error:", str(e))
        print("Traceback:", traceback.format_exc())
        
        return jsonify({
            "code": 500,
            "message": "An error occurred while submitting the poll response."
        }), 500


