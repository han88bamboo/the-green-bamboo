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
    photo VARCHAR(255),
    joinDate TIMESTAMP,
    isPending BOOLEAN,
    isApproved BOOLEAN
);

-- ========= badges =========
CREATE TABLE badges (
    id SERIAL PRIMARY KEY,
    badgeName VARCHAR(255),
    badgePhoto VARCHAR(255),
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
    badgePhoto VARCHAR(255),
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
    producerID INT,
    bottler VARCHAR(255),
    originCountry VARCHAR(255),
    drinkType VARCHAR(255),
    abv FLOAT,
    officialDesc TEXT,
    allowMod BOOLEAN,
    addedDate TIMESTAMP,
    typeCategory VARCHAR(255),
    age VARCHAR(255),
    reviewLink VARCHAR(255),
    sourceLink VARCHAR(255),
    photo VARCHAR(255)
);

-- ========= modRequests =========
CREATE TABLE modRequests (
    id SERIAL PRIMARY KEY,
    userID INT,
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
    photo VARCHAR(255),
    hashedPassword VARCHAR(255),
    claimStatus BOOLEAN,
    statusOB VARCHAR(255),
    questionAnswers TEXT[],
    updates TEXT[],
    producerLink VARCHAR(255),
    stripeCustomerId VARCHAR(255)
);

-- ========= producersProfileViews =========
CREATE TABLE producersProfileViews (
    id SERIAL PRIMARY KEY,
    producerID INT,
    views TEXT[]
);

-- ========= requestEdits =========
CREATE TABLE requestEdits (
    id SERIAL PRIMARY KEY,
    editDesc TEXT,
    listingID INT,
    userID INT,
    brandRelation VARCHAR(255),
    reviewStatus BOOLEAN,
    duplicateLink VARCHAR(255),
    sourceLink VARCHAR(255)
);

-- ========= requestInaccuracy =========
CREATE TABLE requestInaccuracy (
    id SERIAL PRIMARY KEY,
    listingID INT,
    userID INT,
    venueID INT,
    reportDate TIMESTAMP,
    inaccurateReason TEXT,
    reviewStatus BOOLEAN DEFAULT FALSE
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
    userID INT,
    photo VARCHAR(255),
    originCountry VARCHAR(255),
    producerID INT,
    producerNew VARCHAR(255),
    typeCategory VARCHAR(255),
    abv VARCHAR(255),
    age VARCHAR(255),
    reviewLink VARCHAR(255)
);

-- ========= reviews =========
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    userID INT,
    reviewTarget INT,
    rating INT,
    reviewDesc TEXT,
    reviewType VARCHAR(255),
    createdDate TIMESTAMP,
    language VARCHAR(255),
    finish VARCHAR(255),
    willRecommend BOOLEAN,
    wouldBuyAgain BOOLEAN,
    userVotes INT,
    taggedUsers TEXT[],
    flavorTag TEXT[],
    photo VARCHAR(255),
    colour VARCHAR(7),
    aroma VARCHAR(255),
    location INT,
    taste VARCHAR(255),
    observationTag TEXT[],
    address VARCHAR(255)
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
    familyTagId INT,
    subTag VARCHAR(255)
);

-- ========= tokens =========
CREATE TABLE tokens (
    id SERIAL PRIMARY KEY,
    token VARCHAR(255),
    userId INT,
    requestId INT,
    expiry TIMESTAMP
);

-- ========= users =========
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255),
    displayName VARCHAR(255),
    choiceDrinks TEXT[],
    modType TEXT[],
    photo VARCHAR(255),
    hashedPassword VARCHAR(255),
    drinkLists INT,
    joinDate TIMESTAMP,
    followLists INT,
    firstName VARCHAR(255),
    lastName VARCHAR(255),
    email VARCHAR(255),
    isAdmin BOOLEAN,
    birthday TIMESTAMP
);

-- ========= venues =========
CREATE TABLE venues (
    id SERIAL PRIMARY KEY,
    venueName VARCHAR(255),
    address VARCHAR(255),
    venueType VARCHAR(255),
    originLocation VARCHAR(255),
    venueDesc TEXT,
    menu TEXT[],
    hashedPassword VARCHAR(255),
    photo VARCHAR(255),
    claimStatus BOOLEAN,
    openingHours JSONB,
    questionAnswers TEXT[],
    updates TEXT[],
    reservationDetails VARCHAR(255),
    publicHolidays VARCHAR(255),
    stripeCustomerId VARCHAR(255)
);

-- ========= venuesProfileViews =========
CREATE TABLE venuesProfileViews (
    id SERIAL PRIMARY KEY,
    venueID INT,
    views TEXT[]
);
