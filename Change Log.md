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

# Update as of 5 April

Coder: Han

Purpose of the changes:
Producer bottle listings - to allow admin / moderators to delete reviews.
Still require CP's assistance to bug fix thihs issue.
Nature of the changes (frontend / backend / database):
frontend

# Update as of 5 April

Coder: Han

Purpose of the changes:
Producer Profile page - added button to review the producer 

Still need to monitor for bugs, responsiveness, etc

Nature of the changes (frontend / backend / database):
frontend


# Update as of 8 April

Coder: Han

Purpose of the changes:
To create function of reviewing venue on Venue Profile page

Files updated:
(a) createReview.py - [POST] Creates a venue review
(b) deleteReview.py - [DELETE] Deletes a venue review
(c) editReview.py - [POST] Vote venue review /   [PUT] Update venue review
(d) getData.py - [GET] Venue Reviews / 
(e) VenueProfile.vue - buttons, functions, review displays, calling of endpoints
(f) 01-postgresql_data3.sql - venueReviews and venueReviewsUserVotes tables

Nature of the changes (frontend / backend / database):
frontend, backend and database


# Update as of 11 April

Coder: Candy

Purpose of the changes:
Updated profile URL for venue
(1) Updated router - VenueProfile.vue
(2) Updated router - router/index.js
(3) Updated router - NavBar.vue
(4) Updated router - LandingPageNavBar.vue
(5) Updated router - SearchView.vue
getData/getVenueReviews receive 500 Internal server error 
Nature of the changes (frontend / backend / database):
frontend

# Update as of 11 April (Part 2)

Coder: Candy

Purpose of the changes:
Updated profile URL for profile/producer and lisitng/view in search view 
(1) Updated router for both profile/producer and listing/view - SearchView.vue
(2) Updated router for listing/view/:listingid to include listing name - RandomExplorePage.vue
(3) Updated router for listing/view/:listingid to include listing name - ListingRowDisplay.vue
(4) Updated router for listing/view/:listingid to include listing name - ListingRowDisplayProducerProfile.vue
(5) Updated router for listing/view/:listingid to include listing name - SubmitListingNew.vue
(6) Updated router for listing/view/:listingid to include listing name - LandingPage.vue
(7) Updated router for listing/view/:listingid to include listing name - ProducerDashboard.vue
(8) Updated router for listing/view/:listingid to include listing name - ProducerProfile.vue

Nature of the changes (frontend / backend / database):
frontend

# Update as of 11 April (Part 3)

Coder: Candy

Purpose of the changes:
Updated URL for events
(1) Updated router for events URL - SpecificEventPage.vue
(2) Updated router for events URL - router/index.js
(3) Updated router for events URL - events.vue

Nature of the changes (frontend / backend / database):
frontend

# Update as of 11 April (Part 4)

Coder: Candy

Purpose of the changes:
Updated URL for events and club
(1) Updated router for past & recommended events URL - events.vue
(2) Updated router for club/view/:clubid/:clubName - router/index.js

Nature of the changes (frontend / backend / database):
frontend

# Update as of 14 April 

Coder: Candy

Purpose of the changes:
Updated URL for events and club
(1) Updated profile and club/view router for BrowseClubs.vue
(2) Updated router for club/view/:clubid/:clubName - router/index.js
(3) Updated router for CreateClubs.vue

Nature of the changes (frontend / backend / database):
frontend


# Update as of 18 April 

Coder: TZH

Purpose of the changes:
updated NavBar.vue to allow search to autocomplete, referencing code from SearchBar.vue (used Copilot)

Nature of the changes (frontend / backend / database):
frontend


# Update as of 24 April 

Coder: TZH

Purpose of the changes:
updated data folder to include the right countries

Nature of the changes (frontend / backend / database):
frontend


# Update as of 25 April 

Coder: Kai

Purpose of the changes:
updated positioning of reviews in producer bottle listing page

Nature of the changes (frontend / backend / database):
frontend

# Update as of 25 April 

Coder: Kai

Purpose of the changes:
added 3-dot dropwon feature for users to edit reviews - but buggy TZH to fix

Nature of the changes (frontend / backend / database):
frontend

# Update as of 25 April 

Coder: Kai

Purpose of the changes:
neatened the margins and the line spacings on the drink listing pages (mobile + Desktop)
added mobile only row of buttons like add review, bookmark, and extended info

Nature of the changes (frontend / backend / database):
frontend

# Update as of 25 April 

Coder: Kai 
Purpose of changes: 
1. neatened up the spacing of the venue desc and attributes, and the review venue and follow venue buttons (mobile + desktop)
2. adjusted the global css for the display of the venue profile images and also the display of the drink listings rows for producer + venue profile pages (added hover effects, changed sizing etc)

Nature of the changes (frontend/backend / database):
front end

# Update as of 28 April 

Coder: Han
fixed delete review bug on Producer BottleListings page - delete review modal was apparently accidentally deleted
made UX changes for the randomExplorePage - however may need to discuss with Kai how best to show how users should show up when making the latest change Wes suggested to show the latest review dropped on that rating. what's the implication for the sorting function?
made UX changes to navbar

Nature of the changes (frontend/backend / database):
front end

# Update as of 28 April 

Coder: Han
updated drink styles again

Nature of the changes (frontend/backend / database):
front end

# Update as of 28 April 

Coder: Candy

Purpose of the changes:
Updated URL for username & profile photo in bottle listings review
(1) Updated username and profile photo router for producers/BottleListings.vue

Nature of the changes (frontend / backend / database):
frontend

# Update as of 29 April 

Coder: Kai

Purpose of the changes:
Neatening up the spacing and margins on venue profile pages
Fixed the error on ListingRowDisplayProducerProfile. that was preventing it from showing up on mobile

Nature of the changes (frontend / backend / database):
frontend

# Update as of 1 May 

Coder: Kai

Purpose of the changes:
(1) Neaten up spacing on Producer Catalogue
(2) Neaten up spacing on Producer Tours and Experience Review
(3) Neaten up spacing on Venue page where they shared common components with Proudcer profile page
 
Nature of the changes (frontend / backend / database):
frontend

# Update as of 2 May 

Coder: Kai

Purpose of the changes:
(1) Cleaned up Q&A boxes for both Venue and Producers
(2) Cleaned up "CLAIM THIS BUSINESS" lock boxes for both Venue and Producers
 
Nature of the changes (frontend / backend / database):
frontend

# Update as of 3 May 

Coder: Han

Purpose of the changes:
imported code from LandingPage.vue and rssFeed.py in Group-3A's repository to get the new landing page working
 
Nature of the changes (frontend / backend / database):
frontend, backend

# Update as of 3 May 

Coder: Han

Purpose of the changes:
fixing bookmarking bug - producer/bottlelistings.vue , bookmarkmodal.vue and bookmarkicon.vue

Nature of the changes (frontend / backend / database):
frontend