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

# Update as of 4 May 

Coder: Han

Purpose of the changes:
imported code from Group-3B's repository to get (1) "Grails, Up & Coming, and GOATs" feature on dashboard and (2) "add a friend" bar working on user profile. 
also reapplied Danish's notifications code - which still requires some bugfixing

Nature of the changes (frontend / backend / database):
frontend / backend / database


# Update as of 8 May 

Coder: Han

Purpose of the changes:
added searchability of users to follow on own user profile page

Nature of the changes (frontend / backend / database):
frontend & backend


# Update as of 9 May 

Coder: Han

Purpose of the changes:
fixed upvote / downvote bug for reviews on producer/bottlelistings.vue

Nature of the changes (frontend / backend / database):
frontend 


# Update as of 9 May 

Coder: Kai

Purpose of the changes:
cleaned up spacing / sizing / Events cards for the events landing page. created new global css components to simplify Events / Clubs display card designs. 

Nature of the changes (frontend / backend / database):
frontend 


# Update as of 9 May 

Coder: Han

Purpose of the changes:
fixed incorrectly appearing "welcome" message on user profile page
added FooterBar to landing and random explore page
replaced landing page's navbar with correct navbar with search bar

Nature of the changes (frontend / backend / database):
frontend 

# Update as of 9 May (shifted to present day) - point of deployment with no major issues, apart from needing to fix bug on BillingSecurity.vue page where user cannot proceed past that page

Coder: Han

Purpose of the changes:
added an attempted fix to the AdminDashboard.vue page to fix the bug where you can't approve a new business 

Nature of the changes (frontend / backend / database):
frontend 


# Update as of 10 May 

Coder: Han (Danish)

Purpose of the changes:
added Danish's bug fix to notification feature - fix not satisfactory because the red notifications number does not go down when we view or click on the notif messages. we also want to apply a shading to notifications that have newly appeared.

Nature of the changes (frontend / backend / database):
backend

# Update as of 10 May 

Coder: Kai

Purpose of the changes:
front-end changes to individual profile page 
cleaned up spacing, buttons, margins, and design on front end. 

Nature of the changes (frontend / backend / database):
frontend

# Update as of 10 May 

Coder: Han

Purpose of the changes:
attempted fix to get Stripe fully working . made tweak to payment.py file

Nature of the changes (frontend / backend / database):
backend 

# Update as of 11 May - deployed
Coder: Han

Purpose of the changes:
fix to get Stripe working with fields to fill in payment information on BillingSecurity.vue page. made tweak to payment.py and  BillingSecurity.vue files

Nature of the changes (frontend / backend / database):
backend mostly, frontend 

# Update as of 13 May 
Coder: Kai

Purpose of the changes:
Front end changes to individual event page
- Changed the spacing and the sizing of the event elements 
- added new buttons and adjusted mobile compatability

Nature of the changes (frontend / backend / database):
Front end

# Update as of 14 May 
Coder: Kai

Purpose of the changes:
Front end changes to search bar results 
- Changed the spacing and the sizing of the search bar elements 
- add new fields that shows up in search results 

Nature of the changes (frontend / backend / database):
Front end

# Update as of 14 May 
Coder: Kai

Purpose of the changes:
Front end changes to login / sign up / business account sign up / Landing Page:
- Made mobile responsive 
- Cleaned up margins, spacings, sizings

Nature of the changes (frontend / backend / database):
Front end


# Update as of 16 May - Deployed, but with bugs on Stripe **
Coder: Han

Purpose of the changes:
attempted fix to get Stripe working. Able to submit form but payment does not go through to Stripe "paymentintent" error

Nature of the changes (frontend / backend / database):
Front end / backend

# Update as of 16 May 
Coder: Han

Purpose of the changes:
fixed successfully bug where ordinary users who sign up aren't directed to onboarding flow / profile page 

Nature of the changes (frontend / backend / database):
backend

# Update as of 16 May 
Coder: Han

Purpose of the changes:
added a ton of debugging logs to createAccount.py and producerProfile.vue

Nature of the changes (frontend / backend / database):
frontend /backend 

# Update as of 17 May 
Coder: Han

Purpose of the changes:
fixed bug where newly-created producer accounts cannot see their profile page - createAccount.py and producerProfile.vue. however, Settings button still does not work

Nature of the changes (frontend / backend / database):
frontend /backend 

# Update as of 17 May 
Coder: Kai 

Purpose of the changes:
Changing front end of the clubs and events page: fixed spacing, buttons, margins
Edit clubs.py and events.py to change the error message. 

Nature of the changes (frontend / backend / database):
frontend 

# Update as of 17 May - deployed with no major issues
Coder: Han

Purpose of the changes:
adding a ton of debugging logs to producerProfile.vue to diagnose settings button error

Nature of the changes (frontend / backend / database):
frontend 

# Update as of 19 May - deployed with no major issues
Coder: Kai

Purpose of the changes:
Alot of front-end changes, mainly to clubs / events to align spacing, margins, colors, sizings 
This also involved editing other components like EventBox.vue
Also cleaned up margin issues with the Landing page and on the User Profile 
Cleaned up some misalignment in search boxes 

Nature of the changes (frontend / backend / database):
frontend 

# Update as of 20 May 
Coder: CP

Purpose of the changes:
bug fix: edited create event form and upcoming events backend endpoint
- made time and limit and location optional in create event form
- included all day option in create event from
- included user's own events when retrieving upcoming events
- edited error message shown on events page if user did not login


Nature of the changes (frontend / backend / database):
frontend and backend

# Update as of 20 May 
Coder: CP

Purpose of the changes:
fix: added rank color due to merge issue previously


Nature of the changes (frontend / backend / database):
frontend

# Update as of 21 May 
Coder: CP

Purpose of the changes:
bug fixes for clubs
[Clubs] Join status is wrongly stated as "Pending" for members who have already successfully joined
[Clubs] Club can't change from private to public
[Clubs] Profile picture of users postings in clubs is not showing the user's profile picture, just the default user picture.

Nature of the changes (frontend / backend / database):
frontend and a bit of backend

# Update as of 21 May 
Coder: CP

Purpose of the changes:
bug fix: fix total member not showing on clubs you manage section on browse clubs page


Nature of the changes (frontend / backend / database):
frontend and backend

# Update as of 21 May 
Coder: CP

Purpose of the changes:
bug fix: show correct error message on specific event page for more events


Nature of the changes (frontend / backend / database):
frontend and backend


# Update as of 21 May 
Coder: Han

Purpose of the changes:
reverted BillingSecurity.vue and Payment.py files back to original version to fix bug where Stripe payment does not go through. added debugging logs

Nature of the changes (frontend / backend / database):
frontend, backend

# Update as of 21 May 
Coder: CP

Purpose of the changes:
bug fix: fixed club and events bugs
Fixes:
- image uploading for club banner, club post and event banners (base64 issue fix)
- fixed club status on the left menu on browse club page


Nature of the changes (frontend / backend / database):
frontend and backend

# Update as of 22 May 
Coder: Han

Purpose of the changes:
commented out the Scan Bottle feature from landing page.

Nature of the changes (frontend / backend / database):
frontend

# Update as of 22 May 
Coder: Han

Purpose of the changes:
added footer to all the relevant pages

Nature of the changes (frontend / backend / database):
frontend

# Update as of 22 May 
Coder: Han

Purpose of the changes:
fixed broken links to drinks listings on UserProfileRefactor.vue and ListingRowDisplayUserProfile.vue components
also fixed producer error message and added new method to get producers on getdata.py

Nature of the changes (frontend / backend / database):
frontend, backend

# Update as of 22 May 
Coder: Han

Purpose of the changes:
fixed broken links to drinks listings on userdashboard.vue

Nature of the changes (frontend / backend / database):
frontend

# Update as of 23 May 
Coder: Han

Purpose of the changes:
fixed issue whereby delete button didn't work for announcements on deployed site.

Nature of the changes (frontend / backend / database):
frontend

# Update as of 23 May 
Coder: Danish

Purpose of the changes:
•⁠  ⁠Fixed the 'My Drink Lists' button color on badges tab active.
•⁠  ⁠Fixed progress bar calculation in user badges
•⁠  ⁠Added Public Lists badge
•⁠  ⁠Added badge notification in user's notification

Nature of the changes (frontend / backend / database):
backend mostly, and frontend



# Update as of 23 May 
Coder: Kai

Purpose of the changes:
front-end changes for user dashboard + best of selection module

Nature of the changes (frontend / backend / database):
frontend

# Update as of 26 May 
Coder: Kai

Purpose of the changes:
front-end changes for Best Of - mobile responsiveness

Nature of the changes (frontend / backend / database):
frontend

# Update as of 26 May 
Coder: Han (Danish & CP's work )
Purpose of the changes:
– adding rsvp badge, events check in status
– feat: change in events ui
– feat: best of page including show all for type category for each drink type
– bug fixes: fixed best of bugs
  > only users can see cast your vote button
  > fixed routing issue for cast your vote button
  > refactored best of selections to add the exact listing user have selected
– feat: added edit and delete button on club post page


Nature of the changes (frontend / backend / database):
frontend, backend and DB

# Update as of 28 May 
Coder: Kai 

Purpose of the changes:
changed the front end spacing / margin / toggles for venue and producer dashboards
edited the default profile picture for producers, venues and users.

Nature of the changes (frontend / backend / database):
frontend

# Update as of 2 June 
Coder: Jun Wei

Purpose of the changes:
- Debugged the issue of stripe payment element not showing up (payment.py)
- Debugged the issue of blank page redirection after creation of account after stripe payment (BillingSecurity.vue)

Nature of the changes (frontend / backend / database):
frontend and backend


# Update as of 14 June 
Coder: Kai 

Purpose of the changes:
- Edited text and button displays for NavBar on Desktop for various users
- Edited the front end of the mobile navigation bar - changed from dropdown to right panel. 

Nature of the changes (frontend / backend / database):
frontend

# Update as of 15 June 
Coder: Jun Wei 

Purpose of the changes:
- Debugged issue of business settings button not being clickable for claimed and approved businesses (venues and producers)
- Debugged issue of business settings page's broken backend calls due to different Stripe API response values (different api versions). 

Nature of the changes (frontend / backend / database):
frontend and backend

# Update as of 15 June 
Coder: Han 

Purpose of the changes:
added help topics / "get started page" on Drink-X, with first 3 topics:
(1) Features
(2) Drink-X for Venues
(3) Drink–X for Brands

Nature of the changes (frontend / backend / database):
frontend 

# Update as of 15 June - deployed too
Coder: Han 

Purpose of the changes:
added conditionally rendered welcome sections for VenueProfile.vue and ProducerProfile.vue

Nature of the changes (frontend / backend / database):
frontend 

# Update as of 16 June 
Coder: Kai 

Purpose of the changes:
Changed the leaderboard front end and category names 
changed default profile pic for User that shows up on User Dashboard

Nature of the changes (frontend / backend / database):
frontend 

# Update as of 17 June

Coder: Candy

Purpose of the changes:
Updated URL that are not working on user's dashboard
(1) Updated UserDashboard.vue
(2) Updated organiser link format (frontend/src/views/SpecificEventPage.vue)
(2) Updated post discussion user link format (ClubPostView.vue)

Nature of the changes (frontend / backend / database):
frontend

# Update as of 18 June

Coder: Candy

Purpose of the changes:
switched off faulty duplicate checking mechanism - it was causing photo misalignments 

Nature of the changes (frontend / backend / database):
backend



# Update as of 22 June

Coder: CP

Purpose of the changes:
bugfixes

Nature of the changes (frontend / backend / database):
front / backend

# Update as of 23 June

Coder: Kai

Purpose of the changes:
Explore page front end
Fixed the spacing and height issues in the boxes "Drink Shelf", "Pending Listings", "Brands you Follow" 

Nature of the changes (frontend / backend / database):
front end



# Update as of 23 June

Coder: Han

Purpose of the changes:
helptopics.vue - about, support, FAQ
changes to business sign up page

Nature of the changes (frontend / backend / database):
frontend

# Update as of 24 June

Coder: Kai

Purpose of the changes:
fixed spacing and alignment on the user , venue, producer dashboards

Nature of the changes (frontend / backend / database):
frontend

# Update as of 26 June

Coder: Han

Purpose of the changes:
Partner Center + Legal terms

Nature of the changes (frontend / backend / database):
frontend

# Update as of 28 June - deployed with no issues

Coder: Han

Purpose of the changes:
fixed bug where venue link wasn't working / usernames weren't showing up for non-logged in user

Nature of the changes (frontend / backend / database):
frontend

# Update as of 29 June 

Coder: Jun Wei

Purpose of the changes:
- Enabled users to key in coupon code for Stripe payment, applying the appropriate discounts
- Fixed Stripe api version usage to prevent bugs from appearing due to change in response format by Stripe (Version being used is "2025-05-28.basil")

Nature of the changes (frontend / backend / database):
frontend
backend

# Update as of 29 June 

Coder: Ming Sheng

Purpose of the changes:
fixed code allowing for the claiming of business profiles

Nature of the changes (frontend / backend / database):
frontend, backend

# a ton of other changes 

# Update as of 30 June - deployed 

Coder: Han

Purpose of the changes:
fixed error where by points aren't showing up for reviews

Nature of the changes (frontend / backend / database):
backend

# Update as of 30th June 

Coder: Kai

Purpose of the changes:
- Hide where to buy on the bottle listings (Kai) 
- To start tagging friends, follow them first!  (Kai) 
- Ride or Die - change to The Essentials  (kai) 
- “No results found” in the search bar - to remove it  (kai) 
- “Please select a plan” - make it bold, bigger, above the options (Kai) 
- Successful signup “mb-10” (Kai) 
- Venue Edit Menu: Add in a section to explain the sequence to adding new menu times  (Kai) 

Nature of the changes (frontend / backend / database):
front end

# Update as of 1 Jul - deployed 

Coder: Han

Purpose of the changes:
minor fix to allow logged-out users to see points

Nature of the changes (frontend / backend / database):
frontend

# Update as of 4 Jul - deployed 

Coder: Han

Purpose of the changes:
minor frontend bugfixes:
for the mobile nav bar for a normal logged in  set "My Drink Profile" to redirect to the user profile instead of the user dashboard 
mobile version link for venues searched was broken
"Add list" button on mobile doesn't show the pop up window.


Nature of the changes (frontend / backend / database):
frontend

# Update as of 4 July

Coder: Kai

Purpose of the changes:
Fixed the following front end errors 
- Menu Itme Preview on Add Menu Modal on Mobile
- Fix Anchoring issue (hopefully)
- Fix Photo Constrained Rendering on Venue / Brand 
- Fixed Photo not loading on Mobile for Venue / Brand Overview
- Fixed Photo Constrained On Venue / Brand Profile Pictures

Swapped ordering of menu and venue overview on Venue Profile 

Implemented scrollable Pop Up Modals CSS styling because some pop up windows are not scrollable on Mobile View 

Nature of the changes (frontend / backend / database):
frontend

# Update as of 6 July

Coder: MS

Purpose of the changes:
search bar funtionality and postgresql search optimization 

Nature of the changes (frontend / backend / database):
postgresql - create trigram index strategry to index based on listing, producer, venue name
backend - getData.py - implement fuzzy search with similarity score function for bottle,producer and venue listing search
frontend - AutocompleteSearch.vue, NavBar.vue, LandingPage.vue 
introduce new search component to return bottle producer and venue listing.
parallel api calling with promise.all 
logic handling in landing page. 

# Update as of 6 July

Coder: Han

Purpose of the changes:
new partner center pages

Nature of the changes (frontend / backend / database):
frontend + index plus creation of new files in view

# Update as of 6 July

Coder: Kai 

Purpose of the changes:
- Created a new partner center with links to Drink-X for Brands / Venue / Festival Organisers. 
- Adjusted the footer bar to reflect new links 
- I've adjusted the links in the footer header accordingly to the Partner Centre pages : So now all the stuff like FAQs, Privacy Policy, Terms of Use stuff remains under www.drink-x.com/help , but the Business account related stuff goes under www.drink-x.com/partner

Nature of the changes:
Frontend



# Update as of 7 July

Coder: Han

Purpose of the changes:
error handling for dragging and dropping menu operations

Nature of the changes (frontend / backend / database):
frontend 


Coder : MS 

Purpose of the changes:
Moved search selection and navigation logic from LandingPage.vue to a new composable (useSearch.js) and updated NavBar.vue to use this composable. 
finding SQL search query bottle neck of not utilizing indexed column, adjusted SQL query to optimize search time

Nature of the changes (frontend / backend / database):
frontend 

Coder : Kai 

Purpose of the changes:
Created new Badges and Point System page and populated it with visual elements. Still work in progress but main content is now there. 

Nature of the changes (frontend / backend / database):
frontend 

# Update as of 8 July

Coder: Kai

Purpose of the changes:
Finalising content on Badges and Points

Nature of the changes (frontend / backend / database):
frontend 

# Update as of 9 July

Coder: Han

Purpose of the changes:
to allow ratings to be stored as decimals

Nature of the changes (frontend / backend / database):
frontend , backend, database

# Update as of 9 July

Coder: Han

Purpose of the changes:
applied autocomplete search to onboarding flow

Nature of the changes (frontend / backend / database):
frontend

# Update as of 10 July 

Coder: MS 

Purpose of the changes:
- revamp userDashboard.vue
  front end:
  - rework on overall flow to better managed view and optimize for speed
  - removed all irrelevant codes from all components
  - break down into components and migrate into user_dashboard folder for better folder structure
  backend:
  - refactored endpoints for better efficiency and readability. (introduced CTE, merged SQL for better calling effeciency)
- Updates AutocompleteSearch to use 'drinkType' instead of 'typeCategory'.

Nature of the changes (frontend / backend / database):
frontend, backend and database 

# Update as of 10 July 

Coder: Han

Purpose of the changes:
making welcome sections collapsible in the ProducerProfile, UserProfileRefactor and VenueProfile

Nature of the changes (frontend / backend / database):
frontend

# Update as of 11 July 

Coder : MS 

Purpose of the changes:
- Added loading and error states to ActivityFeed component and integrated them into UserDashboard. Backend query for recent follower activity now returns username and limits results in SQL. 
- removed block wise loading state introduced component wise loading state to keep modern application build design
- tag activity fix to return username
- fix for follower activity assigning to the wrong api 
- fix leaderboard listing racing issue causing the dashboard to fail 

Nature of the changes (frontend / backend / database):
frontend , backend

# Update as of 12 July 

Coder: Han

Purpose of the changes:
find friends feature on navbar

Nature of the changes (frontend / backend / database):
frontend


# Update as of 12 July 

Coder: Han

Purpose of the changes:
added support help button in navbar 

Nature of the changes (frontend / backend / database):
frontend


# Update as of 12 July 

Coder: Han

Purpose of the changes:
ambassador badge functionality for bottlelistings and user profile 

Nature of the changes (frontend / backend / database):
frontend, backend


# Update as of 13 July 

Coder: Han

Purpose of the changes:
Venue type field

Nature of the changes (frontend / backend / database):
frontend


# Update as of 13 July 

Coder: Han

Purpose of the changes:
Venue opening hours fix

Nature of the changes (frontend / backend / database):
frontend

# Update as of 14 July  - deployed 

Coder: Han

Purpose of the changes:
partial dev for producer list

Nature of the changes (frontend / backend / database):
frontend, backend


# Update as of 14 July  - deployed 

Coder: Han

Purpose of the changes:
caching of fields for new listing submission

Nature of the changes (frontend / backend / database):
frontend


# Update as of 14 July  - deployed 

Coder: Han

Purpose of the changes:
recent activity copied over to userProfileRefactor.vue

Nature of the changes (frontend / backend / database):
frontend

# Update as of 15 July  - deployed 

Coder: Han

Purpose of the changes:
news notifications

Nature of the changes (frontend / backend / database):
frontend

# Update as of 15 July 
Coder: MS 

Purpose of the changes:
Admin dashboard, some code fixes pending and online regression test needed for existing components.

Nature of the changes (frontend / backend / database):
frontend, backend

# Update as of 15 July 
Coder: Kai 

Purpose of the changes:
- 88 Bamboo's Review on Drink Listing now pulling Article Title instead of URL 
- Text wrap for Venue Resvation / Opening hours Details and for 88 Bamboo's Review 
- Removed "at" for reviews
- Removed "Venue Type" words, and just show the type in italics with a margin under before the description
- Enlarging “Extend Review” button to widen across the page and bold and increase text size

Nature of the changes (frontend / backend / database):
frontend

# Update as of 15 July  - deployed 

Coder: Han

Purpose of the changes:
bottle review submission failure data caching 

Nature of the changes (frontend / backend / database):
frontend

# Update as of 15 July  - deployed 

Coder: Han

Purpose of the changes:
fixed 88b reviews on bottleListings not resolving to chinese / jap characters and permitting venue hours beyond midnight

Nature of the changes (frontend / backend / database):
frontend

# Update as of 15 July 

Coder: Kai

Purpose of the changes:
tweaked the rendering of bottle images on the search results 

Nature of the changes (frontend / backend / database):
frontend

# Update as of 16 July 

Coder: Han

Purpose of the changes:
ensure caching and pulling of data from listings while editing works

Nature of the changes (frontend / backend / database):
frontend

# Update as of 16 July 

Coder: Han

Purpose of the changes:
ensuring admin can upload images for listings

Nature of the changes (frontend / backend / database):
frontend, backend

# Update as of 16 July 

Coder: Han

Purpose of the changes:
claim free brand / venue account

Nature of the changes (frontend / backend / database):
frontend


# Update as of 16 July -deployed with no issues

Coder: Han

Purpose of the changes:
update of autocomplete and search logic

Nature of the changes (frontend / backend / database):
frontend, backend

# Update as of 16 July

Coder: MS

Purpose of the changes:
- Reworks backend endpoints and frontend components to separate and clarify business account and review statistics. 
- Updates chart rendering logic for improved reactivity and performance, adds cumulative review and business account growth charts, and cleans up data structure usage in both backend and frontend. 
- optimize Chart.js bundling in vue.config.js.
- merging of admin_dashboard still a WIP as a side project for now.

Nature of the changes (frontend / backend / database):
frontend, backend

# Update as of 16 July

Coder: Kai

Purpose of the changes:
neatening up front end font sizing 

Nature of the changes (frontend / backend / database):
frontend

# Update as of 17 July - deployed

Coder: Han

Purpose of the changes:
getting search listings / autocomplete to factor in producer name

Nature of the changes (frontend / backend / database):
frontend (searchView), backend


# Update as of 17 July - deployed

Coder: Han

Purpose of the changes:
fixing submission error for listing details on submitListingNew.vue

Nature of the changes (frontend / backend / database):
frontend 

# Update as of 17 July - deployed

Coder: Han

Purpose of the changes:
fixing error where requested listing details don't get populated

Nature of the changes (frontend / backend / database):
frontend 

# Update as of 17 July - deployed

Coder: Han

Purpose of the changes:
extra colours for reviews

Nature of the changes (frontend / backend / database):
frontend, backend, database

# Update as of 19 July - deployed

Coder: MS

Purpose of the changes:
dashboard refector test code

Improves producer account creation with better validation, error handling, and related table initialization in the backend. Updates admin dashboard modals to provide user feedback, success messages, and CSV download for login details. Refines business management UI with more detailed request info, loading states, and improved request review logic. Also includes minor bug fixes and consistency improvements across admin dashboard components.

Nature of the changes (frontend / backend / database):
frontend, backend

# Update as of 19 July 

Coder: Kai

Purpose of the changes:
adding Google analytics tag - Now tracking

Nature of the changes (frontend / backend / database):
frontend


# Update as of 19 July - deployed

Coder: Han

Purpose of the changes:
fixed:
–unable to allow ordinary users to submit drinks description in listing requests
–unable to edit listing requests

Nature of the changes (frontend / backend / database):
frontend, backend, database

# Update as of 19 July - deployed

Coder: Han

Purpose of the changes:
logic for auto-approval of listing requests

Nature of the changes (frontend / backend / database):
frontend, backend, database

# Update as of 20 July - deployed

Coder: Han

Purpose of the changes:
frontend logic for auto-approval of listing requests toggle

Nature of the changes (frontend / backend / database):
frontend, backend


# Update as of 20 July - deployed

Coder: Han

Purpose of the changes:
search bar modal for submission of requests for users

Nature of the changes (frontend / backend / database):
frontend, backend
