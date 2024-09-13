# Port: 5000
# Routes: /getAccountRequests (GET), /getCountries (GET), /getListings (GET), /getListing/<id> (GET), /getProducers (GET), /getProducer/<id> (GET),
#           /getReviews (GET), /getReviewByTarget/<id> (GET), /getUsers (GET), /getUser/<id> (GET), /getUserByUsername/<username> (GET), /getVenues (GET), 
#           /getVenue/<id> (GET), /getVenuesAPI (GET), /getDrinkTypes (GET), /getRequestListings (GET), /getRequestListing/<id> (GET), /getRequestEdits (GET), 
#           /getRequestEdit/<id> (GET), /getModRequests (GET), /getFlavourTags (GET), /getSubTags (GET), /getObservationTags (GET), /getColours (GET), 
#           /getSpecialColours (GET), /getLanguages (GET), /getServingTypes (GET), /getProducersProfileViews (GET), /getVenuesProfileViewsByVenue/<id> (GET), /getRequestInaccuracyByVenue/<id> (GET)
# -----------------------------------------------------------------------------------------

# pip install python-bsonjs
# pip install Flask
# pip install Flask Flask-PyMongo
# pip install pymongo
# pip install flask-cors

import os
import json
from bson import json_util, ObjectId
from flask import Blueprint, g, jsonify
from bson.objectid import ObjectId

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

# converts BSON to JSON
def parse_json(data):
    return json.loads(json_util.dumps(data))

# Helper function to fetch user data from the database
def fetch_user_data(cursor, user_id):
    cursor.execute('SELECT * FROM "users" WHERE "id" = %s', (user_id,))
    return cursor.fetchone()

# Helper function to fetch drink lists for a user
def fetch_drink_lists(cursor, user_id):

    cursor.execute("""
        SELECT "listName", "drinks"
        FROM "usersDrinkLists"
        WHERE "userId" = %s
    """, (user_id,))
    drink_lists_data = cursor.fetchall()
    result = {}
    for row in drink_lists_data:
            list_name = row["listName"]
            drinks = row["drinks"]
            result[list_name] = {
                "listDesc": "",  # You can customize or fetch descriptions for each list if needed
                "listItems": drinks if drinks else []
            }
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
    db = g.db
    data = db.accountRequests.find({})
    print(len(list(data.clone())))
    allAccountRequests = []
    dataEncode = parse_json(data)
    for doc in dataEncode:
        allAccountRequests.append(doc)
    return allAccountRequests

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
@blueprint.route("/getListings")
def getListings():
    conn = g.db

    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM "listings"')
        listings_data = cursor.fetchall()
    
    if not listings_data:
        return jsonify([])

    return jsonify(listings_data)

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

# -----------------------------------------------------------------------------------------

# ================== POSTGRESQL FORMAT ==================

# ----------------------
# [OLD] TO BE DELETED:
# ----------------------

# [GET] Producers
@blueprint.route("/getProducers")
def getProducers():
    conn = g.db
    
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM "producers"')
        producers_data = cursor.fetchall()
    
    if not producers_data:
        return jsonify([])

    return jsonify(producers_data)

# [GET] Specific Producer
@blueprint.route("/getProducer/<id>")
def getProducer(id):
    conn = g.db
    
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM "producers" WHERE "id" = %s', (id,))
        producer_data = cursor.fetchone()
    
    if producer_data is None:
        return jsonify([])

    return jsonify(producer_data)

# [GET] Specific Producer
@blueprint.route("/getProducerByRequestId/<id>")
def getProducerByRequestId(id):
    db = g.db
    data = db.producers.find_one({"requestId": ObjectId(id)})
    if data is None:
        return []
    return parse_json(data)

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

# [GET] Specific Reviews by reviewTarget
@blueprint.route("/getReviewByTarget/<id>")
def getReviewByTarget(id):
    conn = g.db
    
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM "reviews" WHERE "reviewTarget" = %s', (id,))
        reviews_data = cursor.fetchall()
    
    if not reviews_data:
        return jsonify([])

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

        return jsonify(users_data), 200

    except Exception as e:
        print(str(e))
        return jsonify({"code": 500, "message": "An error occurred while fetching users."}), 500

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

        return jsonify(user_data), 200

    except Exception as e:
        print(str(e))
        return jsonify({"code": 500, "message": "An error occurred while fetching the user."}), 500

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
    
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM "venues"')
        venues_data = cursor.fetchall()
    
    if not venues_data:
        return jsonify([])

    return jsonify(venues_data)

# [GET] Specific Venue
@blueprint.route("/getVenue/<id>")
def getVenue(id):
    conn = g.db
    
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM "venues" WHERE "id" = %s', (id,))
        venue_data = cursor.fetchone()
    
    if venue_data is None:
        return jsonify([])

    return jsonify(venue_data)

# [GET] Specific Producer
@blueprint.route("/getVenueByRequestId/<id>")
def getVenueByRequestId(id):
    db = g.db
    data = db.venues.find_one({"requestId": ObjectId(id)})
    if data is None:
        return []
    return parse_json(data)

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
@blueprint.route("/getVenuesAPI")
def getVenuesAPI():
    db = g.db
    data = db.venuesAPI.find({})
    print(len(list(data.clone())))
    allVenuesAPI = []
    dataEncode = parse_json(data)
    for doc in dataEncode:
        allVenuesAPI.append(doc)
    return allVenuesAPI

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
    db = g.db
    data = db.modRequests.find({})
    print(len(list(data.clone())))
    allModRequests = []
    dataEncode = parse_json(data)
    for doc in dataEncode:
        allModRequests.append(doc)
    return allModRequests

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
    db = g.db
    data = db.servingTypes.find({})
    print(len(list(data.clone())))
    servingTypes = []
    dataEncode = parse_json(data)
    for doc in dataEncode:
        servingTypes.append(doc)
    return servingTypes

# -----------------------------------------------------------------------------------------

# ================== POSTGRESQL FORMAT ==================

# ----------------------
# [OLD] TO BE DELETED:
# ----------------------

# [GET] producersProfileViews
@blueprint.route("/getProducersProfileViews")
def getProducersProfileViews():
    conn = g.db

    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM "producersProfileViews"')
        allProducersProfileViews = cursor.fetchall()

    if not allProducersProfileViews:
        return jsonify([])

    return jsonify(allProducersProfileViews)

# [GET] producersProfileViews by producerID
@blueprint.route("/getProducersProfileViewsByProducer/<id>")
def getProducersProfileViewsByProducer():
    db = g.db
    data = db.producersProfileViews.find({"producerID": ObjectId(id)})
    print(len(list(data.clone())))
    producersProfileViews = []
    dataEncode = parse_json(data)
    for doc in dataEncode:
        producersProfileViews.append(doc)
    return producersProfileViews

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
    return parse_json(allProfileViews)

# =======================================================

# -----------------------------------------------------------------------------------------

# ================== POSTGRESQL FORMAT ==================

# ----------------------
# [OLD] TO BE DELETED:
# ----------------------

# [GET] venuesProfileViews
@blueprint.route("/getVenuesProfileViews")
def getVenuesProfileViews():
    db = g.db
    data = db.venuesProfileViews.find({})
    print(len(list(data.clone())))
    venuesProfileViews = []
    dataEncode = parse_json(data)
    for doc in dataEncode:
        venuesProfileViews.append(doc)
    return venuesProfileViews

# [GET] venuesProfileViews by venueID
@blueprint.route("/getVenuesProfileViewsByVenue/<id>")
def getVenuesProfileViewsByVenue(id):
    db = g.db
    data = db.venuesProfileViews.find({"venueID": ObjectId(id)})
    print(len(list(data.clone())))
    venuesProfileViews = []
    dataEncode = parse_json(data)
    for doc in dataEncode:
        venuesProfileViews.append(doc)
    return venuesProfileViews

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
    db = g.db
    data = db.requestInaccuracy.find({"venueID": ObjectId(id), "reviewStatus": False})
    if data is None:
        return []
    allRequestInaccuracy = []
    dataEncode = parse_json(data)
    for doc in dataEncode:
        allRequestInaccuracy.append(doc)
    return allRequestInaccuracy

# -----------------------------------------------------------------------------------------
# [GET] Badges
@blueprint.route("/getBadges")
def getBadges():
    db = g.db
    data = db.badges.find({})
    print(len(list(data.clone())))
    allBadges = []
    dataEncode = parse_json(data)
    for doc in dataEncode:
        allBadges.append(doc)
    return allBadges

# -----------------------------------------------------------------------------------------
# [GET] Specific Token
@blueprint.route("/getToken/<token>")
def getToken(token):
    db = g.db
    data = db.tokens.find_one({"token": token})
    if data is None:
        return []
    return parse_json(data)

# [GET] Specific Token By requestId
@blueprint.route("/getTokenByRequestId/<requestId>")
def getTokenByRequestId(requestId):
    db = g.db
    data = db.tokens.find_one({"requestId": ObjectId(requestId)})
    if data is None:
        return []
    return parse_json(data)

# -----------------------------------------------------------------------------------------
# [GET] Specific Request
@blueprint.route("/getAccountRequest/<id>")
def getAccountRequest(id):
    db = g.db
    data = db.accountRequests.find_one({"_id": ObjectId(id)})
    if data is None:
        return []
    return parse_json(data)

# -----------------------------------------------------------------------------------------
# [GET] Producers
@blueprint.route("/getUsernames")
def getUsernames():
    db = g.db
    producers_data = db.producers.find({}, {'username': 1, '_id': 0})
    venues_data = db.venues.find({}, {'username': 1, '_id': 0})

    all_usernames = [doc['username'] for doc in producers_data] + [doc['username'] for doc in venues_data]

    return parse_json(all_usernames)