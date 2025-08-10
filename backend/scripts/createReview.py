# Port: 5021
# Routes: /createReview (POST), /createProducerReview (POST), /createVenueReview (POST)
# Dataclass: reviews, producerReviews, venueReviews
# -----------------------------------------------------------------------------------------

import os
import s3Images
from flask import Blueprint, g, request, jsonify
from datetime import datetime
from scripts import pointsHelperFunc, badge_helpers, notifications
import re
import unicodedata

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)


def normalize_venue_name(name):
    """Normalize venue name for fuzzy matching"""
    if not name:
        return ""
    
    # Convert to lowercase and remove accents
    name = unicodedata.normalize('NFKD', name.lower())
    name = ''.join(c for c in name if not unicodedata.combining(c))
    
    # Remove punctuation and collapse whitespace
    name = re.sub(r'[^\w\s]', '', name)
    name = re.sub(r'\s+', ' ', name).strip()
    
    # Remove common words
    stop_words = {'bar', 'bars', 'pub', 'pubs', 'taproom', 'tap', 'room', 'taphouse', 
                  'house', 'cellar', 'cocktail', 'cocktails', 'tavern', 'and', 'the', 'at'}
    words = [word for word in name.split() if word not in stop_words]
    
    return ' '.join(words)


# Helper function to create a unique username for the venue
def create_username(location_name):
    conn = g.db
    cur = conn.cursor()

    location_name = location_name.replace(" ", "").lower()

    cur.execute("""
        SELECT id FROM "venues" WHERE "username" LIKE %s
    """, (f"{location_name}%",))

    existing_usernames = cur.fetchall()

    if not existing_usernames:
        return location_name
    else:
        max_suffix = max([int(name[0].split('_')[-1]) for name in existing_usernames if '_' in name[0]], default=0)
        return f"{location_name}_{max_suffix + 1}"
# ======================================================



# -----------------------------------------------------------------------------------------
# [POST] Creates a review
# - Insert entry into the "reviews" collection. Follows reviews dataclass requirements.
# - Duplicate review check: If a review with the same userID and reviewTarget exists, reject the request
# - Possible return codes: 201 (Created), 400 (Duplicate Detected), 500 (Error during creation)
@blueprint.route("/createReview", methods= ['POST'])
def createReviews():
    raw_review = request.get_json()
    print("Raw review data:", raw_review)  # Debugging line to check the input data
    conn = g.db
    cur = conn.cursor()

    review_target = int(raw_review['reviewTarget'])
    user_id = int(raw_review['userID'])
    created_date = datetime.strptime(raw_review['createdDate'], "%Y-%m-%dT%H:%M:%S.%fZ")

    # Handle nullable variant field
    variant = raw_review.get('variant')
    if variant and str(variant).strip():
        variant = int(variant)
    else:
        variant = None

    # Checking for duplicate review
    if variant is None: 
        cur.execute("""
            SELECT * FROM "reviews" 
                WHERE "reviewTarget" = %s 
                AND "userID" = %s
        """, (review_target, user_id))
    else: 
        cur.execute("""
            SELECT * FROM "reviews" 
                WHERE "reviewTarget" = %s 
                AND "variant" = %s    
                AND "userID" = %s
        """, (review_target, variant, user_id))

    if cur.fetchone() is not None:
        return jsonify({
            "code": 400,
            "data": {
                "listingName": raw_review['reviewDesc']
            },
            "message": "Review already exists."
        }), 400

    tagged_users = raw_review.get('taggedUsers', [])
    flavour_tags = raw_review.get('flavourTag', [])
    observation_tags = raw_review.get('observationTag', [])

    will_recommend = raw_review.get('willRecommend')
    would_buy_again = raw_review.get('wouldBuyAgain')

    # if will_recommend is None:
    #     will_recommend = None
    # else:
    #     will_recommend = bool(will_recommend == 'true')

    # if would_buy_again is None:
    #     would_buy_again = None
    # else:
    #     would_buy_again = bool(would_buy_again == 'true')

    # Insert new venue if necessary OR handle "Home" case
    venue_id = None
    stored_address = raw_review.get('address', '')
    if raw_review.get('location') and raw_review.get('address'):
        location_name = raw_review['location']
        address = raw_review['address']
        
        # Check if this is a "Home" tasting
        if location_name.lower() == 'home' and address.lower() == 'home':
            venue_id = None  # NULL for home tastings (no venue reference needed)
            stored_address = 'home'  # Normalize to lowercase for consistency
        else:
            # Existing venue logic for real venues
            # Check for exact match first
            cur.execute("""SELECT id FROM venues WHERE "venueName" = %s AND "address" = %s""", (location_name, address))
            venue_id = cur.fetchone()['id'] if cur.rowcount > 0 else None
            
            if not venue_id:
                # Try fuzzy matching on venue name with exact address match
                normalized_input_name = normalize_venue_name(location_name)
                if normalized_input_name:
                    cur.execute("""
                        WITH normalized_venues AS (
                            SELECT 
                                id, 
                                "venueName",
                                regexp_replace(
                                    regexp_replace(
                                        regexp_replace(
                                            lower("venueName"), 
                                            '[^a-z0-9\\s]', 
                                            '', 
                                            'g'
                                        ),
                                        '(^|\\s+)(bar|bars|pub|pubs|taproom|tap|room|taphouse|house|cellar|cocktail|cocktails|tavern|and|the|at)(\\s+|$)', 
                                        '\\1\\3', 
                                        'g'
                                    ),
                                    '\\s+', 
                                    ' ', 
                                    'g'
                                ) AS normalized_name
                            FROM venues
                            WHERE "address" = %s
                        )
                        SELECT id, "venueName", 
                            similarity(%s, TRIM(normalized_name)) as sim
                        FROM normalized_venues
                        WHERE similarity(%s, TRIM(normalized_name)) > 0.3
                        ORDER BY sim DESC
                        LIMIT 1
                    """, (address, normalized_input_name, normalized_input_name))
                    
                    fuzzy_match = cur.fetchone()
                    if fuzzy_match:
                        venue_id = fuzzy_match['id']
            
            if not venue_id:
                # Create new venue if no exact or fuzzy match found
                username = create_username(location_name)
                insert_venue_sql = """INSERT INTO venues ("venueName", "address", "venueType", "originLocation", "venueDesc",
                                      "hashedPassword", "claimStatus", photo, "reservationDetails", username)
                                      VALUES (%s, %s, '', '', '', %s, FALSE, '', '', %s) RETURNING id"""
                hashed_password = 'hashed_password'
                cur.execute(insert_venue_sql, (location_name, address, hashed_password, username))
                venue_id = cur.fetchone()['id'] if cur.rowcount > 0 else None
        
                conn.commit()

    # Upload image into S3
    if raw_review['photo']:
        base64_string = re.sub(r'^data:image\/[a-zA-Z]+;base64,', '', raw_review['photo'])
        raw_review['photo'] = s3Images.uploadBase64ImageToS3(base64_string)


    # Prepare the insert SQL for reviews
    if variant is None: 
        insert_review_sql = """INSERT INTO reviews ("userID", "reviewTarget", "rating", "reviewDesc", "reviewType", "createdDate", 
                            language, finish, "willRecommend", "wouldBuyAgain", "taggedUsers", "flavourTag", photo, colour, 
                            aroma, taste, "observationTag", location, address)
                            VALUES (%s, %s, %s::DECIMAL(3,1), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        review_values = (user_id, review_target, float(raw_review['rating']), raw_review['reviewDesc'], raw_review['reviewType'],
                        created_date, raw_review['language'], raw_review['finish'], will_recommend,
                        would_buy_again, tagged_users, flavour_tags, raw_review['photo'],
                        raw_review['colour'], raw_review['aroma'], raw_review['taste'],
                        observation_tags, venue_id, stored_address)
    else :
        insert_review_sql = """INSERT INTO reviews ("userID", "reviewTarget", "rating", "reviewDesc", "reviewType", "createdDate", 
                                "language", "finish", "willRecommend", "wouldBuyAgain", "taggedUsers", "flavourTag", "photo", "colour", 
                                "aroma", "taste", "observationTag", "location", "address", "variant")
                                VALUES (%s, %s, %s::DECIMAL(3,1), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        review_values = (user_id, review_target, float(raw_review['rating']), raw_review['reviewDesc'], raw_review['reviewType'],
                        created_date, raw_review['language'], raw_review['finish'], will_recommend,
                        would_buy_again, tagged_users, flavour_tags, raw_review['photo'],
                        raw_review['colour'], raw_review['aroma'], raw_review['taste'],
                        observation_tags, venue_id, stored_address, variant)

    try:
        cur.execute(insert_review_sql, review_values)
        conn.commit()
        
        cur.execute('SELECT "listingName" FROM listings WHERE id = %s', (review_target,))
        listing_row = cur.fetchone()
        listing_name = listing_row['listingName'] if listing_row else "your listing"

        cur.execute('SELECT username FROM users WHERE id = %s', (user_id,))
        user_row = cur.fetchone()
        reviewer_username = user_row['username'] if user_row else "Someone"
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        for tagged_id in tagged_users:
            try:
                tagged_id_int = int(tagged_id)
            except ValueError:
                continue  # skip invalid IDs
            
            # # Check if tagged_id corresponds to a venue
            # cur.execute('SELECT id FROM venues WHERE id = %s', (tagged_id_int,))
            # if cur.rowcount == 0:
            #     continue  # not a venue
            # print("hello3")
            # notification_data = {
            #     "userId": tagged_id_int,
            #     "userType": "venue",
            #     "notiTabs": "forYou",
            #     "notiType": "venue_tagged_review",
            #     "image": None,
            #     "link": f"/listing/view/{review_target}/{listing_name}",
            #     "message": f"@{reviewer_username} mentioned your venue in their review of {listing_name}"
            # }
            # print("Adding notification for tagged venue:", notification_data)
            # notifications.add_notification_to_db(notification_data)

            cur.execute('SELECT 1 FROM "users" WHERE id=%s', (tagged_id_int,))
            if cur.rowcount:
                notification_data = {
                    "userId":   tagged_id_int,
                    "userType": "user",
                    "notiTabs": "forYou",
                    "notiType": "user_tagged_review",
                    "image":    None,
                    "link":     f"/listing/view/{review_target}/{listing_name}",
                    "message":  f"@{reviewer_username} mentioned you in a review of {listing_name}",
                    "createdAt": current_time,
                }
                print("Adding notification for tagged user:", notification_data)
                notifications.add_notification_to_db(notification_data)
                
                

        if pointsHelperFunc.check_max_proof_points(user_id):
            return jsonify({
                "code": 400,
                "data": raw_review['reviewDesc']
            }), 201

        # Calculate proof points earned 
        rule_fulfiled_id = []

        # Basic review: Simple text 
        if (raw_review['reviewDesc'] != None):
            rule_fulfiled_id.append(2)
        
        # Extended review: color, aroma, taste, finish
        is_extensive_review = False
        if (raw_review['finish'] != None or raw_review['colour'] != None or raw_review['aroma'] != None or raw_review['taste'] != None) and \
            (raw_review['finish'] != '' or raw_review['colour'] != '' or raw_review['aroma'] != '' or raw_review['taste'] != ''):
            rule_fulfiled_id.append(3)
            is_extensive_review = True

        # Attach image
        has_photo = False
        if (raw_review['photo'] != None):
            rule_fulfiled_id.append(4)
            has_photo = True

        # Tag location
        has_location = False
        if (venue_id != None):
            rule_fulfiled_id.append(5)
            has_location = True

        # Tag friends
        has_tagged_friends = False
        if (tagged_users != []):
            rule_fulfiled_id.append(6)
            has_tagged_friends = True

        # Get total proof points earned 
        cur.execute('SELECT SUM("proofPoints") FROM "pointSystemRules" WHERE id IN %s', (tuple(rule_fulfiled_id),))
        total_points = cur.fetchone()['sum']


        # Update user points
        if total_points:
            cur.execute('UPDATE "pointsRecorder" SET "currentPoints" = "currentPoints" + %s WHERE "userID" = %s AND "userType" = %s', (total_points, user_id, 'user',))

            conn.commit()

        # Badge Processing
        badges_awarded = []

        # Fetch the listing details to get drinkType, typeCategory and originCountry
        cur.execute("""
            SELECT "drinkType", "typeCategory", "originCountry" 
            FROM "listings" 
            WHERE id = %s
        """, (review_target,))

        listing_info = cur.fetchone()

        if listing_info:
            drink_type = listing_info['drinkType']
            type_category = listing_info['typeCategory']
            origin_country = listing_info['originCountry']

            # Track which badge triggers were activated in this review
            badge_triggers = []

            if origin_country:
                badge_triggers.append({
                    'actionType': 'Review',
                    'mappingType': 'Country',
                    'primaryValue': origin_country,
                    'secondaryValue': None
                })

            if drink_type:
                badge_triggers.append({
                    'actionType': 'Review',
                    'mappingType': 'DrinkType',
                    'primaryValue': drink_type,
                    'secondaryValue': None
                })

            if drink_type and type_category:
                badge_triggers.append({
                    'actionType': 'Review',
                    'mappingType': 'Category',
                    'primaryValue': drink_type,
                    'secondaryValue': type_category
                })

            if is_extensive_review:
                badge_triggers.append({
                    'actionType': 'ExtensiveReview',
                    'mappingType': 'Action',
                    'primaryValue': 'ExtensiveReview',
                    'secondaryValue': None
                })

            if has_photo:
                badge_triggers.append({
                    'actionType': 'PhotoAttached',
                    'mappingType': 'Action', 
                    'primaryValue': 'PhotoAttached',
                    'secondaryValue': None
                })

            if has_location:
                badge_triggers.append({
                    'actionType': 'LocationTagged',
                    'mappingType': 'Action',
                    'primaryValue': 'LocationTagged',
                    'secondaryValue': None
                })

            if has_tagged_friends:
                badge_triggers.append({
                    'actionType': 'FriendTagged',
                    'mappingType': 'Action',
                    'primaryValue': 'FriendTagged',
                    'secondaryValue': None
                })

            badges_awarded = badge_helpers.process_badges(conn, cur, user_id, badge_triggers)

            # Notify user of badges earned
            for badge in badges_awarded:
                notification_data = {
                    "userId": user_id,
                    "userType": "user",
                    "notiTabs": "forYou",
                    "notiType": "badge_earned",
                    "image": None,
                    "link": f"/profile/user/{user_id}/{reviewer_username}",
                    "message": f"Congratulations! You earned a badge: {badge['badgeName']}.",
                    "createdAt": current_time
                }
                notifications.add_notification_to_db(notification_data)

            return jsonify({
                "code": 201,
                "data": raw_review['reviewDesc'],
                "proofPointsEarned": total_points,
                "badgesAwarded": badges_awarded,
            }), 201
        
        else:
            # No listing found, just return without badge processing
            return jsonify({
                "code": 201,
                "data": raw_review['reviewDesc'],
                "proofPointsEarned": total_points,
            }), 201
    except Exception as e:
        import traceback
        traceback.print_exc()
        conn.rollback()
        return jsonify({
            "code": 500,
            "data": {
                "listingName": raw_review['reviewDesc']
            },
            "message": "An error occurred creating the listing."
        }), 500
# ======================================================

# [POST] Creates a producer tour review
@blueprint.route("/createProducerReview", methods=['POST'])
def createProducerReviews():
    raw_review = request.get_json()
    conn = g.db
    cur = conn.cursor()

    producer_id = int(raw_review['producerID'])
    user_id = int(raw_review['userID'])
    created_date = datetime.strptime(raw_review['createdDate'], "%Y-%m-%dT%H:%M:%S.%fZ")

    # Check for duplicate review using EXISTS
    cur.execute("""SELECT EXISTS(SELECT 1 FROM "producerReviews" WHERE "producerID" = %s AND "userID" = %s)""",
                (producer_id, user_id))
    if cur.fetchone()['exists']:
        return jsonify({"code": 400, "message": "Review already exists."}), 400
    
    photos = []

    for photo in raw_review.get('photos', []):
        if photo:
            # Upload images & store their returned URLs
            base64_string = re.sub(r'^data:image\/[a-zA-Z]+;base64,', '', photo)
            uploaded_photo = s3Images.uploadBase64ImageToS3(base64_string)
            photos.append(uploaded_photo)

    # Upload images & store their returned URLs
    # photos = [s3Images.uploadBase64ImageToS3(photo) for photo in raw_review.get('photos', []) if photo]

    insert_review_sql = """
        INSERT INTO "producerReviews" ("userID", "producerID", "rating", "reviewDesc", "createdDate", "photos") 
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    review_values = (user_id, producer_id, float(raw_review['rating']), raw_review['reviewDesc'], created_date, photos)

    try:
        cur.execute(insert_review_sql, review_values)
        conn.commit()

        total_points = 0

        if pointsHelperFunc.check_max_proof_points(user_id):
            return jsonify({"code": 201, "data": raw_review['reviewDesc']}), 201

        # Get the proof points for simple text review
        if raw_review['reviewDesc']:
            cur.execute("""SELECT "proofPoints" FROM "pointSystemRules" WHERE id = 2""")
            total_points += cur.fetchone()['proofPoints']

        # Check if photo was provided
        if photos:
            cur.execute("""SELECT "proofPoints" FROM "pointSystemRules" WHERE id = 4""")
            total_points += cur.fetchone()['proofPoints']

        # Update user points
        cur.execute('UPDATE "pointsRecorder" SET "currentPoints" = "currentPoints" + %s WHERE "userID" = %s AND "userType" = %s', (total_points, user_id, 'user',))
        conn.commit()

        return jsonify({"code": 201, "data": raw_review['reviewDesc'], "pointsEarned": total_points}), 201

    except Exception as e:
        print(str(e))
        return jsonify({"code": 500, "message": "An error occurred creating the review."}), 500
    
# ======================================================

# [POST] Creates a venue review
@blueprint.route("/createVenueReview", methods=['POST'])
def createVenueReviews():
    raw_review = request.get_json()
    conn = g.db
    cur = conn.cursor()

    venue_id = int(raw_review['venueID'])
    user_id = int(raw_review['userID'])
    created_date = datetime.strptime(raw_review['createdDate'], "%Y-%m-%dT%H:%M:%S.%fZ")

    # Check for duplicate review using EXISTS
    cur.execute(
        """SELECT EXISTS(SELECT 1 FROM "venueReviews" WHERE "venueID" = %s AND "userID" = %s)""",
        (venue_id, user_id)
    )
    if cur.fetchone()['exists']:
        return jsonify({"code": 400, "message": "Review already exists."}), 400
    
    photos = []

    for photo in raw_review.get('photos', []):
        if photo:
            # Upload images & store their returned URLs
            base64_string = re.sub(r'^data:image\/[a-zA-Z]+;base64,', '', photo)
            uploaded_photo = s3Images.uploadBase64ImageToS3(base64_string)
            photos.append(uploaded_photo)

    # Upload images & store their returned URLs
    # photos = [s3Images.uploadBase64ImageToS3(photo) for photo in raw_review.get('photos', []) if photo]

    insert_review_sql = """
        INSERT INTO "venueReviews" ("userID", "venueID", "rating", "reviewDesc", "createdDate", "photos") 
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    review_values = (
        user_id,
        venue_id,
        float(raw_review['rating']),
        raw_review['reviewDesc'],
        created_date,
        photos
    )

    try:
        cur.execute(insert_review_sql, review_values)
        conn.commit()

        total_points = 0

        if pointsHelperFunc.check_max_proof_points(user_id):
            return jsonify({"code": 201, "data": raw_review['reviewDesc']}), 201
        
        # Get the proof points for simple text review
        if raw_review['reviewDesc']:
            cur.execute("""SELECT "proofPoints" FROM "pointSystemRules" WHERE id = 2""")
            total_points += cur.fetchone()['proofPoints']

        # Check if photo was provided
        if photos:
            cur.execute("""SELECT "proofPoints" FROM "pointSystemRules" WHERE id = 4""")
            total_points += cur.fetchone()['proofPoints']

        # Update user points
        cur.execute('UPDATE "pointsRecorder" SET "currentPoints" = "currentPoints" + %s WHERE "userID" = %s AND "userType" = %s', (total_points, user_id, 'user',))
        conn.commit()
        
        return jsonify({"code": 201, "data": raw_review['reviewDesc']}), 201

    except Exception as e:
        print(str(e))
        return jsonify({"code": 500, "message": "An error occurred creating the review."}), 500
