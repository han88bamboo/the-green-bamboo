# -----------------------------------------------------------------------------------------
# getData.py
# Port: 5000
# Routes: /getAccountRequests (GET), /getCountries (GET), /getListings (GET), /getListing/<id> (GET), /getProducers (GET), /getProducer/<id> (GET),
#           /getReviews (GET), /getReviewByTarget/<id> (GET), /getUsers (GET), /getUser/<id> (GET), /getUserByUsername/<username> (GET), /getVenues (GET), 
#           /getVenue/<id> (GET), /getVenuesAPI (GET), /getDrinkTypes (GET), /getRequestListings (GET), /getRequestListing/<id> (GET), /getRequestEdits (GET), 
#           /getRequestEdit/<id> (GET), /getModRequests (GET), /getFlavourTags (GET), /getSubTags (GET), /getObservationTags (GET), /getColours (GET), 
#           /getSpecialColours (GET), /getLanguages (GET), /getServingTypes (GET), /getProducersProfileViews (GET), /getVenuesProfileViewsByVenue/<id> (GET), /getRequestInaccuracyByVenue/<id> (GET)

# -----------------------------------------------------------------------------------------
# createListing.py
# Port: 5001
# Routes: /createListing (POST)

# -----------------------------------------------------------------------------------------
# editListing.py
# Port: 5002
# Routes: /updateListing/<id> (PUT), /deleteListing/<id> (DELETE), /getDistance/<origins>/<destinations>/<key> (GET)

# -----------------------------------------------------------------------------------------
# requestListing.py
# Port: 5011
# Routes: /requestListing (POST), /requestListingModify/<requestID> (POST), /requestEdits (POST), /requestEditsModify/<requestID> (POST), /requestInaccuracy (POST), /requestReviewStatus/<requestID> (POST)

# -----------------------------------------------------------------------------------------
# createReview.py
# Port: 5021
# Routes: /createReview (POST)

# -----------------------------------------------------------------------------------------
# editReview.py
# Port: 5022
# Routes: /voteReview (POST), /updateReview/<id> (PUT)

# -----------------------------------------------------------------------------------------
# deleteReview.py
# Port: 5023
# Routes: /deleteReview/<id> (DELETE)

# -----------------------------------------------------------------------------------------
# authcheck.py
# Port: 5030
# Routes: /authcheck (POST), /authcheckUser (POST), /authcheckProducer (POST), /authcheckVenue (POST)

# -----------------------------------------------------------------------------------------
# createAccount.py
# Port: 5031
# Routes: /createAccount (POST), /createAccountRequest (POST), /updateAccountRequest (POST), /createProducerAccount (POST), /createVenueAccount (POST)

# -----------------------------------------------------------------------------------------
# editObservationTag.py
# Port: 5051
# Routes: /updateObservationTag (PUT)

# -----------------------------------------------------------------------------------------
# adminFunctions.py
# Port: 5052
# Routes: /createObservationTag (POST), /updateObservationTag (PUT), /deleteObservationTag/<id> (DELETE), /updateFamilyTag (POST), /updateSubTag (PUT), /deleteFamilyTag/<id> (DELETE), /deleteSubTag/<id> (DELETE), /importListings (POST), /createFamilyTag (POST), /createSubTag (POST), /importListings (POST), /readCSV (GET)

# -----------------------------------------------------------------------------------------
# addToList.py
# Port: 5070
# Routes: /updateListing/<id> (PUT), /deleteListing/<id> (DELETE)

# -----------------------------------------------------------------------------------------
# editModRequests.py
# Port: 5101
# Routes: /submitModRequest (POST), /updateModRequest (POST)

# -----------------------------------------------------------------------------------------
# editProducerProfile.py
# Port: 5200
# Routes: /editDetails (POST), /addUpdates (POST), /sendQuestions (POST), /sendAnswers (POST), /likeUpdates (POST), /unlikeUpdates (POST), /updateProducerStatus (POST), /addProfileCount (POST), /addNewProfileCount (POST), /editUpdate (POST), /deleteUpdate (POST), /editQA (POST), /deleteQA (POST)

# -----------------------------------------------------------------------------------------
# editProfile.py
# Port: 5100
# Routes: /editDetails (POST), /updateBookmark (POST), /updateFollowLists (POST), /updateModType (POST), /removeModType (POST)

# -----------------------------------------------------------------------------------------
# editVenueProfile.py
# Port: 5300
# Routes: /editDetails (POST), /addUpdates (POST), /sendQuestions (POST), /sendAnswers (POST), /likeUpdates (POST), /unlikeUpdates (POST)
#         /editAddress (POST), /editOpeningHours (POST), /editPublicHolidays (POST), /editReservationDetails (POST), /addListingToMenu (POST)
#         /editSectionName (PUT), /editMenu (POST), /updateVenueStatus (POST), /editUpdate (POST), /deleteUpdate (POST), /editQA (POST)
#         /deleteQA (POST), /addProfileCount (POST), /addNewProfileCount (POST)
