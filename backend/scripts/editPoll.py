from flask import Blueprint, request, jsonify, g
from psycopg2.extras import RealDictCursor
import traceback
from datetime import datetime

blueprint = Blueprint('editPoll', __name__)

@blueprint.route("/createPoll", methods=['POST'])
def createPoll():
    """
    Create a new poll with questions and options
    
    Expected request body:
    {
        "creatorId": 123,
        "creatorType": "venue",
        "title": "Poll Title",
        "questionText": "What is your question?",
        "questionType": "multiple_choice_single_selection",
        "isVisible": true,
        "expiresAt": "2024-12-31T23:59:59" or null,
        "orderIndex": 0,
        "options": [
            {"optionText": "Option 1", "optionOrder": 0},
            {"optionText": "Option 2", "optionOrder": 1}
        ]
    }
    """
    try:
        conn = g.db
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['creatorId', 'creatorType', 'title', 'questionText', 'questionType']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    "code": 400,
                    "message": f"Missing required field: {field}"
                }), 400
        
        # Validate creatorType
        if data['creatorType'] not in ['user', 'venue', 'producer']:
            return jsonify({
                "code": 400,
                "message": "Invalid creatorType. Must be 'user', 'venue', or 'producer'"
            }), 400
        
        # Validate questionType
        valid_question_types = ['multiple_choice_single_selection', 'multiple_choice_multi_selection', 'rating_scale']
        if data['questionType'] not in valid_question_types:
            return jsonify({
                "code": 400,
                "message": f"Invalid questionType. Must be one of: {', '.join(valid_question_types)}"
            }), 400
        
        # Validate options for multiple choice questions
        if data['questionType'].startswith('multiple_choice'):
            if 'options' not in data or not data['options'] or len(data['options']) < 2:
                return jsonify({
                    "code": 400,
                    "message": "Multiple choice questions must have at least 2 options"
                }), 400
            
            # Validate each option
            for i, option in enumerate(data['options']):
                if 'optionText' not in option or not option['optionText'].strip():
                    return jsonify({
                        "code": 400,
                        "message": f"Option {i + 1} must have valid text"
                    }), 400
        
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            # Get the next orderIndex for this creator
            if 'orderIndex' not in data:
                cursor.execute("""
                    SELECT COALESCE(MAX("orderIndex"), -1) + 1 as next_order
                    FROM "pollQuestions" 
                    WHERE "creatorId" = %s AND "creatorType" = %s
                """, (data['creatorId'], data['creatorType']))
                
                result = cursor.fetchone()
                next_order_index = result['next_order'] if result else 0
            else:
                next_order_index = data['orderIndex']
            
            # Insert the poll question
            cursor.execute("""
                INSERT INTO "pollQuestions" (
                    "creatorId", "creatorType", "title", "questionText", 
                    "questionType", "isActive", "isVisible", "expiresAt", "orderIndex"
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING "id", "createdAt", "updatedAt"
            """, (
                data['creatorId'],
                data['creatorType'],
                data['title'].strip(),
                data['questionText'].strip(),
                data['questionType'],
                True,  # isActive defaults to True
                data.get('isVisible', True),
                data.get('expiresAt'),
                next_order_index
            ))
            
            poll_result = cursor.fetchone()
            poll_id = poll_result['id']
            created_at = poll_result['createdAt']
            updated_at = poll_result['updatedAt']
            
            # Insert options for multiple choice questions
            options_data = []
            if data['questionType'].startswith('multiple_choice') and 'options' in data:
                for option in data['options']:
                    cursor.execute("""
                        INSERT INTO "pollOptions" ("pollId", "optionText", "optionOrder")
                        VALUES (%s, %s, %s)
                        RETURNING "id"
                    """, (
                        poll_id,
                        option['optionText'].strip(),
                        option['optionOrder']
                    ))
                    
                    option_result = cursor.fetchone()
                    options_data.append({
                        "id": option_result['id'],
                        "pollId": poll_id,
                        "optionText": option['optionText'].strip(),
                        "optionOrder": option['optionOrder']
                    })
            
            # Commit the transaction
            conn.commit()
            
            # Return the created poll data
            poll_data = {
                "id": poll_id,
                "creatorId": data['creatorId'],
                "creatorType": data['creatorType'],
                "title": data['title'].strip(),
                "questionText": data['questionText'].strip(),
                "questionType": data['questionType'],
                "isActive": True,
                "isVisible": data.get('isVisible', True),
                "expiresAt": data.get('expiresAt'),
                "createdAt": created_at.isoformat() if created_at else None,
                "updatedAt": updated_at.isoformat() if updated_at else None,
                "orderIndex": next_order_index,
                "options": options_data
            }
            
            return jsonify({
                "code": 200,
                "message": "Poll created successfully",
                "data": poll_data
            })
    
    except Exception as e:
        # Rollback in case of error
        if 'conn' in locals():
            conn.rollback()
        
        print(f"Error creating poll: {str(e)}")
        return jsonify({
            "code": 500,
            "message": "Internal server error while creating poll"
        }), 500


@blueprint.route("/updatePollVisibility/<int:poll_id>", methods=['PUT'])
def updatePollVisibility(poll_id):
    """
    Update the visibility of a poll
    
    Expected request body:
    {
        "isVisible": true/false
    }
    """
    try:
        conn = g.db
        data = request.get_json()
        
        if 'isVisible' not in data:
            return jsonify({
                "code": 400,
                "message": "Missing required field: isVisible"
            }), 400
        
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            # Update the poll visibility
            cursor.execute("""
                UPDATE "pollQuestions" 
                SET "isVisible" = %s, "updatedAt" = CURRENT_TIMESTAMP
                WHERE "id" = %s
                RETURNING "id", "isVisible", "updatedAt"
            """, (data['isVisible'], poll_id))
            
            result = cursor.fetchone()
            
            if not result:
                return jsonify({
                    "code": 404,
                    "message": "Poll not found"
                }), 404
            
            conn.commit()
            
            return jsonify({
                "code": 200,
                "message": "Poll visibility updated successfully",
                "data": {
                    "id": result['id'],
                    "isVisible": result['isVisible'],
                    "updatedAt": result['updatedAt'].isoformat() if result['updatedAt'] else None
                }
            })
    
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        
        print(f"Error updating poll visibility: {str(e)}")
        return jsonify({
            "code": 500,
            "message": "Internal server error while updating poll visibility"
        }), 500


@blueprint.route("/deletePoll/<int:poll_id>", methods=['DELETE'])
def deletePoll(poll_id):
    """
    Delete a poll and all its associated data
    
    This will cascade delete:
    - Poll options (via CASCADE)
    - Poll responses (via CASCADE)
    """
    try:
        conn = g.db
        
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            # Check if poll exists before deletion
            cursor.execute("""
                SELECT "id", "title" FROM "pollQuestions" WHERE "id" = %s
            """, (poll_id,))
            
            poll = cursor.fetchone()
            
            if not poll:
                return jsonify({
                    "code": 404,
                    "message": "Poll not found"
                }), 404
            
            # Delete the poll (CASCADE will handle options and responses)
            cursor.execute("""
                DELETE FROM "pollQuestions" WHERE "id" = %s
            """, (poll_id,))
            
            conn.commit()
            
            return jsonify({
                "code": 200,
                "message": f"Poll '{poll['title']}' deleted successfully",
                "data": {
                    "deletedPollId": poll_id
                }
            })
    
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        
        print(f"Error deleting poll: {str(e)}")
        return jsonify({
            "code": 500,
            "message": "Internal server error while deleting poll"
        }), 500


@blueprint.route("/updatePollStatus/<int:poll_id>", methods=['PUT'])
def updatePollStatus(poll_id):
    """
    Update the active status of a poll (open/close poll)
    
    Expected request body:
    {
        "isActive": true/false
    }
    """
    try:
        conn = g.db
        data = request.get_json()
        
        if 'isActive' not in data:
            return jsonify({
                "code": 400,
                "message": "Missing required field: isActive"
            }), 400
        
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            # Update the poll status
            cursor.execute("""
                UPDATE "pollQuestions" 
                SET "isActive" = %s, "updatedAt" = CURRENT_TIMESTAMP
                WHERE "id" = %s
                RETURNING "id", "isActive", "updatedAt"
            """, (data['isActive'], poll_id))
            
            result = cursor.fetchone()
            
            if not result:
                return jsonify({
                    "code": 404,
                    "message": "Poll not found"
                }), 404
            
            conn.commit()
            
            return jsonify({
                "code": 200,
                "message": f"Poll {'activated' if data['isActive'] else 'deactivated'} successfully",
                "data": {
                    "id": result['id'],
                    "isActive": result['isActive'],
                    "updatedAt": result['updatedAt'].isoformat() if result['updatedAt'] else None
                }
            })
    
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        
        print(f"Error updating poll status: {str(e)}")
        return jsonify({
            "code": 500,
            "message": "Internal server error while updating poll status"
        }), 500