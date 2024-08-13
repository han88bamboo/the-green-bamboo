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
from flask import Blueprint, g
from bson.objectid import ObjectId

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

# converts BSON to JSON
def parse_json(data):
    return json.loads(json_util.dumps(data)) 

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
    db = g.db
    data = db.countries.find({})
    print(len(list(data.clone())))
    allCountries = []
    dataEncode = parse_json(data)
    for doc in dataEncode:
        allCountries.append(doc)
    return allCountries

# -----------------------------------------------------------------------------------------
# [GET] Listings
@blueprint.route("/getListings")
def getListings():
    db = g.db
    data = db.listings.find({})
    print(len(list(data.clone())))
    allListings = []
    dataEncode = parse_json(data)
    for doc in dataEncode:
        allListings.append(doc)
    return allListings

# [GET] Specific Listing
@blueprint.route("/getListing/<id>")
def getListing(id):
    db = g.db
    data = db.listings.find_one({"_id": ObjectId(id)})
    if data is None:
        return []
    return parse_json(data)

# [GET] Specific Listings By Producer
@blueprint.route("/getListingsByProducer/<id>")
def getListingsByProducer(id):
    db = g.db
    data = db.listings.find({"producerID": ObjectId(id)})
    if data is None:
        return []
    return parse_json(data)

# -----------------------------------------------------------------------------------------

# ================== POSTGRESQL FORMAT ==================

# ----------------------
# [OLD] TO BE DELETED:
# ----------------------

# [GET] Producers
@blueprint.route("/getProducers")
def getProducers():
    db = g.db
    data = db.producers.find({})
    print(len(list(data.clone())))
    allProducers = []
    dataEncode = parse_json(data)
    for doc in dataEncode:
        allProducers.append(doc)
    return allProducers

# [GET] Specific Producer
@blueprint.route("/getProducer/<id>")
def getProducer(id):
    db = g.db
    data = db.producers.find_one({"_id": ObjectId(id)})
    if data is None:
        return []
    return parse_json(data)

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

# [GET] Reviews
@blueprint.route("/getReviews")
def getReviews():
    db = g.db
    data = db.reviews.find({})
    print(len(list(data.clone())))
    allReviews = []
    dataEncode = parse_json(data)
    for doc in dataEncode:
        allReviews.append(doc)
    return allReviews

# [GET] Specific Reviews by reviewTarget
@blueprint.route("/getReviewByTarget/<id>")
def getReviewByTarget(id):
    db = g.db
    data = db.reviews.find({"reviewTarget": ObjectId(id)})
    if data is None:
        return []
    allReviews = []
    dataEncode = parse_json(data)
    for doc in dataEncode:
        allReviews.append(doc)
    return allReviews

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
    db = g.db
    data = db.users.find({})
    print(len(list(data.clone())))
    allUsers = []
    dataEncode = parse_json(data)
    for doc in dataEncode:
        allUsers.append(doc)
    return allUsers

# [GET] Specific User
@blueprint.route("/getUser/<id>")
def getUser(id):
    db = g.db
    data = db.users.find_one({"_id": ObjectId(id)})
    if data is None:
        return []
    return parse_json(data)

# [GET] Specific User by username
@blueprint.route("/getUserByUsername/<username>")
def getUserByUsername(username):
    db = g.db
    data = db.users.find_one({"username": username})
    if data is None:
        return []
    return parse_json(data)

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
    db = g.db
    data = db.venues.find({})
    print(len(list(data.clone())))
    allVenues = []
    dataEncode = parse_json(data)
    for doc in dataEncode:
        allVenues.append(doc)
    return allVenues

# [GET] Specific Venue
@blueprint.route("/getVenue/<id>")
def getVenue(id):
    db = g.db
    data = db.venues.find_one({"_id": ObjectId(id)})
    if data is None:
        return []
    return parse_json(data)

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
    db = g.db
    data = db.drinkTypes.find({})
    print(len(list(data.clone())))
    allDrinkTypes = []
    dataEncode = parse_json(data)
    for doc in dataEncode:
        allDrinkTypes.append(doc)
    return allDrinkTypes

# -----------------------------------------------------------------------------------------
# [GET] RequestListings
@blueprint.route("/getRequestListings")
def getRequestListings():
    db = g.db
    data = db.requestListings.find({})
    print(len(list(data.clone())))
    allRequestListings = []
    dataEncode = parse_json(data)
    for doc in dataEncode:
        allRequestListings.append(doc)
    return allRequestListings

# [GET] Specific Request Listing
@blueprint.route("/getRequestListing/<id>")
def getRequestListing(id):
    db = g.db
    data = db.requestListings.find_one({"_id": ObjectId(id)})
    if data is None:
        return []
    return parse_json(data)

# -----------------------------------------------------------------------------------------
# [GET] RequestEdits
@blueprint.route("/getRequestEdits")
def getRequestEdits():
    db = g.db
    data = db.requestEdits.find({})
    print(len(list(data.clone())))
    allRequestEdits = []
    dataEncode = parse_json(data)
    for doc in dataEncode:
        allRequestEdits.append(doc)
    return allRequestEdits

# [GET] Specific Request Edit
@blueprint.route("/getRequestEdit/<id>")
def getRequestEdit(id):
    db = g.db
    data = db.requestEdits.find_one({"_id": ObjectId(id)})
    if data is None:
        return []
    return parse_json(data)

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
    db = g.db
    data = db.flavourTags.find({})
    print(len(list(data.clone())))
    allFlavourTags = []
    dataEncode = parse_json(data)
    for doc in dataEncode:
        allFlavourTags.append(doc)
    return allFlavourTags
# -----------------------------------------------------------------------------------------
# [GET] subTags
@blueprint.route("/getSubTags")
def getSubTags():
    db = g.db
    data = db.subTags.find({})
    print(len(list(data.clone())))
    allSubTags = []
    dataEncode = parse_json(data)
    for doc in dataEncode:
        allSubTags.append(doc)
    return allSubTags

# -----------------------------------------------------------------------------------------
# [GET] observationTags
@blueprint.route("/getObservationTags")
def getObservationTags():
    db = g.db
    data = db.observationTags.find({})
    print(len(list(data.clone())))
    allObservationTags = []
    dataEncode = parse_json(data)
    for doc in dataEncode:
        allObservationTags.append(doc)
    return allObservationTags

# -----------------------------------------------------------------------------------------
# [GET] colours
@blueprint.route("/getColours")
def getColours():
    db = g.db
    data = db.colours.find({})
    print(len(list(data.clone())))
    allColours = []
    dataEncode = parse_json(data)
    for doc in dataEncode:
        allColours.append(doc)
    return allColours

# -----------------------------------------------------------------------------------------
# [GET] specialColours
@blueprint.route("/getSpecialColours")
def getSpecialColours():
    db = g.db
    data = db.specialColours.find({})
    print(len(list(data.clone())))
    allSpecialColours = []
    dataEncode = parse_json(data)
    for doc in dataEncode:
        allSpecialColours.append(doc)
    return allSpecialColours

# -----------------------------------------------------------------------------------------
# [GET] languages
@blueprint.route("/getLanguages")
def getLanguages():
    db = g.db
    data = db.languages.find({})
    print(len(list(data.clone())))
    languages = []
    dataEncode = parse_json(data)
    for doc in dataEncode:
        languages.append(doc)
    return languages

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
    db = g.db
    data = db.producersProfileViews.find({})
    print(len(list(data.clone())))
    producersProfileViews = []
    dataEncode = parse_json(data)
    for doc in dataEncode:
        producersProfileViews.append(doc)
    return producersProfileViews

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

# [GET] venuesProfileViews
@blueprint.route("/getVenuesProfileViews")
def getVenuesProfileViews():
    db = g.db
    profile_views_data = db.venuesProfileViews.find({})
    allProfileViews = []
    for profile_view in profile_views_data:
        # Fetch related views data based on the id(s) in profile_view's views
        views_data = db.venuesProfileViewsViews.find({
            "_id": {"$in": profile_view['views']}
        })
        profile_view['views'] = list(views_data)
        allProfileViews.append(profile_view)
    return parse_json(allProfileViews)

# [GET] venuesProfileViews by venueID
@blueprint.route("/getVenuesProfileViewsByVenue/<id>")
def getVenuesProfileViewsByVenue(id):
    db = g.db
    profile_views_data = db.venuesProfileViews.find({"venueID": ObjectId(id)})
    allProfileViews = []
    for profile_view in profile_views_data:
        # Fetch related views data based on the id(s) in profile_view's views
        views_data = db.venuesProfileViewsViews.find({
            "_id": {"$in": profile_view['views']}
        })
        profile_view['views'] = list(views_data)
        allProfileViews.append(profile_view)
    return parse_json(allProfileViews)

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