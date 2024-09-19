# Port: 5031
# Routes: /createAccount (POST), /createAccountRequest (POST), /updateAccountRequest (POST), /createProducerAccount (POST), /createVenueAccount (POST)
# -----------------------------------------------------------------------------------------

import json
import data
import s3Images
import os

from bson import json_util
from flask import Blueprint, g, request, jsonify
from flask_mail import Message
from bson.objectid import ObjectId
from datetime import datetime, timedelta
import secrets

from psycopg2 import sql

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

def parse_json(data):
    return json.loads(json_util.dumps(data))

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
        cursor.execute('SELECT "id" FROM "users" WHERE "username" = %s', (rawUsername,))
        existingAccount = cursor.fetchone()
        
        if existingAccount is not None:
            return jsonify(
                {   
                    "code": 400,
                    "data": {
                        "userName": rawUsername
                    },
                    "message": "Username already exists."
                }
            ), 400
    
    # Handle photo upload if present
    if rawAccount['photo']:
        rawAccount['photo'] = s3Images.uploadBase64ImageToS3(rawAccount['photo'])

    # Prepare data for insertion
    columns = ['username', 'displayName', 'firstName', 'lastName', 'email', 'choiceDrinks', 'modType', 
               'photo', 'hashedPassword', 'joinDate', 'birthday', 'isAdmin']
    values = [rawAccount['username'], rawAccount['displayName'], rawAccount['firstName'], rawAccount['lastName'], 
              rawAccount['email'], rawAccount['choiceDrinks'], rawAccount['modType'], 
              rawAccount['photo'], rawAccount['hashedPassword'], rawAccount['joinDate'], 
              rawAccount['birthday'], rawAccount['isAdmin']]
    
    insert_query = sql.SQL('INSERT INTO "users" ({}) VALUES ({}) RETURNING "id"').format(
        sql.SQL(', ').join(map(lambda col: sql.Identifier(col), columns)),
        sql.SQL(', ').join(sql.Placeholder() * len(columns))
    )
    
    try:
        with db_conn.cursor() as cursor:
            cursor.execute(insert_query, values)
            user_id = cursor.fetchone()['id']
            db_conn.commit()

        # Insert into 'usersDrinkLists' table for "Drinks I Want To Try"
        with db_conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO "usersDrinkLists" ("userId", "listName", "drinks")
                VALUES (%s, %s, %s)
            """, (
                user_id,
                "Drinks I Want To Try",
                rawAccount['drinkLists']['Drinks I Want To Try']['listItems']
            ))
            db_conn.commit()

        # Insert into 'usersDrinkLists' table for "Drinks I Have Tried"
        with db_conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO "usersDrinkLists" ("userId", "listName", "drinks")
                VALUES (%s, %s, %s)
            """, (
                user_id,
                "Drinks I Have Tried",
                rawAccount['drinkLists']['Drinks I Have Tried']['listItems']
            ))
            db_conn.commit()

        # Insert into 'usersFollowLists' table
        with db_conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO "usersFollowLists" ("userId", "users", "producers", "venues")
                VALUES (%s, %s, %s, %s)
            """, (
                user_id,
                rawAccount['followLists']['users'],
                rawAccount['followLists']['producers'],
                rawAccount['followLists']['venues']
            ))
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
        
        columns = ', '.join(f'"{key}"' for key in rawAccount.keys())
        placeholders = ', '.join(['%s'] * len(rawAccount))
        sql = f'INSERT INTO "accountRequests" ({columns}) VALUES ({placeholders})'

        cur.execute(sql, list(rawAccount.values()))
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
    # db = g.db
    # data = request.get_json()
    # print(data)
    # requestID = data['requestID']
    # isPending = data['isPending']
    # isApproved = data['isApproved']

    # try: 
    #     updateReviewStatus = db.accountRequests.update_one({'_id': ObjectId(requestID)}, {'$set': {'isPending': isPending, 'isApproved': isApproved}})

    #     return jsonify(
    #         {   
    #             "code": 201,
    #             "data": {
    #                 "requestID": requestID,
    #                 "isPending": isPending, 
    #                 "isApproved": isApproved
    #             }
    #         }
    #     ), 201
    # except Exception as e:
    #     print(str(e))
    #     return jsonify(
    #         {
    #             "code": 500,
    #             "data": {
    #                 "data": {
    #                     "requestID": requestID,
    #                     "isPending": isPending,
    #                     "isApproved": isApproved
    #                 }
    #             },
    #             "message": "An error occurred updating the mod request."
    #         }
    #     ), 500

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
# [POST] Creates an Account
# - Insert entry into the "producers" collection. 
@blueprint.route("/createProducerAccount", methods=['POST'])
def createProducerAccount():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()
    print(data)
    newBusinessData = data["newBusinessData"]

    try:
        # Check if producerName already exists
        cur.execute('SELECT id FROM producers WHERE "producerName" = %s', (newBusinessData['producerName'],))
        existingAccount = cur.fetchone()

        if existingAccount:
            return jsonify(
                {
                    "code": 400,
                    "data": {
                        "producerName": newBusinessData['producerName']
                    },
                    "message": "Producer Name already exists."
                }
            ), 400

        # Insert new producer
        cur.execute("""
            INSERT INTO producers (
                "producerName", "producerDesc", "originCountry", "mainDrinks", "photo", "hashedPassword", 
                "claimStatus", "statusOB", "username", "producerLink", "stripeCustomerId"
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
        """, (
            newBusinessData['producerName'], newBusinessData['producerDesc'], newBusinessData['originCountry'],
            newBusinessData['mainDrinks'], newBusinessData['photo'], newBusinessData['hashedPassword'],
            newBusinessData['claimStatus'], newBusinessData['statusOB'], newBusinessData.get('username', None),
            newBusinessData.get('producerLink', None), newBusinessData.get('stripeCustomerId', None)
        ))

        # Extract the new producer ID
        result = cur.fetchone()

        if result is None:
            raise Exception("Failed to retrieve new producer ID")

        newProducerId = result['id']
        conn.commit()

        # Handle related data: questionsAnswers
        questions_answers = newBusinessData.get('questionsAnswers', [])
        for qa in questions_answers:
            cur.execute(
                """
                INSERT INTO "producersQuestionAnswers" (
                    "question", "answer", "date", "userId", "producerId"
                ) 
                VALUES (%s, %s, %s, %s, %s)
                """,
                (qa['question'], qa['answer'], qa['date'], qa.get('userId', None), newProducerId)
            )
        conn.commit()
        
        # Handle related data: updates
        updates = newBusinessData.get('updates', [])
        for update in updates:
            cur.execute(
                """
                INSERT INTO "producersUpdates" (
                    "date", "text", "photo", "producerId"
                ) 
                VALUES (%s, %s, %s, %s)
                """,
                (update['date'], update['text'], update['photo'], newProducerId)
            )
        conn.commit()

        return jsonify( 
            {   
                "code": 201,
                "data": {
                    "id": newProducerId,
                    "producerName": newBusinessData['producerName']
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
                    "producerName": newBusinessData['producerName']
                },
                "message": "An error occurred creating the producer account."
            }
        ), 500

    finally:
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
            newBusinessData.get('username', None), newBusinessData.get('publicHolidays', None),
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
                    "sectionName", "sectionOrder", "sectionMenu", "venueId"
                ) 
                VALUES (%s, %s, %s, %s)
                """,
                (section.get('sectionName', None), section.get('sectionOrder', None), section.get('sectionMenu', []), newVenueId)
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
                "data": {
                    "id": newVenueId,
                    "venueName": newBusinessData['venueName']
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

    try:
        cur.execute('SELECT * FROM "tokens" WHERE "userId" = %s', (businessId,))
        existingToken = cur.fetchone()

        if existingToken is not None:
            cur.execute('DELETE FROM "tokens" WHERE "token" = %s', (existingToken['token'],))

        token = secrets.token_urlsafe(16)
        expiry = datetime.now() + timedelta(days=3)

        newToken = {
            "token": token,
            "userId": businessId,
            "requestId": requestId,
            "expiry": expiry,
        }

        cur.execute(
            """
                INSERT INTO tokens ("token", "userId", "requestId", "expiry")
                VALUES (%s, %s, %s, %s)
            """,
            (token, businessId, requestId, expiry)
        )
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
    db = g.db

    data = request.get_json()
    print(data)

    businessId = data['businessId']['$oid']
    customerId = data['customerId']
    businessType = data['businessType'] + 's'

    try: 
        update = db[businessType].update_one({'_id': ObjectId(businessId)}, {'$set': {'stripeCustomerId': customerId} })
        return jsonify(
            {   
                "code": 201,
                "message": "Updated customerId successfully!"
            }
        ), 201
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred updating profile!"
            }
        ), 500

# -----------------------------------------------------------------------------------------
# [POST] Delete Token
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/deleteToken', methods=['POST'])
def deleteToken():
    db = g.db

    data = request.get_json()
    print(data)

    token = data['token']

    try: 
        delete_result = db.tokens.delete_one({'token': token})
        return jsonify(
            {   
                "code": 201,
                "message": "Deleted token successfully!"
            }
        ), 201
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred deleting token!"
            }
        ), 500
    
# [POST] Update business username and password
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/updateUsernamePassword', methods=['POST'])
def updateUsernamePassword():
    db = g.db

    data = request.get_json()
    print(data)

    businessId = data['businessId']['$oid']
    username = data['username']
    hashedPassword = data['hashedPassword']
    businessType = data['businessType'] + 's'

    try: 
        update = db[businessType].update_one({'_id': ObjectId(businessId)}, {'$set': {
                                                                                    'username': username,
                                                                                    'hashedPassword': hashedPassword},
                                                                                    })
        return jsonify(
            {   
                "code": 201,
                "message": "Updated username and password successfully!"
            }
        ), 201
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred updating profile!"
            }
        ), 500
    

@blueprint.route('/sendEmail', methods=['POST'])
def sendEmail():
    db = g.db
    mail = g.mail
    data = request.json
    print(data)
    msg = Message(data['subject'], 
                  sender=os.getenv('MAIL_USERNAME'), 
                  recipients=[data['recipient']])
    msg.body = data['message']
    mail.send(msg)
    return jsonify({'message': 'Email sent successfully!'}), 200


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