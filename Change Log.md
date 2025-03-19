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
    (1) Added in a new file (rssFeed.py)
        - Backend API to fetch articles from 88bamboo.co. Returns a dictionary of articles
    (2) Added new functions (getData.py)
        - (a) get_listings_by_observation_tag(tag): get the listings from listing table that matches the observation tag
        - (b) getTop8(): get the top 8 trending tags
        - (c) getTopListings(): get the top trending bottles
        - (d) getListingsName(): get all the listing names from listing table
        - (e) getRandomListings(): randomiser for the explore page
    (3) Updated the packages (getData.py)
        - Added the neccessary packages to for the functions work in getData.py

Nature of the changes (frontend / backend / database):
    backend

Coder: Dycia

Purpose of the changes: 
    (1) New Component - Landing Page Nav Bar (LandingPageNavBar.vue)
        - New nav bar for the landing page. Centered the logo and removed the search bar.
    (2) New Component - Autocomplete Search Bar (SearchBar.vue)
        - New autocomplete search bar for the landing page.
    (3) Updated the UI for landing page (LandingPage.vue)
        - New UI design for the landing page
        - Implemented the trending tags and drink
        - Implemented the articles from 88bamboo.co

Nature of the changes (frontend / backend / database):
    frontend
