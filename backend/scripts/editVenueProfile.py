# Port: 5300
# Routes: /editDetails (POST), /addUpdates (POST), /sendQuestions (POST), /sendAnswers (POST), /likeUpdates (POST), /unlikeUpdates (POST)
#         /editAddress (POST), /editOpeningHours (POST), /editPublicHolidays (POST), /editReservationDetails (POST), /addListingToMenu (POST)
#         /editSectionName (PUT), /editMenu (POST), /updateVenueStatus (POST), /editUpdate (POST), /deleteUpdate (POST), /editQA (POST)
#         /deleteQA (POST), /addProfileCount (POST), /addNewProfileCount (POST), /deleteMenuItem (DELETE), /updateVenueClaimStatus (POST)
# -----------------------------------------------------------------------------------------

import os
import s3Images
import s3pdfMenu
from flask import Blueprint, g, request, jsonify
from datetime import datetime
from scripts import pointsHelperFunc, badge_helpers, notifications
import re
from typing import Dict, Any, Optional, Tuple

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

# TODO: Create function using BOTO Library to upload images to the S3 bucket
# TODO: Create function using BOTO Library to delete images from the S3 bucket

# Amenities field mapping for dynamic processing
AMENITIES_FIELDS = [
    'paymentCash', 'paymentVisa', 'paymentMasterCard', 'paymentAmericanExpress',
    'paymentDiscover', 'paymentApplePay', 'paymentPayNow', 'paymentGooglePay',
    'paymentSamsungPay', 'beverageCocktails', 'beverageWine', 'beverageBeer',
    'beverageWhisky', 'beverageBrandy', 'beverageTequila', 'beverageMezcal',
    'beverageRum', 'beverageSake', 'beverageShochu', 'beverageSoju',
    'beverageBaijiu', 'beverageGin', 'beverageVodka', 'beverageAbsinthe',
    'beverageArrack', 'foodServed', 'outdoorSeating', 'indoorSeating',
    'petFriendly', 'childFriendly', 'familyFriendly', 'smokeFriendly',
    'wheelchairAccessibility', 'freeWiFi', 'happyHourDrinks', 'liveMusic',
    'barGames', 'sommelierService', 'deliveryAvailable', 'lgbtqFriendly',
    'reservationsRequired', 'membershipRequired', 'inStoreScheduling'
]

def process_image_upload(form_data: Dict[str, Any], current_photo: Optional[str]) -> Optional[str]:
    """Handle image upload processing."""
    if not form_data.get('image64'):
        return current_photo
    
    try:
        # Clean base64 string
        base64_string = re.sub(r'^data:image\/[a-zA-Z]+;base64,', '', form_data['image64'])
        
        # Delete old image if exists
        if current_photo:
            s3Images.deleteImageFromS3(current_photo)
        
        # Upload new image
        return s3Images.uploadBase64ImageToS3(base64_string)
    
    except Exception as e:
        print(f"Error processing image upload: {e}")
        return current_photo

def get_venue_by_id(cursor, venue_id: int) -> Optional[Dict[str, Any]]:
    """Retrieve venue by ID."""
    cursor.execute('SELECT * FROM venues WHERE id = %s', (venue_id,))
    return cursor.fetchone()

def validate_venue_data(data: Dict[str, Any]) -> Tuple[bool, str]:
    """Validate required venue data fields."""
    try:
        venue_id = int(data.get('venueId'))
        if venue_id <= 0:
            return False, "Invalid venue ID"
        return True, ""
    except (ValueError, TypeError):
        return False, "Venue ID is required and must be a valid integer"

def extract_venue_data(form_data: Dict[str, Any]) -> Dict[str, Any]:
    """Extract and clean venue data from form."""
    return {
        'venueName': form_data.get('venueName', '').strip(),
        'venueType': form_data.get('venueType', '').strip(),
        'venueDesc': form_data.get('venueDesc', '').strip(),
        'originLocation': form_data.get('originLocation', '').strip(),
        'yearOpened': form_data.get('yearOpened') or None,
        'openForReservations': form_data.get('openForReservations', 'false').lower() == 'true',
        'website': form_data.get('website', '').strip(),
        'instagram': form_data.get('instagram', '').strip(),
        'facebook': form_data.get('facebook', '').strip(),
        'tiktok': form_data.get('tiktok', '').strip(),
        'email': form_data.get('email', '').strip(),
        'phoneNumber': form_data.get('phoneNumber', '').strip(),
        'whatsappNumber': form_data.get('whatsappNumber', '').strip()
    }

def update_venue_details(cursor, venue_data: Dict[str, Any], photo_url: str, venue_id: int):
    """Update venue basic information."""
    update_query = """
        UPDATE venues 
        SET "venueName" = %s, "venueType" = %s, "venueDesc" = %s, 
            "originLocation" = %s, "yearOpened" = %s, "openForReservations" = %s,
            "website" = %s, "instagram" = %s, "facebook" = %s, "tiktok" = %s,
            "email" = %s, "phoneNumber" = %s, "whatsappNumber" = %s, "photo" = %s
        WHERE id = %s
    """
    
    cursor.execute(update_query, (
        venue_data['venueName'], venue_data['venueType'], venue_data['venueDesc'],
        venue_data['originLocation'], venue_data['yearOpened'], venue_data['openForReservations'],
        venue_data['website'], venue_data['instagram'], venue_data['facebook'], venue_data['tiktok'],
        venue_data['email'], venue_data['phoneNumber'], venue_data['whatsappNumber'], 
        photo_url, venue_id
    ))

def extract_amenities_data(form_data: Dict[str, Any]) -> Dict[str, Any]:
    """Extract amenities data from form with dynamic field processing."""
    amenities = {}
    
    # Process boolean fields
    for field in AMENITIES_FIELDS:
        amenities[field] = form_data.get(field, 'false').lower() == 'true'
    
    # Handle text field
    amenities['otherAmenities'] = form_data.get('otherAmenities', '').strip()
    
    return amenities

def upsert_venue_amenities(cursor, amenities: Dict[str, Any], venue_id: int):
    """Insert or update venue amenities using efficient upsert."""
    if not amenities:
        return
    
    # Check if amenities exist
    cursor.execute('SELECT EXISTS(SELECT 1 FROM "venueAmenities" WHERE "venueId" = %s)', (venue_id,))
    result = cursor.fetchone()
    exists = result['exists'] if isinstance(result, dict) else result[0]
    
    # Prepare amenities values
    amenities_values = [amenities.get(field, False) for field in AMENITIES_FIELDS]
    amenities_values.append(amenities.get('otherAmenities', ''))
    
    if exists:
        # Update existing record
        set_clause = ', '.join([f'"{field}" = %s' for field in AMENITIES_FIELDS + ['otherAmenities']])
        update_query = f'UPDATE "venueAmenities" SET {set_clause} WHERE "venueId" = %s'
        cursor.execute(update_query, amenities_values + [venue_id])
    else:
        # Insert new record
        fields = '", "'.join(['venueId'] + AMENITIES_FIELDS + ['otherAmenities'])
        placeholders = ', '.join(['%s'] * (len(AMENITIES_FIELDS) + 2))
        insert_query = f'INSERT INTO "venueAmenities" ("{fields}") VALUES ({placeholders})'
        cursor.execute(insert_query, [venue_id] + amenities_values)

@blueprint.route('/venueInfo', methods=['POST'])
def updateVenueInformation():
    """Main endpoint for updating venue details."""
    conn = g.db
    cursor = conn.cursor()

    try:
        # Validate input data
        form_data = request.form.to_dict()
        is_valid, error_message = validate_venue_data(form_data)
        if not is_valid:
            return jsonify({"code": 400, "message": error_message}), 400
        
        venue_id = int(form_data['venueId'])
        
        # Check if venue exists
        existing_venue = get_venue_by_id(cursor, venue_id)
        if not existing_venue:
            return jsonify({"code": 404, "message": "Venue not found."}), 404
        
        # Extract and process data
        venue_data = extract_venue_data(form_data)
        amenities_data = extract_amenities_data(form_data)
        
        # Handle image upload
        photo_url = process_image_upload(form_data, existing_venue.get('photo'))
        
        # Update venue details
        update_venue_details(cursor, venue_data, photo_url, venue_id)
        
        # Update amenities if provided
        if amenities_data:
            upsert_venue_amenities(cursor, amenities_data, venue_id)
        
        # Commit transaction
        conn.commit()
        
        return jsonify({
            "code": 201,
            "message": "Updated profile successfully!"
        }), 201
        
    except ValueError as e:
        conn.rollback()
        return jsonify({"code": 400, "message": f"Invalid data: {str(e)}"}), 400
    
    except Exception as e:
        conn.rollback()
        print(f"Error updating venue: {e}")
        import traceback
        traceback.print_exc()
        
        return jsonify({
            "code": 500,
            "message": "An error occurred updating profile!"
        }), 500
    
    finally:
        cursor.close()


# -----------------------------------------------------------------------------------------
# [POST] Edit venue profile
# - Update venue profile with new details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/editDetails', methods=['POST'])
def editDetails():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()

    venueID = int(data['venueID'])
    venueName = data['venueName']
    venueType = data['venueType']
    venueDesc = data['venueDesc']
    originLocation = data['originLocation']
    image64 = data.get('image64', '')
    yearOpened = data.get('yearOpened', None)
    openForReservations = data.get('openForReservations')
    website = data.get('website', '')
    instagram = data.get('instagram', '')
    facebook = data.get('facebook', '')
    tiktok = data.get('tiktok', '')
    email = data.get('email', '')
    phoneNumber = data.get('phoneNumber', '')
    whatsappNumber = data.get('whatsappNumber', '')
    amenities = data.get('amenities', {})

    try:
        # Find existing venue
        cur.execute('SELECT * FROM venues WHERE id = %s', (venueID,))
        existingVenue = cur.fetchone()

        if existingVenue:
            if data.get('image64'):  # Only process image if one was provided
                # Only delete old image if we're replacing it
                if existingVenue['photo']:
                    s3Images.deleteImageFromS3(existingVenue['photo'])
                
                # Process and upload the new image
                base64_string = re.sub(r'^data:image\/[a-zA-Z]+;base64,', '', data['image64'])
                image64 = s3Images.uploadBase64ImageToS3(base64_string)
            else:
                # Keep existing photo if no new one was provided
                image64 = existingVenue['photo']
            # Update the venue details in the database
            cur.execute(
                """
                UPDATE venues 
                SET 
                    "venueName" = %s,
                    "venueType" = %s,
                    "venueDesc" = %s,
                    "originLocation" = %s,
                    "yearOpened" = %s,
                    "openForReservations" = %s,
                    "website" = %s,
                    "instagram" = %s,
                    "facebook" = %s,
                    "tiktok" = %s,
                    "email" = %s,
                    "phoneNumber" = %s,
                    "whatsappNumber" = %s,
                    "photo" = %s
                WHERE id = %s
                """,
                (venueName, venueType, venueDesc, originLocation, yearOpened, openForReservations, 
                 website, instagram, facebook, tiktok, email, phoneNumber, whatsappNumber, image64, venueID)
            )

            # Update or insert amenities data
            if amenities:
                # Check if amenities record exists
                cur.execute('SELECT id FROM "venueAmenities" WHERE "venueId" = %s', (venueID,))
                existing_amenities = cur.fetchone()

                amenities_data = (
                    amenities.get('paymentCash', False),
                    amenities.get('paymentVisa', False),
                    amenities.get('paymentMasterCard', False),
                    amenities.get('paymentAmericanExpress', False),
                    amenities.get('paymentDiscover', False),
                    amenities.get('paymentApplePay', False),
                    amenities.get('paymentPayNow', False),
                    amenities.get('paymentGooglePay', False),
                    amenities.get('paymentSamsungPay', False),
                    amenities.get('beverageCocktails', False),
                    amenities.get('beverageWine', False),
                    amenities.get('beverageBeer', False),
                    amenities.get('beverageWhisky', False),
                    amenities.get('beverageBrandy', False),
                    amenities.get('beverageTequila', False),
                    amenities.get('beverageMezcal', False),
                    amenities.get('beverageRum', False),
                    amenities.get('beverageSake', False),
                    amenities.get('beverageShochu', False),
                    amenities.get('beverageSoju', False),
                    amenities.get('beverageBaijiu', False),
                    amenities.get('beverageGin', False),
                    amenities.get('beverageVodka', False),
                    amenities.get('beverageAbsinthe', False),
                    amenities.get('beverageArrack', False),
                    amenities.get('foodServed', False),
                    amenities.get('outdoorSeating', False),
                    amenities.get('indoorSeating', False),
                    amenities.get('petFriendly', False),
                    amenities.get('childFriendly', False),
                    amenities.get('familyFriendly', False),
                    amenities.get('smokeFriendly', False),
                    amenities.get('wheelchairAccessibility', False),
                    amenities.get('freeWiFi', False),
                    amenities.get('happyHourDrinks', False),
                    amenities.get('liveMusic', False),
                    amenities.get('barGames', False),
                    amenities.get('sommelierService', False),
                    amenities.get('deliveryAvailable', False),
                    amenities.get('lgbtqFriendly', False),
                    amenities.get('reservationsRequired', False),
                    amenities.get('membershipRequired', False),
                    amenities.get('inStoreScheduling', False),
                    amenities.get('otherAmenities', '')
                )

                if existing_amenities:
                    # Update existing amenities
                    cur.execute(
                        """
                        UPDATE "venueAmenities" 
                        SET 
                            "paymentCash" = %s,
                            "paymentVisa" = %s,
                            "paymentMasterCard" = %s,
                            "paymentAmericanExpress" = %s,
                            "paymentDiscover" = %s,
                            "paymentApplePay" = %s,
                            "paymentPayNow" = %s,
                            "paymentGooglePay" = %s,
                            "paymentSamsungPay" = %s,
                            "beverageCocktails" = %s,
                            "beverageWine" = %s,
                            "beverageBeer" = %s,
                            "beverageWhisky" = %s,
                            "beverageBrandy" = %s,
                            "beverageTequila" = %s,
                            "beverageMezcal" = %s,
                            "beverageRum" = %s,
                            "beverageSake" = %s,
                            "beverageShochu" = %s,
                            "beverageSoju" = %s,
                            "beverageBaijiu" = %s,
                            "beverageGin" = %s,
                            "beverageVodka" = %s,
                            "beverageAbsinthe" = %s,
                            "beverageArrack" = %s,
                            "foodServed" = %s,
                            "outdoorSeating" = %s,
                            "indoorSeating" = %s,
                            "petFriendly" = %s,
                            "childFriendly" = %s,
                            "familyFriendly" = %s,
                            "smokeFriendly" = %s,
                            "wheelchairAccessibility" = %s,
                            "freeWiFi" = %s,
                            "happyHourDrinks" = %s,
                            "liveMusic" = %s,
                            "barGames" = %s,
                            "sommelierService" = %s,
                            "deliveryAvailable" = %s,
                            "lgbtqFriendly" = %s,
                            "reservationsRequired" = %s,
                            "membershipRequired" = %s,
                            "inStoreScheduling" = %s,
                            "otherAmenities" = %s
                        WHERE "venueId" = %s
                        """,
                        amenities_data + (venueID,)
                    )
                else:
                    # Insert new amenities record
                    cur.execute(
                        """
                        INSERT INTO "venueAmenities" 
                        ("venueId", "paymentCash", "paymentVisa", "paymentMasterCard", "paymentAmericanExpress", "paymentDiscover",
                         "paymentApplePay", "paymentPayNow", "paymentGooglePay", "paymentSamsungPay", "beverageCocktails",
                         "beverageWine", "beverageBeer", "beverageWhisky", "beverageBrandy", "beverageTequila", "beverageMezcal",
                         "beverageRum", "beverageSake", "beverageShochu", "beverageSoju", "beverageBaijiu", "beverageGin", 
                         "beverageVodka", "beverageAbsinthe", "beverageArrack", "foodServed", "outdoorSeating", "indoorSeating",
                         "petFriendly", "childFriendly", "familyFriendly", "smokeFriendly", "wheelchairAccessibility",
                         "freeWiFi", "happyHourDrinks", "liveMusic", "barGames", "sommelierService", "deliveryAvailable", 
                         "lgbtqFriendly", "reservationsRequired", "membershipRequired", "inStoreScheduling", "otherAmenities")
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        (venueID,) + amenities_data
                    )

            conn.commit()

            return jsonify(
                {
                    "code": 201,
                    "message": "Updated profile successfully!"
                }
            ), 201
        
        else:
            return jsonify(
                {
                    "code": 404,
                    "message": "Venue not found."
                }
            ), 404
        
    except Exception as e:
        import traceback
        traceback.print_exc()

        return jsonify(
            {
                "code": 500,
                "message": "An error occurred updating profile!"
            }
        ), 500
    
    finally:
        cur.close()

# -----------------------------------------------------------------------------------------
# [POST] Add updates to venue profile
# - Add updates to the venue profile
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/addUpdates', methods=['POST'])
def addUpdates():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()
    print(data)
    
    venueID = int(data['venueID'])
    date = datetime.strptime(data['date'], "%Y-%m-%dT%H:%M:%S.%fZ")
    text = data['text']
    image64 = data.get('image64', '')

    try:
        # Find existing venue
        cur.execute('SELECT * FROM venues WHERE id = %s', (venueID,))
        existingVenue = cur.fetchone()
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if existingVenue:
            if image64:
                base64_string = re.sub(r'^data:image\/[a-zA-Z]+;base64,', '', image64)
                image64 = s3Images.uploadBase64ImageToS3(base64_string)

            # Update the venue details in the database
            cur.execute(
                """
                INSERT INTO "venuesUpdates"
                ("venueId", "date", "text", "photo")
                VALUES
                (%s, %s, %s, %s)
                """,
                (venueID, date, text, image64)
            )
            conn.commit()

            # Fetch venue name
            cur.execute('SELECT "venueName" FROM venues WHERE id = %s', (venueID,))
            venue_row = cur.fetchone()
            venueName = venue_row['venueName'] if venue_row else "This venue"

            # Notify all users who follow this venue
            cur.execute(
                'SELECT "userId" FROM "usersFollowLists" WHERE %s = ANY("venues")',
                (str(venueID),)
            )
            followers = cur.fetchall()

            for row in followers:
                notification_data = {
                    "userId":   row['userId'],
                    "userType": "user",
                    "notiTabs": "venues & producers",
                    "notiType": "venue_update",
                    "image":    image64 or None,
                    "link":     f"/profile/venue/{venueID}/{venueName}",
                    "message":  f"{venueName} posted a new announcement.",
                    "createdAt": current_time,
                }
                print("Notification data for venue update:", notification_data)
                notifications.add_notification_to_db(notification_data)

            return jsonify(
                {
                    "code": 201,
                    "message": "Added update successfully!"
                }
            ), 201
        
        else:
            return jsonify(
                {
                    "code": 404,
                    "message": "Venue not found."
                }
            ), 404
        
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred adding update!"
            }
        ), 500
    
    finally:
        cur.close()

# -----------------------------------------------------------------------------------------
# [POST] Send questions to venue profile
# - Send questions to the venue profile
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/sendQuestions', methods=['POST'])
def sendQuestions():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()
    print("Received data for sending questions:", data)

    venueID = int(data['venueID'])
    question = data['question']
    answer = data['answer']
    date = datetime.strptime(data['date'], "%Y-%m-%dT%H:%M:%S.%fZ")
    userID = int(data['userID'])
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        cur.execute(
            '''
            INSERT INTO "venuesQuestionAnswers" ("question", "answer", "date", "userId", "venueId")
            VALUES (%s, %s, %s, %s, %s)
            ''',
            (question, answer, date, userID, venueID)
        )
        conn.commit()

        cur.execute("""
            SELECT username
            FROM venues
            WHERE venues.id = %s
        """, (venueID,))
        
        venue_username = cur.fetchone()['username']
        
        cur.execute("""
            SELECT username
            FROM users
            WHERE users.id = %s
        """, (userID,))
        user_username = cur.fetchone()['username']
        
        notification_data = {
            "userId": venueID,                     # the venue (or producer) who should receive this
            "userType": "venue",                   # or "producer" if it were a producer’s Q&A
            "notiTabs": "forYou",
            "notiType": "venue_question",
            "image": None,                          # optional: you can pass an icon/thumbnail if desired
            "link": f"/Venues/VenuesQA/{venueID}",  # wherever you display the new question
            "message": f"@{user_username} asked you a question",
            "createdAt": current_time,
        }
        print("Notification data for venue:", notification_data)
        
        notifications.add_notification_to_db(notification_data)

        # Initialize variables for points and badge processing
        points_earned = 0
        badge_result = None

        # Award points to user for asking a question
        if not pointsHelperFunc.check_max_proof_points(userID):
            # Get points for asking a question
            cur.execute('SELECT "proofPoints", "ruleName" FROM "pointSystemRules" WHERE id = %s', (15,))
            points_rule = cur.fetchone()
            
            if points_rule:
                points_earned = points_rule['proofPoints']
                
                # Update user's points
                cur.execute(
                    'UPDATE "pointsRecorder" SET "currentPoints" = "currentPoints" + %s WHERE "userID" = %s',
                    (points_earned, userID)
                )
                conn.commit()
                
                print(f"{points_earned} points awarded to user {userID} for asking a question")
            
            # Process the Question badge
            badge_result = badge_helpers.process_question_badge(conn, cur, userID)
        
        # Notify for badge
        if badge_result:
            notification_data = {
                "userId":   userID,
                "userType": "user",
                "notiTabs": "forYou",
                "notiType": "badge_earned",
                "image":    None,
                "link":     f"/profile/user/{userID}/{user_username}",
                "message":  f"Congratulations! You earned a badge: {badge_result['badgeName']}.",
                "createdAt": current_time,
            }
            print("Notification data for badge:", notification_data)
            notifications.add_notification_to_db(notification_data)
        
        # Prepare the response
        response_data = {
            "code": 201,
            "message": "Question sent successfully!"
        }
        
        if points_earned > 0:
            response_data["pointsEarned"] = points_earned
            if points_rule and 'ruleName' in points_rule:
                response_data["rule"] = points_rule['ruleName']
            
        if badge_result:
            response_data["badgeAwarded"] = badge_result
            
        return jsonify(response_data), 201
    
    except Exception as e:
        conn.rollback()
        print(str(e))
        return jsonify({
            "code": 500,
            "message": "An error occurred sending the question!"
        }), 500
    
    finally:
        cur.close()

# -----------------------------------------------------------------------------------------
# [POST] Send answers to venue profile
# - Send answers to the venue profile
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/sendAnswers', methods=['POST'])
def sendAnswers():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()
    print(data)

    venueID = int(data['venueID'])
    questionsAnswersID = int(data['questionsAnswersID'])
    answer = data['answer']
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        cur.execute(
            '''
            UPDATE "venuesQuestionAnswers"
            SET "answer" = %s
            WHERE "venueId" = %s AND "id" = %s
            ''',
            (answer, venueID, questionsAnswersID)
        )
        conn.commit()

        # Fetch the original asker
        cur.execute(
            'SELECT "userId" FROM "venuesQuestionAnswers" WHERE id = %s',
            (questionsAnswersID,)
        )
        asker_row = cur.fetchone()
        asker_id = asker_row['userId'] if asker_row else None

        # Fetch venue's username for the notification message
        cur.execute(
            'SELECT username FROM venues WHERE id = %s',
            (venueID,)
        )
        venue_row = cur.fetchone()
        venue_username = venue_row['username'] if venue_row else ''

        # Send notification back to the user who asked
        if asker_id:
            notification_data = {
                "userId":   asker_id,
                "userType": "user",
                "notiTabs": "venues & producers",
                "notiType": "venue_answer",
                "image":    None,
                "link":     f"/profile/venue/{venueID}/{venue_username}",
                "message":  f"@{venue_username} answered your question",
                "createdAt": current_time,
            }
            print("Notification data for asker:", notification_data)
            notifications.add_notification_to_db(notification_data)

        return jsonify(
            {
                "code": 201,
                "message": "Answer sent successfully!"
            }
        ), 201
    
    except Exception as e:
        conn.rollback()
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred sending the answer!"
            }
        ), 500
    
    finally:
        cur.close()

# -----------------------------------------------------------------------------------------
# [POST] Like updates
# - Like updates
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/likeUpdates', methods=['POST'])
def likeUpdates():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()
    print(data)

    venueID = int(data['venueID'])
    updateID = int(data['updateID'])
    userID = int(data['userID'])
    userType = data['userType']

    try:
        # Verify that the update exists and belongs to the venue
        cur.execute('SELECT "venueId" FROM "venuesUpdates" WHERE "id" = %s', (updateID,))
        existingUpdate = cur.fetchone()

        if not existingUpdate or existingUpdate['venueId'] != venueID:
            return jsonify(
                {
                    "code": 404,
                    "message": "Update not found."
                }
            ), 404
        
        # Insert into the likes table
        cur.execute("""
            INSERT INTO "venueUpdateLikes" ("updateId", "userId", "userType")
            VALUES (%s, %s, %s)
        """, (updateID, userID, userType))
        conn.commit()

        return jsonify(
            {
                "code": 201,
                "message": "Update liked successfully!"
            }
        ), 201
    
    except Exception as e:
        conn.rollback()
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred liking the update!"
            }
        ), 500
    
    finally:
        cur.close()

# -----------------------------------------------------------------------------------------
# [POST] Unlike updates
# - Unlike updates
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/unlikeUpdates', methods=['POST'])
def unlikeUpdates():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()
    print(data)

    venueID = int(data['venueID'])
    updateID = int(data['updateID'])
    userID = int(data['userID'])
    userType = data['userType']

    try:
        # Verify that the update exists and belongs to the venue
        cur.execute('SELECT "venueId" FROM "venuesUpdates" WHERE "id" = %s', (updateID,))
        existingUpdate = cur.fetchone()

        if not existingUpdate or existingUpdate['venueId'] != venueID:
            return jsonify(
                {
                    "code": 404,
                    "message": "Update not found."
                }
            ), 404
        
        # Remove from the likes table
        cur.execute("""
            DELETE FROM "venueUpdateLikes"
            WHERE "updateId" = %s AND "userId" = %s AND "userType" = %s
        """, (updateID, userID, userType))
        conn.commit()

        return jsonify(
            {
                "code": 201,
                "message": "Update unliked successfully!"
            }
        ), 201
    
    except Exception as e:
        conn.rollback()
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred unliking the update!"
            }
        ), 500
    
    finally:
        cur.close()

# -----------------------------------------------------------------------------------------
# [POST] Edit address
# - Edit address
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/editAddress', methods=['POST'])
def editAddress():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()
    print(data)

    venueID = int(data['venueID'])
    updatedAddress = data['updatedAddress']

    try:
        cur.execute("""
            UPDATE venues
            SET "address" = %s
            WHERE "id" = %s
        """, (updatedAddress, venueID))
        conn.commit()

        return jsonify(
            {
                "code": 201,
                "message": "Updated address successfully!"
            }
        ), 201
    
    except Exception as e:
        conn.rollback()
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred updating address!"
            }
        ), 500
    
    finally:
        cur.close()

# -----------------------------------------------------------------------------------------
# [POST] Edit opening hours
# - Edit opening hours
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/editOpeningHours', methods=['POST'])
def editOpeningHours():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()
    print(data)

    venueID = int(data['venueID'])
    updatedOpeningHours = data['updatedOpeningHours']

    # Prepare the updated opening hours for insertion
    opening_hours = (
        updatedOpeningHours.get('Monday', []),
        updatedOpeningHours.get('Tuesday', []),
        updatedOpeningHours.get('Wednesday', []),
        updatedOpeningHours.get('Thursday', []),
        updatedOpeningHours.get('Friday', []),
        updatedOpeningHours.get('Saturday', []),
        updatedOpeningHours.get('Sunday', [])
    )

    try:
        # Check if opening hours entry already exists
        cur.execute('SELECT id FROM "venuesOpeningHours" WHERE "venueId" = %s', (venueID,))
        existing_entry = cur.fetchone()

        if existing_entry:
            cur.execute("""
                UPDATE "venuesOpeningHours" 
                SET "Monday" = %s, "Tuesday" = %s, "Wednesday" = %s, 
                    "Thursday" = %s, "Friday" = %s, "Saturday" = %s, 
                    "Sunday" = %s 
                WHERE "venueId" = %s
            """, (*opening_hours, venueID))

        else:
            cur.execute(
                """
                    INSERT INTO "venuesOpeningHours" ("Monday", "Tuesday", "Wednesday", 
                    "Thursday", "Friday", "Saturday", "Sunday", "venueId") 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (*opening_hours, venueID)
            )
        conn.commit()

        return jsonify(
            {
                "code": 201,
                "message": "Updated opening hours successfully!"
            }
        ), 201
    
    except Exception as e:
        conn.rollback()
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred updating opening hours!"
            }
        ), 500
    
    finally:
        cur.close()

# -----------------------------------------------------------------------------------------
# [POST] Edit public holidays
# - Edit public holidays
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/editPublicHolidays', methods=['POST'])
def editPublicHolidays():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()
    print(data)

    venueID = int(data['venueID'])
    publicHolidays = data['updatedPublicHolidays']

    try:
        cur.execute("""
            UPDATE venues
            SET "publicHolidays" = %s
            WHERE "id" = %s
        """, (publicHolidays, venueID))
        conn.commit()

        return jsonify(
            {
                "code": 201,
                "message": "Updated public holidays successfully!"
            }
        ), 201
    
    except Exception as e:
        conn.rollback()
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred updating public holidays!"
            }
        ), 500
    
    finally:
        cur.close()

# -----------------------------------------------------------------------------------------
# [POST] Edit reservation details
# - Edit reservation details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/editReservationDetails', methods=['POST'])
def editReservationDetails():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()
    print(data)

    venueID = int(data['venueID'])
    reservationDetails = data['updatedReservationDetails']

    try:
        cur.execute("""
            UPDATE venues
            SET "reservationDetails" = %s
            WHERE "id" = %s
        """, (reservationDetails, venueID))
        conn.commit()

        return jsonify(
            {
                "code": 201,
                "message": "Updated reservation details successfully!"
            }
        ), 201
    
    except Exception as e:
        conn.rollback()
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred updating reservation details!"
            }
        ), 500
    
    finally:
        cur.close()

# -----------------------------------------------------------------------------------------
# [POST] Add listing to menu
# - Add listing to menu
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/addListingToMenu', methods=['POST'])
def addListingToMenu():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()
    # print("Received data for adding listing to menu:", data)

    venueID = int(data['venueID'])
    menuOrder = int(data['menuOrder'])
    listingID = int(data['listingID'])
    itemPrice = data['itemPrice']
    servingType = int(data['servingType'])
    sectionName = data['sectionName']

    itemVintage = data['itemVintage']
    if itemVintage and str(itemVintage).strip():
        # print("vintage data:", itemVintage)
        itemVintage = int(itemVintage)
    else:
        # print("vintage NULL")
        itemVintage = None
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        # Get sectionId based on the sectionName
        cur.execute(
            'SELECT id FROM "venuesMenu" WHERE "sectionName" = %s AND "venueId" = %s',
            (sectionName, venueID)
        )
        section = cur.fetchone()

        if section is None:
            return jsonify(
                {
                    "code": 404,
                    "message": "Menu section not found."
                }
            ), 404
        
        sectionId = section['id']

        columns = ["itemOrder", "itemPrice", "itemAvailability", "itemID", "itemServingType", "sectionId"]
        values = [menuOrder, itemPrice, True, listingID, servingType, sectionId]

        if itemVintage is not None:
            columns.append("variant")
            values.append(itemVintage)

        column_names = ", ".join(f'"{col}"' for col in columns)
        placeholders = ", ".join(["%s"] * len(values))

        cur.execute(
            f'INSERT INTO "menuItems" ({column_names}) VALUES ({placeholders})',
            values
        )
        conn.commit()

        # ---------------------------------------------------------
        # Build and insert notification for the producer whose bottle listing was added
        # ---------------------------------------------------------
        cur.execute(
            'SELECT "producerID", "listingName" FROM "listings" WHERE "id" = %s',
            (listingID,)
        )
        listing_row = cur.fetchone()
        producerId = listing_row["producerID"]
        listingName = listing_row["listingName"]

        cur.execute(
            'SELECT "venueName" FROM "venues" WHERE "id" = %s',
            (venueID,)
        )
        venueName = cur.fetchone()["venueName"]

        notification_data = {
            "userId": producerId,
            "userType": "producer",
            "notiTabs": "forYou",
            "notiType": "listingIncluded",
            "image": None,  # optional: e.g. listing_row["photo"] if you want the bottle’s image
            "link": f"/profile/venue/{venueID}/{venueName}",
            "message": f"Your listing “{listingName}” has been added to {venueName}’s menu.",
            "createdAt": current_time,
        }

        notifications.add_notification_to_db(notification_data)

        return jsonify(
            {
                "code": 201,
                "message": "Listing added to menu successfully!"
            }
        ), 201
    
    except Exception as e:
        conn.rollback()
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred adding the listing to menu!"
            }
        ), 500
    
    finally:
        cur.close()
# -----------------------------------------------------------------------------------------


#  -----------------------------------------------------------------------------------------
# [POST] Change Section Name 
# - Change Section Name
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/editSectionName', methods=['PUT'])
def editSectionName():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()
    print(data)

    venueID = int(data['venueID'])
    sectionOrder = int(data['order'])
    sectionName = data['sectionName']

    try:
        cur.execute(
            '''
            UPDATE "venuesMenu"
            SET "sectionName" = %s
            WHERE "venueId" = %s AND "sectionOrder" = %s
            ''',
            (sectionName, venueID, sectionOrder)
        )
        conn.commit()

        return jsonify(
            {
                "code": 201,
                "message": "Section name changed successfully!"
            }
        ), 201
    
    except Exception as e:
        conn.rollback()
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred changing the section name!"
            }
        ), 500
    
    finally:
        cur.close()
# -----------------------------------------------------------------------------------------
    
# -----------------------------------------------------------------------------------------
# [POST] Edit menu
# - Edit menu
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/editMenu', methods=['POST'])
def editMenu():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()
    print(data)

    venueID = int(data['venueID'])
    updatedMenu = data['updatedMenu']

    try:
        # Clear existing menu
        cur.execute('DELETE FROM "menuItems" WHERE "sectionId" IN (SELECT "id" FROM "venuesMenu" WHERE "venueId" = %s)', (venueID,))
        cur.execute('DELETE FROM "venuesMenu" WHERE "venueId" = %s', (venueID,))

        # Insert updated menu sections
        for section in updatedMenu:
            cur.execute(
                '''
                INSERT INTO "venuesMenu" ("sectionName", "sectionOrder", "venueId")
                VALUES (%s, %s, %s)
                RETURNING id
                ''',
                (section['sectionName'], section['sectionOrder'], venueID)
            )
            sectionId = cur.fetchone()['id']

            # Insert items for each section
            for item in section.get('sectionMenu', []):
                # dynamically add vintage
                columns = ["itemOrder", "itemPrice", "itemAvailability", "itemID", "itemServingType", "sectionId"]
                values = [item.get('itemOrder'), item.get('itemPrice'), item.get('itemAvailability'), item.get('itemID'), item.get('itemServingType'), sectionId]

                # only add when you find vintage maintained by user
                itemVintage = item.get('itemVintage')
                if itemVintage and str(itemVintage).strip():
                    # print("vintage data:", itemVintage)
                    itemVintage = int(itemVintage)
                else:
                    # print("vintage NULL")
                    itemVintage = None

                if itemVintage is not None:
                    columns.append("variant")
                    values.append(itemVintage)

                # append it back as string to be passed for execution
                column_names = ", ".join(f'"{col}"' for col in columns)
                placeholders = ", ".join(["%s"] * len(values))

                cur.execute(
                    f'INSERT INTO "menuItems" ({column_names}) VALUES ({placeholders})',
                    values
                )

        conn.commit()
        return jsonify(
            {
                "code": 201,
                "message": "Menu edited successfully!"
            }
        ), 201
    
    except Exception as e:
        conn.rollback()
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred editing the menu!"
            }
        ), 500
    
    finally:
        cur.close()

    
# -----------------------------------------------------------------------------------------
# [POST] Edit venue profile
# - Update producer profile with new details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/updateVenueStatus', methods=['POST'])
def updateVenueStatus():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()
    print(data)

    venueID = int(data['businessID'])
    venueName = data['newBusinessData']["businessName"]
    venueDesc = data['newBusinessData']["businessDesc"]
    originLocation = data['newBusinessData']["originCountry"]
    image = data['newBusinessData']["photo"]
    hashedPassword = data['newBusinessData']["hashedPassword"]
    claimStatus = data['newBusinessData']["claimStatus"]
    requestId = int(data['newBusinessData']["requestId"])
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        cur.execute('UPDATE venues SET "venueName" = %s, "venueDesc" = %s, "originLocation" = %s, "hashedPassword" = %s, "claimStatus" = %s, "requestId" = %s WHERE "id" = %s', (venueName, venueDesc, originLocation, hashedPassword, claimStatus, requestId, venueID))
        conn.commit()
        
        # Find all users who follow this venue
        cur.execute(
            '''
            SELECT "userId"
            FROM "usersFollowLists"
            WHERE %s = ANY("venues")
            ''',
            (str(venueID),)
        )
        followers = cur.fetchall()

        # Notify each follower
        for row in followers:
            notification_data = {
                "userId":   row['userId'],
                "userType": "user",
                "notiTabs":"venues & producers",
                "notiType":"status_update",
                "image":   image,
                "link":    f"/profile/venue/{venueID}/{venueName}",
                "message": f"{venueName} updated their status.",
                "createdAt": current_time,
            }
            print("Notification data for venue status update:", notification_data)
            notifications.add_notification_to_db(notification_data)

        return jsonify(
            {
                "code": 201,
                "message": "Updated claim status successfully!"
            }
        ), 201
    
    except Exception as e:
        conn.rollback()
        import traceback
        traceback.print_exc()
        return jsonify({
                "code": 500,
                "message": "An error occurred updating claim status!"
        }), 500
    
    finally:
        cur.close()

# -----------------------------------------------------------------------------------------

# [POST] Edit venue update
# - Update a venue update with new details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/editUpdate', methods=['POST'])
def editUpdate():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()
    print(data)

    venueID = int(data['venueID'])
    updateID = int(data['updateID'])
    update = data['update']
    image64 = data.get('image64', '')

    try:
        # Find existing venue
        cur.execute('SELECT * FROM "venuesUpdates" WHERE "venueId" = %s AND "id" = %s', (venueID, updateID))
        existingUpdate = cur.fetchone()

        if existingUpdate:
            # Delete old photo from S3 if it exists
            if existingUpdate['photo']:
                s3Images.deleteImageFromS3(existingUpdate['photo'])

            if image64:
                base64_string = re.sub(r'^data:image\/[a-zA-Z]+;base64,', '', image64)
                image64 = s3Images.uploadBase64ImageToS3(base64_string)

            # Update the venue details in the database
            cur.execute(
                """
                UPDATE "venuesUpdates"
                SET 
                    "text" = %s,
                    "photo" = %s
                WHERE "venueId" = %s AND "id" = %s
                """,
                (update, image64, venueID, updateID)
            )
            conn.commit()

            return jsonify(
                {
                    "code": 201,
                    "message": "Updated update successfully!"
                }
            ), 201
        
        else:
            return jsonify(
                {
                    "code": 404,
                    "message": "Update not found."
                }
            ), 404
        
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred updating update!"
            }
        ), 500
    
    finally:
        cur.close()

# -----------------------------------------------------------------------------------------

# [POST] Delete venue update
# - Delete a venue update with new details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/deleteUpdate', methods=['POST'])
def deleteUpdate():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()
    print(data)

    venueID = int(data['venueID'])
    updateID = int(data['updateID'])

    try:
        # Find existing venue and see if photo exists, if it does delete it from S3 bucket
        cur.execute('SELECT * FROM "venuesUpdates" WHERE "venueId" = %s AND "id" = %s', (venueID, updateID))
        existingUpdate = cur.fetchone()

        if existingUpdate:
            if existingUpdate['photo']:
                s3Images.deleteImageFromS3(existingUpdate['photo'])

            # Delete the venue update from the database
            cur.execute('DELETE FROM "venuesUpdates" WHERE "venueId" = %s AND "id" = %s', (venueID, updateID))
            conn.commit()

            return jsonify(
                {
                    "code": 201,
                    "message": "Update deleted successfully!"
                }
            ), 201
        
        else:
            return jsonify(
                {
                    "code": 404,
                    "message": "Update not found."
                }
            ), 404
        
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred deleting update!"
            }
        ), 500
    
    finally:
        cur.close()


# -----------------------------------------------------------------------------------------

# [POST] Edit Q&A
# - Update a venue Q&A with new details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/editQA', methods=['POST'])
def editQA():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()
    print(data)

    venueID = int(data['venueID'])
    questionsAnswersID = int(data['questionsAnswersID'])
    answer = data['answer']

    try:
        # Update the answer
        cur.execute('UPDATE "venuesQuestionAnswers" SET "answer" = %s WHERE "venueId" = %s AND "id" = %s', (answer, venueID, questionsAnswersID))
        conn.commit()

        return jsonify(
            {
                "code": 201,
                "message": "Updated venue's Q&A!"
            }
        ), 201
    
    except Exception as e:
        conn.rollback()
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred updating venue's Q&A!"
            }
        ), 500
    
    finally:
        cur.close()

# -----------------------------------------------------------------------------------------

# [POST] Delete venue Q&A
# - Delete a venue Q&A with new details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/deleteQA', methods=['POST'])
def deleteQA():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()
    print(data)

    venueID = int(data['venueID'])
    questionsAnswersID = int(data['questionsAnswersID'])

    try:
        # get the user id of the user who asked the question
        cur.execute('SELECT "userId" FROM "venuesQuestionAnswers" WHERE "venueId" = %s AND "id" = %s', (venueID, questionsAnswersID))
        userId = cur.fetchone()['userId'] 

        cur.execute('DELETE FROM "venuesQuestionAnswers" WHERE "venueId" = %s AND "id" = %s', (venueID, questionsAnswersID))
        conn.commit()

        # Deduct points from user for deleting a question
 
        # get points for deleting a question
        cur.execute('SELECT "proofPoints", "ruleName" FROM "pointSystemRules" WHERE id = %s', (15,))
        points = cur.fetchone()

        # Update user's points
        cur.execute('UPDATE "pointsRecorder" SET "currentPoints" = "currentPoints" - %s WHERE "userID" = %s', (points['proofPoints'], userId,))
        conn.commit()

        print("Points deducted from user: ", points['proofPoints'])
        
        return jsonify(
            {
                "code": 201,
                "message": "Deleted venue's Q&A!",
                "pointsDeducted": points['proofPoints'],
                "rule": points['rule']
            }
        ), 201
    
    except Exception as e:
        conn.rollback()
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred deleting venue's Q&A!"
            }
        ), 500
    
    finally:
        cur.close()

# -----------------------------------------------------------------------------------------

# [POST] Add profile view count
# - Add profile view count
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/addProfileCount', methods=['POST'])
def addProfileCount():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()
    print(data)

    venueID = int(data['venueID'])
    date = datetime.strptime(data['date'], "%Y-%m-%dT%H:%M:%S.%fZ")

    try:
        # Check if a record already exists for the venue
        cur.execute('SELECT * FROM "venuesProfileViews" WHERE "venueId" = %s', (venueID,))
        existingRecord = cur.fetchone()

        if existingRecord:
            cur.execute(
                """
                UPDATE "venuesProfileViews"
                SET "date" = %s, "count" = "count" + 1
                WHERE "venueId" = %s
                """,
                (date, venueID)
            )
        else:
            cur.execute(
                """
                INSERT INTO "venuesProfileViews" ("date", "count", "venueId")
                VALUES (%s, 1, %s)
                """,
                (date, venueID)
            )

        conn.commit()

        return jsonify(
            {
                "code": 201,
                "message": "Profile view count updated successfully!"
            }
        ), 201
    
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred updating the profile view count."
            }
        ), 500
    
    finally:
        cur.close()

# -----------------------------------------------------------------------------------------

# [POST] Add new profile view count
# - Add new profile view count
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/addNewProfileCount', methods=['POST'])
def addNewProfileCount():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()
    print(data)

    venueID = int(data['venueID'])
    date = datetime.strptime(data['date'], "%Y-%m-%dT%H:%M:%S.%fZ")

    try:
        # Check if a record already exists for the venue
        cur.execute('SELECT * FROM "venuesProfileViews" WHERE "venueId" = %s', (venueID,))
        existingRecord = cur.fetchone()

        if existingRecord:
            cur.execute(
                """
                UPDATE "venuesProfileViews"
                SET "date" = %s, "count" = "count" + 1
                WHERE "venueId" = %s
                """,
                (date, venueID)
            )
        else:
            cur.execute(
                """
                INSERT INTO "venuesProfileViews" ("date", "count", "venueId")
                VALUES (%s, 1, %s)
                """,
                (date, venueID)
            )

        conn.commit()

        return jsonify(
            {
                "code": 201,
                "message": "New profile view count updated successfully!"
            }
        ), 201
    
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred updating the new profile view count."
            }
        ), 500
    
    finally:
        cur.close()
    
# -----------------------------------------------------------------------------------------
# [POST] Edit venue profile claim status
# - Update venue profile with new details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/updateVenueClaimStatus', methods=['POST'])
def updateVenueClaimStatus():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()
    print(data)

    venueID = int(data['businessId'])
    claimStatus = data['claimStatus']

    try:
        cur.execute('UPDATE venues SET "claimStatus" = %s WHERE "id" = %s', (claimStatus, venueID))
        conn.commit()

        return jsonify(
            {
                "code": 201,
                "message": "Updated claim status successfully!"
            }
        ), 201
    
    except Exception as e:
        conn.rollback()
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred updating claim status!"
            }
        ), 500
    
    finally:
        cur.close()


# -----------------------------------------------------------------------------------------
# [POST] Edit venue profile last check claim status date
# - Update venue profile with new details
# - Possible return codes: 201 (Updated), 500 (Error during update)
@blueprint.route('/updateVenueClaimStatusCheckDate', methods=['POST'])
def updateVenueClaimStatusCheckDate():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()
    print(data)

    venueID = int(data['businessId'])
    claimStatusCheckDate = datetime.strptime(data['claimStatusCheckDate'], "%Y-%m-%dT%H:%M:%S.%fZ")

    try:
        cur.execute('UPDATE venues SET "claimStatusCheckDate" = %s WHERE "id" = %s', (claimStatusCheckDate, venueID))
        conn.commit()

        return jsonify(
            {
                "code": 201,
                "message": "Updated claim status check date successfully!"
            }
        ), 201
    
    except Exception as e:
        conn.rollback()
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred updating claim status check date!"
            }
        ), 500
    
    finally:
        cur.close()


@blueprint.route('/uploadPDFMenu', methods=['PUT'])
def uploadPDFMenu():
    """Upload PDF menu for venue."""
    conn = g.db
    cursor = conn.cursor()

    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            return jsonify({
                "code": 400,
                "message": "No data provided"
            }), 400
        
        venue_id = data.get('venueID')
        pdf_menu_data = data.get('pdfMenuData')
        
        # Validate required fields
        if not venue_id:
            return jsonify({
                "code": 400,
                "message": "Venue ID is required"
            }), 400
            
        if not pdf_menu_data:
            return jsonify({
                "code": 400,
                "message": "PDF menu data is required"
            }), 400
        
        # Check if venue exists
        cursor.execute('SELECT id, "pdfMenuUrl" FROM venues WHERE id = %s', (venue_id,))
        venue = cursor.fetchone()
        
        if not venue:
            return jsonify({
                "code": 404,
                "message": "Venue not found"
            }), 404
        
        # Get current PDF URL for cleanup if exists
        current_pdf_url = venue.get('pdfMenuUrl') if isinstance(venue, dict) else venue[1]
        
        # Upload new PDF to S3
        pdf_url = s3pdfMenu.uploadBase64PDFToS3(pdf_menu_data)
        
        if not pdf_url:
            return jsonify({
                "code": 500,
                "message": "Failed to upload PDF to S3"
            }), 500
        
        # Delete old PDF from S3 if exists
        if current_pdf_url:
            try:
                s3pdfMenu.deletePDFFromS3(current_pdf_url)
            except Exception as e:
                print(f"Warning: Failed to delete old PDF: {e}")
        
        # Update venue with new PDF URL
        cursor.execute(
            'UPDATE venues SET "pdfMenuUrl" = %s WHERE id = %s',
            (pdf_url, venue_id)
        )
        
        conn.commit()
        
        return jsonify({
            "code": 201,
            "success": True,
            "message": "PDF menu uploaded successfully!",
            "menuUrl": pdf_url
        }), 201
        
    except Exception as e:
        conn.rollback()
        print(f"Error uploading PDF menu: {e}")
        import traceback
        traceback.print_exc()
        
        return jsonify({
            "code": 500,
            "message": "An error occurred while uploading PDF menu"
        }), 500
    
    finally:
        cursor.close()