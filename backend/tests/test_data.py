import unittest
from backend.data import countries, listings, producers, reviews, users, venues, drinkTypes, requestEdits, requestListings,modRequests,requestInaccuracy,flavourTags,languages,observationTags,colours,specialColours
from datetime import datetime
import unittest
from backend.data import users
from datetime import datetime
import unittest
# from your_module import flavourTags

class TestData(unittest.TestCase):
    def test_countries(self):
        # Test case 1: Check if the origin country is set correctly
        country = countries(originCountry="USA", legalAge="21")
        self.assertEqual(country.originCountry, "USA")

        # Test case 2: Check if the legal age is set correctly
        country = countries(originCountry="USA", legalAge="21")
        self.assertEqual(country.legalAge, "21")

        # Test case 3: Check if the origin country is None when not provided
        self.assertRaises(TypeError, countries)

    def test_listings(self):
        # Test case 1: Check if the listing name is set correctly
        listing = listings(listingName="Listing A", producerID=object(), bottler="Bottler A", originCountry="USA", drinkType="Type A", abv=40.0, officialDesc="Description A", addedDate=datetime.now(), allowMod=True)
        self.assertEqual(listing.listingName, "Listing A")

        # Test case 2: Check if the producer ID is set correctly
        producer_id = object()
        listing = listings(listingName="Listing A", producerID=producer_id, bottler="Bottler A", originCountry="USA", drinkType="Type A", abv=40.0, officialDesc="Description A", addedDate=datetime.now(), allowMod=True)
        self.assertEqual(listing.producerID, producer_id)

        # Test case 3: Check if the bottler is set correctly
        listing = listings(listingName="Listing A", producerID=object(), bottler="Bottler A", originCountry="USA", drinkType="Type A", abv=40.0, officialDesc="Description A", addedDate=datetime.now(), allowMod=True)
        self.assertEqual(listing.bottler, "Bottler A")

        # Test case 4: Check if the origin country is set correctly
        listing = listings(listingName="Listing A", producerID=object(), bottler="Bottler A", originCountry="USA", drinkType="Type A", abv=40.0, officialDesc="Description A", addedDate=datetime.now(), allowMod=True)
        self.assertEqual(listing.originCountry, "USA")

        # Test case 5: Check if the drink type is set correctly
        listing = listings(listingName="Listing A", producerID=object(), bottler="Bottler A", originCountry="USA", drinkType="Type A", abv=40.0, officialDesc="Description A", addedDate=datetime.now(), allowMod=True)
        self.assertEqual(listing.drinkType, "Type A")

        # Test case 6: Check if the ABV is set correctly
        listing = listings(listingName="Listing A", producerID=object(), bottler="Bottler A", originCountry="USA", drinkType="Type A", abv=40.0, officialDesc="Description A", addedDate=datetime.now(), allowMod=True)
        self.assertEqual(listing.abv, 40.0)

        # Test case 7: Check if the official description is set correctly
        listing = listings(listingName="Listing A", producerID=object(), bottler="Bottler A", originCountry="USA", drinkType="Type A", abv=40.0, officialDesc="Description A", addedDate=datetime.now(), allowMod=True)
        self.assertEqual(listing.officialDesc, "Description A")

        # Test case 8: Check if the added date is set correctly
        now = datetime.now()
        listing = listings(listingName="Listing A", producerID=object(), bottler="Bottler A", originCountry="USA", drinkType="Type A", abv=40.0, officialDesc="Description A", addedDate=now, allowMod=True)
        self.assertEqual(listing.addedDate, now)

        # Test case 9: Check if the allow modification flag is set correctly
        listing = listings(listingName="Listing A", producerID=object(), bottler="Bottler A", originCountry="USA", drinkType="Type A", abv=40.0, officialDesc="Description A", addedDate=datetime.now(), allowMod=True)
        self.assertTrue(listing.allowMod)

        # Test case 10: Check if the age is None when not provided
        listing = listings(listingName="Listing A", producerID=object(), bottler="Bottler A", originCountry="USA", drinkType="Type A", abv=40.0, officialDesc="Description A", addedDate=datetime.now(), allowMod=True)
        self.assertIsNone(listing.age)

        # Test case 11: Check if the photo is None when not provided
        listing = listings(listingName="Listing A", producerID=object(), bottler="Bottler A", originCountry="USA", drinkType="Type A", abv=40.0, officialDesc="Description A", addedDate=datetime.now(), allowMod=True)
        self.assertIsNone(listing.photo)

        # Test case 12: Check if the type category is None when not provided
        listing = listings(listingName="Listing A", producerID=object(), bottler="Bottler A", originCountry="USA", drinkType="Type A", abv=40.0, officialDesc="Description A", addedDate=datetime.now(), allowMod=True)
        self.assertIsNone(listing.typeCategory)

        # Test case 13: Check if the review link is None when not provided
        listing = listings(listingName="Listing A", producerID=object(), bottler="Bottler A", originCountry="USA", drinkType="Type A", abv=40.0, officialDesc="Description A", addedDate=datetime.now(), allowMod=True)
        self.assertIsNone(listing.reviewLink)

        # Test case 14: Check if the source link is None when not provided
        listing = listings(listingName="Listing A", producerID=object(), bottler="Bottler A", originCountry="USA", drinkType="Type A", abv=40.0, officialDesc="Description A", addedDate=datetime.now(), allowMod=True)
        self.assertIsNone(listing.sourceLink)

    def test_producers(self):
        # Test case 1: Check if the producer name is set correctly
        producer = producers(producerName="Producer A", producerDesc="Description A", originCountry="Country A", mainDrinks=[], hashedPassword="password123", photo="producer.jpg", claimStatus=True)
        self.assertEqual(producer.producerName, "Producer A")

        # Test case 2: Check if the producer description is set correctly
        producer = producers(producerName="Producer A", producerDesc="Description A", originCountry="Country A", mainDrinks=[], hashedPassword="password123", photo="producer.jpg", claimStatus=True)
        self.assertEqual(producer.producerDesc, "Description A")

        # Test case 3: Check if the origin country is set correctly
        producer = producers(producerName="Producer A", producerDesc="Description A", originCountry="Country A", mainDrinks=[], hashedPassword="password123", photo="producer.jpg", claimStatus=True)
        self.assertEqual(producer.originCountry, "Country A")

        # Test case 4: Check if the main drinks list is set correctly
        main_drinks = ["Drink A", "Drink B", "Drink C"]
        producer = producers(producerName="Producer A", producerDesc="Description A", originCountry="Country A", mainDrinks=main_drinks, hashedPassword="password123", photo="producer.jpg", claimStatus=True)
        self.assertEqual(producer.mainDrinks, main_drinks)

        # Test case 5: Check if the hashed password is set correctly
        producer = producers(producerName="Producer A", producerDesc="Description A", originCountry="Country A", mainDrinks=[], hashedPassword="password123", photo="producer.jpg", claimStatus=True)
        self.assertEqual(producer.hashedPassword, "password123")

        # Test case 6: Check if the photo is set correctly
        producer = producers(producerName="Producer A", producerDesc="Description A", originCountry="Country A", mainDrinks=[], hashedPassword="password123", photo="producer.jpg", claimStatus=True)
        self.assertEqual(producer.photo, "producer.jpg")

        # Test case 7: Check if the claim status is set correctly
        producer = producers(producerName="Producer A", producerDesc="Description A", originCountry="Country A", mainDrinks=[], hashedPassword="password123", photo="producer.jpg", claimStatus=True)
        self.assertTrue(producer.claimStatus)

        # Test case 8: Check if the question answers list is set correctly
        question_answers = ["Answer A", "Answer B", "Answer C"]
        producer = producers(producerName="Producer A", producerDesc="Description A", originCountry="Country A", mainDrinks=[], hashedPassword="password123", photo="producer.jpg", claimStatus=True, questionAnswers=question_answers)
        self.assertEqual(producer.questionAnswers, question_answers)

        # Test case 9: Check if the updates list is set correctly
        updates = ["Update A", "Update B", "Update C"]
        producer = producers(producerName="Producer A", producerDesc="Description A", originCountry="Country A", mainDrinks=[], hashedPassword="password123", photo="producer.jpg", claimStatus=True, updates=updates)
        self.assertEqual(producer.updates, updates)

        # Test case 10: Check if the status OB is set correctly
        producer = producers(producerName="Producer A", producerDesc="Description A", originCountry="Country A", mainDrinks=[], hashedPassword="password123", photo="producer.jpg", claimStatus=True, statusOB="Status A")
        self.assertEqual(producer.statusOB, "Status A")

        # Test case 11: Check if the producer link is set correctly
        producer = producers(producerName="Producer A", producerDesc="Description A", originCountry="Country A", mainDrinks=[], hashedPassword="password123", photo="producer.jpg", claimStatus=True, producerLink="https://example.com")
        self.assertEqual(producer.producerLink, "https://example.com")

    def test_reviews(self):
        # Test case 1: Check if the userID is set correctly
        user_id = object()
        review = reviews(userID=user_id, reviewTarget=object(), rating=5, reviewDesc="Great product", reviewType="Venue", createdDate=datetime.now(), language="English", finish="Smooth", willRecommend=True, wouldBuyAgain=True, userVotes=object(), photo="review.jpg")
        self.assertEqual(review.userID, user_id)

        # Test case 2: Check if the review target is set correctly
        review_target = object()
        review = reviews(userID=object(), reviewTarget=review_target, rating=5, reviewDesc="Great product", reviewType="Venue", createdDate=datetime.now(), language="English", finish="Smooth", willRecommend=True, wouldBuyAgain=True, userVotes=object(), photo="review.jpg")
        self.assertEqual(review.reviewTarget, review_target)

        # Test case 3: Check if the rating is set correctly
        review = reviews(userID=object(), reviewTarget=object(), rating=5, reviewDesc="Great product", reviewType="Venue", createdDate=datetime.now(), language="English", finish="Smooth", willRecommend=True, wouldBuyAgain=True, userVotes=object(), photo="review.jpg")
        self.assertEqual(review.rating, 5)

        # Test case 4: Check if the review description is set correctly
        review = reviews(userID=object(), reviewTarget=object(), rating=5, reviewDesc="Great product", reviewType="Venue", createdDate=datetime.now(), language="English", finish="Smooth", willRecommend=True, wouldBuyAgain=True, userVotes=object(), photo="review.jpg")
        self.assertEqual(review.reviewDesc, "Great product")

        # Test case 5: Check if the review type is set correctly
        review = reviews(userID=object(), reviewTarget=object(), rating=5, reviewDesc="Great product", reviewType="Venue", createdDate=datetime.now(), language="English", finish="Smooth", willRecommend=True, wouldBuyAgain=True, userVotes=object(), photo="review.jpg")
        self.assertEqual(review.reviewType, "Venue")

        # Test case 6: Check if the created date is set correctly
        now = datetime.now()
        review = reviews(userID=object(), reviewTarget=object(), rating=5, reviewDesc="Great product", reviewType="Venue", createdDate=now, language="English", finish="Smooth", willRecommend=True, wouldBuyAgain=True, userVotes=object(), photo="review.jpg")
        self.assertEqual(review.createdDate, now)

        # Test case 7: Check if the language is set correctly
        review = reviews(userID=object(), reviewTarget=object(), rating=5, reviewDesc="Great product", reviewType="Venue", createdDate=datetime.now(), language="English", finish="Smooth", willRecommend=True, wouldBuyAgain=True, userVotes=object(), photo="review.jpg")
        self.assertEqual(review.language, "English")

        # Test case 8: Check if the finish is set correctly
        review = reviews(userID=object(), reviewTarget=object(), rating=5, reviewDesc="Great product", reviewType="Venue", createdDate=datetime.now(), language="English", finish="Smooth", willRecommend=True, wouldBuyAgain=True, userVotes=object(), photo="review.jpg")
        self.assertEqual(review.finish, "Smooth")

        # Test case 9: Check if the will recommend flag is set correctly
        review = reviews(userID=object(), reviewTarget=object(), rating=5, reviewDesc="Great product", reviewType="Venue", createdDate=datetime.now(), language="English", finish="Smooth", willRecommend=True, wouldBuyAgain=True, userVotes=object(), photo="review.jpg")
        self.assertTrue(review.willRecommend)

        # Test case 10: Check if the would buy again flag is set correctly
        review = reviews(userID=object(), reviewTarget=object(), rating=5, reviewDesc="Great product", reviewType="Venue", createdDate=datetime.now(), language="English", finish="Smooth", willRecommend=True, wouldBuyAgain=True, userVotes=object(), photo="review.jpg")
        self.assertTrue(review.wouldBuyAgain)

        # Test case 11: Check if the photo is set correctly
        review = reviews(userID=object(), reviewTarget=object(), rating=5, reviewDesc="Great product", reviewType="Venue", createdDate=datetime.now(), language="English", finish="Smooth", willRecommend=True, wouldBuyAgain=True, userVotes=object(), photo="review.jpg")
        self.assertEqual(review.photo, "review.jpg")

        # Test case 12: Check if the colour is None when not provided
        review = reviews(userID=object(), reviewTarget=object(), rating=5, reviewDesc="Great product", reviewType="Venue", createdDate=datetime.now(), language="English", finish="Smooth", willRecommend=True, wouldBuyAgain=True, userVotes=object(), photo="review.jpg")
        self.assertIsNone(review.colour)

        # Test case 13: Check if the aroma is None when not provided
        review = reviews(userID=object(), reviewTarget=object(), rating=5, reviewDesc="Great product", reviewType="Venue", createdDate=datetime.now(), language="English", finish="Smooth", willRecommend=True, wouldBuyAgain=True, userVotes=object(), photo="review.jpg")
        self.assertIsNone(review.aroma)

        # Test case 14: Check if the location is None when not provided
        review = reviews(userID=object(), reviewTarget=object(), rating=5, reviewDesc="Great product", reviewType="Venue", createdDate=datetime.now(), language="English", finish="Smooth", willRecommend=True, wouldBuyAgain=True, userVotes=object(), photo="review.jpg")
        self.assertIsNone(review.location)

        # Test case 15: Check if the taste is None when not provided
        review = reviews(userID=object(), reviewTarget=object(), rating=5, reviewDesc="Great product", reviewType="Venue", createdDate=datetime.now(), language="English", finish="Smooth", willRecommend=True, wouldBuyAgain=True, userVotes=object(), photo="review.jpg")
        self.assertIsNone(review.taste)

        # Test case 16: Check if the tagged users is None when not provided
        review = reviews(userID=object(), reviewTarget=object(), rating=5, reviewDesc="Great product", reviewType="Venue", createdDate=datetime.now(), language="English", finish="Smooth", willRecommend=True, wouldBuyAgain=True, userVotes=object(), photo="review.jpg")
        self.assertIsNone(review.taggedUsers)

        # Test case 17: Check if the flavor tag is None when not provided
        review = reviews(userID=object(), reviewTarget=object(), rating=5, reviewDesc="Great product", reviewType="Venue", createdDate=datetime.now(), language="English", finish="Smooth", willRecommend=True, wouldBuyAgain=True, userVotes=object(), photo="review.jpg")
        self.assertIsNone(review.flavorTag)

        # Test case 18: Check if the observation tag is None when not provided
        review = reviews(userID=object(), reviewTarget=object(), rating=5, reviewDesc="Great product", reviewType="Venue", createdDate=datetime.now(), language="English", finish="Smooth", willRecommend=True, wouldBuyAgain=True, userVotes=object(), photo="review.jpg")
        self.assertIsNone(review.observationTag)

    
    def test_users(self):

        # Test case 1: Check if the username is set correctly
        user = users(username="john_doe", displayName="John Doe", choiceDrinks=[], drinkLists=None, modType=[], photo="john.jpg", hashedPassword="password123", joinDate=datetime.now(), followLists=None, firstName="John", lastName="Doe", email="john.doe@example.com", isAdmin=False, birthday=datetime.now())
        self.assertEqual(user.username, "john_doe")

        # Test case 2: Check if the display name is set correctly
        user = users(username="john_doe", displayName="John Doe", choiceDrinks=[], drinkLists=None, modType=[], photo="john.jpg", hashedPassword="password123", joinDate=datetime.now(), followLists=None, firstName="John", lastName="Doe", email="john.doe@example.com", isAdmin=False, birthday=datetime.now())
        self.assertEqual(user.displayName, "John Doe")

        # Test case 3: Check if the choice drinks list is set correctly
        choice_drinks = ["Drink A", "Drink B", "Drink C"]
        user = users(username="john_doe", displayName="John Doe", choiceDrinks=choice_drinks, drinkLists=None, modType=[], photo="john.jpg", hashedPassword="password123", joinDate=datetime.now(), followLists=None, firstName="John", lastName="Doe", email="john.doe@example.com", isAdmin=False, birthday=datetime.now())
        self.assertEqual(user.choiceDrinks, choice_drinks)

        # Test case 4: Check if the drink lists object is set correctly
        drink_lists = object()
        user = users(username="john_doe", displayName="John Doe", choiceDrinks=[], drinkLists=drink_lists, modType=[], photo="john.jpg", hashedPassword="password123", joinDate=datetime.now(), followLists=None, firstName="John", lastName="Doe", email="john.doe@example.com", isAdmin=False, birthday=datetime.now())
        self.assertEqual(user.drinkLists, drink_lists)

        # Test case 5: Check if the mod type list is set correctly
        mod_type = ["Type A", "Type B", "Type C"]
        user = users(username="john_doe", displayName="John Doe", choiceDrinks=[], drinkLists=None, modType=mod_type, photo="john.jpg", hashedPassword="password123", joinDate=datetime.now(), followLists=None, firstName="John", lastName="Doe", email="john.doe@example.com", isAdmin=False, birthday=datetime.now())
        self.assertEqual(user.modType, mod_type)

        # Test case 6: Check if the photo is set correctly
        user = users(username="john_doe", displayName="John Doe", choiceDrinks=[], drinkLists=None, modType=[], photo="john.jpg", hashedPassword="password123", joinDate=datetime.now(), followLists=None, firstName="John", lastName="Doe", email="john.doe@example.com", isAdmin=False, birthday=datetime.now())
        self.assertEqual(user.photo, "john.jpg")

        # Test case 7: Check if the hashed password is present
        user = users(username="JohnDoe", displayName="John Doe", choiceDrinks=[], drinkLists=None, modType=[], photo="", hashedPassword="password123", joinDate=datetime.now(), followLists=None, firstName="John", lastName="Doe", email="john.doe@example.com", isAdmin=False, birthday=datetime.now())
        self.assertTrue(hasattr(user, "hashedPassword"))

        # Test case 8: Check if followList is an object 
        follow_lists = object()
        user = users(username="JohnDoe", displayName="John Doe", choiceDrinks=[], drinkLists=None, modType=[], photo="", hashedPassword="password123", joinDate=datetime.now(), followLists=follow_lists, firstName="John", lastName="Doe", email="john.doe@example.com", isAdmin=False, birthday=datetime.now())
        self.assertEqual(user.followLists, follow_lists)

    
    def test_venues(self):

        # Test case 1: Check if the venue name is set correctly
        venue = venues(venueName="Venue A", address="Address A", venueType="Type A", venueDesc="Description A", originLocation="Location A", menu=[], photo="photo.jpg", claimStatus=True, openingHours=object(), hashedPassword="password123")
        self.assertEqual(venue.venueName, "Venue A")

        # Test case 2: Check if the address is set correctly
        venue = venues(venueName="Venue A", address="Address A", venueType="Type A", venueDesc="Description A", originLocation="Location A", menu=[], photo="photo.jpg", claimStatus=True, openingHours=object(), hashedPassword="password123")
        self.assertEqual(venue.address, "Address A")

        # Test case 3: Check if the venue type is set correctly
        venue = venues(venueName="Venue A", address="Address A", venueType="Type A", venueDesc="Description A", originLocation="Location A", menu=[], photo="photo.jpg", claimStatus=True, openingHours=object(), hashedPassword="password123")
        self.assertEqual(venue.venueType, "Type A")

        # Test case 4: Check if the venue description is set correctly
        venue = venues(venueName="Venue A", address="Address A", venueType="Type A", venueDesc="Description A", originLocation="Location A", menu=[], photo="photo.jpg", claimStatus=True, openingHours=object(), hashedPassword="password123")
        self.assertEqual(venue.venueDesc, "Description A")

        # Test case 5: Check if the origin location is set correctly
        venue = venues(venueName="Venue A", address="Address A", venueType="Type A", venueDesc="Description A", originLocation="Location A", menu=[], photo="photo.jpg", claimStatus=True, openingHours=object(), hashedPassword="password123")
        self.assertEqual(venue.originLocation, "Location A")

        # Test case 6: Check if the menu list is set correctly
        menu = ["Item A", "Item B", "Item C"]
        venue = venues(venueName="Venue A", address="Address A", venueType="Type A", venueDesc="Description A", originLocation="Location A", menu=menu, photo="photo.jpg", claimStatus=True, openingHours=object(), hashedPassword="password123")
        self.assertEqual(venue.menu, menu)

        # Test case 7: Check if the photo is set correctly
        venue = venues(venueName="Venue A", address="Address A", venueType="Type A", venueDesc="Description A", originLocation="Location A", menu=[], photo="photo.jpg", claimStatus=True, openingHours=object(), hashedPassword="password123")
        self.assertEqual(venue.photo, "photo.jpg")

        # Test case 8: Check if the claim status is set correctly
        venue = venues(venueName="Venue A", address="Address A", venueType="Type A", venueDesc="Description A", originLocation="Location A", menu=[], photo="photo.jpg", claimStatus=True, openingHours=object(), hashedPassword="password123")
        self.assertEqual(venue.claimStatus, True)

        # Test case 9: Check if the opening hours object is set correctly
        opening_hours = object()
        venue = venues(venueName="Venue A", address="Address A", venueType="Type A", venueDesc="Description A", originLocation="Location A", menu=[], photo="photo.jpg", claimStatus=True, openingHours=opening_hours, hashedPassword="password123")
        self.assertEqual(venue.openingHours, opening_hours)

        # Test case 10: Check if the hashed password is set correctly
        venue = venues(venueName="Venue A", address="Address A", venueType="Type A", venueDesc="Description A", originLocation="Location A", menu=[], photo="photo.jpg", claimStatus=True, openingHours=object(), hashedPassword="password123")
        self.assertEqual(venue.hashedPassword, "password123")

        # Test case 11: Check if the question answers list is set correctly (optional)
        question_answers = ["Answer A", "Answer B", "Answer C"]
        venue = venues(venueName="Venue A", address="Address A", venueType="Type A", venueDesc="Description A", originLocation="Location A", menu=[], photo="photo.jpg", claimStatus=True, openingHours=object(), hashedPassword="password123", questionAnswers=question_answers)
        self.assertEqual(venue.questionAnswers, question_answers)

        # Test case 12: Check if the updates list is set correctly (optional)
        updates = ["Update A", "Update B", "Update C"]
        venue = venues(venueName="Venue A", address="Address A", venueType="Type A", venueDesc="Description A", originLocation="Location A", menu=[], photo="photo.jpg", claimStatus=True, openingHours=object(), hashedPassword="password123", updates=updates)
        self.assertEqual(venue.updates, updates)



    def test_drinkTypes(self):
        # Test case 1: Check if the drink type is set correctly
        drink_type = "Type A"
        dt = drinkTypes(drinkType=drink_type)
        self.assertEqual(dt.drinkType, drink_type)

        # Test case 2: Check if the type category is set correctly
        type_category = ["Category A", "Category B", "Category C"]
        dt = drinkTypes(drinkType="Type A", typeCategory=type_category)
        self.assertEqual(dt.typeCategory, type_category)

        # Test case 3: Check if the type category is None by default
        dt = drinkTypes(drinkType="Type A")
        self.assertIsNone(dt.typeCategory)

    def test_requestListings(self):
        # Test case 1: Check if the listing name is set correctly
        listing_name = "Listing A"
        request_listing = requestListings(listingName=listing_name, bottler="Bottler A", drinkType="Drink Type A", sourceLink="Source Link A", brandRelation="Brand Relation A", reviewStatus=True, userID=object(), photo="Photo A")
        self.assertEqual(request_listing.listingName, listing_name)

        # Test case 2: Check if the bottler is set correctly
        bottler = "Bottler A"
        request_listing = requestListings(listingName="Listing A", bottler=bottler, drinkType="Drink Type A", sourceLink="Source Link A", brandRelation="Brand Relation A", reviewStatus=True, userID=object(), photo="Photo A")
        self.assertEqual(request_listing.bottler, bottler)

        # Test case 3: Check if the drink type is set correctly
        drink_type = "Drink Type A"
        request_listing = requestListings(listingName="Listing A", bottler="Bottler A", drinkType=drink_type, sourceLink="Source Link A", brandRelation="Brand Relation A", reviewStatus=True, userID=object(), photo="Photo A")
        self.assertEqual(request_listing.drinkType, drink_type)

        # Test case 4: Check if the source link is set correctly
        source_link = "Source Link A"
        request_listing = requestListings(listingName="Listing A", bottler="Bottler A", drinkType="Drink Type A", sourceLink=source_link, brandRelation="Brand Relation A", reviewStatus=True, userID=object(), photo="Photo A")
        self.assertEqual(request_listing.sourceLink, source_link)

        # Test case 5: Check if the brand relation is set correctly
        brand_relation = "Brand Relation A"
        request_listing = requestListings(listingName="Listing A", bottler="Bottler A", drinkType="Drink Type A", sourceLink="Source Link A", brandRelation=brand_relation, reviewStatus=True, userID=object(), photo="Photo A")
        self.assertEqual(request_listing.brandRelation, brand_relation)

        # Test case 6: Check if the review status is set correctly
        request_listing = requestListings(listingName="Listing A", bottler="Bottler A", drinkType="Drink Type A", sourceLink="Source Link A", brandRelation="Brand Relation A", reviewStatus=True, userID=object(), photo="Photo A")
        self.assertTrue(request_listing.reviewStatus)

        # Test case 7: Check if the user ID is set correctly
        user_id = object()
        request_listing = requestListings(listingName="Listing A", bottler="Bottler A", drinkType="Drink Type A", sourceLink="Source Link A", brandRelation="Brand Relation A", reviewStatus=True, userID=user_id, photo="Photo A")
        self.assertEqual(request_listing.userID, user_id)

        # Test case 8: Check if the photo is set correctly
        photo = "Photo A"
        request_listing = requestListings(listingName="Listing A", bottler="Bottler A", drinkType="Drink Type A", sourceLink="Source Link A", brandRelation="Brand Relation A", reviewStatus=True, userID=object(), photo=photo)
        self.assertEqual(request_listing.photo, photo)

        # Test case 9: Check if the optional fields are set correctly
        producer_new = "Producer New A"
        producer_id = object()
        origin_country = "Origin Country A"
        type_category = "Type Category A"
        age = "Age A"
        abv = "ABV A"
        review_link = "Review Link A"
        request_listing = requestListings(listingName="Listing A", bottler="Bottler A", drinkType="Drink Type A", sourceLink="Source Link A", brandRelation="Brand Relation A", reviewStatus=True, userID=object(), photo="Photo A", producerNew=producer_new, producerID=producer_id, originCountry=origin_country, typeCategory=type_category, age=age, abv=abv, reviewLink=review_link)
        self.assertEqual(request_listing.producerNew, producer_new)
        self.assertEqual(request_listing.producerID, producer_id)
        self.assertEqual(request_listing.originCountry, origin_country)
        self.assertEqual(request_listing.typeCategory, type_category)
        self.assertEqual(request_listing.age, age)
        self.assertEqual(request_listing.abv, abv)
        self.assertEqual(request_listing.reviewLink, review_link)

    def test_requestEdits(self):
        # Test case 1: Check if the edit description is set correctly
        edit_desc = "Edit Description A"
        request_edit = requestEdits(editDesc=edit_desc, brandRelation="Brand Relation A", listingID=object(), userID=object(), reviewStatus=True)
        self.assertEqual(request_edit.editDesc, edit_desc)

        # Test case 2: Check if the brand relation is set correctly
        brand_relation = "Brand Relation A"
        request_edit = requestEdits(editDesc="Edit Description A", brandRelation=brand_relation, listingID=object(), userID=object(), reviewStatus=True)
        self.assertEqual(request_edit.brandRelation, brand_relation)

        # Test case 3: Check if the listing ID is set correctly
        listing_id = object()
        request_edit = requestEdits(editDesc="Edit Description A", brandRelation="Brand Relation A", listingID=listing_id, userID=object(), reviewStatus=True)
        self.assertEqual(request_edit.listingID, listing_id)

        # Test case 4: Check if the user ID is set correctly
        user_id = object()
        request_edit = requestEdits(editDesc="Edit Description A", brandRelation="Brand Relation A", listingID=object(), userID=user_id, reviewStatus=True)
        self.assertEqual(request_edit.userID, user_id)

        # Test case 5: Check if the review status is set correctly
        request_edit = requestEdits(editDesc="Edit Description A", brandRelation="Brand Relation A", listingID=object(), userID=object(), reviewStatus=True)
        self.assertTrue(request_edit.reviewStatus)

        # Test case 6: Check if the duplicate link is set correctly
        duplicate_link = "Duplicate Link A"
        request_edit = requestEdits(editDesc="Edit Description A", brandRelation="Brand Relation A", listingID=object(), userID=object(), reviewStatus=True, duplicateLink=duplicate_link)
        self.assertEqual(request_edit.duplicateLink, duplicate_link)

        # Test case 7: Check if the source link is set correctly
        source_link = "Source Link A"
        request_edit = requestEdits(editDesc="Edit Description A", brandRelation="Brand Relation A", listingID=object(), userID=object(), reviewStatus=True, sourceLink=source_link)
        self.assertEqual(request_edit.sourceLink, source_link)

        # Test case 8: Check if the optional fields are set correctly
        request_edit = requestEdits(editDesc="Edit Description A", brandRelation="Brand Relation A", listingID=object(), userID=object(), reviewStatus=True)
        self.assertIsNone(request_edit.duplicateLink)
        self.assertIsNone(request_edit.sourceLink)

    def test_modRequests(self):
        # Test case 1: Check if the userID is set correctly
        user_id = object()
        mod_request = modRequests(userID=user_id, drinkType="Drink Type A", modDesc="Mod Description A",reviewStatus=True)
        self.assertEqual(mod_request.userID, user_id)

        # Test case 2: Check if the drink type is set correctly
        drink_type = "Drink Type A"
        mod_request = modRequests(userID=object(), drinkType=drink_type, modDesc="Mod Description A",reviewStatus=True)
        self.assertEqual(mod_request.drinkType, drink_type)

        # Test case 3: Check if the mod description is set correctly
        mod_desc = "Mod Description A"
        mod_request = modRequests(userID=object(), drinkType="Drink Type A", modDesc=mod_desc,reviewStatus=True)
        self.assertEqual(mod_request.modDesc, mod_desc)

    def test_requestInaccuracy(self):

        # Test case 1: Check if the listing ID is set correctly
        listing_id = object()
        request_inaccuracy = requestInaccuracy(listingID=listing_id, userID=object(), venueID=object(), inaccurateReason="Reason A")
        self.assertEqual(request_inaccuracy.listingID, listing_id)

        # Test case 2: Check if the user ID is set correctly
        user_id = object()
        request_inaccuracy = requestInaccuracy(listingID=object(), userID=user_id, venueID=object(), inaccurateReason="Reason A")
        self.assertEqual(request_inaccuracy.userID, user_id)

        # Test case 3: Check if the venue ID is set correctly
        venue_id = object()
        request_inaccuracy = requestInaccuracy(listingID=object(), userID=object(), venueID=venue_id, inaccurateReason="Reason A")
        self.assertEqual(request_inaccuracy.venueID, venue_id)

        # Test case 4: Check if the inaccurate reason is set correctly
        inaccurate_reason = "Reason A"
        request_inaccuracy = requestInaccuracy(listingID=object(), userID=object(), venueID=object(), inaccurateReason=inaccurate_reason)
        self.assertEqual(request_inaccuracy.inaccurateReason, inaccurate_reason)

        # Test case 5: Check if the inaccurate reason is None when not provided
        request_inaccuracy = requestInaccuracy(listingID=object(), userID=object(), venueID=object())
        self.assertIsNone(request_inaccuracy.inaccurateReason)


    def test_flavourTags(self):
        # Test case 1: Check if the hexcode is set correctly
        hexcode = "#FF0000"
        flavour_tag = flavourTags(hexcode=hexcode, familyTag="Fruity")
        self.assertEqual(flavour_tag.hexcode, hexcode)

    
        # Test case 2: Check if the familyTag is set correctly
        family_tag = "Fruity"
        flavour_tag = flavourTags(hexcode="#FF0000", familyTag=family_tag)
        self.assertEqual(flavour_tag.familyTag, family_tag)

    def test_observation_tag(self):
        # Test case 1: Check if the observation tag is set correctly
        observation_tag = "Tag A"
        observation = observationTags(observationTag=observation_tag)
        self.assertEqual(observation.observationTag, observation_tag)

        # # Test case 2: Check if the observation tag is None when not provided
        # observation = observationTags()
        # self.assertIsNone(observation.observationTag)



    def test_colours(self):
        # Test case 1: Check if the hexcode is set correctly
        hexcode = "#FF0000"
        color = colours(hexcode=hexcode)
        self.assertEqual(color.hexcode, hexcode)

        # # Test case 2: Check if the hexcode is None when not provided
        # color = colours()
        # self.assertIsNone(color.hexcode)

    def test_specialColours(self):
        # Test case 1: Check if the hexList is set correctly
        hex_list = ["#FF0000", "#00FF00", "#0000FF"]
        special_color = specialColours(hexList=hex_list, colour="Red")
        self.assertEqual(special_color.hexList, hex_list)

        # Test case 2: Check if the colour is set correctly
        colour = "Red"
        special_color = specialColours(hexList=["#FF0000", "#00FF00", "#0000FF"], colour=colour)
        self.assertEqual(special_color.colour, colour)


    def test_language(self):
        # Test case 1: Check if the language is set correctly
        language = "English"
        lang = languages(language=language)
        self.assertEqual(lang.language, language)

        # # Test case 2: Check if the language is None when not provided
        # lang = languages()
        # self.assertIsNone(lang.language)








# if __name__ == '__main__':
#     unittest.main()

#     # TEST FOR PRESENCE OF HASHED PASSWORD
    

    

    

    
# if __name__ == '__main__':
#     unittest.main()


