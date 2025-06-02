import stripe
import os
import json
from flask import Blueprint, g, request, jsonify
from datetime import datetime

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

# Debug flag - set to True to enable detailed logging
DEBUG = True

def log_debug(message, data=None):
    if DEBUG:
        if data:
            print(f"STRIPE_DEBUG: {message}", data)
        else:
            print(f"STRIPE_DEBUG: {message}")
    return {"debug_message": message, "debug_data": data}

def inspect_object(obj, max_depth=2, current_depth=0):
    """Helper function to safely inspect objects of unknown structure"""
    if current_depth >= max_depth:
        return "Max depth reached"
    
    if obj is None:
        return None
        
    if isinstance(obj, dict):
        return {k: inspect_object(v, max_depth, current_depth+1) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [inspect_object(i, max_depth, current_depth+1) for i in obj]
    elif hasattr(obj, '__dict__'):
        try:
            return {k: inspect_object(v, max_depth, current_depth+1) 
                   for k, v in obj.__dict__.items() 
                   if not k.startswith('_')}
        except:
            return str(type(obj))
    else:
        return str(obj)

@blueprint.route('/check-env', methods=['GET'])
def check_env():
    try:
        # Test Stripe connection with a simple API call
        test_result = stripe.Account.retrieve()
        
        debug_info = {
            "stripe_api_key_configured": stripe.api_key is not None,
            "stripe_api_key_length": len(stripe.api_key) if stripe.api_key else 0,
            "stripe_api_key_prefix": stripe.api_key[:4] + "..." if stripe.api_key else None,
            "stripe_test": isinstance(test_result, dict),
            "publishable_key_prefix": os.environ.get('STRIPE_PUBLISHABLE_KEY', '')[:10] + "..." if os.environ.get('STRIPE_PUBLISHABLE_KEY') else "Not set"
        }
        
        return jsonify({"status": "success", "debug_info": debug_info}), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

@blueprint.route('/create-customer', methods=['POST'])
def create_customer():
    db = g.db
    data = request.get_json()
    customer_email = data['customerEmail']
    customer_name = data['customerName']

    print("Creating customer...")

    log_debug("Creating customer with data", {
        "email": customer_email,
        "name": customer_name
    })

    try: 
        log_debug("Calling stripe.Customer.create")
        customer = stripe.Customer.create(
            email=customer_email,
            name=customer_name,
        )
        log_debug("Customer created successfully", {
            "customer_id": customer.id
        })
        return jsonify(customerId=customer.id, debug_info=log_debug("Customer creation response sent")), 200

    except Exception as e:
        error_info = {
            "error_type": type(e).__name__,
            "error_message": str(e),
            "user_message": getattr(e, 'user_message', str(e))
        }
        log_debug("Error creating customer", error_info)
        return jsonify(error={'message': e.user_message}), 400



@blueprint.route('/create-subscription', methods=['POST'])
def create_subscription():
    db = g.db
    data = json.loads(request.data)
    customer_id = data['customerId']
    price_id = data['priceId']

    try:
        # Create the subscription. Note we're expanding the Subscription's
        # latest invoice and that invoice's payment_intent
        # so we can pass it to the front end to confirm the payment
        # Note that expand might be optional due to the update of API version on stripe's end
        # API used to return latest_invoice.payment_intent.client_secret
        subscription = stripe.Subscription.create(
            customer=customer_id,
            items=[{
                'price': price_id,
            }],
            payment_behavior='default_incomplete',
            payment_settings={'save_default_payment_method': 'on_subscription'},
            expand=['latest_invoice.confirmation_secret'],
        )
        
        return jsonify(subscriptionId=subscription.id, clientSecret=subscription.latest_invoice.confirmation_secret.client_secret), 200

    except Exception as e:
        return jsonify(error={'message': e.user_message}), 400
# def create_subscription():
#     db = g.db
#     data = json.loads(request.data)
#     customer_id = data['customerId']
#     price_id = data['priceId']

#     debug_collection = {}

#     log_debug("Creating subscription with data", {
#         "customer_id": customer_id,
#         "price_id": price_id
#     })

#     debug_collection["input_data"] = {
#             "customer_id": customer_id,
#             "price_id": price_id
#         }

#     try:

#         # Check if customer exists first
#         log_debug("Verifying customer exists")
#         try:
#             customer = stripe.Customer.retrieve(customer_id)
#             debug_collection["customer_check"] = {
#                 "exists": True,
#                 "id": customer.id,
#                 "email": customer.email
#             }
#             log_debug("Customer verified", debug_collection["customer_check"])
#         except Exception as e:
#             debug_collection["customer_check"] = {
#                 "exists": False,
#                 "error": str(e)
#             }
#             log_debug("Customer verification failed", debug_collection["customer_check"])
        
#         # Check if price exists
#         log_debug("Verifying price exists")
#         try:
#             price = stripe.Price.retrieve(price_id)
#             debug_collection["price_check"] = {
#                 "exists": True,
#                 "id": price.id,
#                 "active": price.active,
#                 "unit_amount": price.unit_amount,
#                 "currency": price.currency
#             }
#             log_debug("Price verified", debug_collection["price_check"])
#         except Exception as e:
#             debug_collection["price_check"] = {
#                 "exists": False,
#                 "error": str(e)
#             }
#             log_debug("Price verification failed", debug_collection["price_check"])
            

#         # Create the subscription. Note we're expanding the Subscription's
#         # latest invoice and that invoice's payment_intent
#         # so we can pass it to the front end to confirm the payment
#         log_debug("Calling stripe.Subscription.create")
#         subscription = stripe.Subscription.create(
#             customer=customer_id,
#             items=[{
#                 'price': price_id,
#             }],
#             payment_behavior='default_incomplete',
#             payment_settings={'save_default_payment_method': 'on_subscription'},
#             #expand=['latest_invoice.payment_intent'],
#         )

         
#         # Log subscription raw data
#         log_debug("Raw subscription response keys", list(subscription.keys()))
        
#         # Check basic subscription properties
#         debug_collection["subscription_basic"] = {
#             "id": subscription.id,
#             "status": subscription.status,
#             "current_period_start": subscription.current_period_start,
#             "current_period_end": subscription.current_period_end
#         }
#         log_debug("Basic subscription properties", debug_collection["subscription_basic"])
        
#         # Retrieve latest_invoice and payment_intent separately
#         log_debug("Retrieving invoice and payment intent separately")
#         client_secret = None

#         # Get the latest invoice ID from the subscription
#         if hasattr(subscription, 'latest_invoice') and subscription.latest_invoice:
#             latest_invoice_id = subscription.latest_invoice
#             debug_collection["latest_invoice_id"] = latest_invoice_id
            
#             try:
#                 # Retrieve the full invoice
#                 invoice = stripe.Invoice.retrieve(latest_invoice_id)
#                 debug_collection["invoice_retrieved"] = {
#                     "id": invoice.id,
#                     "status": invoice.status
#                 }
                
#                 # If the invoice has a payment_intent, retrieve it
#                 if hasattr(invoice, 'payment_intent') and invoice.payment_intent:
#                     payment_intent_id = invoice.payment_intent
#                     debug_collection["payment_intent_id"] = payment_intent_id
                    
#                     try:
#                         # Retrieve the full payment intent
#                         payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
#                         debug_collection["payment_intent_retrieved"] = {
#                             "id": payment_intent.id,
#                             "status": payment_intent.status
#                         }
                        
#                         # Get the client secret from the payment intent
#                         if hasattr(payment_intent, 'client_secret'):
#                             client_secret = payment_intent.client_secret
#                             debug_collection["client_secret_retrieved"] = True
                        
#                     except Exception as e:
#                         debug_collection["payment_intent_retrieval_error"] = str(e)
#                         log_debug("Error retrieving payment intent", str(e))
            
#             except Exception as e:
#                 debug_collection["invoice_retrieval_error"] = str(e)
#                 log_debug("Error retrieving invoice", str(e))

#         # Check if latest_invoice exists
#         has_latest_invoice = hasattr(subscription, 'latest_invoice') and subscription.latest_invoice is not None
#         debug_collection["has_latest_invoice"] = has_latest_invoice
        
#         if has_latest_invoice:
#             debug_collection["latest_invoice"] = {
#                 "id": subscription.latest_invoice.id,
#                 "total": subscription.latest_invoice.total,
#                 "status": subscription.latest_invoice.status,
#             }
            
#             # Check if payment_intent exists
#             has_payment_intent = (hasattr(subscription.latest_invoice, 'payment_intent') 
#                                 and subscription.latest_invoice.payment_intent is not None)
#             debug_collection["has_payment_intent"] = has_payment_intent
            
#             if has_payment_intent:
#                 debug_collection["payment_intent"] = {
#                     "id": subscription.latest_invoice.payment_intent.id,
#                     "status": subscription.latest_invoice.payment_intent.status,
#                     "amount": subscription.latest_invoice.payment_intent.amount,
#                     "has_client_secret": hasattr(subscription.latest_invoice.payment_intent, 'client_secret')
#                 }

#         # Detailed logging of the subscription structure
#         log_debug("Checking subscription structure", {
#             "has_latest_invoice": hasattr(subscription, 'latest_invoice'),
#             "invoice_keys": dir(subscription.latest_invoice) if hasattr(subscription, 'latest_invoice') else [],
#             "has_payment_intent": hasattr(subscription, 'latest_invoice') and hasattr(subscription.latest_invoice, 'payment_intent'),
#             "subscription_status": subscription.status,
#         })

#          # Extremely detailed object inspection
#         subscription_dict = inspect_object(subscription, max_depth=3)
#         debug_collection["subscription_structure"] = subscription_dict
#         log_debug("Full subscription structure", subscription_dict)


#         # Check if payment_intent exists before trying to access it
#         if hasattr(subscription, 'latest_invoice') and hasattr(subscription.latest_invoice, 'payment_intent'):
#             if subscription.latest_invoice.payment_intent is not None:
#                 client_secret = subscription.latest_invoice.payment_intent.client_secret
#                 debug_data = {
#                     "subscription_id": subscription.id,
#                     "client_secret_prefix": client_secret[:10] + "..." if client_secret else None,
#                     "payment_intent_id": subscription.latest_invoice.payment_intent.id
#                 }
#                 log_debug("Subscription created with payment intent", debug_data)
                
#                 return jsonify(
#                     subscriptionId=subscription.id, 
#                     clientSecret=client_secret,
#                     debug_info=debug_data
#                 ), 200
#             else:
#                 error_info = {
#                     "error_type": "NullPaymentIntent",
#                     "error_message": "Subscription created but payment_intent is null",
#                     "subscription_id": subscription.id
#                 }
#                 log_debug("Error: Null payment_intent in subscription", error_info)
#                 return jsonify(error={'message': 'Payment setup failed. Please try again.'}, 
#                               debug_info=error_info), 400
#         else:
#             error_info = {
#                 "error_type": "MissingPaymentIntent",
#                 "error_message": "Subscription created but payment_intent is missing",
#                 "subscription_id": subscription.id
#             }
#             log_debug("Error: Missing payment_intent in subscription", error_info)
#             return jsonify(error={'message': 'Payment setup failed. Please try again.'}, 
#                           debug_info=error_info), 400

#     except Exception as e:
#         error_info = {
#             "error_type": type(e).__name__,
#             "error_message": str(e),
#             "user_message": getattr(e, 'user_message', str(e))
#         }
#         log_debug("Error creating subscription", error_info)
#         return jsonify(error={'message': getattr(e, 'user_message', str(e))}, debug_info=error_info), 400


@blueprint.route('/retrieve-latest-subscription', methods=['POST'])
def retrieve_latest_subscription():
    db = g.db
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


@blueprint.route('/retrieve-payment-method', methods=['POST'])
def retrieve_payment_method():
    db = g.db
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
    

@blueprint.route('/cancel-subscription', methods=['POST'])
def cancel_subscription():
    db = g.db
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
    


@blueprint.route('/retrieve-upcoming-invoice', methods=['POST'])
def retrieve_upcoming_invoice():
    db = g.db
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


@blueprint.route('/resume-subscription', methods=['POST'])
def resume_subscription():
    db = g.db
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
    