# Port: 5000
# Routes: /getAccountRequests (GET), /getCountries (GET), /getListings (GET), /getListingsByIDs (POST), /getListing/<id> (GET), /getProducers (GET), /getProducer/<id> (GET),
#           /getRecentListingReviews/<id> (GET), /getAllListingsNames (GET), /getBookmarkListings (POST), /getUserReviewSummary/<id> (GET),
#           /getReviews (GET), /getReviewsByListingIDs (POST), /getReviewByTarget/<id> (GET), /getReviewsByUserIds (GET), /getProducerTourReviews (GET), /getVenueReviews (GET), 
#           /getVenueReviewsByVenueId/<id> (GET), /getProducerReviewsByProducerId/<id> (GET),
#           /getUsers (GET), /getUsersFromList (POST), /getUserFollowListDetails (POST) /getUser/<id> (GET), 
#           /getUserPhoto/<id>/<userType> (GET), /getUserByUsername/<username> (GET), /getVenues (GET), 
#           /getVenue/<id> (GET), /getVenuesAPI (GET), /getDrinkTypes (GET), /getTypeCategories (GET), /getRequestListings (GET), /getRequestListing/<id> (GET), /getRequestEdits (GET), 
#           /getRequestEdit/<id> (GET), /getModRequests (GET), /getFlavourTags (GET), /getSubTags (GET), /getObservationTags (GET), /getColours (GET), 
#           /getSpecialColours (GET), /getLanguages (GET), /getServingTypes (GET), /getProducersProfileViews (GET), /getVenuesProfileViewsByVenue/<id> (GET), /getRequestInaccuracyByVenue/<id> (GET)
#           /getUserFollowList/<id> (GET), /getUserNames (GET), /checkFollowing/<userId>/<userType>/<followId>/<followType> (GET) /getLatestNews (GET)
# -----------------------------------------------------------------------------------------

# pip install python-bsonjs
# pip install Flask
# pip install Flask Flask-PyMongo
# pip install pymongo
# pip install flask-cors

import os
import json
import random # ADDED BY SMU GROUP 3
import feedparser
import re
import requests
from urllib.parse import unquote
from bs4 import BeautifulSoup
from bson import json_util
from flask import Blueprint, g, jsonify, request
from psycopg2.extras import RealDictCursor # ADDED BY SMU GROUP 3
from decimal import Decimal
from datetime import datetime, timezone, date, timedelta
from scripts import pointsHelperFunc

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

# clean up html tags
def clean_html(html):
    """Remove HTML tags and extract plain text."""
    if not html:
        return ""
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator=" ")  # Extract plain text with spaces instead of HTML tags
    
    text = text.replace("\\n", "\n")  # Replace escaped '\n' with actual new lines
    text = text.replace('\\"', '"')  # Replace escaped quotes with actual quotes
    text = text.replace("\\'", "'")  # Replace escaped single quotes (if needed)
    text = re.sub(r'\\+', '', text)  # Remove any remaining backslashes
    text = re.sub(r'\s+', ' ', text).strip()  # Remove excessive spaces
    
    return text

# # converts 88 bamboo atom rss to JSON
def parse_rss(rss_url):
    feed = feedparser.parse(rss_url)

    if not feed.entries:
        return {"error": "Invalid RSS feed or no entries found."}

    rss_data = {
        "feed": {
            "title": feed.feed.get("title", "No title"),
            "link": feed.feed.get("link", "No link"),
            "description": feed.feed.get("subtitle", "No description"),
            "language": feed.feed.get("language", "Unknown"),
            "updated": feed.feed.get("updated", "Unknown date"),
            "author": feed.feed.get("author", "Unknown author")
        },
        "entries": []
    }

    for entry in feed.entries:
        formatted_entry = {
            "title": entry.get("title", "No title"),
            "link": entry.get("link", "No link"),
            "published": entry.get("published", "Unknown date"),
            "summary": clean_html(entry.get("summary", "No summary")), 
            "author": entry.get("author", "Unknown author"),
            "categories": [tag.term for tag in entry.get("tags", [])] if "tags" in entry else [],
            "content": clean_html(entry.get("content", [{"value": ""}])[0]["value"] if "content" in entry else ""),  
        }
        rss_data["entries"].append(formatted_entry)

    return rss_data

def get_og_image(url):
    """Extract Open Graph image from a given article URL."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}  # Prevent bot-blocking
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        og_image = soup.find("meta", property="og:image")

        if og_image and og_image.get("content"):
            return og_image["content"]
        return None  # No OG image found
    except requests.exceptions.RequestException:
        return None  # Request failed


# converts BSON to JSON
def parse_json(data):
    return json.loads(json_util.dumps(data))

# Helper function to fetch user data from the database
def fetch_user_data(cursor, user_id):
    cursor.execute('SELECT * FROM "users" WHERE "id" = %s', (user_id,))

    # Remove unnecessary fields
    user_data = cursor.fetchone()

    return user_data

# Helper function to fetch drink lists for a user
def fetch_drink_lists(cursor, user_id):
    # First, get all drink lists for the user
    cursor.execute("""
        SELECT "id", "listName", "listDesc"
        FROM "usersDrinkLists"
        WHERE "userId" = %s
    """, (user_id,))
    
    drink_lists_data = cursor.fetchall()
    result = {}

    for row in drink_lists_data:
        list_id = row["id"]
        list_name = row["listName"]

        # Initialize the list in the result dictionary
        result[list_name] = {
            "listDesc": row["listDesc"],
            "listItems": [],
        }

        # Fetch the drinks for this list, along with their addedDate
        cursor.execute("""
            SELECT "drinkId", "addedDate"
            FROM "usersDrinkListItems"
            WHERE "listId" = %s
            ORDER BY "addedDate" DESC
        """, (list_id,))
        
        drinks_data = cursor.fetchall()

        # Add drinks to the list
        result[list_name]["listItems"] = [
            {"drinkId": row["drinkId"], "addedDate": row["addedDate"]}
            for row in drinks_data
        ]

    return result

# Helper function to fetch follow lists for a user
def fetch_follow_lists(cursor, user_id):
    cursor.execute("""
        SELECT "users", "producers", "venues"
        FROM "usersFollowLists"
        WHERE "userId" = %s
    """, (user_id,))
    follow_lists_data = cursor.fetchone()
    
    return {
        "users": follow_lists_data["users"] if follow_lists_data and follow_lists_data["users"] else [],
        "producers": follow_lists_data["producers"] if follow_lists_data and follow_lists_data["producers"] else [],
        "venues": follow_lists_data["venues"] if follow_lists_data and follow_lists_data["venues"] else []
    }

# Helper function to fetch venue menu items based on venueId
def fetch_venue_listings(cursor, venue_id):
    cursor.execute("""
        SELECT * 
        FROM "listings" 
        WHERE "id" IN (
            SELECT mi."itemID"
            FROM "menuItems" mi
            JOIN "venuesMenu" vm ON mi."sectionId" = vm."id"
            WHERE vm."venueId" = %s
        );
    """, (venue_id,))
    venue_items = cursor.fetchall()

    return venue_items

# def modifyPhotos():
#     data = db.producers.find({})
#     dataEncode = parse_json(data)
#     for doc in dataEncode:
#         try:
#             if(doc['photo']):
#                 photo = s3Images.uploadBase64ImageToS3(doc['photo'])
#                 updateImage = db.producers.update_one({'_id': ObjectId(doc['_id']['$oid'])}, {'$set': {'photo': photo, 'updates': []}})
#         except Exception as e:
#             print(e)
#         print(doc['_id'])

# modifyPhotos()

# -----------------------------------------------------------------------------------------
# [GET] accountRequests
@blueprint.route('/getAccountRequests', methods=['GET'])
def getAccountRequests():
    conn = g.db
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM "accountRequests"')
        allAccountRequests = cursor.fetchall()

    if not allAccountRequests:
        return jsonify([])

    return jsonify(allAccountRequests)

# -----------------------------------------------------------------------------------------
# [GET] Countries
@blueprint.route('/getCountries', methods=['GET'])
def getCountries():
    conn = g.db
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM countries")
        allCountries = cursor.fetchall()

    if not allCountries:
        return jsonify([])
    
    return jsonify(allCountries)

# -----------------------------------------------------------------------------------------
# [GET] Listings
@blueprint.route("/getListings", methods=['GET'])
def getListings():
    conn = g.db

    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM "listings"')
        listings_data = cursor.fetchall()
    
    if not listings_data:
        return jsonify([])

    return jsonify(listings_data)


# -----------------------------------------------------------------------------------------
# [POST] Listings by IDs
@blueprint.route("/getListingsByIDs", methods=['POST'])
def getListingsByIDs():
    conn = g.db

    listing_ids = request.json.get('listingIDs', [])

    if not listing_ids:
        return jsonify([]), 404

    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM "listings" WHERE "id" IN %s', (tuple(listing_ids),))
        listings_data = cursor.fetchall()
    
    if not listings_data:
        return jsonify([])

    return jsonify(listings_data)

# -----------------------------------------------------------------------------------------
# [GET] Get Listings from db where id> last item in list
@blueprint.route("/getNext30/<id>")
def getNext30(id):
    conn = g.db
    id = int(id)
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM "listings" where "id" > %s LIMIT 30', (id,))
        listings_data = cursor.fetchall()
    
    if not listings_data:
        return jsonify([])

    return jsonify(listings_data)

# -----------------------------------------------------------------------------------------
# [GET] Listings from db when filter is applied for next 30 in discovery tab
@blueprint.route("/getFiltered30/<id>")
def getFiltered30(id):
    conn = g.db
    id = int(id)
    drinkType= request.args.get('drinkType')  # e.g. ?age=30
    drinkCategory = request.args.get('drinkCategory')
    
    with conn.cursor() as cursor:
        if(drinkType and drinkCategory):
            cursor.execute('SELECT * FROM "listings" where "id" > %s AND "drinkType" = %s AND "typeCategory" = %s LIMIT 30', (id,drinkType,drinkCategory,))
        elif(drinkType):
            cursor.execute('SELECT * FROM "listings" where "id" > %s AND "drinkType" = %s LIMIT 30', (id,drinkType,))      
        else:
            cursor.execute('SELECT * FROM "listings" where "id" > %s LIMIT 30', (id,))
        listings_data = cursor.fetchall()
    
    if not listings_data:
        return jsonify([])

    return jsonify(listings_data)

# -----------------------------------------------------------------------------------------
# [GET] Get Listings from next in following list for both venue and producer
@blueprint.route("/getNextFollowing30/<id>")
def getNextFollowing30(id):
    conn = g.db
    id = int(id)

    followedProducers = request.args.get('followedProducers').replace('[', '').replace(']', '').replace('"', '').split(',')
    followedVenues = request.args.get('followedVenues')
    print(followedVenues)
    # Make sure followedProducers is a tuple so SQL can process
    placeholders = ', '.join(['%s'] * len(followedProducers))

    with conn.cursor() as cursor:
        query = f'SELECT * FROM "listings" WHERE "id" > %s AND "producerID" IN ({placeholders}) LIMIT 30'
        params = (id, *followedProducers)
        cursor.execute(query, params)
        listings_data = cursor.fetchall()
        if followedVenues != '"null"':
            print('in')
            venue_listings = fetch_venue_listings(cursor, followedVenues.replace('"',''))
            listings_data += venue_listings
    
    if not listings_data:
        return jsonify([])

    return jsonify(listings_data)

# -----------------------------------------------------------------------------------------
# [GET] Listings from db when filter is applied for next 30 in following tab
@blueprint.route("/getFilteredFollowing30/<id>")
def getFilteredFollowing30(id):
    conn = g.db
    id = int(id)
    drinkType= request.args.get('drinkType')  # e.g. ?age=30
    drinkCategory = request.args.get('drinkCategory')
    
    with conn.cursor() as cursor:
        if(drinkType and drinkCategory):
            cursor.execute('SELECT * FROM "listings" where "id" > %s AND "drinkType" = %s AND "typeCategory" = %s LIMIT 30', (id,drinkType,drinkCategory,))
        elif(drinkType):
            cursor.execute('SELECT * FROM "listings" where "id" > %s AND "drinkType" = %s LIMIT 30', (id,drinkType,))      
        else:
            cursor.execute('SELECT * FROM "listings" where "id" > %s LIMIT 30', (id,))
        listings_data = cursor.fetchall()
    
    if not listings_data:
        return jsonify([])

    return jsonify(listings_data)

# -----------------------------------------------------------------------------------------
# [GET] Specific Listing
@blueprint.route("/getListing/<id>")
def getListing(id):
    conn = g.db

    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM "listings" WHERE "id" = %s', (id,))
        listing_data = cursor.fetchone()

    if listing_data is None:
        return jsonify([])
    
    return jsonify(listing_data)

# [GET] Specific Listings By Producer
@blueprint.route("/getListingsByProducer/<id>")
def getListingsByProducer(id):
    conn = g.db

    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM "listings" WHERE "producerID" = %s', (id,))
        listings_data = cursor.fetchall()

    if not listings_data:
        return jsonify([])

    return jsonify(listings_data)

# [GET] Get Listings details by listing name
@blueprint.route("/getListingByName/<listing_name>")
def getListingByName(listing_name):
    # URL decode the listing name in case there are special characters
    listing_name = unquote(listing_name)
    
    print(f"Decoded listing_name: {listing_name}")

    conn = g.db

    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM "listings" WHERE "listingName" = %s', (listing_name,))
        listing_data = cursor.fetchone()

    if listing_data is None:
        return jsonify({"code": 404, "message": "Listing not found"}), 404

    return jsonify(listing_data)

# -----------------------------------------------------------------------------------------

# ================== POSTGRESQL FORMAT ==================

# ----------------------
# [OLD] TO BE DELETED:
# ----------------------

# [GET] Producers
@blueprint.route("/getProducers")
def getProducers():
    conn = g.db
    cur = conn.cursor()

    try:
        # Query to get producers and related data
        query = """
            SELECT 
                p.id, p."producerName", p."producerDesc", p."originCountry", p."mainDrinks", p.photo, 
                p."hashedPassword", p."claimStatus", p."statusOB", p.username, p."producerLink", 
                p."yearFounded", p."activeStatus", p.owner, p.location, p."openForTours", p.website,
                p."stripeCustomerId", p."claimStatusCheckDate", p."isIndependentBottler",
                COALESCE((
                    SELECT json_agg(json_build_object(
                        'id', qa.id,
                        'question', qa.question,
                        'answer', qa.answer,
                        'date', qa.date,
                        'userId', qa."userId",
                        'producerId', qa."producerId"
                    ))
                    FROM "producersQuestionAnswers" qa
                    WHERE qa."producerId" = p.id
                ), '[]') AS "questionsAnswers",
                COALESCE((
                    SELECT row_to_json(oh)
                    FROM "producersOpeningHours" oh
                    WHERE oh."producerId" = p.id
                ), '{}'::json) AS "openingHours",
                COALESCE((
                    SELECT json_agg(json_build_object(
                        'id', u.id,
                        'date', u.date,
                        'text', u.text,
                        'photo', u.photo,
                        'producerId', u."producerId",
                        'likes', COALESCE((
                            SELECT json_agg(json_build_object('userId', l."userId", 'userType', l."userType"))
                            FROM "producerUpdateLikes" l
                            WHERE l."updateId" = u.id
                        ), '[]')
                    ) ORDER BY u.id)
                    FROM "producersUpdates" u
                    WHERE u."producerId" = p.id
                ), '[]') AS updates
            FROM producers p
            ORDER BY p.id
        """

        cur.execute(query)
        producers_data = cur.fetchall()

        if not producers_data:
            return jsonify([])

        producers_list = []
        for row in producers_data:
            producer = dict(row)
            producer['questionsAnswers'] = producer['questionsAnswers'] if producer['questionsAnswers'] else []
            producer['openingHours'] = producer['openingHours'] if producer['openingHours'] else {}
            producer['updates'] = producer['updates'] if producer['updates'] else []
            producers_list.append(producer)

        return jsonify(producers_list), 200

    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred retrieving producers."
            }
        ), 500

    finally:
        cur.close()

# [GET] Specific Producer
@blueprint.route("/getProducer/<int:id>")
def getProducer(id):
    conn = g.db
    cur = conn.cursor()

    try:
        # Query to get a specific producer and related data
        query = """
            SELECT 
                p.id, p."producerName", p."producerDesc", p."originCountry", p."mainDrinks", p.photo, 
                p."hashedPassword", p."claimStatus", p."statusOB", p.username, p."producerLink", 
                p."yearFounded", p."activeStatus", p.owner, p.location, p."openForTours", p.website,
                p."stripeCustomerId", p."claimStatusCheckDate", p."isIndependentBottler",
                COALESCE((
                    SELECT json_agg(json_build_object(
                        'id', qa.id,
                        'question', qa.question,
                        'answer', qa.answer,
                        'date', qa.date,
                        'userId', qa."userId",
                        'producerId', qa."producerId"
                    ))
                    FROM "producersQuestionAnswers" qa
                    WHERE qa."producerId" = p.id
                ), '[]') AS "questionsAnswers",
                COALESCE((
                    SELECT row_to_json(oh)
                    FROM "producersOpeningHours" oh
                    WHERE oh."producerId" = p.id
                ), '{}'::json) AS "openingHours",
                COALESCE((
                    SELECT json_agg(json_build_object(
                        'id', u.id,
                        'date', u.date,
                        'text', u.text,
                        'photo', u.photo,
                        'producerId', u."producerId",
                        'likes', COALESCE((
                            SELECT json_agg(json_build_object('userId', l."userId", 'userType', l."userType"))
                            FROM "producerUpdateLikes" l
                            WHERE l."updateId" = u.id
                        ), '[]')
                    ))
                    FROM "producersUpdates" u
                    WHERE u."producerId" = p.id
                ), '[]') AS updates
            FROM producers p
            WHERE p.id = %s
        """

        cur.execute(query, (id,))
        producer_data = cur.fetchone()
        print("This is producer data", producer_data)

        if producer_data is None:
            return jsonify({"message": "Producer not found"}), 404

        producer = dict(producer_data)
        producer['questionsAnswers'] = producer['questionsAnswers'] if producer['questionsAnswers'] else []
        producer['openingHours'] = producer['openingHours'] if producer['openingHours'] else {}
        producer['updates'] = producer['updates'] if producer['updates'] else []

        return jsonify(producer), 200

    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred retrieving the producer."
            }
        ), 500

    finally:
        cur.close()

# [GET] Specific Producer
@blueprint.route("/getProducerByRequestId/<id>")
def getProducerByRequestId(id):
    conn = g.db
    cur = conn.cursor()

    try:
        query = """
            SELECT 
                p.id, p."producerName", p."producerDesc", p."originCountry", p."mainDrinks", p.photo, 
                p."hashedPassword", p."claimStatus", p."statusOB", p.username, p."producerLink", 
                p."yearFounded", p."activeStatus", p.owner, p.location, p."openForTours", p.website,
                p."stripeCustomerId", p."claimStatusCheckDate", p."isIndependentBottler",
                COALESCE((
                    SELECT json_agg(json_build_object(
                        'id', qa.id,
                        'question', qa.question,
                        'answer', qa.answer,
                        'date', qa.date,
                        'userId', qa."userId",
                        'producerId', qa."producerId"
                    ))
                    FROM "producersQuestionAnswers" qa
                    WHERE qa."producerId" = p.id
                ), '[]') AS "questionsAnswers",
                COALESCE((
                    SELECT row_to_json(oh)
                    FROM "producersOpeningHours" oh
                    WHERE oh."producerId" = p.id
                ), '{}'::json) AS "openingHours",
                COALESCE((
                    SELECT json_agg(json_build_object(
                        'id', u.id,
                        'date', u.date,
                        'text', u.text,
                        'photo', u.photo,
                        'producerId', u."producerId",
                        'likes', COALESCE((
                            SELECT json_agg(json_build_object('userId', l."userId", 'userType', l."userType"))
                            FROM "producerUpdateLikes" l
                            WHERE l."updateId" = u.id
                        ), '[]')
                    ))
                    FROM "producersUpdates" u
                    WHERE u."producerId" = p.id
                ), '[]') AS updates
            FROM "producers" p
            WHERE p.id = %s
        """

        cur.execute(query, (id,))
        producer_data = cur.fetchone()

        if producer_data is None:
            return jsonify({"message": "Producer not found"}), 404

        producer = dict(producer_data)
        producer['questionsAnswers'] = producer['questionsAnswers'] if producer['questionsAnswers'] else []
        producer['openingHours'] = producer['openingHours'] if producer['openingHours'] else {}
        producer['updates'] = producer['updates'] if producer['updates'] else []

        return jsonify(producer), 200
    
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred retrieving the producer."
            }
        ), 500
    
    finally:
        cur.close()

# [GET] List of unique producers names and id
@blueprint.route("/getUniqueProducersNamesID")
def getUniqueProducersNamesID():
    conn = g.db
    with conn.cursor() as cursor:
        cursor.execute('SELECT DISTINCT "producerName", "isIndependentBottler", "id" FROM "producers"')
        producers_data = cursor.fetchall()

    if not producers_data:
        return jsonify({
            "code": 404,
            "message": "No producers found."
        })
    
    # Convert the data to a list of dictionaries

    producers_list = []
    for producer in producers_data:
        if producer["producerName"] == None:
            continue
        producer_dict = {
            "producerName": producer["producerName"],
            "isIndependentBottler": producer["isIndependentBottler"],
            "id": producer["id"]
        }
        producers_list.append(producer_dict)

    return jsonify({
        "code": 200,
        "message": "Producers fetched successfully.",
        "data": producers_list
    })
# [GET] All producers with basic info needed for listings
@blueprint.route("/getAllProducers")
def getAllProducers():
    conn = g.db
    with conn.cursor() as cursor:
        cursor.execute('SELECT "id", "producerName" FROM "producers"')
        producers_data = cursor.fetchall()

    if not producers_data:
        return jsonify([])
    
    return jsonify(producers_data)



# ----------------------
# [NEW] TO BE ADDED:
# ----------------------

# # [GET] Producers
# @blueprint.route("/getProducers")
# def getProducers():
#     db = g.db
#     # Fetch all producers
#     producers_data = db.producers.find({})
#     allProducers = []
#     for producer in producers_data:
#         # Fetch the related question answers based on the id stored in producer's questionAnswers
#         question_answers_data = db.producersQuestionAnswers.find({
#             "id": {"$in": producer['questionAnswers']}
#         })
#         producer['questionsAnswers'] = list(question_answers_data)
#         # Fetch the related updates based on the id stored in producer's updates
#         updates_data = db.producersUpdates.find({
#             "id": {"$in": producer['updates']}
#         })
#         producer['updates'] = list(updates_data)
#         allProducers.append(producer)
#     return parse_json(allProducers)

# # [GET] Specific Producer by ID
# @blueprint.route("/getProducer/<id>")
# def getProducer(id):
#     db = g.db
#     # Fetch the specific producer
#     producer = db.producers.find_one({"_id": ObjectId(id)})
#     if producer is None:
#         return []
#     # Fetch related question answers based on the id(s) in producer's questionAnswers
#     question_answers_data = db.producersQuestionAnswers.find({
#         "id": {"$in": producer['questionAnswers']}
#     })
#     producer['questionsAnswers'] = list(question_answers_data)
#     # Fetch related updates based on the id(s) in producer's updates
#     updates_data = db.producersUpdates.find({
#         "id": {"$in": producer['updates']}
#     })
#     producer['updates'] = list(updates_data)
#     return parse_json(producer)

# # [GET] Specific Producer by Request ID
# @blueprint.route("/getProducerByRequestId/<id>")
# def getProducerByRequestId(id):
#     db = g.db
#     # Fetch the specific producer by requestId
#     producer = db.producers.find_one({"requestId": ObjectId(id)})
#     if producer is None:
#         return []
#     # Fetch related question answers based on the id(s) in producer's questionAnswers
#     question_answers_data = db.producersQuestionAnswers.find({
#         "id": {"$in": producer['questionAnswers']}
#     })
#     producer['questionsAnswers'] = list(question_answers_data)
#     # Fetch related updates based on the id(s) in producer's updates
#     updates_data = db.producersUpdates.find({
#         "id": {"$in": producer['updates']}
#     })
#     producer['updates'] = list(updates_data)
#     return parse_json(producer)

# =======================================================

# -----------------------------------------------------------------------------------------

# ================== POSTGRESQL FORMAT ==================

# ----------------------
# [OLD] TO BE DELETED:
# ----------------------

# -- ========= [NEW!] "reviewsUserVotes" =========
# CREATE TABLE "reviewsUserVotes" (
#     "id" SERIAL PRIMARY KEY,
#     "upvotes" TEXT[], -- Contain "users"("id")s
#     "downvotes" TEXT[], -- Contain "users"("id")s
#     "reviewId" INTEGER REFERENCES "reviews"("id") on DELETE SET NULL -- [!] reference "reviews" FK
# );


# [GET] Get recent listing reviews by a specific user + top 5 listings based on the review ratings + number of reviews done (aka drink count)
@blueprint.route("/getRecentListingReviews/<id>")
def getRecentListingReviews(id):

    conn = g.db

    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT "reviews".*, "reviewsUserVotes"."upvotes", "reviewsUserVotes"."downvotes"
            FROM "reviews"
            LEFT JOIN "reviewsUserVotes" ON "reviews"."id" = "reviewsUserVotes"."reviewId"
            WHERE "reviews"."userID" = %s 
            AND "reviews"."reviewType" = 'Listing'
            AND "reviews"."createdDate" >= NOW() - INTERVAL '5 days'
            ORDER BY "reviews"."createdDate" DESC
            LIMIT 10
        """, (id,))

        reviews_data = cursor.fetchall()

        if not reviews_data:
            reviews_data = []

    for review in reviews_data:
        review["userVotes"] = {
            "upvotes": review["upvotes"] if review["upvotes"] else [],
            "downvotes": review["downvotes"] if review["downvotes"] else []
        }
        del review["upvotes"]
        del review["downvotes"]

    # Retrieve top 5 listings based on the review ratings
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT "reviewTarget" FROM "reviews" WHERE "reviewType" = 'Listing' AND "rating" >= 8
            LIMIT 10
        """)
        top_listings_data = cursor.fetchall()

    top_listings = []

    # Convert the top listings data to a list
    for listing in top_listings_data:
        top_listings.append(listing["reviewTarget"])

    # Retrieve the number of reviews done by the user (number of unique listings reviewed)
    with conn.cursor() as cursor:
        cursor.execute('SELECT COUNT(DISTINCT "reviewTarget") FROM "reviews" WHERE "userID" = %s', (id,))
        drink_count = cursor.fetchone()


    return jsonify({"recentReview" : reviews_data,
                    "topListings" : top_listings,
                    "drinkCount" : drink_count["count"]}), 200
    

# [GET] Get all listings names
@blueprint.route("/getAllListingsNames")
def getAllListingsNames():
    conn = g.db
    with conn.cursor() as cursor:
        cursor.execute('SELECT "id", "listingName" FROM "listings"')
        listings_data = cursor.fetchall()

    if not listings_data:
        return jsonify([]), 404

    return jsonify(listings_data), 200

# [POST] Get bookmarked listings
@blueprint.route("/getBookmarkListings", methods=['POST'])
def getBookmarkListings():
    conn = g.db
    listing_ids = [listing["drinkId"] for listing in request.json.get('listingIDs', [])]

    if not listing_ids:
        return jsonify({
            "code": 404,
            "message": "At least one listing ID is required."
        }), 404

    # Retrieve listing information based on the provided IDs
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM "listings" WHERE "id" IN %s', (tuple(listing_ids),))
        bookmarked_listings = cursor.fetchall()

        if not bookmarked_listings:
            return jsonify([]), 404

        return_data = {}
        # Fetch the average review rating for each listing
        for listing in bookmarked_listings:
            cursor.execute('SELECT AVG("rating") FROM "reviews" WHERE "reviewTarget" = %s', (listing["id"],))
            avg_rating = cursor.fetchone()

            # Add to listing data
            return_data[listing["id"]] = listing
            return_data[listing["id"]]["avgRating"] = avg_rating["avg"]

    return jsonify(return_data), 200

# [GET] Get user's review summary
@blueprint.route("/getUserReviewSummary/<id>")
def getUserReviewSummary(id):
    conn = g.db

    with conn.cursor() as cursor:
        # Step 1: Get all listings reviewed by the user
        cursor.execute('''
            SELECT "reviewTarget", "address", "taggedUsers"
            FROM "reviews"
            WHERE "userID" = %s
        ''', (id,))
        reviewed_listings = cursor.fetchall()

        if not reviewed_listings:
            return jsonify({
                "code": 404,
                "message": "No reviews found for the specified user."
            }), 404
        
        # Use a set for distinct reviewTargets and addresses, but allow duplicates for taggedUsers
        unique_listing_id = []
        locations_tagged = set()
        tagged_users = []

        for review in reviewed_listings:
            # Add distinct reviewTargets
            if review.get("reviewTarget"):
                if review["reviewTarget"] not in unique_listing_id:
                    unique_listing_id.append(review["reviewTarget"])
            # Add distinct addresses
            if review.get("address"):
                locations_tagged.add(review["address"])
            # For taggedUsers, append all users (assuming it's stored as an array)
            if review.get("taggedUsers"):
                tagged_users.extend(review["taggedUsers"])

        locations_tagged = list(locations_tagged)
        tagged_users_count = len(tagged_users)

        # Step 2: Get the number of unique drinkType and typeCategory based on the listings reviewed
        categories_reviewed_dict = {}  # {drinkType: {typeCategory: count, ...}, ...}
        for listing_id in unique_listing_id:
            cursor.execute('SELECT "drinkType", "typeCategory" FROM "listings" WHERE "id" = %s', (listing_id,))
            drink_data = cursor.fetchone()
            if drink_data:
                drink_type = drink_data["drinkType"]
                drink_category = drink_data["typeCategory"]

                if drink_type not in categories_reviewed_dict:
                    categories_reviewed_dict[drink_type] = {}

                # Increment the count for the drink_category within the given drink_type.
                if drink_category in categories_reviewed_dict[drink_type]:
                    categories_reviewed_dict[drink_type][drink_category] += 1
                else:
                    categories_reviewed_dict[drink_type][drink_category] = 1

        # Step 3: Get the number of upvotes for the user's reviews (new schema)
        cursor.execute('''
            SELECT COUNT(*) FROM "reviewsUserVotes"
            WHERE EXISTS (
                SELECT 1 FROM jsonb_array_elements("upvotes") AS upvote
                WHERE (upvote->>'userId')::TEXT = %s
            )
        ''', (id,))
        upvotes_count = cursor.fetchone()['count']

    return jsonify({
        "code": 200,
        "message": "User review summary fetched successfully.",
        "data": {
            "categoriesReviewed": categories_reviewed_dict,
            "locationsTagged": locations_tagged,
            "upvotesCount": upvotes_count,
            "taggedUsers": tagged_users_count
        }
    })

# [GET] Reviews
@blueprint.route("/getReviews")
def getReviews():
    conn = g.db
    
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT "reviews".*, "reviewsUserVotes"."upvotes", "reviewsUserVotes"."downvotes"
            FROM "reviews"
            LEFT JOIN "reviewsUserVotes" ON "reviews"."id" = "reviewsUserVotes"."reviewId"
        """)

        reviews_data = cursor.fetchall()
    
    if not reviews_data:
        return jsonify([])

    for review in reviews_data:
        review["userVotes"] = {
            "upvotes": review["upvotes"] if review["upvotes"] else [],
            "downvotes": review["downvotes"] if review["downvotes"] else []
        }
        del review["upvotes"]
        del review["downvotes"]

    return jsonify(reviews_data)

# [POST] Reviews by listing IDs
@blueprint.route("/getReviewsByListingIDs", methods=['POST'])
def getReviewsByListingIDs():
    conn = g.db

    listing_ids = request.json.get('listingIDs', [])

    if not listing_ids:
        return jsonify([]), 404

    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT "reviews".*, "reviewsUserVotes"."upvotes", "reviewsUserVotes"."downvotes"
            FROM "reviews"
            LEFT JOIN "reviewsUserVotes" ON "reviews"."id" = "reviewsUserVotes"."reviewId"
            WHERE "reviews"."reviewTarget" IN %s
        """, (tuple(listing_ids),))
        reviews_data = cursor.fetchall()
    
    if not reviews_data:
        return jsonify([])

    return jsonify(reviews_data)

# [GET] Specific Reviews by reviewTarget
@blueprint.route("/getReviewByTarget/<id>")
def getReviewByTarget(id):
    conn = g.db
    
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT "reviews".*, "reviewsUserVotes"."upvotes", "reviewsUserVotes"."downvotes"
            FROM "reviews"
            LEFT JOIN "reviewsUserVotes" ON "reviews"."id" = "reviewsUserVotes"."reviewId"
            WHERE "reviews"."reviewTarget" = %s
        """, (id,))
        reviews_data = cursor.fetchall()
    
    if not reviews_data:
        return jsonify([])
    
    for review in reviews_data:
        review["userVotes"] = {
            "upvotes": review["upvotes"] if review["upvotes"] else [],
            "downvotes": review["downvotes"] if review["downvotes"] else []
        }
        del review["upvotes"]
        del review["downvotes"]

    return jsonify(reviews_data)


# [GET] Latest 10 Specific Reviews by usr(s) - using one or more user IDs (retrieve latest reviews for the specified user(s) as well as the review target(s) data)
# @blueprint.route("/getReviewsByUserIds")
# def getReviewsByUserIds():

#     user_ids_str = request.args.get('user_ids')
#     user_ids = user_ids_str.split(',')
#     conn = g.db
    
#     with conn.cursor() as cursor:
#         # Fetch latest reviews for the specified user(s)
        
#         cursor.execute('''
#             WITH latest_reviews AS (
#                 SELECT "reviewDesc", "rating", "reviewTarget", "createdDate", "userID"
#                 FROM "reviews"
#                 WHERE "userID" IN %s
#                 ORDER BY "createdDate" DESC
#                 LIMIT 10
#             )
#             SELECT "reviewDesc", "rating", "reviewTarget", "createdDate", "userID"
#             FROM latest_reviews
#             ORDER BY "createdDate" DESC;
#         ''', (tuple(user_ids),))
#         latest_reviews = cursor.fetchall()

#         # Retrieve the display name(s) for each user
#         cursor.execute('SELECT "id", "displayName", "photo" FROM "users" WHERE "id" IN %s', (tuple(user_ids),))
#         user_display_names = cursor.fetchall()

#         # Convert the user display names to dictionary format where the key is the user ID
#         user_display_names = {user['id']: user for user in user_display_names}

#         # Retrieve the review target(s) for each review
#         review_target_list = []
#         for review in latest_reviews:
#             review = dict(review)
#             if (review['reviewTarget'] not in review_target_list):
#                 review_target_list.append(review['reviewTarget'])
        
#         # Fetch the review target(s) data
#         cursor.execute('SELECT "id", "listingName", "photo" FROM "listings" WHERE "id" IN %s', (tuple(review_target_list),))
#         review_targets_data = cursor.fetchall()

#         # Map the review target data to the reviews
#         for review in latest_reviews:
#             review['userInfo'] = user_display_names[review['userID']]
#             review['reviewTarget'] = next((item for item in review_targets_data if item["id"] == review['reviewTarget']), None)
        
#         # Convert the reviews to JSON format
#         latest_reviews = parse_json(latest_reviews)
    
#     if not latest_reviews:
#         return jsonify({
#             'code': 404,
#             'message': 'No reviews found for the specified user(s).'
#         })

#     return jsonify({
#         'code': 200,
#         'message': 'Latest reviews fetched successfully.',
#         'data': latest_reviews
#     })

# Updated blueprint route
@blueprint.route("/getReviewsByUserIds")
def getReviewsByUserIds():
    user_ids_str = request.args.get('user_ids')
    if not user_ids_str:
        return jsonify({
            'code': 400,
            'message': 'Missing user_ids query parameter.'
        })

    user_ids = user_ids_str.split(',')
    user_ids = [int(uid) for uid in user_ids]  # Ensure integers
    conn = g.db

    with conn.cursor() as cursor:
        # Build dynamic placeholders for user_ids
        placeholders = ','.join(['%s'] * len(user_ids))

        # --- Fetch latest reviews ---
        cursor.execute(f'''
            WITH latest_reviews AS (
                SELECT "reviewDesc", "rating", "reviewTarget", "createdDate", "userID"
                FROM "reviews"
                WHERE "userID" IN ({placeholders})
                ORDER BY "createdDate" DESC
                LIMIT 10
            )
            SELECT "reviewDesc", "rating", "reviewTarget", "createdDate", "userID"
            FROM latest_reviews
            ORDER BY "createdDate" DESC;
        ''', tuple(user_ids))
        latest_reviews = cursor.fetchall()

        if not latest_reviews:
            return jsonify({
                'code': 404,
                'message': 'No reviews found for the specified user(s).'
            })

        # Convert to dicts early
        latest_reviews = [dict(r) for r in latest_reviews]

        # --- Fetch user display info ---
        cursor.execute(f'''
            SELECT "id", "displayName", "photo"
            FROM "users"
            WHERE "id" IN ({placeholders})
        ''', tuple(user_ids))
        user_display_names = {u['id']: dict(u) for u in cursor.fetchall()}

        # --- Prepare listing IDs from reviewTarget ---
        review_target_ids = list(set([r['reviewTarget'] for r in latest_reviews]))
        if review_target_ids:
            target_placeholders = ','.join(['%s'] * len(review_target_ids))
            cursor.execute(f'''
                SELECT "id", "listingName", "photo"
                FROM "listings"
                WHERE "id" IN ({target_placeholders})
            ''', tuple(review_target_ids))
            review_targets_data = {l['id']: dict(l) for l in cursor.fetchall()}
        else:
            review_targets_data = {}

        # --- Enrich reviews with user and listing info ---
        for r in latest_reviews:
            r['userInfo'] = user_display_names.get(r['userID'], {})
            r['reviewTarget'] = review_targets_data.get(r['reviewTarget'], {})
            for k, v in r.items():
                if isinstance(v, Decimal):
                    r[k] = float(v)

        return jsonify({
            'code': 200,
            'message': 'Latest reviews fetched successfully.',
            'data': parse_json(latest_reviews)
        })

# [GET] Producer Tour Reviews
@blueprint.route("/getProducerTourReviews")
def getTourReviews():
    conn = g.db

    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT "producerReviews".*, "producerReviewsUserVotes"."upvotes", "producerReviewsUserVotes"."downvotes"
            FROM "producerReviews"
            LEFT JOIN "producerReviewsUserVotes" ON "producerReviews"."id" = "producerReviewsUserVotes"."reviewId"
        """)

        reviews_data = cursor.fetchall()

        if not reviews_data:
            return jsonify([])
        
        for review in reviews_data:
            review["userVotes"] = {
                "upvotes": review["upvotes"] if review["upvotes"] else [],
                "downvotes": review["downvotes"] if review["downvotes"] else []
            }
            del review["upvotes"]
            del review["downvotes"]

        return jsonify(reviews_data)

# [GET] Venue Reviews
@blueprint.route("/getVenueReviews")
def getVenueReviews():
    conn = g.db

    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT "venueReviews".*, "venueReviewsUserVotes"."upvotes", "venueReviewsUserVotes"."downvotes"
            FROM "venueReviews"
            LEFT JOIN "venueReviewsUserVotes" ON "venueReviews"."id" = "venueReviewsUserVotes"."reviewId"
        """)

        reviews_data = cursor.fetchall()

        if not reviews_data:
            return jsonify([])
        
        for review in reviews_data:
            review["userVotes"] = {
                "upvotes": review["upvotes"] if review["upvotes"] else [],
                "downvotes": review["downvotes"] if review["downvotes"] else []
            }
            del review["upvotes"]
            del review["downvotes"]

        return jsonify(reviews_data)


# [GET] Venue Reviews by venue ID
@blueprint.route("/getVenueReviewsByVenueId/<id>", methods=['GET'])
def getVenueReviewsByVenueId(id):
    conn = g.db

    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT "venueReviews".*, "venueReviewsUserVotes"."upvotes", "venueReviewsUserVotes"."downvotes"
            FROM "venueReviews"
            LEFT JOIN "venueReviewsUserVotes" ON "venueReviews"."id" = "venueReviewsUserVotes"."reviewId"
            WHERE "venueReviews"."venueID" = %s
        """, (id,))

        reviews_data = cursor.fetchall()

        if not reviews_data:
            return jsonify([])
        
        for review in reviews_data:
            review["userVotes"] = {
                "upvotes": review["upvotes"] if review["upvotes"] else [],
                "downvotes": review["downvotes"] if review["downvotes"] else []
            }
            del review["upvotes"]
            del review["downvotes"]

        return jsonify(reviews_data)


# [GET] Producer Reviews by producer ID
@blueprint.route("/getProducerReviewsByProducerId/<id>", methods=['GET'])
def getProducerReviewsByProducerId(id):
    conn = g.db

    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT "producerReviews".*, "producerReviewsUserVotes"."upvotes", "producerReviewsUserVotes"."downvotes"
            FROM "producerReviews"
            LEFT JOIN "producerReviewsUserVotes" ON "producerReviews"."id" = "producerReviewsUserVotes"."reviewId"
            WHERE "producerReviews"."producerID" = %s
        """, (id,))

        reviews_data = cursor.fetchall()

        if not reviews_data:
            return jsonify([])
        
        for review in reviews_data:
            review["userVotes"] = {
                "upvotes": review["upvotes"] if review["upvotes"] else [],
                "downvotes": review["downvotes"] if review["downvotes"] else []
            }
            del review["upvotes"]
            del review["downvotes"]

        return jsonify(reviews_data)


# ----------------------
# [NEW] TO BE ADDED:
# ----------------------

# # [GET] Reviews
# @blueprint.route("/getReviews")
# def getReviews():
#     db = g.db
#     reviews_data = db.reviews.find({})
#     allReviews = []
#     for review in reviews_data:
#         # Fetch related user votes based on the id(s) in review's userVotes
#         user_votes_data = db.reviewsUserVotes.find({
#             "_id": {"$in": review['userVotes']}
#         })
#         review['userVotes'] = list(user_votes_data)
#         allReviews.append(review)
#     return parse_json(allReviews)

# # [GET] Specific Reviews by reviewTarget
# @blueprint.route("/getReviewByTarget/<id>")
# def getReviewByTarget(id):
#     db = g.db
#     reviews_data = db.reviews.find({"reviewTarget": ObjectId(id)})
#     if reviews_data is None:
#         return []
#     allReviews = []
#     for review in reviews_data:
#         # Fetch related user votes based on the id(s) in review's userVotes
#         user_votes_data = db.reviewsUserVotes.find({
#             "_id": {"$in": review['userVotes']}
#         })
#         review['userVotes'] = list(user_votes_data)
#         allReviews.append(review)
#     return parse_json(allReviews)

# =======================================================

# -----------------------------------------------------------------------------------------

# ================== POSTGRESQL FORMAT ==================

# ----------------------
# [OLD] TO BE DELETED:
# ----------------------

# [GET] Users
@blueprint.route("/getUsers")
def getUsers():
    conn = g.db
    
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM "users"')
            users_data = cursor.fetchall()

            for user_data in users_data:
                user_id = user_data['id']
                
                user_data["drinkLists"] = fetch_drink_lists(cursor, user_id)
                user_data["followLists"] = fetch_follow_lists(cursor, user_id)


                # Remove unnecessary fields
                del user_data["hashedPassword"]
                del user_data["pin"]

        return jsonify(users_data), 200

    except Exception as e:
        print(str(e))
        return jsonify({"code": 500, "message": "An error occurred while fetching users."}), 500


# [POST] A list of users
@blueprint.route("/getUsersFromList", methods=['POST'])
def getUsersFromList():
    conn = g.db
    user_ids = request.json.get('userIDs', [])

    if not user_ids or len(user_ids) == 0:
        return jsonify({
            "code": 404,
            "message": "At least one user ID is required."
        }), 404

    # Retrieve user information based on the provided IDs
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM "users" WHERE "id" IN %s', (tuple(user_ids),))
        users_data = cursor.fetchall()

        if not users_data:
            return jsonify([]), 404

        for user_data in users_data:
            user_id = user_data['id']
            
            user_data["drinkLists"] = fetch_drink_lists(cursor, user_id)
            user_data["followLists"] = fetch_follow_lists(cursor, user_id)
            user_data['proofRank'] = pointsHelperFunc.get_rank_by_user_id(user_id)
            user_data['currentPoints'] = pointsHelperFunc.get_current_proof_points(user_id)

            # Remove unnecessary fields
            del user_data["hashedPassword"]
            del user_data["pin"]


    return jsonify(users_data), 200


# [POST] A list of users a specific user is following
@blueprint.route("/getUserFollowListDetails", methods=['POST'])
def getUserFollowListDetails():
    conn = g.db
    user_ids = request.json.get('userIDs', [])

    if not user_ids or len(user_ids) == 0:
        return jsonify({
            "code": 404,
            "message": "At least one user ID is required."
        }), 404
    
    try: 
        # Retrieve user information based on the provided IDs
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM "users" WHERE "id" IN %s', (tuple(user_ids),))
            users_data = cursor.fetchall()

            if not users_data:
                return jsonify([]), 404

            for user_data in users_data:
                user_id = user_data['id']
                user_data['proofRank'] = pointsHelperFunc.get_rank_by_user_id(user_id)
                user_data['currentPoints'] = pointsHelperFunc.get_current_proof_points(user_id)

                # Remove unnecessary fields
                del user_data["hashedPassword"]
                del user_data["pin"]
                del user_data["email"]

        return jsonify(users_data), 200
    
    except Exception as e:
        print(str(e))
        return jsonify({"code": 500, "message": "An error occurred while fetching user follow list details."}), 500

# [GET] Specific User by ID
@blueprint.route("/getUser/<id>")
def getUser(id):
    conn = g.db
    
    try:
        with conn.cursor() as cursor:
            user_data = fetch_user_data(cursor, id)
            if not user_data:
                return jsonify({}), 404

            user_data["drinkLists"] = fetch_drink_lists(cursor, id)
            user_data["followLists"] = fetch_follow_lists(cursor, id)
            user_data['proofRank'] = pointsHelperFunc.get_rank_by_user_id(id)
            user_data['currentPoints'] = pointsHelperFunc.get_current_proof_points(id)

            # Remove unnecessary fields
            del user_data["hashedPassword"]
            del user_data["birthday"]
            del user_data["email"]
            del user_data["pin"]

            # Make sure these fields exist (even if empty)
            if 'grails' not in user_data:
                user_data['grails'] = []
            if 'upAndComing' not in user_data:
                user_data['upAndComing'] = []
            if 'goats' not in user_data:
                user_data['goats'] = []

        return jsonify(user_data), 200

    except Exception as e:
        print(str(e))
        return jsonify({"code": 500, "message": "An error occurred while fetching the user."}), 500


# [GET] Get user profile photo by ID
@blueprint.route("/getUserPhoto/<id>/<userType>")
def getUserPhoto(id, userType):

    conn = g.db
    try:
        with conn.cursor() as cursor:
            if userType == "producer":
                cursor.execute('SELECT "photo" FROM "producers" WHERE "id" = %s', (id,))
            elif userType == "venue":
                cursor.execute('SELECT "photo" FROM "venues" WHERE "id" = %s', (id,))
            else:
                cursor.execute('SELECT "photo" FROM "users" WHERE "id" = %s', (id,))
            photo = cursor.fetchone()
        
        if not photo:
            return jsonify([]), 404
        
        # Standardize the photo field
        if photo["photo"] == None:
            photo["photo"] = ""

        return jsonify(photo), 200

    except Exception as e:
        print(str(e))
        return jsonify({"code": 500, "message": "An error occurred while fetching the user photo."}), 500


# [GET] Specific User by Username
@blueprint.route("/getUserByUsername/<username>")
def getUserByUsername(username):
    conn = g.db
    
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM "users" WHERE "username" = %s', (username,))
            user_data = cursor.fetchone()
        
            if not user_data:
                return jsonify([]), 404

            user_id = user_data['id']

            # Remove unnecessary fields
            del user_data["hashedPassword"]
            del user_data["pin"]

            user_data["drinkLists"] = fetch_drink_lists(cursor, user_id)
            user_data["followLists"] = fetch_follow_lists(cursor, user_id)

        return jsonify(user_data), 200

    except Exception as e:
        print(str(e))
        return jsonify({"code": 500, "message": "An error occurred while fetching the user."}), 500

# ----------------------
# [NEW] TO BE ADDED:
# ----------------------

# # [GET] Users
# @blueprint.route("/getUsers")
# def getUsers():
#     db = g.db
#     users_data = db.users.find({})
#     allUsers = []
#     for user in users_data:
#         # Fetch related drink lists based on the id(s) in user's drinkLists
#         drink_lists_data = db.usersDrinkLists.find({
#             "_id": {"$in": user['drinkLists']}
#         })
#         user['drinkLists'] = list(drink_lists_data)
#         # Fetch related follow lists based on the id(s) in user's followLists
#         follow_lists_data = db.usersFollowLists.find({
#             "_id": {"$in": user['followLists']}
#         })
#         user['followLists'] = list(follow_lists_data)
#         allUsers.append(user)
#     return parse_json(allUsers)

# # [GET] Specific User by ID
# @blueprint.route("/getUser/<id>")
# def getUser(id):
#     db = g.db
#     user = db.users.find_one({"_id": ObjectId(id)})
#     if user is None:
#         return []
#     # Fetch related drink lists based on the id(s) in user's drinkLists
#     drink_lists_data = db.usersDrinkLists.find({
#         "_id": {"$in": user['drinkLists']}
#     })
#     user['drinkLists'] = list(drink_lists_data)
#     # Fetch related follow lists based on the id(s) in user's followLists
#     follow_lists_data = db.usersFollowLists.find({
#         "_id": {"$in": user['followLists']}
#     })
#     user['followLists'] = list(follow_lists_data)
#     return parse_json(user)

# # [GET] Specific User by Username
# @blueprint.route("/getUserByUsername/<username>")
# def getUserByUsername(username):
#     db = g.db
#     user = db.users.find_one({"username": username})
#     if user is None:
#         return []
#     # Fetch related drink lists based on the id(s) in user's drinkLists
#     drink_lists_data = db.usersDrinkLists.find({
#         "_id": {"$in": user['drinkLists']}
#     })
#     user['drinkLists'] = list(drink_lists_data)
#     # Fetch related follow lists based on the id(s) in user's followLists
#     follow_lists_data = db.usersFollowLists.find({
#         "_id": {"$in": user['followLists']}
#     })
#     user['followLists'] = list(follow_lists_data)
#     return parse_json(user)

# =======================================================

# -----------------------------------------------------------------------------------------

# ================== POSTGRESQL FORMAT ==================

# ----------------------
# [OLD] TO BE DELETED:
# ----------------------

# [GET] Venues
@blueprint.route("/getVenues")
def getVenues():
    conn = g.db
    cur = conn.cursor()

    try:
        # Query to get venues and related data
        query = """
            SELECT 
                v.id, v.address, v."claimStatus", v."hashedPassword", v."venueName", v."venueDesc", 
                v."originLocation", v.photo, v."publicHolidays", v."reservationDetails", v."claimStatusCheckDate",
                v."yearOpened", v."openForReservations", v.website,
                v.username, v."venueType", v."stripeCustomerId", v.pin,
                -- Build the menu JSON
                COALESCE((
                    SELECT json_agg(json_build_object(
                        'sectionOrder',vm."sectionOrder",
                        'sectionName', vm."sectionName",
                        'sectionId', vm.id,
                        'sectionMenu', COALESCE((
                            SELECT json_agg(json_build_object(
                                'itemOrder', mi."itemOrder",
                                'itemPrice', mi."itemPrice",
                                'itemAvailability', mi."itemAvailability",
                                'itemID', mi."itemID",
                                'itemServingType', mi."itemServingType"
                            ) ORDER BY mi."itemOrder")
                            FROM "menuItems" mi
                            WHERE mi."sectionId" = vm.id
                        ), '[]')
                    ) ORDER BY vm."sectionOrder")
                    FROM "venuesMenu" vm
                    WHERE vm."venueId" = v.id
                ), '[]') AS menu,
                -- Build openingHours JSON
                COALESCE((
                    SELECT row_to_json(oh)
                    FROM "venuesOpeningHours" oh
                    WHERE oh."venueId" = v.id
                ), '{}'::json) AS "openingHours",
                -- Build questionsAnswers JSON
                COALESCE((
                    SELECT json_agg(json_build_object(
                        'id', qa.id,
                        'question', qa.question,
                        'answer', qa.answer,
                        'date', qa.date,
                        'userId', qa."userId"
                    ))
                    FROM "venuesQuestionAnswers" qa
                    WHERE qa."venueId" = v.id
                ), '[]') AS "questionsAnswers",
                -- Build updates JSON
                COALESCE((
                    SELECT json_agg(json_build_object(
                        'id', u.id,
                        'date', u.date,
                        'text', u.text,
                        'photo', u.photo,
                        'venueId', u."venueId",
                        'likes', COALESCE((
                            SELECT json_agg(json_build_object('userId', l."userId", 'userType', l."userType"))
                            FROM "venueUpdateLikes" l
                            WHERE l."updateId" = u.id
                        ), '[]')
                    ) ORDER BY u.date DESC)
                    FROM "venuesUpdates" u
                    WHERE u."venueId" = v.id
                ), '[]') AS updates
            FROM venues v
            ORDER BY v.id
        """

        cur.execute(query)
        venues_data = cur.fetchall()

        if not venues_data:
            return jsonify([])

        venues_list = []
        for row in venues_data:
            venue = dict(row)
            venue['menu'] = venue['menu'] if venue['menu'] else []
            venue['openingHours'] = venue['openingHours'] if venue['openingHours'] else {}
            venue['questionsAnswers'] = venue['questionsAnswers'] if venue['questionsAnswers'] else []
            venue['updates'] = venue['updates'] if venue['updates'] else []
            venues_list.append(venue)

        return jsonify(venues_list), 200

    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred retrieving venues."
            }
        ), 500

    finally:
        cur.close()

# [GET] Specific Venue
@blueprint.route("/getVenue/<id>")
def getVenue(id):
    conn = g.db
    cur = conn.cursor()

    try:
        # Query to get a specific venue and related data
        query = """
            SELECT 
                v.id, v.address, v."claimStatus", v."hashedPassword", v."venueName", v."venueDesc", 
                v."originLocation", v.photo, v."publicHolidays", v."reservationDetails", v."claimStatusCheckDate",
                v."yearOpened", v."openForReservations", v.website,
                v.username, v."venueType", v."stripeCustomerId", v.pin,
                -- Build the menu JSON
                COALESCE((
                    SELECT json_agg(json_build_object(
                        'sectionOrder', vm."sectionOrder",
                        'sectionName', vm."sectionName",
                        'sectionId', vm.id,
                        'sectionMenu', COALESCE((
                            SELECT json_agg(json_build_object(
                                'itemOrder', mi."itemOrder",
                                'itemPrice', mi."itemPrice",
                                'itemAvailability', mi."itemAvailability",
                                'itemID', mi."itemID",
                                'itemServingType', mi."itemServingType"
                            ) ORDER BY mi."itemOrder")
                            FROM "menuItems" mi
                            WHERE mi."sectionId" = vm.id
                        ), '[]')
                    ) ORDER BY vm."sectionOrder")
                    FROM "venuesMenu" vm
                    WHERE vm."venueId" = v.id
                ), '[]') AS menu,
                -- Build openingHours JSON
                COALESCE((
                    SELECT row_to_json(oh)
                    FROM "venuesOpeningHours" oh
                    WHERE oh."venueId" = v.id
                ), '{}'::json) AS "openingHours",
                -- Build questionsAnswers JSON
                COALESCE((
                    SELECT json_agg(json_build_object(
                        'id', qa.id,
                        'question', qa.question,
                        'answer', qa.answer,
                        'date', qa.date,
                        'userId', qa."userId"
                    ))
                    FROM "venuesQuestionAnswers" qa
                    WHERE qa."venueId" = v.id
                ), '[]') AS "questionsAnswers",
                -- Build updates JSON
                COALESCE((
                    SELECT json_agg(json_build_object(
                        'id', u.id,
                        'date', u.date,
                        'text', u.text,
                        'photo', u.photo,
                        'venueId', u."venueId",
                        'likes', COALESCE((
                            SELECT json_agg(json_build_object('userId', l."userId", 'userType', l."userType"))
                            FROM "venueUpdateLikes" l
                            WHERE l."updateId" = u.id
                        ), '[]')
                    ) ORDER BY u.date DESC)
                    FROM "venuesUpdates" u
                    WHERE u."venueId" = v.id
                ), '[]') AS updates
            FROM venues v
            WHERE v.id = %s
            GROUP BY v.id
        """

        cur.execute(query, (id,))
        venue_data = cur.fetchone()

        if venue_data is None:
            return jsonify({"message": "Venue not found"}), 404

        venue = dict(venue_data)
        venue['menu'] = venue['menu'] if venue['menu'] else []
        venue['openingHours'] = venue['openingHours'] if venue['openingHours'] else {}
        venue['questionsAnswers'] = venue['questionsAnswers'] if venue['questionsAnswers'] else []
        venue['updates'] = venue['updates'] if venue['updates'] else []

        return jsonify(venue), 200

    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred retrieving the venue."
            }
        ), 500

    finally:
        cur.close()

# [GET] Specific Producer
@blueprint.route("/getVenueByRequestId/<id>")
def getVenueByRequestId(id):
    conn = g.db
    cur = conn.cursor()

    try:
        # Query to get a specific venue by requestId and related data
        query = """
            SELECT 
                v.id, v.address, v."claimStatus", v."hashedPassword", v."venueName", v."venueDesc", 
                v."originLocation", v.photo, v."publicHolidays", v."reservationDetails", v."claimStatusCheckDate",
                v."yearOpened", v."openForReservations", v.website,
                v.username, v."venueType", v."stripeCustomerId", v.pin,
                -- Build the menu JSON
                COALESCE((
                    SELECT json_agg(json_build_object(
                        'sectionOrder', vm."sectionOrder",
                        'sectionName', vm."sectionName",
                        'sectionId', vm.id,
                        'sectionMenu', COALESCE((
                            SELECT json_agg(json_build_object(
                                'itemOrder', mi."itemOrder",
                                'itemPrice', mi."itemPrice",
                                'itemAvailability', mi."itemAvailability",
                                'itemID', mi."itemID",
                                'itemServingType', mi."itemServingType"
                            ) ORDER BY mi."itemOrder")
                            FROM "menuItems" mi
                            WHERE mi."sectionId" = vm.id
                        ), '[]')
                    ) ORDER BY vm."sectionOrder")
                    FROM "venuesMenu" vm
                    WHERE vm."venueId" = v.id
                ), '[]') AS menu,
                -- Build openingHours JSON
                COALESCE((
                    SELECT row_to_json(oh)
                    FROM "venuesOpeningHours" oh
                    WHERE oh."venueId" = v.id
                ), '{}'::json) AS "openingHours",
                -- Build questionsAnswers JSON
                COALESCE((
                    SELECT json_agg(json_build_object(
                        'id', qa.id,
                        'question', qa.question,
                        'answer', qa.answer,
                        'date', qa.date,
                        'userId', qa."userId"
                    ))
                    FROM "venuesQuestionAnswers" qa
                    WHERE qa."venueId" = v.id
                ), '[]') AS "questionsAnswers",
                -- Build updates JSON
                COALESCE((
                    SELECT json_agg(json_build_object(
                        'id', u.id,
                        'date', u.date,
                        'text', u.text,
                        'photo', u.photo,
                        'venueId', u."venueId",
                        'likes', COALESCE((
                            SELECT json_agg(json_build_object('userId', l."userId", 'userType', l."userType"))
                            FROM "venueUpdateLikes" l
                            WHERE l."updateId" = u.id
                        ), '[]')
                    ) ORDER BY u.date DESC)
                    FROM "venuesUpdates" u
                    WHERE u."venueId" = v.id
                ), '[]') AS updates
            FROM venues v
            WHERE v.id = %s
            GROUP BY v.id
        """

        cur.execute(query, (id,))
        venue_data = cur.fetchone()

        if venue_data is None:
            return jsonify({"message": "Venue not found"}), 404

        venue = dict(venue_data)
        venue['menu'] = venue['menu'] if venue['menu'] else []
        venue['openingHours'] = venue['openingHours'] if venue['openingHours'] else {}
        venue['questionsAnswers'] = venue['questionsAnswers'] if venue['questionsAnswers'] else []
        venue['updates'] = venue['updates'] if venue['updates'] else []

        return jsonify(venue), 200
    
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred retrieving the venue."
            }
        ), 500
    
    finally:
        cur.close()

# ----------------------
# [NEW] TO BE ADDED:
# ----------------------

# # [GET] Venues
# @blueprint.route("/getVenues")
# def getVenues():
#     db = g.db
#     venues_data = db.venues.find({})
#     allVenues = []
#     for venue in venues_data:
#         # Fetch related menu based on the id(s) in venue's menu
#         menu_data = db.venuesMenu.find({
#             "_id": {"$in": venue['menu']}
#         })
#         venue['menu'] = list(menu_data)
#         # Fetch related opening hours based on the id(s) in venue's openingHours
#         opening_hours_data = db.venuesOpeningHours.find({
#             "_id": {"$in": venue['openingHours']}
#         })
#         venue['openingHours'] = list(opening_hours_data)
#         # Fetch related question answers based on the id(s) in venue's questionAnswers
#         question_answers_data = db.venuesQuestionAnswers.find({
#             "_id": {"$in": venue['questionAnswers']}
#         })
#         venue['questionAnswers'] = list(question_answers_data)
#         # Fetch related updates based on the id(s) in venue's updates
#         updates_data = db.venuesUpdates.find({
#             "_id": {"$in": venue['updates']}
#         })
#         venue['updates'] = list(updates_data)
#         allVenues.append(venue)
#     return parse_json(allVenues)

# # [GET] Specific Venue by ID
# @blueprint.route("/getVenue/<id>")
# def getVenue(id):
#     db = g.db
#     venue = db.venues.find_one({"_id": ObjectId(id)})
#     if venue is None:
#         return []
#     # Fetch related menu based on the id(s) in venue's menu
#     menu_data = db.venuesMenu.find({
#         "_id": {"$in": venue['menu']}
#     })
#     venue['menu'] = list(menu_data)
#     # Fetch related opening hours based on the id(s) in venue's openingHours
#     opening_hours_data = db.venuesOpeningHours.find({
#         "_id": {"$in": venue['openingHours']}
#     })
#     venue['openingHours'] = list(opening_hours_data)
#     # Fetch related question answers based on the id(s) in venue's questionAnswers
#     question_answers_data = db.venuesQuestionAnswers.find({
#         "_id": {"$in": venue['questionAnswers']}
#     })
#     venue['questionAnswers'] = list(question_answers_data)
#     # Fetch related updates based on the id(s) in venue's updates
#     updates_data = db.venuesUpdates.find({
#         "_id": {"$in": venue['updates']}
#     })
#     venue['updates'] = list(updates_data)
#     return parse_json(venue)

# # [GET] Specific Venue by Request ID
# @blueprint.route("/getVenueByRequestId/<id>")
# def getVenueByRequestId(id):
#     db = g.db
#     venue = db.venues.find_one({"requestId": ObjectId(id)})
#     if venue is None:
#         return []
#     # Fetch related menu based on the id(s) in venue's menu
#     menu_data = db.venuesMenu.find({
#         "_id": {"$in": venue['menu']}
#     })
#     venue['menu'] = list(menu_data)
#     # Fetch related opening hours based on the id(s) in venue's openingHours
#     opening_hours_data = db.venuesOpeningHours.find({
#         "_id": {"$in": venue['openingHours']}
#     })
#     venue['openingHours'] = list(opening_hours_data)
#     # Fetch related question answers based on the id(s) in venue's questionAnswers
#     question_answers_data = db.venuesQuestionAnswers.find({
#         "_id": {"$in": venue['questionAnswers']}
#     })
#     venue['questionAnswers'] = list(question_answers_data)
#     # Fetch related updates based on the id(s) in venue's updates
#     updates_data = db.venuesUpdates.find({
#         "_id": {"$in": venue['updates']}
#     })
#     venue['updates'] = list(updates_data)
#     return parse_json(venue)

# =======================================================

# -----------------------------------------------------------------------------------------
# [GET] VenuesAPI
# @blueprint.route("/getVenuesAPI")
# def getVenuesAPI():
#     db = g.db
#     data = db.venuesAPI.find({})
#     print(len(list(data.clone())))
#     allVenuesAPI = []
#     dataEncode = parse_json(data)
#     for doc in dataEncode:
#         allVenuesAPI.append(doc)
#     return allVenuesAPI

# -----------------------------------------------------------------------------------------
# [GET] DrinkTypes
@blueprint.route("/getDrinkTypes")
def getDrinkTypes():
    conn = g.db
    
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM "drinkTypes"')
        drink_types_data = cursor.fetchall()
    
    if not drink_types_data:
        return jsonify([])

    return jsonify(drink_types_data)

# -----------------------------------------------------------------------------------------
# [GET] DrinkCategories
@blueprint.route("/getTypeCategories")
def getTypeCategories():
    conn = g.db
    
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM "typeCategories"')
        type_categories_data = cursor.fetchall()
    
    if not type_categories_data:
        return jsonify([])

    return jsonify(type_categories_data)

# -----------------------------------------------------------------------------------------
# [GET] RequestListings
@blueprint.route("/getRequestListings")
def getRequestListings():
    conn = g.db
    
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM "requestListings"')
        request_listings_data = cursor.fetchall()
    
    if not request_listings_data:
        return jsonify([])

    return jsonify(request_listings_data)

# [GET] Specific Request Listing
@blueprint.route("/getRequestListing/<id>")
def getRequestListing(id):
    conn = g.db
    
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM "requestListings" WHERE "id" = %s', (id,))
        request_listing_data = cursor.fetchone()
    
    if request_listing_data is None:
        return jsonify([])

    return jsonify(request_listing_data)

# -----------------------------------------------------------------------------------------
# [GET] RequestEdits
@blueprint.route("/getRequestEdits")
def getRequestEdits():
    conn = g.db
    
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM "requestEdits"')
        request_edits_data = cursor.fetchall()
    
    if not request_edits_data:
        return jsonify([])

    return jsonify(request_edits_data)

# [GET] Specific Request Edit
@blueprint.route("/getRequestEdit/<id>")
def getRequestEdit(id):
    conn = g.db
    
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM "requestEdits" WHERE "id" = %s', (id,))
        request_edit_data = cursor.fetchone()
    
    if request_edit_data is None:
        return jsonify([])

    return jsonify(request_edit_data)

# -----------------------------------------------------------------------------------------
# [GET] modRequests
@blueprint.route("/getModRequests")
def getModRequests():
    conn = g.db

    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM "modRequests"')
        mod_requests_data = cursor.fetchall()

    if not mod_requests_data:
        return jsonify([])

    return jsonify(mod_requests_data)

# -----------------------------------------------------------------------------------------
# [GET] flavourTags
@blueprint.route("/getFlavourTags")
def getFlavourTags():
    conn = g.db

    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM "flavourTags"')
        flavour_tags_data = cursor.fetchall()

    if not flavour_tags_data:
        return jsonify([])

    return jsonify(flavour_tags_data)
# -----------------------------------------------------------------------------------------
# [GET] subTags
@blueprint.route("/getSubTags")
def getSubTags():
    conn = g.db

    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM "subTags"')
        allSubTags = cursor.fetchall()

    if not allSubTags:
        return jsonify([])

    return jsonify(allSubTags)

# -----------------------------------------------------------------------------------------
# [GET] observationTags
@blueprint.route("/getObservationTags")
def getObservationTags():
    conn = g.db

    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM "observationTags"')
        observation_tags_data = cursor.fetchall()

    if not observation_tags_data:
        return jsonify([])

    return jsonify(observation_tags_data)

# -----------------------------------------------------------------------------------------
# [GET] colours
@blueprint.route("/getColours")
def getColours():
    conn = g.db

    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM "colours"')
        colours_data = cursor.fetchall()

    if not colours_data:
        return jsonify([])

    return jsonify(colours_data)

# -----------------------------------------------------------------------------------------
# [GET] specialColours
@blueprint.route("/getSpecialColours")
def getSpecialColours():
    conn = g.db

    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM "specialColours"')
        allSpecialColours = cursor.fetchall()

    if not allSpecialColours:
        return jsonify([])

    return jsonify(allSpecialColours)

# -----------------------------------------------------------------------------------------
# [GET] languages
@blueprint.route("/getLanguages")
def getLanguages():
    conn = g.db

    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM "languages"')
        languages = cursor.fetchall()

    if not languages:
        return jsonify([])

    return jsonify(languages)

# -----------------------------------------------------------------------------------------
# [GET] servingTypes
@blueprint.route("/getServingTypes")
def getServingTypes():
    conn = g.db

    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM "servingTypes"')
        serving_types_data = cursor.fetchall()

    if not serving_types_data:
        return jsonify([])
    
    return jsonify(serving_types_data), 200

# -----------------------------------------------------------------------------------------

# ================== POSTGRESQL FORMAT ==================

# ----------------------
# [OLD] TO BE DELETED:
# ----------------------

# [GET] producersProfileViews
@blueprint.route("/getProducersProfileViews")
def getProducersProfileViews():
    conn = g.db
    cur = conn.cursor()

    try:
        cur.execute('SELECT * FROM "producersProfileViews"')
        producers_profile_views_data = cur.fetchall()

        if not producers_profile_views_data:
            return jsonify([])

        return jsonify(producers_profile_views_data), 200
    
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred retrieving the profile views."
            }
        ), 500
    
    finally:
        cur.close()

# [GET] producersProfileViews by producerID
@blueprint.route("/getProducersProfileViewsByProducer/<id>")
def getProducersProfileViewsByProducer():
    conn = g.db
    cur = conn.cursor()

    try:
        cur.execute('SELECT * FROM "producersProfileViews" WHERE "producerID" = %s', (id,))
        producers_profile_views_data = cur.fetchall()

        if not producers_profile_views_data:
            return jsonify([]), 404

        return jsonify(producers_profile_views_data), 200
    
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred retrieving the profile views."
            }
        ), 500
    
    finally:
        cur.close()

# ----------------------
# [NEW] TO BE ADDED:
# ----------------------

# # [GET] producersProfileViews
# @blueprint.route("/getProducersProfileViews")
# def getProducersProfileViews():
#     db = g.db
#     profile_views_data = db.producersProfileViews.find({})
#     allProfileViews = []
#     for profile_view in profile_views_data:
#         # Fetch related views data based on the id(s) in profile_view's views
#         views_data = db.producersProfileViewsViews.find({
#             "_id": {"$in": profile_view['views']}
#         })
#         profile_view['views'] = list(views_data)
#         allProfileViews.append(profile_view)
#     return parse_json(allProfileViews)

# # [GET] producersProfileViews by producerID
# @blueprint.route("/getProducersProfileViewsByProducer/<id>")
# def getProducersProfileViewsByProducer(id):
#     db = g.db
#     profile_views_data = db.producersProfileViews.find({"producerID": ObjectId(id)})
#     allProfileViews = []
#     for profile_view in profile_views_data:
#         # Fetch related views data based on the id(s) in profile_view's views
#         views_data = db.producersProfileViewsViews.find({
#             "_id": {"$in": profile_view['views']}
#         })
#         profile_view['views'] = list(views_data)
#         allProfileViews.append(profile_view)
    # return parse_json(allProfileViews)

# =======================================================

# -----------------------------------------------------------------------------------------

# ================== POSTGRESQL FORMAT ==================

# ----------------------
# [OLD] TO BE DELETED:
# ----------------------

# [GET] venuesProfileViews
@blueprint.route("/getVenuesProfileViews")
def getVenuesProfileViews():
    conn = g.db
    cur = conn.cursor()

    try:
        cur.execute('SELECT * FROM "venuesProfileViews"')
        profile_views_data = cur.fetchall()

        if not profile_views_data:
            return jsonify([])

        return jsonify(profile_views_data), 200
    
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred retrieving the profile views."
            }
        ), 500
    
    finally:
        cur.close()

# [GET] venuesProfileViews by venueID
@blueprint.route("/getVenuesProfileViewsByVenue/<id>")
def getVenuesProfileViewsByVenue(id):
    conn = g.db
    cur = conn.cursor()

    try:
        cur.execute('SELECT * FROM "venuesProfileViews" WHERE "venueId" = %s', (id,))
        profile_views_data = cur.fetchall()

        if not profile_views_data:
            return jsonify([])

        return jsonify(profile_views_data), 200
    
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred retrieving the profile views."
            }
        ), 500
    
    finally:
        cur.close()

# ----------------------
# [NEW] TO BE ADDED:
# ----------------------

# # [GET] venuesProfileViews
# @blueprint.route("/getVenuesProfileViews")
# def getVenuesProfileViews():
#     db = g.db
#     profile_views_data = db.venuesProfileViews.find({})
#     allProfileViews = []
#     for profile_view in profile_views_data:
#         # Fetch related views data based on the id(s) in profile_view's views
#         views_data = db.venuesProfileViewsViews.find({
#             "_id": {"$in": profile_view['views']}
#         })
#         profile_view['views'] = list(views_data)
#         allProfileViews.append(profile_view)
#     return parse_json(allProfileViews)

# # [GET] venuesProfileViews by venueID
# @blueprint.route("/getVenuesProfileViewsByVenue/<id>")
# def getVenuesProfileViewsByVenue(id):
#     db = g.db
#     profile_views_data = db.venuesProfileViews.find({"venueID": ObjectId(id)})
#     allProfileViews = []
#     for profile_view in profile_views_data:
#         # Fetch related views data based on the id(s) in profile_view's views
#         views_data = db.venuesProfileViewsViews.find({
#             "_id": {"$in": profile_view['views']}
#         })
#         profile_view['views'] = list(views_data)
#         allProfileViews.append(profile_view)
#     return parse_json(allProfileViews)

# =======================================================

# -----------------------------------------------------------------------------------------
# [GET] requestInaccuracy by venueID
@blueprint.route("/getRequestInaccuracyByVenue/<id>")
def getRequestInaccuracyByVenue(id):
    # only get requestInaccuracy that has reviewStatus = False
    conn = g.db
    cur = conn.cursor()

    try:
        cur.execute('SELECT * FROM "requestInaccuracy" WHERE "venueId" = %s AND "reviewStatus" = FALSE', (id,))
        request_inaccuracy_data = cur.fetchall()

        if not request_inaccuracy_data:
            return jsonify([])

        return jsonify(request_inaccuracy_data), 200
    
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred retrieving the request inaccuracy."
            }
        ), 500
    
    finally:
        cur.close()

# -----------------------------------------------------------------------------------------
# [GET] Badges
@blueprint.route("/getBadges")
def getBadges():
    conn = g.db
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM "badges"')
        badges_data = cursor.fetchall()

    if not badges_data:
        return jsonify([])

    return jsonify(badges_data)

# [GET] User Badges
@blueprint.route("/getUserBadges/<int:user_id>")
def getUserBadges(user_id):
    conn = g.db
    with conn.cursor() as cursor:
        # Get user badges with details
        cursor.execute('''
            SELECT ub.*, b.*, 
                   ub."dateEarned", ub."currentLevel", ub."currentProgress",
                   br."actionsRequired" as "nextLevelRequirement"
            FROM "userBadges" ub
            JOIN "badges" b ON ub."badgeId" = b.id
            LEFT JOIN "badgeRules" br ON 
                (CASE 
                    WHEN b."badgeType" = 'Action' THEN b."relatedEntity"
                    ELSE 'Review'
                END) = br."actionType" AND 
                ub."currentLevel" + 1 BETWEEN br."levelStart" AND br."levelEnd"
            WHERE ub."userId" = %s
            ORDER BY ub."dateEarned" DESC
        ''', (user_id,))
        
        user_badges = cursor.fetchall()
    
    return jsonify(user_badges)

# -----------------------------------------------------------------------------------------
# [GET] Specific Token
@blueprint.route("/getToken/<token>")
def getToken(token):
    conn = g.db
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT * FROM "tokens" WHERE "token" = %s
        """, (token,))

        token_data = cur.fetchone()

        if token_data is None:
            return jsonify({
                "code": 404,
                "message": "Token not found."
            }), 404
        
        if token_data['userId'] is not None:
            user_id = token_data['userId']
        elif token_data['producerId'] is not None:
            user_id = token_data['producerId']
        elif token_data['venueId'] is not None:
            user_id = token_data['venueId']
        else:
            return jsonify({
                "code": 500,
                "message": "Token does not have a valid associated user."
            }), 500
        
        response_data = {
            "id": token_data['id'],
            "token": token_data['token'],
            "requestId": token_data['requestId'],
            "expiry": token_data['expiry'],
            "userId": user_id
        }

        
        return jsonify({
            "code": 200,
            "data": response_data
        }), 200
    
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred retrieving the token."
            }
        ), 500
    
    finally:
        cur.close()

@blueprint.route("/getTokenByRequestId/<requestId>")
def getTokenByRequestId(requestId):
    conn = g.db
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT * FROM "tokens" WHERE "requestId" = %s
        """, (requestId,))
        token_data = cur.fetchone()

        if token_data is None:
            return jsonify({
                "code": 404,
                "message": "Token not found."
            }), 404
        
        if token_data['userId'] is not None:
            user_id = token_data['userId']
        elif token_data['producerId'] is not None:
            user_id = token_data['producerId']
        elif token_data['venueId'] is not None:
            user_id = token_data['venueId']
        else:
            return jsonify({
                "code": 500,
                "message": "Token does not have a valid associated user."
            }), 500
        
        response_data = {
            "id": token_data['id'],
            "token": token_data['token'],
            "requestId": token_data['requestId'],
            "expiry": token_data['expiry'],
            "userId": user_id
        }

        return jsonify({
            "code": 200,
            "data": response_data
        }), 200
    
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred retrieving the token."
            }
        ), 500
    
    finally:
        cur.close()

# -----------------------------------------------------------------------------------------
# [GET] Specific Request
@blueprint.route("/getAccountRequest/<id>")
def getAccountRequest(id):
    conn = g.db
    cur = conn.cursor()
    try:
        # check if theres parameters, only for profile + profile settings, will it send this
        if request.args:
            businessType = request.args.get('businessType')  # e.g. ?businessType=venue

            cur.execute("""
                SELECT * FROM "accountRequests" WHERE "businessId" = %s AND "businessType" = %s
            """, (id, businessType,))

        else:
            cur.execute("""
                SELECT * FROM "accountRequests" WHERE "id" = %s
            """, (id,))

        request_data = cur.fetchone()

        if request_data is None:
            return jsonify([]), 200
        
        return jsonify(request_data), 200
    
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred retrieving the request."
            }
        ), 500
    
    finally:
        cur.close()

# -----------------------------------------------------------------------------------------
# [GET] Producers
@blueprint.route("/getUsernames")
def getUsernames():
    conn = g.db
    cur = conn.cursor()

    try:
        cur.execute('SELECT "username" FROM "producers"')
        producer_usernames = cur.fetchall()

        cur.execute('SELECT "username" FROM "venues"')
        venue_usernames = cur.fetchall()

        # Combine and filter usernames
        usernames = (
            [username['username'] for username in producer_usernames] +
            [username['username'] for username in venue_usernames]
        )
        usernames = [username for username in usernames if username]  # Filter out any None values

        return jsonify(usernames), 200
    
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred retrieving usernames."
            }
        ), 500
    
    finally:
        cur.close()


# -----------------------------------------------------------------------------------------
# [GET] Any User Regardless of Type by Email
@blueprint.route("/getUserByEmail/<email>")
def getUserByEmail(email):
    conn = g.db
    cur = conn.cursor()

    # Define return data
    return_data = None

    try:
        # Check if user is a user and retrieve the id 
        cur.execute('SELECT * FROM "users" WHERE "email" = %s', (email,))
        user_data = cur.fetchone()

        if user_data is not None:
            return_data = {'id': user_data['id'], 'type': 'user', 'username': user_data['username']}
            
            return jsonify(return_data), 200
        
        # Check if user is a producer and retrieve the id
        cur.execute('SELECT * FROM "producers" WHERE "email" = %s', (email,))
        producer_data = cur.fetchone()

        if producer_data is not None:
            return_data = {'id': producer_data['id'], 'type': 'producer', 'username': producer_data['username']}
            
            return jsonify(return_data), 200
        
        # Check if user is a venue and retrieve the id
        cur.execute('SELECT * FROM "venues" WHERE "email" = %s', (email,))
        venue_data = cur.fetchone()

        if venue_data is not None:
            return_data = {'id': venue_data['id'], 'type': 'venue', 'username': venue_data['username']}
            
            return jsonify(return_data), 200
        
        return jsonify(
            {
                "code": 404,
                "message": "Email not found."
            }
        ), 404
    
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": str(e)
            }
        ), 500
    
    finally:
        cur.close()


# -----------------------------------------------------------------------------------------
# [GET] A list of users a specific user is following
# @param id: The id of the user
# @return: A list of users the user is following and their photos
# Used: CreateClub.vue (frontend/src/views/Users/CreateClub.vue)
@blueprint.route("/getUserFollowList/<id>")
def getUserFollowList(id):
    conn = g.db
    cur = conn.cursor()

    try:
        # Step 1: Check if id is a valid user in the table based on userType
        cur.execute('SELECT * FROM "users" WHERE "id" = %s', (id,))
        user_data = cur.fetchone()

        if user_data is None:
            return jsonify(
                {
                    "code": 404,
                    "message": "User not found."
                }
            ), 404
        
        # Step 2: Retrieve the follow list using the fetch_user_follow_list function
        follow_list = fetch_follow_lists(cur, id)


        return_data = {
            'users': {}, # A dictionary of objects containing the id, displayName, and photo of the users in the follow list
        }

        # Step 3: Get the id, displayName and photo of the users in the follow list
        for user in follow_list['users']:
            cur.execute('SELECT "id", "displayName", "photo" FROM "users" WHERE "id" = %s', (user,))
            user = cur.fetchone()

            return_data['users'][user['id']] = { 'displayName': user['displayName'], 'photo': user['photo'] }

        return jsonify({
            'followList': return_data
        }), 200

    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred retrieving the follow list."
            }
        ), 500
    
    finally:
        cur.close()

# -----------------------------------------------------------------------------------------
# [GET] All the usernames in the database [users only]
@blueprint.route("/getAllUsernames")
def getAllUsernames():
    conn = g.db
    cur = conn.cursor(cursor_factory=RealDictCursor)  # Use RealDictCursor for dictionaries

    try:
        # Get all the required user fields
        cur.execute('SELECT "id", "username", "displayName", "photo" FROM "users"')
        users_data = cur.fetchall()
        
        if not users_data:
            return jsonify([]), 404
            
        return jsonify(users_data)
    except Exception as e:
        print(str(e))
        return jsonify([])
    finally:
        cur.close()


# -----------------------------------------------------------------------------------------
# [GET] Check if a user is in the follow list of another user
@blueprint.route("/checkUserInFollowList/<userId>/<userType>/<followId>/<followType>")
def checkUserInFollowList(userId, userType, followId, followType):
    conn = g.db
    cur = conn.cursor()

    try:
        # Step 1: Check if userId and followId are valid users in the table based on userType and followType
        if userType == 'user':
            cur.execute('SELECT * FROM "users" WHERE "id" = %s', (userId,))
        elif userType == 'producer':
            cur.execute('SELECT * FROM "producers" WHERE "id" = %s', (userId,))
        else:
            cur.execute('SELECT * FROM "venues" WHERE "id" = %s', (userId,))
        user_data = cur.fetchone()

        if user_data is None:
            return jsonify(
                {
                    "code": 404,
                    "message": "User not found."
                }
            ), 404

        if followType == 'user':
            cur.execute('SELECT * FROM "users" WHERE "id" = %s', (followId,))
        elif followType == 'producer':
            cur.execute('SELECT * FROM "producers" WHERE "id" = %s', (followId,))
        else:
            cur.execute('SELECT * FROM "venues" WHERE "id" = %s', (followId,))
        follow_data = cur.fetchone()
        
        if follow_data is None:
            return jsonify(
                {
                    "code": 404,
                    "message": "Follow user not found."
                }
            ), 404
        
        key = None
        
        # Step 2: Retrieve the follow list of the user
        if followType == 'venue':
            key = 'venues'
            cur.execute('SELECT venues FROM "usersFollowLists" WHERE "userId" = %s', (userId,))
        elif followType == 'producer':
            key = 'producers'
            cur.execute('SELECT producers FROM "usersFollowLists" WHERE "userId" = %s', (userId,))
        else:
            key = 'users'
            cur.execute('SELECT users FROM "usersFollowLists" WHERE "userId" = %s', (userId,))
        follow_list = cur.fetchone()

        if follow_list is None:
            return jsonify(
                {
                    "code": 404,
                    "message": "Follow list not found."
                }
            ), 404
        
        # Step 3: Check if the followId is in the follow list of the userId
        if followId in follow_list[key]:
            return jsonify(
                {
                    "code": 200,
                    "following": True
                }
            ), 200
        
        return jsonify(
            {
                "code": 404,
                "following": False
            }
        ), 404

    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred checking the follow list."
            }
        ), 500
    
    finally:
        cur.close()


# -----------------------------------------------------------------------------------------
# [GET] Get news from https://88bamboo.co/blogs/news.atom and convert from RSS to JSON //parse_rss funciton 
@blueprint.route("/getLatestNews", methods=['GET'])
def getLatestNews():
    """API endpoint to fetch RSS data and return it as JSON."""
    rss_url = "https://88bamboo.co/blogs/news.atom"

    try:
        rss_json = parse_rss(rss_url)

         # Add Open Graph images to each news entry
        for entry in rss_json.get("entries", []):
            og_image = get_og_image(entry["link"])
            entry["image"] = og_image if og_image else "https://placehold.co/600x400"  # Place your own placeholder image

        return jsonify(rss_json)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -----------------------------------------------------------------------------------------
# [GET] get listings by observation tags -- ADDED BY SMU GROUP 3
@blueprint.route("/getListingsByObservationTag/<tag>")
def get_listings_by_observation_tag(tag):
    selected_tag = tag  

    if not selected_tag:
        return jsonify({"error": "Tag is required"}), 400

    conn = g.db  

    try:
        with conn.cursor() as cursor:
            query = """
            SELECT DISTINCT l.*
            FROM "listings" l
            JOIN "reviews" r ON l."id" = r."reviewTarget"
            WHERE %s = ANY(r."observationTag");
            """
            cursor.execute(query, (selected_tag,))

            listings = cursor.fetchall()  # Fetch results as dictionaries

            # Convert the dictionary rows into a list of dictionaries
            listing_dicts = [dict(row) for row in listings]

            # Debugging output
            print("Listings as Dicts:", listing_dicts)

        # Return the result as JSON
        return jsonify(listing_dicts)

    except Exception as e:
        # If an error occurs, print the error message and return an error response
        print(f"Error fetching listings: {e}")
        return jsonify({"error": "A server error occurred."}), 500

# -----------------------------------------------------------------------------------------
# [GET] Top 8 Trending Observation Tags -- ADDED BY SMU GROUP 3
@blueprint.route("/getTop8")
def getTop8():
    conn = g.db

    with conn.cursor() as cursor:
        query = """
            SELECT TRIM(BOTH '"' FROM tag_name_clean) AS tag_name, SUM(tag_count) AS tag_count
            FROM (
                SELECT unnest(string_to_array(tag_name, ',')) AS tag_name_clean, tag_count
                FROM (
                    SELECT trim(both '"' FROM unnest(string_to_array(
                        replace(trim(both '{}' FROM "observationTag"::TEXT), '","', '|||'), '|||'
                    ))) AS tag_name, 1 AS tag_count
                    FROM "reviews"
                    WHERE "observationTag" IS NOT NULL
                ) sub
            ) final_sub
            GROUP BY TRIM(BOTH '"' FROM tag_name_clean)
            ORDER BY tag_count DESC
            LIMIT 8;
        """
        cursor.execute(query)
        top8_data = cursor.fetchall() 
        columns = [desc[0] for desc in cursor.description]  

        print("Columns:", columns)  
        print("Listings:", top8_data)  

        listing_dicts = []
        for row in top8_data:
            raw_tags = row["tag_name"].strip('{}')  
            tag_names = [tag.strip('"') for tag in raw_tags.split(',')]  
            
            for tag in tag_names:
                listing_dicts.append({"tag_name": tag, "tag_count": row["tag_count"]})
        final_listings = []

        for tag_entry in listing_dicts:
            if len(final_listings) < 7:  
                final_listings.append(tag_entry["tag_name"])
            else:
                break

        print("Final Processed Tags:", final_listings)  

    return jsonify(final_listings)

# -----------------------------------------------------------------------------------------
# [GET] Top Trending Bottle Listings -- ADDED BY SMU GROUP 3
# getTopListings, retrieves the top 6 bottle listings from a database, prioritizing listings with the highest number of reviews. 
# If fewer than 6 listings have reviews, additional listings are fetched based on the most recently added ones. 
# The function ensures that listings with reviews are prioritized while filling the remaining slots with newly added listings.
@blueprint.route("/getTopListings")
def getTopListings():
    conn = g.db  # Get database connection from Flask's global object
    
    with conn.cursor() as cursor:
        # Query to get listings that have reviews, ordered by review count (most reviewed first)
        query = """
            SELECT l.*, COUNT(r."reviewTarget") AS review_count
            FROM "reviews" r
            JOIN "listings" l ON r."reviewTarget" = l."id"
            GROUP BY l."id", l."listingName", l."bottler", l."bottlerID",
                    l."originCountry", l."drinkType", l."abv", l."officialDesc", l."allowMod",
                    l."addedDate", l."typeCategory", l."age", l."reviewLink", l."sourceLink",
                    l."photo", l."drinkStyle"
            ORDER BY review_count DESC, l."addedDate" DESC
            LIMIT 6;  -- Limit the results to 6 top listings
        """
        
        cursor.execute(query)
        top_listings = cursor.fetchall()  # Fetch the top-reviewed listings
        
        # If fewer than 6 listings were found, fetch additional recent listings
        if len(top_listings) < 6:
            remaining_count = 6 - len(top_listings)  # Determine how many more are needed
            
            # Extract the IDs of listings already retrieved to avoid duplicates
            existing_ids = [listing["id"] for listing in top_listings]
            
            # Construct the fallback query to fetch additional listings
            if existing_ids:
                # Exclude the already retrieved listings from the results
                fallback_query = f"""
                    SELECT l.*, 0 AS review_count  -- No reviews for these additional listings
                    FROM "listings" l
                    WHERE l."id" NOT IN ({','.join(str(id) for id in existing_ids)})  -- Exclude already retrieved listings
                    ORDER BY l."addedDate" DESC  -- Order by most recently added
                    LIMIT {remaining_count};  -- Fetch only the required number of listings
                """
            else:
                # If no listings were retrieved initially, just fetch the most recent ones
                fallback_query = f"""
                    SELECT l.*, 0 AS review_count
                    FROM "listings" l
                    ORDER BY l."addedDate" DESC
                    LIMIT {remaining_count};
                """
            
            cursor.execute(fallback_query)
            additional_listings = cursor.fetchall()  # Fetch additional listings
            
            # Merge the two result sets
            top_listings.extend(additional_listings)
        
        # Debugging output to verify results
        print("Top Listings:", top_listings)
    
    return jsonify(top_listings)  # Return the final list of listings as JSON response


# -----------------------------------------------------------------------------------------
#  [GET] ALL Listing Names in Listing Table -- ADDED BY SMU GROUP 3
@blueprint.route("/getListingsName")
def getListingsName():
    conn = g.db

    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM "listings"')
        listingsName_data = cursor.fetchall()
    
    if not listingsName_data:
        return jsonify([])
    
    # Extract listingName from each record
    listing_names = [listing['listingName'] for listing in listingsName_data]

    return jsonify(listing_names)

# -----------------------------------------------------------------------------------------
# [GET] Get Listings from a randomly selected date -- ADDED BY SMU GROUP 3
@blueprint.route("/getRandomListings")
def getRandomListings():
    conn = g.db

    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        # Fetch distinct dates by converting timestamps to dates
        cursor.execute('SELECT DISTINCT "addedDate"::DATE FROM "listings"')
        date_results = cursor.fetchall()

        if not date_results:
            return jsonify({"error": "No dates found in listings"}), 400

        # Log the fetched dates
        print("Fetched date_results:", date_results)

        try:
            # Extract 'addedDate' values properly from RealDictRow
            date_list = [row['addedDate'] for row in date_results if 'addedDate' in row]
            
            # Log the extracted date list
            print("Extracted date_list:", date_list)

            if not date_list:
                return jsonify({"error": "Date extraction failed (empty list)"}), 400

            random_date = random.choice(date_list)  # Select a random date
        except Exception as e:
            return jsonify({"error": f"Random selection failed: {str(e)}"}), 500

        # Fetch listings from the selected random date
        cursor.execute('SELECT * FROM "listings" WHERE "addedDate"::DATE = %s ORDER BY RANDOM() LIMIT 30', (random_date,))
        listings_data = cursor.fetchall()

    if not listings_data:
        return jsonify({"error": "No listings found for selected date"}), 400

    return jsonify(listings_data)

# -----------------------------------------------------------------------------------------
# [GET] Get User Notifications
# Purpose: Fetch notifications for a user based on their account type
# Output: Notification items for the logged-in user
@blueprint.route('/getNotifications/<acc_type>/<acc_id>', methods=['GET'])
def getNotifications(acc_type, acc_id):
    conn = g.db
    cur = conn.cursor()
    
    try:
        acc_id = int(acc_id)
        
        for_you_notifications = []
        venues_notifications = []

        def normalize_datetime(time_value):
            if time_value is None:
                return None
                
            if isinstance(time_value, str):
                try:
                    return datetime.strptime(time_value, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc)
                except ValueError:
                    try:
                        return datetime.strptime(time_value, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
                    except ValueError:
                        return datetime.now(timezone.utc)
            elif isinstance(time_value, date) and not isinstance(time_value, datetime):
                return datetime.combine(time_value, datetime.min.time()).replace(tzinfo=timezone.utc)
            elif isinstance(time_value, datetime):
                if time_value.tzinfo is None:
                    return time_value.replace(tzinfo=timezone.utc)
                return time_value
            
            return datetime.now(timezone.utc)
        
        if acc_type == "user":
            # Getting upvoted reviews notifications
            cur.execute("""
                SELECT r.id AS review_id, r."reviewTarget", r."userID", rv.upvotes, l."listingName" 
                FROM reviews r
                JOIN "reviewsUserVotes" rv ON r.id = rv."reviewId"
                JOIN listings l ON r."reviewTarget" = l.id
                WHERE r."userID" = %s AND rv.upvotes IS NOT NULL AND jsonb_array_length(rv.upvotes) > 0
                ORDER BY r."createdDate" DESC
            """, (acc_id,))
            upvoted_reviews = cur.fetchall()
            
            for review in upvoted_reviews:
                upvotes = review['upvotes']
                for i, upvote in enumerate(upvotes):
                    if i >= 3:
                        break
                    
                    notification = {
                        'type': 'review_upvote',
                        'title': f"Your review on {review['listingName']} got upvoted!",
                        'time': upvote['date'],
                        'link': f"/listing/view/{review['reviewTarget']}/{review['listingName']}",
                        'read': False
                    }
                    for_you_notifications.append(notification)
            
            # Getting comment likes notifications
            cur.execute("""
                SELECT cc.id AS comment_id, cc."commentContent", cc."commentDate", 
                       cp.id AS post_id, c.id AS club_id, c."clubName",
                       ccl.id AS like_id, ccl."memberID" AS liker_id
                FROM "clubPostComments" cc
                JOIN "clubPosts" cp ON cc."postID" = cp.id
                JOIN clubs c ON cp."clubID" = c.id
                JOIN "clubMembers" cm ON cc."commenterID" = cm.id
                LEFT JOIN "clubPostCommentsLikes" ccl ON cc.id = ccl."commentID"
                WHERE cm."userID" = %s AND cm."userType" = 'user'
                ORDER BY ccl.id DESC
            """, (acc_id,))
            comment_activities = cur.fetchall()
            
            comment_likes_count = {}
            for activity in comment_activities:
                if activity['like_id'] is not None:
                    comment_id = activity['comment_id']
                    if comment_id not in comment_likes_count:
                        comment_likes_count[comment_id] = 0
                    
                    if comment_likes_count[comment_id] < 3:
                        notification = {
                            'type': 'comment_like',
                            'title': f"Someone liked your comment in {activity['clubName']}",
                            'time': activity['commentDate'],
                            'link': f"/club/{activity['club_id']}/post/{activity['post_id']}",
                            'read': False
                        }
                        for_you_notifications.append(notification)
                        comment_likes_count[comment_id] += 1
            
            # Getting club invites notifications
            cur.execute("""
                SELECT ci.id AS invite_id, ci."inviteDate", c.id AS club_id, c."clubName",
                       CASE 
                           WHEN ci."inviterUserType" = 'user' THEN (SELECT username FROM users WHERE id = ci."inviterID")
                           WHEN ci."inviterUserType" = 'producer' THEN (SELECT username FROM producers WHERE id = ci."inviterID")
                           WHEN ci."inviterUserType" = 'venue' THEN (SELECT username FROM venues WHERE id = ci."inviterID")
                       END AS inviter_username
                FROM "clubInvites" ci
                JOIN clubs c ON ci."clubID" = c.id
                WHERE ci."inviteeID" = %s AND ci."inviteeUserType" = 'user'
                ORDER BY ci."inviteDate" DESC
            """, (acc_id,))
            club_invites = cur.fetchall()
            
            for invite in club_invites:
                notification = {
                    'type': 'club_invite',
                    'title': f"@{invite['inviter_username']} invited you to join a club: {invite['clubName']}!",
                    'time': invite['inviteDate'],
                    'link': f"/club/view/{invite['club_id']}/{invite['clubName']}",
                    'read': False
                }
                for_you_notifications.append(notification)
            
            # Getting tagged in reviews notifications
            cur.execute("""
                SELECT r.id AS review_id, r."createdDate", r."reviewTarget", l."listingName",
                       u.username AS tagger_username, u.id AS tagger_id
                FROM reviews r
                JOIN listings l ON r."reviewTarget" = l.id
                JOIN users u ON r."userID" = u.id
                WHERE %s = ANY(r."taggedUsers")
                ORDER BY r."createdDate" DESC
            """, (str(acc_id),))
            tagged_reviews = cur.fetchall()
            
            for review in tagged_reviews:
                notification = {
                    'type': 'tagged_in_review',
                    'title': f"@{review['tagger_username']} just tagged you in their review of {review['listingName']}!",
                    'time': review['createdDate'],
                    'link': f"/listing/view/{review['reviewTarget']}/{review['listingName']}",
                    'read': False
                }
                for_you_notifications.append(notification)

            # Getting new badge notifications
            thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
            cur.execute("""
                SELECT ub."badgeId", ub."currentLevel", ub."dateEarned", ub."lastUpdated",
                       b."badgeName", b."badgePhoto", b."badgeDesc", b."badgeType",
                       u.username
                FROM "userBadges" ub
                JOIN "badges" b ON ub."badgeId" = b.id
                JOIN "users" u ON ub."userId" = u.id
                WHERE ub."userId" = %s 
                ORDER BY ub."lastUpdated" DESC, ub."dateEarned" DESC
                LIMIT 20
            """, (acc_id,))
            
            recent_badges = cur.fetchall()

            for badge in recent_badges:
                # Normalize the datetime objects
                date_earned = normalize_datetime(badge['dateEarned'])
                
                # Check if this badge activity is within the last 30 days
                if date_earned and date_earned >= thirty_days_ago:
                    # New badge earned
                    notification = {
                        'type': 'badge_earned',
                        'title': f"You just earned a new badge: {badge['badgeName']}!",
                        'time': date_earned,
                        'link': f"/profile/user/{acc_id}/{badge['username']}",
                        'read': False,
                        'badgePhoto': badge['badgePhoto'],
                        'badgeLevel': badge['currentLevel']
                    }
                    for_you_notifications.append(notification)

        elif acc_type == "producer":
            # Getting producer questions notifications
            cur.execute("""
                SELECT pqa.id, pqa.question, pqa.date, pqa."userId",
                       u.username AS user_username,
                       p.id AS producer_id, p."producerName", p.username AS producer_username
                FROM "producersQuestionAnswers" pqa
                JOIN users u ON pqa."userId" = u.id
                JOIN producers p ON pqa."producerId" = p.id
                WHERE pqa."producerId" = %s
                ORDER BY pqa.date DESC
            """, (acc_id,))
            producer_questions = cur.fetchall()
            
            for question in producer_questions:
                notification = {
                    'type': 'producer_question',
                    'title': f"@{question['user_username']} asked you a question",
                    'time': question['date'],
                    'link': f"/profile/producer/{question['producer_id']}/{question['producer_username']}",
                    'read': False
                }
                for_you_notifications.append(notification)
                
            # Getting edit requests notifications
            cur.execute("""
                SELECT re.id, re."editDesc", re."listingID", l."listingName",
                       u.username AS user_username
                FROM "requestEdits" re
                JOIN listings l ON re."listingID" = l.id
                JOIN users u ON re."userID" = u.id
                WHERE l."producerID" = %s
                ORDER BY re.id DESC
            """, (acc_id,))
            edit_requests = cur.fetchall()
            
            for request in edit_requests:
                notification = {
                    'type': 'edit_request',
                    'title': f"@{request['user_username']} requested an edit for {request['listingName']}",
                    'time': None,
                    'link': f"/request/view",
                    'read': False
                }
                for_you_notifications.append(notification)
                
            # Getting menu inclusions notifications
            cur.execute("""
                SELECT mi.id, mi."itemPrice", mi."itemAvailability",
                       l.id AS listing_id, l."listingName",
                       v.id AS venue_id, v."venueName", v.username AS venue_username,
                       vm.id AS menu_id
                FROM "menuItems" mi
                JOIN listings l ON mi."itemID" = l.id
                JOIN "venuesMenu" vm ON mi."sectionId" = vm.id
                JOIN venues v ON vm."venueId" = v.id
                WHERE l."producerID" = %s
                ORDER BY mi.id DESC
            """, (acc_id,))
            menu_inclusions = cur.fetchall()
            
            for inclusion in menu_inclusions:
                notification = {
                    'type': 'menu_inclusion',
                    'title': f"{inclusion['venueName']} added your {inclusion['listingName']} to their menu",
                    'time': None,
                    'link': f"/profile/venue/{inclusion['venue_id']}/{inclusion['venue_username']}",
                    'read': False
                }
                for_you_notifications.append(notification)
            
            # Getting club joins notifications (for producer-owned clubs)
            cur.execute("""
                SELECT cm.id, cm."joinDate", cm."userID", cm."userType",
                       c.id AS club_id, c."clubName",
                       CASE 
                           WHEN cm."userType" = 'user' THEN (SELECT username FROM users WHERE id = cm."userID")
                           WHEN cm."userType" = 'producer' THEN (SELECT username FROM producers WHERE id = cm."userID")
                           WHEN cm."userType" = 'venue' THEN (SELECT username FROM venues WHERE id = cm."userID")
                       END AS member_username
                FROM "clubMembers" cm
                JOIN clubs c ON cm."clubID" = c.id
                WHERE c.id IN (
                    SELECT cm2."clubID" FROM "clubMembers" cm2 
                    WHERE cm2."userID" = %s AND cm2."userType" = 'producer' AND cm2."isAdmin" = TRUE
                )
                ORDER BY cm."joinDate" DESC
            """, (acc_id,))
            club_joins = cur.fetchall()
            
            for join in club_joins:
                notification = {
                    'type': 'club_join',
                    'title': f"@{join['member_username']} joined your club: {join['clubName']}",
                    'time': join['joinDate'],
                    'link': f"/club/view/{join['club_id']}/{join['clubName']}",
                    'read': False
                }
                for_you_notifications.append(notification)
                
            # Getting event joins notifications (for producer-owned events)
            cur.execute("""
                SELECT ea.id, ea."eventDate", ea."userID", ea."attendeeType",
                       e.id AS event_id, e."eventName",
                       CASE 
                           WHEN ea."attendeeType" = 'user' THEN (SELECT username FROM users WHERE id = ea."userID")
                           WHEN ea."attendeeType" = 'producer' THEN (SELECT username FROM producers WHERE id = ea."userID")
                           WHEN ea."attendeeType" = 'venue' THEN (SELECT username FROM venues WHERE id = ea."userID")
                       END AS attendee_username
                FROM "eventAttendees" ea
                JOIN events e ON ea."eventID" = e.id
                WHERE e."eventOwnerID" = %s AND e."eventOwnerType" = 'producer'
                ORDER BY ea."eventDate" DESC
            """, (acc_id,))
            event_joins = cur.fetchall()
            
            for join in event_joins:
                notification = {
                    'type': 'event_join',
                    'title': f"@{join['attendee_username']} is attending your event: {join['eventName']}",
                    'time': join['eventDate'],
                    'link': f"/event/{join['event_id']}/{join['eventName']}",
                    'read': False
                }
                for_you_notifications.append(notification)
                
        elif acc_type == "venue":
            # Getting venue questions notifications
            cur.execute("""
                SELECT vqa.id, vqa.question, vqa.date, vqa."userId",
                       u.username AS user_username,
                       v.id AS venue_id, v."venueName", v.username AS venue_username
                FROM "venuesQuestionAnswers" vqa
                JOIN users u ON vqa."userId" = u.id
                JOIN venues v ON vqa."venueId" = v.id
                WHERE vqa."venueId" = %s
                ORDER BY vqa.date DESC
            """, (acc_id,))
            venue_questions = cur.fetchall()
            
            for question in venue_questions:
                notification = {
                    'type': 'venue_question',
                    'title': f"@{question['user_username']} asked you a question",
                    'time': question['date'],
                    'link': f"/profile/venue/{question['venue_id']}/{question['venue_username']}",
                    'read': False
                }
                for_you_notifications.append(notification)
                
            # Getting venue tagged in reviews notifications
            cur.execute("""
                SELECT r.id AS review_id, r."createdDate", r."reviewTarget", l."listingName",
                       u.username AS reviewer_username, u.id AS reviewer_id
                FROM reviews r
                JOIN listings l ON r."reviewTarget" = l.id
                JOIN users u ON r."userID" = u.id
                WHERE r.location = %s
                ORDER BY r."createdDate" DESC
                LIMIT 10
            """, (acc_id,))
            venue_tag_reviews = cur.fetchall()
            
            for review in venue_tag_reviews:
                notification = {
                    'type': 'venue_tagged_review',
                    'title': f"@{review['reviewer_username']} mentioned your venue in their review of {review['listingName']}",
                    'time': review['createdDate'],
                    'link': f"/listing/view/{review['reviewTarget']}/{review['listingName']}",
                    'read': False
                }
                for_you_notifications.append(notification)
                
            # Getting club joins notifications (for venue-owned clubs)
            cur.execute("""
                SELECT cm.id, cm."joinDate", cm."userID", cm."userType",
                       c.id AS club_id, c."clubName",
                       CASE 
                           WHEN cm."userType" = 'user' THEN (SELECT username FROM users WHERE id = cm."userID")
                           WHEN cm."userType" = 'producer' THEN (SELECT username FROM producers WHERE id = cm."userID")
                           WHEN cm."userType" = 'venue' THEN (SELECT username FROM venues WHERE id = cm."userID")
                       END AS member_username
                FROM "clubMembers" cm
                JOIN clubs c ON cm."clubID" = c.id
                WHERE c.id IN (
                    SELECT cm2."clubID" FROM "clubMembers" cm2 
                    WHERE cm2."userID" = %s AND cm2."userType" = 'venue' AND cm2."isAdmin" = TRUE
                )
                ORDER BY cm."joinDate" DESC
            """, (acc_id,))
            club_joins = cur.fetchall()
            
            for join in club_joins:
                notification = {
                    'type': 'club_join',
                    'title': f"@{join['member_username']} joined your club: {join['clubName']}",
                    'time': join['joinDate'],
                    'link': f"/club/view/{join['club_id']}/{join['clubName']}",
                    'read': False
                }
                for_you_notifications.append(notification)
                
            # Getting event joins notifications (for venue-owned events)
            cur.execute("""
                SELECT ea.id, ea."eventDate", ea."userID", ea."attendeeType",
                       e.id AS event_id, e."eventName",
                       CASE 
                           WHEN ea."attendeeType" = 'user' THEN (SELECT username FROM users WHERE id = ea."userID")
                           WHEN ea."attendeeType" = 'producer' THEN (SELECT username FROM producers WHERE id = ea."userID")
                           WHEN ea."attendeeType" = 'venue' THEN (SELECT username FROM venues WHERE id = ea."userID")
                       END AS attendee_username
                FROM "eventAttendees" ea
                JOIN events e ON ea."eventID" = e.id
                WHERE e."eventOwnerID" = %s AND e."eventOwnerType" = 'venue'
                ORDER BY ea."eventDate" DESC
            """, (acc_id,))
            event_joins = cur.fetchall()
            
            for join in event_joins:
                notification = {
                    'type': 'event_join',
                    'title': f"@{join['attendee_username']} is attending your event: {join['eventName']}",
                    'time': join['eventDate'],
                    'link': f"/event/{join['event_id']}/{join['eventName']}",
                    'read': False
                }
                for_you_notifications.append(notification)
        
        # Process venues notifications for user account type
        if acc_type == "user":
            # Getting venue status updates
            cur.execute("""
                SELECT vu.id, vu.date, vu.text, vu.photo,
                       v.id AS venue_id, v."venueName", v.photo AS venue_photo, v.username AS venue_username
                FROM "venuesUpdates" vu
                JOIN venues v ON vu."venueId" = v.id
                ORDER BY vu.date DESC
                LIMIT 20
            """)
            venue_updates = cur.fetchall()
            
            for update in venue_updates:
                notification = {
                    'type': 'venue_status_update',
                    'title': f"{update['venueName']} just updated their status: \"{update['text']}\"",
                    'time': update['date'],
                    'link': f"/profile/venue/{update['venue_id']}/{update['venue_username']}",
                    'read': False,
                    'logo': update['venue_photo']
                }
                venues_notifications.append(notification)
            
            # Getting producer status updates
            cur.execute("""
                SELECT pu.id, pu.date, pu.text, pu.photo,
                       p.id AS producer_id, p."producerName", p.photo AS producer_photo, p.username AS producer_username
                FROM "producersUpdates" pu
                JOIN producers p ON pu."producerId" = p.id
                ORDER BY pu.date DESC
                LIMIT 20
            """)
            producer_updates = cur.fetchall()
            
            for update in producer_updates:
                notification = {
                    'type': 'producer_status_update',
                    'title': f"{update['producerName']} just updated their status: \"{update['text']}\"",
                    'time': update['date'],
                    'link': f"/profile/producer/{update['producer_id']}/{update['producer_username']}",
                    'read': False,
                    'logo': update['producer_photo']
                }
                venues_notifications.append(notification)
            
            # Getting venue question answers
            cur.execute("""
                SELECT vqa.id, vqa.question, vqa.answer, vqa.date,
                       v.id AS venue_id, v."venueName", v.photo AS venue_photo, v.username AS venue_username
                FROM "venuesQuestionAnswers" vqa
                JOIN venues v ON vqa."venueId" = v.id
                WHERE vqa."userId" = %s
                AND vqa.answer IS NOT NULL
                ORDER BY vqa.date DESC
                LIMIT 20
            """, (acc_id,))
            venue_answers = cur.fetchall()
            
            for answer in venue_answers:
                notification = {
                    'type': 'venue_question_reply',
                    'title': f"{answer['venueName']} just posted a reply to the question: \"{answer['question']}\"",
                    'time': answer['date'],
                    'link': f"/profile/venue/{answer['venue_id']}/{answer['venue_username']}",
                    'read': False,
                    'logo': answer['venue_photo']
                }
                venues_notifications.append(notification)
            
            # Getting producer question answers
            cur.execute("""
                SELECT pqa.id, pqa.question, pqa.answer, pqa.date,
                       p.id AS producer_id, p."producerName", p.photo AS producer_photo, p.username AS producer_username
                FROM "producersQuestionAnswers" pqa
                JOIN producers p ON pqa."producerId" = p.id
                WHERE pqa."userId" = %s
                AND pqa.answer IS NOT NULL
                ORDER BY pqa.date DESC
                LIMIT 20
            """, (acc_id,))
            producer_answers = cur.fetchall()
            
            for answer in producer_answers:
                notification = {
                    'type': 'producer_question_reply',
                    'title': f"{answer['producerName']} just posted a reply to the question: \"{answer['question']}\"",
                    'time': answer['date'],
                    'link': f"/profile/producer/{answer['producer_id']}/{answer['producer_username']}",
                    'read': False,
                    'logo': answer['producer_photo']
                }
                venues_notifications.append(notification)
            
            # Getting events
            cur.execute("""
                SELECT e.id, e."eventName", e."eventStartDate", e."eventEndDate", 
                       e."eventStartTime", e."eventEndTime", e."createdDate",
                       e."eventOwnerID", e."eventOwnerType",
                       CASE 
                           WHEN e."eventOwnerType" = 'producer' THEN 
                               (SELECT "producerName" FROM producers WHERE id = e."eventOwnerID")
                           WHEN e."eventOwnerType" = 'venue' THEN 
                               (SELECT "venueName" FROM venues WHERE id = e."eventOwnerID")
                       END AS owner_name,
                       CASE 
                           WHEN e."eventOwnerType" = 'producer' THEN 
                               (SELECT photo FROM producers WHERE id = e."eventOwnerID")
                           WHEN e."eventOwnerType" = 'venue' THEN 
                               (SELECT photo FROM venues WHERE id = e."eventOwnerID")
                       END AS owner_photo,
                       CASE 
                           WHEN e."eventOwnerType" = 'producer' THEN 
                               (SELECT username FROM producers WHERE id = e."eventOwnerID")
                           WHEN e."eventOwnerType" = 'venue' THEN 
                               (SELECT username FROM venues WHERE id = e."eventOwnerID")
                       END AS owner_username
                FROM events e
                WHERE e."eventOwnerType" IN ('producer', 'venue')
                ORDER BY e."createdDate" DESC
                LIMIT 20
            """)
            events = cur.fetchall()
            
            for event in events:
                event_date = event['eventStartDate'].strftime('%B %d, %Y')
                if event['eventStartTime']:
                    event_date += f" at {event['eventStartTime'].strftime('%I:%M %p')}"
                
                notification = {
                    'type': 'new_event',
                    'title': f"{event['owner_name']} is hosting a new event: {event['eventName']} on {event_date}",
                    'time': event['createdDate'],
                    'link': f"/event/{event['id']}/{event['eventName']}",
                    'read': False,
                    'logo': event['owner_photo']
                }
                venues_notifications.append(notification)
            
            # Getting current time and calculate 24 hours ago
            now = datetime.now(timezone.utc)
            twenty_four_hours_ago = now - timedelta(hours=24)
            
            cur.execute("""
                SELECT l.id, l."listingName", l."addedDate", l."producerID",
                       p."producerName", p.photo AS producer_photo, p.username AS producer_username
                FROM listings l
                JOIN producers p ON l."producerID" = p.id
                WHERE l."addedDate" >= %s
                ORDER BY l."addedDate" DESC
            """, (twenty_four_hours_ago,))
            new_listings = cur.fetchall()
            
            # Group by producer and limit to 2 per producer
            producer_drink_count = {}
            for listing in new_listings:
                producer_id = listing['producerID']
                if producer_id not in producer_drink_count:
                    producer_drink_count[producer_id] = 0
                
                if producer_drink_count[producer_id] < 2:
                    notification = {
                        'type': 'new_drink',
                        'title': f"{listing['producerName']} added a new drink: {listing['listingName']}",
                        'time': listing['addedDate'],
                        'link': f"/listing/view/{listing['id']}/{listing['listingName']}",
                        'read': False,
                        'logo': listing['producer_photo']
                    }
                    venues_notifications.append(notification)
                    producer_drink_count[producer_id] += 1
        
        def normalize_datetime(time_value):
            if time_value is None:
                return None
                
            if isinstance(time_value, str):
                try:
                    return datetime.strptime(time_value, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc)
                except ValueError:
                    try:
                        return datetime.strptime(time_value, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
                    except ValueError:
                        return datetime.now(timezone.utc)
            elif isinstance(time_value, date) and not isinstance(time_value, datetime):
                return datetime.combine(time_value, datetime.min.time()).replace(tzinfo=timezone.utc)
            elif isinstance(time_value, datetime):
                if time_value.tzinfo is None:
                    return time_value.replace(tzinfo=timezone.utc)
                return time_value
            
            return datetime.now(timezone.utc)
        
        # Helper function for sorting
        def get_sort_key(notification):
            time_value = notification.get('time')
            if time_value is not None:
                return normalize_datetime(time_value)
            return datetime.now(timezone.utc)
        
        # Normalize datetime objects in notifications
        for notification in for_you_notifications:
            if notification['time'] is not None:
                notification['time'] = normalize_datetime(notification['time'])
        
        for notification in venues_notifications:
            if notification['time'] is not None:
                notification['time'] = normalize_datetime(notification['time'])
        
        # Sort notifications by time (recent first)
        for_you_notifications.sort(key=get_sort_key, reverse=True)
        venues_notifications.sort(key=get_sort_key, reverse=True)
        
        # Return the notifications
        return jsonify({
            'forYou': for_you_notifications[:10],  # Limit to 10 most recent notifications
            'venues': venues_notifications[:20]
        }), 200
        
    except Exception as e:
        print(str(e))
        return jsonify({
            'code': 500,
            'message': 'An error occurred fetching notifications.'
        }), 500
    
    finally:
        cur.close()