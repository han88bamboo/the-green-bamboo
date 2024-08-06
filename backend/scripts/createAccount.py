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
    db = g.db
    rawAccount = request.get_json()
    rawAccount['joinDate'] = datetime.strptime(rawAccount['joinDate'], "%Y-%m-%dT%H:%M:%S.%fZ")# convert date to datetime object
    rawAccount['birthday'] = datetime.strptime(rawAccount['birthday'], "%Y-%m-%d")# convert birthday to datetime object
    # rawAccount['birthday'] = datetime.strftime(rawAccount['birthday'], "%Y-%m-%dT%H:%M:%S.%fZ")# format birthday to desired object type
    rawUsername= rawAccount['username']
    # Duplicate listing check: Reject if review with the same userID and reviewTarget exists in the database
    existingAccount = db.users.find_one({"username": rawUsername})
    if(existingAccount!= None):
        return jsonify(
            {   
                "code": 400,
                "data": {
                    "userName": rawUsername
                },
                "message": "Username already exists."
            }
        ), 400
    
    
    # Insert new review into database
    if rawAccount['photo']:
        rawAccount['photo'] = s3Images.uploadBase64ImageToS3(rawAccount['photo'])
    newAccount = data.users(**rawAccount)
    try:
        insertResult = db.users.insert_one(data.asdict(newAccount))

        return jsonify( 
            {   
                "code": 201,
                "data": {
                    "userName": rawUsername,
                    "userID": str(insertResult.inserted_id)
                }
            }
        ), 201
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": {
                    "userame": rawUsername
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
    db = g.db
    rawAccount = request.get_json()
    rawEmail= rawAccount['email']
    rawAccount['joinDate'] = datetime.strptime(rawAccount['joinDate'], "%Y-%m-%dT%H:%M:%S.%fZ")
    # Duplicate listing check: Reject if review with the same userID and reviewTarget exists in the database
    existingAccount = db.accountRequests.find_one({"email": rawEmail})
    if(existingAccount!= None):
        return jsonify(
            {   
                "code": 400,
                "data": {
                    "userName": rawEmail
                },
                "message": "Request already exists."
            }
        ), 400
    
    
    # Insert new review into database
    # newAccount = data.users(**rawAccount)
    try:
        insertResult = db.accountRequests.insert_one(rawAccount)

        return jsonify( 
            {   
                "code": 201,
                "data": rawEmail
            }
        ), 201
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": {
                    "email": rawEmail
                },
                "message": "An error occurred creating the account request."
            }
        ), 500
# -----------------------------------------------------------------------------------------
# [POST] Updates a Business Account Request
@blueprint.route("/updateAccountRequest", methods= ['POST'])
def updateAccountRequest():
    db = g.db
    data = request.get_json()
    print(data)
    requestID = data['requestID']
    isPending = data['isPending']
    isApproved = data['isApproved']

    try: 
        updateReviewStatus = db.accountRequests.update_one({'_id': ObjectId(requestID)}, {'$set': {'isPending': isPending, 'isApproved': isApproved}})

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
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": {
                    "data": {
                        "requestID": requestID,
                        "isPending": isPending,
                        "isApproved": isApproved
                    }
                },
                "message": "An error occurred updating the mod request."
            }
        ), 500
# -----------------------------------------------------------------------------------------
# [POST] Creates an Account
# - Insert entry into the "producers" collection. 
@blueprint.route("/createProducerAccount", methods= ['POST'])
def createProducerAccount():
    db = g.db
    data = request.get_json()
    print(data)
    newBusinessData = data["newBusinessData"]
    newBusinessData["requestId"] = ObjectId(newBusinessData["requestId"])

    print(newBusinessData["producerName"])

    existingAccount = db.producers.find_one({"producerName": newBusinessData['producerName']})
    if(existingAccount!= None):
        return jsonify(
            {   
                "code": 400,
                "data": {
                    "producerName": newBusinessData['producerName']
                },
                "message": "Producer Name already exists."
            }
        ), 400

    try:
        insertResult = db.producers.insert_one(newBusinessData)
        newBusinessData['_id'] = str(newBusinessData['_id'])

        return jsonify( 
            {   
                "code": 201,
                "data": newBusinessData
            }
        ), 201
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": {
                    "userame": newBusinessData
                },
                "message": "An error occurred creating the account."
            }
        ), 500
# -----------------------------------------------------------------------------------------
# [POST] Creates a Venue Account
# - Insert entry into the "venues" collection.
@blueprint.route("/createVenueAccount", methods= ['POST'])
def createVenueAccount():
    db = g.db
    data = request.get_json()
    print(data)
    newBusinessData = data["newBusinessData"]
    newBusinessData["requestId"] = ObjectId(newBusinessData["requestId"])

    print(newBusinessData["venueName"])

    existingAccount = db.venues.find_one({"venueName": newBusinessData['venueName']})
    if(existingAccount!= None):
        return jsonify(
            {   
                "code": 400,
                "data": {
                    "venueName": newBusinessData['venueName']
                },
                "message": "Venue Name already exists."
            }
        ), 400

    try:
        insertResult = db.venues.insert_one(newBusinessData)
        newBusinessData['_id'] = str(newBusinessData['_id'])

        return jsonify( 
            {   
                "code": 201,
                "data": newBusinessData
            }
        ), 201
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": {
                    "userame": newBusinessData
                },
                "message": "An error occurred creating the account."
            }
        ), 500
    
# -----------------------------------------------------------------------------------------
# [POST] Creates a Token for new accounts

@blueprint.route("/createToken", methods= ['POST'])
def createToken():
    db = g.db
    data = request.get_json()
    print(data)

    existingToken = db.tokens.find_one({"userId": ObjectId(data['businessId'])})

    if (existingToken != None):
        db.tokens.delete_one({'token': existingToken['token']})

    token = secrets.token_urlsafe(16)
    expiry = datetime.now() + timedelta(days=3)

    newToken = {
        "token": token,
        "userId": ObjectId(data['businessId']),
        "requestId": ObjectId(data['requestId']),
        "expiry": expiry,
        "isNew": data['isNew']
    }

    try:
        createToken = db.tokens.insert_one(newToken)
        return jsonify(
            {   
                "code": 201,
                "data": {
                    "userId": data['businessId'],
                    "token": token
                }
            }
        ), 201
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": {
                    "userId": data['businessId'],
                },
                "message": "An error occurred creating the token."
            }
        ), 500
    
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

