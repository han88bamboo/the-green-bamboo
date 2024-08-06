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
from bson import json_util
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

# -----------------------------------------------------------------------------------------
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

# -----------------------------------------------------------------------------------------
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

# -----------------------------------------------------------------------------------------
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

# -----------------------------------------------------------------------------------------
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