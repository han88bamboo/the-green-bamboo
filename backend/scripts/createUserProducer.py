# Port: 5049
# Routes: /createUserProducer (POST)
# -----------------------------------------------------------------------------------------

from flask import Blueprint, g, request, jsonify
from datetime import datetime
from psycopg2 import sql
import os
from dotenv import load_dotenv

# Load env variables
load_dotenv()

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

# -----------------------------------------------------------------------------------------
# [POST] Creates a Producer Account from a User Submission
# - Inserts entry into the "producers" collection
# - Also initializes related tables like producersProfileViews and producerReviews
# - Possible return codes: 201 (Created), 400 (Duplicate Detected), 500 (Error during creation)
@blueprint.route("/createUserProducer", methods=['POST'])
def create_user_producer():
    """Create a new producer account from user submission"""
    try:
        # Get data from request
        data = request.json

        # Check required fields
        if not data.get('producerName') or not data.get('producerDesc') or not data.get('originCountry'):
            return jsonify({"message": "Missing required fields"}), 400

        # Validate input
        producer_name = data.get('producerName')
        producer_desc = data.get('producerDesc')
        origin_country = data.get('originCountry')
        is_independent_bottler = data.get('isIndependentBottler', False)

        # Check if producer already exists
        cursor = g.db.cursor()
        cursor.execute('SELECT "id" FROM "producers" WHERE LOWER("producerName") = LOWER(%s)', (producer_name,))
        existing_producer = cursor.fetchone()
        
        if existing_producer:
            cursor.close()
            return jsonify({"message": "A producer with this name already exists"}), 400

        # Begin transaction to ensure consistency across all related tables
        try:
            # Insert into producers table
            cursor.execute("""
                INSERT INTO "producers" (
                    "producerName", 
                    "producerDesc", 
                    "originCountry", 
                    "isIndependentBottler", 
                    "mainDrinks", 
                    "photo", 
                    "statusOB", 
                    "username", 
                    "producerLink", 
                    "stripeCustomerId", 
                    "location",
                    "claimStatus"
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING "id"
                """, 
                (
                    producer_name,
                    producer_desc,
                    origin_country,
                    is_independent_bottler,
                    '{}',  # mainDrinks as empty array
                    '',    # photo as empty string
                    '',    # statusOB as empty string
                    producer_name,  # username set to producerName
                    '',    # producerLink as empty string
                    None,  # stripeCustomerId as null
                    'Location not specified',  # default location
                    False  # not claimed initially
                )
            )
            
            # Get the new producer's ID
            result = cursor.fetchone()
            if result is None:
                raise Exception("Failed to retrieve producer ID from database")
            producer_id = result['id']
            
            # Initialize producersProfileViews
            cursor.execute("""
                INSERT INTO "producersProfileViews" ("producerId", "date", "count")
                VALUES (%s, CURRENT_DATE, 0)
                """,
                (producer_id,)
            )
            
            # Initialize producerReviews
            cursor.execute("""
                INSERT INTO "producerReviews" ("producerID")
                VALUES (%s)
                """,
                (producer_id,)
            )
            
            # Commit the transaction
            g.db.commit()
            
            # Return success with new producer ID
            return jsonify({
                "message": "Producer created successfully",
                "id": producer_id,
                "name": producer_name
            }), 201
            
        except Exception as e:
            # Rollback in case of error
            g.db.rollback()
            raise e
            
    except Exception as e:
        import traceback
        print(f"Error creating producer: {str(e)}")
        print(f"Error type: {type(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({"message": f"Error creating producer: {str(e)}"}), 500
    finally:
        cursor.close()
