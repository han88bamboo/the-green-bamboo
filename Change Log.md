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
    (1) Added new tables (associations, pointsRecorder, pointSystemRules) -- 01-postgressql_data3.sql
    (2) Updated new columns into "users" tables -- 01-postgressql_data3.sql
    (3) Added new values for the newly created table (associations) -- 02-insert-data.sql
    (4) Updated the users table value -- 02-insert-data.sql
    (5) Changed the port number in docker-compose-db.yml

Nature of the changes (frontend / backend / database):
    database


