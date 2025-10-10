# Port: 5031
# Routes: /createAccount (POST), /createAccountRequest (POST), /updateAccountRequest (POST), /createProducerAccount (POST), /createVenueAccount (POST)
# -----------------------------------------------------------------------------------------

import json
import data
import s3Images
import os
import re
import unicodedata

from scripts.mail import send_email, send_email_aws
from flask import Blueprint, g, request, jsonify
from datetime import datetime, timedelta
from dotenv import load_dotenv # ADDED BY SMU GROUP 3
import psycopg2 # ADDED BY SMU GROUP 3

import secrets

from psycopg2 import sql

# load env variables
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
# [POST] Creates an Account
# - Insert entry into the "users" collection. Follows reviews dataclass requirements.
# - Duplicate review check: If a user with the same username, reject the request
# - Possible return codes: 201 (Created), 400 (Duplicate Detected), 500 (Error during creation)
@blueprint.route("/createAccount", methods= ['POST'])
def createAccount():
    db_conn = g.db
    rawAccount = request.get_json()
    
    # Convert date strings to datetime objects
    rawAccount['joinDate'] = datetime.strptime(rawAccount['joinDate'], "%Y-%m-%dT%H:%M:%S.%fZ")
    rawAccount['birthday'] = datetime.strptime(rawAccount['birthday'], "%Y-%m-%d")
    
    rawUsername = rawAccount['username']
    
    # Check for existing account with the same username
    with db_conn.cursor() as cursor:
        # 1. First check users table
        cursor.execute('SELECT "id" FROM "users" WHERE LOWER("username") = LOWER(%s)', (rawUsername,))
        existingAccount = cursor.fetchone()
        
        if existingAccount is not None:
            return jsonify(
                {   
                    "code": 400,
                    "data": {
                        "userName": rawUsername
                    },
                    "message": "Username already exists (Code: users)."
                }
            ), 400
    
        # 2. Then check venues table
        cursor.execute('SELECT "id" FROM "venues" WHERE LOWER("username") = LOWER(%s)', (rawUsername,))
        existingVenue = cursor.fetchone()
        
        if existingVenue is not None:
            return jsonify(
                {   
                    "code": 400,
                    "data": {
                        "userName": rawUsername
                    },
                    "message": "Username already exists (Code: venues)."
                }
            ), 400

        # 3. Finally check producers table
        cursor.execute('SELECT "id" FROM "producers" WHERE LOWER("username") = LOWER(%s)', (rawUsername,))
        existingProducer = cursor.fetchone()
        
        if existingProducer is not None:
            return jsonify(
                {   
                    "code": 400,
                    "data": {
                        "userName": rawUsername
                    },
                    "message": "Username already exists (Code: producers)."
                }
            ), 400

        # Now check for duplicate emails
        rawEmail = rawAccount['email']
        
        # 1. Check if email exists in users table
        cursor.execute('SELECT * FROM "users" WHERE email = %s', (rawEmail,))
        existingUserEmail = cursor.fetchone()
        
        if existingUserEmail is not None:
            return jsonify(
                {   
                    "code": 400,
                    "data": {
                        "email": rawEmail
                    },
                    "message": "Email already exists in user accounts."
                }
            ), 400
        
        # 2. Check if email exists in accountRequests table
        cursor.execute('SELECT * FROM "accountRequests" WHERE email = %s', (rawEmail,))
        existingRequestEmail = cursor.fetchone()
        
        if existingRequestEmail is not None:
            return jsonify(
                {   
                    "code": 400,
                    "data": {
                        "email": rawEmail
                    },
                    "message": "This email has a pending account request."
                }
            ), 400

    # Handle photo upload if present
    if rawAccount['photo']:
        base64_string = re.sub(r'^data:image\/[a-zA-Z]+;base64,', '', rawAccount['photo'])
        rawAccount['photo'] = s3Images.uploadBase64ImageToS3(base64_string)

    # Prepare data for insertion
    columns = ['username', 'displayName', 'firstName', 'lastName', 'email', 'choiceDrinks', 'modType', 
               'photo', 'hashedPassword', 'joinDate', 'birthday', 'country', 'isAdmin']
    values = [rawAccount['username'], rawAccount['displayName'], rawAccount['firstName'], rawAccount['lastName'], 
              rawAccount['email'], rawAccount['choiceDrinks'], rawAccount['modType'], 
              rawAccount['photo'], rawAccount['hashedPassword'], rawAccount['joinDate'], 
              rawAccount['birthday'], rawAccount['country'], rawAccount['isAdmin']]
    
    insert_query = sql.SQL('INSERT INTO "users" ({}) VALUES ({}) RETURNING "id"').format(
        sql.SQL(', ').join(map(lambda col: sql.Identifier(col), columns)),
        sql.SQL(', ').join(sql.Placeholder() * len(columns))
    )
    
    try:
        with db_conn.cursor() as cursor:
            cursor.execute(insert_query, values)
            user_id = cursor.fetchone()['id']
            db_conn.commit()

        with db_conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO "usersDrinkLists" ("userId", "listName")
                VALUES (%s, %s)
                RETURNING "id"
            """, (user_id, "Drinks I Want To Try"))
            want_to_try_list_id = cursor.fetchone()["id"]

            cursor.execute("""
                INSERT INTO "usersDrinkLists" ("userId", "listName")
                VALUES (%s, %s)
                RETURNING "id"
            """, (user_id, "Drinks I Have Tried"))
            have_tried_list_id = cursor.fetchone()["id"]

        with db_conn.cursor() as cursor:
            for drink in rawAccount['drinkLists']['Drinks I Have Tried']['listItems']:
                cursor.execute("""
                    INSERT INTO "usersDrinkListItems" ("listId", "drinkId", "addedDate")
                    VALUES (%s, %s, NOW())
                """, (have_tried_list_id, drink["drinkId"]))
            db_conn.commit()

        # Create proof point record for the new user
        with db_conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO "pointsRecorder" ("userID", "userType", "currentPoints")
                VALUES (%s, %s, %s)""",
                (user_id, "user", 0))
            db_conn.commit()

        
        return jsonify(
            {   
                "code": 201,
                "data": {
                    "userName": rawUsername,
                    "userID": str(user_id)
                }
            }
        ), 201
    
    except Exception as e:
        db_conn.rollback()
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": {
                    "userName": rawUsername
                },
                "message": "An error occurred creating the account."
            }
        ), 500
    
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
# [POST] Creates a Business Account Request
# - Insert entry into the "accountRequests" collection. Follows reviews dataclass requirements.
# - Duplicate review check: If a user with the same username, reject the request
# - Possible return codes: 201 (Created), 400 (Duplicate Detected), 500 (Error during creation)
@blueprint.route("/createAccountRequest", methods= ['POST'])
def createAccountRequest():
    conn = g.db
    cur = conn.cursor()
    rawAccount = request.get_json()

    rawEmail = rawAccount['email']
    rawAccount['joinDate'] = datetime.strptime(rawAccount['joinDate'], "%Y-%m-%dT%H:%M:%S.%fZ")

    try:
        # Check if email already exists in accountRequests table
        cur.execute('SELECT * FROM "accountRequests" WHERE email = %s', (rawEmail,))
        existingAccount = cur.fetchone()

        if existingAccount is not None:
            return jsonify(
                {   
                    "code": 400,
                    "data": {
                        "userName": rawEmail
                    },
                    "message": "Request already exists."
                }
            ), 400
        
        # Check if email exists in users table
        cur.execute('SELECT * FROM "users" WHERE email = %s', (rawEmail,))
        existingUser = cur.fetchone()
        
        if existingUser is not None:
            return jsonify({
                "code": 400,
                "data": {"email": rawEmail},
                "message": "Email already exists in user accounts."
            }), 400

        # Extract only the values that correspond to database columns
        values = [rawAccount.get(col) for col in rawAccount]

        # Create the SQL with explicit column names
        columns = ', '.join(f'"{col}"' for col in rawAccount)
        placeholders = ', '.join(['%s'] * len(rawAccount))
        sql = f'INSERT INTO "accountRequests" ({columns}) VALUES ({placeholders})'

        cur.execute(sql, values)
        conn.commit()

        return jsonify( 
            {   
                "code": 201,
                "data": rawEmail
            }
        ), 201
    
    except Exception as e:
        print(str(e))
        conn.rollback()
        return jsonify(
            {
                "code": 500,
                "data": {
                    "email": rawEmail
                },
                "message": "An error occurred creating the account request."
            }
        ), 500

    finally:
        cur.close()

# -----------------------------------------------------------------------------------------
# [POST] Updates a Business Account Request
@blueprint.route("/updateAccountRequest", methods= ['POST'])
def updateAccountRequest():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()
    print(data)

    requestID = int(data['requestID'])
    isPending = data['isPending']
    isApproved = data['isApproved']

    try:
        cur.execute(
            """
                UPDATE "accountRequests"
                SET "isPending" = %s, "isApproved" = %s
                WHERE "id" = %s
            """,
            (isPending, isApproved, requestID)
        )
        conn.commit()

        return jsonify(
            {   
                "code": 201,
                "data": {
                    "requestID": requestID,
                    "isPending": isPending, 
                    "isApproved": isApproved
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
                    "requestID": requestID,
                    "isPending": isPending,
                    "isApproved": isApproved
                },
                "message": "An error occurred updating the account request."
            }
        ), 500
    
    finally:
        cur.close()

# -----------------------------------------------------------------------------------------
# [POST] Updates a Business Account Request with Business Id after creation of account from admin dashbboard approving account request
@blueprint.route("/updateAccountRequestBusinessID", methods= ['POST'])
def updateAccountRequestBusinessID():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()
    print(data)

    accountID = int(data['businessID'])
    requestID = int(data['requestID'])
    print(accountID)
    print(requestID)
    try:
        cur.execute(
            """
                UPDATE "accountRequests"
                SET "businessId" = %s
                WHERE "id" = %s
            """,
            (accountID, requestID)
        )
        conn.commit()

        return jsonify(
            {   
                "code": 201,
                "data": {
                    "requestID": accountID
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
                    "requestID": accountID
                },
                "message": "An error occurred updating the account request."
            }
        ), 500
    
    finally:
        cur.close()

# -----------------------------------------------------------------------------------------
# [POST] Creates an Account
# - Insert entry into the "producers" collection. 
@blueprint.route("/createProducerAccount", methods=['POST'])
def createProducerAccount():
    conn = g.db
    cur = conn.cursor()
    
    try:
        # Validate request data
        data = request.get_json()
        if not data or 'newBusinessData' not in data:
            return jsonify({
                "code": 400,
                "message": "Invalid request data. 'newBusinessData' is required."
            }), 400
        
        newBusinessData = data["newBusinessData"]
        
        # Validate required fields
        # required_fields = ['producerName', 'producerDesc', 'originCountry', 'mainDrinks', 'hashedPassword']
        # missing_fields = [field for field in required_fields if not newBusinessData.get(field)]
        # if missing_fields:
        #     return jsonify({
        #         "code": 400,
        #         "message": f"Missing required fields: {', '.join(missing_fields)}"
        #     }), 400
        
        # Validate producerName length and format
        producer_name = newBusinessData['producerName'].strip()
        if len(producer_name) < 2 or len(producer_name) > 100:
            return jsonify({
                "code": 400,
                "message": "Producer name must be between 2 and 100 characters."
            }), 400
        
        # Check if producerName already exists (case-insensitive)
        cur.execute('SELECT id FROM producers WHERE LOWER("producerName") = LOWER(%s)', (producer_name,))
        existing_account = cur.fetchone()
        
        if existing_account:
            return jsonify({
                "code": 400,
                "data": {"producerName": producer_name},
                "message": "Producer name already exists."
            }), 400
        
        # Prepare producer data with defaults
        # Sanitize the username if provided, otherwise use sanitized producer name
        original_username = newBusinessData.get('username', '').strip()
        sanitized_username = sanitize_username(original_username) if original_username else sanitize_username(producer_name)
        
        producer_data = {
            'producerName': producer_name,
            'producerDesc': newBusinessData['producerDesc'].strip(),
            'originCountry': newBusinessData['originCountry'].strip(),
            'mainDrinks': newBusinessData['mainDrinks'],
            'photo': newBusinessData.get('photo', ''),
            'hashedPassword': newBusinessData['hashedPassword'],
            'claimStatus': newBusinessData.get('claimStatus', 'pending'),
            'statusOB': newBusinessData.get('statusOB', 'active'),
            'username': sanitized_username,
            'producerLink': newBusinessData.get('producerLink', '').strip() or None,
            'stripeCustomerId': newBusinessData.get('stripeCustomerId', '').strip() or None,
            'isIndependentBottler': bool(newBusinessData.get('isIndependentBottler', False)),
            'location': newBusinessData.get('location', '').strip() or 'Location not specified'
        }
        
        # Insert new producer with all fields including location
        cur.execute("""
            INSERT INTO producers (
                "producerName", "producerDesc", "originCountry", "mainDrinks", "photo", 
                "hashedPassword", "claimStatus", "statusOB", "username", "producerLink", 
                "stripeCustomerId", "isIndependentBottler", "location"
            )
            VALUES (%(producerName)s, %(producerDesc)s, %(originCountry)s, %(mainDrinks)s, 
                   %(photo)s, %(hashedPassword)s, %(claimStatus)s, %(statusOB)s, 
                   %(username)s, %(producerLink)s, %(stripeCustomerId)s, %(isIndependentBottler)s, 
                   %(location)s) 
            RETURNING id
        """, producer_data)
        
        result = cur.fetchone()
        if not result:
            raise Exception("Failed to create producer account")
        
        new_producer_id = result['id']
        
        # Handle questions and answers
        questions_answers = newBusinessData.get('questionsAnswers', [])
        if questions_answers:
            qa_values = []
            for qa in questions_answers:
                # Validate QA data
                if not qa.get('question') or not qa.get('answer'):
                    continue
                qa_values.append((
                    qa['question'],  # Limit question length
                    qa['answer'],   # Limit answer length
                    qa.get('date', 'NOW()'),
                    qa.get('userId'),
                    new_producer_id
                ))
            
            if qa_values:
                cur.executemany("""
                    INSERT INTO "producersQuestionAnswers" (
                        "question", "answer", "date", "userId", "producerId"
                    ) 
                    VALUES (%s, %s, %s, %s, %s)
                """, qa_values)
        
        # Handle updates
        updates = newBusinessData.get('updates', [])
        if updates:
            update_values = []
            for update in updates:
                # Validate update data
                if not update.get('text'):
                    continue
                update_values.append((
                    update.get('date', 'NOW()'),
                    update['text'][:2000],  # Limit text length
                    update.get('photo', ''),
                    new_producer_id
                ))
            
            if update_values:
                cur.executemany("""
                    INSERT INTO "producersUpdates" (
                        "date", "text", "photo", "producerId"
                    ) 
                    VALUES (%s, %s, %s, %s)
                """, update_values)
        
        # Initialize related tables efficiently
        init_queries = []
        
        # Check and initialize producer reviews
        cur.execute('SELECT COUNT(*) AS count FROM "producerReviews" WHERE "producerID" = %s', (new_producer_id,))
        if cur.fetchone()['count'] == 0:
            init_queries.append(('INSERT INTO "producerReviews" ("producerID") VALUES (%s)', (new_producer_id,)))
        
        # Check and initialize profile views
        cur.execute('SELECT COUNT(*) AS count FROM "producersProfileViews" WHERE "producerId" = %s', (new_producer_id,))
        if cur.fetchone()['count'] == 0:
            init_queries.append((
                'INSERT INTO "producersProfileViews" ("producerId", "date", "count") VALUES (%s, CURRENT_DATE, 0)',
                (new_producer_id,)
            ))
        
        # Execute initialization queries
        for query, params in init_queries:
            cur.execute(query, params)
        
        # Commit transaction
        conn.commit()
        
        # Prepare response data
        response_data = {
            "code": 201,
            "data": {
                "producerId": new_producer_id,
                "producerName": producer_name
            },
            "message": "Producer account created successfully"
        }
        
        return jsonify(response_data), 201
        
    except Exception as e:
        # Rollback transaction on error
        conn.rollback()
        
        # Log error for debugging
        import logging
        logging.error(f"Error creating producer account: {str(e)}", exc_info=True)
        
        # Return generic error response
        return jsonify({
            "code": 500,
            "message": "An error occurred while creating the producer account. Please try again."
        }), 500
        
    finally:
        if cur:
            cur.close()
        

# -----------------------------------------------------------------------------------------
# [POST] Creates a Venue Account
# - Insert entry into the "venues" collection.
@blueprint.route("/createVenueAccount", methods= ['POST'])
def createVenueAccount():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()
    print(data)
    newBusinessData = data["newBusinessData"]

    try:
        # Check if venueName already exists
        cur.execute('SELECT id FROM venues WHERE "venueName" = %s', (newBusinessData['venueName'],))
        existingAccount = cur.fetchone()

        if existingAccount:
            return jsonify(
                {
                    "code": 400,
                    "data": {
                        "venueName": newBusinessData['venueName']
                    },
                    "message": "Venue Name already exists."
                }
            ), 400

        # Insert new venue
        # Sanitize the username if provided, otherwise use sanitized venue name
        original_username = newBusinessData.get('username', '')
        sanitized_username = sanitize_username(original_username) if original_username else sanitize_username(newBusinessData['venueName'])
        
        cur.execute("""
            INSERT INTO venues (
                "venueName", "address", "venueType", "originLocation", "venueDesc", 
                "hashedPassword", "photo", "claimStatus", "reservationDetails", "username", 
                "publicHolidays", "stripeCustomerId", "pin"
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
        """, (
            newBusinessData['venueName'], newBusinessData['address'], newBusinessData['venueType'],
            newBusinessData['originLocation'], newBusinessData['venueDesc'], newBusinessData['hashedPassword'],
            newBusinessData['photo'], newBusinessData['claimStatus'], newBusinessData['reservationDetails'],
            sanitized_username, newBusinessData.get('publicHolidays', None),
            newBusinessData.get('stripeCustomerId', None), newBusinessData.get('pin', None)
        ))

        # Extract the new venue ID
        result = cur.fetchone()
        
        if result is None:
            raise Exception("Failed to retrieve new venue ID")

        newVenueId = result['id']
        conn.commit()

        # Handle related data: menu
        menu = newBusinessData.get('menu', [])
        for section in menu:
            cur.execute(
                """
                INSERT INTO "venuesMenu" (
                    "sectionName", "sectionOrder", "sectionMenu", "venueId", "isVisible"
                ) 
                VALUES (%s, %s, %s, %s, %s)
                """,
                (section.get('sectionName', None), section.get('sectionOrder', None), section.get('sectionMenu', []), newVenueId, section.get('isVisible', True))
            )
        conn.commit()

        # Handle related data: openingHours
        opening_hours = newBusinessData.get('openingHours', {})
        cur.execute(
            """
            INSERT INTO "venuesOpeningHours" (
                "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "venueId"
            ) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (opening_hours.get('Monday', []), opening_hours.get('Tuesday', []), opening_hours.get('Wednesday', []),
             opening_hours.get('Thursday', []), opening_hours.get('Friday', []), opening_hours.get('Saturday', []),
             opening_hours.get('Sunday', []), newVenueId)
        )
        conn.commit()

        # Handle related data: questionsAnswers
        questions_answers = newBusinessData.get('questionsAnswers', [])
        for qa in questions_answers:
            cur.execute(
                """
                INSERT INTO "venuesQuestionAnswers" (
                    "question", "answer", "date", "userId", "venueId"
                ) 
                VALUES (%s, %s, %s, %s, %s)
                """,
                (qa['question'], qa['answer'], qa['date'], qa.get('userId', None), newVenueId)
            )
        conn.commit()

        # Handle related data: updates
        updates = newBusinessData.get('updates', [])
        for update in updates:
            cur.execute(
                """
                INSERT INTO "venuesUpdates" (
                    "date", "text", "photo", "venueId"
                ) 
                VALUES (%s, %s, %s, %s)
                """,
                (update['date'], update['text'], update['photo'], newVenueId)
            )
        conn.commit()

        return jsonify( 
            {   
                "code": 201,
                "data": newVenueId
            }
        ), 201

    except Exception as e:
        conn.rollback()
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": {
                    "venueName": newBusinessData['venueName']
                },
                "message": "An error occurred creating the venue account."
            }
        ), 500

    finally:
        cur.close()
    
# -----------------------------------------------------------------------------------------
# [POST] Creates a Token for new accounts

@blueprint.route("/createToken", methods= ['POST'])
def createToken():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()
    print(data)

    businessId = int(data['businessId'])
    requestId = int(data['requestId'])
    businessType = data['businessType']

    try:
        # Determine the correct ID field and table based on businessType
        if businessType == 'producer':
            id_field = 'producerId'
        elif businessType == 'venue':
            id_field = 'venueId'
        else:
            id_field = 'userId' # Default to 'userId'

        # Check for existing token
        cur.execute(f'SELECT * FROM "tokens" WHERE "{id_field}" = %s', (businessId,))
        existingToken = cur.fetchone()

        if existingToken is not None:
            cur.execute('DELETE FROM "tokens" WHERE "token" = %s', (existingToken['token'],))

        token = secrets.token_urlsafe(16)
        expiry = datetime.now() + timedelta(days=3)

        # Insert new token
        query = f"""
            INSERT INTO "tokens" ("token", "{id_field}", "requestId", "expiry")
            VALUES (%s, %s, %s, %s)
        """
        cur.execute(query, (token, businessId, requestId, expiry))
        conn.commit()

        return jsonify(
            {
                "code": 201,
                "data": {
                    "userId": businessId,
                    "token": token
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
                    "userId": businessId,
                },
                "message": "An error occurred creating the token."
            }
        ), 500
    
    finally:
        cur.close()
    
# [POST] Update customerId
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/updateCustomerId', methods=['POST'])
def updateCustomerId():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()
    print(data)

    businessId = int(data['businessId'])
    customerId = data['customerId']
    businessType = data['businessType']

    try:
        cur.execute(
            f"""
            UPDATE "{businessType}s"
            SET "stripeCustomerId" = %s
            WHERE "id" = %s
            """,
            (customerId, businessId)
        )
        conn.commit()

        return jsonify(
            {
                "code": 201,
                "data": {
                    "businessId": businessId,
                    "customerId": customerId
                }
            }
        ), 201
    
    except Exception as e:
        conn.rollback()
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred updating the profile."
            }
        ), 500
    
    finally:
        cur.close()

# -----------------------------------------------------------------------------------------
# [POST] Delete Token
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/deleteToken', methods=['POST'])
def deleteToken():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()
    print(data)

    token = data['token']

    try:
        cur.execute('DELETE FROM "tokens" WHERE "token" = %s', (token,))
        conn.commit()

        return jsonify(
            {
                "code": 201,
                "data": {
                    "token": token
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
                    "token": token
                },
                "message": "An error occurred deleting the token."
            }
        ), 500
    
    finally:
        cur.close()
    
# [POST] Update business username and password
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/updateUsernamePassword', methods=['POST'])
def updateUsernamePassword():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()
    print(data)

    businessId = int(data['businessId'])
    username = data['username']
    hashedPassword = data['hashedPassword']
    businessType = data['businessType']

    try:
        cur.execute(
            f"""
            UPDATE "{businessType}s"
            SET "username" = %s, "hashedPassword" = %s
            WHERE "id" = %s
            """,
            (username, hashedPassword, businessId)
        )
        conn.commit()

        return jsonify(
            {
                "code": 201,
                "data": {
                    "businessId": businessId,
                    "username": username
                }
            }
        ), 201
    
    except Exception as e:
        conn.rollback()
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred updating the profile."
            }
        ), 500
    
    finally:
        cur.close()

@blueprint.route('/sendEmail', methods=['POST'])
def sendEmail():
    data = request.json
    print(data)

    # skip the email process if we are on local env
    if os.getenv("PURPOSE") == "development":
        return jsonify({'message': 'Local dev skip Email successfully!'}), 200

    # else we will send out emails as usual
    send_email_aws(
        subject=data['subject'],
        recipient=data['recipient'],
        body=data['message']
    )
    return jsonify({'message': 'Email sent successfully!'}), 200

# -----------------------------------------------------------------------------------------
# [POST] Updates User Preferences from Onboarding Form -- ADDED BY SMU GROUP 3
@blueprint.route("/addPreferences/<username>", methods=['POST'])
def add_preferences(username):
    conn = g.db
    cur = conn.cursor()
    rawAccount = request.get_json()

    try:
        # Print the incoming request data for debugging
        print(f"Received data to update preferences for user: {username}")
        print(f"Request data: {rawAccount}")

        # Update user preferences in the database
        cur.execute("""
                    UPDATE "users"
                    SET "choiceDrinks" = %s,
                    "choiceFlavours" = %s,
                    "preferences" = %s
                    WHERE "username" = %s
                """, (
                    rawAccount['choiceDrinks'],
                    rawAccount['choiceFlavours'],
                    rawAccount['preferences'],
                    username
                ))

        conn.commit()

        # Print success message
        print(f"Preferences updated successfully for user: {username}")

        return jsonify(
            {
                "code": 201,
                "message": "Preferences updated successfully",
                "data": {
                    "username": username,
                    "choiceDrinks": rawAccount['choiceDrinks'],
                    "choiceFlavours": rawAccount['choiceFlavours'],
                    "preferences": rawAccount['preferences']
                }
            }
        ), 201

    except Exception as e:
        # Print error message and details
        print(f"Error occurred while updating preferences for user: {username}")
        print(f"Error details: {str(e)}")

        # Rollback in case of error
        conn.rollback()

        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while updating the user preferences.",
                "error": str(e),
                "data": {
                    "username": username,
                    "choiceDrinks": rawAccount.get('choiceDrinks', 'N/A'),
                    "choiceFlavours": rawAccount.get('choiceFlavours', 'N/A'),
                    "preferences": rawAccount.get('preferences', 'N/A')
                }
            }
        ), 500

    finally:
        # Clean up database cursor
        cur.close()

##### POSTGRESQL migration code
# # ======================================================
# # Optimize + simple rework (code not tested.)
# # ------------------------------------------------------
# # ======================================================
# # Exception class
# # ------------------------------------------------------
# class CreateUserError(Exception):
#     pass 

# class CreateBizUserError(Exception):
#     pass 

# class UpdateBizUserError(Exception):
#     pass

# class CreateProducerError(Exception):
#     pass 

# class CreateVenueError(Exception):
#     pass 

# class CreateTokenError(Exception):
#     pass

# class UpdatePIDError(Exception):
#     pass

# class UpdatePwdError(Exception):
#     pass

# # ======================================================
# # logic layer
# # # ------------------------------------------------------
# def create_db_user(user_data):
#     db = g.db
#     try: 
#         # with is to ensure the proper connection closure when 
#         # query is done 
#         with db.cursor() as cursor:
#             # fetch only necessary columns limits to only 1
#             select_query = "SELECT username FROM users WHERE username = %s LIMIT 1"
#             cursor.execute(select_query, (user_data["username"],))
#             # listing exist in db
#             if cursor.fetchone():
#                 raise ValueError("Username already exists.")

#             # upload to s3 and if user uploaded a photo
#             if user_data['photo']:
#                 user_data['photo'] = s3Images.uploadBase64ImageToS3(user_data['photo'])

#             # insert new listing data into postgresql
#             columns = ', '.join(user_data.keys())
#             placeholders = ', '.join(['%s'] * len(user_data))
#             insert_sql = f"INSERT INTO users ({columns}) VALUES ({placeholders}) RETURNING id"
#             cursor.execute(insert_sql, list(user_data.values()))
#             new_id = cursor.fetchone()['id']
#             db.commit()

#             return { "id": new_id, "username": user_data["username"]}
#     except Exception as e: 
#         db.rollback()
#         raise CreateUserError(f"Error creating User: {str(e)}") from e


# # -----------------------------------------------------------------------------------------
# # [POST] Creates an Account
# # - Insert entry into the "users" collection. Follows reviews dataclass requirements.
# # - Duplicate review check: If a user with the same username, reject the request
# # - Possible return codes: 201 (Created), 400 (Duplicate Detected), 500 (Error during creation)
# @blueprint.route("/createAccount", methods= ['POST'])
# def createAccount():
#     try: 
#         user_data = request.get_json()
#         user_data['joinDate'] = datetime.strptime(user_data['joinDate'], "%Y-%m-%dT%H:%M:%S.%fZ")# convert date to datetime object
#         user_data['birthday'] = datetime.strptime(user_data['birthday'], "%Y-%m-%d")# convert birthday to datetime object

#         result = create_db_user(user_data)

#         return jsonify({
#             "code": 201,
#             "userID": str(result["id"])
#         }), 201

#     except ValueError as ve:
#         return jsonify({
#             "code": 400,
#             "message": str(ve)
#         }), 400

#     except CreateUserError as cue: 
#         return jsonify({
#             "code": 500,
#             "message": "An error occured while creating new user."
#         }), 500

#     except Exception as e: 
#         return jsonify({
#             "code": 500,
#             "message": f"An error occurred: {str(e)}"
#         }), 500


# # ======================================================
# # logic layer
# # # ------------------------------------------------------
# def create_db_acc_req(biz_acc_data):
#     db = g.db
#     try: 
#         # with is to ensure the proper connection closure when 
#         # query is done 
#         with db.cursor() as cursor:
#             # fetch only necessary columns limits to only 1
#             select_query = "SELECT email FROM accountRequests WHERE email = %s LIMIT 1"
#             cursor.execute(select_query, (biz_acc_data["email"],))
#             # listing exist in db
#             if cursor.fetchone():
#                 raise ValueError("Request already exists.")

#             # insert new listing data into postgresql
#             columns = ', '.join(biz_acc_data.keys())
#             placeholders = ', '.join(['%s'] * len(biz_acc_data))
#             insert_sql = f"INSERT INTO accountRequests ({columns}) VALUES ({placeholders}) RETURNING id"
#             cursor.execute(insert_sql, list(biz_acc_data.values()))
#             new_id = cursor.fetchone()['id']
#             db.commit()

#             return { "id": new_id, "email": biz_acc_data["email"]}

#     except Exception as e: 
#         db.rollback()
#         raise CreateBizUserError(f"An error occurred creating the account request. : {str(e)}") from e

# # -----------------------------------------------------------------------------------------
# # [POST] Creates a Business Account Request
# # - Insert entry into the "accountRequests" collection. Follows reviews dataclass requirements.
# # - Duplicate review check: If a user with the same username, reject the request
# # - Possible return codes: 201 (Created), 400 (Duplicate Detected), 500 (Error during creation)
# @blueprint.route("/createAccountRequest", methods= ['POST'])
# def createAccountRequest():
#     try: 
#         biz_acc_data = request.get_json()
#         biz_acc_data['joinDate'] = datetime.strptime(biz_acc_data['joinDate'], "%Y-%m-%dT%H:%M:%S.%fZ")

#         result = create_db_acc_req(biz_acc_data)

#         return jsonify({
#             "code": 201,
#             "userID": result["email"]
#         }), 201

#     except ValueError as ve:
#         return jsonify({
#             "code": 400,
#             "message": str(ve)
#         }), 400

#     except CreateBizUserError as cue: 
#         return jsonify({
#             "code": 500,
#             "message": "An error occurred creating the account request."
#         }), 500

#     except Exception as e: 
#         return jsonify({
#             "code": 500,
#             "message": f"An error occurred: {str(e)}"
#         }), 500


# # ======================================================
# # logic layer
# # # ------------------------------------------------------
# def create_db_producer(producer_data):
#     db = g.db
#     try: 
#         # with is to ensure the proper connection closure when 
#         # query is done 
#         with db.cursor() as cursor:
#             # fetch only necessary columns limits to only 1
#             select_query = "SELECT producerName FROM producers WHERE producerName = %s LIMIT 1"
#             cursor.execute(select_query, (producer_data["producerName"],))
#             # listing exist in db
#             if cursor.fetchone():
#                 raise ValueError("Producer Name already exists.")

#             # insert new listing data into postgresql
#             columns = ', '.join(producer_data.keys())
#             placeholders = ', '.join(['%s'] * len(producer_data))
#             insert_sql = f"INSERT INTO producers ({columns}) VALUES ({placeholders}) RETURNING id"
#             cursor.execute(insert_sql, list(producer_data.values()))
#             new_id = cursor.fetchone()['id']
#             db.commit()

#             return { "id": new_id, "producerName": producer_data["producerName"]}

#     except Exception as e: 
#         db.rollback()
#         raise CreateProducerError(f"An error occurred creating the account: {str(e)}") from e

# # -----------------------------------------------------------------------------------------
# # [POST] Creates an Account
# # - Insert entry into the "producers" collection. 
# @blueprint.route("/createProducerAccount", methods= ['POST'])
# def createProducerAccount():
#     try: 
#         producer_acc = request.get_json()
#         business_data = producer_acc["newBusinessData"]

#         _ = create_db_producer(business_data)

#         return jsonify({
#             "code": 201,
#             "data": business_data
#         }), 201

#     except ValueError as ve:
#         return jsonify({
#             "code": 400,
#             "data": {
#                 "producerName": business_data['producerName']
#             }
#             "message": str(ve)
#         }), 400

#     except CreateProducerError as cpe: 
#         return jsonify({
#             "code": 500,
#             "data": {
#                 "username": business_data
#             },
#             "message": "An error occurred creating the account request."
#         }), 500

#     except Exception as e: 
#         return jsonify({
#             "code": 500,
#             "data": {
#                 "username": business_data
#             },
#             "message": f"An error occurred: {str(e)}"
#         }), 500


# # ======================================================
# # logic layer
# # # ------------------------------------------------------
# def create_db_venue(venue_data):
#     db = g.db
#     try: 
#         # with is to ensure the proper connection closure when 
#         # query is done 
#         with db.cursor() as cursor:
#             # fetch only necessary columns limits to only 1
#             select_query = "SELECT venueName FROM venues WHERE venueName = %s LIMIT 1"
#             cursor.execute(select_query, (venue_data["venueName"],))
#             # listing exist in db
#             if cursor.fetchone():
#                 raise ValueError("Venue Name already exists.")

#             # insert new listing data into postgresql
#             columns = ', '.join(venue_data.keys())
#             placeholders = ', '.join(['%s'] * len(venue_data))
#             insert_sql = f"INSERT INTO producers ({columns}) VALUES ({placeholders}) RETURNING id"
#             cursor.execute(insert_sql, list(venue_data.values()))
#             new_id = cursor.fetchone()['id']
#             db.commit()

#             return { "id": new_id, "venueName": venue_data["venueName"]}

#     except Exception as e: 
#         db.rollback()
#         raise CreateVenueError(f"An error occurred creating the account: {str(e)}") from e

# # -----------------------------------------------------------------------------------------
# # [POST] Creates a Venue Account
# # - Insert entry into the "venues" collection.
# # https://stackoverflow.com/questions/28261959/what-is-best-representation-for-mongo-id-field-in-postgresql
# @blueprint.route("/createVenueAccount", methods= ['POST'])
# def createVenueAccount():
#     try:
#         data = request.get_json()
#         business_data = data["newBusinessData"]
#         # why do we need to create requestid ? 
#         business_data["requestId"] = int(business_data["requestId"])

#         result = create_db_venue(business_data)
#         business_data["_id"] = result["id"]
#         business_data['requestId'] = str(business_data['requestId'])

#         return jsonify( 
#             {   
#                 "code": 201,
#                 "data": business_data
#             }
#         ), 201

#     except ValueError as ve:
#         return jsonify({
#             "code": 400,
#             "data": {
#                 "producerName": business_data['producerName']
#             }
#             "message": str(ve)
#         }), 400

#     except CreateProducerError as cpe: 
#         return jsonify({
#             "code": 500,
#             "data": {
#                 "username": business_data
#             },
#             "message": "An error occurred creating the account request."
#         }), 500

#     except Exception as e: 
#         return jsonify({
#             "code": 500,
#             "data": {
#                 "username": business_data
#             },
#             "message": f"An error occurred: {str(e)}"
#         }), 500


# # ======================================================
# # logic layer
# # # ------------------------------------------------------
# def create_db_token(token_data):
#     db = g.db
#     try: 
#         # with is to ensure the proper connection closure when 
#         # query is done 
#         with db.cursor() as cursor:
#             # fetch only necessary columns limits to only 1
#             # select_query = "SELECT userId FROM tokens WHERE userId = %s LIMIT 1"
#             # cursor.execute(select_query, (token_data["businessId"],))
#             delete_query = "DELETE FROM tokens WHERE userId = %s"
#             cursor.execute(delete_query, (token_data["businessId"],))
            
#             # prepare for new token 
#             new_token = {
#                 "token": secrets.token_urlsafe(16),
#                 "userId": int(token_data["businessId"]), 
#                 "requestId": int(token_data["requestId"]),
#                 "expiry": datetime.now() + timedelta(days=3)
#             }

#             # insert new listing data into postgresql
#             columns = ', '.join(token_data.keys())
#             placeholders = ', '.join(['%s'] * len(token_data))
#             insert_sql = f"INSERT INTO tokens ({columns}) VALUES ({placeholders}) RETURNING id"
#             cursor.execute(insert_sql, list(token_data.values()))
#             new_id = cursor.fetchone()['id']
#             db.commit()

#             return { "id": new_id, "userId": new_token["userId"], "token": new_token["token"] }

#     except Exception as e: 
#         db.rollback()
#         raise CreateTokenError(f"An error occurred creating the token: {str(e)}") from e

# # -----------------------------------------------------------------------------------------
# # [POST] Creates a Token for new accounts
# @blueprint.route("/createToken", methods= ['POST'])
# def createToken():
#     try:
#         token_data = request.get_json()

#         result = create_db_token(token_data)

#         return jsonify({   
#             "code": 201,
#             "data": result["userId"],
#             "token": result["token"]
#         }), 201

#     except ValueError as ve:
#         return jsonify({
#             "code": 400,
#             "data": {
#                 "producerName": business_data['producerName']
#             }
#             "message": str(ve)
#         }), 400

#     except CreateProducerError as cpe: 
#         return jsonify({
#             "code": 500,
#             "data": {
#                 "username": business_data
#             },
#             "message": "An error occurred creating the account request."
#         }), 500

#     except Exception as e: 
#         return jsonify({
#             "code": 500,
#             "data": {
#                 "username": business_data
#             },
#             "message": f"An error occurred: {str(e)}"
#         }), 500


# # ======================================================
# # logic layer
# # # ------------------------------------------------------
# def update_db_acc_req(biz_acc_data):
#     db = g.db
#     try: 
#         # Ensure the connection and cursor are properly closed
#         with db.cursor() as cursor:
#             # Prepare the update query
#             update_query = "UPDATE accountRequests SET isPending = %s, isApproved = %s WHERE id = %s"
#             cursor.execute(update_query, (biz_acc_data["isPending"], biz_acc_data["isApproved"], biz_acc_data['requestID']))
#             # Commit the transaction
#             db.commit()
            
#             # Return the updated data
#             return {
#                 "requestID": biz_acc_data['requestID'],
#                 "isPending": biz_acc_data["isPending"],
#                 "isApproved": biz_acc_data["isApproved"]
#             }
    
#     except Exception as e: 
#         # Rollback in case of error
#         db.rollback()
#         # Raise a custom exception with the error message
#         raise UpdateBizUserError(f"An error occurred updating the mod request: {str(e)}") from e

# # -----------------------------------------------------------------------------------------
# # [POST] Updates a Business Account Request
# @blueprint.route("/updateAccountRequest", methods= ['POST'])
# def updateAccountRequest():
#     try: 
#         data = request.get_json()
    
#         result = update_db_acc_req(data)

#         return jsonify({   
#                 "code": 201,
#                 "data": {
#                     "requestID": result["requestID"],
#                     "isPending": result["isPending"], 
#                     "isApproved": result["isApproved"]
#                 }
#         }), 201

#     except UpdateBizUserError as uue: 
#         return jsonify({
#             "code": 500,
#             "data": {
#                 "data": {
#                     "requestID": requestID,
#                     "isPending": isPending,
#                     "isApproved": isApproved
#                 }
#             },
#             "message": "An error occurred creating the account request."
#         }), 500

#     except Exception as e:
#         return jsonify(
#             {
#                 "code": 500,
#                 "data": {
#                     "data": {
#                         "requestID": requestID,
#                         "isPending": isPending,
#                         "isApproved": isApproved
#                     }
#                 },
#                 "message": f"An error occurred: {str(e)}"
#             }
#         ), 500


# # ======================================================
# # logic layer
# # # ------------------------------------------------------
# def update_db_customer(data):
#     db = g.db
#     try: 
#         # Ensure the connection and cursor are properly closed
#         with db.cursor() as cursor:
#             # Prepare the update query
#             update_query = f"UPDATE {data['businessType']+'s'} SET stripeCustomerId = %s WHERE id = %s"
#             cursor.execute(update_query, (data['customerId'], data['businessId']['$oid']))
#             # Commit the transaction
#             db.commit()
            
#             # Return the updated data
#             return { "id": data['businessId']['$oid'] }
    
#     except Exception as e: 
#         # Rollback in case of error
#         db.rollback()
#         # Raise a custom exception with the error message
#         raise UpdatePIDError(f"An error occurred updating profile: {str(e)}") from e

# # [POST] Update customerId
# # - Possible return codes: 201 (Updated), 500 (Error during update)
# @blueprint.route('/updateCustomerId', methods=['POST'])
# def updateCustomerId():
#     data = {}
#     try: 
#         data = request.get_json()
#         result = update_db_customer(data)

#         return jsonify({   
#             "code": 201,
#             "message": "Updated customerId successfully!"
#         }), 201
#     except UpdatePIDError as upe: 
#         return jsonify({
#                 "code": 500,
#                 "data": data,
#                 "message": "An error occurred updating profile."
#         }), 500
#     except Exception as e:
#         return jsonify({
#                 "code": 500,
#                 "data": data,
#                 "message": f"An error occurred: {str(e)}"
#         }), 500


# # ======================================================
# # logic layer
# # # ------------------------------------------------------
# def delete_db_tokens(token_data):
#     db = g.db
#     try: 
#         # Ensure the connection and cursor are properly closed
#         with db.cursor() as cursor:
#             # Prepare the update query
#             delete_query = f"DELETE FROM tokens WHERE tokens = %s RETURNING *"
#             cursor.execute(update_query, (token_data['token']))

#             # safety net to prevent multirow deletion
#             if cursor.rowcount > 1: 
#                 # Rollback in case of error
#                 db.rollback()
#                 raise Exception("Multiple duplicate tokens detected.")
#             # Commit the transaction
#             db.commit()
            
#             # Return the updated data
#             return { "id": data['businessId']['$oid'] }
    
#     except Exception as e: 
#         # Rollback in case of error
#         db.rollback()
#         # Raise a custom exception with the error message
#         raise Exception(f"An error occurred deleting token: {str(e)}") from e

# # -----------------------------------------------------------------------------------------
# # [POST] Delete Token
# # - Possible return codes: 201 (Updated), 500 (Error during update)
# @blueprint.route('/deleteToken', methods=['POST'])
# def deleteToken():
#     try: 
#         data = request.get_json()
#         result = delete_db_tokens(data)

#         return jsonify({   
#             "code": 201,
#             "message": "Deleted token successfully!"
#         }), 201

#     except Exception as e:
#         return jsonify({
#             "code": 500,
#             "data": data,
#             "message": "An error occurred deleting token!"
#         }), 500


# # ======================================================
# # logic layer
# # # ------------------------------------------------------
# def update_db_password(token_data):
#     db = g.db
#     try: 
#         # Ensure the connection and cursor are properly closed
#         with db.cursor() as cursor:
#             update_query = f"UPDATE {data['businessType']+'s'} SET username = %s, hashedPassword = %s WHERE id = %s"
#             cursor.execute(update_query, (data['username'], data['hashedPassword'], data['businessId']['$oid']))

#             # Commit the transaction
#             db.commit()
            
#             # Return the updated data
#             return { "id": data['businessId']['$oid'] }
    
#     except Exception as e: 
#         # Rollback in case of error
#         db.rollback()
#         # Raise a custom exception with the error message
#         raise UpdatePwdError(f"An error occurred updating profile: {str(e)}") from e

# # [POST] Update business username and password
# # - Possible return codes: 201 (Updated), 500 (Error during update)
# @blueprint.route('/updateUsernamePassword', methods=['POST'])
# def updateUsernamePassword():
    
#     try:
#         data = request.get_json() 
#         result = update_db_password(data)

#         return jsonify({   
#             "code": 201,
#             "message": "Updated username and password successfully!"
#         }), 201

#     except UpdatePwdError as upe: 
#         return jsonify({
#             "code": 500,
#             "data": data,
#             "message": "An error occurred updating profile!"
#         }), 500

#     except Exception as e:
#         return jsonify({
#             "code": 500,
#             "data": data,
#             "message": "An error occurred updating profile!"
#         }), 500


# @blueprint.route('/sendEmail', methods=['POST'])
# def sendEmail():
#     try: 
#         mail = g.mail
#         data = request.get_json() 

#         msg = Message(data['subject'], 
#                     sender=os.getenv('MAIL_USERNAME'), 
#                     recipients=[data['recipient']])
#         msg.body = data['message']
#         mail.send(msg)

#         return jsonify({
#             'message': 'Email sent successfully!'
#         }), 200

#     except Exception as e:
#         return jsonify({
#             "code": 500,
#             "data": data,
#             "message": "Failed to send out email."
#         }), 500