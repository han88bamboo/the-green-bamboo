# Port: 5000
# Routes: 
#           [Account Requests]
#           /getAccountRequests (GET), 

#           [Countries]
#           /getCountries (GET), 

#           [Listings]
#           /getListings (GET), /getListingsByIDs (POST), /getListing/<id> (GET), /getListingsBySearch (GET),
#           /getListingsDetailedByID/<id> (GET), /getListingNamesDynamicSearch/<searchTerm> (GET), /getListingsNames/<search_term> (GET),
#           /getRecentlyAddedListings (POST), /getListingByName/<listing_name> (GET), /getListingNamesByProducer/<searchTerm>/<producerId> (GET)

#           [Producers]
#           /getProducers (GET), /getProducer/<id> (GET), /getProducersByIDs (POST), /getProducersBySearch (GET),
#           /getProducersProfileViews (GET), /getProducersProfileViewsByProducer/<id> (GET), /getProducerNamesDynamicSearch/<searchTerm> (GET),
#           /getBestRatedExpressions/<producerID> (GET), /getMostReviewedExpressions/<producerID> (GET),
#           /getProducerDashBoardData/<producerID> (GET), /getProducerLatestReviews/<producerID> (GET),

#           [Venues]
#           /getVenuesWithSpecificListing/<listingID> (GET), /getVenuesBySearch (GET), /getVenues (GET), /getVenuesByIds
#           /getVenue/<id> (GET), /getVenuesAPI (GET), /getVenuesProfileViewsByVenue/<id> (GET),

#           [Users]
#           /getUsers (GET), /getUsersFromList (POST), /getUserFollowListDetails (POST) /getUser/<id> (GET), 
#           /getUserPhoto/<id>/<userType> (GET), /getUserByUsername/<username> (GET), /getUsernameFromEmail/<email> (GET), /getUserFollowList/<id> (GET), 
#           /checkFollowing/<userId>/<userType>/<followId>/<followType> (GET), /getUserReviewSummary/<id> (GET),
#           /getUserDashBoardData/<id> (GET), /getRecentFollowersActivity/<id> (GET), /getRecentReviewsActivity/<id> (GET),
#           /getLatestReviewsDrinks/<id> (GET),
#           /getRecentUserActivity/<id> (GET), /getAllUserFollowingsIDs/<id> (GET), /getAllUserFollowing/<id> (GET), /getAllUserFollowers/<id> (GET),

#           [Listing Reviews]
#           /getRecentListingReviews/<id> (GET), /getAllUserReviews/<id> (GET), /getReviews (GET),
#           /getReviewsByListingIDs (POST), /getReviewByTarget/<id> (GET), /getReviewsByUserIds (GET), 
#           /getListingReviewsRating/<listing_id> (GET), /getTop5MostReviewedListings (GET),

#           [Producer Reviews]
#           /getProducerTourReviews (GET), /getProducerReviewsByProducerId/<id> (GET),

#           [Venue Reviews]
#           /getVenueReviews (GET), /getVenueReviewsByVenueId/<id>/<lastReviewID> (GET), /getHomeReviews (GET), 

#           [User Bookmarks]
#           /getBookmarkListings (POST), 

#           [Request listings]
#           /getRequestListings (GET), /getRequestListing/<id> (GET), /getRequestListingsByRole/<role>/<id> (GET),
   
#           [Request Edits]
#           /getRequestEdits (GET), /getRequestEditsByRole/<role>/<id> (GET), /getRequestEdit/<id> (GET),

#           [Others]
#           /getDrinkTypes (GET), /getTypeCategories (GET), /getModRequests (GET),
#           /getFlavourTags (GET), /getSubTags (GET), /getObservationTags (GET),
#           /getColours (GET), /getSpecialColours (GET), /getLanguages (GET),
#           /getServingTypes (GET), /getLatestNews (GET), /getRequestInaccuracyByVenue/<id> (GET),
#           /getUserNames (GET), /getQuestionsUpdates (GET), /getRequestsCount (POST), /getUserNamesDynamic/<search_Term> (GET),
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
import hashlib
import traceback
from urllib.parse import unquote
from bs4 import BeautifulSoup
from bson import json_util
from flask import Blueprint, g, jsonify, request
from psycopg2.extras import RealDictCursor # ADDED BY SMU GROUP 3
from decimal import Decimal
from datetime import datetime, timezone, date, timedelta
from scripts import pointsHelperFunc
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

# Helper function to fetch drink lists for a user
def fetch_drink_lists(cursor, user_id):
    result = {}
    try: 
        # Single query using LEFT JOIN to get all data at once
        cursor.execute("""
            SELECT 
                udl."id" as list_id,
                udl."listName",
                udl."listDesc",
                udli."drinkId",
                udli."addedDate"
            FROM "usersDrinkLists" udl
            LEFT JOIN "usersDrinkListItems" udli ON udl."id" = udli."listId"
            WHERE udl."userId" = %s
            ORDER BY udl."listName", udli."addedDate" DESC
        """, (user_id,))
        
        rows = cursor.fetchall()
        
        # Process results in a single pass
        for row in rows:
            list_name = row["listName"]
            
            # Initialize list if not exists
            if list_name not in result:
                result[list_name] = {
                    "listDesc": row["listDesc"],
                    "listItems": []
                }
            
            # Add drink item if it exists (LEFT JOIN may return NULL for empty lists)
            if row["drinkId"] is not None:
                result[list_name]["listItems"].append({
                    "drinkId": row["drinkId"],
                    "addedDate": row["addedDate"]
                })
        
        return result
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        # print("something went wrong" + str(e), flush=True)
        return result

# Helper function to fetch producer lists for a user
def fetch_producer_lists(cursor, user_id):
    result = {}
    try: 
        # Single query using LEFT JOIN to get all data at once
        cursor.execute("""
            SELECT 
                upl."id" as list_id,
                upl."listName",
                upl."listDesc",
                upli."producerId",
                upli."addedDate"
            FROM "userProducerLists" upl
            LEFT JOIN "userProducerListItems" upli ON upl."id" = upli."listId"
            WHERE upl."userId" = %s
            ORDER BY upl."listName", upli."addedDate" DESC
        """, (user_id,))
        
        rows = cursor.fetchall()
        
        # Process results in a single pass
        for row in rows:
            list_name = row["listName"]
            
            # Initialize list if not exists
            if list_name not in result:
                result[list_name] = {
                    "listDesc": row["listDesc"],
                    "listItems": []
                }
            
            # Add producer item if it exists (LEFT JOIN may return NULL for empty lists)
            if row["producerId"] is not None:
                result[list_name]["listItems"].append({
                    "producerId": row["producerId"],
                    "addedDate": row["addedDate"]
                })
        
        return result
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        # print("something went wrong" + str(e), flush=True)
        return result
    
def fetch_venue_lists(cursor, user_id):
    result = {}
    try: 
        cursor.execute("""
            SELECT 
                uvl."id" as list_id,
                uvl."listName",
                uvl."listDesc",
                uvli."venueId",
                uvli."addedDate"
            FROM "userVenueLists" uvl
            LEFT JOIN "userVenueListItems" uvli ON uvl."id" = uvli."listId"
            WHERE uvl."userId" = %s
            ORDER BY uvl."listName", uvli."addedDate" DESC
        """, (user_id,))

        rows = cursor.fetchall()

        for row in rows:
            list_name = row["listName"]

            if list_name not in result:
                result[list_name] = {
                    "listDesc": row["listDesc"],
                    "listItems": []
                }

            if row["venueId"] is not None:
                result[list_name]["listItems"].append({
                    "venueId": row["venueId"],
                    "addedDate": row["addedDate"]
                })

        return result

    except Exception as e:
        import traceback
        traceback.print_exc()
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
# [GET] Listings by user id
@blueprint.route("/lbListings", methods=['GET'])
def lbListings():
    conn = g.db
    try:
        # Get query parameters
        user_id = request.args.get('id', '').strip()

        sql = """
            SELECT "user_id", "listing_id", "category"
            FROM "userLeaderboard"
            WHERE "user_id" = %s
            ORDER BY "sort_order" ASC; 
        """

        with conn.cursor() as cursor:
            cursor.execute(sql, (user_id,))
            rows = cursor.fetchall()

        # if nothing was found
        if not rows:
            return jsonify([]), 200

        # Initialize lists
        grails = []
        upAndComing = []
        goats = []

        # Loop through rows and sort into respective lists
        for row in rows:
            listing_id = row["listing_id"]
            category = row["category"]
            if category == 'grails':
                grails.append(listing_id)
            elif category == 'upAndComing':
                upAndComing.append(listing_id)
            elif category == 'goats':
                goats.append(listing_id)

        # Return as JSON response
        return jsonify({
            "userID": user_id,
            "grails": grails,
            "upAndComing": upAndComing,
            "goats": goats
        }), 200
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        # print("something went wrong" + str(e), flush=True)
        return jsonify({"error": str(e)}), 500


@blueprint.route("/getListingsByIDs", methods=['GET', 'POST'])
def getListingsByIDs():
    conn = g.db

    try:
        # Handle both GET and POST requests
        if request.method == 'POST':
            # For POST requests, get IDs from JSON body
            data = request.get_json()
            listing_ids = data.get('listingIDs', []) if data else []
        else:
            # For GET requests, get IDs from query parameters
            raw_ids = request.args.getlist('ids')
            listing_ids = [int(i) for i in raw_ids]

        if not listing_ids:
            return jsonify([]), 200

        # Ensure all IDs are integers
        listing_ids = [int(i) for i in listing_ids]

        sql = """
            SELECT l."id", l."listingName", l."drinkType", l."typeCategory",
                l."originCountry", l."bottler", l."photo", l."producerID",
                p."producerName"
            FROM listings l
            LEFT JOIN producers p ON l."producerID" = p."id"
            WHERE l."id" IN %s;
        """

        with conn.cursor() as cursor:
            cursor.execute(sql, (tuple(listing_ids),))
            rows = cursor.fetchall()

        result = [
            {
                "id": row["id"], 
                "listingName": row["listingName"], 
                "drinkType": row.get("drinkType", ""),
                "typeCategory": row.get("typeCategory", ""),
                "originCountry": row.get("originCountry", ""),
                "bottler": row.get("bottler", ""),
                "photo": row.get("photo", ""),
                "producerID": row.get("producerID", ""),
                "producerName": row.get("producerName", ""),
            } 
            for row in rows
        ]

        return jsonify(result), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# -----------------------------------------------------------------------------------------
# [GET] Get Listings from db where id> last item in list [discovery tab]
@blueprint.route("/getNext30/<id>")
def getNext30(id):
    conn = g.db
    id = int(id)
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM "listings" where "id" > %s LIMIT 30', (id,))
        listings_data = cursor.fetchall()

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
    
    if not listings_data:
        return jsonify([])

    return jsonify(listings_data)

# -----------------------------------------------------------------------------------------
# [GET] Listings from db when filter is applied for next 30 in discovery tab [discover tab]
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
# [POST] Get Listings from next in following list for both venue and producer [following tab]
@blueprint.route("/getNextFollowing30", methods=['POST'])
def getNextFollowing30():
    conn = g.db

    followedProducers = request.args.get('followedProducers')
    followedVenues = request.args.get('followedVenues')
    lastListingIdP = request.args.get('lastListingIdP', 0)
    lastMenuId = request.args.get('lastMenuId', 0)

    last_listing_id_p = 0
    last_menu_id = 0

    listings_data = []

    try:

        with conn.cursor() as cursor:

            if followedProducers and len(followedProducers) > 0:
                cursor.execute('SELECT * FROM "listings" WHERE "id" < %s  AND "producerID" IN %s ORDER BY "addedDate" DESC LIMIT 15', (lastListingIdP, tuple(followedProducers),))
                producer_listings = cursor.fetchall()
                listings_data.extend(producer_listings)
                last_listing_id_p = producer_listings[-1]['id']

            if followedVenues and len(followedVenues) > 0:
                cursor.execute("""
                    SELECT 
                        l.*,                             
                        vm."venueId",                     
                        v."venueName",                  
                        m."id" AS "menuItemId"           
                    FROM "menuItems" m
                    JOIN "listings" l ON m."itemID" = l."id"
                    JOIN "venuesMenu" vm ON m."sectionId" = vm."id"
                    JOIN "venues" v ON vm."venueId" = v."id"
                    WHERE m."itemID" IS NOT NULL
                    AND m."id" < %s
                    AND vm."venueId" IN %s
                    ORDER BY m."id" DESC
                    LIMIT 15;
                """, (lastMenuId, tuple(followedVenues),))
                venue_listings = cursor.fetchall()

                # Loop through the venue listings to remove duplicate listings
                for venue_listing in venue_listings:
                    # Check if the listing already exists in the listings_data
                    if not any(listing['id'] == venue_listing['id'] for listing in listings_data):
                        last_menu_id = venue_listing['menuItemId']
                        listings_data.append(venue_listing)

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

                    # Get the producer name if it's a listing
                    if 'producerID' in listing:
                        cursor.execute('SELECT "producerName" FROM "producers" WHERE "id" = %s', (listing['producerID'],))
                        producer_name = cursor.fetchone()
                        listing['producerName'] = producer_name['producerName'] if producer_name else 'Unknown Producer'

        return jsonify({
            "listings": listings_data,
            "lastListingIdP": last_listing_id_p,
            "lastMenuId": last_menu_id
        })
    except Exception as e:
        print(f"Error fetching next following listings: {str(e)}")
        return jsonify({"code": 500, "message": "An error occurred while fetching listings."}), 500

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


# [GET] Listings by search term
# Parameters: searchTerm (string), lastID (int)
@blueprint.route("/getListingsBySearch")
def getListingsBySearch():
    conn = g.db
    cursor = conn.cursor()
    searchTerm = request.args.get('searchTerm', '').strip()
    lastID = request.args.get('lastID', '0').strip()
    lastID = int(lastID) if lastID.isdigit() else 0

    try:
        search = f'%{searchTerm}%'

        offset = int(request.args.get('offset', 0))
        cursor.execute("""
            SELECT 
                l.*, 
                p."producerName",
                (similarity(unaccent(l."listingName"), unaccent(%s)) + 3 * similarity(unaccent(p."producerName"), unaccent(%s))) AS combined_sim_score
            FROM "listings" l
            JOIN "producers" p ON l."producerID" = p."id"
            WHERE unaccent(l."listingName") %% unaccent(%s)
            
            UNION
                       
            SELECT 
                l.*, 
                p."producerName",
                (similarity(unaccent(l."listingName"), unaccent(%s)) + 3 * similarity(unaccent(p."producerName"), unaccent(%s))) AS combined_sim_score
            FROM "listings" l
            JOIN "producers" p ON l."producerID" = p."id"
            WHERE unaccent(p."producerName") %% unaccent(%s)

            ORDER BY combined_sim_score DESC
            LIMIT 30 OFFSET %s
        """, (searchTerm, searchTerm, searchTerm, searchTerm, searchTerm, searchTerm, offset))
                       
        listings_data = cursor.fetchall()

            
        if not listings_data:
            return jsonify([])
        
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
                listing['averageRating'] = round(avg_rating, 1)
            else:
                listing['averageRating'] = '-'

            # Get the producer name
            cursor.execute('SELECT "producerName" FROM "producers" WHERE "id" = %s', (listing['producerID'],))
            producer_name = cursor.fetchone()
            listing['producerName'] = producer_name['producerName'] if producer_name else 'Unknown Producer'
        
        return jsonify(listings_data)

    except Exception as e:
        print(f"Error fetching listings by search: {str(e)}")
        return jsonify({"code": 500, "message": "An error occurred while fetching listings."}), 500


# [GET] Get detailed listing information by listing ID
@blueprint.route("/getListingsDetailedByID/<id>")
def getListingsDetailedByID(id):
    conn = g.db
    cursor = conn.cursor()

    try: 
        # Fetch the listing details
        cursor.execute('SELECT * FROM "listings" WHERE "id" = %s', (id,))
        listing_data = cursor.fetchone()

        if listing_data is None:
            return jsonify({"code": 404, "message": "Listing not found"}), 404

        # Fetch the producer details
        cursor.execute('SELECT "producerName", "photo" FROM "producers" WHERE "id" = %s', (listing_data['producerID'],))
        producer_data = cursor.fetchone()

        if producer_data is None:
            return jsonify({"code": 404, "message": "Producer not found"}), 404

        # Combine the listing and producer data
        detailed_listing = {
            **listing_data,
            "producerName": producer_data['producerName'],
            "photo": producer_data['photo']
        }

        # Get the average rating for the listing
        cursor.execute("""
            SELECT AVG("rating") AS "averageRating"
            FROM "reviews"
            WHERE "reviewTarget" = %s
        """, (id,))

        avg_rating = cursor.fetchone()['averageRating']

        if avg_rating is not None:
            detailed_listing['avgRating'] = round(avg_rating, 1)
        else:
            detailed_listing['avgRating'] = '-'

        return jsonify(detailed_listing), 200

    except Exception as e:
        print(f"Error fetching detailed listing by ID {id}: {str(e)}")
        return jsonify({"code": 500, "message": "An error occurred while fetching the listing."}), 500


# [GET] Get Listing names by dynamic search term
@blueprint.route("/getListingNamesDynamicSearch/<searchTerm>")
def getListingNamesDynamicSearch(searchTerm):
    conn = g.db
    cursor = conn.cursor()

    try:
        # Searches for listings by name, starting from the lastID
        cursor.execute(""" 
            SELECT 
                l."id", 
                l."listingName", 
                l."photo",
                p."producerName",
                l."drinkType",
                l."typeCategory",
                l."abv",
                l."originCountry",
                l."officialDesc",
                COALESCE((SELECT AVG(r."rating") FROM "reviews" r WHERE r."reviewTarget" = l."id"), 0) as "avgRating",
                (similarity(unaccent(l."listingName"), unaccent(%s)) + 3 * similarity(unaccent(p."producerName"), unaccent(%s))) AS combined_sim_score
            FROM "listings" l
            JOIN "producers" p ON l."producerID" = p."id"
            WHERE unaccent(l."listingName") %% unaccent(%s)
            
            UNION
            
            SELECT 
                l."id", 
                l."listingName", 
                l."photo",
                p."producerName",
                l."drinkType",
                l."typeCategory",
                l."abv",
                l."originCountry",
                l."officialDesc",
                COALESCE((SELECT AVG(r."rating") FROM "reviews" r WHERE r."reviewTarget" = l."id"), 0) as "avgRating",
                (similarity(unaccent(l."listingName"), unaccent(%s)) + 3 * similarity(unaccent(p."producerName"), unaccent(%s))) AS combined_sim_score
            FROM "listings" l
            JOIN "producers" p ON l."producerID" = p."id"
            WHERE unaccent(p."producerName") %% unaccent(%s)
            
            ORDER BY combined_sim_score DESC
            LIMIT 50
        """, (searchTerm, searchTerm, searchTerm, searchTerm, searchTerm, searchTerm))

        listings_data = cursor.fetchall()

        # Convert the fetched data to a list of dictionaries
        for listing in listings_data:
            listing_dict = {
                "id": listing["id"],
                "listingName": listing["listingName"],
                "producerName": listing["producerName"],
                "photo": listing["photo"],
                "drinkType": listing["drinkType"],
                "typeCategory": listing["typeCategory"],
                "abv": listing["abv"],
                "originCountry": listing["originCountry"],
                "officialDesc": listing["officialDesc"],
                "avgRating": listing["avgRating"],
                "similarity": listing["combined_sim_score"]
            }
            # Convert Decimal to float if necessary
            for key, value in listing_dict.items():
                if isinstance(value, Decimal):
                    listing_dict[key] = float(value)
            listing.update(listing_dict)

        if not listings_data:
            return jsonify([])

        return jsonify(listings_data)

    except Exception as e:
        print(f"Error fetching listing names by dynamic search: {str(e)}")
        return jsonify({"code": 500, "message": "An error occurred while fetching listing names."}), 500

# [GET] Get producer names by dynamic search term
@blueprint.route("/getProducerNamesDynamicSearch/<searchTerm>")
def getProducerNamesDynamicSearch(searchTerm):
    conn = g.db
    cursor = conn.cursor()

    try:
        # Searches for producers by name with similarity
        cursor.execute(""" 
            SELECT 
                p."id", 
                p."producerName",
                p."originCountry",
                p."photo",
                similarity(unaccent(p."producerName"), unaccent(%s)) AS sim_score
            FROM "producers" p
            WHERE unaccent(p."producerName") %% unaccent(%s)
            ORDER BY sim_score DESC
            LIMIT 20
        """, (searchTerm, searchTerm))

        producers_data = cursor.fetchall()

        # Convert the fetched data to a list of dictionaries
        for producer in producers_data:
            producer_dict = {
                "id": producer["id"],
                "producerName": producer["producerName"],
                "originCountry": producer["originCountry"],
                "photo": producer["photo"],
                "similarity": producer["sim_score"]
            }
            # Convert Decimal to float if necessary
            for key, value in producer_dict.items():
                if isinstance(value, Decimal):
                    producer_dict[key] = float(value)
            producer.update(producer_dict)

        if not producers_data:
            return jsonify([])

        return jsonify(producers_data)

    except Exception as e:
        print(f"Error in getProducerNamesDynamicSearch: {str(e)}")
        return jsonify({"code": 500, "message": "An error occurred while searching producers."}), 500

# [GET] Get Listing names by dynamic search term filtered by producer
@blueprint.route("/getListingNamesByProducer/<searchTerm>/<int:producerId>")
def getListingNamesByProducer(searchTerm, producerId):
    conn = g.db
    cursor = conn.cursor()

    try:

        # First, lower the similarity threshold to 0.15 for more permissive matching
        cursor.execute("SET pg_trgm.similarity_threshold = 0.15")

        # Searches for listings by name from a specific producer
        cursor.execute(""" 
            SELECT 
                l."id", 
                l."listingName", 
                l."photo",
                p."producerName",
                l."drinkType",
                l."typeCategory",
                l."abv",
                l."originCountry",
                l."officialDesc",
                COALESCE((SELECT AVG(r."rating") FROM "reviews" r WHERE r."reviewTarget" = l."id"), 0) as "avgRating",
                similarity(unaccent(l."listingName"), unaccent(%s)) AS sim_score
            FROM "listings" l
            JOIN "producers" p ON l."producerID" = p."id"
            WHERE l."producerID" = %s
            AND unaccent(l."listingName") %% unaccent(%s)
            ORDER BY sim_score DESC
            LIMIT 30
        """, (searchTerm, producerId, searchTerm))

        listings_data = cursor.fetchall()

        # Convert the fetched data to a list of dictionaries
        for listing in listings_data:
            listing_dict = {
                "id": listing["id"],
                "listingName": listing["listingName"],
                "producerName": listing["producerName"],
                "photo": listing["photo"],
                "drinkType": listing["drinkType"],
                "typeCategory": listing["typeCategory"],
                "abv": listing["abv"],
                "originCountry": listing["originCountry"],
                "officialDesc": listing["officialDesc"],
                "avgRating": listing["avgRating"],
                "similarity": listing["sim_score"]
            }
            # Convert Decimal to float if necessary
            for key, value in listing_dict.items():
                if isinstance(value, Decimal):
                    listing_dict[key] = float(value)
            listing.update(listing_dict)

        if not listings_data:
            return jsonify([])

        return jsonify(listings_data)

    except Exception as e:
        print(f"Error in getListingNamesByProducer: {str(e)}")
        return jsonify({"code": 500, "message": "An error occurred while searching listings by producer."}), 500
    finally:
        # Make sure to reset the threshold back to default (0.3)
        # This will run even if there's an exception in the try block
        try:
            cursor.execute("SET pg_trgm.similarity_threshold TO DEFAULT")
        except:
            pass  # Ignore any errors during cleanup

# [GET] Specific Listings By Producer
@blueprint.route("/getListingsByProducer/<id>")
def getListingsByProducer(id):
    conn = g.db

    with conn.cursor() as cursor:
        cursor.execute('''
            SELECT * FROM "listings"
            WHERE "producerID" = %s OR "bottlerID" = %s
        ''', (id, id))
        listings_data = cursor.fetchall()

    if not listings_data:
        return jsonify([])

    return jsonify(listings_data)

# [GET] Get Listings details by listing name
@blueprint.route("/getListingByName/<listing_name>")
def getListingByName(listing_name):
    # URL decode the listing name in case there are special characters
    listing_name = unquote(listing_name)

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
# [GET] Get all listings names test
@blueprint.route('/producer-listings', methods=['GET'])
def get_producer_listings():
    conn = g.db
    """Get producer ttle listings with search functionality"""
    try:
        # Get query parameters
        query = request.args.get('q', '').strip()
        limit = int(request.args.get('limit', 3))

        # Validate query
        if not query:
            return jsonify([])
        
        # Optimized query using trigram index for fuzzy string matching
        sql = """
            SELECT "id", "producerName", "originCountry",
                similarity(unaccent("producerName"), unaccent(%s)) as sim_score
            FROM producers
            WHERE unaccent("producerName") %% unaccent(%s)
            ORDER BY sim_score DESC
            LIMIT %s;
        """

        with conn.cursor() as cursor:
            cursor.execute(sql, (query, query, limit))
            rows = cursor.fetchall()

        # if nothing was found
        if not rows:
            return jsonify([]), 200

        result = [
            {
                "id": row["id"], 
                "producerName": row["producerName"], 
                "originCountry": row["originCountry"]
            } 
            for row in rows
        ]

        return jsonify(result), 200
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        # print("something went wrong" + str(e), flush=True)
        return jsonify({"error": str(e)}), 500

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
                p."claimStatus", p."statusOB", p.username, p."producerLink", 
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


# [GET] Producers by IDs
@blueprint.route("/getProducersByIDs", methods=['POST'])
def getProducersByIDs():
    conn = g.db
    cursor = conn.cursor()

    try:
        producer_ids = request.json.get('producerIDs', [])

        if not producer_ids:
            return jsonify([
                {
                    "code": 404,
                    "message": "At least one producer ID is required."
                }
            ]), 404
        
        producers_data = []
        for id in producer_ids:
            cursor.execute('SELECT "id", "producerName" FROM "producers" WHERE "id" = %s', (id,))
            producer_data = cursor.fetchone()

            if producer_data:
                producers_data.append({
                    "id": producer_data["id"],
                    "producerName": producer_data["producerName"]
                })

        if not producers_data:
            return jsonify([
                {
                    "code": 404,
                    "message": "No producers found for the provided IDs."
                }
            ]), 404

        return jsonify({
            "code": 200,
            "message": "Producers fetched successfully.",
            "data": producers_data
        }), 200
    
    except Exception as e:
        print(str(e))
        return jsonify({
            "code": 500,
            "message": "An error occurred retrieving the producers."
        }), 500

# [GET] Producers by search term
@blueprint.route("/getProducersBySearch", methods=['GET'])
def getProducersBySearch():
    conn = g.db
    searchTerm = request.args.get('searchTerm', '').strip()
    lastID = request.args.get('lastID', '0').strip()
    lastID = int(lastID) if lastID.isdigit() else 0

    try:
        cursor = conn.cursor()

        # Searches for producers by name or origin country, starting from the lastID
        cursor.execute("""
            SELECT * FROM "producers"
            WHERE ("producerName" ILIKE %s OR "originCountry" ILIKE %s)
            AND "id" > %s
            ORDER BY "id" ASC
            LIMIT 30
        """, ('%' + searchTerm + '%', '%' + searchTerm + '%', lastID))

        producers_data = cursor.fetchall()

        if not producers_data:
            return jsonify([])
        
        # Loop through the producers to get both ratings for each producer
        for producer in producers_data:
            # Get the average Tour & Experience rating for the producer (from producerReviews)
            cursor.execute("""
                SELECT AVG("rating") AS "averageRating"
                FROM "producerReviews"
                WHERE "producerID" = %s 
            """, (producer['id'],))

            # Check if the producer has tour & experience reviews
            avg_tour_rating = cursor.fetchone()['averageRating']
            if avg_tour_rating is not None:
                producer['averageTourRating'] = round(avg_tour_rating, 1)
            else:
                producer['averageTourRating'] = '-'

            # Get the average Drink rating for the producer (from reviews of their listings)
            cursor.execute("""
                SELECT AVG(r."rating") AS "averageDrinkRating"
                FROM "reviews" r
                INNER JOIN "listings" l ON r."reviewTarget" = l."id"
                WHERE l."producerID" = %s
            """, (producer['id'],))

            # Check if the producer has drink reviews
            avg_drink_rating = cursor.fetchone()['averageDrinkRating']
            if avg_drink_rating is not None:
                producer['averageDrinkRating'] = round(avg_drink_rating, 1)
            else:
                producer['averageDrinkRating'] = '-'

            # Keep the old 'averageRating' field for backward compatibility (use tour rating)
            producer['averageRating'] = producer['averageTourRating']

            # Remove the hashed password and other sensitive fields
            producer.pop('hashedPassword', None)

        return jsonify(producers_data)

    except Exception as e:
        print(f"Error fetching producers by search: {str(e)}")
        return jsonify({"code": 500, "message": "An error occurred while fetching producers."}), 500

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
@blueprint.route("/getUniqueProducersNamesID/<search_term>/<pid>")
def getUniqueProducersNamesID(search_term, pid):
    conn = g.db
    cursor = conn.cursor()

    search_term = search_term.strip().lower()

    try:
        # Retrieve producer name and ID is pid is not '0' - stop here since we only want to return this one
        if pid != '0':
            cursor.execute('SELECT "id", "producerName", "originCountry" FROM "producers" WHERE "id" = %s', (int(pid),))
            producer_data = cursor.fetchone()
            
            if producer_data:

                return jsonify({
                    "code": 200,
                    "message": "Producer fetched successfully.",
                    "id": producer_data["id"],
                    "producerName": producer_data["producerName"],
                    "originCountry": producer_data["originCountry"]
                })
            
        # If pid is '0', search for producers by name to populate into the input field for suggestions [SubmitListingNew.vue]
        cursor.execute("""
            SELECT "id", "producerName", "isIndependentBottler", "originCountry"
            FROM "producers"
            WHERE "producerName" ILIKE %s
            LIMIT 30
        """, ('%' + search_term + '%',))
        
        producers_data = cursor.fetchall()  

        if not producers_data:
            return jsonify({
                "code": 404,
                "message": "No producers found."
            })

    except Exception as e:
        print(f"Error fetching producers by search: {str(e)}")
        return jsonify({"code": 500, "message": "An error occurred while fetching producers."}), 500
    
    # Convert the data to a list of dictionaries

    producers_list = []
    for producer in producers_data:
        if producer["producerName"] == None:
            continue
        producer_dict = {
            "producerName": producer["producerName"],
            "isIndependentBottler": producer["isIndependentBottler"],
            "originCountry": producer["originCountry"],
            "id": producer["id"]
        }
        producers_list.append(producer_dict)

    return jsonify({
        "code": 200,
        "message": "Producers fetched successfully.",
        "data": producers_list
    })


# [GET] List of unique bottlers names and id
@blueprint.route("/getUniqueBottlersNamesID/<search_term>")
def getUniqueBottlersNamesID(search_term):
    conn = g.db

    search_term = search_term.strip().lower()

    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT "id", "producerName"
            FROM "producers"
            WHERE "producerName" ILIKE %s AND "isIndependentBottler" = TRUE
            LIMIT 30
        """, ('%' + search_term + '%',))
        
        bottlers_data = cursor.fetchall()

    if not bottlers_data:
        return jsonify({
            "code": 404,
            "message": "No independent bottlers found."
        })
    
    # Convert the data to a list of dictionaries
    bottlers_list = []
    for bottler in bottlers_data:
        if bottler["producerName"] == None:
            continue
        bottler_dict = {
            "producerName": bottler["producerName"],
            "id": bottler["id"]
        }
        bottlers_list.append(bottler_dict)

    return jsonify({
        "code": 200,
        "message": "Independent bottlers fetched successfully.",
        "data": bottlers_list
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

# [GET] All venues with basic info needed for listings
@blueprint.route('/getAllVenues', methods=['GET'])
def getAllVenues():
    conn = g.db
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT "id", "venueName", "address", "venueType", "originLocation", "photo", "username" FROM "venues"')
        venues = cursor.fetchall()
        cursor.close()
        return jsonify(venues), 200
    except Exception as e:
        print("Get all venues error:", str(e))
        return jsonify({
            "code": 500,
            "message": "An error occurred retrieving venues."
        }), 500

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


# [GET] Get recent listing reviews by a specific user + top 5 listings based on the review ratings by a specific user + number of reviews done (aka drink count)
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

    # Get top 5 highest rated reviews by the user (changed from just listing IDs)
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT r.*, l."listingName", l."photo" as "listingPhoto", 
                   p."producerName", v."venueName"
            FROM "reviews" r
            LEFT JOIN "listings" l ON r."reviewTarget" = l."id"
            LEFT JOIN "producers" p ON l."producerID" = p."id"
            LEFT JOIN "venues" v ON r."location" = v."id"
            WHERE r."reviewType" = 'Listing' 
            AND r."userID" = %s
            AND r."rating" IS NOT NULL
            ORDER BY r."rating" DESC, r."createdDate" DESC
            LIMIT 5
        """, (id,))
        
        top_rated_reviews_data = cursor.fetchall()

    # Retrieve the number of reviews done by the user (number of unique listings reviewed)
    with conn.cursor() as cursor:
        cursor.execute('SELECT COUNT(DISTINCT "reviewTarget") FROM "reviews" WHERE "userID" = %s', (id,))
        drink_count = cursor.fetchone()

    return jsonify({
        "recentReview": reviews_data,
        "topRatedReviews": top_rated_reviews_data,  # top rated reviews
        "drinkCount": drink_count["count"]
    }), 200

# [GET] Get all reviews by a specific user with pagination
@blueprint.route("/getAllUserReviews/<id>")
def getAllUserReviews(id):
    conn = g.db
    
    # Get pagination parameters
    offset = int(request.args.get('offset', 0))
    limit = int(request.args.get('limit', 50))  # Default to 50 reviews per page
        
    try:
        # Convert id to int and validate
        user_id = int(id)
        if user_id <= 0:
            print(f"DEBUG: Invalid user ID: {user_id}")
            return jsonify({"code": 400, "message": "Invalid user ID"}), 400
        
        with conn.cursor() as cursor:
            # Get total count of reviews by the user
            print(f"DEBUG: Executing count query for userID={user_id}")
            cursor.execute("""
                SELECT COUNT(*) as total
                FROM "reviews"
                WHERE "userID" = %s 
                AND "reviewType" = 'Listing'
            """, (user_id,))
            
            total_count = cursor.fetchone()["total"]
            
            # Get paginated reviews
            cursor.execute("""
                SELECT "reviews".*, "reviewsUserVotes"."upvotes", "reviewsUserVotes"."downvotes"
                FROM "reviews"
                LEFT JOIN "reviewsUserVotes" ON "reviews"."id" = "reviewsUserVotes"."reviewId"
                WHERE "reviews"."userID" = %s 
                AND "reviews"."reviewType" = 'Listing'
                ORDER BY "reviews"."createdDate" DESC
                LIMIT %s OFFSET %s
            """, (user_id, limit, offset))

            reviews_data = cursor.fetchall()

            if not reviews_data:
                reviews_data = []

            # Process user votes for each review
            for review in reviews_data:
                review["userVotes"] = {
                    "upvotes": review["upvotes"] if review["upvotes"] else [],
                    "downvotes": review["downvotes"] if review["downvotes"] else []
                }
                # Remove the raw vote fields
                if "upvotes" in review:
                    del review["upvotes"]
                if "downvotes" in review:
                    del review["downvotes"]

            # Calculate if there are more reviews
            has_more = (offset + len(reviews_data)) < total_count

            return jsonify({
                "code": 200,
                "message": "User reviews fetched successfully",
                "reviews": reviews_data,
                "total": total_count,
                "hasMore": has_more,
                "offset": offset,
                "limit": limit
            }), 200

    except ValueError:
        print(f"DEBUG: Could not convert id to integer: {id}")
        return jsonify({"code": 400, "message": "Invalid user ID format"}), 400
    except Exception as e:
        print(f"Error fetching all user reviews: {str(e)}")
        return jsonify({
            "code": 500,
            "message": "An error occurred while fetching user reviews."
        }), 500
    
# [GET] Get all listings names test
@blueprint.route('/bottle-listings', methods=['GET'])
def get_bottle_listings():
    conn = g.db
    """Get bottle listings with search functionality"""
    try:
        # Get query parameters
        query = request.args.get('q', '').strip()
        limit = int(request.args.get('limit', 3))

        # Validate query
        if not query:
            return jsonify([])

        # Optimized query using trigram index for fuzzy string matching
        sql = """           
            SELECT 
                l."id", 
                l."listingName", 
                l."drinkType", 
                l."originCountry", 
                l."bottler",
                l."photo",
                p."producerName",
                (similarity(unaccent(l."listingName"), unaccent(%s)) + 3 * similarity(unaccent(p."producerName"), unaccent(%s))) AS combined_sim_score
            FROM "listings" l
            JOIN "producers" p ON l."producerID" = p."id"
            WHERE unaccent(l."listingName") %% unaccent(%s)
            
            UNION

            SELECT 
                l."id", 
                l."listingName", 
                l."drinkType", 
                l."originCountry", 
                l."bottler",
                l."photo",
                p."producerName",
                (similarity(unaccent(l."listingName"), unaccent(%s)) + 3 * similarity(unaccent(p."producerName"), unaccent(%s))) AS combined_sim_score
            FROM "listings" l
            JOIN "producers" p ON l."producerID" = p."id"
            WHERE unaccent(p."producerName") %% unaccent(%s)

            ORDER BY combined_sim_score DESC
            LIMIT %s;
        """
        with conn.cursor() as cursor:
            cursor.execute(sql, (query, query, query, query, query, query, limit))
            rows = cursor.fetchall()

        # if nothing was found
        if not rows:
            return jsonify([]), 200

        result = [
            {
                "id": row["id"], 
                "listingName": row["listingName"], 
                "drinkType": row.get("drinkType", ""),
                "originCountry": row.get("originCountry", ""),
                "photo": row.get("photo", ""),
                "bottler": row.get("bottler", ""),
                "producerName": row.get("producerName", "")
            } 
            for row in rows
        ]

        return jsonify(result), 200
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        # print("something went wrong" + str(e), flush=True)
        return jsonify({"error": str(e)}), 500


# [GET] Get all listings names
@blueprint.route("/getListingsNames/<search_term>")
def getListingsNames(search_term):
    conn = g.db
    search_term = search_term.strip()

    try:

        with conn.cursor() as cursor:
            # Fetch 20 listings names based on the search term
            cursor.execute("""
                SELECT "listingName"
                FROM "listings"
                WHERE "listingName" ILIKE %s
                LIMIT 20
            """, ('%' + search_term + '%',))

            listings_data = cursor.fetchall()

        if not listings_data:
            return jsonify([]), 404

        # Convert into a list
        listings_data = [listing['listingName'] for listing in listings_data]

        return jsonify(listings_data), 200

    except Exception as e:
        print(f"Error fetching listings names: {str(e)}")
        return jsonify({"code": 500, "message": "An error occurred while fetching listings names."}), 500



# [POST] Get recently added listings by producers and venues from a list of producer IDs and venue IDs that a user follows
@blueprint.route("/getRecentlyAddedListings", methods=['POST'])
def getRecentlyAddedListings():
    conn = g.db 
    cursor = conn.cursor()

    producer_ids = request.json.get('producerIDs', [])
    venue_ids = request.json.get('venueIDs', [])

    listings_data = []
    last_listing_id_p = 0
    last_menu_id = 0

    try:
        # Retrieve the top 10 recently added listings by producers whose IDs are in the provided list
        if len(producer_ids) > 0:
            cursor.execute("""
                SELECT * FROM "listings" 
                WHERE "producerID" IN %s 
                ORDER BY "addedDate" DESC
                LIMIT 15
            """, (tuple(producer_ids),))
            producer_listings = cursor.fetchall()

            listings_data.extend(producer_listings)

            last_listing_id_p = producer_listings[-1]['id'] if producer_listings else 0

        # Retrieve the top 10 recently added menu items by venues whose IDs are in the provided list
        if len(venue_ids) > 0:
            cursor.execute("""
                SELECT 
                    l.*,                             
                    vm."venueId",                     
                    v."venueName",                  
                    m."id" AS "menuItemId"           
                FROM "menuItems" m
                JOIN "listings" l ON m."itemID" = l."id"
                JOIN "venuesMenu" vm ON m."sectionId" = vm."id"
                JOIN "venues" v ON vm."venueId" = v."id"
                WHERE m."itemID" IS NOT NULL
                AND vm."venueId" IN %s
                ORDER BY m."id" DESC
                LIMIT 15;
            """, (tuple(venue_ids),))
            venue_listings = cursor.fetchall()

            # Add unique venue listings to the listings_data
            for venue_listing in venue_listings:
                # Check if the listing already exists in listings_data
                if not any(listing['id'] == venue_listing['id'] for listing in listings_data):
                    last_menu_id = venue_listing['menuItemId']
                    listings_data.append(venue_listing)

        # Loop through the listings to get the average rating for each listing and producer name
        if len(listings_data) == 0:
            return jsonify([]), 200
        
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

            # Get the producer name if it's a listing from a producer
            if 'producerID' in listing:
                cursor.execute('SELECT "producerName" FROM "producers" WHERE "id" = %s', (listing['producerID'],))
                producer_name = cursor.fetchone()
                listing['producerName'] = producer_name['producerName'] if producer_name else 'Unknown Producer'
            else:
                listing['producerName'] = 'N/A'

        return jsonify({
            "listings": listings_data,
            "lastListingIdP": last_listing_id_p,
            "lastMenuID": last_menu_id
        }), 200


    
    except Exception as e:
        print(f"Error fetching recently added listings: {str(e)}")
        return jsonify({"code": 500, "message": "An error occurred while fetching recently added listings."}), 500
    
    finally:
        cursor.close()


# [POST] Get bookmarked listings
@blueprint.route("/getBookmarkListings", methods=['POST'])
def getBookmarkListings():
    conn = g.db
    listing_ids = request.json.get('listingIDs', [])

    if not listing_ids:
        return jsonify({
            "code": 404,
            "message": "At least one listing ID is required."
        }), 404

    # Convert to integers in case they come as strings
    listing_ids = [int(id) for id in listing_ids]

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


# [GET] Get aggregated reviews score from user reviews
@blueprint.route("/getVintageAgg/<reviewTarget>")
def getVintageAgg(reviewTarget):
    conn = g.db 

    sql = """
        SELECT 
            "variant" as year,
            ROUND(AVG("rating"), 1) as avgRating,
            ROUND(
                (COUNT(CASE WHEN "willRecommend" = true THEN 1 END) * 100.0 / 
                NULLIF(COUNT(CASE WHEN "willRecommend" IS NOT NULL THEN 1 END), 0)), 0
            ) as recommendPercent,
            ROUND(
                (COUNT(CASE WHEN "wouldBuyAgain" = true THEN 1 END) * 100.0 / 
                NULLIF(COUNT(CASE WHEN "wouldBuyAgain" IS NOT NULL THEN 1 END), 0)), 0
            ) as drinkAgainPercent
        FROM "reviews"
        WHERE "reviewTarget" = %s
        AND "variant" IS NOT NULL
        AND "rating" IS NOT NULL
        GROUP BY "variant"
        ORDER BY "variant" DESC;
    """

    try: 
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql, (reviewTarget, ))
            variant_data = cursor.fetchall()

        if not variant_data:
            return jsonify([])
        
        return jsonify(variant_data)
    except Exception as e:
        import traceback
        traceback.print_exc()
        # Log the error appropriately
        print(f"Error in getVintageAgg: {str(e)}")
        return jsonify({"error": "Failed to fetch review statistics"}), 500


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
@blueprint.route("/getReviews/<int:id>")
def getReviews(id):
    conn = g.db

    sql = """
        SELECT 
            COUNT(*) as total_reviews,
            ARRAY[
                COUNT(CASE WHEN EXTRACT(MONTH FROM "createdDate") = 1 THEN 1 END),
                COUNT(CASE WHEN EXTRACT(MONTH FROM "createdDate") = 2 THEN 1 END),
                COUNT(CASE WHEN EXTRACT(MONTH FROM "createdDate") = 3 THEN 1 END),
                COUNT(CASE WHEN EXTRACT(MONTH FROM "createdDate") = 4 THEN 1 END),
                COUNT(CASE WHEN EXTRACT(MONTH FROM "createdDate") = 5 THEN 1 END),
                COUNT(CASE WHEN EXTRACT(MONTH FROM "createdDate") = 6 THEN 1 END),
                COUNT(CASE WHEN EXTRACT(MONTH FROM "createdDate") = 7 THEN 1 END),
                COUNT(CASE WHEN EXTRACT(MONTH FROM "createdDate") = 8 THEN 1 END),
                COUNT(CASE WHEN EXTRACT(MONTH FROM "createdDate") = 9 THEN 1 END),
                COUNT(CASE WHEN EXTRACT(MONTH FROM "createdDate") = 10 THEN 1 END),
                COUNT(CASE WHEN EXTRACT(MONTH FROM "createdDate") = 11 THEN 1 END),
                COUNT(CASE WHEN EXTRACT(MONTH FROM "createdDate") = 12 THEN 1 END)
            ] as monthly_distribution, 
            ARRAY[ 
                COUNT(CASE WHEN rating >= 1 AND rating < 2 THEN 1 END), 
                COUNT(CASE WHEN rating >= 2 AND rating < 3 THEN 1 END), 
                COUNT(CASE WHEN rating >= 3 AND rating < 4 THEN 1 END), 
                COUNT(CASE WHEN rating >= 4 AND rating < 5 THEN 1 END), 
                COUNT(CASE WHEN rating >= 5 AND rating < 6 THEN 1 END), 
                COUNT(CASE WHEN rating >= 6 AND rating < 7 THEN 1 END), 
                COUNT(CASE WHEN rating >= 7 AND rating < 8 THEN 1 END), 
                COUNT(CASE WHEN rating >= 8 AND rating < 9 THEN 1 END), 
                COUNT(CASE WHEN rating >= 9 AND rating < 10 THEN 1 END), 
                COUNT(CASE WHEN rating >= 10 THEN 1 END) 
            ] as rating_distribution 
        FROM "reviews" 
        WHERE "userID" = %s;
    """
    try: 
        # Validate that id is a positive integer
        if not isinstance(id, int) or id <= 0:
            return jsonify({"code": 400, "message": "Invalid user ID"}), 400 

        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql, (id,))
            reviews_data = cursor.fetchone()

            # Handle case where user has no reviews
            if reviews_data is None:
                review_data = {
                    "total_reviews": 0,
                    "monthly_distribution": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    "rating_distribution": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                }
            else:
                review_data = {
                    "total_reviews": reviews_data["total_reviews"],
                    "monthly_distribution": reviews_data["monthly_distribution"],
                    "rating_distribution": reviews_data["rating_distribution"]
                }

            return jsonify(review_data)
        
    except Exception as e:
        print(f"Error fetching recently added listings: {str(e)}")
        return jsonify({"code": 500, "message": "An error occurred while fetching recently added listings."}), 500


# [GET] Admin dashboard review statistics
@blueprint.route("/getSignupStats", methods=['GET'])
def getSignupStats():
    conn = g.db
    # Get the date parameters from query string
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')

    # Convert ISO dates to date strings for better compatibility
    from datetime import datetime
    if start_date and end_date:
        start_date_obj = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        end_date_obj = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        
        start_date_str = start_date_obj.strftime('%Y-%m-%d')
        end_date_str = end_date_obj.strftime('%Y-%m-%d')
    else:
        return jsonify({"error": "startDate and endDate parameters are required"}), 400


    try: 
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            # Get total reviews count
            total_sql = """
                SELECT 
                    'Total Signups' as category,
                    (
                        COALESCE((SELECT COUNT(*) FROM "users" 
                                WHERE "joinDate" IS NOT NULL 
                                AND ("isAdmin" IS FALSE OR "isAdmin" IS NULL)
                                AND DATE("joinDate") BETWEEN %s AND %s), 0) 
                    ) as "total_count";
            """
            cursor.execute(total_sql, (start_date_str, end_date_str))
            total_result = cursor.fetchone()
            total_signups = total_result['total_count'] if total_result else 0
            
            # Get daily signup data with cumulative counts and fill missing dates with 0
            sql = """
                WITH baseline_counts AS (
                    SELECT 
                        'users' as entity_type,
                        COUNT(*) as baseline_count
                    FROM "users"
                    WHERE "joinDate" IS NOT NULL 
                    AND ("isAdmin" IS FALSE OR "isAdmin" IS NULL)
                    AND DATE("joinDate") < %s  -- before start date
                ),
                daily_signups AS (
                    SELECT
                        DATE("joinDate") as signup_date,
                        'users' as entity_type,
                        COUNT(*) as daily_count
                    FROM "users"
                    WHERE "joinDate" IS NOT NULL AND ("isAdmin" IS FALSE OR "isAdmin" IS NULL)
                    AND DATE("joinDate") BETWEEN %s AND %s
                    GROUP BY DATE("joinDate")
                ),
                all_dates AS (
                    SELECT generate_series(
                        %s::date,
                        %s::date,
                        '1 day'::interval
                    )::date as signup_date
                ),
                entity_types AS (
                    SELECT unnest(ARRAY['users']) as entity_type
                ),
                complete_data AS (
                    SELECT
                        ad.signup_date,
                        et.entity_type,
                        COALESCE(ds.daily_count, 0) as daily_count
                    FROM all_dates ad
                    CROSS JOIN entity_types et
                    LEFT JOIN daily_signups ds ON ad.signup_date = ds.signup_date
                                              AND et.entity_type = ds.entity_type
                )
                SELECT
                    signup_date,
                    cd.entity_type, 
                    daily_count,
                    SUM(daily_count) OVER (
                        PARTITION BY cd.entity_type 
                        ORDER BY signup_date
                        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                    ) + COALESCE(bc.baseline_count, 0) as cumulative_count
                FROM complete_data cd
                LEFT JOIN baseline_counts bc ON cd.entity_type = bc.entity_type
                ORDER BY signup_date DESC, cd.entity_type;
            """
            cursor.execute(sql, (start_date_str, start_date_str, end_date_str, start_date_str, end_date_str))
            all_data = cursor.fetchall()

            qualified_sql = """
                SELECT COUNT(*) AS "qualified_user_count"
                FROM (
                SELECT 
                    "userID"
                FROM "pointsRecorder"
                WHERE "userType" = 'user'
                GROUP BY "userID"
                HAVING SUM("currentPoints") >= 100
                ) AS sub;
            """
            cursor.execute(qualified_sql)
            qualified_user = cursor.fetchone()
            
            # Process data by entity type
            users_data = []
            venues_data = []
            producers_data = []
            
            for row in all_data:
                data_point = {
                    "date": str(row['signup_date']), 
                    "count": row['daily_count'],
                    "cumulative_count": row['cumulative_count']
                }
                
                if row['entity_type'] == 'users':
                    users_data.append(data_point)
                elif row['entity_type'] == 'venues':
                    venues_data.append(data_point)
                elif row['entity_type'] == 'producers':
                    producers_data.append(data_point)
            
            signup_data = {
                "total_signups": total_signups,
                "users": users_data,
                "qualified_user": qualified_user['qualified_user_count']
            }
            
            return jsonify(signup_data)
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        # Log the error appropriately
        print(f"Error in getReviews: {str(e)}")
        return jsonify({"error": "Failed to fetch review statistics"}), 500


# [GET] Admin dashboard review statistics
@blueprint.route("/getReviewStats", methods=['GET'])
def getReviewStats():
    conn = g.db

    # Get the date parameters from query string
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')

    # Convert ISO dates to date strings for better compatibility
    from datetime import datetime
    if start_date and end_date:
        start_date_obj = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        end_date_obj = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        
        start_date_str = start_date_obj.strftime('%Y-%m-%d')
        end_date_str = end_date_obj.strftime('%Y-%m-%d')
    else:
        return jsonify({"error": "startDate and endDate parameters are required"}), 400

    try: 
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            # Single query to get all stats
            combined_sql = """
                SELECT 
                  COALESCE((
                    SELECT COUNT(*) FROM "reviews"
                        WHERE DATE("createdDate") BETWEEN %s AND %s), 0) AS listing_review,
                  COALESCE((
                    SELECT COUNT(*) FROM "producerReviews"
                        WHERE DATE("createdDate") BETWEEN %s AND %s), 0) AS producer_review,
                  COALESCE((
                    SELECT COUNT(*) FROM "venueReviews"
                        WHERE DATE("createdDate") BETWEEN %s AND %s), 0) AS venue_review,
                  COALESCE((
                    SELECT COUNT(*) FROM "listings"
                        WHERE DATE("addedDate") BETWEEN %s AND %s), 0) AS total_listings,
                  COALESCE((
                    SELECT COUNT(*) FROM "clubs" 
                        WHERE "totalMembers" >= 2
                        AND DATE("dateCreated") BETWEEN %s AND %s), 0) AS total_clubs;
            """
            cursor.execute(combined_sql, (start_date_str, end_date_str, start_date_str, end_date_str, 
                                 start_date_str, end_date_str, start_date_str, end_date_str, start_date_str, end_date_str))
            final_result = cursor.fetchone() or {}

            cummulative_review = """
                WITH baseline_counts AS (                    
                    SELECT 
                        'listing_reviews' as entity_type,
                        COUNT(*) as baseline_count
                    FROM "reviews"
                    WHERE "createdDate" IS NOT NULL
                    AND DATE("createdDate") < %s
                    
                    UNION ALL
                    
                    SELECT 
                        'producer_reviews' as entity_type,
                        COUNT(*) as baseline_count
                    FROM "producerReviews"
                    WHERE "createdDate" IS NOT NULL
                    AND DATE("createdDate") < %s
                    
                    UNION ALL
                    
                    SELECT 
                        'venue_reviews' as entity_type,
                        COUNT(*) as baseline_count
                    FROM "venueReviews"
                    WHERE "createdDate" IS NOT NULL
                    AND DATE("createdDate") < %s
                ),
                daily_reviews AS (
                    SELECT
                        DATE("createdDate") as review_date,
                        'listing_reviews' as entity_type,
                        COUNT(*) as daily_count
                    FROM "reviews"
                    WHERE "createdDate" IS NOT NULL
                    AND DATE("createdDate") BETWEEN %s AND %s
                    GROUP BY DATE("createdDate")

                    UNION ALL

                    SELECT
                        DATE("createdDate") as review_date,
                        'producer_reviews' as entity_type,
                        COUNT(*) as daily_count
                    FROM "producerReviews"
                    WHERE "createdDate" IS NOT NULL
                    AND DATE("createdDate") BETWEEN %s AND %s
                    GROUP BY DATE("createdDate")
                    
                    UNION ALL

                    SELECT
                        DATE("createdDate") as review_date,
                        'venue_reviews' as entity_type,
                        COUNT(*) as daily_count
                    FROM "venueReviews"
                    WHERE "createdDate" IS NOT NULL
                    AND DATE("createdDate") BETWEEN %s AND %s
                    GROUP BY DATE("createdDate")
                ),
                all_dates AS (
                    SELECT generate_series(
                        %s::date,
                        %s::date,
                        '1 day'::interval
                    )::date as review_date
                ),
                entity_types AS (
                    SELECT unnest(ARRAY['listing_reviews', 'producer_reviews', 'venue_reviews']) as entity_type
                ),
                complete_data AS (
                    SELECT
                        ad.review_date,
                        et.entity_type,
                        COALESCE(dr.daily_count, 0) as daily_count
                    FROM all_dates ad
                    CROSS JOIN entity_types et
                    LEFT JOIN daily_reviews dr ON ad.review_date = dr.review_date
                                            AND et.entity_type = dr.entity_type
                )
                SELECT
                    review_date,
                    cd.entity_type,
                    daily_count,
                    SUM(daily_count) OVER (
                        PARTITION BY cd.entity_type
                        ORDER BY review_date
                        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                    ) + COALESCE(bc.baseline_count, 0) as cumulative_count
                FROM complete_data cd
                LEFT JOIN baseline_counts bc ON cd.entity_type = bc.entity_type
                ORDER BY review_date DESC, cd.entity_type;
            """
            cursor.execute(cummulative_review, (start_date_str, start_date_str, 
                                 start_date_str, start_date_str, end_date_str, 
                                 start_date_str, end_date_str, start_date_str,
                                 end_date_str, start_date_str, end_date_str))
            all_data = cursor.fetchall()

            # Process data by entity type
            listing_review = []
            producer_review = []
            venue_review = []
            
            for row in all_data:
                data_point = {
                    "date": str(row['review_date']), 
                    "count": row['daily_count'],
                    "cumulative_count": row['cumulative_count']
                }
                
                if row['entity_type'] == 'listing_reviews':
                    listing_review.append(data_point)
                elif row['entity_type'] == 'producer_reviews':
                    producer_review.append(data_point)
                elif row['entity_type'] == 'venue_reviews':
                    venue_review.append(data_point)
            
            response = {
                "listing_review": final_result.get("listing_review", 0),
                "producer_review": final_result.get("producer_review", 0),
                "venue_review": final_result.get("venue_review", 0),
                "total_listings": final_result.get("total_listings", 0),
                "total_clubs": final_result.get("total_clubs", 0),
                "lr_counts": listing_review,
                "pr_counts": producer_review,
                "vr_counts": venue_review
            }

        return jsonify(response), 200
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# [GET] Admin dashboard business claimed status 
@blueprint.route("/getClaimStats", methods=['GET'])
def getClaimStats():
    conn = g.db
    
    # Get the date parameters from query string
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')

    # Convert ISO dates to date strings for better compatibility
    from datetime import datetime
    if start_date and end_date:
        start_date_obj = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        end_date_obj = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        
        start_date_str = start_date_obj.strftime('%Y-%m-%d')
        end_date_str = end_date_obj.strftime('%Y-%m-%d')
    else:
        return jsonify({"error": "startDate and endDate parameters are required"}), 400
    
    try: 
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            # Get total reviews count
            total_sql = """
                SELECT 
                    'Total Signups' as category,
                    (
                        COALESCE((SELECT COUNT(*) FROM "venues" 
                                WHERE "claimStatusCheckDate" IS NOT NULL
                                AND DATE("claimStatusCheckDate") BETWEEN %s AND %s), 0) +
                        COALESCE((SELECT COUNT(*) FROM "producers" 
                                WHERE "claimStatusCheckDate" IS NOT NULL
                                AND DATE("claimStatusCheckDate") BETWEEN %s AND %s), 0)
                    ) as "total_count";
            """
            cursor.execute(total_sql, (start_date_str, end_date_str, start_date_str, 
                                       end_date_str))
            total_result = cursor.fetchone()
            total_signups = total_result['total_count'] if total_result else 0
            
            # Get daily signup data with cumulative counts and fill missing dates with 0
            sql = """
                WITH baseline_counts AS (                    
                    SELECT 
                        'venues' as entity_type,
                        COUNT(*) as baseline_count
                    FROM "venues"
                    WHERE "claimStatusCheckDate" IS NOT NULL
                    AND DATE("claimStatusCheckDate") < %s
                    
                    UNION ALL
                    
                    SELECT 
                        'producers' as entity_type,
                        COUNT(*) as baseline_count
                    FROM "producers"
                    WHERE "claimStatusCheckDate" IS NOT NULL
                    AND DATE("claimStatusCheckDate") < %s
                ),
                daily_signups AS (
                    SELECT
                        DATE("claimStatusCheckDate") as signup_date,
                        'venues' as entity_type,
                        COUNT(*) as daily_count
                    FROM "venues"
                    WHERE "claimStatusCheckDate" IS NOT NULL
                    AND DATE("claimStatusCheckDate") BETWEEN %s AND %s
                    GROUP BY DATE("claimStatusCheckDate")

                    UNION ALL

                    SELECT
                        DATE("claimStatusCheckDate") as signup_date,
                        'producers' as entity_type,
                        COUNT(*) as daily_count
                    FROM "producers"
                    WHERE "claimStatusCheckDate" IS NOT NULL
                    AND DATE("claimStatusCheckDate") BETWEEN %s AND %s
                    GROUP BY DATE("claimStatusCheckDate")
                ),
                all_dates AS (
                    SELECT generate_series(
                        %s::date,
                        %s::date,
                        '1 day'::interval
                    )::date as signup_date
                ),
                entity_types AS (
                    SELECT unnest(ARRAY['venues', 'producers']) as entity_type
                ),
                complete_data AS (
                    SELECT
                        ad.signup_date,
                        et.entity_type,
                        COALESCE(ds.daily_count, 0) as daily_count
                    FROM all_dates ad
                    CROSS JOIN entity_types et
                    LEFT JOIN daily_signups ds ON ad.signup_date = ds.signup_date
                                              AND et.entity_type = ds.entity_type
                )
                SELECT
                    signup_date,
                    cd.entity_type, 
                    daily_count,
                    SUM(daily_count) OVER (
                        PARTITION BY cd.entity_type 
                        ORDER BY signup_date
                        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                    ) + COALESCE(bc.baseline_count, 0) as cumulative_count
                FROM complete_data cd
                LEFT JOIN baseline_counts bc ON cd.entity_type = bc.entity_type
                ORDER BY signup_date DESC, cd.entity_type;
            """
            cursor.execute(sql, (start_date_str, start_date_str, 
                                 start_date_str, end_date_str, start_date_str, 
                                 end_date_str, start_date_str, end_date_str))
            all_data = cursor.fetchall()
            
            # Process data by entity type
            users_data = []
            venues_data = []
            producers_data = []
            
            for row in all_data:
                data_point = {
                    "date": str(row['signup_date']), 
                    "count": row['daily_count'],
                    "cumulative_count": row['cumulative_count']
                }
                
                if row['entity_type'] == 'users':
                    users_data.append(data_point)
                elif row['entity_type'] == 'venues':
                    venues_data.append(data_point)
                elif row['entity_type'] == 'producers':
                    producers_data.append(data_point)
            
            business_data = {
                "total_signups": total_signups,
                "producers": producers_data,
                "venues": venues_data
            }
            
            return jsonify(business_data)
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@blueprint.route("/getFutureEventsCount", methods=['GET'])
def getFutureEventsCount():
    conn = g.db
    
    # Get the date parameters from query string
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')

    # Convert ISO dates to date strings for better compatibility
    from datetime import datetime
    if start_date and end_date:
        start_date_obj = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        end_date_obj = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        
        start_date_str = start_date_obj.strftime('%Y-%m-%d')
        end_date_str = end_date_obj.strftime('%Y-%m-%d')
    else:
        return jsonify({"error": "startDate and endDate parameters are required"}), 400
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            count_sql = """
                SELECT 
                    (SELECT COUNT(*)
                        FROM "events" 
                        WHERE DATE("eventStartDate") BETWEEN %s AND %s
                    ) as active_events_count, 
                    (SELECT COUNT(*) FROM "events" WHERE DATE("createdDate") BETWEEN %s AND %s
                    ) as all_events_count
            """
            cursor.execute(count_sql, (
                start_date_str, end_date_str,  # venues date range
                start_date_str, end_date_str   # producers date range
            ))
            result = cursor.fetchone() or {}
            
            # Format the result as requested (numeric values)
            final_result = {
                'active_events_count': result.get('active_events_count', 0),
                'all_events_count': result.get('all_events_count', 0)
            }

            return jsonify(final_result), 200
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


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
@blueprint.route("/getReviewByTarget/<id>/<last_review_id>")
def getReviewByTarget(id, last_review_id):
    conn = g.db
    cursor = conn.cursor()
    
    try:

        if last_review_id == "0":
            # If last_review_id is 0, fetch the latest 20 reviews for the target
            cursor.execute("""
                SELECT "reviews".*, "reviewsUserVotes"."upvotes", "reviewsUserVotes"."downvotes"
                FROM "reviews"
                LEFT JOIN "reviewsUserVotes" ON "reviews"."id" = "reviewsUserVotes"."reviewId"
                WHERE "reviews"."reviewTarget" = %s
                ORDER BY "reviews"."id" DESC
                LIMIT 20
            """, (id,))
        else:
            cursor.execute("""
                SELECT "reviews".*, "reviewsUserVotes"."upvotes", "reviewsUserVotes"."downvotes"
                FROM "reviews"
                LEFT JOIN "reviewsUserVotes" ON "reviews"."id" = "reviewsUserVotes"."reviewId"
                WHERE "reviews"."reviewTarget" = %s
                AND "reviews"."id" < %s
                ORDER BY "reviews"."id" DESC
                LIMIT 20
            """, (id, last_review_id))

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

    except Exception as e:
        print(f"Error fetching reviews by target {id}: {str(e)}")
        return jsonify({
            "code": 500,
            "message": "An error occurred while fetching reviews."
        }), 500


# [GET] Latest 10 Specific Reviews by usr(s) - using one or more user IDs (retrieve latest reviews for the specified user(s) as well as the review target(s) data)
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
                SELECT "reviewDesc", "rating", "reviewTarget", "createdDate", "userID", "photo"
                FROM "reviews"
                WHERE "userID" IN ({placeholders})
                ORDER BY "createdDate" DESC
                LIMIT 10
            )
            SELECT "reviewDesc", "rating", "reviewTarget", "createdDate", "userID", "photo"
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
            SELECT "id", "displayName"
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


# [GET] Get average rating for a specific listing based on reviews
@blueprint.route("/getListingReviewsRating/<listing_id>")
def getListingReviewsRating(listing_id):
    conn = g.db
    cursor = conn.cursor()

    if listing_id is None:
        return jsonify({
            "code": 400,
            "message": "Listing ID is required."
        }), 400

    try:
        # Fetch the average rating for the listing
        cursor.execute("""
            SELECT AVG("rating") AS "averageRating"
            FROM "reviews"
            WHERE "reviewTarget" = %s AND "reviewType" = 'Listing'
        """, (listing_id,))

        avg_rating = cursor.fetchone()

        if avg_rating is None or avg_rating['averageRating'] is None:
            return jsonify({
                "code": 200,
                "averageRating": "-",
                "reviewCount": 0
            }), 200
        
        # Fetch the number of reviews for the listing
        cursor.execute("""
            SELECT COUNT(*) AS "reviewCount"
            FROM "reviews"
            WHERE "reviewTarget" = %s AND "reviewType" = 'Listing'
        """, (listing_id,))
        review_count = cursor.fetchone()

        return jsonify({
            "code": 200,
            "averageRating": round(avg_rating['averageRating'], 1),
            "reviewCount": review_count['reviewCount'] or 0
        }), 200
    
    except Exception as e:
        print(f"Error fetching average rating for listing {listing_id}: {str(e)}")
        return jsonify({
            "code": 500,
            "message": "An error occurred while fetching the average rating."
        }), 500


# [GET] Get top 5 listings reviews by count
@blueprint.route("/getTop5MostReviewedListings")
def getTop5MostReviewedListings():
    conn = g.db
    cursor = conn.cursor()

    try:
        # Fetch the top 5 most reviewed listings
        cursor.execute("""
            SELECT "reviewTarget", COUNT(*) AS "reviewCount"
            FROM "reviews"
            WHERE "reviewType" = 'Listing'
            GROUP BY "reviewTarget"
            ORDER BY "reviewCount" DESC
            LIMIT 5
        """)

        top_listings = cursor.fetchall()

        if not top_listings:
            return jsonify([]), 200

        # Loop through the top listings to get their details (average rating, producer name, listing name)
        for listing in top_listings:
            listing_id = listing['reviewTarget']

            # Get the average rating for the listing
            cursor.execute("""
                SELECT AVG("rating") AS "averageRating"
                FROM "reviews"
                WHERE "reviewTarget" = %s AND "reviewType" = 'Listing'
            """, (listing_id,))
            avg_rating = cursor.fetchone()['averageRating']

            if avg_rating is not None:
                listing['rating'] = round(avg_rating, 1)
            else:
                listing['rating'] = '-'

            # Get the producer ID for the listing
            cursor.execute('SELECT "producerID", "listingName", "drinkType" FROM "listings" WHERE "id" = %s', (listing_id,))
            listing_details = cursor.fetchone()
            listing['listingName'] = listing_details['listingName'] if listing_details else 'Unknown Listing'
            listing['producerID'] = listing_details['producerID'] if listing_details else None
            listing['drinkType'] = listing_details['drinkType'] if listing_details else 'Unknown Drink Type'

            # Get the producer name for the listing
            cursor.execute('SELECT "producerName" FROM "producers" WHERE "id" = %s', (listing_details['producerID'],))
            producer_name = cursor.fetchone()
            listing['producerName'] = producer_name['producerName'] if producer_name else 'Unknown Producer'

        return jsonify(top_listings), 200
    
    except Exception as e:
        print(f"Error fetching top 5 most reviewed listings: {str(e)}")
        return jsonify({
            "code": 500,
            "message": "An error occurred while fetching the top listings."
        }), 500
    
    finally:
        cursor.close()

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
@blueprint.route("/getVenueReviewsByVenueId/<id>/<lastReviewID>", methods=['GET'])
def getVenueReviewsByVenueId(id, lastReviewID):
    conn = g.db

    with conn.cursor() as cursor:
        if lastReviewID == "0":
            # If lastReviewID is 0, fetch the latest 20 reviews for the venue
            cursor.execute("""
                SELECT "venueReviews".*, "venueReviewsUserVotes"."upvotes", "venueReviewsUserVotes"."downvotes"
                FROM "venueReviews"
                LEFT JOIN "venueReviewsUserVotes" ON "venueReviews"."id" = "venueReviewsUserVotes"."reviewId"
                WHERE "venueReviews"."venueID" = %s
                ORDER BY "venueReviews"."id" DESC
                LIMIT 20
            """, (id,))
        else:
            cursor.execute("""
                SELECT "venueReviews".*, "venueReviewsUserVotes"."upvotes", "venueReviewsUserVotes"."downvotes"
                FROM "venueReviews"
                LEFT JOIN "venueReviewsUserVotes" ON "venueReviews"."id" = "venueReviewsUserVotes"."reviewId"
                WHERE "venueReviews"."venueID" = %s
                AND "venueReviews"."id" < %s
                ORDER BY "venueReviews"."id" DESC
                LIMIT 20
            """, (id, lastReviewID))

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

@blueprint.route("/getBottleReviewsByVenueId/<id>", methods=['GET'])
def getBottleReviewsByVenueId(id):
    conn = g.db

    with conn.cursor() as cursor:
        # Get bottle reviews where the location field matches the venue ID
        cursor.execute("""
            SELECT "reviews".*, "reviewsUserVotes"."upvotes", "reviewsUserVotes"."downvotes"
            FROM "reviews"
            LEFT JOIN "reviewsUserVotes" ON "reviews"."id" = "reviewsUserVotes"."reviewId"
            WHERE "reviews"."location" = %s
            AND "reviews"."photo" IS NOT NULL
            AND "reviews"."photo" != ''
            ORDER BY "reviews"."createdDate" DESC
        """, (id,))

        reviews_data = cursor.fetchall()

        if not reviews_data:
            return jsonify([])
        
        # Format the user votes data similar to venue reviews
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

# [GET] Home reviews - reviews where location IS NULL (Home tastings)
@blueprint.route("/getHomeReviews", methods=['GET'])
def getHomeReviews():
    conn = g.db
    
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT r.*, u.username, u.photo as "userPhoto", l."listingName"
                FROM reviews r
                JOIN users u ON r."userID" = u.id
                JOIN listings l ON r."reviewTarget" = l.id
                WHERE r.location IS NULL AND r.address = 'home'  -- Home reviews
                ORDER BY r."createdDate" DESC
            """)
            
            reviews_data = cursor.fetchall()
            
            if not reviews_data:
                return jsonify([])
            
            # Process user votes for each review
            for review in reviews_data:
                review["userVotes"] = {
                    "upvotes": review.get("upvotes", []) if review.get("upvotes") else [],
                    "downvotes": review.get("downvotes", []) if review.get("downvotes") else []
                }
                # Clean up if these fields exist
                if "upvotes" in review:
                    del review["upvotes"]
                if "downvotes" in review:
                    del review["downvotes"]
            
            return jsonify(reviews_data)
            
    except Exception as e:
        print(str(e))
        return jsonify({
            "code": 500,
            "message": "An error occurred retrieving home reviews."
        }), 500


# [GET] Venue information where their menu contains a specific drink/listing
@blueprint.route("/getVenuesWithSpecificListing/<listingID>", methods=['GET'])
def getVenuesWithSpecificListing(listingID):
    conn = g.db

    try:
        listingID = int(listingID)  # ensure it's an integer

        with conn.cursor() as cursor:
            # Single optimized query with JOIN and LIMIT
            cursor.execute("""
                SELECT v."id", v."venueName", v."originLocation", v."photo", v."website", v."address", 
                    COALESCE((
                        SELECT json_agg(DISTINCT mi2."variant" ORDER BY mi2."variant")
                        FROM "menuItems" mi2
                        JOIN "venuesMenu" vm2 ON mi2."sectionId" = vm2.id
                        WHERE vm2."venueId" = v.id 
                            AND mi2."itemID" = %s 
                            AND mi2."variant" IS NOT NULL
                    ), '[]'::json) AS vintages
                FROM "menuItems" mi
                JOIN "venuesMenu" vm ON mi."sectionId" = vm."id"
                JOIN "venues" v ON vm."venueId" = v."id"
                WHERE mi."itemID" = %s
                GROUP BY v."id", v."venueName", v."originLocation", v."photo", v."website", v."address"
                LIMIT 3;
            """, (listingID, listingID,))

            venues_data = cursor.fetchall()

            # if not venues_data:
            #     return jsonify({
            #         "code": 404,
            #         "message": "No venue data found for the specified listing."
            #     }), 404

            if not venues_data:
                return jsonify([]), 200
            
            # Convert to list of dictionaries (if not already done by cursor)
            result = []
            for venue in venues_data:
                result.append({
                    "id": venue["id"],
                    "venueName": venue["venueName"],
                    "originLocation": venue["originLocation"],
                    "photo": venue["photo"],
                    "website": venue["website"],
                    "address": venue["address"],
                    "vintages": venue["vintages"]
                })

            return jsonify(result), 200

    except ValueError:
        return jsonify({
            "code": 400,
            "message": "Invalid listing ID. Must be a valid integer."
        }), 400
    except Exception as e:
        print(str(e))
        return jsonify({
            "code": 500,
            "message": "An error occurred while fetching venues with the specified listing.",
            "error": str(e)
        }), 500


# [GET] Get all listings names test
@blueprint.route('/venue-listings', methods=['GET'])
def get_venue_listings():
    conn = g.db
    """Get venue listings with search functionality"""
    try:
        # Get query parameters
        query = request.args.get('q', '').strip()
        limit = int(request.args.get('limit', 3))

        # Validate query
        if not query:
            return jsonify([])
        
        # Optimized query using trigram index for fuzzy string matching
        sql = """
            SELECT "id", "venueName", "originLocation", "address",
                similarity(unaccent("venueName"), unaccent(%s)) as sim_score
            FROM venues
            WHERE unaccent("venueName") %% unaccent(%s)
            ORDER BY sim_score DESC
            LIMIT %s;
        """

        with conn.cursor() as cursor:
            cursor.execute(sql, (query, query, limit))
            rows = cursor.fetchall()

        # if nothing was found
        if not rows:
            return jsonify([]), 200

        result = [
            {
                "id": row["id"], 
                "venueName": row["venueName"], 
                "originLocation": row["originLocation"],
                "address": row["address"]
            } 
            for row in rows
        ]

        return jsonify(result), 200
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        # print("something went wrong" + str(e), flush=True)
        return jsonify({"error": str(e)}), 500

# [GET] Get venues by search term
@blueprint.route("/getVenuesBySearch", methods=['GET'])
def getVenuesBySearch():
    searchTerm = request.args.get('searchTerm', '').strip()
    lastID = request.args.get('lastID', '0')
    lastID = int(lastID) if lastID.isdigit() else 0
    conn = g.db

    try:
        with conn.cursor() as cursor:
            
            # Search for venues by name or origin location
            cursor.execute("""
                SELECT "id", "venueName", "address", "venueType", "originLocation", "photo", "username", "website"
                FROM "venues"
                WHERE ("venueName" ILIKE %s OR "originLocation" ILIKE %s)
                AND "id" > %s
                ORDER BY "id" ASC
                LIMIT 30
            """, (f'%{searchTerm}%', f'%{searchTerm}%', lastID))
            venues_data = cursor.fetchall()

            if not venues_data:
                return jsonify([])
            
            # Loop through all the venues and get their average rating 
            for venue in venues_data:
                cursor.execute("""
                    SELECT AVG("rating") AS avg_rating
                    FROM "venueReviews"
                    WHERE "venueID" = %s
                """, (venue["id"],))
                avg_rating = cursor.fetchone()

                if avg_rating and avg_rating["avg_rating"] is not None:
                    venue["averageRating"] = round(avg_rating["avg_rating"], 1)
                else:
                    venue["averageRating"] = '-'
            
            return jsonify(venues_data), 200
    except Exception as e:
        print(str(e))
        return jsonify({
            "code": 500,
            "message": "An error occurred while fetching venues by search term.",
            "error": str(e)
        }), 500

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
                user_data["producerLists"] = fetch_producer_lists(cursor, user_id)
                user_data["venueLists"] = fetch_venue_lists(cursor, id)
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
            user_data["producerLists"] = fetch_producer_lists(cursor, user_id)
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
    
    sql = """ 
        SELECT "id", "username", "displayName", "choiceDrinks", "modType", "photo", 
        "joinDate", "firstName", "lastName", "isAdmin", "birthday", "choiceFlavours",
        "preferences", "grails", "upAndComing", "goats", "blueDot", "ambassador", "categoryExpert"
        FROM "users"
        WHERE "id" = %s
    """  

    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, (id, ))
            user_data = cursor.fetchone()

            if not user_data:
                return jsonify({}), 404

            user_data["drinkLists"] = fetch_drink_lists(cursor, id)
            user_data["producerLists"] = fetch_producer_lists(cursor, id)
            user_data["venueLists"] = fetch_venue_lists(cursor, id)
            user_data["followLists"] = fetch_follow_lists(cursor, id)
            user_data['proofRank'] = pointsHelperFunc.get_rank_by_user_id(id)
            user_data['currentPoints'] = pointsHelperFunc.get_current_proof_points(id)

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
            user_data["producerLists"] = fetch_producer_lists(cursor, user_id) 
            user_data["venueLists"] = fetch_venue_lists(cursor, id)
            user_data["followLists"] = fetch_follow_lists(cursor, user_id)

        return jsonify(user_data), 200

    except Exception as e:
        print(str(e))
        return jsonify({"code": 500, "message": "An error occurred while fetching the user."}), 500

# [GET] Get username from email address
@blueprint.route("/getUsernameFromEmail/<email>")
def getUsernameFromEmail(email):
    conn = g.db
    
    try:
        with conn.cursor() as cursor:
            # First, check in users table
            cursor.execute('SELECT "username" FROM "users" WHERE LOWER(REPLACE("email", \' \', \'\')) = LOWER(REPLACE(%s, \' \', \'\'))', (email,))
            user_data = cursor.fetchone()
            
            if user_data:
                return jsonify({"username": user_data["username"]}), 200
            
            # If not found in users, check in accountRequests table
            cursor.execute('SELECT "businessId", "businessType" FROM "accountRequests" WHERE LOWER(REPLACE("email", \' \', \'\')) = LOWER(REPLACE(%s, \' \', \'\'))', (email,))
            account_request = cursor.fetchone()
            
            if account_request:
                business_id = account_request["businessId"]
                business_type = account_request["businessType"]
                
                if business_type == "producer":
                    cursor.execute('SELECT "username" FROM "producers" WHERE "id" = %s', (business_id,))
                    producer_data = cursor.fetchone()
                    if producer_data:
                        return jsonify({"username": producer_data["username"]}), 200
                        
                elif business_type == "venue":
                    cursor.execute('SELECT "username" FROM "venues" WHERE "id" = %s', (business_id,))
                    venue_data = cursor.fetchone()
                    if venue_data:
                        return jsonify({"username": venue_data["username"]}), 200
            
            # No account found with this email
            return jsonify({"username": None}), 404

    except Exception as e:
        print(str(e))
        return jsonify({"code": 500, "message": "An error occurred while fetching username from email."}), 500

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


# [GET] Get venues by IDs
@blueprint.route("/getVenuesByIds", methods=['POST'])
def getVenuesByIds():
    conn = g.db
    venue_ids = request.json.get('venueIDs', [])

    if not venue_ids or len(venue_ids) == 0:
        return jsonify({
            "code": 404,
            "message": "At least one venue ID is required."
        }), 404

    try:
        with conn.cursor() as cursor:
            # Retrieve venue information based on the provided IDs
            cursor.execute('SELECT * FROM "venues" WHERE "id" IN %s', (tuple(venue_ids),))
            venues_data = cursor.fetchall()

            if not venues_data:
                return jsonify([]), 404
            
            venues_list = []
            for row in venues_data:
                venue = {
                "id": row["id"],
                "venueName": row["venueName"],
                "originLocation": row["originLocation"],
                "photo": row["photo"],
                "website": row["website"],
                "address": row["address"]
                }
                venues_list.append(venue)

        return jsonify(venues_list), 200

    except Exception as e:
        print(str(e))
        return jsonify({"code": 500, "message": "An error occurred while fetching venues by IDs."}), 500

# [GET] Specific Venue
@blueprint.route("/venue/<id>")
def venue(id):
    conn = g.db
    cur = conn.cursor()

    try:
        # Query to get a specific venue and related data
        query = """
            SELECT 
                v.id, v.address, v."claimStatus", v."venueName", v."venueDesc", 
                v."originLocation", v.photo, v."publicHolidays", v."reservationDetails", v."claimStatusCheckDate",
                v."yearOpened", v."openForReservations", v.website, v.instagram, v.facebook, v.tiktok, 
                v.email, v."phoneNumber", v."whatsappNumber",
                v.username, v."venueType", 
                -- Build the menu JSON
                COALESCE((
                    SELECT json_agg(json_build_object(
                        'id', vm.id,
                        'sectionName', vm."sectionName",
                        'sectionOrder', vm."sectionOrder"
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


# [GET] Specific Venue
@blueprint.route("/getVenueMenu/<section_id>")
def getVenueMenu(section_id):
    """Optimized version with performance improvements and better error handling"""
    
    # Input validation
    if not section_id:
        return jsonify({"code": 400, "message": "Menu category is mandatory."}), 400
    
    # Parse and validate query parameters
    try:
        page = max(1, int(request.args.get("page", 1)))
        limit = min(100, max(1, int(request.args.get("limit", 20))))  # Cap at 100
        search = request.args.get("search", "").strip()
    except ValueError:
        return jsonify({"code": 400, "message": "Invalid pagination parameters"}), 400
    
    offset = (page - 1) * limit
    
    conn = g.db
    cur = conn.cursor()
    
    try:
        # Build WHERE conditions (use proper parameterization)
        where_conditions = ['"sectionId" = %s']
        params = [section_id]
        
        if search:
            # Search across multiple fields for better UX
            where_conditions.append('(LOWER(mi."variant") LIKE %s OR LOWER(mi."itemID") LIKE %s)')
            search_param = f"%{search.lower()}%"
            params.extend([search_param, search_param])
        
        where_clause = " AND ".join(where_conditions)
        
        # Use a single query with window function for better performance
        # This eliminates the need for a separate COUNT query
        sql = f"""
            SELECT 
                mi."id", mi."sectionId", mi."itemID", mi."itemOrder", lst."listingName", lst."photo", 
                lst."bottler", lst."drinkType", lst."abv", mi."itemPrice", mi."itemAvailability", 
                srvTyp."servingType", mi."variant", COUNT(*) OVER() as total_count
            FROM "menuItems" mi
            INNER JOIN "listings" lst
                ON mi."itemID" = lst."id"
            LEFT JOIN "servingTypes" srvTyp
                ON mi."itemServingType" = srvTyp."id"
            WHERE {where_clause}
            ORDER BY mi."itemOrder" ASC -- , mi."id" ASC  Add secondary sort for consistency
            LIMIT %s OFFSET %s;
        """
        
        cur.execute(sql, params + [limit, offset])
        rows = cur.fetchall()
        
        if not rows:
            total_items = 0
            menu_items = []
        else:
            # Get total count from the window function (access by key since using RealDictRow)
            # "description": row['officialDesc'],
            total_items = rows[0]['total_count']
            menu_items = [
                {
                    "id": row['id'],
                    "sectionId": row['sectionId'], 
                    "itemID": row['itemID'],
                    "itemOrder": row['itemOrder'],
                    "name": row['listingName'],
                    "photo": row['photo'],
                    "bottler": row['bottler'], 
                    "drinkType": row['drinkType'],
                    "abv": row['abv'],
                    "itemAvailability": row['itemAvailability'],
                    "variant": row['variant'],
                    "servingType": row['servingType'],
                    "itemPrice": float(row['itemPrice']) if row['itemPrice'] is not None else None,
                }
                for row in rows
            ]
        
        # Calculate pagination info
        total_pages = (total_items + limit - 1) // limit
        has_next = page < total_pages
        has_prev = page > 1
        
        return jsonify({
            "code": 200,
            "data": menu_items,
            "pagination": {
                "page": page,
                "limit": limit,
                "total_items": total_items,
                "total_pages": total_pages,
                "has_next": has_next,
                "has_prev": has_prev
            }
        }), 200
        
    except Exception as e:
        # # Log the actual error for debugging
        # import logging
        # logging.error(f"Database error in get_menu_items: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Return generic error to client
        return jsonify({
            "code": 500,
            "message": "An error occurred retrieving menu items."
        }), 500
        
    finally:
        if cur:
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
                v.id, v.address, v."claimStatus", v."venueName", v."venueDesc", 
                v."originLocation", v.photo, v."publicHolidays", v."reservationDetails", v."claimStatusCheckDate",
                v."yearOpened", v."openForReservations", v.website, v.instagram, v.facebook, v.tiktok, 
                v.email, v."phoneNumber", v."whatsappNumber",
                v.username, v."venueType", v."stripeCustomerId", v.pin,
                -- Build amenities JSON
                COALESCE((
                    SELECT row_to_json(va)
                    FROM "venueAmenities" va
                    WHERE va."venueId" = v.id
                ), '{}'::json) AS amenities,
                -- Build the menu JSON
                COALESCE((
                    SELECT json_agg(json_build_object(
                        'sectionOrder', vm."sectionOrder",
                        'sectionName', vm."sectionName",
                        'sectionId', vm.id,
                        'sectionMenu', COALESCE((
                            SELECT json_agg(json_build_object(
                                'itemOrder', mi."itemOrder",
                                'itemVintage', mi."variant",
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
        venue['amenities'] = venue['amenities'] if venue['amenities'] else {}

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


# -----------------------------------------------------------------------------------------
# [GET] Get request listings filtered by role and id
@blueprint.route("/getRequestListingsByRole/<role>/<id>")
def getRequestListingsByRole(role, id):
    conn = g.db
    cursor = conn.cursor()

    try:
        # Convert id to integer
        id = int(id)

        # Step 1: Check if user is a producer 
        if role == 'producer':

            # Check if the producer exists
            cursor.execute("""
                SELECT * FROM "producers" WHERE "id" = %s
            """, (id,))
            producer_data = cursor.fetchone()

            if producer_data is None:
                return jsonify({
                    "code": 404,
                    "message": "Producer not found."
                }), 404

            cursor.execute("""
                SELECT * FROM "requestListings"
                WHERE "producerID" = %s AND "reviewStatus" = false
            """, (id,))

            request_listings_data = cursor.fetchall()

        elif role == 'user':

            # Get the isAdmin status of the user and modType
            cursor.execute("""
                SELECT "isAdmin", "modType" FROM "users" WHERE "id" = %s
            """, (id,))
            user_data = cursor.fetchone()

            if user_data is None:
                return jsonify({
                    "code": 404,
                    "message": "User not found."
                }), 404

            if user_data['isAdmin']: 
                cursor.execute("""
                    SELECT * FROM "requestListings"
                    WHERE "reviewStatus" = false
                """)
                request_listings_data = cursor.fetchall()
            
            else:
                mod_type = user_data['modType']
                if mod_type:
                    placeholders = ','.join(['%s'] * len(mod_type))  # -> "%s, %s"
                    query = f"""
                        SELECT * FROM "requestListings"
                        WHERE "reviewStatus" = false AND (
                            "userID" = %s OR "drinkType" IN ({placeholders})
                        )
                    """
                    params = [id] + mod_type
                    cursor.execute(query, params)
                else:
                    # No mod types: filter only by userID
                    cursor.execute("""
                        SELECT * FROM "requestListings"
                        WHERE "reviewStatus" = false AND "userID" = %s
                    """, (id,))

                request_listings_data = cursor.fetchall()

        else:
            return jsonify({
                "code": 400,
                "message": "Invalid role specified."
            }), 400
                
        if not request_listings_data:
            return jsonify([])
        
        # Loop through the request Listings
        for request_listing in request_listings_data:

            # Get producer name 
            producer_id = request_listing['producerID']

            if producer_id is None or producer_id == '':
                request_listing['producerName'] = request_listing['producerNew']
            else:
                cursor.execute("""
                    SELECT "producerName" FROM "producers" WHERE "id" = %s
                """, (producer_id,))
                producer_name_data = cursor.fetchone()

                if producer_name_data:
                    request_listing['producerName'] = producer_name_data['producerName']
                else:
                    request_listing['producerName'] = "Unknown Producer"

            # Get requester username   
            requester_id = request_listing['userID']

            if requester_id is None or requester_id == '':
                request_listing['requesterUsername'] = '(Anonymous)'
            else:
                cursor.execute("""
                    SELECT "username" FROM "users" WHERE "id" = %s
                """, (requester_id,))
                requester_username_data = cursor.fetchone()

                if requester_username_data:
                    request_listing['requesterUsername'] = requester_username_data['username']
                else:
                    request_listing['requesterUsername'] = '(Anonymous)'

        return jsonify(request_listings_data), 200

    except Exception as e:
        print(str(e))
        return jsonify({
            "code": 500,
            "message": "An error occurred while fetching request listings by role and isAdmin status."
        }), 500


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


# -----------------------------------------------------------------------------------------
# [GET] Get request edits filtered by role and id
@blueprint.route("/getRequestEditsByRole/<role>/<id>")
def getRequestEditsByRole(role, id):
    conn = g.db
    cursor = conn.cursor()
    print(f"==== getRequestEditsByRole called with role={role}, id={id} ====")


    # Return data arrays
    request_edits_data = []
    request_dups_data = []

    try:
        print(f"Converting ID {id} to integer")
        id = int(id)  # Ensure ID is an integer
        print(f"ID successfully converted to {id}")

        if role == 'producer':
            # Validate producer exists
            print(f"PRODUCER PATH: Validating producer with ID {id}")
            cursor.execute("""SELECT * FROM "producers" WHERE "id" = %s""", (id,))
            producer_data = cursor.fetchone()

            if producer_data is None:
                print(f"ERROR: Producer with ID {id} not found in database")
                return jsonify({"code": 404, "message": "Producer not found."}), 404

            print(f"Producer exists: {producer_data.get('producerName', 'Unknown name')}")

            # Fetch unreviewed edits for this producer
            print(f"Fetching unreviewed edits for producer {id}")
            cursor.execute("""
                SELECT * FROM "requestEdits"
                WHERE "producerID" = %s AND "reviewStatus" = false
            """, (id,))
            request_edits_raw = cursor.fetchall()
            print(f"Found {len(request_edits_raw) if request_edits_raw else 0} unreviewed edits")

        elif role == 'user':
            print(f"USER PATH: Fetching user info for ID {id}")

            # Fetch user info
            cursor.execute("""SELECT "isAdmin", "modType" FROM "users" WHERE "id" = %s""", (id,))
            user_data = cursor.fetchone()

            if user_data is None:
                print(f"ERROR: User with ID {id} not found in database")
                return jsonify({"code": 404, "message": "User not found."}), 404
            
            print(f"User exists: isAdmin={user_data['isAdmin']}, modType={user_data['modType']}")

            if user_data['isAdmin']:
                print("Admin user: fetching all unreviewed edits")
                # Admin gets all unreviewed edits
                cursor.execute("""SELECT * FROM "requestEdits" WHERE "reviewStatus" = false""")
                request_edits_raw = cursor.fetchall()
                print(f"Found {len(request_edits_raw) if request_edits_raw else 0} unreviewed edits for admin")

            else:
                # Standard user: fetch edits by user or by drinkType from modType
                print("Standard user: filtering by user or modType")
                mod_type = user_data['modType']
                if mod_type:
                    print(f"User has modType: {mod_type}")
                    placeholders = ','.join(['%s'] * len(mod_type))
                    query = f"""
                        SELECT re.*
                        FROM "requestEdits" re
                        JOIN "listings" l ON re."listingID" = l."id"
                        WHERE re."reviewStatus" = false AND (
                            re."userID" = %s OR l."drinkType" IN ({placeholders})
                        )
                    """
                    params = [id] + mod_type
                    print(f"Executing query with parameters: {params}")
                    cursor.execute(query, params)
                else:
                    print(f"User has no modType, only fetching own requests")
                    # No modType: only include own requests
                    cursor.execute("""
                        SELECT * FROM "requestEdits"
                        WHERE "reviewStatus" = false AND "userID" = %s
                    """, (id,))
                request_edits_raw = cursor.fetchall()
                print(f"Found {len(request_edits_raw) if request_edits_raw else 0} unreviewed edits for standard user")

        else:
            print(f"ERROR: Invalid role specified: {role}")
            return jsonify({"code": 400, "message": "Invalid role specified."}), 400

        if not request_edits_raw:
            print("No request edits found, returning empty arrays")
            return jsonify({"requestEdits": [], "requestDups": []}), 200

        # Enrich and split request data
        print(f"Beginning to enrich and split {len(request_edits_raw)} request edits")
        for request_edit in request_edits_raw:
            listing_id = request_edit['listingID']
            print(f"Edit has listingID: {listing_id}")

            if listing_id:
                print(f"Fetching data for listing ID {listing_id}")
                cursor.execute("""
                    SELECT "listingName", "photo", "producerID"
                    FROM "listings"
                    WHERE "id" = %s
                """, (listing_id,))
                listing_data = cursor.fetchone()

                if listing_data:
                    print(f"Found listing: {listing_data['listingName']}")
                    request_edit['listingName'] = listing_data['listingName']
                    request_edit['listingPhoto'] = listing_data['photo']
                    request_edit['producerID'] = listing_data['producerID']
                else:
                    print(f"WARNING: No listing found for ID {listing_id}")

            # Get producer name
            producer_id = request_edit.get('producerID')
            print(f"Edit has producerID: {producer_id}")
            if producer_id:
                print(f"Fetching data for producer ID {producer_id}")
                cursor.execute("""SELECT "producerName" FROM "producers" WHERE "id" = %s""", (producer_id,))
                producer_info = cursor.fetchone()
                
                request_edit['producerName'] = producer_info['producerName'] if producer_info else "Unknown Producer"
            else:
                print(f"WARNING: No producer found for ID {producer_id}")
                request_edit['producerName'] = "Unknown Producer"

            # Get requester username
            requester_id = request_edit.get('userID')
            print(f"Edit has userID: {requester_id}")
            if requester_id:
                print(f"Fetching username for user ID {requester_id}")
                cursor.execute("""SELECT "username" FROM "users" WHERE "id" = %s""", (requester_id,))
                requester_info = cursor.fetchone()
                request_edit['requesterUsername'] = requester_info['username'] if requester_info else '(Anonymous)'
            else:
                request_edit['requesterUsername'] = '(Anonymous)'

            # Sort into correct array
            if request_edit.get('duplicateLink'):
                request_dups_data.append(request_edit)
            else:
                request_edits_data.append(request_edit)

        return jsonify({
            "requestEdits": request_edits_data,
            "requestDups": request_dups_data
        }), 200

    except Exception as e:
        print("Error in getRequestEditsByRole:", str(e))
        print(f"TRACEBACK: {traceback.format_exc()}")
        return jsonify({
            "code": 500,
            "message": "An error occurred while fetching request edits by role."
        }), 500


# -----------------------------------------------------------------------------------------
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
# [GET] moreColours
@blueprint.route("/getMoreColours")
def getMoreColours():
    conn = g.db

    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM "moreColours"')
        more_colours_data = cursor.fetchall()

    if not more_colours_data:
        return jsonify([])

    return jsonify(more_colours_data)

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


# -----------------------------------------------------------------------------------------
# [GET] producersProfileViews by producerID
@blueprint.route("/getProducersProfileViewsByProducer/<id>")
def getProducersProfileViewsByProducer(id):
    conn = g.db
    cur = conn.cursor()

    try:
        cur.execute('SELECT * FROM "producersProfileViews" WHERE "producerId" = %s', (id,))
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


# -----------------------------------------------------------------------------------------
# [GET] Get best rated expressions for a producer
@blueprint.route("/getBestRatedExpressions/<producerID>")
def getBestRatedExpressions(producerID):
    conn = g.db
    cur = conn.cursor()

    bestRatedExpressions = []

    try:
        # Query to get best rated expressions for a producer
        query = """
            SELECT 
                l."listingName", 
                l."photo",
                l.id, 
                AVG(r."rating") AS "rating"
            FROM 
                "listings" l
            JOIN 
                "reviews" r ON l.id = r."reviewTarget"
            WHERE 
                l."producerID" = %s
            GROUP BY 
                l.id, l."listingName"
            ORDER BY 
                "rating" DESC
            LIMIT 5;
        """
        cur.execute(query, (producerID,))
        best_rated_expressions = cur.fetchall()

        # Loop through the best rated expressions to round ratings to 1 decimal place
        for expression in best_rated_expressions:
            expression['rating'] = round(expression['rating'], 1)
            bestRatedExpressions.append(expression)

        return jsonify(best_rated_expressions), 200
    
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred retrieving the best rated expressions."
            }
        ), 500
    
    finally:
        cur.close()


# -----------------------------------------------------------------------------------------
# [GET] Get most reviewed expressions for a producer
@blueprint.route("/getMostReviewedExpressions/<producerID>")
def getMostReviewedExpressions(producerID):
    conn = g.db
    cur = conn.cursor()

    mostReviewedExpressions = []

    try:
        # Query to get most reviewed expressions for a producer
        query = """
            SELECT 
                l."listingName",
                l."photo", 
                l.id, 
                COUNT(*) AS "reviewCount"
            FROM 
                listings l
            JOIN 
                reviews r ON l.id = r."reviewTarget"
            WHERE 
                l."producerID" = %s
            GROUP BY 
                l.id, l."listingName"
            ORDER BY 
                "reviewCount" DESC
            LIMIT 5;
        """
        cur.execute(query, (producerID,))
        most_reviewed_expressions = cur.fetchall()

        for expression in most_reviewed_expressions:
            mostReviewedExpressions.append(expression)

        return jsonify(mostReviewedExpressions), 200
    
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred retrieving the most reviewed expressions."
            }
        ), 500
    
    finally:
        cur.close()


# -----------------------------------------------------------------------------------------
# [GET] Get producer dashboard data
@blueprint.route("/getProducerDashBoardData/<producerID>")
def getProducerDashBoardData(producerID):
    conn = g.db
    cursor = conn.cursor()

    topCategories = []
    roundedRatingsCount = {}
    numReviewsSpread = {}

    try:
        # Get the top 5 most reviewed categories 
        cursor.execute("""
            SELECT l."drinkType", COUNT(r.*) as "count"
            FROM "listings" l
            JOIN "reviews" r ON l.id = r."reviewTarget"
            WHERE l."producerID" = %s
            GROUP BY l."drinkType"
            ORDER BY "count" DESC
            LIMIT 5
        """, (producerID,))
        top_categories_data = cursor.fetchall()

        for category in top_categories_data:
            # Category as key and count as value
            topCategories.append({ category['drinkType']: category['count'] })
    

        # Get rounded ratings and the corresponding count based on the reviews on listings by a specific producer
        cursor.execute("""
            SELECT ROUND(r."rating", 0) as "roundedRating", COUNT(*) as "count"
            FROM "reviews" r
            JOIN "listings" l ON r."reviewTarget" = l.id
            WHERE l."producerID" = %s
            GROUP BY "roundedRating"
        """, (producerID,))
        rounded_ratings_data = cursor.fetchall()

        for rating in rounded_ratings_data:
            # Rounded rating as key and count as value
            roundedRatingsCount[int(round(rating['roundedRating'], 0))] = rating['count']

        # Get the number of reviews spread by month
        cursor.execute("""
            SELECT DATE_TRUNC('month', r."createdDate") as "month", COUNT(*) as "count"
            FROM "reviews" r
            JOIN "listings" l ON r."reviewTarget" = l.id
            WHERE l."producerID" = %s
            GROUP BY "month"
            ORDER BY "month"
        """, (producerID,))
        num_reviews_spread_data = cursor.fetchall()

        for review in num_reviews_spread_data:
            # Month as key and count as value
            month_str = review['month'].strftime('%Y-%m')
            numReviewsSpread[month_str] = review['count']

        return jsonify({
            "topCategories": topCategories,
            "roundedRatingsCount": roundedRatingsCount,
            "numReviewsSpread": numReviewsSpread
        }), 200
    
    
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred retrieving the producer dashboard data."
            }
        ), 500
    finally:
        cursor.close()


# -----------------------------------------------------------------------------------------
# [GET] Get producer latest reviews from users on listings that are owned by the producer 
@blueprint.route("/getProducerLatestReviews/<producerID>")
def getProducerLatestReviews(producerID):
    conn = g.db
    cursor = conn.cursor()

    latestReviews = []

    try:
        # Query to get the latest reviews for listings owned by the producer
        query = """
            SELECT r.id, r."userID", l."listingName", l.id as "listingID", u."username", r."rating"
            FROM "reviews" r
            JOIN "listings" l ON r."reviewTarget" = l.id
            JOIN "users" u ON r."userID" = u.id
            WHERE l."producerID" = %s
            ORDER BY r."createdDate" DESC
            LIMIT 5
        """
        cursor.execute(query, (producerID,))
        latest_reviews_data = cursor.fetchall()

        for review in latest_reviews_data:
            latestReviews.append(review)

        return jsonify(latestReviews), 200
    
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred retrieving the producer's latest reviews."
            }
        ), 500
    
    finally:
        cursor.close()



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

        # Add query for users table
        cur.execute('SELECT "username" FROM "users"')
        user_usernames = cur.fetchall()

        cur.execute('SELECT "username" FROM "producers"')
        producer_usernames = cur.fetchall()

        cur.execute('SELECT "username" FROM "venues"')
        venue_usernames = cur.fetchall()

        # Combine and filter usernames
        usernames = (
            [username['username'] for username in user_usernames] +
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
# [GET] Get all the IDs for all the 3 user types whom the user is following
@blueprint.route("/getAllUserFollowingsIDs/<id>")
def getAllUserFollowingsIDs(id):
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
        cur.execute('SELECT "users", "producers", "venues" FROM "usersFollowLists" WHERE "userId" = %s', (id,))
        follow_list = fetch_follow_lists(cur, id)

        return jsonify({
            'users': follow_list['users'],
            'producers': follow_list['producers'],
            'venues': follow_list['venues']
        }), 200

    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred retrieving the followings IDs."
            }
        ), 500
    
    finally:
        cur.close()

# -----------------------------------------------------------------------------------------
# [GET] Get user dashboard data
# Data includes: 
#   - top 5 best rated listings
#   - top 5 best rated category
#   - top 5 venues where the user left the most reviews (checks the location column in the reviews table)
#   - top 5 producers where the user left the most reviews (checks the producerId column in the reviews table)
#   - top 5 drink styles which the user left the most reviews (drink styles)
#   - total number of reviews the user has made
#   - total number of followers the user has
@blueprint.route("/getUserDashBoardData/<id>")
def getUserDashBoardData(id):
    conn = g.db

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            # Single query to get all dashboard data at once
            cursor.execute("""
                WITH user_check AS (
                    SELECT 1 as exists FROM "users" WHERE "id" = %s
                ),
                user_reviews AS (
                    SELECT 
                        r."id" as review_id,
                        r."reviewTarget",
                        r."rating",
                        r."location",
                        l."listingName",
                        l."photo",
                        l."drinkType",
                        l."drinkStyle",
                        l."producerID",
                        p."producerName",
                        v."venueName"
                    FROM "reviews" r
                    JOIN "listings" l ON r."reviewTarget" = l."id"
                    LEFT JOIN "producers" p ON l."producerID" = p."id"
                    LEFT JOIN "venues" v ON r."location" = v."id"
                    WHERE r."userID" = %s
                    AND r."reviewType" = 'Listing'
                ),
                top_listings AS (
                    SELECT 
                        "reviewTarget" as id,
                        "rating",
                        "listingName",
                        "photo",
                        ROW_NUMBER() OVER (ORDER BY "rating" DESC) as rn
                    FROM user_reviews
                    WHERE "rating" IS NOT NULL
                    ORDER BY "rating" DESC
                    LIMIT 5
                ),
                top_categories AS (
                    SELECT 
                        "drinkType",
                        COUNT(*) as "reviewCount"
                    FROM user_reviews
                    WHERE "drinkType" IS NOT NULL
                    GROUP BY "drinkType"
                    ORDER BY "reviewCount" DESC
                    LIMIT 5
                ),
                top_venues AS (
                    SELECT 
                        "location" as "venueId",
                        "venueName",
                        COUNT(*) as "reviewCount"
                    FROM user_reviews
                    WHERE "location" IS NOT NULL
                    GROUP BY "location", "venueName"
                    ORDER BY "reviewCount" DESC
                    LIMIT 5
                ),
                top_producers AS (
                    SELECT 
                        "producerID" as "producerId",
                        "producerName",
                        COUNT(*) as "reviewCount"
                    FROM user_reviews
                    WHERE "producerID" IS NOT NULL
                    GROUP BY "producerID", "producerName"
                    ORDER BY "reviewCount" DESC
                    LIMIT 5
                ),
                top_drink_styles AS (
                    SELECT 
                        "drinkStyle",
                        COUNT(*) as "reviewCount"
                    FROM user_reviews
                    WHERE "drinkStyle" IS NOT NULL 
                    AND "drinkStyle" <> '' 
                    AND "drinkStyle" <> '-'
                    GROUP BY "drinkStyle"
                    ORDER BY "reviewCount" DESC
                    LIMIT 5
                ),
                total_reviews AS (
                    SELECT COUNT(*) as "totalReviews"
                    FROM "reviews"
                    WHERE "userID" = %s
                ),
                total_followers AS (
                    SELECT COUNT(*) as "totalFollowers"
                    FROM "usersFollowLists"
                    WHERE "users" @> ARRAY[%s]::TEXT[]
                )
                SELECT 
                    (SELECT array_to_json(array_agg(row_to_json(t))) FROM (
                        SELECT "id", "rating", "listingName", "photo"
                        FROM top_listings WHERE rn <= 5
                    ) t) as top_listings,
                    (SELECT array_to_json(array_agg(row_to_json(t))) FROM top_categories t) as top_categories,
                    (SELECT array_to_json(array_agg(row_to_json(t))) FROM top_venues t) as top_venues,
                    (SELECT array_to_json(array_agg(row_to_json(t))) FROM top_producers t) as top_producers,
                    (SELECT array_to_json(array_agg(row_to_json(t))) FROM top_drink_styles t) as top_drink_styles,
                    (SELECT "totalReviews" FROM total_reviews) as total_reviews,
                    (SELECT "totalFollowers" FROM total_followers) as total_followers,
                    (SELECT exists FROM user_check) as user_exists
            """, (id, id, id, id))

            result = cursor.fetchone()
            
            if not result['user_exists']:
                return jsonify({"code": 404, "message": "User not found."}), 404

            return jsonify({
                "code": 200,
                "data": {
                    "top5BestReviewedListings": result['top_listings'] or [],
                    "top5MostReviewedCategories": result['top_categories'] or [],
                    "top5Venues": result['top_venues'] or [],
                    "top5Producers": result['top_producers'] or [],
                    "top5DrinkStyles": result['top_drink_styles'] or [],
                    "totalReviews": result['total_reviews'] or 0,
                    "totalFollowers": result['total_followers'] or 0
                }
            }), 200

    except Exception as e:
        print(f"Error in getUserDashBoardData: {str(e)}")
        return jsonify({"code": 500, "message": "An error occurred retrieving the user data."}), 500


# -----------------------------------------------------------------------------------------
# [GET] Get recent followers activity for a user
@blueprint.route('/getRecentFollowersActivity/<id>', methods=['GET'])
def recent_follower_activity(id):

    conn = g.db

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            # 2. Reviews where user was tagged
            cursor.execute("""
                SELECT r."userID", r."reviewTarget", r."createdDate"
                    , l."listingName", u."username"
                FROM reviews r
                JOIN listings l ON r."reviewTarget" = l."id"
                JOIN users u ON r."userID" = u."id"
                WHERE r."reviewType" = 'Listing'
                AND %s = ANY(r."taggedUsers")
                ORDER BY r."createdDate" DESC
                LIMIT 10
            """, (id,))
            tagged_rows = cursor.fetchall()
            tags = [{
                'userID': row['userID'],
                'username': row['username'],
                'listingID': row['reviewTarget'],
                'listingName': row['listingName'],
                'date': row['createdDate'],
                'type': 'tag'
            } for row in tagged_rows]

            # Get the users who is now following the current user
            cursor.execute("""
                SELECT f."userId", f."followDate", u."username"
                FROM "latestUserFollowers" f
                JOIN users u ON f."userId" = u.id
                WHERE f."followingId" = %s
                ORDER BY f."followDate" DESC
                LIMIT 5
            """, (id,))
            follow_rows = cursor.fetchall()
            follows = [{
                'userID': row['userId'],
                'username': row['username'],
                'date': row['followDate'],
                'type': 'follow'
            } for row in follow_rows]

            activities = follows + tags

            # Sort activities by date in descending order
            activities.sort(key=lambda x: x['date'], reverse=True)

            # Limit to 10 results
            activities = activities[:10]

            return jsonify(activities)
    
    except Exception as e:
        print(f"Error in recent_follower_activity: {str(e)}")
        return jsonify({"error": "An error occurred while fetching recent follower activity."}), 500


# -----------------------------------------------------------------------------------------
# [GET] Get recent reviews activity for a user
@blueprint.route('/getRecentReviewsActivity/<id>', methods=['GET'])
def recent_review_activity_optimized(id):
    conn = g.db
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor: 
            # Single query that extracts and flattens all vote activities
            cursor.execute("""
                WITH recent_reviews AS (
                    SELECT r."id", r."reviewTarget"
                    FROM reviews r
                    WHERE r."userID" = %s
                    ORDER BY r."createdDate" DESC
                    LIMIT 10
                ),
                vote_activities AS (
                    SELECT 
                        rr."reviewTarget",
                        jsonb_array_elements(COALESCE(ruv."upvotes", '[]'::jsonb)) AS vote_data,
                        'upvote' AS vote_type
                    FROM recent_reviews rr
                    JOIN "reviewsUserVotes" ruv ON rr."id" = ruv."reviewId"
                    WHERE jsonb_array_length(COALESCE(ruv."upvotes", '[]'::jsonb)) > 0
                    
                    UNION ALL
                    
                    SELECT 
                        rr."reviewTarget",
                        jsonb_array_elements(COALESCE(ruv."downvotes", '[]'::jsonb)) AS vote_data,
                        'downvote' AS vote_type
                    FROM recent_reviews rr
                    JOIN "reviewsUserVotes" ruv ON rr."id" = ruv."reviewId"
                    WHERE jsonb_array_length(COALESCE(ruv."downvotes", '[]'::jsonb)) > 0
                )
                SELECT 
                    (vote_data->>'userId')::int AS "userID",
                    "reviewTarget",
                    vote_type AS "type",
                    vote_data->>'date' AS "date"
                FROM vote_activities
                ORDER BY vote_data->>'date' DESC
                LIMIT 10;
            """, (id,))
            
            activities = cursor.fetchall()

            # Limit to 10 results
            activities = activities[:10]
            # Loop through all activities to get the user and listing information
            for activity in activities:
                
                userID = activity['userID']
                listingID = activity['reviewTarget']

                # Get the username for the userID
                cursor.execute("""
                    SELECT "username" FROM "users" WHERE "id" = %s
                """, (userID,))
                user_row = cursor.fetchone()

                if user_row:
                    activity['username'] = user_row['username']

                # Get the listing name for the listingID
                cursor.execute("""
                    SELECT "listingName" FROM "listings" WHERE "id" = %s
                """, (listingID,))
                listing_row = cursor.fetchone()

                if listing_row:
                    activity['listingName'] = listing_row['listingName']

            # Convert to list of dictionaries
            result = [dict(activity) for activity in activities]
            
            return jsonify(result)
        
    except Exception as e:
        print(f"Error in recent_review_activity_optimized: {str(e)}")
        return jsonify({"error": "An error occurred while fetching recent review activity."}), 500


# -----------------------------------------------------------------------------------------
# [GET] Get the listing details for listings that user has recently reviewed - lastest 5
@blueprint.route('/getLatestReviewsDrinks/<id>', methods=['GET'])
def get_latest_reviews_drinks(id):
    conn = g.db
    cursor = conn.cursor()

    try:
        # Step 1: Get the latest 3 reviews by the user
        cursor.execute("""
            SELECT r."reviewTarget", r."rating", r."createdDate", l."listingName", l."photo"
            FROM reviews r
            JOIN listings l ON r."reviewTarget" = l."id"
            WHERE r."userID" = %s
            ORDER BY r."createdDate" DESC
            LIMIT 5
        """, (id,))
        reviews = cursor.fetchall()

        if not reviews:
            return jsonify([])

        # Step 2: Prepare the response data
        response_data = []
        for review in reviews:
            response_data.append({
                'id': review['reviewTarget'],
                'listingName': review['listingName'],
                'createdDate': review['createdDate'],
                'photo': review['photo']
            })

        return jsonify(response_data)
    
    except Exception as e:
        print(f"Error in get_latest_reviews_drinks: {str(e)}")
        return jsonify({"error": "An error occurred while fetching latest reviews drinks."}), 500
    
    finally:
        cursor.close()


# -----------------------------------------------------------------------------------------
# [GET] Get recent user activity for a user
@blueprint.route('/getRecentUserActivity/<id>', methods=['GET'])
def recent_user_activity(id):
    conn = g.db
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor: 
            # Single query using UNION ALL to combine all activities
            cursor.execute("""
                WITH user_reviews AS (
                    SELECT 
                        'review' as activity_type,
                        r."reviewTarget" as "listingID",
                        l."listingName",
                        r."rating",
                        NULL as "listName",
                        r."createdDate" as activity_date
                    FROM reviews r
                    JOIN listings l ON r."reviewTarget" = l."id"
                    WHERE r."userID" = %s
                    ORDER BY r."createdDate" DESC
                    LIMIT 5
                ),
                user_bookmarks AS (
                    SELECT 
                        'bookmark' as activity_type,
                        udli."drinkId" as "listingID",
                        l."listingName",
                        NULL::numeric as rating,
                        udl."listName",
                        udli."addedDate" as activity_date
                    FROM "usersDrinkLists" udl
                    JOIN "usersDrinkListItems" udli ON udl."id" = udli."listId"
                    LEFT JOIN listings l ON udli."drinkId" = l."id"
                    WHERE udl."userId" = %s
                    AND udli."addedDate" IS NOT NULL
                    ORDER BY udli."addedDate" DESC
                    LIMIT 20  -- Get more bookmarks since we'll limit to 10 total
                ),
                combined_activities AS (
                    SELECT * FROM user_reviews
                    UNION ALL
                    SELECT * FROM user_bookmarks
                )
                SELECT 
                    activity_type as "type",
                    "listingID",
                    "listingName",
                    rating,
                    "listName",
                    activity_date as "date"
                FROM combined_activities
                WHERE activity_date IS NOT NULL
                ORDER BY activity_date DESC
                LIMIT 10;
            """, (id, id))
            
            activities = cursor.fetchall()

            # 2. Fetch the "follow" activity separately (like the original code)
            follow_activity = []

            cursor.execute("""
                SELECT u."id", u."username", f."followDate"
                FROM "latestUserFollowers" f
                JOIN users u ON f."followingId" = u."id"
                WHERE f."userId" = %s
                ORDER BY f."followDate" DESC
                LIMIT 5
            """, (id,))
            users_data = cursor.fetchall()

            if users_data:
                for user in users_data:
                    follow_activity.append({
                        'type': 'follow',
                        'userID': user['id'],
                        'username': user['username'],
                        'date': user['followDate'], 
                    })

            final_activities = follow_activity + activities

            # Sort the final activities by date in descending order
            final_activities.sort(key=lambda x: x['date'], reverse=True)

            # Limit to 10 results
            final_activities = final_activities[:10]
            
            # Final cleanup of None values from the combined list
            result = []
            for activity in final_activities:
                activity_dict = {k: v for k, v in activity.items() if v is not None}
                result.append(activity_dict)

            return jsonify(result)
        
    except Exception as e:
        print(f"Error in recent_user_activity: {str(e)}")
        return jsonify({"error": "An error occurred while fetching recent user activity."}), 500


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
# [GET] Get Listings from a randomly selected date -- ADDED BY SMU GROUP 3 - logic for randomisation
@blueprint.route("/getRandomListings")
def getRandomListings():
    conn = g.db

    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        # Fetch distinct dates by converting timestamps to dates
        cursor.execute('SELECT DISTINCT "addedDate"::DATE FROM "listings"')
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

        # Fetch listings from the selected random date
        cursor.execute('SELECT * FROM "listings" WHERE "addedDate"::DATE = %s ORDER BY RANDOM() LIMIT 30', (random_date,))
        listings_data = cursor.fetchall()

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


    if not listings_data:
        return jsonify({"error": "No listings found for selected date"}), 400

    return jsonify(listings_data)

# -----------------------------------------------------------------------------------------
# [GET] Get User Notifications
# Purpose: Fetch notifications for a user based on their account type
# Output: Notification items for the logged-in user
# @blueprint.route('/getNotifications/<acc_type>/<acc_id>', methods=['GET'])
# def getNotifications(acc_type, acc_id):
#     conn = g.db
#     cur = conn.cursor()
    
#     try:
#         acc_id = int(acc_id)
        
#         cur.execute(
#             'SELECT notif_hash FROM "userNotificationsRead" WHERE user_id = %s',
#             (acc_id,)
#         )
#         read_hashes = {row[0] for row in cur.fetchall()}
        
#         for_you_notifications = []
#         venues_notifications = []
        
#         if acc_type == "user":
#             # Getting upvoted reviews notifications
#             cur.execute("""
#                 SELECT r.id AS review_id, r."reviewTarget", r."userID", rv.upvotes, l."listingName" 
#                 FROM reviews r
#                 JOIN "reviewsUserVotes" rv ON r.id = rv."reviewId"
#                 JOIN listings l ON r."reviewTarget" = l.id
#                 WHERE r."userID" = %s AND rv.upvotes IS NOT NULL AND jsonb_array_length(rv.upvotes) > 0
#                 ORDER BY r."createdDate" DESC
#             """, (acc_id,))
#             upvoted_reviews = cur.fetchall()
            
#             for review in upvoted_reviews:
#                 upvotes = review['upvotes']
#                 for i, upvote in enumerate(upvotes):
#                     if i >= 3:
#                         break
                    
#                     notification = {
#                         'type': 'review_upvote',
#                         'title': f"Your review on {review['listingName']} got upvoted!",
#                         'time': upvote['date'],
#                         'link': f"/listing/view/{review['reviewTarget']}/{review['listingName']}",
#                         'read': False
#                     }
#                     notification['hash'] = make_hash(notification)
                    
#                     if notification['hash'] in read_hashes:
#                         continue
                    
#                     for_you_notifications.append(notification)
            
#             # Getting comment likes notifications
#             cur.execute("""
#                 SELECT cc.id AS comment_id, cc."commentContent", cc."commentDate", 
#                        cp.id AS post_id, c.id AS club_id, c."clubName",
#                        ccl.id AS like_id, ccl."memberID" AS liker_id
#                 FROM "clubPostComments" cc
#                 JOIN "clubPosts" cp ON cc."postID" = cp.id
#                 JOIN clubs c ON cp."clubID" = c.id
#                 JOIN "clubMembers" cm ON cc."commenterID" = cm.id
#                 LEFT JOIN "clubPostCommentsLikes" ccl ON cc.id = ccl."commentID"
#                 WHERE cm."userID" = %s AND cm."userType" = 'user'
#                 ORDER BY ccl.id DESC
#             """, (acc_id,))
#             comment_activities = cur.fetchall()
            
#             comment_likes_count = {}
#             for activity in comment_activities:
#                 if activity['like_id'] is not None:
#                     comment_id = activity['comment_id']
#                     if comment_id not in comment_likes_count:
#                         comment_likes_count[comment_id] = 0
                    
#                     if comment_likes_count[comment_id] < 3:
#                         notification = {
#                             'type': 'comment_like',
#                             'title': f"Someone liked your comment in {activity['clubName']}",
#                             'time': activity['commentDate'],
#                             'link': f"/club/{activity['club_id']}/post/{activity['post_id']}",
#                             'read': False
#                         }
#                         notification['hash'] = make_hash(notification)
                        
#                         if notification['hash'] in read_hashes:
#                             continue
                        
#                         for_you_notifications.append(notification)
#                         comment_likes_count[comment_id] += 1
            
#             # Getting club invites notifications
#             cur.execute("""
#                 SELECT ci.id AS invite_id, ci."inviteDate", c.id AS club_id, c."clubName",
#                        CASE 
#                            WHEN ci."inviterUserType" = 'user' THEN (SELECT username FROM users WHERE id = ci."inviterID")
#                            WHEN ci."inviterUserType" = 'producer' THEN (SELECT username FROM producers WHERE id = ci."inviterID")
#                            WHEN ci."inviterUserType" = 'venue' THEN (SELECT username FROM venues WHERE id = ci."inviterID")
#                        END AS inviter_username
#                 FROM "clubInvites" ci
#                 JOIN clubs c ON ci."clubID" = c.id
#                 WHERE ci."inviteeID" = %s AND ci."inviteeUserType" = 'user'
#                 ORDER BY ci."inviteDate" DESC
#             """, (acc_id,))
#             club_invites = cur.fetchall()
            
#             for invite in club_invites:
#                 notification = {
#                     'type': 'club_invite',
#                     'title': f"@{invite['inviter_username']} invited you to join a club: {invite['clubName']}!",
#                     'time': invite['inviteDate'],
#                     'link': f"/club/view/{invite['club_id']}/{invite['clubName']}",
#                     'read': False
#                 }
#                 notification['hash'] = make_hash(notification)
                
#                 if notification['hash'] in read_hashes:
#                     continue
                
#                 for_you_notifications.append(notification)
            
#             # Getting tagged in reviews notifications
#             cur.execute("""
#                 SELECT r.id AS review_id, r."createdDate", r."reviewTarget", l."listingName",
#                        u.username AS tagger_username, u.id AS tagger_id
#                 FROM reviews r
#                 JOIN listings l ON r."reviewTarget" = l.id
#                 JOIN users u ON r."userID" = u.id
#                 WHERE %s = ANY(r."taggedUsers")
#                 ORDER BY r."createdDate" DESC
#             """, (str(acc_id),))
#             tagged_reviews = cur.fetchall()
            
#             for review in tagged_reviews:
#                 notification = {
#                     'type': 'tagged_in_review',
#                     'title': f"@{review['tagger_username']} just tagged you in their review of {review['listingName']}!",
#                     'time': review['createdDate'],
#                     'link': f"/listing/view/{review['reviewTarget']}/{review['listingName']}",
#                     'read': False
#                 }
#                 notification['hash'] = make_hash(notification)
                
#                 if notification['hash'] in read_hashes:
#                     continue
                
#                 for_you_notifications.append(notification)
                
#         elif acc_type == "producer":
#             # Getting producer questions notifications
#             cur.execute("""
#                 SELECT pqa.id, pqa.question, pqa.date, pqa."userId",
#                        u.username AS user_username,
#                        p.id AS producer_id, p."producerName", p.username AS producer_username
#                 FROM "producersQuestionAnswers" pqa
#                 JOIN users u ON pqa."userId" = u.id
#                 JOIN producers p ON pqa."producerId" = p.id
#                 WHERE pqa."producerId" = %s
#                 ORDER BY pqa.date DESC
#             """, (acc_id,))
#             producer_questions = cur.fetchall()
            
#             for question in producer_questions:
#                 notification = {
#                     'type': 'producer_question',
#                     'title': f"@{question['user_username']} asked you a question",
#                     'time': question['date'],
#                     'link': f"/profile/producer/{question['producer_id']}/{question['producer_username']}",
#                     'read': False
#                 }
#                 notification['hash'] = make_hash(notification)
                
#                 if notification['hash'] in read_hashes:
#                     continue
                
#                 for_you_notifications.append(notification)
                
#             # Getting edit requests notifications
#             cur.execute("""
#                 SELECT re.id, re."editDesc", re."listingID", l."listingName",
#                        u.username AS user_username
#                 FROM "requestEdits" re
#                 JOIN listings l ON re."listingID" = l.id
#                 JOIN users u ON re."userID" = u.id
#                 WHERE l."producerID" = %s
#                 ORDER BY re.id DESC
#             """, (acc_id,))
#             edit_requests = cur.fetchall()
            
#             for request in edit_requests:
#                 notification = {
#                     'type': 'edit_request',
#                     'title': f"@{request['user_username']} requested an edit for {request['listingName']}",
#                     'time': None,
#                     'link': f"/request/view",
#                     'read': False
#                 }
#                 notification['hash'] = make_hash(notification)
                
#                 if notification['hash'] in read_hashes:
#                     continue
                
#                 for_you_notifications.append(notification)
                
#             # Getting menu inclusions notifications
#             cur.execute("""
#                 SELECT mi.id, mi."itemPrice", mi."itemAvailability",
#                        l.id AS listing_id, l."listingName",
#                        v.id AS venue_id, v."venueName", v.username AS venue_username,
#                        vm.id AS menu_id
#                 FROM "menuItems" mi
#                 JOIN listings l ON mi."itemID" = l.id
#                 JOIN "venuesMenu" vm ON mi."sectionId" = vm.id
#                 JOIN venues v ON vm."venueId" = v.id
#                 WHERE l."producerID" = %s
#                 ORDER BY mi.id DESC
#             """, (acc_id,))
#             menu_inclusions = cur.fetchall()
            
#             for inclusion in menu_inclusions:
#                 notification = {
#                     'type': 'menu_inclusion',
#                     'title': f"{inclusion['venueName']} added your {inclusion['listingName']} to their menu",
#                     'time': None,
#                     'link': f"/profile/venue/{inclusion['venue_id']}/{inclusion['venue_username']}",
#                     'read': False
#                 }
#                 notification['hash'] = make_hash(notification)
                
#                 if notification['hash'] in read_hashes:
#                     continue
                
#                 for_you_notifications.append(notification)
            
#             # Getting club joins notifications (for producer-owned clubs)
#             cur.execute("""
#                 SELECT cm.id, cm."joinDate", cm."userID", cm."userType",
#                        c.id AS club_id, c."clubName",
#                        CASE 
#                            WHEN cm."userType" = 'user' THEN (SELECT username FROM users WHERE id = cm."userID")
#                            WHEN cm."userType" = 'producer' THEN (SELECT username FROM producers WHERE id = cm."userID")
#                            WHEN cm."userType" = 'venue' THEN (SELECT username FROM venues WHERE id = cm."userID")
#                        END AS member_username
#                 FROM "clubMembers" cm
#                 JOIN clubs c ON cm."clubID" = c.id
#                 WHERE c.id IN (
#                     SELECT cm2."clubID" FROM "clubMembers" cm2 
#                     WHERE cm2."userID" = %s AND cm2."userType" = 'producer' AND cm2."isAdmin" = TRUE
#                 )
#                 ORDER BY cm."joinDate" DESC
#             """, (acc_id,))
#             club_joins = cur.fetchall()
            
#             for join in club_joins:
#                 notification = {
#                     'type': 'club_join',
#                     'title': f"@{join['member_username']} joined your club: {join['clubName']}",
#                     'time': join['joinDate'],
#                     'link': f"/club/view/{join['club_id']}/{join['clubName']}",
#                     'read': False
#                 }
#                 notification['hash'] = make_hash(notification)
                
#                 if notification['hash'] in read_hashes:
#                     continue
                
#                 for_you_notifications.append(notification)
                
#             # Getting event joins notifications (for producer-owned events)
#             cur.execute("""
#                 SELECT ea.id, ea."eventDate", ea."userID", ea."attendeeType",
#                        e.id AS event_id, e."eventName",
#                        CASE 
#                            WHEN ea."attendeeType" = 'user' THEN (SELECT username FROM users WHERE id = ea."userID")
#                            WHEN ea."attendeeType" = 'producer' THEN (SELECT username FROM producers WHERE id = ea."userID")
#                            WHEN ea."attendeeType" = 'venue' THEN (SELECT username FROM venues WHERE id = ea."userID")
#                        END AS attendee_username
#                 FROM "eventAttendees" ea
#                 JOIN events e ON ea."eventID" = e.id
#                 WHERE e."eventOwnerID" = %s AND e."eventOwnerType" = 'producer'
#                 ORDER BY ea."eventDate" DESC
#             """, (acc_id,))
#             event_joins = cur.fetchall()
            
#             for join in event_joins:
#                 notification = {
#                     'type': 'event_join',
#                     'title': f"@{join['attendee_username']} is attending your event: {join['eventName']}",
#                     'time': join['eventDate'],
#                     'link': f"/event/{join['event_id']}/{join['eventName']}",
#                     'read': False
#                 }
#                 notification['hash'] = make_hash(notification)
                
#                 if notification['hash'] in read_hashes:
#                     continue
                
#                 for_you_notifications.append(notification)
                
#         elif acc_type == "venue":
#             # Getting venue questions notifications
#             cur.execute("""
#                 SELECT vqa.id, vqa.question, vqa.date, vqa."userId",
#                        u.username AS user_username,
#                        v.id AS venue_id, v."venueName", v.username AS venue_username
#                 FROM "venuesQuestionAnswers" vqa
#                 JOIN users u ON vqa."userId" = u.id
#                 JOIN venues v ON vqa."venueId" = v.id
#                 WHERE vqa."venueId" = %s
#                 ORDER BY vqa.date DESC
#             """, (acc_id,))
#             venue_questions = cur.fetchall()
            
#             for question in venue_questions:
#                 notification = {
#                     'type': 'venue_question',
#                     'title': f"@{question['user_username']} asked you a question",
#                     'time': question['date'],
#                     'link': f"/profile/venue/{question['venue_id']}/{question['venue_username']}",
#                     'read': False
#                 }
#                 notification['hash'] = make_hash(notification)
                
#                 if notification['hash'] in read_hashes:
#                     continue
                
#                 for_you_notifications.append(notification)
                
#             # Getting venue tagged in reviews notifications
#             cur.execute("""
#                 SELECT r.id AS review_id, r."createdDate", r."reviewTarget", l."listingName",
#                        u.username AS reviewer_username, u.id AS reviewer_id
#                 FROM reviews r
#                 JOIN listings l ON r."reviewTarget" = l.id
#                 JOIN users u ON r."userID" = u.id
#                 WHERE r.location = %s
#                 ORDER BY r."createdDate" DESC
#                 LIMIT 10
#             """, (acc_id,))
#             venue_tag_reviews = cur.fetchall()
            
#             for review in venue_tag_reviews:
#                 notification = {
#                     'type': 'venue_tagged_review',
#                     'title': f"@{review['reviewer_username']} mentioned your venue in their review of {review['listingName']}",
#                     'time': review['createdDate'],
#                     'link': f"/listing/view/{review['reviewTarget']}/{review['listingName']}",
#                     'read': False
#                 }
#                 notification['hash'] = make_hash(notification)
                
#                 if notification['hash'] in read_hashes:
#                     continue
                
#                 for_you_notifications.append(notification)
                
#             # Getting club joins notifications (for venue-owned clubs)
#             cur.execute("""
#                 SELECT cm.id, cm."joinDate", cm."userID", cm."userType",
#                        c.id AS club_id, c."clubName",
#                        CASE 
#                            WHEN cm."userType" = 'user' THEN (SELECT username FROM users WHERE id = cm."userID")
#                            WHEN cm."userType" = 'producer' THEN (SELECT username FROM producers WHERE id = cm."userID")
#                            WHEN cm."userType" = 'venue' THEN (SELECT username FROM venues WHERE id = cm."userID")
#                        END AS member_username
#                 FROM "clubMembers" cm
#                 JOIN clubs c ON cm."clubID" = c.id
#                 WHERE c.id IN (
#                     SELECT cm2."clubID" FROM "clubMembers" cm2 
#                     WHERE cm2."userID" = %s AND cm2."userType" = 'venue' AND cm2."isAdmin" = TRUE
#                 )
#                 ORDER BY cm."joinDate" DESC
#             """, (acc_id,))
#             club_joins = cur.fetchall()
            
#             for join in club_joins:
#                 notification = {
#                     'type': 'club_join',
#                     'title': f"@{join['member_username']} joined your club: {join['clubName']}",
#                     'time': join['joinDate'],
#                     'link': f"/club/view/{join['club_id']}/{join['clubName']}",
#                     'read': False
#                 }
#                 notification['hash'] = make_hash(notification)
                
#                 if notification['hash'] in read_hashes:
#                     continue
                
#                 for_you_notifications.append(notification)
                
#             # Getting event joins notifications (for venue-owned events)
#             cur.execute("""
#                 SELECT ea.id, ea."eventDate", ea."userID", ea."attendeeType",
#                        e.id AS event_id, e."eventName",
#                        CASE 
#                            WHEN ea."attendeeType" = 'user' THEN (SELECT username FROM users WHERE id = ea."userID")
#                            WHEN ea."attendeeType" = 'producer' THEN (SELECT username FROM producers WHERE id = ea."userID")
#                            WHEN ea."attendeeType" = 'venue' THEN (SELECT username FROM venues WHERE id = ea."userID")
#                        END AS attendee_username
#                 FROM "eventAttendees" ea
#                 JOIN events e ON ea."eventID" = e.id
#                 WHERE e."eventOwnerID" = %s AND e."eventOwnerType" = 'venue'
#                 ORDER BY ea."eventDate" DESC
#             """, (acc_id,))
#             event_joins = cur.fetchall()
            
#             for join in event_joins:
#                 notification = {
#                     'type': 'event_join',
#                     'title': f"@{join['attendee_username']} is attending your event: {join['eventName']}",
#                     'time': join['eventDate'],
#                     'link': f"/event/{join['event_id']}/{join['eventName']}",
#                     'read': False
#                 }
#                 notification['hash'] = make_hash(notification)
                
#                 if notification['hash'] in read_hashes:
#                     continue
                
#                 for_you_notifications.append(notification)
        
#         # Process venues notifications for user account type
#         if acc_type == "user":
#             # Getting venue status updates
#             cur.execute("""
#                 SELECT vu.id, vu.date, vu.text, vu.photo,
#                        v.id AS venue_id, v."venueName", v.photo AS venue_photo, v.username AS venue_username
#                 FROM "venuesUpdates" vu
#                 JOIN venues v ON vu."venueId" = v.id
#                 ORDER BY vu.date DESC
#                 LIMIT 20
#             """)
#             venue_updates = cur.fetchall()
            
#             for update in venue_updates:
#                 notification = {
#                     'type': 'venue_status_update',
#                     'title': f"{update['venueName']} just updated their status: \"{update['text']}\"",
#                     'time': update['date'],
#                     'link': f"/profile/venue/{update['venue_id']}/{update['venue_username']}",
#                     'read': False,
#                     'logo': update['venue_photo']
#                 }
#                 notification['hash'] = make_hash(notification)
                
#                 if notification['hash'] in read_hashes:
#                     continue
                
#                 venues_notifications.append(notification)
            
#             # Getting producer status updates
#             cur.execute("""
#                 SELECT pu.id, pu.date, pu.text, pu.photo,
#                        p.id AS producer_id, p."producerName", p.photo AS producer_photo, p.username AS producer_username
#                 FROM "producersUpdates" pu
#                 JOIN producers p ON pu."producerId" = p.id
#                 ORDER BY pu.date DESC
#                 LIMIT 20
#             """)
#             producer_updates = cur.fetchall()
            
#             for update in producer_updates:
#                 notification = {
#                     'type': 'producer_status_update',
#                     'title': f"{update['producerName']} just updated their status: \"{update['text']}\"",
#                     'time': update['date'],
#                     'link': f"/profile/producer/{update['producer_id']}/{update['producer_username']}",
#                     'read': False,
#                     'logo': update['producer_photo']
#                 }
#                 notification['hash'] = make_hash(notification)
                
#                 if notification['hash'] in read_hashes:
#                     continue
                
#                 venues_notifications.append(notification)
            
#             # Getting venue question answers
#             cur.execute("""
#                 SELECT vqa.id, vqa.question, vqa.answer, vqa.date,
#                        v.id AS venue_id, v."venueName", v.photo AS venue_photo, v.username AS venue_username
#                 FROM "venuesQuestionAnswers" vqa
#                 JOIN venues v ON vqa."venueId" = v.id
#                 WHERE vqa."userId" = %s
#                 AND vqa.answer IS NOT NULL
#                 ORDER BY vqa.date DESC
#                 LIMIT 20
#             """, (acc_id,))
#             venue_answers = cur.fetchall()
            
#             for answer in venue_answers:
#                 notification = {
#                     'type': 'venue_question_reply',
#                     'title': f"{answer['venueName']} just posted a reply to the question: \"{answer['question']}\"",
#                     'time': answer['date'],
#                     'link': f"/profile/venue/{answer['venue_id']}/{answer['venue_username']}",
#                     'read': False,
#                     'logo': answer['venue_photo']
#                 }
#                 notification['hash'] = make_hash(notification)
                
#                 if notification['hash'] in read_hashes:
#                     continue
                
#                 venues_notifications.append(notification)
            
#             # Getting producer question answers
#             cur.execute("""
#                 SELECT pqa.id, pqa.question, pqa.answer, pqa.date,
#                        p.id AS producer_id, p."producerName", p.photo AS producer_photo, p.username AS producer_username
#                 FROM "producersQuestionAnswers" pqa
#                 JOIN producers p ON pqa."producerId" = p.id
#                 WHERE pqa."userId" = %s
#                 AND pqa.answer IS NOT NULL
#                 ORDER BY pqa.date DESC
#                 LIMIT 20
#             """, (acc_id,))
#             producer_answers = cur.fetchall()
            
#             for answer in producer_answers:
#                 notification = {
#                     'type': 'producer_question_reply',
#                     'title': f"{answer['producerName']} just posted a reply to the question: \"{answer['question']}\"",
#                     'time': answer['date'],
#                     'link': f"/profile/producer/{answer['producer_id']}/{answer['producer_username']}",
#                     'read': False,
#                     'logo': answer['producer_photo']
#                 }
#                 notification['hash'] = make_hash(notification)
                
#                 if notification['hash'] in read_hashes:
#                     continue
                
#                 venues_notifications.append(notification)
            
#             # Getting events
#             cur.execute("""
#                 SELECT e.id, e."eventName", e."eventStartDate", e."eventEndDate", 
#                        e."eventStartTime", e."eventEndTime", e."createdDate",
#                        e."eventOwnerID", e."eventOwnerType",
#                        CASE 
#                            WHEN e."eventOwnerType" = 'producer' THEN 
#                                (SELECT "producerName" FROM producers WHERE id = e."eventOwnerID")
#                            WHEN e."eventOwnerType" = 'venue' THEN 
#                                (SELECT "venueName" FROM venues WHERE id = e."eventOwnerID")
#                        END AS owner_name,
#                        CASE 
#                            WHEN e."eventOwnerType" = 'producer' THEN 
#                                (SELECT photo FROM producers WHERE id = e."eventOwnerID")
#                            WHEN e."eventOwnerType" = 'venue' THEN 
#                                (SELECT photo FROM venues WHERE id = e."eventOwnerID")
#                        END AS owner_photo,
#                        CASE 
#                            WHEN e."eventOwnerType" = 'producer' THEN 
#                                (SELECT username FROM producers WHERE id = e."eventOwnerID")
#                            WHEN e."eventOwnerType" = 'venue' THEN 
#                                (SELECT username FROM venues WHERE id = e."eventOwnerID")
#                        END AS owner_username
#                 FROM events e
#                 WHERE e."eventOwnerType" IN ('producer', 'venue')
#                 ORDER BY e."createdDate" DESC
#                 LIMIT 20
#             """)
#             events = cur.fetchall()
            
#             for event in events:
#                 event_date = event['eventStartDate'].strftime('%B %d, %Y')
#                 if event['eventStartTime']:
#                     event_date += f" at {event['eventStartTime'].strftime('%I:%M %p')}"
                
#                 notification = {
#                     'type': 'new_event',
#                     'title': f"{event['owner_name']} is hosting a new event: {event['eventName']} on {event_date}",
#                     'time': event['createdDate'],
#                     'link': f"/event/{event['id']}/{event['eventName']}",
#                     'read': False,
#                     'logo': event['owner_photo']
#                 }
#                 notification['hash'] = make_hash(notification)
                
#                 if notification['hash'] in read_hashes:
#                     continue
                
#                 venues_notifications.append(notification)
            
#             # Getting current time and calculate 24 hours ago
#             now = datetime.now(timezone.utc)
#             twenty_four_hours_ago = now - timedelta(hours=24)
            
#             cur.execute("""
#                 SELECT l.id, l."listingName", l."addedDate", l."producerID",
#                        p."producerName", p.photo AS producer_photo, p.username AS producer_username
#                 FROM listings l
#                 JOIN producers p ON l."producerID" = p.id
#                 WHERE l."addedDate" >= %s
#                 ORDER BY l."addedDate" DESC
#             """, (twenty_four_hours_ago,))
#             new_listings = cur.fetchall()
            
#             # Group by producer and limit to 2 per producer
#             producer_drink_count = {}
#             for listing in new_listings:
#                 producer_id = listing['producerID']
#                 if producer_id not in producer_drink_count:
#                     producer_drink_count[producer_id] = 0
                
#                 if producer_drink_count[producer_id] < 2:
#                     notification = {
#                         'type': 'new_drink',
#                         'title': f"{listing['producerName']} added a new drink: {listing['listingName']}",
#                         'time': listing['addedDate'],
#                         'link': f"/listing/view/{listing['id']}/{listing['listingName']}",
#                         'read': False,
#                         'logo': listing['producer_photo']
#                     }
#                     notification['hash'] = make_hash(notification)
                    
#                     if notification['hash'] in read_hashes:
#                         continue
                    
#                     venues_notifications.append(notification)
#                     producer_drink_count[producer_id] += 1
        
#         def normalize_datetime(time_value):
#             if time_value is None:
#                 return None
                
#             if isinstance(time_value, str):
#                 try:
#                     return datetime.strptime(time_value, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc)
#                 except ValueError:
#                     try:
#                         return datetime.strptime(time_value, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
#                     except ValueError:
#                         return datetime.now(timezone.utc)
#             elif isinstance(time_value, date) and not isinstance(time_value, datetime):
#                 return datetime.combine(time_value, datetime.min.time()).replace(tzinfo=timezone.utc)
#             elif isinstance(time_value, datetime):
#                 if time_value.tzinfo is None:
#                     return time_value.replace(tzinfo=timezone.utc)
#                 return time_value
            
#             return datetime.now(timezone.utc)
        
#         # Helper function for sorting
#         def get_sort_key(notification):
#             time_value = notification.get('time')
#             if time_value is not None:
#                 return normalize_datetime(time_value)
#             return datetime.now(timezone.utc)
        
#         # Normalize datetime objects in notifications
#         for notification in for_you_notifications:
#             if notification['time'] is not None:
#                 notification['time'] = normalize_datetime(notification['time'])
        
#         for notification in venues_notifications:
#             if notification['time'] is not None:
#                 notification['time'] = normalize_datetime(notification['time'])
        
#         # Sort notifications by time (recent first)
#         for_you_notifications.sort(key=get_sort_key, reverse=True)
#         venues_notifications.sort(key=get_sort_key, reverse=True)
        
#         # Return the notifications
#         return jsonify({
#             'forYou': for_you_notifications[:10],  # Limit to 10 most recent notifications
#             'venues': venues_notifications[:20]
#         }), 200
        
#     except Exception as e:
#         print(str(e))
#         return jsonify({
#             'code': 500,
#             'message': 'An error occurred fetching notifications.',
#             'error': str(e)
#         }), 500
    
#     finally:
#         cur.close()

# -----------------------------------------------------------------------------------------
# [GET] Get User Notifications
# Purpose: Fetch notifications for a user based on their account type
# Output: Notification items for the logged-in user
@blueprint.route('/getNotifications/<acc_type>/<acc_id>', methods=['GET'])
def getNotifications(acc_type, acc_id):
    conn = g.db
    # use RealDictCursor so that fetchall() returns a list of dicts
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        acc_id = int(acc_id)

        # 1) Decide which notiTabs to include based on acc_type
        if acc_type == 'user':
            tabs = ['forYou', 'venues & producers', 'news']
        else:  # acc_type == 'venue' or 'producer'
            tabs = ['forYou', 'news']

        # 2) Fetch only notifications for this userId AND the desired notiTabs
        cur.execute(
            'SELECT * '
            'FROM "notifications" '
            'WHERE "userId" = %s '
            '  AND "notiTabs" = ANY(%s)',
            (acc_id, tabs)
        )
        rows = cur.fetchall()  # each row is a dict because of RealDictCursor

        # 3) Split into two lists based on notiTabs
        for_you_notifications = []
        venues_notifications = []
        news_notifications = []
        
        for notif in rows:
            tab = notif.get('notiTabs')
            # Copy createdAt into a uniform 'time' field for sorting
            notif['time'] = notif.get('createdAt')

            if tab == 'forYou':
                for_you_notifications.append(notif)
            elif tab == 'venues & producers':
                venues_notifications.append(notif)
            elif tab == 'news':
                news_notifications.append(notif)

        # 4) Helper to normalize any kind of datetime-like value
        def normalize_datetime(time_value):
            if time_value is None:
                return None

            # if it's already a string, try to parse as ISO8601 Zulu
            if isinstance(time_value, str):
                try:
                    return datetime.strptime(time_value, '%Y-%m-%dT%H:%M:%S.%fZ') \
                                   .replace(tzinfo=timezone.utc)
                except ValueError:
                    try:
                        return datetime.strptime(time_value, '%Y-%m-%dT%H:%M:%SZ') \
                                       .replace(tzinfo=timezone.utc)
                    except ValueError:
                        return datetime.now(timezone.utc)

            # if it's a date (but not a datetime), convert to datetime at midnight UTC
            if isinstance(time_value, date) and not isinstance(time_value, datetime):
                return datetime.combine(time_value, datetime.min.time()) \
                               .replace(tzinfo=timezone.utc)

            # if it's already a datetime
            if isinstance(time_value, datetime):
                if time_value.tzinfo is None:
                    return time_value.replace(tzinfo=timezone.utc)
                return time_value

            # fallback
            return datetime.now(timezone.utc)

        # 5) Key function for sorting (most recent first)
        def get_sort_key(notification):
            t = notification.get('time')
            if t is not None:
                return normalize_datetime(t)
            return datetime.now(timezone.utc)

        # 6) Normalize and sort each list
        for notif in for_you_notifications:
            if notif['time'] is not None:
                notif['time'] = normalize_datetime(notif['time'])

        for notif in venues_notifications:
            if notif['time'] is not None:
                notif['time'] = normalize_datetime(notif['time'])

        for_you_notifications.sort(key=get_sort_key, reverse=True)
        venues_notifications.sort(key=get_sort_key, reverse=True)

        # 7) Return JSON with limits (10 for "forYou", 20 for "venues")
        return jsonify({
            'forYou': for_you_notifications[:10],
            'venues': venues_notifications[:20],
            'news': news_notifications
        }), 200

    except Exception as e:
        print(str(e))
        return jsonify({
            'code': 500,
            'message': 'An error occurred fetching notifications.'
        }), 500

    finally:
        cur.close()


# ------------------------------------------------------------------------------------------
# [GET] Get questions and updates from producers and venues the user follows
# Purpose: Get questions and updates for a specific user (get questions and updates from producers and venues the user follows)
@blueprint.route('/getQuestionsUpdates/<user_id>', methods=['GET'])
def get_questions_updates(user_id):

    conn = g.db
    cursor = conn.cursor()

    try:
        # Get the list of producers and venues the user follows
        cursor.execute("""
            SELECT "producers", "venues" FROM "usersFollowLists" WHERE "userId" = %s
        """, (user_id,))
        follow_data = cursor.fetchone()

        producers = follow_data['producers']
        venues = follow_data['venues']

        producer_questions = []
        producer_updates = []
        venue_questions = []
        venue_updates = []

        # Loop through producers 
        if producers:

            for pid in producers:

                # Get producer questions with answers
                cursor.execute("""
                    SELECT pqa.id, pqa.question, pqa.answer, pqa.date,
                           p.id AS "producerID", p."producerName", p.photo
                    FROM "producersQuestionAnswers" pqa
                    JOIN producers p ON pqa."producerId" = p.id
                    WHERE p.id = %s AND pqa.answer IS NOT NULL
                    ORDER BY pqa.date DESC
                    LIMIT 5
                """, (pid,))
                producer_questions = cursor.fetchall()
                # Add type to each question
                for question in producer_questions:
                    question['type'] = 'producerQuestion'


                # Get producer updates
                cursor.execute("""
                    SELECT pu.id, pu.date, pu.text,
                           p.id AS "producerID", p."producerName", p.photo
                    FROM "producersUpdates" pu
                    JOIN producers p ON pu."producerId" = p.id
                    WHERE p.id = %s
                    ORDER BY pu.date DESC
                    LIMIT 3
                """, (pid,))
                producer_updates = cursor.fetchall()

                # Add type to each update
                for update in producer_updates:
                    update['type'] = 'producerUpdate'

        # Loop through venues 
        if venues:

            for vid in venues:

                # Get venue questions with answers
                cursor.execute("""
                    SELECT vqa.id, vqa.question, vqa.answer, vqa.date,
                           v.id AS "venueID", v."venueName", v.photo
                    FROM "venuesQuestionAnswers" vqa
                    JOIN venues v ON vqa."venueId" = v.id
                    WHERE v.id = %s AND vqa.answer IS NOT NULL
                    ORDER BY vqa.date DESC
                    LIMIT 5
                """, (vid,))
                venue_questions = cursor.fetchall()
                # Add type to each question
                for question in venue_questions:
                    question['type'] = 'venueQuestion'

                # Get venue updates
                cursor.execute("""
                    SELECT vu.id, vu.date, vu.text,
                           v.id AS "venueID", v."venueName", v.photo
                    FROM "venuesUpdates" vu
                    JOIN venues v ON vu."venueId" = v.id
                    WHERE v.id = %s
                    ORDER BY vu.date DESC
                    LIMIT 3
                """, (vid,))
                venue_updates = cursor.fetchall()
                # Add type to each update
                for update in venue_updates:
                    update['type'] = 'venueUpdate'


        # Prepare the response
        response = {
            'producerQuestion': producer_questions if producer_questions else [],
            'producerUpdate': producer_updates if producer_updates else [],
            'venueQuestion': venue_questions if venue_questions else [],
            'venueUpdate': venue_updates if venue_updates else []
        }
        return jsonify(response), 200

    except Exception as e:
        print(str(e))
        return jsonify({
            'code': 500,
            'message': 'An error occurred fetching questions and updates.'
        }), 500
    finally:
        cursor.close()

# ------------------------------------------------------------------------------------------
# [POST] Get the number of requests for a specific user, specifically the number of listing requests, listing edits requests, and duplicate requests
# Post data: user_id, user_type, is_admin, drink_types
@blueprint.route('/getRequestsCount', methods=['POST'])
def get_requests_count():
    conn = g.db
    cur = conn.cursor()

    data = request.get_json()
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({
            'code': 400,
            'message': 'User ID is required.'
        }), 400
    
    user_type = data.get('user_type')
    is_admin = data.get('is_admin')
    drink_types = data.get('drink_types', [])

    try:
        # Check user type
        if user_type == 'user':

            # Check if user is admin 
            if is_admin:

                # Get all requests for admin user
                cur.execute("""
                    SELECT COUNT(*) AS count FROM "requestListings"
                    WHERE "reviewStatus" = FALSE
                """)
                listing_requests_count = cur.fetchone()['count']

                # Get all listing edits requests for admin user
                cur.execute("""
                    SELECT COUNT(*) AS count FROM "requestEdits"
                    WHERE "reviewStatus" = FALSE
                    AND "duplicateLink" IS NULL
                """)
                listing_edits_requests_count = cur.fetchone()['count']

                # Get all duplicate requests for admin user
                cur.execute("""
                    SELECT COUNT(*) AS count FROM "requestEdits"
                    WHERE "reviewStatus" = FALSE
                    AND "duplicateLink" IS NOT NULL
                """)
                duplicate_requests_count = cur.fetchone()['count']
            else:
                # Get requests raised by the user or request is part of the user's drink types (moderator)
                cur.execute("""
                    SELECT COUNT(*) AS count FROM "requestListings"
                    WHERE "userID" = %s OR "drinkType" = ANY(%s)
                    AND "reviewStatus" = FALSE
                """, (user_id, drink_types))
                listing_requests_count = cur.fetchone()['count']

                # Get listing edits requests raised by the user or request is part of the user's drink types (moderator)
                cur.execute("""
                    SELECT COUNT(*) AS count
                    FROM "requestEdits" re
                    JOIN listings l ON re."listingID" = l.id
                    WHERE (
                        re."userID" = %s OR l."drinkType" = ANY(%s)
                    )
                    AND re."reviewStatus" = FALSE
                    AND re."duplicateLink" IS NULL
                """, (user_id, drink_types))
                listing_edits_requests_count = cur.fetchone()['count']


                # Get duplicate requests raised by the user or request is part of the user's drink types (moderator)
                cur.execute("""
                    SELECT COUNT(*) AS count 
                    FROM "requestEdits" re
                    JOIN listings l ON re."listingID" = l.id
                    WHERE (
                            re."userID" = %s OR l."drinkType" = ANY(%s)
                        )
                    AND re."reviewStatus" = FALSE
                    AND re."duplicateLink" IS NOT NULL
                """, (user_id, drink_types))
                duplicate_requests_count = cur.fetchone()['count']

        elif user_type == 'producer':
            # Get requests related to the producer
            cur.execute("""
                SELECT COUNT(*) AS count FROM "requestListings"
                WHERE "producerID" = %s
                AND "reviewStatus" = FALSE
            """, (user_id,))
            listing_requests_count = cur.fetchone()['count']

            # Get listing edits requests related to the producer
            cur.execute("""
                SELECT COUNT(*) AS count 
                FROM "requestEdits" re
                JOIN listings l ON re."listingID" = l.id
                WHERE l."producerID" = %s
                AND re."reviewStatus" = FALSE
                AND re."duplicateLink" IS NULL
            """, (user_id,))
            listing_edits_requests_count = cur.fetchone()['count']

            # Get duplicate requests related to the producer
            cur.execute("""
                SELECT COUNT(*) AS count 
                FROM "requestEdits" re
                JOIN listings l ON re."listingID" = l.id
                WHERE l."producerID" = %s
                AND "reviewStatus" = FALSE
                AND "duplicateLink" IS NOT NULL
            """, (user_id,))
            duplicate_requests_count = cur.fetchone()['count']
        else:
            return jsonify({
                'code': 400,
                'message': 'Invalid user type.'
            }), 400

        return jsonify({
            'listingRequests': listing_requests_count,
            'listingEditsRequests': listing_edits_requests_count,
            'duplicateRequests': duplicate_requests_count
        }), 200

    except Exception as e:
        print(str(e))
        return jsonify({
            'code': 500,
            'message': 'An error occurred fetching requests count.'
        }), 500

    finally:
        cur.close()

# ------------------------------------------------------------------------------------------
# [GET] Get User Names Dynamic
# Purpose: Get user names dynamically based on search term
@blueprint.route('/getUserNamesDynamic/<search_term>', methods=['GET'])
def getUserNamesDynamic(search_term):

    conn = g.db
    cur = conn.cursor()
    try:

        cur.execute("""
            SELECT id, username, photo, "displayName"
            FROM users
            WHERE username ILIKE %s
            ORDER BY username
            LIMIT 15
        """, ('%' + search_term + '%',))
        user_names = cur.fetchall()

        if not user_names:
            return jsonify({}), 200

        return jsonify(user_names), 200

    except Exception as e:
        print(str(e))
        return jsonify({
            'code': 500,
            'message': 'An error occurred fetching requests count.'
        }), 500

    finally:
        cur.close()


# [GET] Get a specific system setting by name
@blueprint.route("/getSystemSetting/<setting_name>", methods=['GET'])
def getSystemSetting(setting_name):
    conn = g.db
    cursor = conn.cursor()

    try:
        cursor.execute(
            'SELECT * FROM "systemSettings" WHERE "settingName" = %s',
            (setting_name,)
        )
        
        setting = cursor.fetchone()
        
        if not setting:
            return jsonify({
                "code": 404,
                "message": f"System setting '{setting_name}' not found."
            }), 404
        
        return jsonify({
            "code": 200,
            "message": "System setting fetched successfully.",
            "settingName": setting["settingName"],
            "settingValue": setting["settingValue"],
            "settingDescription": setting["settingDescription"],
            "lastUpdated": setting["lastUpdated"]
        })
        
    except Exception as e:
        print(f"Error fetching system setting: {str(e)}")
        return jsonify({
            "code": 500,
            "message": "An error occurred while fetching the system setting."
        }), 500
    
    finally:
        cursor.close()

# to get canonical username for login

@blueprint.route("/getCanonicalUsername/<username>", methods=['GET'])
def getCanonicalUsername(username):
    try:
        conn = g.db
        cur = conn.cursor()
        
        # Check all three tables for the username
        # First check users table
        cur.execute('SELECT username FROM users WHERE REPLACE(LOWER(username), \' \', \'\') = REPLACE(LOWER(%s), \' \', \'\')', (username,))
        user = cur.fetchone()
        
        if user is not None:
            return jsonify({
                "code": 200,
                "username": user['username']
            }), 200
            
        # Check producers table
        cur.execute('SELECT username FROM producers WHERE REPLACE(LOWER(username), \' \', \'\') = REPLACE(LOWER(%s), \' \', \'\')', (username,))
        producer = cur.fetchone()
        
        if producer is not None:
            return jsonify({
                "code": 200,
                "username": producer['username']
            }), 200
            
        # Check venues table
        cur.execute('SELECT username FROM venues WHERE REPLACE(LOWER(username), \' \', \'\') = REPLACE(LOWER(%s), \' \', \'\')', (username,))
        venue = cur.fetchone()
        
        if venue is not None:
            return jsonify({
                "code": 200,
                "username": venue['username']
            }), 200
            
        # No user found
        return jsonify({
            "code": 404,
            "message": "Username not found"
        }), 404
        
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": "An error occurred retrieving the username"
        }), 500


# -----------------------------------------------------------------------------------------
# [GET] Get all users that a specific user is following (detailed user info)
@blueprint.route("/getAllUserFollowing/<id>")
def getAllUserFollowing(id):
    """Get detailed info of all users that a specific user is following"""
    conn = g.db
    cur = conn.cursor()

    try:
        # Step 1: Check if id is a valid user
        cur.execute('SELECT * FROM "users" WHERE "id" = %s', (id,))
        user_data = cur.fetchone()

        if user_data is None:
            return jsonify({
                "code": 404,
                "message": "User not found."
            }), 404
        
        # Step 2: Get the list of user IDs this user is following
        cur.execute('SELECT "users" FROM "usersFollowLists" WHERE "userId" = %s', (id,))
        follow_data = cur.fetchone()
        
        if not follow_data or not follow_data['users']:
            return jsonify({
                "following": []
            }), 200
        
        user_ids = follow_data['users']
        if not user_ids:
            return jsonify({
                "following": []
            }), 200
        
        # Step 3: Get detailed info for each user being followed
        placeholders = ','.join(['%s'] * len(user_ids))
        query = f'''
            SELECT 
                u."id", u."username", u."displayName", u."photo", u."joinDate",
                u."firstName", u."lastName", u."ambassador", u."categoryExpert",
                u."choiceDrinks", u."choiceFlavours",
                COUNT(r."id") as "reviewCount"
            FROM "users" u
            LEFT JOIN "reviews" r ON u."id" = r."userID"
            WHERE u."id" IN ({placeholders})
            GROUP BY u."id", u."username", u."displayName", u."photo", u."joinDate",
                     u."firstName", u."lastName", u."ambassador", u."categoryExpert",
                     u."choiceDrinks", u."choiceFlavours"
            ORDER BY u."displayName", u."username"
        '''
        
        cur.execute(query, user_ids)
        following_users = cur.fetchall()
        
        # Step 4: Add follower count, current points, and rank for each user
        for user in following_users:
            # Count how many people follow this user
            cur.execute('''
                SELECT COUNT(*) as follower_count
                FROM "usersFollowLists" 
                WHERE %s = ANY("users")
            ''', (str(user['id']),))
            
            follower_result = cur.fetchone()
            user['followerCount'] = follower_result['follower_count'] if follower_result else 0
            
            # Get current points from pointsRecorder table
            cur.execute('''
                SELECT "currentPoints" 
                FROM "pointsRecorder" 
                WHERE "userID" = %s AND "userType" = %s
            ''', (user['id'], 'user'))
            
            points_result = cur.fetchone()
            user['currentPoints'] = points_result['currentPoints'] if points_result else 0
            
            # Get user rank based on proof points
            user['proofRank'] = pointsHelperFunc.get_rank(user['currentPoints']) if user['currentPoints'] else pointsHelperFunc.get_rank(0)

        return jsonify({
            "following": following_users
        }), 200

    except Exception as e:
        print(f"Error in getAllUserFollowing: {str(e)}")
        return jsonify({
            "code": 500,
            "message": "An error occurred retrieving the following users."
        }), 500
    
    finally:
        cur.close()


# -----------------------------------------------------------------------------------------
# [GET] Get all users that are following a specific user (detailed user info)
@blueprint.route("/getAllUserFollowers/<id>")
def getAllUserFollowers(id):
    """Get detailed info of all users that are following a specific user"""
    conn = g.db
    cur = conn.cursor()

    try:
        # Step 1: Check if id is a valid user
        cur.execute('SELECT * FROM "users" WHERE "id" = %s', (id,))
        user_data = cur.fetchone()

        if user_data is None:
            return jsonify({
                "code": 404,
                "message": "User not found."
            }), 404
        
        # Step 2: Find all users who have this user in their follow lists
        cur.execute('''
            SELECT "userId" FROM "usersFollowLists" 
            WHERE %s = ANY("users")
        ''', (str(id),))
        
        follower_data = cur.fetchall()
        
        if not follower_data:
            return jsonify({
                "followers": []
            }), 200
        
        follower_user_ids = [row['userId'] for row in follower_data]
        
        # Step 3: Get detailed info for each follower
        placeholders = ','.join(['%s'] * len(follower_user_ids))
        query = f'''
            SELECT 
                u."id", u."username", u."displayName", u."photo", u."joinDate",
                u."firstName", u."lastName", u."ambassador", u."categoryExpert",
                u."choiceDrinks", u."choiceFlavours",
                COUNT(r."id") as "reviewCount"
            FROM "users" u
            LEFT JOIN "reviews" r ON u."id" = r."userID"
            WHERE u."id" IN ({placeholders})
            GROUP BY u."id", u."username", u."displayName", u."photo", u."joinDate",
                     u."firstName", u."lastName", u."ambassador", u."categoryExpert",
                     u."choiceDrinks", u."choiceFlavours"
            ORDER BY u."displayName", u."username"
        '''
        
        cur.execute(query, follower_user_ids)
        follower_users = cur.fetchall()
        
        # Step 4: Add follower count, current points, and rank for each user
        for user in follower_users:
            # Count how many people follow this user
            cur.execute('''
                SELECT COUNT(*) as follower_count
                FROM "usersFollowLists" 
                WHERE %s = ANY("users")
            ''', (str(user['id']),))
            
            follower_result = cur.fetchone()
            user['followerCount'] = follower_result['follower_count'] if follower_result else 0
            
            # Get current points from pointsRecorder table
            cur.execute('''
                SELECT "currentPoints" 
                FROM "pointsRecorder" 
                WHERE "userID" = %s AND "userType" = %s
            ''', (user['id'], 'user'))
            
            points_result = cur.fetchone()
            user['currentPoints'] = points_result['currentPoints'] if points_result else 0
            
            # Get user rank based on proof points
            user['proofRank'] = pointsHelperFunc.get_rank(user['currentPoints']) if user['currentPoints'] else pointsHelperFunc.get_rank(0)

        return jsonify({
            "followers": follower_users
        }), 200

    except Exception as e:
        print(f"Error in getAllUserFollowers: {str(e)}")
        return jsonify({
            "code": 500,
            "message": "An error occurred retrieving the followers."
        }), 500
    
    finally:
        cur.close()
