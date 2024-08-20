# Port: 5030
# Routes: /authcheck (POST), /authcheckUser (POST), /authcheckProducer (POST), /authcheckVenue (POST)
# -----------------------------------------------------------------------------------------

import os
import json
import smtplib
import random
import string

from bson import json_util
from flask import request, jsonify, g, Blueprint
from bson.objectid import ObjectId
from datetime import datetime

# import psycopg2
# from psycopg2.extras import RealDictCursor

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)


# EXAMPLE ROUTE
# @blueprint.route('/get_data', methods=['GET'])
# def get_data():
#     try:
#         conn = g.db  # Get the DB connection from g
#         cur = conn.cursor()
#         cur.execute('SELECT * FROM testing')  # Replace with your query
#         results = cur.fetchall()
#         cur.close()  # Close the cursor
#         return jsonify(results)  # Convert the results to JSON and return
#     except Exception as e:
#         return jsonify({"error": str(e)})

def parse_json(data):
    return json.loads(json_util.dumps(data))

# -----------------------------------------------------------------------------------------
# [POST] Authenticates an account
# - Check if account exists in the "users", "producers", or "venues" collection. If so, check if the password matches.
# - Possible return codes: 200 (Authenticated), 400 (Account not found), 401 (Incorrect password), 500 (Error during authentication)
@blueprint.route("/authcheck", methods= ['POST'])
def authcheck():
    try:
        # db = g.db
        loginInfo = request.get_json()

        conn = g.db  # Get the DB connection from g
        cur = conn.cursor()
        username = loginInfo["username"]
        password = loginInfo["password"]

        # Check if user exists in the "users" table
        cur.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cur.fetchone()
        if user is not None:
            if(str(user["hashedpassword"]) == str(password)):
                return jsonify(
                    {   
                        "code": 200,
                        "id": user['id'],
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

        # Check if producer exists in the "producers" table
        cur.execute('SELECT * FROM producers WHERE username = %s', (username,))
        producer = cur.fetchone()
        if (producer is not None):
            # Producer exists, check if password matches
            if(str(producer["hashedpassword"]) == str(password)):
                return jsonify(
                    {   
                        "code": 200,
                        "id": producer['id'],
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

        # Check if venue exists in the "venues" table
        cur.execute('SELECT * FROM venues WHERE username = %s', (username,))
        venue = cur.fetchone()
        if (venue is not None):

            # Venue exists, check if password matches
            if(str(venue["hashedpassword"]) == str(password)):
                return jsonify(
                    {   
                        "code": 200,
                        "id": venue['id'],
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

        # Account does not exist at all in all three tables
        return jsonify(
            {   
                "code": 400,
                "message": "An account of this username does not exist!"
            }
        ), 400

    #     userExistsRaw = db.users.find_one({"username": loginInfo["username"]})
    #     userExists = parse_json(userExistsRaw)
    #     if (userExists != None):

    #         # User exists, check if password matches
    #         if(str(userExists["hashedPassword"]) == str(loginInfo["password"])):
    #             return jsonify(
    #                 {   
    #                     "code": 200,
    #                     "id": userExists["_id"]["$oid"],
    #                     "role": "user",
    #                     "message": "Authenticated!"
    #                 }
    #             ), 200
            
    #         # Password does not match
    #         else:
    #             return jsonify(
    #                 {   
    #                     "code": 401,
    #                     "message": "Invalid username or password!"
    #                 }
    #             ), 401


    #     # Check if producer exists in the "producers" collection
    #     producerExistsRaw = db.producers.find_one({"username": loginInfo["username"]})
    #     producerExists = parse_json(producerExistsRaw)
    #     if (producerExists != None):

    #         # Producer exists, check if password matches
    #         if(str(producerExists["hashedPassword"]) == str(loginInfo["password"])):
    #             return jsonify(
    #                 {   
    #                     "code": 200,
    #                     "id": producerExists["_id"]["$oid"],
    #                     "role": "producer",
    #                     "message": "Authenticated!"
    #                 }
    #             ), 200
            
    #         # Password does not match
    #         else:
    #             return jsonify(
    #                 {   
    #                     "code": 401,
    #                     "message": "Invalid username or password!"
    #                 }
    #             ), 401


    #     # Check if venue exists in the "venues" collection
    #     venueExistsRaw = db.venues.find_one({"username": loginInfo["username"]})
    #     venueExists = parse_json(venueExistsRaw)
    #     if (venueExists != None):

    #         # Venue exists, check if password matches
    #         if(str(venueExists["hashedPassword"]) == str(loginInfo["password"])):
    #             return jsonify(
    #                 {   
    #                     "code": 200,
    #                     "id": venueExists["_id"]["$oid"],
    #                     "role": "venue",
    #                     "message": "Authenticated!"
    #                 }
    #             ), 200
            
    #         # Password does not match
    #         else:
    #             return jsonify(
    #                 {   
    #                     "code": 401,
    #                     "message": "Invalid username or password!"
    #                 }
    #             ), 401
        

    #     # Account does not exist
    #     return jsonify(
    #         {   
    #             "code": 400,
    #             "message": "An account of this username does not exist!"
    #         }
    #     ), 400


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
@blueprint.route('/editPassword/<id>', methods=['POST'])
def editPassword(id):
    # db = g.db
    conn = g.db  # Get the DB connection from g
    cur = conn.cursor()
    data = request.get_json()
    print(data)
    newHash = data['newHash']

    if data["userType"] == "user":
        cur.execute('SELECT * FROM users WHERE id = %s', (id,))
        user = cur.fetchone()
        # userRaw = db.users.find_one({"_id": ObjectId(id)})
    if data["userType"] == "producer":
        cur.execute('SELECT * FROM producers WHERE id = %s', (id,))
        user = cur.fetchone()
        # userRaw = db.producers.find_one({"_id": ObjectId(id)})
    if data["userType"] == "venue":
        cur.execute('SELECT * FROM venues WHERE id = %s', (id,))
        user = cur.fetchone()
        # userRaw = db.venues.find_one({"_id": ObjectId(id)})
        
    if user is None:
        return jsonify(
            {   
                "code": 404,
                "data": {
                    "userID": id
                }
            }
        ), 404
    try: 
        print(user['hashedpassword'])
        print(data['oldHash'])
        print(str(user['hashedpassword'])==str(data['oldHash']))
        # print(user['hashedpasssword'], data['oldHash'])
        if str(user['hashedpassword'])!=str(data['oldHash']):
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
                cur.execute('UPDATE users set hashedpassword = %s WHERE id = %s', (newHash ,id,))
                # updatePassword = db.users.update_one({'_id': ObjectId(id)}, {'$set': {'hashedPassword': data['newHash']}})
            if data["userType"] == "producer":
                cur.execute('UPDATE producers set hashedpassword = %s WHERE id = %s', (newHash ,id,))
                # updatePassword = db.producers.update_one({'_id': ObjectId(id)}, {'$set': {'hashedPassword': data['newHash']}})
            if data["userType"] == "venue":
                cur.execute('UPDATE venues set hashedpassword = %s WHERE id = %s', (newHash ,id,))
                # updatePassword = db.venues.update_one({'_id': ObjectId(id)}, {'$set': {'hashedPassword': data['newHash']}})
            conn.commit()

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
@blueprint.route('/sendResetPin/<id>', methods=['POST'])
def sendResetPin(id):
    # db = g.db
    conn = g.db
    cur = conn.cursor()
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
            # userRaw = db.users.find_one({"_id": ObjectId(id)})
            cur.execute('SELECT * FROM users WHERE id = %s', (id,))
            userRaw = cur.fetchone()
            if userRaw != None:
                cur.execute('UPDATE users set pin = %s WHERE id = %s', (updatePin ,id,))
                # updatePin = db.users.update_one({'_id': ObjectId(id)}, {'$set': {'pin': updatePin}})

        if data["userType"] == "producer":
            # userRaw = db.producers.find_one({"_id": ObjectId(id)})
            cur.execute('SELECT * FROM producers WHERE id = %s', (id,))
            userRaw = cur.fetchone()
            if userRaw != None:
                # updatePin = db.producers.update_one({'_id': ObjectId(id)}, {'$set': {'pin': updatePin}})
                cur.execute('UPDATE producers set pin = %s WHERE id = %s', (updatePin ,id,))                  
            # Need to get the email from producers and assign to variable to send email

        if data["userType"] == "venue":
            cur.execute('SELECT * FROM venues WHERE id = %s', (id,))
            userRaw = cur.fetchone()
            # userRaw = db.venues.find_one({"_id": ObjectId(id)})
            if userRaw != None:
                # updatePin = db.venues.update_one({'_id': ObjectId(id)}, {'$set': {'pin': updatePin}})
                cur.execute('UPDATE venues set pin = %s WHERE id = %s', (updatePin ,id,))
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
        
        conn.commit()

        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(email_address, password)

        message = 'Subject: Drink-X Reset Password\n\n Your pin is {} and expires in 1 hour, please ignore this message if you did not try to reset your password, alternatively, you can email us'.format(pin)
        server.sendmail(email_address, userRaw["email"], message)
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
@blueprint.route('/verifyPin/<id>', methods=['POST'])
def verifyPin(id):
    # db = g.db
    conn = g.db
    cur = conn.cursor()

    data = request.get_json()
    print(data)
    
    time = datetime.now()
    time = time.strftime("%Y-%m-%d %H:%M:%S")
    try:
        # check user type
        if data["userType"] == "user":
            # userRaw = db.users.find_one({"_id": ObjectId(id)})
            cur.execute('SELECT * FROM users WHERE id = %s', (id,))

        if data["userType"] == "producer":
            # userRaw = db.producers.find_one({"_id": ObjectId(id)})
            cur.execute('SELECT * FROM producers WHERE id = %s', (id,))

        if data["userType"] == "venue":
            # userRaw = db.venues.find_one({"_id": ObjectId(id)})
            cur.execute('SELECT * FROM venues WHERE id = %s', (id,))

        userRaw = cur.fetchone()
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
@blueprint.route('/resetPassword/<id>', methods=['POST'])
def resetPassword(id):
    # db = g.db
    conn = g.db
    cur = conn.cursor()

    data = request.get_json()
    print(data)
    email_address = os.getenv('EMAIL_ADDRESS')
    email_password = os.getenv('PASSWORD')
    try:
        # check user type
        if data["userType"] == "user":
            # userRaw = db.users.find_one({"_id": ObjectId(id)})
            cur.execute('SELECT * FROM users WHERE id = %s', (id,))
            # if userRaw != None:
            #     username = userRaw['username']

        if data["userType"] == "producer":
            cur.execute('SELECT * FROM producers WHERE id = %s', (id,))
            # userRaw = db.producers.find_one({"_id": ObjectId(id)})
            # if userRaw != None:
            #     username = userRaw['producerName']

        if data["userType"] == "venue":
            cur.execute('SELECT * FROM venues WHERE id = %s', (id,))
            # userRaw = db.venues.find_one({"_id": ObjectId(id)})
            # if userRaw != None:
            #     username = userRaw['venueName']

        userRaw = cur.fetchone()
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
        username = userRaw['username']
        # get actual pin
        splitPinData = userRaw['pin'].split(',')
        actualPin = splitPinData[0]
        
        # check if pin is correct just in case someone accesses the url
        if str(actualPin) == str(data['pin']):

            # create a new password here

            # Define the set of characters to exclude
            excludeChars = '"\\'  # Double quote and backslash, for example so that it doesnt interefere with code
            filteredPunctuations = ''.join(ch for ch in string.punctuation if ch not in excludeChars)
            characters = string.ascii_letters + string.digits + filteredPunctuations
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
                # updatePassword = db.users.update_one({'_id': ObjectId(id)}, {'$set': {'hashedPassword': str(hash), 'pin':''}})
                cur.execute('UPDATE users set hashedpassword = %s, pin = %s WHERE id = %s', (str(hash), '' ,id,))
            if data["userType"] == "producer":
                # updatePassword = db.producers.update_one({'_id': ObjectId(id)}, {'$set': {'hashedPassword': str(hash), 'pin':''}})
                cur.execute('UPDATE producers set hashedpassword = %s, pin = %s WHERE id = %s', (str(hash), '' ,id,))
            if data["userType"] == "venue":
                # updatePassword = db.venues.update_one({'_id': ObjectId(id)}, {'$set': {'hashedPassword': str(hash), 'pin':''}})
                cur.execute('UPDATE venues set hashedpassword = %s, pin = %s WHERE id = %s', (str(hash), '' ,id,))
            conn.commit()

            # send email containing the password
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(email_address, email_password)

            message = 'Subject: Drink-X Reset Password\n\n Your new password is {}, please email us if you did not authorise this'.format(password)
            server.sendmail(email_address, userRaw["email"], message)
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