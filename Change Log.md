# Change Log for Drink-X

<!-- Instructions to all coders working on Drink-X:

Each time BEFORE you make ANY pull request / push changes to the Github repo, please create a new "update" section and indicate the nature and purpose of the changes below.

The purpose of this change log is to ensure that all  are working on the correct and most updated version of the code.

======================== Format ========================

# Update as of [DATE]
Coder: [xxx]

Purpose of the changes: (1) [xxx] (2) [xxx] (3) [xxx]

Nature of the changes (frontend / backend / database): [xxx]

======================== Format ========================
-->

# Update as of 13 March 2025

Coder: Danish
Purpose of the changes:
(1) Help Speed Up Bulk Upload Through Proposed Method of Threading
(2) Add A Tab to the Producer Page “Tours and Experience” and Add Feature for Users to Submit Reviews of Producers’ Tours + Edit Display of Fields
(3) Edit Code such that Independent Bottlers displayed drink listings can be clicked into and have their own producer page too.
(4) Fix bug where most popular “Flavour Tags” are not showing on the Drinks Listing page
(5) Help add fields to User Dashboard: Top Brands, Top Venues, Top Styles, Your Recent Activity
Nature of the changes (frontend / backend / database):
Frontend, backend and database

# Update as of 14 March

Coder: Danish
Purpose of the changes:
bugfixing for missing “drinks” column of “usersDrinkLists”
Nature of the changes (frontend / backend / database):
Database

# Update as of 15 March

Coder: Danish
Purpose of the changes:
(1) bugfixing for logic for independent bottlers when CSV file is uploaded
(2) allowing users to upload up to 3 images when submitting a review of a producer tour
Nature of the changes (frontend / backend / database):
Frontend, Backend

# Update as of 19 March

Coder: Dycia

Purpose of the changes:
(1) Added new tables (associations, pointsRecorder, pointSystemRules) -- 01-postgresql_data3.sql
(2) Updated new columns into "users" tables -- 01-postgresql_data3.sql
(3) Added new values for the newly created table (associations) -- 02-insert-data.sql
(4) Updated the users table value -- 02-insert-data.sql
(5) Changed the port number in docker-compose-db.yml

Nature of the changes (frontend / backend / database):
database

Coder: Dycia

Purpose of the changes:
(1) Added in a new file (rssFeed.py) - Backend API to fetch articles from 88bamboo.co. Returns a dictionary of articles
(2) Added new functions (getData.py) - (a) get_listings_by_observation_tag(tag): get the listings from listing table that matches the observation tag - (b) getTop8(): get the top 8 trending tags - (c) getTopListings(): get the top trending bottles - (d) getListingsName(): get all the listing names from listing table - (e) getRandomListings(): randomiser for the explore page
(3) Updated the packages (getData.py) - Added the neccessary packages to for the functions work in getData.py

Nature of the changes (frontend / backend / database):
backend

Coder: Dycia

Purpose of the changes:
(1) New Component - Landing Page Nav Bar (LandingPageNavBar.vue) - New nav bar for the landing page. Centered the logo and removed the search bar.
(2) New Component - Autocomplete Search Bar (SearchBar.vue) - New autocomplete search bar for the landing page.
(3) Updated Page - Landing page (LandingPage.vue) - New UI design for the landing page - Implemented the trending tags and drink - Implemented the articles from 88bamboo.co

Nature of the changes (frontend / backend / database):
frontend

Coder: Dycia

Purpose of the changes:
(1) add_preferences(username): update the database with the user's preferences (createAccount.py)
(2) editDetails(): updated the edit detail function to include the updating of database when user changes flavour tag and observation tags preferences (editProfile.py)

Nature of the changes (frontend / backend / database):
backend

Coder: Dycia

Purpose of the changes:
(1) Updated Component - OnboardPopup (OnboardPopup.vue) - Fixed the routing of search bar and exit button.
(2) Updated Component - ReusablePopup (ReusablePopup.vue) - Dynamic retrieval of drink type, flavour tags and observation tag from database to be displayed in the popup form to record user preference.
(3) Updated Page - SignUpPage (SignUpPage.vue) - Implemented the reusuable popups to collect the user preferences
(4) New Page - RandomExplorePage (RandomExplorePage.vue) - Replaces the current explore page. It randomises the listing for each reload.
(5) Updated Component - Nav Bar (NavBar.vue) - Added in the routing for future for you page as well as routed explore to "RandomExplorePage.vue"
(6) Updated Page - Profie Page (UserProfileRefactor.vue) - Implemented the feature to update flavour tag and observation tag preference. - Dynamic display of updated choices. - Routed the buttons in the "Welcome" section.
(7) Updated Routing (index.js) - Updated the routing for /explore to route it to "RandomExplorePage.vue"

Nature of the changes (frontend / backend / database):
frontend

# Update as of 20 March

Coder: Carissa

Purpose of the changes:
(1) Updated Page - LandingPage (LandingPage.vue) - changed card layout of icon buttons back to the original, routed text on icon buttons, colour of text changes when hovered over
(2) Updated Logic (LandingPage.vue) - included a list called fallbackTags in case there is insufficient review to obtain the trending tags or API call failed, updated function fetchTop8() to do the switch between fallbackTags when there are sufficient reviews

Nature of the changes (frontend / backend / database):
frontend

Coder: Dycia

Purpose of the changes:
(1) Updated Backend API (getData.py) - Updated getTopListings() such that when there is no reviews there is a fallback algorithm that retrieve the trending drinks based on addedDate. - Code summary: getTopListings, retrieves the top 6 bottle listings from a database, prioritizing listings with the highest number of reviews.
If fewer than 6 listings have reviews, additional listings are fetched based on the most recently added ones. The function ensures that listings with reviews are prioritized while filling
the remaining slots with newly added listings.

Nature of the changes (frontend / backend / database):
backend

Coder: Dycia

Purpose of the changes:
(1) Updated Database (02-insert-data.sql) - Removed all the insert query from "reviews" table - Removed all the insert query from "reviewsUserVotes" table because it is linked to the reviews in the "reviews" table. Thus, if there is no reviews in the "reviews" table
there cannot be any insert query for "reviewsUserVotes"

Nature of the changes (frontend / backend / database):
database

Coder: Dycia

Purpose of the changes:
(1) Updated Component - LandingPageNavBar (LandingPageNavBar.vue) - Removed the routing for "For You" page
(2) Updated Component - NavBar (NavBar.vue) - Removed the routing for "For You" page

Nature of the changes (frontend / backend / database):
frontend

# Update as of 22 March

Coder: Dycia

Purpose of the changes:
(1) Updated Component - LandingPageNavBar (LandingPageNavBar.vue) - Resolved the responsiveness issue when in mobile view
(2) Updated Page - Landing Page (LandingPage.vue) - Resolved the wonky code in landing page
--> Implemented fetchTopListings() function to dynamically retrieve the trending listings
--> Refined goSearchListing() function to ensure consistent execution on every page reload
--> Standardized the UI for trending listings
Previously, the code for the trending tag was missing. because of the trending tags code missing, when a user presses the trending tags an error pops out. now we added in the trending tag code to resolve the error
(3) Added Page - Listing By Tag (ListingByTag.vue) - Implemented this page to display related listings when users click on a trending tag on the landing page
(4) Updated Page - Search View (SearchView.vue) - Expanded search functionality to allow searching bottles by tags
(5) Updated Router (index.js) - Added routing for ListingByTag.vue - Implemented UX improvements to ensure users are automatically scrolled to the top when navigating between pages
(6) Updated Component - NavBar (NavBar.vue) - Resolved the responsiveness issue when in mobile view
Nature of the changes (frontend / backend / database):
frontend

# Update as of 26 Mar 2025 - code is ok as of this date

Coder: Zhe Han

Purpose of the changes: Bugfix for Latest News page.
Latest news page images not showing up. found it was due to https://via.placeholder.com/600x400 not working in getData.py
replaced it with https://placehold.co/600x400 and deployed

Nature of the changes (frontend / backend / database): Backend
# Update as of 27 Mar 2025
Coder: Carissa

Purpose of the changes: 
    (1) Updated Component - LandingPageNavBar (LandingPageNavBar.vue) 
        - To include the tab for "For You" page
    (2) Added Page - For You Page (ForYouPage.vue)
        - Implemented this page to display related listings and clubs recommended for users
    (3) Updated component - Nav Bar (NavBar.vue)
        - To include the tab for "For You" page
    (4) Updated Router (index.js)
        - Added routing for ForYouPage.vue
    
Nature of the changes (frontend / backend / database): 
    frontend

Coder: Dycia

Purpose of the changes: 
    (1) Updated Backend API (getData.py)
        - Added getRecommendedListings(userID) backend api to fetch recommended listings
        - Added get_recommended_clubs(userID) backend api to fetch recommended clubs
        - Added basic_algo(userID) for basic algo for drinks recommendation
        - Added advanced_algo_reviews(userID) for advanced algo for drinks recommendations via flavourTags
        - Added testRecommender(userID) for the testing of recommender backend api
    
Nature of the changes (frontend / backend / database): 
    Backend

Coder: Carissa

Purpose of the changes: 
    (1) Updated Page - Dashboard Page (UserDashboard.vue) 
        - updated frontend to look like figma (added columns for Grails, GOATS, and Ride or Dies), 
        added addDrink() function to retrieve drinks from the database to be added into the list, 
        added openPopup(), and closePopup() for pop up, added styling for pop up
    (2) Added Page - Best Of Page (BestOf.vue)
        - Implemented this page to display Top 5 listings for each category
    (3) Updated Router (index.js)
        - Editted routing for best of to BestOf.vue
    (4) Updated Component - LandingPageNavBar (LandingPageNavBar.vue) 
        - To editted the tab for "Best Of" page to route it to the correct page
    (5) Updated component - Nav Bar (NavBar.vue)
        - To editted the tab for "Best Of" page to route it to the correct page

Nature of the changes (frontend / backend / database): 
    frontend

Coder: Carissa

Purpose of the changes: 
    (1) Added backend code in getData.py 
        - Added backend api (/getTopCategoryListings) for Best Of to retrieve top 5 listings per category (Grails, GOATS, and Ride or Dies), 
        accounted for fallback algo where it will randomly have 5 listings if there are insufficient people using the feature in the Dashboard page
    
Nature of the changes (frontend / backend / database): 
    backend

Coder: Dycia

Purpose of the changes: 
    (1) Updated Backend API (getData.py)
        - Added getListingByName(listing_name) backend api to fetch listing details by listing name
    
Nature of the changes (frontend / backend / database): 
    Backend

Coder: Dycia

Purpose of the changes: 
    (1) Updated 01-postgresql_data3.sql
        - Added new columns into "users" tables for dashboard
            - "grails", "rideOrDies", "goats"
    (3) Updated 02-insert-data.sql
        - Updated the users table value

Nature of the changes (frontend / backend / database):
    database

Coder: Dycia

Purpose of the changes: 
    (1) Added new backend file - editDashboard.py 
        - editDetails() to update the top 3 categories
    
Nature of the changes (frontend / backend / database): 
    backend


# Update as of 27 Mar 2025
Coder: TeckXuan

Purpose of the changes: 
    (1) Added new frontend file - ImageSearchResults.vue 
        - To show the results of the reverse Image Search
    (2) Updated new Reverse Image Search frontend
        - To enable user to uplaod the photos and send for reverse image search
    (3) Updated index.js to include new frontend file 
    (4) Added new backend API
        - Getimagesearchresults to retrieve listings based on Google Vision API
        - Added 2 new imports
    
Nature of the changes (frontend / backend / database): 
    backend / frontend


# Update as of 28 Mar 2025
Coder: Carissa
Purpose of the changes: 
    (1) Edited backend code in getData.py 
                - Edited backend api (/getTopCategoryListings) for Best Of to account for when there are no listings at all in grails, goats, and ride or dies 
                
Nature of the changes (frontend / backend / database): backend

Coder: Dycia

Purpose of the changes: 
    (1) Updated Page - Dashboard Page (UserDashboard.vue) 
        - Updated the popup to display the drink listing retrieved from the "user" table
        - Fixed the UI of the cards
        - Updated the popup to display the drink listing within the popup modal
        - Added in function to remove drink listing in popup modal
        - Updated popup modal to limit selection for "rideOrDies" and "goats" to 3 selection
        - Toast to notify the user when they reached the selection limit
        - Toast to notify the user when dashboard is updated sucessfully

Nature of the changes (frontend / backend / database): 
    frontend

# Update as of 27 Mar 2025
Coder: Carissa

Purpose of the changes: 
    (1) Updated Component - LandingPageNavBar (LandingPageNavBar.vue) 
        - To include the tab for "For You" page
    (2) Added Page - For You Page (ForYouPage.vue)
        - Implemented this page to display related listings and clubs recommended for users
    (3) Updated component - Nav Bar (NavBar.vue)
        - To include the tab for "For You" page
    (4) Updated Router (index.js)
        - Added routing for ForYouPage.vue
    
Nature of the changes (frontend / backend / database): 
    frontend

Coder: Dycia

Purpose of the changes: 
    (1) Updated Backend API (getData.py)
        - Added getRecommendedListings(userID) backend api to fetch recommended listings
        - Added get_recommended_clubs(userID) backend api to fetch recommended clubs
        - Added basic_algo(userID) for basic algo for drinks recommendation
        - Added advanced_algo_reviews(userID) for advanced algo for drinks recommendations via flavourTags
        - Added testRecommender(userID) for the testing of recommender backend api
    
Nature of the changes (frontend / backend / database): 
    Backend

Coder: Carissa

Purpose of the changes: 
    (1) Updated Page - Dashboard Page (UserDashboard.vue) 
        - updated frontend to look like figma (added columns for Grails, GOATS, and Ride or Dies), 
        added addDrink() function to retrieve drinks from the database to be added into the list, 
        added openPopup(), and closePopup() for pop up, added styling for pop up
    (2) Added Page - Best Of Page (BestOf.vue)
        - Implemented this page to display Top 5 listings for each category
    (3) Updated Router (index.js)
        - Editted routing for best of to BestOf.vue
    (4) Updated Component - LandingPageNavBar (LandingPageNavBar.vue) 
        - To editted the tab for "Best Of" page to route it to the correct page
    (5) Updated component - Nav Bar (NavBar.vue)
        - To editted the tab for "Best Of" page to route it to the correct page

Nature of the changes (frontend / backend / database): 
    frontend

Coder: Carissa

Purpose of the changes: 
    (1) Added backend code in getData.py 
        - Added backend api (/getTopCategoryListings) for Best Of to retrieve top 5 listings per category (Grails, GOATS, and Ride or Dies), 
        accounted for fallback algo where it will randomly have 5 listings if there are insufficient people using the feature in the Dashboard page
    
Nature of the changes (frontend / backend / database): 
    backend

Coder: Dycia

Purpose of the changes: 
    (1) Updated Backend API (getData.py)
        - Added getListingByName(listing_name) backend api to fetch listing details by listing name
    
Nature of the changes (frontend / backend / database): 
    Backend

Coder: Dycia

Purpose of the changes: 
    (1) Updated 01-postgresql_data3.sql
        - Added new columns into "users" tables for dashboard
            - "grails", "rideOrDies", "goats"
    (3) Updated 02-insert-data.sql
        - Updated the users table value

Nature of the changes (frontend / backend / database):
    database

Coder: Dycia

Purpose of the changes: 
    (1) Added new backend file - editDashboard.py 
        - editDetails() to update the top 3 categories
    
Nature of the changes (frontend / backend / database): 
    backend


# Update as of 27 Mar 2025
Coder: TeckXuan

Purpose of the changes: 
    (1) Added new frontend file - ImageSearchResults.vue 
        - To show the results of the reverse Image Search
    (2) Updated new Reverse Image Search frontend
        - To enable user to uplaod the photos and send for reverse image search
    (3) Updated index.js to include new frontend file 
    (4) Added new backend API
        - Getimagesearchresults to retrieve listings based on Google Vision API
        - Added 2 new imports
    
Nature of the changes (frontend / backend / database): 
    backend / frontend


# Update as of 28 Mar 2025
Coder: Carissa
Purpose of the changes: 
    (1) Edited backend code in getData.py 
                - Edited backend api (/getTopCategoryListings) for Best Of to account for when there are no listings at all in grails, goats, and ride or dies 
                
Nature of the changes (frontend / backend / database): backend

Coder: Dycia

Purpose of the changes: 
    (1) Updated Page - Dashboard Page (UserDashboard.vue) 
        - Updated the popup to display the drink listing retrieved from the "user" table
        - Fixed the UI of the cards
        - Updated the popup to display the drink listing within the popup modal
        - Added in function to remove drink listing in popup modal
        - Updated popup modal to limit selection for "rideOrDies" and "goats" to 3 selection
        - Toast to notify the user when they reached the selection limit
        - Toast to notify the user when dashboard is updated sucessfully

Nature of the changes (frontend / backend / database): 
    frontend

# Update as of 29 Mar 2025

Coder: Shahzaib Saeed
Changes Implemented:

UI/UX enhancements on the Explore Page, Login, Signup, and Bottle Listings.

Updated the UI to align with the Figma design.

Ensured responsiveness across all screen sizes.

# Update as of 30 March

Coder: Candy

Purpose of the changes:
URL names for producer and user profiles
(1) Updated Router - LandingPageNavBar (LandingPageNavBar.vue)
Updater Router - NavBar (NavBar.vue)
Updated Router - router/index.js
Updated Router - LoginPage.vue
Updated Router - SignUpPage.vue
Updated Router - UserProfileRefactor.vue
Updated Router - ProducerProfile.vue - Added username to router link for Producer and Users profile page when logged in
Nature of the changes (frontend / backend / database):
frontend

Test

# Update as of 30 Mar 2025
Coder: Carissa
Purpose of the changes: 
    (1) Edited backend code in getData.py 
                - Edited backend api (/getTopCategoryListings) to change to select from upAndComing instead of rideOrDies
    (2) Edited backend code in editDashboard.py 
                - Edited backend api (/editTop3) to change to select from upAndComing instead of rideOrDies
                
Nature of the changes (frontend / backend / database): backend

Coder: Coder: Carissa

Purpose of the changes: 
    (1) Updated Page - Dashboard Page (UserDashboard.vue) 
        - Updated naming of Ride or Dies to Up & Coming

Nature of the changes (frontend / backend / database): 
    frontend

Coder: Coder: Carissa

Purpose of the changes: 
    (1) Updated users table "rideOrDies" to "upAndComing"

Nature of the changes (frontend / backend / database): 
    database

# Update as of 31 Mar 2025
Coder: Jovinne
Purpose of the changes: 
    (1) Edited backend code in getData.py 
                - Updated getRecommendedListings and all related helper functions
                - Fixed basic algo to correctly retrieve and use flavour tags
                - Added helper function advanced_algo_list to recommend listings to users if they have at least 5 drinks total in their drink lists

Nature of the changes (frontend / backend / database): backend

Coder: Jovinne

Purpose of the changes: 
    (1) Updated 'drinkType' col in"listings" table to maintain consistency across all tables
                - Changed 'Whiskey' to Whiskey / Whisky'
                - Changed 'Rum' to 'Rum / Rhum'

Nature of the changes (frontend / backend / database): 
    database
# Update as of 30 March

Coder: Candy

Purpose of the changes:
Updated URL link to producer page and user profile My Drink List
(1) Updated Router - Producers/Bottlelisting.vue
(2) Updated Router - UserProfileRefactor.vue
Nature of the changes (frontend / backend / database):
frontend

# Update as of 31 March

Coder: Candy

Purpose of the changes:
Updated URL link to producer page on RandomExplorePage.Vue
(1) Updated Router - RandomExplorePage.Vue
(2) Updated Router - users/BottleListing.Vue
(3) Updated Router - ClubView.vue - Fixed profile URL for users
Nature of the changes (frontend / backend / database):
frontend

# Update as of 31 March

Coder: Candy

Purpose of the changes:
Updated Backend getReviewsByUserIds code to accommodate tuple userIds
(1) Updated backend/getData.py
Nature of the changes (frontend / backend / database):
backend
