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

        else:
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
    


@app.route('/change-subscription-plan', methods=['POST'])
def change_subscription_plan():
    data = json.loads(request.data)
    try:
        subscription = data['subscription']
        subscription_id = data['subscription_id']
        new_price_id = data['new_price_id']
        
        # Retrieve the subscription
        # subscription = stripe.Subscription.retrieve(subscription_id)
        
        # Update the subscription with proration_behavior set to 'none'
        updated_subscription = stripe.Subscription.modify(
            subscription_id,
            proration_behavior='create_prorations',
            items=[{
                'id': subscription['items']['data'][0]['id'],
                'price': new_price_id,
            }]
        )
        
        return jsonify(updated_subscription)
        
    except Exception as e:
        return jsonify(error=str(e)), 403
    

@app.route('/cancel-subscription', methods=['POST'])
def cancel_subscription():
    data = json.loads(request.data)
    try:
        subscription_id = data['subscription_id']
        subscription = data['subscription']
        
        if subscription['schedule']:
            subscription_schedule_id = subscription['schedule']
            subscription_schedule = stripe.SubscriptionSchedule.retrieve(subscription_schedule_id)
            
            current_phase_start = subscription['current_period_start']
            current_phase_end = subscription['current_period_end']
            
            current_phase = subscription_schedule['phases'][-1]
            items = current_phase['items']
            
            canceled_schedule = stripe.SubscriptionSchedule.modify(
                subscription_schedule_id,
                end_behavior='cancel',
                phases=[{
                    'start_date': current_phase_start,
                    'end_date': current_phase_end,
                    'items': items
                }]
            )
            
            return jsonify(canceled_schedule)
        else:
            canceled_subscription = stripe.Subscription.modify(
                subscription_id,
                cancel_at_period_end=True
            )
            
            return jsonify(canceled_subscription)   
    except stripe.error.StripeError as e:
        # Handle general Stripe errors
        return jsonify(error=f"Stripe error: {str(e)}"), 403
    except Exception as e:
        # Handle other exceptions
        return jsonify(error=f"An error occurred: {str(e)}"), 500
    


@app.route('/retrieve-upcoming-invoice', methods=['POST'])
def retrieve_upcoming_invoice():
    data = json.loads(request.data)
    try:
        subscription_id = data['subscription_id']
        
        # Retrieve the upcoming invoice for the subscription
        upcoming_invoice = stripe.Invoice.upcoming(
            subscription=subscription_id
        )
        
        return jsonify(upcoming_invoice)
        
    except stripe.error.StripeError as e:
        # Handle general Stripe errors
        return jsonify(error=f"Stripe error: {str(e)}"), 403
    except Exception as e:
        # Handle other exceptions
        return jsonify(error=f"An error occurred: {str(e)}"), 500


@app.route('/resume-subscription', methods=['POST'])
def resume_subscription():
    data = json.loads(request.data)
    subscription_id = data['subscription_id']
    subscription = data['subscription']

    try:
        if subscription["status"] == 'active' and subscription["cancel_at_period_end"]:
            # Handle the case where the subscription is active but set to end
            updated_subscription = stripe.Subscription.modify(
                subscription_id,
                cancel_at_period_end=False,
            )
            return jsonify({"message": "Subscription extended successfully", "subscription": updated_subscription}), 200

        else:
            return jsonify({"error": "Subscription is not eligible for resumption or extension"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

# -----------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5009)