import stripe
stripe.api_key = "sk_test_51PV6CNDnjokAiSGzSjzjlwoN9jseVPhOi90H7BlGP0wMmfJ1Kx7jDzAW1xQAS9NxpI1MebZibT5kIfaETzrncq8l006ToZRlJ1"


import bson
import json
from bson import json_util
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS

from bson.objectid import ObjectId

from gridfs import GridFS
import os
from datetime import datetime

from dotenv import load_dotenv
import os

from adminFunctions import hash_password

app = Flask(__name__)
CORS(app)  # Allow all requests

load_dotenv()
app.config["MONGO_URI"] = os.getenv('MONGO_DB_URL')
db = PyMongo(app).db

mongo = PyMongo(app)
fs = GridFS(mongo.db)

@app.route('/create-customer', methods=['POST'])
def create_customer():
    data = request.get_json()
    customer_email = data['customerEmail']
    customer_name = data['customerName']
    # address = data['address']

    try: 
        customer = stripe.Customer.create(
            email=customer_email,
            name=customer_name,
            # shipping={
            #     "address": address,
            #     "name": customer_name,
            # },
            # address=address,
        )
        return jsonify(customerId=customer.id), 200

    except Exception as e:
        return jsonify(error={'message': e.user_message}), 400



@app.route('/create-subscription', methods=['POST'])
def create_subscription():
    data = json.loads(request.data)
    customer_id = data['customerId']
    price_id = data['priceId']

    try:
        # Create the subscription. Note we're expanding the Subscription's
        # latest invoice and that invoice's payment_intent
        # so we can pass it to the front end to confirm the payment
        subscription = stripe.Subscription.create(
            customer=customer_id,
            items=[{
                'price': price_id,
            }],
            payment_behavior='default_incomplete',
            payment_settings={'save_default_payment_method': 'on_subscription'},
            expand=['latest_invoice.payment_intent'],
        )
        return jsonify(subscriptionId=subscription.id, clientSecret=subscription.latest_invoice.payment_intent.client_secret), 200

    except Exception as e:
        return jsonify(error={'message': e.user_message}), 400




# -----------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5009)