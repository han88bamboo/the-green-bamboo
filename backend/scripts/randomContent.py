# This backend script is to handle backend functions that supports the random content shown on the random explore page - discover tab

# Routes: 
#   [Content Retrieval - On Random Explore Page]
#   /getRandomListings [GET], /getNext30 [POST]

#   [Content Retrieval - On respective page]
#   /getListingsCommentsDetails [POST], /getReviewsCommentsDetails [POST]

#   [Likes]
#   /likeContent [POST], /unlikeContent [POST]

#   [Comments]
#   /addComment [POST], /editComment [POST], /deleteComment [DELETE]
# -----------------------------------------------------------------------------------------

import os
from flask import Blueprint, g, jsonify, request
import random
from email.utils import parsedate_to_datetime
from psycopg2.extras import RealDictCursor


file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

# Helper Functions

# Get top 3 comments
def get_top_comments(content_id, content_type, table_user_type):
    conn = g.db
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:

        # Get table name 
        table_name = get_table_name(content_type, "comment", table_user_type)

        # Get unique field 
        unique_field = get_unique_field(content_type, table_user_type)

        cursor.execute(f"""
            SELECT * FROM "{table_name}"
            WHERE "{unique_field}" = %s
            ORDER BY "createdAt" DESC
            LIMIT 3
        """, (content_id,))
        comments = cursor.fetchall()

        # Loop through each comment and get the username or producerName or venueName
        if comments:
            for comment in comments:

                if comment["userType"] == "user":
                    cursor.execute("""
                        SELECT "username"
                        FROM "users"
                        WHERE "id" = %s
                    """, (comment["userId"],))
                    comment["username"] = cursor.fetchone()["username"]

                elif comment["userType"] == "producer":
                    cursor.execute("""
                        SELECT "producerName"
                        FROM "producers"
                        WHERE "id" = %s
                    """, (comment["userId"],))
                    comment["username"] = cursor.fetchone()["producerName"]

                elif comment["userType"] == "venue":
                    cursor.execute("""
                        SELECT "venueName"
                        FROM "venues"
                        WHERE "id" = %s
                    """, (comment["userId"],))
                    comment["username"] = cursor.fetchone()["venueName"]

        return comments


# Get number of likes on content
def get_likes_count(content_id, content_type, table_user_type):

    conn = g.db
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:

        # Get table name 
        table_name = get_table_name(content_type, "like", table_user_type)

        # Get unique field 
        unique_field = get_unique_field(content_type, table_user_type)

        # If table name is reviewsUserVotes
        if table_name == "reviewsUserVotes" and table_user_type == "user":
            cursor.execute(f"""
                           SELECT upvotes FROM "{table_name}"
                           WHERE "id" = %s
                       """, (content_id,))
            upvotes = cursor.fetchone()
            if not upvotes or not upvotes.get("upvotes"):   # <-- safe check
                return 0
            return len(upvotes["upvotes"])

        # If table name is producerUpdateLikes or venueUpdateLikes
        if table_name == "producerUpdateLikes" or table_name == "venueUpdateLikes":
            cursor.execute(f"""
                           SELECT COUNT(*) FROM "{table_name}"
                           WHERE "id" = %s
                       """, (content_id,))
            upvotes = cursor.fetchone()
            if not upvotes or not upvotes.get("count"):   # <-- safe check
                return 0
            return upvotes["count"]

        # If table name is listingsLikes or 88BContentLikes
        if table_name == "listingsLikes" or table_name == "88BContentLikes":
            cursor.execute(f"""
                           SELECT COUNT(*) FROM "{table_name}"
                           WHERE "{unique_field}" = %s
                       """, (content_id,))
            upvotes = cursor.fetchone()
            if not upvotes or not upvotes.get("count"):   # <-- safe check
                return 0
            return upvotes["count"]
        


# Get a list of content id user has liked based on a list of content ids given
def get_liked_content_ids(user_id, user_type, content_type, content_ids):
    """
    Returns a list of content IDs liked by a given user.
    Works for reviewsUserVotes, producerUpdateLikes, venueUpdateLikes, listingsLikes, 88BContentLikes.
    """
    conn = g.db
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:

        # Get table name and unique field
        table_name = get_table_name(content_type, "like", user_type)
        unique_field = get_unique_field(content_type, user_type)

        # ---------- reviewsUserVotes ----------
        if table_name == "reviewsUserVotes" and user_type == "user":
            cursor.execute("""
                SELECT "id"
                FROM "reviewsUserVotes"
                WHERE "id" = ANY(%s)
                AND EXISTS (
                    SELECT 1
                    FROM jsonb_array_elements("upvotes") elem
                    WHERE (elem->>'id')::int = %s
                )
            """, (content_ids, user_id))
            rows = cursor.fetchall()
            return [row['id'] for row in rows] if rows else []

        # ---------- producerUpdateLikes / venueUpdateLikes ----------
        if table_name in ("producerUpdateLikes", "venueUpdateLikes"):
            cursor.execute(f"""
                SELECT "id"
                FROM "{table_name}"
                WHERE "id" = ANY(%s)
                AND "userId" = %s
            """, (content_ids, user_id))
            rows = cursor.fetchall()
            return [row['id'] for row in rows] if rows else []

        # ---------- listingsLikes / 88BContentLikes ----------
        if table_name in ("listingsLikes", "88BContentLikes"):
            cursor.execute(f"""
                SELECT "{unique_field}"
                FROM "{table_name}"
                WHERE "userId" = %s
                AND "{unique_field}" = ANY(%s)
            """, (user_id, content_ids))
            rows = cursor.fetchall()
            return [row[unique_field] for row in rows] if rows else []

        # Default fallback
        return []


# Get table name based on content_type and feature and user_type
def get_table_name(content_type, feature, user_type):

    if content_type == "Listing":
        if feature == "like" or feature == "dislike":
            return "listingsLikes"
        elif feature == "comment":
            return "listingsComments"
        
    elif content_type == "Review":
        if feature == "like" or feature == "dislike":
            return "reviewsUserVotes"
        elif feature == "comment":
            return "listingReviewsComments"
        
    elif content_type == "Update":
        if feature == "like" or feature == "dislike":
            if user_type == "producer":
                return "producerUpdateLikes"
            elif user_type == "venue":
                return "venueUpdateLikes"
            
        elif feature == "comment":
            if user_type == "producer":
                return "producerUpdateComments"
            elif user_type == "venue":
                return "venueUpdateComments"

    elif content_type == "88B":
        if feature == "like" or feature == "dislike":
            return "88BContentLikes"
        elif feature == "comment":
            return "88BContentComments"

    return None


# Get unique field from content comments tables based on content_type
def get_unique_field(content_type, user_type):
    if content_type == "Listing":
        return "listingId"

    elif content_type == "Review":
        return "reviewId"

    elif content_type == "Update":
        if user_type == "producer":
            return "producerUpdateId"
        elif user_type == "venue":
            return "venueUpdateId"

    elif content_type == "88B":
        return "contentId"

    return None







# -----------------------------------------------------------------------------------------
# [GET] Get random content
@blueprint.route("/getRandomListings/<user_id>/<user_type>")
def getRandomListings(user_id, user_type):
    conn = g.db

    try:

        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            # Fetch distinct dates by converting timestamps to dates
            cursor.execute('SELECT DISTINCT "addedDate"::DATE FROM "listings" WHERE "addedDate" != CURRENT_DATE')
            date_results = cursor.fetchall()

            if not date_results:
                return jsonify({"error": "No dates found in listings"}), 400

            try:
                # Extract 'addedDate' values properly from RealDictRow
                date_list = [row['addedDate'] for row in date_results if 'addedDate' in row]
                
                if not date_list:
                    return jsonify({"error": "Date extraction failed (empty list)"}), 400

                random_date = random.choice(date_list)  # Select a random date
            except Exception as e:
                return jsonify({"error": f"Random selection failed: {str(e)}"}), 500


            # Randomizer to determine if we want to include producerUpdates ONLY, venueUpdates ONLY, or BOTH
            update_type = random.choice(['producerUpdates', 'venueUpdates', 'both'])

            # Number of records to retrieve per call
            num_records = 30

            # Fetch listings from the selected random date 
            # Set random limit
            limit = random.randint(8, 15)
            cursor.execute('SELECT * FROM "listings" WHERE "addedDate"::DATE = %s LIMIT %s', (random_date, limit))
            listings_data = cursor.fetchall()

            # Determine if there are 10 records for listings from random date
            if len(listings_data) < num_records:

                # Get listings that have been created today
                # Set random limit
                limit = random.randint(2, 10)
                cursor.execute('SELECT * FROM "listings" WHERE "addedDate"::DATE = CURRENT_DATE LIMIT %s', (limit,))
                additional_listings = cursor.fetchall()
                listings_data.extend(additional_listings)

            new_listings_last_id = additional_listings[-1]['id'] if additional_listings else None

            # Loop through the listings and get the producer name
            for listing in listings_data:
                cursor.execute('SELECT "producerName" FROM "producers" WHERE "id" = %s', (listing['producerID'],))
                producer_data = cursor.fetchone()
                if producer_data:
                    listing['producerName'] = producer_data['producerName']
                else:
                    listing['producerName'] = None

                # Get rating for the listing
                cursor.execute("""
                    SELECT AVG("rating") AS "averageRating"
                    FROM "reviews"
                    WHERE "reviewTarget" = %s AND "reviewType" = 'Listing'
                """, (listing['id'],))

                rating_data = cursor.fetchone()
                listing['rating'] = round(rating_data['averageRating'],1) if rating_data and rating_data['averageRating'] is not None else '-'
                listing['contentType'] = 'Listing'

                # Get top 3 comments 
                listing['topComments'] = get_top_comments(listing['id'], 'Listing', None)
                
                # Get number of likes
                listing['totalLikes'] = get_likes_count(listing['id'], 'Listing', None)

            # Determine if there are 30 records, else, retrieve new reviews from other users (reviews up to a week ago)
            # Set random limit
            limit = random.randint(3, 8)
            if len(listings_data) < num_records:
                cursor.execute("""
                    SELECT * FROM "reviews"
                    WHERE "createdDate" >= NOW() - INTERVAL '14 days'
                    ORDER BY "createdDate" DESC
                    LIMIT %s
                """, (limit,))

                reviews = cursor.fetchall()

                # Add contentType to each review and retrieve userName
                for review in reviews:
                    review['contentType'] = 'Review'

                    # Get username
                    cursor.execute("SELECT username, photo FROM users WHERE id = %s", (review['userID'],))
                    user_data = cursor.fetchone()
                    review['username'] = user_data['username'] if user_data else None
                    review['userPhoto'] = user_data['photo'] if user_data else None

                    # Get listing name
                    cursor.execute("""SELECT "listingName" FROM listings WHERE id = %s""", (review['reviewTarget'],))
                    listing_data = cursor.fetchone()
                    review['listingName'] = listing_data['listingName'] if listing_data else None

                    # Get top 3 comments
                    review['topComments'] = get_top_comments(review['id'], 'Review', None)

                    # Get number of likes
                    review['totalLikes'] = get_likes_count(review['id'], 'Review', None)

            reviews_last_id = reviews[-1]['id'] if reviews else None

            producers_updates = []
            venues_updates = []
            
            # Determine if there are 30 records, else, retrieve announcements by venue and brand accounts
            if len(listings_data) + len(reviews) < num_records:

                # Calculate how many records are still needed
                remaining = num_records - len(listings_data) - len(reviews)

                # Set random limit
                limit = random.randint(1, remaining)

                # Based on randomizer, retrieve the relevant information
                if update_type == "producerUpdates":
                    cursor.execute("""
                        SELECT * FROM "producersUpdates" 
                        WHERE date >= NOW() - INTERVAL '14 days'
                        LIMIT %s
                    """, (limit,)
                    )
                    producers_updates = cursor.fetchall()

                elif update_type == "venueUpdates":
                    cursor.execute("""
                        SELECT * FROM "venuesUpdates" 
                        WHERE date >= NOW() - INTERVAL '14 days'
                        LIMIT %s
                    """, (limit,)
                    )
                    venues_updates = cursor.fetchall()

                elif update_type == "both":

                    # Randomly decide how many go to producers vs venues
                    producers_limit = random.randint(0, limit)   # any number between 0 and remaining
                    venue_limit = remaining - producers_limit 

                    cursor.execute("""
                        SELECT * FROM "producersUpdates" 
                        WHERE date >= NOW() - INTERVAL '14 days'
                        LIMIT %s
                    """, (producers_limit,)
                    )
                    producers_updates = cursor.fetchall()

                    cursor.execute("""
                        SELECT * FROM "venuesUpdates" 
                        WHERE date >= NOW() - INTERVAL '14 days'
                        LIMIT %s
                    """, (venue_limit,)
                    )
                    venues_updates = cursor.fetchall()

                # Add contentType to each update
                if len(producers_updates):
                    for update in producers_updates:
                        update['contentType'] = 'Update'

                        # Get producer name
                        cursor.execute("""SELECT "producerName", photo FROM producers WHERE id = %s""", (update['producerId'],))
                        producer_data = cursor.fetchone()
                        update['producerName'] = producer_data['producerName'] if producer_data else None
                        update['producerPhoto'] = producer_data['photo'] if producer_data else None

                        # Get top 3 comments
                        update['topComments'] = get_top_comments(update['id'], 'Update', 'producer')

                        # Get number of likes
                        update['totalLikes'] = get_likes_count(update['id'], 'Update', 'producer')

                if len(venues_updates):
                    for update in venues_updates:
                        update['contentType'] = 'Update'

                        # Get venue name
                        cursor.execute("""SELECT "venueName", photo FROM venues WHERE id = %s""", (update['venueId'],))
                        venue_data = cursor.fetchone()
                        update['venueName'] = venue_data['venueName'] if venue_data else None
                        update['venuePhoto'] = venue_data['photo'] if venue_data else None

                        # Get top 3 comments
                        update['topComments'] = get_top_comments(update['id'], 'Update', 'venue')

                        # Get number of likes
                        update['totalLikes'] = get_likes_count(update['id'], 'Update', 'venue')

        if not listings_data:
            return jsonify({"error": "No listings found for selected date"}), 400
        
        # Get current user's likes for the content
        if user_id and user_type:
            listings_likes = get_liked_content_ids(user_id, user_type, "Listing", [row["id"] for row in listings_data])
            reviews_likes = get_liked_content_ids(user_id, user_type, "Review", [row["id"] for row in reviews])
            producers_updates_likes = get_liked_content_ids(user_id, user_type, "Update", [row["id"] for row in producers_updates])
            venues_updates_likes = get_liked_content_ids(user_id, user_type, "Update", [row["id"] for row in venues_updates])

        content = listings_data + reviews + producers_updates + venues_updates
        random.shuffle(content)

        return jsonify({
            "content": content,
            "datedListingPreviousDate": random_date,
            "newListingsLastID": new_listings_last_id,
            "reviewsLastID": reviews_last_id,
            "pUpdateLastID": producers_updates[-1]['id'] if producers_updates else None,
            "vUpdateLastID": venues_updates[-1]['id'] if venues_updates else None,
            "listingsLikes": listings_likes,
            "reviewsLikes": reviews_likes,
            "producersUpdatesLikes": producers_updates_likes,
            "venuesUpdatesLikes": venues_updates_likes
        })
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500

# -----------------------------------------------------------------------------------------
# [POST] Get next 30 random content - Edited By CP [25 Aug]
@blueprint.route("/getNext30", methods=['POST'])
def getNext30():
    conn = g.db

    data = request.get_json()

    datedListingPreviousDate = data.get('datedListingPreviousDate')
    datedListingPreviousDate = parsedate_to_datetime(datedListingPreviousDate).date()
    newListingsLastID = data.get('newListingsLastID')
    pUpdateLastID = data.get('pUpdateLastID')

    if pUpdateLastID:
        pUpdateLastID = int(pUpdateLastID)
    else:
        pUpdateLastID = None
    reviewsLastID = data.get('reviewsLastID')
    if reviewsLastID:
        reviewsLastID = int(reviewsLastID)
    else:
        reviewsLastID = None
    vUpdateLastID = data.get('vUpdateLastID')
    if vUpdateLastID:
        vUpdateLastID = int(vUpdateLastID)
    else:
        vUpdateLastID = None

    # Initialize list
    listings_data = []
    recent_reviews = []
    producers_updates = []
    venues_updates = []

    try:

        with conn.cursor() as cursor:

            # Fetch distinct dates by converting timestamps to dates
            cursor.execute(
                """
                SELECT DISTINCT "addedDate"::DATE
                FROM "listings"
                WHERE "addedDate"::DATE != %s
                AND "addedDate"::DATE != CURRENT_DATE
                """, (datedListingPreviousDate,)
            )
            date_results = cursor.fetchall()

            if not date_results:
                return jsonify({"error": "No dates found in listings"}), 400

            try:
                # Extract 'addedDate' values properly from RealDictRow
                date_list = [row['addedDate'] for row in date_results if 'addedDate' in row]
                
                if not date_list:
                    return jsonify({"error": "Date extraction failed (empty list)"}), 400

                random_date = random.choice(date_list)  # Select a random date
            except Exception as e:
                return jsonify({"error": f"Random selection failed: {str(e)}"}), 500
            
            # Randomizer logic 
            limit = 30
            # Randomizer to determine if we want to include producerUpdates ONLY, venueUpdates ONLY, or BOTH
            update_type = random.choice(['producerUpdates', 'venueUpdates', 'both'])

            # Get dated listings 
            random_records = random.randint(3, 8)
            cursor.execute("""
                SELECT * FROM "listings"
                WHERE "addedDate" = %s
                LIMIT %s
            """, (random_date, random_records,))
            listings_data = cursor.fetchall()
            limit -= len(listings_data)
            
            # Get today's created listings after newListingsLastID
            random_records = random.randint(3, 10)
            
            if newListingsLastID and newListingsLastID != '':
                cursor.execute("""
                    SELECT * FROM "listings"
                    WHERE "addedDate" = CURRENT_DATE AND "id" > %s
                    LIMIT %s
                """, (newListingsLastID, random_records,))
                todays_listings = cursor.fetchall()
                listings_data.extend(todays_listings)
                newListingsLastID = todays_listings[-1]['id'] if todays_listings else None
                limit -= len(todays_listings)

            if listings_data:
                # Loop through the listings to get the average rating for each listing and producer name
                for listing in listings_data:
                    # Get the average rating for the listing
                    cursor.execute("""
                        SELECT AVG("rating") AS "averageRating"
                        FROM "reviews"
                        WHERE "reviewTarget" = %s
                    """, (listing['id'],))

                    avg_rating = cursor.fetchone()['averageRating']

                    if avg_rating is not None:
                        listing['rating'] = round(avg_rating, 1)
                    else:
                        listing['rating'] = '-'

                    listing['contentType'] = 'Listing'


            # Get reviews by users within the last 2 weeks after reviewsLastID
            random_records = random.randint(8, 12)
            cursor.execute("""
                SELECT * FROM "reviews"
                WHERE "createdDate" >= NOW() - INTERVAL '14 days'
                AND "id" > %s
                ORDER BY "createdDate" DESC
                LIMIT %s
            """, (reviewsLastID, random_records))
            recent_reviews = cursor.fetchall()
            reviewsLastID = recent_reviews[-1]['id'] if recent_reviews else None
            limit -= len(recent_reviews)

            for review in recent_reviews:
                review['contentType'] = 'Review'

                # Retrieve listing name
                cursor.execute('SELECT "listingName" FROM "listings" WHERE "id" = %s', (review['reviewTarget'],))
                listing = cursor.fetchone()
                review['listingName'] = listing['listingName'] if listing else None

                # Retrieve username and photo
                cursor.execute('SELECT "username", "photo" FROM "users" WHERE "id" = %s', (review['userID'],))
                user_data = cursor.fetchone()
                review['username'] = user_data['username'] if user_data else None
                review['userPhoto'] = user_data['photo'] if user_data else None

            # Get producer or venue updates after *UpdateLastID
            if limit > 0:

                random_records = random.randint(4, 7)
                if update_type == 'producerUpdates':
                    cursor.execute("""
                        SELECT * FROM "producersUpdates"
                        WHERE "date" >= NOW() - INTERVAL '2 weeks'
                        AND (%s IS NULL OR "id" > %s)
                        LIMIT %s
                    """, (pUpdateLastID, pUpdateLastID, random_records))
                    producers_updates = cursor.fetchall()

                elif update_type == 'venueUpdates':
                    cursor.execute("""
                        SELECT * FROM "venuesUpdates"
                        WHERE "date" >= NOW() - INTERVAL '2 weeks' 
                        AND (%s IS NULL OR "id" > %s)
                        LIMIT %s
                    """, (vUpdateLastID, vUpdateLastID, random_records,))
                    venues_updates = cursor.fetchall()

                else:
                    # Randomly decide how many go to producers vs venues
                    producers_limit = random.randint(0, limit)   # any number between 0 and remaining
                    venue_limit = limit - producers_limit 

                    cursor.execute("""
                        SELECT * FROM "producersUpdates" 
                        WHERE date >= NOW() - INTERVAL '14 days'
                        AND (%s IS NULL OR "id" > %s)
                        LIMIT %s
                    """, (pUpdateLastID, pUpdateLastID, producers_limit)
                    )
                    producers_updates = cursor.fetchall()

                    cursor.execute("""
                        SELECT * FROM "venuesUpdates" 
                        WHERE date >= NOW() - INTERVAL '14 days'
                        AND (%s IS NULL OR "id" > %s)
                        LIMIT %s
                    """, (vUpdateLastID, vUpdateLastID, venue_limit)
                    )
                    venues_updates = cursor.fetchall()

            if producers_updates:
                pUpdateLastID = producers_updates[-1]['id']

                for update in producers_updates:
                    update['contentType'] = 'Update'

                    # Get producer name
                    cursor.execute('SELECT "producerName", "photo" FROM "producers" WHERE "id" = %s', (update['producerId'],))
                    producer = cursor.fetchone()
                    update['producerName'] = producer['producerName'] if producer else None
                    update['producerPhoto'] = producer['photo'] if producer else None

            if venues_updates:
                vUpdateLastID = venues_updates[-1]['id']

                for update in venues_updates:
                    update['contentType'] = 'Update'
                    
                    # Get venue name
                    cursor.execute('SELECT "venueName", "photo" FROM "venues" WHERE "id" = %s', (update['venueId'],))
                    venue = cursor.fetchone()
                    update['venueName'] = venue['venueName'] if venue else None
                    update['venuePhoto'] = venue['photo'] if venue else None

        if len(listings_data) + len(recent_reviews) + len(producers_updates) + len(venues_updates) == 0:
            return jsonify([])
        

        # Shuffle data 
        content = listings_data + recent_reviews + producers_updates + venues_updates
        random.shuffle(content)

        return jsonify({
            "content": content,
            "datedListingLastID": random_date,
            "newListingsLastID": newListingsLastID,
            "pUpdateLastID": pUpdateLastID,
            "reviewsLastID": reviewsLastID,
            "vUpdateLastID": vUpdateLastID
        })

    except Exception as e:
        print("Error occurred while fetching data:", e)


# -----------------------------------------------------------------------------------------
# [POST] Like a content 
# Input: { "contentType": <content_type>, "contentId": <content_id>, "userId": <user_id>, "userType": <user_type> }
@blueprint.route("/likeContent", methods=['POST'])
def likeContent():
    data = request.json
    content_type = data.get("contentType")
    content_id = data.get("contentId")
    user_id = data.get("userId")
    user_type = data.get("userType")

    if not all([content_type, content_id, user_id, user_type]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        conn = g.db
        with conn.cursor() as cursor:

            # Retrieve the table name 
            table_name = get_table_name(content_type, "like", user_type)
            if not table_name:
                return jsonify({"error": "Invalid content type or user type"}), 400

            # Insert the like into the appropriate table
            
            # If it is listingLikes
            if table_name == "listingLikes":
                cursor.execute(f"""
                    INSERT INTO ""{table_name} ("listingId", "userId", "userType")
                    VALUES (%s, %s, %s)
                """, (content_id, user_id, user_type))
                cursor.commit()

            # If it is reviewsUserVotes
            elif table_name == "reviewsUserVotes" and user_type == "user":
                cursor.execute("""
                    UPDATE "reviewsUserVotes"
                    SET "upvotes" = "upvotes" || jsonb_build_array(
                        jsonb_build_object(
                            'userId', %s,
                            'date', CURRENT_TIMESTAMP
                        )
                    )
                    WHERE "id" = %s;
                """, (user_id, content_id))
                cursor.commit()

            # If it is producerUpdateLikes
            elif table_name == "producerUpdateLikes":
                cursor.execute(f"""
                    INSERT INTO "{table_name}" ("updateId", "userId", "userType")
                    VALUES (%s, %s, %s)
                """, (content_id, user_id, user_type))
                cursor.commit()

            # If it is venueUpdateLikes
            elif table_name == "venueUpdateLikes":
                cursor.execute(f"""
                    INSERT INTO "{table_name}" ("venueId", "userId", "userType")
                    VALUES (%s, %s, %s)
                """, (content_id, user_id, user_type))
                cursor.commit()

            # If it is 88BContentLikes
            elif table_name == "88BContentLikes":
                cursor.execute(f"""
                    INSERT INTO "{table_name}" ("contentId", "userId", "userType")
                    VALUES (%s, %s, %s)
                """, (content_id, user_id, user_type))
                cursor.commit()

            return jsonify({
                "message": "Content liked successfully",
                "contentId": content_id
            }), 200

    except Exception as e:
        print("Error occurred while liking content:", e)
        return jsonify({"error": "Failed to like content"}), 500


# -----------------------------------------------------------------------------------------
# [POST] Unlike a content
# Input: { "contentType": <content_type>, "contentId": <content_id>, "userId": <user_id>, "userType": <user_type> }
@blueprint.route("/unlikeContent", methods=['POST'])
def unlikeContent():
    data = request.json
    content_type = data.get("contentType")
    content_id = data.get("contentId")
    user_id = data.get("userId")
    user_type = data.get("userType")

    if not all([content_type, content_id, user_id, user_type]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        conn = g.db
        with conn.cursor() as cursor:

            # Retrieve the table name
            table_name = get_table_name(content_type, "unlike", user_type)
            if not table_name:
                return jsonify({"error": "Invalid content type or user type"}), 400

            # Delete the like from the appropriate table
            # If it is listingLikes
            if table_name == "listingLikes":
                cursor.execute(f"""
                    DELETE FROM "{table_name}"
                    WHERE "listingId" = %s AND "userId" = %s AND "userType" = %s
                """, (content_id, user_id, user_type))
                cursor.commit()

            elif table_name == "reviewsUserVotes" and user_type == "user":
                cursor.execute("""
                    UPDATE "reviewsUserVotes"
                    SET "upvotes" = COALESCE((
                        SELECT jsonb_agg(elem)
                        FROM jsonb_array_elements("upvotes") elem
                        WHERE elem->>'userId' <> %s
                    ), '[]')
                    WHERE "reviewId" = %s;
                """, (str(user_id), content_id))
                cursor.commit()

            elif table_name == "producerUpdateLikes":
                cursor.execute(f"""
                    DELETE FROM "{table_name}"
                    WHERE "updateId" = %s AND "userId" = %s AND "userType" = %s
                """, (content_id, user_id, user_type))
                cursor.commit()

            elif table_name == "venueUpdateLikes":
                cursor.execute(f"""
                    DELETE FROM "{table_name}"
                    WHERE "updateId" = %s AND "userId" = %s AND "userType" = %s
                """, (content_id, user_id, user_type))
                cursor.commit()

            elif table_name == "88BContentLikes":
                cursor.execute(f"""
                    DELETE FROM "{table_name}"
                    WHERE "contentId" = %s AND "userId" = %s AND "userType" = %s
                """, (content_id, user_id, user_type))
                cursor.commit()

            return jsonify({
                "message": "Content unliked successfully",
                "contentId": content_id
            }), 200

    except Exception as e:
        print("Error occurred while unliking content:", e)
        return jsonify({"error": "Failed to unlike content"}), 500


# -----------------------------------------------------------------------------------------
# [POST] Add a comment
# Input: { "contentType": <content_type>, "contentId": <content_id>, "userId": <user_id>, "userType": <user_type>, "comment": <comment_text>, "parentId": <parent_id> }
@blueprint.route("/addComment", methods=['POST'])
def addComment():
    data = request.json
    content_type = data.get("contentType")
    content_id = data.get("contentId")
    user_id = data.get("userId")
    user_type = data.get("userType")
    comment = data.get("comment")
    parent_id = data.get("parentId")  # Optional, for replies to comments

    if not all([content_type, content_id, user_id, user_type, comment]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        conn = g.db
        with conn.cursor() as cursor:

            # Retrieve the table name
            table_name = get_table_name(content_type, "comment", user_type)
            if not table_name:
                return jsonify({"error": "Invalid content type or user type"}), 400

            # Retrieve the unique field name
            unique_field = get_unique_field(content_type, user_type)
            if not unique_field:
                return jsonify({"error": "Invalid content type or user type"}), 400

            # Insert the comment into the appropriate table
            cursor.execute(f"""
                INSERT INTO "{table_name}" ("{unique_field}", "userId", "userType", "comment", "parentId")
                VALUES (%s, %s, %s, %s, %s)
            """, (content_id, user_id, user_type, comment, parent_id))
            cursor.commit()

            return jsonify({
                "message": "Comment added successfully",
                "contentId": content_id,
                "comment": comment
            }), 201

    except Exception as e:
        print("Error occurred while adding comment:", e)
        return jsonify({"error": "Failed to add comment"}), 500


# -----------------------------------------------------------------------------------------
# [PUT] Edit a comment
# Input: { "contentType": <content_type>, "userId": <user_id>, "userType": <user_type>, "commentId": <comment_id>, "newComment": <new_comment_text> }
@blueprint.route("/editComment", methods=['PUT'])
def editComment():
    data = request.json
    content_type = data.get("contentType")
    user_id = data.get("userId")
    user_type = data.get("userType")
    comment_id = data.get("commentId")
    new_comment = data.get("newComment")

    if not all([content_type, user_id, user_type, comment_id, new_comment]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        conn = g.db
        with conn.cursor() as cursor:

            # Retrieve the table name
            table_name = get_table_name(content_type, "comment", user_type)
            if not table_name:
                return jsonify({"error": "Invalid content type or user type"}), 400

            # Update the comment in the appropriate table
            cursor.execute(f"""
                UPDATE "{table_name}"
                SET "comment" = %s
                WHERE id = %s AND "userId" = %s AND "userType" = %s
            """, (new_comment, comment_id, user_id, user_type))
            cursor.commit()

            return jsonify({
                "message": "Comment edited successfully",
                "commentId": comment_id,
                "newComment": new_comment
            }), 200

    except Exception as e:
        print("Error occurred while editing comment:", e)
        return jsonify({"error": "Failed to edit comment"}), 500


# -----------------------------------------------------------------------------------------
# [DELETE] Delete a comment
# Input: { "contentType": <content_type>, "userId": <user_id>, "userType": <user_type>, "commentId": <comment_id> }
@blueprint.route("/deleteComment", methods=['DELETE'])
def deleteComment():
    data = request.json
    content_type = data.get("contentType")
    user_id = data.get("userId")
    user_type = data.get("userType")
    comment_id = data.get("commentId")

    if not all([content_type, user_id, user_type, comment_id]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        conn = g.db
        with conn.cursor() as cursor:

            # Retrieve the table name
            table_name = get_table_name(content_type, "comment", user_type)
            if not table_name:
                return jsonify({"error": "Invalid content type or user type"}), 400

            # Delete the comment from the appropriate table
            cursor.execute(f"""
                DELETE FROM "{table_name}"
                WHERE id = %s AND "userId" = %s AND "userType" = %s
            """, (comment_id, user_id, user_type))
            cursor.commit()

            return jsonify({
                "message": "Comment deleted successfully"
            }), 200

    except Exception as e:
        print("Error occurred while deleting comment:", e)
        return jsonify({"error": "Failed to delete comment"}), 500

    user_id = data.get("userId")
    user_type = data.get("userType")
    comment_id = data.get("commentId")

    if not all([content_type, content_id, user_id, user_type, comment_id]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        conn = g.db
        with conn.cursor() as cursor:

            # Retrieve the table name
            table_name = get_table_name(content_type, "comment", user_type)
            if not table_name:
                return jsonify({"error": "Invalid content type or user type"}), 400

            # Delete the comment from the appropriate table
            cursor.execute(f"""
                DELETE FROM "{table_name}"
                WHERE id = %s AND "userId" = %s AND "userType" = %s
            """, (comment_id, user_id, user_type))
            cursor.commit()

            return jsonify({
                "message": "Comment deleted successfully",
                "commentId": comment_id
            }), 200

    except Exception as e:
        print("Error occurred while deleting comment:", e)
        return jsonify({"error": "Failed to delete comment"}), 500

