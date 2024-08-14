-- DROP TABLES IF EXISTS -- 
DROP TABLE IF EXISTS accountRequests;
DROP TABLE IF EXISTS badges;
DROP TABLE IF EXISTS colours;
DROP TABLE IF EXISTS countries;
DROP TABLE IF EXISTS drinkTypes;
DROP TABLE IF EXISTS flavourTags;
DROP TABLE IF EXISTS languages;
DROP TABLE IF EXISTS listings;
DROP TABLE IF EXISTS modRequests;
DROP TABLE IF EXISTS observationTags;
DROP TABLE IF EXISTS producers;
DROP TABLE IF EXISTS producersQuestionAnswers;
DROP TABLE IF EXISTS producersUpdates;
DROP TABLE IF EXISTS producersProfileViews;
DROP TABLE IF EXISTS producersProfileViewsViews;
DROP TABLE IF EXISTS requestEdits;
DROP TABLE IF EXISTS requestInaccuracy;
DROP TABLE IF EXISTS requestListings;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS reviewsUserVotes;
DROP TABLE IF EXISTS servingTypes;
DROP TABLE IF EXISTS specialColours;
DROP TABLE IF EXISTS subTags;
DROP TABLE IF EXISTS tokens;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS usersDrinkLists;
DROP TABLE IF EXISTS usersfollowLists;
DROP TABLE IF EXISTS venues;
DROP TABLE IF EXISTS venuesMenu;
DROP TABLE IF EXISTS venuesOpeningHours;
DROP TABLE IF EXISTS venuesQuestionAnswers;
DROP TABLE IF EXISTS venuesUpdates;
DROP TABLE IF EXISTS venuesProfileViews;
DROP TABLE IF EXISTS venuesProfileViewsViews;

-- CREATE TABLES -- 
-- ========= accountRequests =========
CREATE TABLE accountRequests (
    id SERIAL PRIMARY KEY,
    businessName VARCHAR(255),
    businessType VARCHAR(255),
    businessDesc TEXT,
    country VARCHAR(255),
    pricing VARCHAR(255),
    businessLink VARCHAR(255),
    firstName VARCHAR(255),
    lastName VARCHAR(255),
    relationship VARCHAR(255),
    email VARCHAR(255),
    contact VARCHAR(255),
    referenceDocument VARCHAR(255),
    photo TEXT,
    joinDate TIMESTAMP,
    isPending BOOLEAN,
    isApproved BOOLEAN
);

-- ========= badges =========
CREATE TABLE badges (
    id SERIAL PRIMARY KEY,
    badgeName VARCHAR(255),
    badgePhoto TEXT,
    badgeDesc TEXT
);

-- ========= colours =========
CREATE TABLE colours (
    id SERIAL PRIMARY KEY,
    hexcode VARCHAR(7)
);

-- ========= countries =========
CREATE TABLE countries (
    id SERIAL PRIMARY KEY,
    originCountry VARCHAR(255),
    legalAge INT
);

-- ========= drinkTypes =========
CREATE TABLE drinkTypes (
    id SERIAL PRIMARY KEY,
    drinkType VARCHAR(255),
    badgePhoto TEXT,
    typeCategory TEXT[]
);

-- ========= flavourTags =========
CREATE TABLE flavourTags (
    id SERIAL PRIMARY KEY,
    hexcode VARCHAR(7),
    familyTag VARCHAR(255)
);

-- ========= languages =========
CREATE TABLE languages (
    id SERIAL PRIMARY KEY,
    language VARCHAR(255)
);

-- ========= listings =========
CREATE TABLE listings (
    id SERIAL PRIMARY KEY,
    listingName VARCHAR(255),
    producerID SERIAL,
    bottler VARCHAR(255),
    originCountry VARCHAR(255),
    drinkType VARCHAR(255),
    abv FLOAT,
    officialDesc TEXT,
    allowMod BOOLEAN,
    addedDate TIMESTAMP,
    typeCategory VARCHAR(255) ,
    age VARCHAR(255) ,
    reviewLink VARCHAR(255) ,
    sourceLink VARCHAR(255) ,
    photo TEXT 
);

-- ========= modRequests =========
CREATE TABLE modRequests (
    id SERIAL PRIMARY KEY,
    userID SERIAL,
    drinkType VARCHAR(255),
    modDesc TEXT,
    reviewStatus BOOLEAN
);

-- ========= observationTags =========
CREATE TABLE observationTags (
    id SERIAL PRIMARY KEY,
    observationTag VARCHAR(255)
);

-- ========= producers =========
CREATE TABLE producers (
    id SERIAL PRIMARY KEY,
    producerName VARCHAR(255),
    producerDesc TEXT,
    originCountry VARCHAR(255),
    mainDrinks TEXT[],
    photo TEXT,
    hashedPassword VARCHAR(255),
    claimStatus BOOLEAN,
    statusOB VARCHAR(255) ,
    questionAnswers SERIAL , -- [!] reference producersQuestionAnswers
    updates SERIAL , -- [!] reference producersUpdates
    username VARCHAR(255),
    producerLink VARCHAR(255) ,
    stripeCustomerId VARCHAR(255) 
);

-- ========= [NEW!] producersQuestionAnswers =========
CREATE TABLE producersQuestionAnswers (
    id SERIAL PRIMARY KEY,
    question VARCHAR(255),
    answer VARCHAR(255),
    date TIMESTAMP,
    userID SERIAL
);

-- ========= [NEW!] producersUpdates =========
CREATE TABLE producersUpdates (
    id SERIAL PRIMARY KEY,
    date TIMESTAMP,
    text VARCHAR(255),
    photo TEXT
);

-- ========= producersProfileViews =========
CREATE TABLE producersProfileViews (
    id SERIAL PRIMARY KEY,
    producerID INT,
    views SERIAL  -- [!] reference producersProfileViewsViews
);

-- ========= [NEW!] producersProfileViewsViews =========
CREATE TABLE producersProfileViewsViews (
    id SERIAL PRIMARY KEY,
    date TIMESTAMP,
    count INT
);

-- ========= requestEdits =========
CREATE TABLE requestEdits (
    id SERIAL PRIMARY KEY,
    editDesc TEXT,
    listingID SERIAL,
    userID SERIAL,
    brandRelation VARCHAR(255),
    reviewStatus BOOLEAN,
    duplicateLink VARCHAR(255) ,
    sourceLink VARCHAR(255) 
);

-- ========= requestInaccuracy =========
CREATE TABLE requestInaccuracy (
    id SERIAL PRIMARY KEY,
    listingID SERIAL,
    userID SERIAL,
    venueID SERIAL,
    reportDate TIMESTAMP,
    inaccurateReason TEXT ,
    reviewStatus BOOLEAN 
);

-- ========= requestListings =========
CREATE TABLE requestListings (
    id SERIAL PRIMARY KEY,
    listingName VARCHAR(255),
    bottler VARCHAR(255),
    drinkType VARCHAR(255),
    sourceLink VARCHAR(255),
    brandRelation VARCHAR(255),
    reviewStatus BOOLEAN,
    userID SERIAL,
    photo TEXT,
    originCountry VARCHAR(255) ,
    producerID SERIAL ,
    producerNew VARCHAR(255) ,
    typeCategory VARCHAR(255) ,
    abv VARCHAR(255) ,
    age VARCHAR(255) ,
    reviewLink VARCHAR(255) 
);

-- ========= reviews =========
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    userID SERIAL,
    reviewTarget SERIAL,
    rating INT,
    reviewDesc TEXT,
    reviewType VARCHAR(255),
    createdDate TIMESTAMP,
    language VARCHAR(255),
    finish VARCHAR(255),
    willRecommend BOOLEAN,
    wouldBuyAgain BOOLEAN,
    userVotes SERIAL, -- [!] reference reviewsUserVotes
    taggedUsers TEXT[] ,
    flavorTag TEXT[] ,
    photo TEXT ,
    colour VARCHAR(7) ,
    aroma VARCHAR(255) ,
    location SERIAL ,
    taste VARCHAR(255) ,
    observationTag TEXT[] ,
    address VARCHAR(255) 
);

-- ========= [NEW!] reviewsUserVotes =========
CREATE TABLE reviewsUserVotes (
    id SERIAL PRIMARY KEY,
    upvotes TEXT[],
    downvotes TEXT[]
);

-- ========= servingTypes =========
CREATE TABLE servingTypes (
    id SERIAL PRIMARY KEY,
    servingType VARCHAR(255)
);

-- ========= specialColours =========
CREATE TABLE specialColours (
    id SERIAL PRIMARY KEY,
    hexList TEXT[],
    colour VARCHAR(255)
);

-- ========= subTags =========
CREATE TABLE subTags (
    id SERIAL PRIMARY KEY,
    familyTagId SERIAL,
    subTag VARCHAR(255)
);

-- ========= tokens =========
CREATE TABLE tokens (
    id SERIAL PRIMARY KEY,
    token VARCHAR(255),
    userId SERIAL,
    requestId SERIAL,
    expiry TIMESTAMP
);

-- ========= users =========
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255),
    displayName VARCHAR(255),
    choiceDrinks TEXT[],
    modType TEXT[],
    photo TEXT,
    hashedPassword VARCHAR(255),
    drinkLists SERIAL, -- [!] reference usersDrinkLists
    joinDate TIMESTAMP,
    followLists SERIAL, -- [!] reference usersFollowLists
    firstName VARCHAR(255),
    lastName VARCHAR(255),
    email VARCHAR(255),
    isAdmin BOOLEAN,
    birthday TIMESTAMP
);

-- ========= [NEW!] usersDrinkLists =========
CREATE TABLE usersDrinkLists (
    id SERIAL PRIMARY KEY,
    user SERIAL,  -- [!] reference usersFollowLists
    drinksIHaveTried TEXT[],
    drinksIWantToTry TEXT[]
);

-- ========= [NEW!] usersFollowLists =========
CREATE TABLE usersFollowLists (
    id SERIAL PRIMARY KEY,
    users TEXT[],
    producers TEXT[],
    venues TEXT[]
);

-- ========= venues =========
CREATE TABLE venues (
    id SERIAL PRIMARY KEY,
    venueName VARCHAR(255),
    address VARCHAR(255),
    venueType VARCHAR(255),
    originLocation VARCHAR(255),
    venueDesc TEXT,
    menu SERIAL, -- [!] reference venuesMenu
    hashedPassword VARCHAR(255),
    photo TEXT,
    claimStatus BOOLEAN,
    openingHours SERIAL, -- [!] reference venuesOpeningHours
    questionAnswers SERIAL , -- [!] reference venuesQuestionAnswers
    updates SERIAL , -- [!] reference venuesUpdates
    reservationDetails VARCHAR(255) ,
    username VARCHAR(255),
    publicHolidays VARCHAR(255) ,
    stripeCustomerId VARCHAR(255) 
);

-- ========= [NEW!] venuesMenu =========
CREATE TABLE venuesMenu (
    id SERIAL PRIMARY KEY,
    sectionName VARCHAR(255),
    sectionOrder VARCHAR(255),
    sectionMenu TEXT[]
);

-- ========= [NEW!] venuesOpeningHours =========
CREATE TABLE venuesOpeningHours (
    id SERIAL PRIMARY KEY,
    Monday TEXT[],
    Tuesday TEXT[],
    Wednesday TEXT[],
    Thursday TEXT[],
    Friday TEXT[],
    Saturday TEXT[],
    Sunday TEXT[]
);

-- ========= [NEW!] venuesQuestionAnswers =========
CREATE TABLE venuesQuestionAnswers (
    id SERIAL PRIMARY KEY,
    question VARCHAR(255),
    answer VARCHAR(255),
    date TIMESTAMP,
    userID SERIAL
);

-- ========= [NEW!] venuesUpdates =========
CREATE TABLE venuesUpdates (
    id SERIAL PRIMARY KEY,
    date TIMESTAMP,
    text VARCHAR(255),
    photo TEXT
);

-- ========= venuesProfileViews =========
CREATE TABLE venuesProfileViews (
    id SERIAL PRIMARY KEY,
    venueID INT,
    views TEXT[] 
);

-- ========= [NEW!] venuesProfileViewsViews =========
CREATE TABLE venuesProfileViewsViews (
    id SERIAL PRIMARY KEY,
    date TIMESTAMP,
    count INT
);