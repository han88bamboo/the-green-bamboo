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

import bson
import json
from bson import json_util
from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
from bson.objectid import ObjectId

from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)  # Allow all requests

load_dotenv()
app.config["MONGO_URI"] = os.getenv('MONGO_DB_URL')
db = PyMongo(app).db

#This is to parse BSON data from Mongo so that we can parse it as JSON
#possibility to put this into a separate python file so that each flask function can just import that instead of having this chunk of code
def parse_json(data):
    return json.loads(json_util.dumps(data))

# -----------------------------------------------------------------------------------------
# [GET] accountRequests
@app.route("/getAccountRequests")
def getAccountRequests():
    #this step finds all the items in the collection, specifying accountRequests
    data = db.accountRequests.find({})
    #have to use data.clone so that cursor is not used up
    print(len(list(data.clone())))
    allAccountRequests = []
    #parse bson as json
    dataEncode = parse_json(data)
    for doc in dataEncode:
        # print(doc)
        allAccountRequests.append(doc)
    return allAccountRequests

# -----------------------------------------------------------------------------------------
# [GET] Countries
@app.route("/getCountries")
def getCountries():
    #this step finds all the items in the collection, specifying Countries
    data = db.countries.find({})
    #have to use data.clone so that cursor is not used up
    print(len(list(data.clone())))
    allCountries = []
    #parse bson as json
    dataEncode = parse_json(data)
    for doc in dataEncode:
        # print(doc)
        allCountries.append(doc)
    return allCountries

# -----------------------------------------------------------------------------------------
# [GET] Listings
@app.route("/getListings")
def getListings():
    #this step finds all the items in the collection, specifying Listings
    data = db.listings.find({})
    #have to use data.clone so that cursor is not used up
    print(len(list(data.clone())))
    allListings = []
    #parse bson as json
    dataEncode = parse_json(data)
    for doc in dataEncode:
        # print(doc)
        allListings.append(doc)
    return allListings

# [GET] Specific Listing
@app.route("/getListing/<id>")
def getListing(id):
    data = db.listings.find_one({"_id": ObjectId(id)})
    if data is None:
        return []
    return parse_json(data)

# [GET] Specific Listings By Producer
@app.route("/getListingsByProducer/<id>")
def getListingsByProducer(id):
    data = db.listings.find({"producerID": ObjectId(id)})
    if data is None:
        return []
    return parse_json(data)

# -----------------------------------------------------------------------------------------
# [GET] Producers
@app.route("/getProducers")
def getProducers():
    #this step finds all the items in the collection, specifying Producers
    data = db.producers.find({})
    #have to use data.clone so that cursor is not used up
    print(len(list(data.clone())))
    allProducers = []
    #parse bson as json
    dataEncode = parse_json(data)
    for doc in dataEncode:
        # print(doc)
        allProducers.append(doc)
    return allProducers

# [GET] Specific Producer
@app.route("/getProducer/<id>")
def getProducer(id):
    data = db.producers.find_one({"_id": ObjectId(id)})
    if data is None:
        return []
    return parse_json(data)

# -----------------------------------------------------------------------------------------
# [GET] Reviews
@app.route("/getReviews")
def getReviews():
    #this step finds all the items in the collection, specifying Reviews
    data = db.reviews.find({})
    #have to use data.clone so that cursor is not used up
    print(len(list(data.clone())))
    allReviews = []
    #parse bson as json
    dataEncode = parse_json(data)
    for doc in dataEncode:
        # print(doc)
        allReviews.append(doc)
    return allReviews

# [GET] Specific Reviews by reviewTarget
@app.route("/getReviewByTarget/<id>")
def getReviewByTarget(id):
    data = db.reviews.find({"reviewTarget": ObjectId(id)})
    if data is None:
        return []
    allReviews = []
    #parse bson as json
    dataEncode = parse_json(data)
    for doc in dataEncode:
        # print(doc)
        allReviews.append(doc)
    return allReviews

# -----------------------------------------------------------------------------------------
# [GET] Users
@app.route("/getUsers")
def getUsers():
    #this step finds all the items in the collection, specifying Users
    data = db.users.find({})
    #have to use data.clone so that cursor is not used up
    print(len(list(data.clone())))
    allUsers = []
    #parse bson as json
    dataEncode = parse_json(data)
    for doc in dataEncode:
        # print(doc)
        allUsers.append(doc)
    return allUsers

# [GET] Specific User
@app.route("/getUser/<id>")
def getUser(id):
    data = db.users.find_one({"_id": ObjectId(id)})
    if data is None:
        return []
    return parse_json(data)

# [GET] Specific User by username
@app.route("/getUserByUsername/<username>")
def getUserByUsername(username):
    data = db.users.find_one({"username": username})
    if data is None:
        return []
    return parse_json(data)

# -----------------------------------------------------------------------------------------
# [GET] Venues
@app.route("/getVenues")
def getVenues():
    #this step finds all the items in the collection, specifying Venues
    data = db.venues.find({})
    #have to use data.clone so that cursor is not used up
    print(len(list(data.clone())))
    allVenues = []
    #parse bson as json
    dataEncode = parse_json(data)
    for doc in dataEncode:
        # print(doc)
        allVenues.append(doc)
    return allVenues

# [GET] Specific Venue
@app.route("/getVenue/<id>")
def getVenue(id):
    data = db.venues.find_one({"_id": ObjectId(id)})
    if data is None:
        return []
    return parse_json(data)

# -----------------------------------------------------------------------------------------
# [GET] VenuesAPI
@app.route("/getVenuesAPI")
def getVenuesAPI():
    #this step finds all the items in the collection, specifying VenuesAPI
    data = db.venuesAPI.find({})
    #have to use data.clone so that cursor is not used up
    print(len(list(data.clone())))
    allVenuesAPI = []
    #parse bson as json
    dataEncode = parse_json(data)
    for doc in dataEncode:
        # print(doc)
        allVenuesAPI.append(doc)
    return allVenuesAPI

# -----------------------------------------------------------------------------------------
# [GET] DrinkTypes
@app.route("/getDrinkTypes")
def getDrinkTypes():
    #this step finds all the items in the collection, specifying Drink Types
    data = db.drinkTypes.find({})
    #have to use data.clone so that cursor is not used up
    print(len(list(data.clone())))
    allDrinkTypes = []
    #parse bson as json
    dataEncode = parse_json(data)
    for doc in dataEncode:
        # print(doc)
        allDrinkTypes.append(doc)
    return allDrinkTypes

# -----------------------------------------------------------------------------------------
# [GET] RequestListings
@app.route("/getRequestListings")
def getRequestListings():
    #this step finds all the items in the collection, specifying Request Listings
    data = db.requestListings.find({})
    #have to use data.clone so that cursor is not used up
    print(len(list(data.clone())))
    allRequestListings = []
    #parse bson as json
    dataEncode = parse_json(data)
    for doc in dataEncode:
        # print(doc)
        allRequestListings.append(doc)
    return allRequestListings

# [GET] Specific Request Listing
@app.route("/getRequestListing/<id>")
def getRequestListing(id):
    data = db.requestListings.find_one({"_id": ObjectId(id)})
    if data is None:
        return []
    return parse_json(data)

# -----------------------------------------------------------------------------------------
# [GET] RequestEdits
@app.route("/getRequestEdits")
def getRequestEdits():
    #this step finds all the items in the collection, specifying Request Edits
    data = db.requestEdits.find({})
    #have to use data.clone so that cursor is not used up
    print(len(list(data.clone())))
    allRequestEdits = []
    #parse bson as json
    dataEncode = parse_json(data)
    for doc in dataEncode:
        # print(doc)
        allRequestEdits.append(doc)
    return allRequestEdits

# [GET] Specific Request Edit
@app.route("/getRequestEdit/<id>")
def getRequestEdit(id):
    data = db.requestEdits.find_one({"_id": ObjectId(id)})
    if data is None:
        return []
    return parse_json(data)

# -----------------------------------------------------------------------------------------
# [GET] modRequests
@app.route("/getModRequests")
def getModRequests():
    #this step finds all the items in the collection, specifying Mod Requests
    data = db.modRequests.find({})
    #have to use data.clone so that cursor is not used up
    print(len(list(data.clone())))
    allModRequests = []
    #parse bson as json
    dataEncode = parse_json(data)
    for doc in dataEncode:
        # print(doc)
        allModRequests.append(doc)
    return allModRequests

# -----------------------------------------------------------------------------------------
# [GET] flavourTags
@app.route("/getFlavourTags")
def getFlavourTags():
    #this step finds all the items in the collection, specifying Flavour Tags
    data = db.flavourTags.find({})
    #have to use data.clone so that cursor is not used up
    print(len(list(data.clone())))
    allFlavourTags = []
    #parse bson as json
    dataEncode = parse_json(data)
    for doc in dataEncode:
        # print(doc)
        allFlavourTags.append(doc)
    return allFlavourTags
# -----------------------------------------------------------------------------------------
# [GET] subTags
@app.route("/getSubTags")
def getSubTags():
    #this step finds all the items in the collection, specifying Flavour Tags
    data = db.subTags.find({})
    #have to use data.clone so that cursor is not used up
    print(len(list(data.clone())))
    allSubTags = []
    #parse bson as json
    dataEncode = parse_json(data)
    for doc in dataEncode:
        # print(doc)
        allSubTags.append(doc)
    return allSubTags

# -----------------------------------------------------------------------------------------
# [GET] observationTags
@app.route("/getObservationTags")
def getObservationTags():
    #this step finds all the items in the collection, specifying Flavour Tags
    data = db.observationTags.find({})
    #have to use data.clone so that cursor is not used up
    print(len(list(data.clone())))
    allObservationTags = []
    #parse bson as json
    dataEncode = parse_json(data)
    for doc in dataEncode:
        # print(doc)
        allObservationTags.append(doc)
    return allObservationTags

# -----------------------------------------------------------------------------------------
# [GET] colours
@app.route("/getColours")
def getColours():
    #this step finds all the items in the collection, specifying Flavour Tags
    data = db.colours.find({})
    #have to use data.clone so that cursor is not used up
    print(len(list(data.clone())))
    allColours = []
    #parse bson as json
    dataEncode = parse_json(data)
    for doc in dataEncode:
        # print(doc)
        allColours.append(doc)
    return allColours

# -----------------------------------------------------------------------------------------
# [GET] specialColours
@app.route("/getSpecialColours")
def getSpecialColours():
    #this step finds all the items in the collection, specifying Flavour Tags
    data = db.specialColours.find({})
    #have to use data.clone so that cursor is not used up
    print(len(list(data.clone())))
    allSpecialColours = []
    #parse bson as json
    dataEncode = parse_json(data)
    for doc in dataEncode:
        # print(doc)
        allSpecialColours.append(doc)
    return allSpecialColours

# -----------------------------------------------------------------------------------------
# [GET] languages
@app.route("/getLanguages")
def getLanguages():
    #this step finds all the items in the collection, specifying languages
    data = db.languages.find({})
    #have to use data.clone so that cursor is not used up
    print(len(list(data.clone())))
    languages = []
    #parse bson as json
    dataEncode = parse_json(data)
    for doc in dataEncode:
        # print(doc)
        languages.append(doc)
    return languages

# -----------------------------------------------------------------------------------------
# [GET] servingTypes
@app.route("/getServingTypes")
def getServingTypes():
    #this step finds all the items in the collection, specifying servingTypes
    data = db.servingTypes.find({})
    #have to use data.clone so that cursor is not used up
    print(len(list(data.clone())))
    servingTypes = []
    #parse bson as json
    dataEncode = parse_json(data)
    for doc in dataEncode:
        # print(doc)
        servingTypes.append(doc)
    return servingTypes

# -----------------------------------------------------------------------------------------
# [GET] producersProfileViews
@app.route("/getProducersProfileViews")
def getProducersProfileViews():
    #this step finds all the items in the collection, specifying producersProfileViews
    data = db.producersProfileViews.find({})
    #have to use data.clone so that cursor is not used up
    print(len(list(data.clone())))
    producersProfileViews = []
    #parse bson as json
    dataEncode = parse_json(data)
    for doc in dataEncode:
        # print(doc)
        producersProfileViews.append(doc)
    return producersProfileViews

# -----------------------------------------------------------------------------------------
# [GET] venuesProfileViews by venueID
@app.route("/getVenuesProfileViewsByVenue/<id>")
def getVenuesProfileViewsByVenue(id):
    #this step finds all the items in the collection, specifying venuesProfileViews
    data = db.venuesProfileViews.find({"venueID": ObjectId(id)})
    #have to use data.clone so that cursor is not used up
    print(len(list(data.clone())))
    venuesProfileViews = []
    #parse bson as json
    dataEncode = parse_json(data)
    for doc in dataEncode:
        # print(doc)
        venuesProfileViews.append(doc)
    return venuesProfileViews

# -----------------------------------------------------------------------------------------
# [GET] requestInaccuracy by venueID
@app.route("/getRequestInaccuracyByVenue/<id>")
def getRequestInaccuracyByVenue(id):
    # only get requestInaccuracy that has reviewStatus = False
    data = db.requestInaccuracy.find({"venueID": ObjectId(id), "reviewStatus": False})
    if data is None:
        return []
    allRequestInaccuracy = []
    #parse bson as json
    dataEncode = parse_json(data)
    for doc in dataEncode:
        # print(doc)
        allRequestInaccuracy.append(doc)
    return allRequestInaccuracy

# -----------------------------------------------------------------------------------------
# [GET] Badges
@app.route("/getBadges")
def getBadges():
    #this step finds all the items in the collection, specifying Badges
    data = db.badges.find({})
    #have to use data.clone so that cursor is not used up
    print(len(list(data.clone())))
    allBadges = []
    #parse bson as json
    dataEncode = parse_json(data)
    for doc in dataEncode:
        # print(doc)
        allBadges.append(doc)
    return allBadges

# -----------------------------------------------------------------------------------------
# [GET] Specific Token
@app.route("/getToken/<token>")
def getToken(token):
    data = db.tokens.find_one({"token": token})
    if data is None:
        return []
    return parse_json(data)

# [GET] Specific Token By requestId
@app.route("/getTokenByRequestId/<requestId>")
def getTokenByRequestId(requestId):
    data = db.tokens.find_one({"requestId": ObjectId(requestId)})
    if data is None:
        return []
    return parse_json(data)

# -----------------------------------------------------------------------------------------
# [GET] Specific Request
@app.route("/getAccountRequest/<id>")
def getAccountRequest(id):
    data = db.accountRequests.find_one({"_id": ObjectId(id)})
    if data is None:
        return []
    return parse_json(data)

# -----------------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port = 5000)