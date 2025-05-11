import stripe
import os
import json
from flask import Blueprint, g, request, jsonify
from datetime import datetime
from dotenv import load_dotenv 

# Load environment variables from .env file
load_dotenv()  # Add this line

# Debug print - add this line
stripe_key = os.environ.get('STRIPE_SECRET_KEY')
print(f"STRIPE_SECRET_KEY at module level: '{stripe_key}'")

# Add this line to initialize Stripe with your API key
stripe.api_key = stripe_key

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

@blueprint.route('/create-customer', methods=['POST'])
def create_customer():
    db = g.db
    data = request.get_json()
    customer_email = data['customerEmail']
    customer_name = data['customerName']

    # Enhanced debug message
    api_key = os.environ.get('STRIPE_SECRET_KEY')
    debug_message = f"Creating customer with email: {customer_email}, name: {customer_name}. Using API key: '{api_key}'"
    print(debug_message)

    try: 
        # Get API key directly from env
        if not api_key:
            # If API key is missing, return a specific error
            error_message = "STRIPE_SECRET_KEY environment variable is not set or empty"
            print(error_message)
            return jsonify(error={
                'message': 'API key missing',
                'debug_message': error_message
            }), 400

        # Pass API key explicitly to override any global settings
        customer = stripe.Customer.create(
            api_key=api_key,
            email=customer_email,
            name=customer_name,
        )
        return jsonify(
            customerId=customer.id,
            debug_message=debug_message,
            api_key_status="API key is present and valid"
        ), 200

    except Exception as e:
        error_message = f"Customer creation error: {str(e)}"
        print(error_message)
        return jsonify(error={
            'message': getattr(e, 'user_message', str(e)),
            'debug_message': error_message,
            'api_key_status': f"API key {'is present' if api_key else 'is missing'}"
        }), 400



@blueprint.route('/create-subscription', methods=['POST'])
def create_subscription():
    db = g.db
    data = json.loads(request.data)
    customer_id = data['customerId']
    price_id = data['priceId']
    debug_message = f"Creating subscription with customer_id: {customer_id}, price_id: {price_id}"
    print(debug_message) # for bug fixing
    try:
        api_key = os.environ.get('STRIPE_SECRET_KEY')
        # Create the subscription. Note we're expanding the Subscription's
        # latest invoice and that invoice's payment_intent
        # so we can pass it to the front end to confirm the payment
        subscription = stripe.Subscription.create(
            api_key=api_key,  # Add this line
            customer=customer_id,
            items=[{
                'price': price_id,
            }],
            payment_behavior='default_incomplete',
            payment_settings={'save_default_payment_method': 'on_subscription'},
        )
         # Check if payment_intent exists before trying to access it
        if hasattr(subscription, 'latest_invoice') and hasattr(subscription.latest_invoice, 'payment_intent') and subscription.latest_invoice.payment_intent:
            client_secret = subscription.latest_invoice.payment_intent.client_secret
        else:
            # Create a SetupIntent as fallback if there's no payment_intent
            setup_intent = stripe.SetupIntent.create(
                api_key=api_key,
                customer=customer_id,
                payment_method_types=['card'],
            )
            client_secret = setup_intent.client_secret
            
        return jsonify(subscriptionId=subscription.id, clientSecret=client_secret), 200

    except Exception as e:
        error_message = f"Subscription creation error: {str(e)}"
        detailed_error = ""
        print(error_message)
        if hasattr(e, 'json_body'):
            detailed_error = f"Detailed error: {e.json_body}"
            print(detailed_error)
        return jsonify(error={
            'message': getattr(e, 'user_message', str(e)),
            'debug_message': error_message,
            'detailed_error': detailed_error
        }), 400


@blueprint.route('/retrieve-latest-subscription', methods=['POST'])
def retrieve_latest_subscription():
    db = g.db
    data = json.loads(request.data)
    try:
        customer_id = data['customerId']
        api_key = os.environ.get('STRIPE_SECRET_KEY')
        subscriptions = stripe.Subscription.list(
            customer=customer_id,
            api_key=api_key,  # Add this line
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


@blueprint.route('/retrieve-payment-method', methods=['POST'])
def retrieve_payment_method():
    db = g.db
    data = json.loads(request.data)
    try:
        subscription = data['subscription']
        print(subscription)
        default_payment_method_id = subscription['default_payment_method']
        
        if default_payment_method_id:
            api_key = os.environ.get('STRIPE_SECRET_KEY')
            payment_method = stripe.PaymentMethod.retrieve(default_payment_method_id,
                api_key=api_key  # Add this line
                )
            
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



@blueprint.route('/retrieve-subscription-details', methods=['POST'])
def retrieve_subscription_details():
    db = g.db
    data = json.loads(request.data)
    try:
        subscription = data['subscription']
        
        for item in subscription['items']['data']:
            price_id = item['price']['id']
            price = item['price']['unit_amount'] / 100  # Convert from cents to dollars
            product_id = item['price']['product']
            interval = item['price']['recurring']['interval']  # Monthly or yearly
            
            # Retrieve product details to get the name
            api_key = os.environ.get('STRIPE_SECRET_KEY')
            product = stripe.Product.retrieve(
                product_id,
                api_key=api_key  # Add this line
                )
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
    


@blueprint.route('/change-subscription-plan', methods=['POST'])
def change_subscription_plan():
    db = g.db
    data = json.loads(request.data)
    try:
        subscription = data['subscription']
        subscription_id = data['subscription_id']
        new_price_id = data['new_price_id']
        
        # Retrieve the subscription
        # subscription = stripe.Subscription.retrieve(subscription_id)
        
        # Update the subscription with proration_behavior set to 'none'
        api_key = os.environ.get('STRIPE_SECRET_KEY')
        updated_subscription = stripe.Subscription.modify(
            subscription_id,
            api_key=api_key,  # Add this line
            proration_behavior='create_prorations',
            items=[{
                'id': subscription['items']['data'][0]['id'],
                'price': new_price_id,
            }]
        )
        
        return jsonify(updated_subscription)
        
    except Exception as e:
        return jsonify(error=str(e)), 403
    

@blueprint.route('/cancel-subscription', methods=['POST'])
def cancel_subscription():
    db = g.db
    data = json.loads(request.data)
    try:
        subscription_id = data['subscription_id']
        subscription = data['subscription']
        
        if subscription['schedule']:
            subscription_schedule_id = subscription['schedule']
            api_key = os.environ.get('STRIPE_SECRET_KEY')
            subscription_schedule = stripe.SubscriptionSchedule.retrieve(
                subscription_schedule_id,
                api_key=api_key 
                )
            
            current_phase_start = subscription['current_period_start']
            current_phase_end = subscription['current_period_end']
            
            current_phase = subscription_schedule['phases'][-1]
            items = current_phase['items']
            
            api_key = os.environ.get('STRIPE_SECRET_KEY')
            canceled_schedule = stripe.SubscriptionSchedule.modify(
                subscription_schedule_id,
                api_key=api_key, 
                end_behavior='cancel',
                phases=[{
                    'start_date': current_phase_start,
                    'end_date': current_phase_end,
                    'items': items
                }]
            )
            
            return jsonify(canceled_schedule)
        else:
            api_key = os.environ.get('STRIPE_SECRET_KEY')
            canceled_subscription = stripe.Subscription.modify(
                subscription_id,
                 api_key=api_key,
                cancel_at_period_end=True
            )
            
            return jsonify(canceled_subscription)   
    except stripe.error.StripeError as e:
        # Handle general Stripe errors
        return jsonify(error=f"Stripe error: {str(e)}"), 403
    except Exception as e:
        # Handle other exceptions
        return jsonify(error=f"An error occurred: {str(e)}"), 500
    


@blueprint.route('/retrieve-upcoming-invoice', methods=['POST'])
def retrieve_upcoming_invoice():
    db = g.db
    data = json.loads(request.data)
    try:
        subscription_id = data['subscription_id']
        
        # Retrieve the upcoming invoice for the subscription
        api_key = os.environ.get('STRIPE_SECRET_KEY')
        upcoming_invoice = stripe.Invoice.upcoming(
            api_key=api_key,  
            subscription=subscription_id
        )
        
        return jsonify(upcoming_invoice)
        
    except stripe.error.StripeError as e:
        # Handle general Stripe errors
        return jsonify(error=f"Stripe error: {str(e)}"), 403
    except Exception as e:
        # Handle other exceptions
        return jsonify(error=f"An error occurred: {str(e)}"), 500


@blueprint.route('/resume-subscription', methods=['POST'])
def resume_subscription():
    db = g.db
    data = json.loads(request.data)
    subscription_id = data['subscription_id']
    subscription = data['subscription']

    try:
        if subscription["status"] == 'active' and subscription["cancel_at_period_end"]:
            # Handle the case where the subscription is active but set to end
            api_key = os.environ.get('STRIPE_SECRET_KEY')
            updated_subscription = stripe.Subscription.modify(
                subscription_id,
                api_key=api_key, 
                cancel_at_period_end=False,
            )
            return jsonify({"message": "Subscription extended successfully", "subscription": updated_subscription}), 200

        else:
            return jsonify({"error": "Subscription is not eligible for resumption or extension"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Add this entire new route at the end of your payment.py file
@blueprint.route('/check-env', methods=['GET'])
def check_env():
    """Debug endpoint to check environment variables"""
    api_key = os.environ.get('STRIPE_SECRET_KEY')
    
    # Don't return the full key, just the first few and last few chars
    masked_key = "Not set"
    if api_key:
        if len(api_key) > 10:
            masked_key = api_key[:4] + "..." + api_key[-4:]
        else:
            masked_key = "Too short to display safely"
            
    env_info = {
        "STRIPE_SECRET_KEY_status": "Present" if api_key else "Missing",
        "STRIPE_SECRET_KEY_preview": masked_key,
        "ENV_VARS": list(os.environ.keys())  # List all env var names (not values)
    }
    
    return jsonify(env_info), 200