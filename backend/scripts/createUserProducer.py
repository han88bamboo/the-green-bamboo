# Port: 5049
# Routes: /createUserProducer (POST)
# -----------------------------------------------------------------------------------------

from flask import Blueprint, g, request, jsonify
from datetime import datetime
from psycopg2 import sql
import os
import re
import unicodedata
from dotenv import load_dotenv

# Load env variables
load_dotenv()

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

# -----------------------------------------------------------------------------------------
# Helper function to sanitize username by removing non-English characters
def sanitize_username(producer_name):
    """
    Sanitize producer name for use as username by:
    1. Removing Chinese/Japanese characters (CJK ideographs)
    2. Removing accented characters (converting to ASCII equivalents)
    3. Removing special characters except alphanumeric, spaces, hyphens, underscores
    4. Collapsing multiple spaces into single spaces
    5. Stripping leading/trailing whitespace
    
    WARNING: If the producer name contains ONLY Chinese/Japanese characters with no English letters
    (e.g., "山崎蒸留所"), the result will be the original unsanitized producer name. This means
    the username may contain special characters that could cause issues with authentication
    or URL handling.
    """
    if not producer_name:
        return ""
    
    # Step 1: Remove CJK (Chinese, Japanese, Korean) characters
    # Unicode ranges for CJK characters:
    # U+4E00-U+9FFF: CJK Unified Ideographs
    # U+3400-U+4DBF: CJK Extension A
    # U+20000-U+2A6DF: CJK Extension B
    # U+3040-U+309F: Hiragana
    # U+30A0-U+30FF: Katakana
    cjk_pattern = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\u3040-\u309f\u30a0-\u30ff]+')
    cleaned_name = cjk_pattern.sub('', producer_name)
    
    # Step 2: Convert accented characters to ASCII equivalents (NFD normalization)
    # This converts characters like Ā, Å, é, ñ to their base ASCII forms
    normalized = unicodedata.normalize('NFD', cleaned_name)
    ascii_name = ''.join(char for char in normalized if unicodedata.category(char) != 'Mn')
    
    # Step 3: Remove any remaining non-ASCII characters and special characters
    # Keep only alphanumeric, spaces, hyphens, and underscores
    sanitized = re.sub(r'[^a-zA-Z0-9\s\-_]', '', ascii_name)
    
    # Step 4: Collapse multiple spaces and strip whitespace
    sanitized = re.sub(r'\s+', ' ', sanitized).strip()
    
    # Step 5: If the result is empty (all characters were removed), use original producer name
    if not sanitized:
        return producer_name
    
    return sanitized

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

        # Sanitize the producer name for use as username
        sanitized_username = sanitize_username(producer_name)

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
                    sanitized_username,  # username set to sanitized producerName
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
