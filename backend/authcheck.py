# Port: 5030
# Routes: /authcheck (POST), /authcheckUser (POST), /authcheckProducer (POST), /authcheckVenue (POST)
# -----------------------------------------------------------------------------------------

import bson
import json
import smtplib
import random
import string

from bson import json_util
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS

from bson.objectid import ObjectId

from datetime import datetime

import data

from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)  # Allow all requests

load_dotenv()
app.config["MONGO_URI"] = os.getenv('MONGO_DB_URL')
db = PyMongo(app).db

def parse_json(data):
    return json.loads(json_util.dumps(data))

# -----------------------------------------------------------------------------------------
# [POST] Authenticates an account
# - Check if account exists in the "users", "producers", or "venues" collection. If so, check if the password matches.
# - Possible return codes: 200 (Authenticated), 400 (Account not found), 401 (Incorrect password), 500 (Error during authentication)
@app.route("/authcheck", methods= ['POST'])
def authcheck():

    try:
        loginInfo = request.get_json()


        # Check if user exists in the "users" collection
        userExistsRaw = db.users.find_one({"username": loginInfo["username"]})
        userExists = parse_json(userExistsRaw)
        if (userExists != None):

            # User exists, check if password matches
            if(str(userExists["hashedPassword"]) == str(loginInfo["password"])):
                return jsonify(
                    {   
                        "code": 200,
                        "id": userExists["_id"]["$oid"],
                        "role": "user",
                        "message": "Authenticated!"
                    }
                ), 200
            
            # Password does not match
            else:
                return jsonify(
                    {   
                        "code": 401,
                        "message": "Invalid username or password!"
                    }
                ), 401


        # Check if producer exists in the "producers" collection
        producerExistsRaw = db.producers.find_one({"producerName": loginInfo["username"]})
        producerExists = parse_json(producerExistsRaw)
        if (producerExists != None):

            # Producer exists, check if password matches
            if(str(producerExists["hashedPassword"]) == str(loginInfo["password"])):
                return jsonify(
                    {   
                        "code": 200,
                        "id": producerExists["_id"]["$oid"],
                        "role": "producer",
                        "message": "Authenticated!"
                    }
                ), 200
            
            # Password does not match
            else:
                return jsonify(
                    {   
                        "code": 401,
                        "message": "Invalid username or password!"
                    }
                ), 401


        # Check if venue exists in the "venues" collection
        venueExistsRaw = db.venues.find_one({"venueName": loginInfo["username"]})
        venueExists = parse_json(venueExistsRaw)
        if (venueExists != None):

            # Venue exists, check if password matches
            if(str(venueExists["hashedPassword"]) == str(loginInfo["password"])):
                return jsonify(
                    {   
                        "code": 200,
                        "id": venueExists["_id"]["$oid"],
                        "role": "venue",
                        "message": "Authenticated!"
                    }
                ), 200
            
            # Password does not match
            else:
                return jsonify(
                    {   
                        "code": 401,
                        "message": "Invalid username or password!"
                    }
                ), 401
        

        # Account does not exist
        return jsonify(
            {   
                "code": 400,
                "message": "An account of this username does not exist!"
            }
        ), 400


    # Error during authentication
    except Exception as e:
        return jsonify(
            {   
                "code": 500,
                "message": "An unknown error occurred while logging in, please try again."
            }
        ), 500

# -----------------------------------------------------------------------------------------
# [POST] Authenticates a user
# - Check if user exists in the "users" collection. If so, check if the password matches.
# - Possible return codes: 200 (Authenticated), 400 (User not found), 401 (Incorrect password), 500 (Error during authentication)
@app.route("/authcheckUser", methods= ['POST'])
def authcheckUser():

    try:
        # Check if user exists in the "users" collection
        loginInfo = request.get_json()
        userExistsRaw = db.users.find_one({"username": loginInfo["username"]})
        userExists = parse_json(userExistsRaw)

        # User does not exist
        if(userExists == None):
            return jsonify(
                {   
                    "code": 400,
                    "message": "An account of this type and username does not exist!"
                }
            ), 400
        
        # User exists, check if password matches
        if(str(userExists["hashedPassword"]) == str(loginInfo["password"])):
            return jsonify(
                {   
                    "code": 200,
                    "id": userExists["_id"]["$oid"],
                    "message": "Authenticated!"
                }
            ), 200
        
        # Password does not match
        else:
            return jsonify(
                {   
                    "code": 401,
                    "message": "Invalid username or password!"
                }
            ), 401
    
    # Error during authentication
    except Exception as e:
        return jsonify(
            {   
                "code": 500,
                "message": "An unknown error occurred while logging in, please try again."
            }
        ), 500

# -----------------------------------------------------------------------------------------
# [POST] Authenticates a producer
# - Check if producer exists in the "producers" collection. If so, check if the password matches.
# - Possible return codes: 200 (Authenticated), 400 (Producer not found), 401 (Incorrect password), 500 (Error during authentication)
@app.route("/authcheckProducer", methods= ['POST'])
def authcheckProducer():

    try:
        # Check if producer exists in the "producers" collection
        loginInfo = request.get_json()
        producerExistsRaw = db.producers.find_one({"producerName": loginInfo["username"]})
        producerExists = parse_json(producerExistsRaw)

        # Producer does not exist
        if(producerExists == None):
            return jsonify(
                {   
                    "code": 400,
                    "message": "An account of this type and username does not exist!"
                }
            ), 400
        
        # Producer exists, check if password matches
        if(str(producerExists["hashedPassword"]) == str(loginInfo["password"])):
            return jsonify(
                {   
                    "code": 200,
                    "id": producerExists["_id"]["$oid"],
                    "message": "Authenticated!"
                }
            ), 200
        
        # Password does not match
        else:
            return jsonify(
                {   
                    "code": 401,
                    "message": "Invalid username or password!"
                }
            ), 401
    
    # Error during authentication
    except Exception as e:
        return jsonify(
            {   
                "code": 500,
                "message": "An unknown error occurred while logging in, please try again."
            }
        ), 500

# -----------------------------------------------------------------------------------------
# [POST] Authenticates a venue
# - Check if venue exists in the "venues" collection. If so, check if the password matches.
# - Possible return codes: 200 (Authenticated), 400 (Venue not found), 401 (Incorrect password), 500 (Error during authentication)
@app.route("/authcheckVenue", methods= ['POST'])
def authcheckVenue():

    try:
        # Check if venue exists in the "venues" collection
        loginInfo = request.get_json()
        venueExistsRaw = db.venues.find_one({"venueName": loginInfo["username"]})
        venueExists = parse_json(venueExistsRaw)

        # Venue does not exist
        if(venueExists == None):
            return jsonify(
                {   
                    "code": 400,
                    "message": "An account of this type and username does not exist!"
                }
            ), 400
        
        # Venue exists, check if password matches
        if(str(venueExists["hashedPassword"]) == str(loginInfo["password"])):
            return jsonify(
                {   
                    "code": 200,
                    "id": venueExists["_id"]["$oid"],
                    "message": "Authenticated!"
                }
            ), 200
        
        # Password does not match
        else:
            return jsonify(
                {   
                    "code": 401,
                    "message": "Invalid username or password!"
                }
            ), 401
    
    # Error during authentication
    except Exception as e:
        return jsonify(
            {   
                "code": 500,
                "message": "An unknown error occurred while logging in, please try again."
            }
        ), 500

# -----------------------------------------------------------------------------------------
# [POST] Edit user password
# - Update user password with new password
# - Possible return codes: 201 (Updated), 401(Passwords do not match) , 404(User not exist), 500 (Error during update)
@app.route('/editPassword/<id>', methods=['POST'])
def editPassword(id):
    data = request.get_json()
    print(data)
    # if data contains image64
    if data["userType"] == "user":
        userRaw = db.users.find_one({"_id": ObjectId(id)})
    if data["userType"] == "producer":
        userRaw = db.producers.find_one({"_id": ObjectId(id)})
    if data["userType"] == "venue":
        userRaw = db.venues.find_one({"_id": ObjectId(id)})
        
    if userRaw is None:
        return jsonify(
            {   
                "code": 404,
                "data": {
                    "userID": id
                }
            }
        ), 404
    try: 
        if data['oldHash'] != userRaw['hashedPassword']:
            return jsonify(
                {   
                    "code": 401,
                    "data": {
                        "userID": id
                    }
                }
            ), 401
        else:
            if data["userType"] == "user":
                updatePassword = db.users.update_one({'_id': ObjectId(id)}, {'$set': {'hashedPassword': data['newHash']}})
            if data["userType"] == "producer":
                updatePassword = db.producers.update_one({'_id': ObjectId(id)}, {'$set': {'hashedPassword': data['newHash']}})
            if data["userType"] == "venue":
                updatePassword = db.venues.update_one({'_id': ObjectId(id)}, {'$set': {'hashedPassword': data['newHash']}})

            return jsonify(
                {   
                    "code": 201,
                    "data": {
                        "userID": id,
                    }
                }
            ), 201
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": {
                    "userID": id
                },
                "message": "An error occurred updating the password."
            }
        ), 500
# -----------------------------------------------------------------------------------------
# [POST] Reset user password
# - Sends email with 6 digit PIN
# - Possible return codes: 201 (Sent), 404 (Email not exist), 500 (Error during email sending)
@app.route('/sendResetPin/<id>', methods=['POST'])
def sendResetPin(id):
    data = request.get_json()
    print(data)
    
    email_address = os.getenv('EMAIL_ADDRESS')
    password = os.getenv('PASSWORD')
    pin = random.randint(100000, 999999)
    time = datetime.now()
    time = time.strftime("%Y-%m-%d %H:%M:%S")
    updatePin = str(pin) +',' + time
    try:
        # check user type
        if data["userType"] == "user":
            userRaw = db.users.find_one({"_id": ObjectId(id)})
            if userRaw != None:
                updatePin = db.users.update_one({'_id': ObjectId(id)}, {'$set': {'pin': updatePin}})

        if data["userType"] == "producer":
            userRaw = db.producers.find_one({"_id": ObjectId(id)})
            if userRaw != None:
                updatePin = db.producers.update_one({'_id': ObjectId(id)}, {'$set': {'pin': updatePin}})
            # Need to get the email from producers and assign to variable to send email
        if data["userType"] == "venue":
            userRaw = db.venues.find_one({"_id": ObjectId(id)})
            if userRaw != None:
                updatePin = db.venues.update_one({'_id': ObjectId(id)}, {'$set': {'pin': updatePin}})
            # Need to get the email from venues and assign to variable to send email
            
        if userRaw is None:
            return jsonify(
                {   
                    "code": 404,
                    "data": {
                        "userID": id
                    },
                    "message": "User not found"
                }
            ), 404
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(email_address, password)

        message = 'Subject: Drink-X Reset Password\n\n Your pin is {} and expires in 1 hour, please ignore this message if you did not try to reset your password, alternatively, you can email us'.format(pin)
        server.sendmail(email_address, email_address, message)
        server.quit()
        print(email_address)
        print("Success: Email sent!")
        
        return jsonify(
                {   
                    "code": 201,
                    "data": {
                        "userID": id,
                    }
                }
            ), 201

    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": {
                    "userID": id
                },
                "message": "An error occurred sending the email."
            }
        ), 500
    
# -----------------------------------------------------------------------------------------
# [POST] Check sent pin actual reset pin
# - Check whether user sent pin equals to generated pin
# - Possible return codes: 201 (Sent), 404 (Email not exist), 500 (Error during email sending)
# To allow SMTP to login to google account, need to go here and create an app password, afterwards, store it in the .env file
# https://myaccount.google.com/u/1/apppasswords
@app.route('/verifyPin/<id>', methods=['POST'])
def verifyPin(id):
    data = request.get_json()
    print(data)
    
    time = datetime.now()
    time = time.strftime("%Y-%m-%d %H:%M:%S")
    try:
        # check user type
        if data["userType"] == "user":
            userRaw = db.users.find_one({"_id": ObjectId(id)})

        if data["userType"] == "producer":
            userRaw = db.producers.find_one({"_id": ObjectId(id)})

        if data["userType"] == "venue":
            userRaw = db.venues.find_one({"_id": ObjectId(id)})
            
        if userRaw is None:
            return jsonify(
                {   
                    "code": 404,
                    "data": {
                        "userID": id
                    },
                    "message": "User not found"
                }
            ), 404
        splitPinData = userRaw['pin'].split(',')
        actualPin, dateTime = splitPinData[0], splitPinData[1]

        datetime_str1 = dateTime
        datetime_obj1 = datetime.strptime(datetime_str1, "%Y-%m-%d %H:%M:%S")
        datetime_obj2 = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        time_difference = datetime_obj2 - datetime_obj1

        if str(actualPin) == str(data['pin']) and time_difference.total_seconds()<=7200.0:

            return jsonify(
                    {   
                        "code": 201,
                        "data": {
                            "userID": id,
                        }
                    }
                ), 201  
        
        else:
            return jsonify(
                {
                    "code": 400,
                    "data": {
                        "userID": id
                    },
                    "message": "OTP is wrong or expired."
                }
            ), 500

    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": {
                    "userID": id
                },
                "message": "An error verifying the pin. Please resend pin or try again"
            }
        ), 500
    
# -----------------------------------------------------------------------------------------
# [POST] Reset Password
# - Check whether user exists and then changes the hash value
# - Possible return codes: 201 (Sent), 404 (Email not exist), 500 (Error during email sending)
@app.route('/resetPassword/<id>', methods=['POST'])
def resetPassword(id):
    data = request.get_json()
    print(data)
    email_address = os.getenv('EMAIL_ADDRESS')
    email_password = os.getenv('PASSWORD')
    try:
        # check user type
        if data["userType"] == "user":
            userRaw = db.users.find_one({"_id": ObjectId(id)})
            if userRaw != None:
                username = userRaw['username']

        if data["userType"] == "producer":
            userRaw = db.producers.find_one({"_id": ObjectId(id)})
            if userRaw != None:
                username = userRaw['producerName']

        if data["userType"] == "venue":
            userRaw = db.venues.find_one({"_id": ObjectId(id)})
            if userRaw != None:
                username = userRaw['venueName']
            
        if userRaw is None:
            return jsonify(
                {   
                    "code": 404,
                    "data": {
                        "userID": id
                    },
                    "message": "User not found"
                }
            ), 404
        # get actual pin
        splitPinData = userRaw['pin'].split(',')
        actualPin = splitPinData[0]
        
        # check if pin is correct just in case someone accesses the url
        if str(actualPin) == str(data['pin']):

            # create a new password here
            characters = string.ascii_letters + string.digits + string.punctuation
            password = ''.join(random.choice(characters) for _ in range(10))

            combinedString = str(username) + password
            hash = 0
            
            # hash it here
            for i in range(len(combinedString)):
                char = ord(combinedString[i])
                hash = (hash << 5) - hash + char
                hash &= 0xFFFFFFFF  # Convert to 32-bit integer

            if hash & (1 << 31):  # If the highest bit is set
                hash -= 1 << 32  # Convert to a signed integer


            # Update the hash with new hash and remove the pin used to prevent re-reset
            if data["userType"] == "user":
                updatePassword = db.users.update_one({'_id': ObjectId(id)}, {'$set': {'hashedPassword': str(hash), 'pin':''}})
            if data["userType"] == "producer":
                updatePassword = db.producers.update_one({'_id': ObjectId(id)}, {'$set': {'hashedPassword': str(hash), 'pin':''}})
            if data["userType"] == "venue":
                updatePassword = db.venues.update_one({'_id': ObjectId(id)}, {'$set': {'hashedPassword': str(hash), 'pin':''}})


            # send email containing the password
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(email_address, email_password)

            message = 'Subject: Drink-X Reset Password\n\n Your new password is {}, please email us if you did not authorise this'.format(password)
            server.sendmail(email_address, email_address, message)
            server.quit()
            print("Success: Email sent!")

            return jsonify(
                {   
                    "code": 201,
                    "data": {
                        "userID": id,
                    }
                }
            ), 201  
        else:
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "userID": id
                    },
                    "message": "Something went wrong resetting the password. Please resend pin and try again."
                }
            ), 500      

    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": {
                    "userID": id
                },
                "message": "An error resetting the password. Please resend pin and try again. Please resend pin and try again."
            }
        ), 500
    
# -----------------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port = 5030)