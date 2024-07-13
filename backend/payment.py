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

    try: 
        customer = stripe.Customer.create(
            email=customer_email,
            name=customer_name,
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


@app.route('/retrieve-latest-subscription', methods=['POST'])
def retrieve_latest_subscription():
    data = json.loads(request.data)
    try:
        customer_id = data['customerId']
        
        subscriptions = stripe.Subscription.list(
            customer=customer_id,
            limit=1,
            status='active',
        )

        if not subscriptions['data']:
            return jsonify(error="No active subscriptions found for this customer"), 404
        
        latest_subscription = max(subscriptions['data'], key=lambda s: s['created'])
        return jsonify(latest_subscription)
        
    except Exception as e:
        return jsonify(error=str(e)), 403


@app.route('/retrieve-payment-method', methods=['POST'])
def retrieve_payment_method():
    data = json.loads(request.data)
    try:
        subscription = data['subscription']
        print(subscription)
        default_payment_method_id = subscription['default_payment_method']
        
        if default_payment_method_id:
            payment_method = stripe.PaymentMethod.retrieve(default_payment_method_id)
            
            payment_method_info = {
                "id": payment_method['id'],
                "brand": payment_method.card['brand'],
                "last4": payment_method.card['last4'],
                "exp_month": payment_method.card['exp_month'],
                "exp_year": payment_method.card['exp_year']
            }
            
            return jsonify(payment_method_info)
        else:
            return jsonify(error="No default payment method found for the latest subscription"), 404
        
    except Exception as e:
        return jsonify(error=str(e)), 403



@app.route('/retrieve-subscription-details', methods=['POST'])
def retrieve_subscription_details():
    data = json.loads(request.data)
    try:
        subscription = data['subscription']
        
        for item in subscription['items']['data']:
            price_id = item['price']['id']
            price = item['price']['unit_amount'] / 100  # Convert from cents to dollars
            product_id = item['price']['product']
            interval = item['price']['recurring']['interval']  # Monthly or yearly
            
            # Retrieve product details to get the name
            product = stripe.Product.retrieve(product_id)
            subscription_name = product['name']
            
            # Get the next billing date
            next_billing_date_unix = subscription['current_period_end']
            next_billing_date = datetime.fromtimestamp(next_billing_date_unix).isoformat()
            
            subscription_details = {
                "subscription_id": subscription['id'],
                "price_id": price_id,
                "subscription_name": subscription_name,
                "price": price,
                "currency": item['price']['currency'],
                "next_billing_date": next_billing_date,
                "interval": interval  # Monthly or yearly
            }
                    
        return jsonify(subscription_details)
        
    except Exception as e:
        return jsonify(error=str(e)), 403



# -----------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5009)