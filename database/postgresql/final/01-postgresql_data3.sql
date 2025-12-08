-- DROP TABLES IF EXISTS -- 

DROP TABLE IF EXISTS "notifications" CASCADE;
DROP TABLE IF EXISTS "eventAttendees" CASCADE;
DROP TABLE IF EXISTS "events" CASCADE;
DROP TABLE IF EXISTS "clubPostCommentsLikes" CASCADE;
DROP TABLE IF EXISTS "clubPostCommentsDislikes" CASCADE;
DROP TABLE IF EXISTS "clubPostComments" CASCADE;
DROP TABLE IF EXISTS "clubPostsLikes" CASCADE;
DROP TABLE IF EXISTS "clubPostsDislikes" CASCADE;
DROP TABLE IF EXISTS "clubPosts" CASCADE;
DROP TABLE IF EXISTS "clubRequests" CASCADE;
DROP TABLE IF EXISTS "clubInvites" CASCADE;
DROP TABLE IF EXISTS "clubMembers" CASCADE;
DROP TABLE IF EXISTS "clubs" CASCADE;
DROP TABLE IF EXISTS "accountRequests" CASCADE;
DROP TABLE IF EXISTS "badges" CASCADE;
DROP TABLE IF EXISTS "badgeActions" CASCADE;
DROP TABLE IF EXISTS "badgeRules" CASCADE;
DROP TABLE IF EXISTS "badgeMappings" CASCADE;
DROP TABLE IF EXISTS "userBadges" CASCADE;
DROP TABLE IF EXISTS "colours" CASCADE;
DROP TABLE IF EXISTS "moreColours" CASCADE;
DROP TABLE IF EXISTS "countries" CASCADE;
DROP TABLE IF EXISTS "drinkTypes" CASCADE;
DROP TABLE IF EXISTS "flavourTags" CASCADE;
DROP TABLE IF EXISTS "languages" CASCADE;
DROP TABLE IF EXISTS "listings" CASCADE;
DROP TABLE IF EXISTS "menuItems" CASCADE;
DROP TABLE IF EXISTS "modRequests" CASCADE;
DROP TABLE IF EXISTS "observationTags" CASCADE;
DROP TABLE IF EXISTS "producerUpdateLikes" CASCADE;
DROP TABLE IF EXISTS "producers" CASCADE;
DROP TABLE IF EXISTS "producersProfileViews" CASCADE;
DROP TABLE IF EXISTS "producersOpeningHours" CASCADE;
DROP TABLE IF EXISTS "producersQuestionAnswers" CASCADE;
DROP TABLE IF EXISTS "producersUpdates" CASCADE;
DROP TABLE IF EXISTS "requestEdits" CASCADE;
DROP TABLE IF EXISTS "requestInaccuracy" CASCADE;
DROP TABLE IF EXISTS "requestListings" CASCADE;
DROP TABLE IF EXISTS "reviews" CASCADE;
DROP TABLE IF EXISTS "reviewsUserVotes" CASCADE;
DROP TABLE IF EXISTS "producerReviews" CASCADE;
DROP TABLE IF EXISTS "producerReviewsUserVotes" CASCADE;
DROP TABLE IF EXISTS "servingTypes" CASCADE;
DROP TABLE IF EXISTS "currencySymbols" CASCADE;
DROP TABLE IF EXISTS "specialColours" CASCADE;
DROP TABLE IF EXISTS "subTags" CASCADE;
DROP TABLE IF EXISTS "tokens" CASCADE;
DROP TABLE IF EXISTS "users" CASCADE;
DROP TABLE IF EXISTS "usersDrinkLists" CASCADE;
DROP TABLE IF EXISTS "usersDrinkListItems" CASCADE;
DROP TABLE IF EXISTS "usersDrinkListUpvotes" CASCADE;
DROP TABLE IF EXISTS "userProducerLists" CASCADE;
DROP TABLE IF EXISTS "userProducerListItems" CASCADE;
DROP TABLE IF EXISTS "usersFollowLists" CASCADE;
DROP TABLE IF EXISTS "venueUpdateLikes" CASCADE;
DROP TABLE IF EXISTS "venues" CASCADE;
DROP TABLE IF EXISTS "venueAmenities" CASCADE;
DROP TABLE IF EXISTS "venuesMenu" CASCADE;
DROP TABLE IF EXISTS "venuesOpeningHours" CASCADE;
DROP TABLE IF EXISTS "venuesProfileViews" CASCADE;
DROP TABLE IF EXISTS "venuesProfileViewsViews" CASCADE;
DROP TABLE IF EXISTS "venuesQuestionAnswers" CASCADE;
DROP TABLE IF EXISTS "venuesUpdates" CASCADE;
DROP TABLE IF EXISTS "typeCategories" CASCADE;
DROP TABLE IF EXISTS "associations" CASCADE; -- ADDED BY SMU GROUP 3
DROP TABLE IF EXISTS "pointsRecorder" CASCADE; -- ADDED BY SMU GROUP 3
DROP TABLE IF EXISTS "pointSystemRules" CASCADE; -- ADDED BY SMU GROUP 3
DROP TABLE IF EXISTS "venueReviews" CASCADE;
DROP TABLE IF EXISTS "venueReviewsUserVotes" CASCADE;
DROP TABLE IF EXISTS "userNotificationsRead" CASCADE;
DROP TABLE IF EXISTS "systemSettings" CASCADE;
DROP TABLE IF EXISTS "myCellarItemsChangelog" CASCADE;
DROP TABLE IF EXISTS "myCellarItems" CASCADE;
DROP TABLE IF EXISTS "myCellarCollections" CASCADE;

-- to enable trigram index for fuzzy search
CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE EXTENSION IF NOT EXISTS unaccent;

-- CREATE TABLES -- 
-- ========= "accountRequests" =========
CREATE TABLE "accountRequests" (
    "id" SERIAL PRIMARY KEY,
    "businessId" INTEGER,
    "businessName" VARCHAR(255),
    "businessType" VARCHAR(255),
    "isIndependentBottler" BOOLEAN DEFAULT FALSE,
    "businessDesc" TEXT,
    "country" VARCHAR(255),
    "pricing" VARCHAR(255),
    "businessLink" VARCHAR(255),
    "firstName" VARCHAR(255),
    "lastName" VARCHAR(255),
    "relationship" VARCHAR(255),
    "email" VARCHAR(255),
    "contact" VARCHAR(255),
    "referenceDocument" TEXT,  -- Changed to TEXT
    "photo" TEXT,
    "joinDate" TIMESTAMP,
    "isPending" BOOLEAN,
    "isApproved" BOOLEAN,
    "isNew" BOOLEAN
);

-- ========= "servingTypes" =========
CREATE TABLE "servingTypes" (
    "id" SERIAL PRIMARY KEY,
    "servingType" VARCHAR(255)
);

-- ========= "currencySymbols" =========
CREATE TABLE "currencySymbols" (
    "id" SERIAL PRIMARY KEY,
    "symbol" VARCHAR(10) NOT NULL UNIQUE
);

-- ========= "specialColours" =========
CREATE TABLE "specialColours" (
    "id" SERIAL PRIMARY KEY,
    "hexList" TEXT[],
    "colour" VARCHAR(255)
);

-- ========= "flavourTags" =========
CREATE TABLE "flavourTags" (
    "id" SERIAL PRIMARY KEY,
    "hexcode" VARCHAR(7),
    "familyTag" VARCHAR(255)
);

-- ========= "subTags" =========
CREATE TABLE "subTags" (
    "id" SERIAL PRIMARY KEY,
    "familyTagId" INTEGER REFERENCES "flavourTags"("id") ON DELETE SET NULL, -- [!] reference "flavourTags" as FK
    "subTag" VARCHAR(255) UNIQUE
);

-- ========= "badges" =========
CREATE TABLE "badges" (
    "id" SERIAL PRIMARY KEY,
    "badgeName" VARCHAR(255),
    "badgePhoto" TEXT,
    "badgeDesc" TEXT,
    "badgeType" VARCHAR(50), -- 'Country', 'Category', 'Action', 'DrinkType'
    "relatedEntity" VARCHAR(255) NULL
);

-- ========= "badgeRules" =========
CREATE TABLE "badgeRules" (
    "id" SERIAL PRIMARY KEY,
    "actionType" VARCHAR(50) NOT NULL, -- 'Country', 'Category', 'Action'
    "levelStart" INTEGER NOT NULL,
    "levelEnd" INTEGER NOT NULL,
    "actionsRequired" INTEGER NOT NULL -- Number of actions needed for levels in this range
);

-- ========= "badgeMappings" =========
CREATE TABLE "badgeMappings" (
    "id" SERIAL PRIMARY KEY,
    "badgeId" INTEGER REFERENCES "badges"("id") ON DELETE CASCADE,
    "mappingType" VARCHAR(50) NOT NULL, -- 'DrinkType', 'Category', 'Country'
    "primaryValue" VARCHAR(255) NOT NULL, -- Drink type, country name, or parent drink type for categories
    "secondaryValue" VARCHAR(255), -- Used for categories (stores the specific category)
    UNIQUE("badgeId", "mappingType", "primaryValue", "secondaryValue")
);

-- ========= "colours" =========
CREATE TABLE "colours" (
    "id" SERIAL PRIMARY KEY,
    "hexcode" VARCHAR(7)
);

-- ========= "countries" =========
CREATE TABLE "countries" (
    "id" SERIAL PRIMARY KEY,
    "originCountry" VARCHAR(255),
    "legalAge" INT
);

-- ========= "drinkTypes" =========
CREATE TABLE "drinkTypes" (
    "id" SERIAL PRIMARY KEY,
    "drinkType" VARCHAR(255),
    "badgePhoto" TEXT,
    "typeCategory" TEXT[]
);

-- ========= "typeCategories" -added by tzh for drinkStyle =========
CREATE TABLE "typeCategories" (
    "id" SERIAL PRIMARY KEY,
    "drinkType_id" INT REFERENCES "drinkTypes"(id) ON DELETE CASCADE,
    "typeCategory" VARCHAR(255) NOT NULL,
    "drinkStyle" TEXT[],
    UNIQUE("drinkType_id", "typeCategory") 
);

-- ========= "languages" =========
CREATE TABLE "languages" (
    "id" SERIAL PRIMARY KEY,
    "language" VARCHAR(255)
);

-- ========= "observationTags" =========
CREATE TABLE "observationTags" (
    "id" SERIAL PRIMARY KEY,
    "observationTag" VARCHAR(255)
);

-- ========= "venueMainTypes" =========
CREATE TABLE "venueMainTypes" (
    "id" SERIAL PRIMARY KEY,
    "venueMainType" VARCHAR(255) NOT NULL UNIQUE
);

-- ========= "venueSubTypes" =========
CREATE TABLE "venueSubTypes" (
    "id" SERIAL PRIMARY KEY,
    "venueSubType" VARCHAR(255) NOT NULL UNIQUE
);

-- ========= "producers" =========
CREATE TABLE "producers" (
    "id" SERIAL PRIMARY KEY,
    "producerName" VARCHAR(255),
    "producerDesc" TEXT,
    "originCountry" VARCHAR(255),
    "isIndependentBottler" BOOLEAN DEFAULT FALSE,
    "mainDrinks" TEXT[],
    "photo" TEXT,
    "hashedPassword" VARCHAR(255),
    "claimStatus" BOOLEAN,
    "claimStatusCheckDate" TIMESTAMP,
    "statusOB" VARCHAR(255),
    "yearFounded" INTEGER,
    "activeStatus" VARCHAR(10),
    "owner" VARCHAR(255),
    "location" VARCHAR(255),
    "openForTours" BOOLEAN,
    "website" TEXT,
    -- "questionAnswers" INTEGER REFERENCES "producersQuestionAnswers"("id") ON DELETE SET NULL, -- Alternative ON DELETE CASCADE to delete all related child records[!] reference "producersQuestionAnswers" as FK
    -- "updates" INTEGER REFERENCES "producersUpdates"("id") ON DELETE SET NULL, -- Alternative ON DELETE CASCADE to delete all related child records[!] reference "producersUpdates" as FK
    "username" VARCHAR(255),
    "producerLink" TEXT,
    "stripeCustomerId" VARCHAR(255)
);

-- Create a GIN index on listingName for trigram fuzzy search
CREATE INDEX idx_producers_name_trgm ON "producers" USING gin ("producerName" gin_trgm_ops);

CREATE TABLE "producerTextSections" (
    "id" SERIAL PRIMARY KEY,
    "producerId" INTEGER REFERENCES "producers"("id") ON DELETE CASCADE,
    "sectionTitle" VARCHAR(255),
    "richTextContent" TEXT,
    "sectionOrder" INTEGER DEFAULT 0,
    "createdDate" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "updatedDate" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ========= "venues" =========
CREATE TABLE "venues" (
    "id" SERIAL PRIMARY KEY,
    "venueName" VARCHAR(255),
    "address" VARCHAR(255),
    "venueType" VARCHAR(255),
    "originLocation" VARCHAR(255),
    "venueDesc" TEXT,
    -- "menu" SERIAL, -- [!] reference "venuesMenu"
    "hashedPassword" VARCHAR(255),
    "photo" TEXT,
    "claimStatus" BOOLEAN,
    "claimStatusCheckDate" TIMESTAMP,
    "yearOpened" INTEGER,
    "openForReservations" BOOLEAN,
    "website" TEXT,
    -- "openingHours" SERIAL, -- [!] reference "venuesOpeningHours"
    -- "questionAnswers" SERIAL, -- [!] reference "venuesQuestionAnswers"
    -- "updates" SERIAL, -- [!] reference "venuesUpdates"
    "reservationDetails" VARCHAR(255),
    "username" VARCHAR(255),
    "publicHolidays" VARCHAR(255),
    "stripeCustomerId" VARCHAR(255),
    "pin" VARCHAR(255),
    "requestId" INTEGER, -- [!] reference "accountRequests"
    "instagram" TEXT,
    "facebook" TEXT,
    "tiktok" TEXT,
    "email" TEXT,
    "phoneNumber" TEXT,
    "whatsappNumber" TEXT,
    "pdfMenuUrl" TEXT DEFAULT NULL,
    "venueMainType" INTEGER REFERENCES "venueMainTypes"("id") ON DELETE SET NULL,
    "venueSubType" INTEGER REFERENCES "venueSubTypes"("id") ON DELETE SET NULL,
    "specialStatus" VARCHAR(50) DEFAULT NULL, -- NULL for ordinary venues, 'EVENT_FESTIVAL' for event/festival organizers that need checkbox-style menu
    "showRating" BOOLEAN DEFAULT TRUE -- Whether to show average rating on profile
);

-- ALTER TABLE your_table_name 
-- ADD COLUMN "venueMainType" INTEGER REFERENCES "venueMainTypes"("id") ON DELETE SET NULL,
-- ADD COLUMN "venueSubType" INTEGER REFERENCES "venueSubTypes"("id") ON DELETE SET NULL;

-- ========= "venueAmenities" =========
CREATE TABLE "venueAmenities" (
    "id" SERIAL PRIMARY KEY,
    "venueId" INTEGER REFERENCES "venues"("id") ON DELETE CASCADE,
    -- Payment Modes
    "paymentCash" BOOLEAN DEFAULT FALSE,
    "paymentVisa" BOOLEAN DEFAULT FALSE,
    "paymentMasterCard" BOOLEAN DEFAULT FALSE,
    "paymentAmericanExpress" BOOLEAN DEFAULT FALSE,
    "paymentDiscover" BOOLEAN DEFAULT FALSE,
    "paymentApplePay" BOOLEAN DEFAULT FALSE,
    "paymentPayNow" BOOLEAN DEFAULT FALSE,
    "paymentGooglePay" BOOLEAN DEFAULT FALSE,
    "paymentSamsungPay" BOOLEAN DEFAULT FALSE,
    -- Beverage Offerings
    "beverageCocktails" BOOLEAN DEFAULT FALSE,
    "beverageWine" BOOLEAN DEFAULT FALSE,
    "beverageBeer" BOOLEAN DEFAULT FALSE,
    "beverageWhisky" BOOLEAN DEFAULT FALSE,
    "beverageBrandy" BOOLEAN DEFAULT FALSE,
    "beverageTequila" BOOLEAN DEFAULT FALSE,
    "beverageMezcal" BOOLEAN DEFAULT FALSE,
    "beverageRum" BOOLEAN DEFAULT FALSE,
    "beverageSake" BOOLEAN DEFAULT FALSE,
    "beverageShochu" BOOLEAN DEFAULT FALSE,
    "beverageSoju" BOOLEAN DEFAULT FALSE,
    "beverageBaijiu" BOOLEAN DEFAULT FALSE,
    "beverageGin" BOOLEAN DEFAULT FALSE,
    "beverageVodka" BOOLEAN DEFAULT FALSE,
    "beverageAbsinthe" BOOLEAN DEFAULT FALSE,
    "beverageArrack" BOOLEAN DEFAULT FALSE,
    -- Other Amenities (Yes/No)
    "foodServed" BOOLEAN DEFAULT FALSE,
    "outdoorSeating" BOOLEAN DEFAULT FALSE,
    "indoorSeating" BOOLEAN DEFAULT FALSE,
    "petFriendly" BOOLEAN DEFAULT FALSE,
    "childFriendly" BOOLEAN DEFAULT FALSE,
    "familyFriendly" BOOLEAN DEFAULT FALSE,
    "smokeFriendly" BOOLEAN DEFAULT FALSE,
    "wheelchairAccessibility" BOOLEAN DEFAULT FALSE,
    "freeWiFi" BOOLEAN DEFAULT FALSE,
    "happyHourDrinks" BOOLEAN DEFAULT FALSE,
    "liveMusic" BOOLEAN DEFAULT FALSE,
    "barGames" BOOLEAN DEFAULT FALSE,
    "sommelierService" BOOLEAN DEFAULT FALSE,
    "deliveryAvailable" BOOLEAN DEFAULT FALSE,
    "lgbtqFriendly" BOOLEAN DEFAULT FALSE,
    "reservationsRequired" BOOLEAN DEFAULT FALSE,
    "membershipRequired" BOOLEAN DEFAULT FALSE,
    "inStoreScheduling" BOOLEAN DEFAULT FALSE,
    "localNotPartOfChain" BOOLEAN DEFAULT FALSE,
    "casualDressing" BOOLEAN DEFAULT FALSE,
    "formalDressing" BOOLEAN DEFAULT FALSE,
    "vegetarianOptions" BOOLEAN DEFAULT FALSE,
    "breakfastService" BOOLEAN DEFAULT FALSE,
    "lunchService" BOOLEAN DEFAULT FALSE,
    "dinnerService" BOOLEAN DEFAULT FALSE,
    "nonAlcoholicOptions" BOOLEAN DEFAULT FALSE,
    "nonSmoking" BOOLEAN DEFAULT FALSE,
    "largeGroupsFriendly" BOOLEAN DEFAULT FALSE,
    "airConditioning" BOOLEAN DEFAULT FALSE,
    "indoorHeating" BOOLEAN DEFAULT FALSE,
    "coveredOutdoorSeating" BOOLEAN DEFAULT FALSE,
    "toiletsAvailable" BOOLEAN DEFAULT FALSE,
    "workStudyFriendly" BOOLEAN DEFAULT FALSE,
    "driveThru" BOOLEAN DEFAULT FALSE,
    "streetParking" BOOLEAN DEFAULT FALSE,
    "bikeParking" BOOLEAN DEFAULT FALSE,
    "tvEntertainment" BOOLEAN DEFAULT FALSE,
    "onlineOrdering" BOOLEAN DEFAULT FALSE,
    "catering" BOOLEAN DEFAULT FALSE,
    "takeaway" BOOLEAN DEFAULT FALSE,
    -- Custom amenities
    "otherAmenities" TEXT,
    "createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "ticketed" BOOLEAN DEFAULT FALSE,
    UNIQUE("venueId")
);

-- create index 
-- Create a GIN index on listingName for trigram fuzzy search
CREATE INDEX idx_venues_name_trgm ON "venues" USING gin ("venueName" gin_trgm_ops);

-- ========= "users" =========
CREATE TABLE "users" (
    "id" SERIAL PRIMARY KEY,
    "username" VARCHAR(255),
    "displayName" VARCHAR(255),
    "choiceDrinks" TEXT[],
    "modType" TEXT[],
    "photo" TEXT,
    "hashedPassword" VARCHAR(255),
    "drinkLists" JSONB,
    "producerLists" JSONB,
    "joinDate" TIMESTAMP,
    -- "followLists" SERIAL, -- [!] reference "usersFollowLists"
    "firstName" VARCHAR(255),
    "lastName" VARCHAR(255),
    "email" VARCHAR(255),
    "isAdmin" BOOLEAN,
    "birthday" TIMESTAMP,
    "pin" VARCHAR(255),
    "choiceFlavours" TEXT[], -- SMU Group 3 added in "choiceFlavours"
    "preferences" TEXT[],-- SMU Group 3 added in "preferences"
    "grails" TEXT[], -- SMU Group 3 added in "grails" - remove this to decouple db
    "upAndComing" TEXT[], -- SMU Group 3 added in "upAndComing" - remove this to decouple db
    "goats" TEXT[], -- SMU Group 3 added in "goats" - remove this to decouple db
    "blueDot" BOOLEAN DEFAULT TRUE, -- Indicates if the blue dot should be shown
    "ambassador" BOOLEAN DEFAULT FALSE,
    "categoryExpert" VARCHAR(255) DEFAULT NULL, -- Category expert designation (e.g., "Champagne Expert", "Whisky Expert", etc.)
    "country" VARCHAR(255)
);

-- Create a GIN index on username for trigram fuzzy search
CREATE INDEX idx_users_username_trgm ON "users" USING gin ("username" gin_trgm_ops);

-- ========= "userBadges" =========
CREATE TABLE "userBadges" (
    "id" SERIAL PRIMARY KEY,
    "userId" INTEGER REFERENCES "users"("id") ON DELETE CASCADE,
    "badgeId" INTEGER REFERENCES "badges"("id") ON DELETE CASCADE,
    "currentLevel" INTEGER DEFAULT 1,
    "currentProgress" INTEGER DEFAULT 0, -- Progress toward next level
    "dateEarned" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "lastUpdated" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE("userId", "badgeId")
);


-- ========= [NEW!] "producersQuestionAnswers" =========
CREATE TABLE "producersQuestionAnswers" (
    "id" SERIAL PRIMARY KEY,
    "question" VARCHAR(255),
    "answer" VARCHAR(255),
    "date" TIMESTAMP,
    "userId" INTEGER REFERENCES "users"("id") ON DELETE SET NULL, -- [!] reference "users"("id")
    "producerId" INTEGER REFERENCES "producers"("id") ON DELETE SET NULL -- [!] reference "producers"("id")
);

-- ========= [NEW!] "producersUpdates" =========
CREATE TABLE "producersUpdates" (
    "id" SERIAL PRIMARY KEY,
    "date" TIMESTAMP,
    "text" VARCHAR(255),
    "photo" TEXT,
    "producerId" INTEGER REFERENCES "producers"("id") ON DELETE SET NULL
    -- need to add likes?
);

-- ========= [NEW!] "producerUpdateLikes" =========
CREATE TABLE "producerUpdateLikes" (
    "id" SERIAL PRIMARY KEY,
    "updateId" INTEGER REFERENCES "producersUpdates"("id") ON DELETE CASCADE,
    "userId" INTEGER,
    "userType" VARCHAR(50)
);

-- ========= "producersProfileViews" =========
CREATE TABLE "producersProfileViews" (
    "id" SERIAL PRIMARY KEY,
    "date" TIMESTAMP, 
    "count" INTEGER, -- do i need this?
    "producerId" INTEGER REFERENCES "producers"("id") ON DELETE SET NULL -- [!] reference "producers" FK
    -- "views" INTEGER REFERENCES "producersProfileViewsViews"("id") ON DELETE SET NULL  -- [!] reference "producersProfileViewsViews" FK
);

-- ========= "producersOpeningHours" =========
CREATE TABLE "producersOpeningHours" (
    "id" SERIAL PRIMARY KEY,
    "Monday" TEXT[],
    "Tuesday" TEXT[],
    "Wednesday" TEXT[],
    "Thursday" TEXT[],
    "Friday" TEXT[],
    "Saturday" TEXT[],
    "Sunday" TEXT[],
    "producerId" INTEGER REFERENCES "producers"("id") ON DELETE SET NULL -- [!] reference "producers" FK
);

-- -- ========= [NEW!] "producersProfileViewsViews" =========
-- CREATE TABLE "producersProfileViewsViews" (
--     "id" SERIAL PRIMARY KEY,
--     "date" TIMESTAMP,
--     "count" INTEGER,
--     "producersProfileViewsId" INTEGER REFERENCES "producersProfileViews"("id"),
--     "producerId" INTEGER REFERENCES "producers"("id") ON DELETE SET NULL, -- [!] reference "producers" FK
-- );

-- ========= "listings" =========
CREATE TABLE "listings" (
    "id" SERIAL PRIMARY KEY,
    "listingName" VARCHAR(500),
    "producerID" INTEGER REFERENCES "producers"("id") ON DELETE SET NULL, -- [!] reference "producers" FK
    "bottler" VARCHAR(255),
    "bottlerID" INTEGER REFERENCES "producers"("id") ON DELETE SET NULL, -- [!] reference "producers" FK
    "originCountry" VARCHAR(255),
    "drinkType" VARCHAR(255),
    "abv" FLOAT,
    "officialDesc" TEXT,
    "allowMod" BOOLEAN,
    "addedDate" TIMESTAMP,
    "typeCategory" VARCHAR(255),
    "age" VARCHAR(500),
    "reviewLink" VARCHAR(255),
    "sourceLink" VARCHAR(255),
    "photo" TEXT,
    "drinkStyle" VARCHAR(255), -- added by tzh
    "tags" TEXT,
    "order" INTEGER DEFAULT NULL,
    "varietyTags" TEXT[]  -- added for variety tags feature (array of text)
);

-- create index 
-- CREATE INDEX idx_listings_search_vector 
-- ON "listings" USING GIN("searchVector");
-- Create a GIN index on listingName for trigram fuzzy search
CREATE INDEX idx_listings_name_trgm ON "listings" USING gin ("listingName" gin_trgm_ops);

-- Create index for producer-aware randomized sorting
CREATE INDEX idx_listings_producer_random_sort ON "listings" (ABS(HASHTEXT("id"::text || '-' || "producerID"::text)));

-- Cleanup function to remove listing follows when a listing is deleted
CREATE OR REPLACE FUNCTION cleanup_listing_follows()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE "usersFollowLists" 
    SET "listings" = array_remove("listings", OLD.id::text);
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- Trigger to automatically clean up follow relationships when listings are deleted
CREATE TRIGGER cleanup_listing_follows_trigger
    BEFORE DELETE ON "listings"
    FOR EACH ROW
    EXECUTE FUNCTION cleanup_listing_follows();

-- ========= "listingVariants" ========= to store user's favourite
-- CREATE TABLE "listingVariants" (
--     "listing_id" INTEGER REFERENCES "listings"("id") ON DELETE CASCADE,
--     "variant" SMALLINT, -- 2 bytes per row, Handles years from -32,768 to 32,767
--     -- "user_id" INTEGER REFERENCES "users"("id") ON DELETE CASCADE, if we ever want to track user
--     "added_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );

-- ========= "modRequests" =========
CREATE TABLE "modRequests" (
    "id" SERIAL PRIMARY KEY,
    "userID" INTEGER REFERENCES "users"("id") ON DELETE SET NULL,
    "drinkType" VARCHAR(255),
    "modDesc" TEXT,
    "reviewStatus" BOOLEAN
);

-- ========= "usersFollowLists" =========
CREATE TABLE "usersFollowLists" (
    "id" SERIAL PRIMARY KEY, 
    "userId" INTEGER REFERENCES "users"("id") ON DELETE SET NULL, -- [!] reference "users"("id")
    "users" TEXT[], -- Contains "users"("id")s
    "producers" TEXT[], -- Contains "producers"("id")s
    "venues" TEXT[], -- Contains "venues"("id")s
    "listings" TEXT[] -- Contains "listings"("id")s
);

-- ========= "usersDrinkLists" =========
CREATE TABLE "usersDrinkLists" (
    "id" SERIAL PRIMARY KEY,
    "userId" INTEGER REFERENCES "users"("id") ON DELETE SET NULL,  -- [!] reference "users" FK
    "listName" TEXT,
    "listDesc" TEXT,
    "isPublic" BOOLEAN DEFAULT false,
    "upvotes" INTEGER DEFAULT 0,
    "createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- "drinks" TEXT[],-- Contains "listings"("id")s
    UNIQUE ("userId", "listName")
);

-- ========= "usersDrinkListItems" =========
CREATE TABLE "usersDrinkListItems" (
    "id" SERIAL PRIMARY KEY,
    "listId" INTEGER REFERENCES "usersDrinkLists"("id") ON DELETE CASCADE, -- [!] reference "usersDrinkLists" FK
    "drinkId" INTEGER REFERENCES "listings"("id") ON DELETE CASCADE,
    "addedDate" TIMESTAMP,
    "note" TEXT DEFAULT '',
    UNIQUE ("listId", "drinkId")
);

-- ========= "usersDrinkListUpvotes" =========
CREATE TABLE IF NOT EXISTS "usersDrinkListUpvotes" (
    "id" SERIAL PRIMARY KEY,
    "listId" INTEGER REFERENCES "usersDrinkLists"("id") ON DELETE CASCADE,
    "userId" INTEGER REFERENCES "users"("id") ON DELETE CASCADE,
    "createdAt" TIMESTAMP DEFAULT NOW(),
    UNIQUE ("listId", "userId")
);

-- ========= "userProducerLists" =========
CREATE TABLE "userProducerLists" (
    "id" SERIAL PRIMARY KEY,
    "userId" INTEGER REFERENCES "users"("id") ON DELETE SET NULL,
    "listName" TEXT,
    "listDesc" TEXT,
    UNIQUE ("userId", "listName")
);

-- ========= "userProducerListItems" =========
CREATE TABLE "userProducerListItems" (
    "id" SERIAL PRIMARY KEY,
    "listId" INTEGER REFERENCES "userProducerLists"("id") ON DELETE CASCADE,
    "producerId" INTEGER REFERENCES "producers"("id") ON DELETE CASCADE,
    "addedDate" TIMESTAMP,
    UNIQUE ("listId", "producerId")
);

-- ========= "userVenueLists" =========
CREATE TABLE "userVenueLists" (
    "id" SERIAL PRIMARY KEY,
    "userId" INTEGER REFERENCES "users"("id") ON DELETE SET NULL,
    "listName" TEXT,
    "listDesc" TEXT,
    UNIQUE ("userId", "listName")
);

-- ========= "userVenueListItems" =========
CREATE TABLE "userVenueListItems" (
    "id" SERIAL PRIMARY KEY,
    "listId" INTEGER REFERENCES "userVenueLists"("id") ON DELETE CASCADE,
    "venueId" INTEGER REFERENCES "venues"("id") ON DELETE CASCADE,
    "addedDate" TIMESTAMP,
    UNIQUE ("listId", "venueId")
);

-- ========= "reviews" =========
CREATE TABLE "reviews" (
    "id" SERIAL PRIMARY KEY,
    "userID" INTEGER REFERENCES "users"("id") ON DELETE SET NULL, -- [!] reference "users"("id")
    "reviewTarget" INTEGER REFERENCES "listings"("id") ON DELETE SET NULL, -- [!] reference "listings"("id")
    "rating" DECIMAL(3,1),
    "reviewDesc" TEXT,
    "reviewType" VARCHAR(255),
    "createdDate" TIMESTAMP,
    "language" VARCHAR(255),
    "finish" VARCHAR(750),
    "willRecommend" BOOLEAN NULL,
    "wouldBuyAgain" BOOLEAN NULL,
    -- "userVotes" SERIAL, -- [!] reference "reviewsUserVotes" FK
    "taggedUsers" TEXT[], -- Contains "users"("id")s
    "flavourTag" TEXT[], -- Contains "flavourTags"("id")s
    "photo" TEXT,
    "colour" VARCHAR(7),
    "aroma" VARCHAR(750),
    "location" INTEGER REFERENCES "venues"("id") ON DELETE SET NULL, -- [!] references "venues" FK
    "taste" VARCHAR(750),
    "observationTag" TEXT[], -- Contains "observationTags" text
    "address" VARCHAR(255),
    "variant" SMALLINT DEFAULT NULL, -- 2 bytes per row, Handles years from -32,768 to 32,767
    "isPublic" BOOLEAN DEFAULT TRUE -- True if publicly viewable
);

-- ========= "reviewsUserVotes" =========
CREATE TABLE "reviewsUserVotes" (
    "id" SERIAL PRIMARY KEY,
    "upvotes" JSONB DEFAULT '[]', -- Contains "users"("id")s and date
    "downvotes" JSONB DEFAULT '[]', -- Contains "users"("id")s and date
    "reviewId" INTEGER REFERENCES "reviews"("id") on DELETE SET NULL -- [!] reference "reviews" FK
);

-- ========= "userLeaderboard" ========= to store user's favourite
CREATE TABLE "userLeaderboard" (
    "user_id" INTEGER REFERENCES "users"("id") ON DELETE CASCADE,
    "listing_id" INTEGER REFERENCES "listings"("id") ON DELETE CASCADE,
    "category" VARCHAR(20),  -- e.g. 'grails', 'upAndComing', 'goats'
    "sort_order" INTEGER,    -- whatever user listed will always be kept in order
    "added_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "vintage" SMALLINT DEFAULT NULL,
    PRIMARY KEY ("user_id", "listing_id", "category")
);

CREATE TABLE "producerReviews" (
    "id" SERIAL PRIMARY KEY,
    "userID" INTEGER REFERENCES "users"("id") ON DELETE SET NULL, -- Reference to users table
    "producerID" INTEGER REFERENCES "producers"("id") ON DELETE SET NULL, -- Reference to producers table
    "rating" DECIMAL(3,1),
    "reviewDesc" TEXT,
    "createdDate" TIMESTAMP,
    "photos" TEXT[]
    -- "userVotes" SERIAL, -- [!] reference "producerReviewsUserVotes" FK
);

CREATE TABLE "producerReviewsUserVotes" (
    "id" SERIAL PRIMARY KEY,
    "upvotes" TEXT[], -- Contain "users"("id")s
    "downvotes" TEXT[], -- Contain "users"("id")s
    "reviewId" INTEGER REFERENCES "producerReviews"("id") on DELETE SET NULL -- [!] reference "producerReviews" FK
);

-- ==========================================
-- VENUE REVIEWS
-- ==========================================
CREATE TABLE "venueReviews" (
    "id" SERIAL PRIMARY KEY,
    "userID" INTEGER REFERENCES "users"("id") ON DELETE SET NULL,
    "venueID" INTEGER REFERENCES "venues"("id") ON DELETE SET NULL,
    "rating" DECIMAL(3,1),
    "reviewDesc" TEXT,
    "createdDate" TIMESTAMP,
    "photos" TEXT[]
);

-- ==========================================
-- VENUE REVIEWS USER VOTES
-- ==========================================
CREATE TABLE "venueReviewsUserVotes" (
    "id" SERIAL PRIMARY KEY,
    "upvotes" TEXT[], -- Contain "users"("id")s
    "downvotes" TEXT[], -- Contain "users"("id")s
    "reviewId" INTEGER REFERENCES "venueReviews"("id") ON DELETE SET NULL    
);


-- ========= "tokens" =========
CREATE TABLE "tokens" (
    "id" SERIAL PRIMARY KEY,
    "token" VARCHAR(255),
    "userId" INTEGER REFERENCES "users"("id") ON DELETE SET NULL, -- [!] reference "users" FK
    "producerId" INTEGER REFERENCES "producers"("id") ON DELETE SET NULL, -- [!] reference "producers" FK
    "venueId" INTEGER REFERENCES "venues"("id") ON DELETE SET NULL, -- [!] reference "venues" FK
    "requestId" INTEGER REFERENCES "accountRequests"("id") ON DELETE SET NULL, -- [!] reference "accountRequests" FK
    "expiry" TIMESTAMP
);


-- 1. Rename existing table
-- ALTER TABLE "venuesMenu" RENAME TO "venuesMenu_old";


-- ========= "venuesMenu" =========
CREATE TABLE "venuesMenu" (
    "id" SERIAL PRIMARY KEY,
    "sectionName" VARCHAR(255),
    "sectionOrder" VARCHAR(255),
    "venueId" INTEGER REFERENCES "venues"("id") ON DELETE SET NULL ,
    "parentSectionId" INTEGER REFERENCES "venuesMenu"("id") ON DELETE CASCADE,
    "isSubSection" BOOLEAN GENERATED ALWAYS AS ("parentSectionId" IS NOT NULL) STORED,
    "isVisible" BOOLEAN NOT NULL DEFAULT TRUE,
    "sectionDescription" TEXT, -- Description text for the menu section
    "subscribersEnabled" BOOLEAN DEFAULT FALSE, -- Whether venue has enabled subscription for this section
    "subscribers" TEXT[] DEFAULT '{}', -- Array of user IDs who have subscribed to this section
    "createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Natural key for UPSERT matching (must be unique index with expression for COALESCE)
CREATE UNIQUE INDEX "unique_section_per_venue" 
ON "venuesMenu" ("venueId", "sectionName", COALESCE("parentSectionId", -1));

-- 3. Copy data from old table
-- INSERT INTO "venuesMenu" ("id", "sectionName", "sectionOrder", "venueId")
-- SELECT "id",
--        "sectionName",
--        "sectionOrder"::INTEGER,
--        "venueId"
-- FROM "venuesMenu_old";


-- 4. remove the old table
-- DROP TABLE "venuesMenu_old";


-- ========= "menuItems" =========
CREATE TABLE "menuItems" (
    "id" SERIAL PRIMARY KEY,
    "itemOrder" INTEGER,
    "itemPrice" DECIMAL(10,2),
    "itemAvailability" BOOLEAN,
    "itemID" INTEGER REFERENCES "listings"("id") ON DELETE SET NULL,
    "itemServingType" INTEGER REFERENCES "servingTypes"("id") ON DELETE SET NULL,
    "sectionId" INTEGER REFERENCES "venuesMenu"("id") ON DELETE CASCADE,
    "variant" SMALLINT DEFAULT NULL, -- 2 bytes per row, Handles years from -32,768 to 32,767
    "new" BOOLEAN,
    "staffPick" BOOLEAN,
    "itemPriceCurrency" VARCHAR(10) DEFAULT 'Tokens', -- newly added to support currency drop-down list
    "createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Natural key for UPSERT matching (must be unique index with expression for COALESCE)
CREATE UNIQUE INDEX "unique_item_per_section" 
ON "menuItems" ("sectionId", "itemID", COALESCE("variant", -1));

-- ALTER TABLE "menuItems" ADD COLUMN "variant" SMALLINT DEFAULT NULL;

-- ========= "venuesOpeningHours" =========
CREATE TABLE "venuesOpeningHours" (
    "id" SERIAL PRIMARY KEY,
    "Monday" TEXT[],
    "Tuesday" TEXT[],
    "Wednesday" TEXT[],
    "Thursday" TEXT[],
    "Friday" TEXT[],
    "Saturday" TEXT[],
    "Sunday" TEXT[],
    "venueId" INTEGER REFERENCES "venues"("id") ON DELETE SET NULL -- [!] References venues FK
);

-- ========= "venuesQuestionAnswers" =========
CREATE TABLE "venuesQuestionAnswers" (
    "id" SERIAL PRIMARY KEY,
    "question" VARCHAR(255),
    "answer" VARCHAR(255),
    "date" TIMESTAMP,
    "userId" INTEGER REFERENCES "users"("id") ON DELETE SET NULL,
    "venueId" INTEGER REFERENCES "venues"("id") ON DELETE SET NULL -- [!] References venues FK
);

-- ========= "venuesUpdates" =========
CREATE TABLE "venuesUpdates" (
    "id" SERIAL PRIMARY KEY,
    "date" TIMESTAMP,
    "text" VARCHAR(255),
    "photo" TEXT,
    "venueId" INTEGER REFERENCES "venues"("id") ON DELETE SET NULL -- [!] References venues FK
    -- need add likes?
);

-- ========= "venueUpdateLikes" =========
CREATE TABLE "venueUpdateLikes" (
    "id" SERIAL PRIMARY KEY,
    "updateId" INTEGER REFERENCES "venuesUpdates"("id") ON DELETE CASCADE,
    "userId" INTEGER,
    "userType" VARCHAR(50)
);

-- -- ========= "venuesProfileViewsViews" =========
-- CREATE TABLE "venuesProfileViewsViews" (
--     "id" SERIAL PRIMARY KEY,
--     "date" TIMESTAMP,
--     "count" INT
-- );

-- ========= "venuesProfileViews" =========
CREATE TABLE "venuesProfileViews" (
    "id" SERIAL PRIMARY KEY,
    "date" TIMESTAMP,
    "count" INT,
    "venueId" INTEGER REFERENCES "venues"("id") ON DELETE SET NULL -- [!] References venues FK
);

-- -- ========= "venuesProfileViews" =========
-- CREATE TABLE "venuesProfileViews" (
--     "id" SERIAL PRIMARY KEY,
--     "venueId" INT, -- [!] FK VENUES
--     "views" TEXT[] -- [!] reference venuesProfileViewsViews FK
--     "venueId" INTEGER REFERENCES "venues"("id") ON DELETE SET NULL -- [!] References venues FK
-- );

-- ========= "requestInaccuracy" =========
CREATE TABLE "requestInaccuracy" (
    "id" SERIAL PRIMARY KEY,
    "listingId" INTEGER REFERENCES "listings"("id") ON DELETE SET NULL, -- [!] References listings FK
    "userId" INTEGER REFERENCES "users"("id") ON DELETE SET NULL, -- [!] References users FK
    "venueId" INTEGER REFERENCES "venues"("id") ON DELETE SET NULL, -- [!] References venues FK
    "reportDate" TIMESTAMP,
    "inaccurateReason" TEXT,
    "reviewStatus" BOOLEAN 
);

-- ========= "requestListings" =========
CREATE TABLE "requestListings" (
    "id" SERIAL PRIMARY KEY,
    "listingName" VARCHAR(255),
    "bottler" VARCHAR(255), 
    "drinkType" VARCHAR(255),
    "sourceLink" VARCHAR(255),
    "brandRelation" VARCHAR(255),
    "reviewStatus" BOOLEAN,
    "userID" INTEGER REFERENCES "users"("id") ON DELETE SET NULL, -- [!] References users FK
    "photo" TEXT,
    "originCountry" VARCHAR(255),
    "producerID" INTEGER REFERENCES "producers"("id") ON DELETE SET NULL, -- [!] References producers FK
    "bottlerID" INTEGER REFERENCES "producers"("id") ON DELETE SET NULL, -- [!] References producers FK
    "producerNew" VARCHAR(255),
    "typeCategory" VARCHAR(255),
    "abv" VARCHAR(255),
    "age" VARCHAR(255),
    "reviewLink" VARCHAR(255),
    "drinkStyle" VARCHAR(255), -- added by tzh
    "officialDesc" TEXT, -- added by tzh
    "submitterType" VARCHAR(20) DEFAULT 'user',  -- added by tzh
    "venueID" INTEGER REFERENCES "venues"("id") ON DELETE SET NULL,  -- added by tzh
    "varietyTags" TEXT[]  -- added for variety tags feature
);

-- ========= "requestEdits" =========
CREATE TABLE "requestEdits" (
    "id" SERIAL PRIMARY KEY,
    "editDesc" TEXT,
    "listingID" INTEGER REFERENCES "listings"("id") ON DELETE SET NULL, -- [!] References listings FK
    "userID" INTEGER REFERENCES "users"("id") ON DELETE SET NULL, -- [!] References users FK
    "brandRelation" VARCHAR(255),
    "reviewStatus" BOOLEAN,
    "duplicateLink" VARCHAR(255),
    "sourceLink" VARCHAR(255)
);

-- ========= "clubs" =========
CREATE TABLE "clubs" (
    "id" SERIAL PRIMARY KEY,
    "clubName" VARCHAR(255),
    "clubDesc" TEXT,
    "isInviteOnly" BOOLEAN,
    "clubLink" VARCHAR(255),
    "clubBanner" TEXT,
    "dateCreated" TIMESTAMP,
    "totalMembers" INTEGER,
    "createdByID" INTEGER, -- [!] "producers" or "venues" or "users" id in their respective tables
    "createdByType" VARCHAR(255) -- [!] "producers" or "venues" or "users"
);

-- ========= "clubMembers" =========
CREATE TABLE "clubMembers" (
    "id" SERIAL PRIMARY KEY,
    "clubID" INTEGER REFERENCES "clubs"("id") ON DELETE SET NULL, -- [!] References clubs FK
    "userID" INTEGER,
    "userType" VARCHAR(255),
    "joinDate" TIMESTAMP,
    "isAdmin" BOOLEAN
);

-- ========= "clubInvites" =========
CREATE TABLE "clubInvites" (
    "id" SERIAL PRIMARY KEY,
    "clubID" INTEGER REFERENCES "clubs"("id") ON DELETE SET NULL, -- [!] References clubs FK
    "inviteeID" INTEGER,
    "inviteeUserType" VARCHAR(255),
    "inviterID" INTEGER,
    "inviterUserType" VARCHAR(255),
    "inviteDate" TIMESTAMP
);

-- ========= "clubRequests" =========
CREATE TABLE "clubRequests" (
    "id" SERIAL PRIMARY KEY,
    "clubID" INTEGER REFERENCES "clubs"("id") ON DELETE SET NULL, -- [!] References clubs FK
    "userID" INTEGER,
    "userType" VARCHAR(255),
    "requestDate" TIMESTAMP
);

-- ========= "clubPosts" =========
CREATE TABLE "clubPosts" (
    "id" SERIAL PRIMARY KEY,
    "clubID" INTEGER REFERENCES "clubs"("id") ON DELETE SET NULL, -- [!] References clubs FK
    "postDate" TIMESTAMP,
    "postContent" TEXT,
    "postPhotos" TEXT[],
    "posterID" INTEGER REFERENCES "clubMembers"("id") ON DELETE SET NULL -- [!] References clubMembers FK
);

-- ========= "clubPostsLikes" =========
CREATE TABLE "clubPostsLikes" (
    "id" SERIAL PRIMARY KEY,
    "clubID" INTEGER REFERENCES "clubs"("id") ON DELETE SET NULL, -- [!] References clubs FK
    "postID" INTEGER REFERENCES "clubPosts"("id") ON DELETE SET NULL, -- [!] References clubPOsts FK
    "memberID" INTEGER REFERENCES "clubMembers"("id") ON DELETE SET NULL -- [!] References clubMembers FK
);

-- ========= "clubPostsDislikes" =========
 CREATE TABLE "clubPostsDislikes" (
     "id" SERIAL PRIMARY KEY,
     "clubID" INTEGER REFERENCES "clubs"("id") ON DELETE SET NULL, -- [!] References clubs FK
     "postID" INTEGER REFERENCES "clubPosts"("id") ON DELETE SET NULL, -- [!] References clubPOsts FK
     "memberID" INTEGER REFERENCES "clubMembers"("id") ON DELETE SET NULL -- [!] References clubMembers FK
 );

-- ========= "clubPostComments" =========
CREATE TABLE "clubPostComments" (
    "id" SERIAL PRIMARY KEY,
    "postID" INTEGER REFERENCES "clubPosts"("id") ON DELETE SET NULL, -- [!] References clubPosts FK
    "commentDate" TIMESTAMP,
    "commentContent" TEXT,
    "commenterID" INTEGER REFERENCES "clubMembers"("id") ON DELETE SET NULL -- [!] References clubMembers FK
);

-- ========= "clubPostCommentsLikes" =========
CREATE TABLE "clubPostCommentsLikes" (
    "id" SERIAL PRIMARY KEY,
    "postID" INTEGER REFERENCES "clubPosts"("id") ON DELETE CASCADE, -- Automatically delete when clubPosts record is deleted
    "commentID" INTEGER REFERENCES "clubPostComments"("id") ON DELETE SET NULL, -- Keep as SET NULL if needed
    "memberID" INTEGER REFERENCES "clubMembers"("id") ON DELETE SET NULL -- Keep as SET NULL if needed
);

-- ========= "clubPostCommentsDislikes" =========
CREATE TABLE "clubPostCommentsDislikes" (
    "id" SERIAL PRIMARY KEY,
    "postID" INTEGER REFERENCES "clubPosts"("id") ON DELETE CASCADE, -- Automatically delete when clubPosts record is deleted
    "commentID" INTEGER REFERENCES "clubPostComments"("id") ON DELETE SET NULL, -- Keep as SET NULL if needed
    "memberID" INTEGER REFERENCES "clubMembers"("id") ON DELETE SET NULL -- Keep as SET NULL if needed
);

-- ========= "events" =========
CREATE TABLE "events" (
    "id" SERIAL PRIMARY KEY,
    "eventName" VARCHAR(255),
    "eventDesc" TEXT,
    "eventType" VARCHAR(255),
    "eventStartDate" DATE,
    "eventEndDate" DATE,
    "eventStartTime" TIME,
    "eventEndTime" TIME,
    "eventLimit" INTEGER,
    "eventBanners" TEXT[],
    "ticketed" BOOLEAN,
    "paidEvent" BOOLEAN,
    "eventLocation" TEXT,
    "paymentLink" VARCHAR(255),
    "eventOwnerID" INTEGER, -- [!] "producers" or "venues" or "users" id in their respective tables 
    "eventOwnerType" VARCHAR(255), -- [!] "producers" or "venues" or "users"
    "numAttendees" INTEGER,
    "createdDate" TIMESTAMP,
    "passcode" JSONB DEFAULT NULL, -- Optional passcode for event access with usage limits [{"code": "Merlion65", "limit": 50}, {"code": "Changi66", "limit": 30}]
    "signupOpen" BOOLEAN DEFAULT TRUE -- Indicates if event signup is open - NOT USED AT THE MOMENT
);

-- ========= "eventAttendees" =========
CREATE TABLE "eventAttendees" (
    "id" SERIAL PRIMARY KEY,
    "eventID" INTEGER REFERENCES "events"("id") ON DELETE SET NULL, -- [!] References events FK
    "eventDate" DATE,
    "eventStartTime" TIME,
    "userID" INTEGER,
    "attendeeType" VARCHAR(255),
    "attendeeStatus" BOOLEAN,
    "hasPaid" BOOLEAN DEFAULT FALSE,
    "attendanceStatus" VARCHAR(50) DEFAULT 'Not Checked In',
    "rsvpTimestamp" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "firstName" VARCHAR(50), -- contact info for RSVP event access
    "lastName" VARCHAR(50), -- contact info for RSVP event access
    "phoneNumber" VARCHAR(50), -- contact info for RSVP event access
    "email" VARCHAR(50), -- contact info for RSVP event access
    "passcodeUsed" VARCHAR(100) -- tracks which specific passcode each attendee used
);

-- ========= "associations" =========
CREATE TABLE "associations" (
    "id" SERIAL PRIMARY KEY,
    "subTag1" VARCHAR(255) REFERENCES "subTags"("subTag") ON DELETE SET NULL, -- [!] References subTags FK
    "subTag2" VARCHAR(255) REFERENCES "subTags"("subTag") ON DELETE SET NULL -- [!] References subTags FK
);

-- ======== "pointsRecorder" =========
CREATE TABLE "pointsRecorder" (
    "id" SERIAL PRIMARY KEY,
    "userID" INTEGER,
    "userType" VARCHAR(255),
    "currentPoints" INTEGER
);

-- ========= "pointSystemRules" =========
CREATE TABLE "pointSystemRules" (
    "id" SERIAL PRIMARY KEY,
    "ruleName" VARCHAR(255),
    "ruleDesc" TEXT,
    "ruleCategory" VARCHAR(255),
    "proofPoints" INTEGER
);

-- ========= "grails" ==========
CREATE TABLE "grails" (
    "id" SERIAL PRIMARY KEY,
    "listingName" VARCHAR(255),
    "listingID" INTEGER REFERENCES "listings"("id") ON DELETE SET NULL, -- [!] References listings FK
    "drinkType" VARCHAR(255),
    "typeCategory" VARCHAR(255),
    "counter" INTEGER,
    "vintage" SMALLINT DEFAULT NULL -- 2 bytes per row, Handles years from -32,768 to 32,767
);

-- ========= "upAndComing" ==========
CREATE TABLE "upAndComing" (
    "id" SERIAL PRIMARY KEY,
    "listingName" VARCHAR(255),
    "listingID" INTEGER REFERENCES "listings"("id") ON DELETE SET NULL, -- [!] References listings FK
    "drinkType" VARCHAR(255),
    "typeCategory" VARCHAR(255),
    "counter" INTEGER,
    "vintage" SMALLINT DEFAULT NULL -- 2 bytes per row, Handles years from -32,768 to 32,767
);

-- ========= "goats" ==========
CREATE TABLE "goats" (
    "id" SERIAL PRIMARY KEY,
    "listingName" VARCHAR(255),
    "listingID" INTEGER REFERENCES "listings"("id") ON DELETE SET NULL, -- [!] References listings FK
    "drinkType" VARCHAR(255),
    "typeCategory" VARCHAR(255),
    "counter" INTEGER,
    "vintage" SMALLINT DEFAULT NULL -- 2 bytes per row, Handles years from -32,768 to 32,767
);

-- ========= [NEW!] notifications =========
CREATE TABLE "notifications" (
    "id" SERIAL PRIMARY KEY,
    "userId" INTEGER, -- User ID who receives the notification
    "userType" VARCHAR(50), -- e.g., 'producer', 'venue', 'user'
    "notiTabs" VARCHAR(50), -- e.g., 'forYou', 'venues & producers'
    "notiType" VARCHAR(50), -- e.g., 'newEvent', 'clubPost', 'producerUpdate', 'venueUpdate', 'drinkReview'
    "image" TEXT, -- Image associated with the notification
    "link" TEXT, -- Link to the related entity
    "message" TEXT,
    "createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "read" BOOLEAN DEFAULT FALSE, -- Indicates if the notification has been read
    "blueDot" BOOLEAN DEFAULT TRUE -- Indicates if the blue dot should be shown
);

-- ========== [NEW!] latestFollowers =========
-- This table stores the latest followers for each user
CREATE TABLE "latestUserFollowers" (
    "id" SERIAL PRIMARY KEY,
    "userId" INTEGER REFERENCES "users"("id") ON DELETE CASCADE, -- User who is following someone
    "followingId" INTEGER REFERENCES "users"("id") ON DELETE CASCADE, -- User being followed
    "followDate" TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Date when the follow occurred
    UNIQUE ("userId", "followingId") -- Ensure no duplicate follows
);

-- ========== [NEW!] moreColours for reviews =========
CREATE TABLE "moreColours" (
    "id" SERIAL PRIMARY KEY,
    "hexcode" VARCHAR(7)
);


-- ========= "systemSettings" =========
CREATE TABLE "systemSettings" (
    "id" SERIAL PRIMARY KEY,
    "settingName" VARCHAR(255) UNIQUE NOT NULL,
    "settingValue" TEXT NOT NULL,
    "settingDescription" TEXT,
    "lastUpdated" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ========= "myCellarCollections" =========
CREATE TABLE "myCellarCollections" (
    "id" SERIAL PRIMARY KEY,
    "ownerID" INTEGER NOT NULL, -- Account ID (user, producer, or venue)
    "ownerType" VARCHAR(50) NOT NULL, -- 'user', 'producer', 'venue'
    "collectionName" VARCHAR(255) NOT NULL,
    "isDefault" BOOLEAN DEFAULT FALSE, -- True for the default collection
    "isPublic" BOOLEAN DEFAULT TRUE, -- True if publicly viewable
    "createdDate" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "updatedDate" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE ("ownerID", "ownerType", "collectionName") -- Prevent duplicate collection names per owner
);

-- Create partial unique constraint: only one default collection per owner
CREATE UNIQUE INDEX idx_cellar_collections_default_unique 
ON "myCellarCollections" ("ownerID", "ownerType") 
WHERE "isDefault" = TRUE;

-- Create index for faster lookups
CREATE INDEX idx_cellar_collections_owner ON "myCellarCollections" ("ownerID", "ownerType");

-- ========= "myCellarItems" =========
CREATE TABLE "myCellarItems" (
    "id" SERIAL PRIMARY KEY,
    "listingID" INTEGER REFERENCES "listings"("id") ON DELETE SET NULL, -- Reference to the drink listing
    "collectionID" INTEGER REFERENCES "myCellarCollections"("id") ON DELETE SET NULL, -- Collection this item belongs to
    "variant" SMALLINT DEFAULT NULL, -- Wine vintage or other variant (reusing existing pattern)
    
    -- Inventory Details
    "quantityVariantID" INTEGER DEFAULT 1, -- 1 = master record, >1 = individual bottles
    "variantGroupID" INTEGER REFERENCES "myCellarItems"("id") ON DELETE SET NULL, -- Groups versions with the same information across all these fields (collectionID, listingID, variant, drinkFormat, volumeNumber, volumeUnit), by referencing the primary master item's ID
    
    -- SHARED PROPERTIES (only stored in quantityVariantID = 1, NULL for others)
    "drinkFormat" VARCHAR(50) DEFAULT NULL, -- 'Bottle', 'Can', 'Sample', etc. [MASTER ONLY]
    "volumeNumber" DECIMAL(10,2) DEFAULT NULL, -- Volume number [MASTER ONLY]
    "volumeUnit" VARCHAR(10) DEFAULT NULL,
    "drinkByDate" DATE DEFAULT NULL, -- Latest recommended consumption date [MASTER ONLY]
    "drinkOnwardsDate" DATE DEFAULT NULL, -- Earliest recommended consumption date [MASTER ONLY]
    "currentValueEstimation" DECIMAL(10,2) DEFAULT NULL, -- Current market value [MASTER ONLY]
    "currentValueCurrency" VARCHAR(3) DEFAULT NULL, -- ISO currency code [MASTER ONLY]
    "suggestedFoodPairing" TEXT DEFAULT NULL, -- User-defined food pairing suggestions [MASTER ONLY]
    
    -- INDIVIDUAL BOTTLE PROPERTIES (stored for each bottle including master)
    "purchaseDate" DATE DEFAULT NULL,
    "deliveryDate" DATE DEFAULT NULL,
    "purchasePrice" DECIMAL(10,2) DEFAULT NULL,
    "purchaseCurrency" VARCHAR(3) DEFAULT 'USD', -- ISO currency code
    "purchaseVenueID" INTEGER REFERENCES "venues"("id") ON DELETE SET NULL, -- If purchased from a known venue
    "purchasePlaceName" VARCHAR(255) DEFAULT NULL, -- Name of place purchased (for non-venue locations)
    "purchaseAddress" VARCHAR(255) DEFAULT NULL, -- Address from Google Maps API (similar to reviews.address)
    "status" VARCHAR(50) DEFAULT 'In Possession', -- 'In Possession', 'On Its Way', 'Purchased', 'Held Elsewhere', 'Wishlisted', 'Consumed'
    "consumption" VARCHAR(50) DEFAULT 'Unopened', -- 'Opened', 'Unopened', 'Empty'
    "currentLocation" VARCHAR(255) DEFAULT 'At Home', -- 'At Home', 'At Friend''s Home', 'At Restaurant', or custom
    "subLocation" VARCHAR(255) DEFAULT NULL, -- 'In my attic', 'Wine fridge', etc. - custom location details
    "noteToSelf" TEXT DEFAULT NULL, -- Personal notes about this specific bottle
    "archiveStatus" BOOLEAN DEFAULT FALSE, -- True if bottle is archived (soft delete), False if active
    
    -- Metadata
    "addedDate" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "updatedDate" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT check_status CHECK ("status" IN ('In Possession', 'On Its Way', 'Purchased', 'Held Elsewhere', 'Wishlisted', 'Consumed')),
    CONSTRAINT check_consumption CHECK ("consumption" IN ('Opened', 'Unopened', 'Empty')),
    CONSTRAINT check_quantity_variant_positive CHECK ("quantityVariantID" >= 1),
    CONSTRAINT check_volume_positive CHECK ("volumeNumber" IS NULL OR "volumeNumber" > 0),
    CONSTRAINT check_price_positive CHECK ("purchasePrice" IS NULL OR "purchasePrice" >= 0),
    CONSTRAINT check_value_positive CHECK ("currentValueEstimation" IS NULL OR "currentValueEstimation" >= 0),
    
    -- Master-Detail Pattern Constraints
    -- Only quantityVariantID = 1 can have shared properties
    
    CONSTRAINT check_master_shared_properties CHECK (
    ("quantityVariantID" = 1) OR 
    ("quantityVariantID" > 1 AND "drinkFormat" IS NULL AND "volumeNumber" IS NULL AND "volumeUnit" IS NULL AND
     "drinkByDate" IS NULL AND "drinkOnwardsDate" IS NULL AND 
     "currentValueEstimation" IS NULL AND "currentValueCurrency" IS NULL AND 
     "suggestedFoodPairing" IS NULL)
    ),
    
    -- Ensure unique master record per listing+variant+format+volume combination
    UNIQUE ("listingID", "variant", "drinkFormat", "volumeNumber", "volumeUnit", "quantityVariantID") DEFERRABLE INITIALLY DEFERRED
);

-- Create indexes for performance
CREATE INDEX idx_cellar_listing ON "myCellarItems" ("listingID");
CREATE INDEX idx_cellar_collection ON "myCellarItems" ("collectionID");
CREATE INDEX idx_cellar_status ON "myCellarItems" ("status");
CREATE INDEX idx_cellar_dates ON "myCellarItems" ("drinkByDate", "drinkOnwardsDate");
CREATE INDEX idx_cellar_archive_status ON "myCellarItems" ("archiveStatus");
CREATE INDEX idx_cellar_variant_group ON "myCellarItems" ("variantGroupID");

-- Master-Detail Pattern Indexes
CREATE INDEX idx_cellar_master_lookup ON "myCellarItems" ("listingID", "variant", "drinkFormat", "volumeNumber", "volumeUnit", "quantityVariantID");
CREATE INDEX idx_cellar_group_lookup ON "myCellarItems" ("listingID", "variant", "drinkFormat", "volumeNumber", "volumeUnit") WHERE "quantityVariantID" = 1;

-- ========= "myCellarItemsChangelog" =========
CREATE TABLE "myCellarItemsChangelog" (
    "id" SERIAL PRIMARY KEY,
    "cellarItemID" INTEGER REFERENCES "myCellarItems"("id") ON DELETE CASCADE, -- Reference to the cellar item
    "changeType" VARCHAR(50) NOT NULL, -- 'CREATED', 'QUANTITY_UPDATED', 'STATUS_CHANGED', 'CONSUMPTION_CHANGED', 'LOCATION_CHANGED', 'NOTES_UPDATED', 'FINANCIAL_UPDATED', 'PURCHASE_UPDATED', 'ARCHIVE_CHANGED', 'DELETED'
    "fieldName" VARCHAR(100), -- Specific field that changed (e.g., 'quantityVariantID', 'status', 'consumption', 'purchase_info')
    "oldValue" TEXT, -- Previous value (JSON string for complex data)
    "newValue" TEXT, -- New value (JSON string for complex data)
    "changeDescription" TEXT, -- Human-readable description of the change
    "quantityDelta" INTEGER DEFAULT NULL, -- For quantity changes: +5, -2, etc.
    "triggeredBy" VARCHAR(50) DEFAULT 'USER', -- 'USER', 'SYSTEM', 'IMPORT', 'API'
    "changeDate" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for changelog performance
CREATE INDEX idx_changelog_cellar_item ON "myCellarItemsChangelog" ("cellarItemID");
CREATE INDEX idx_changelog_change_type ON "myCellarItemsChangelog" ("changeType");
CREATE INDEX idx_changelog_date ON "myCellarItemsChangelog" ("changeDate");
CREATE INDEX idx_changelog_field ON "myCellarItemsChangelog" ("fieldName");

-- Composite index for common queries (item history by date)
CREATE INDEX idx_changelog_item_date ON "myCellarItemsChangelog" ("cellarItemID", "changeDate" DESC);

-- ========= OPTIONAL: Auto-update timestamps (can be handled in backend instead) =========
-- Uncomment these if you want automatic updatedDate handling at database level

-- CREATE OR REPLACE FUNCTION update_cellar_updated_date()
-- RETURNS TRIGGER AS $$
-- BEGIN
--     NEW."updatedDate" = CURRENT_TIMESTAMP;
--     RETURN NEW;
-- END;
-- $$ language 'plpgsql';

-- CREATE TRIGGER trigger_update_cellar_updated_date
--     BEFORE UPDATE ON "myCellarItems"
--     FOR EACH ROW
--     EXECUTE FUNCTION update_cellar_updated_date();

-- CREATE OR REPLACE FUNCTION update_cellar_collections_updated_date()
-- RETURNS TRIGGER AS $$
-- BEGIN
--     NEW."updatedDate" = CURRENT_TIMESTAMP;
--     RETURN NEW;
-- END;
-- $$ language 'plpgsql';

-- CREATE TRIGGER trigger_update_cellar_collections_updated_date
--     BEFORE UPDATE ON "myCellarCollections"
--     FOR EACH ROW
--     EXECUTE FUNCTION update_cellar_collections_updated_date();

-- ========= CHANGELOG TRIGGERS FOR myCellarItems (RECOMMENDED) =========
-- This provides bulletproof audit trail regardless of how data is modified

-- Function to log cellar item changes
CREATE OR REPLACE FUNCTION log_cellar_item_changes()
RETURNS TRIGGER AS $$
DECLARE
    change_desc TEXT;
    listing_name TEXT;
BEGIN
    -- Get listing name for better descriptions
    IF TG_OP = 'DELETE' THEN
        SELECT "listingName" INTO listing_name FROM "listings" WHERE "id" = OLD."listingID";
        listing_name := COALESCE(listing_name, 'Unknown item');
    ELSE
        SELECT "listingName" INTO listing_name FROM "listings" WHERE "id" = NEW."listingID";
        listing_name := COALESCE(listing_name, 'Unknown item');
    END IF;

    -- Handle INSERT (new item created)
    IF TG_OP = 'INSERT' THEN
        -- Determine initial status description
        change_desc := CASE NEW."status"
            WHEN 'Wishlisted' THEN 'Added to wishlist: ' || listing_name
            WHEN 'Purchased' THEN 'Purchased: ' || listing_name
            WHEN 'In Possession' THEN 'Added to cellar: ' || listing_name
            WHEN 'On Its Way' THEN 'Added as on its way: ' || listing_name
            WHEN 'Held Elsewhere' THEN 'Added as held elsewhere: ' || listing_name
            ELSE 'New cellar item added: ' || listing_name
        END;

        INSERT INTO "myCellarItemsChangelog" (
            "cellarItemID", "changeType", "changeDescription", 
            "newValue", "quantityDelta", "changeDate"
        ) VALUES (
            NEW."id", 'CREATED', change_desc,
            json_build_object(
                'quantityVariantID', NEW."quantityVariantID",
                'drinkFormat', NEW."drinkFormat",
                'status', NEW."status",
                'consumption', NEW."consumption",
                'currentLocation', NEW."currentLocation"
            )::text,
            1, -- Each record represents one bottle
            CURRENT_TIMESTAMP
        );
        RETURN NEW;
    END IF;

    -- Handle UPDATE (item modified)
    IF TG_OP = 'UPDATE' THEN
        -- Status changed - with detailed descriptions for important transitions
        IF OLD."status" != NEW."status" THEN
            change_desc := CASE 
                -- Consumption transitions
                WHEN OLD."status" != 'Consumed' AND NEW."status" = 'Consumed' THEN
                    'Bottle consumed: ' || listing_name || ' (was ' || OLD."status" || ')'
                -- Acquisition transitions  
                WHEN OLD."status" = 'Wishlisted' AND NEW."status" = 'Purchased' THEN
                    'Wishlist item purchased: ' || listing_name
                WHEN OLD."status" = 'Wishlisted' AND NEW."status" = 'In Possession' THEN
                    'Wishlist item acquired: ' || listing_name
                WHEN OLD."status" = 'Purchased' AND NEW."status" = 'In Possession' THEN
                    'Purchased item received: ' || listing_name
                WHEN OLD."status" = 'On Its Way' AND NEW."status" = 'In Possession' THEN
                    'Item delivered to cellar: ' || listing_name
                WHEN OLD."status" = 'Held Elsewhere' AND NEW."status" = 'In Possession' THEN
                    'Item moved to cellar: ' || listing_name
                -- Reverse consumption (restored from consumed)
                WHEN OLD."status" = 'Consumed' AND NEW."status" != 'Consumed' THEN
                    'Bottle status restored from consumed: ' || listing_name || ' (now ' || NEW."status" || ')'
                -- Generic status change
                ELSE 'Status changed: ' || listing_name || ' from "' || OLD."status" || '" to "' || NEW."status" || '"'
            END;
            
            INSERT INTO "myCellarItemsChangelog" (
                "cellarItemID", "changeType", "fieldName", "oldValue", "newValue",
                "changeDescription", "changeDate"
            ) VALUES (
                NEW."id", 'STATUS_CHANGED', 'status', 
                OLD."status", NEW."status", change_desc, CURRENT_TIMESTAMP
            );
        END IF;

        -- Consumption status changed - with detailed descriptions for important transitions
        IF OLD."consumption" != NEW."consumption" THEN
            change_desc := CASE 
                -- Opening bottle
                WHEN OLD."consumption" = 'Unopened' AND NEW."consumption" = 'Opened' THEN
                    'Bottle opened: ' || listing_name
                -- Emptying bottle
                WHEN OLD."consumption" != 'Empty' AND NEW."consumption" = 'Empty' THEN
                    'Bottle emptied: ' || listing_name || ' (was ' || OLD."consumption" || ')'
                -- Restoring from empty
                WHEN OLD."consumption" = 'Empty' AND NEW."consumption" != 'Empty' THEN
                    'Bottle consumption status restored: ' || listing_name || ' from Empty to ' || NEW."consumption"
                -- Closing bottle (opened -> unopened, unusual but possible)
                WHEN OLD."consumption" = 'Opened' AND NEW."consumption" = 'Unopened' THEN
                    'Bottle marked as unopened: ' || listing_name || ' (was opened)'
                -- Generic consumption change
                ELSE 'Consumption status changed: ' || listing_name || ' from "' || OLD."consumption" || '" to "' || NEW."consumption" || '"'
            END;
            
            INSERT INTO "myCellarItemsChangelog" (
                "cellarItemID", "changeType", "fieldName", "oldValue", "newValue",
                "changeDescription", "changeDate"
            ) VALUES (
                NEW."id", 'CONSUMPTION_CHANGED', 'consumption', 
                OLD."consumption", NEW."consumption", change_desc, CURRENT_TIMESTAMP
            );
        END IF;

        -- Location changed
        IF OLD."currentLocation" IS DISTINCT FROM NEW."currentLocation" OR 
           OLD."subLocation" IS DISTINCT FROM NEW."subLocation" THEN
            
            change_desc := 'Location changed: ' || listing_name || ' moved from "' || 
                          COALESCE(OLD."currentLocation", '(no location)') || 
                          CASE WHEN OLD."subLocation" IS NOT NULL THEN ' (' || OLD."subLocation" || ')' ELSE '' END ||
                          '" to "' || COALESCE(NEW."currentLocation", '(no location)') ||
                          CASE WHEN NEW."subLocation" IS NOT NULL THEN ' (' || NEW."subLocation" || ')' ELSE '' END || '"';
            
            INSERT INTO "myCellarItemsChangelog" (
                "cellarItemID", "changeType", "fieldName", "oldValue", "newValue",
                "changeDescription", "changeDate"
            ) VALUES (
                NEW."id", 'LOCATION_CHANGED', 'currentLocation', 
                json_build_object('currentLocation', OLD."currentLocation", 'subLocation', OLD."subLocation")::text,
                json_build_object('currentLocation', NEW."currentLocation", 'subLocation', NEW."subLocation")::text,
                change_desc, CURRENT_TIMESTAMP
            );
        END IF;

        -- Notes updated
        IF OLD."noteToSelf" IS DISTINCT FROM NEW."noteToSelf" OR
           OLD."suggestedFoodPairing" IS DISTINCT FROM NEW."suggestedFoodPairing" THEN
            
            change_desc := CASE
                WHEN OLD."noteToSelf" IS DISTINCT FROM NEW."noteToSelf" AND 
                     OLD."suggestedFoodPairing" IS DISTINCT FROM NEW."suggestedFoodPairing" THEN
                    'Notes and food pairing updated: ' || listing_name
                WHEN OLD."noteToSelf" IS DISTINCT FROM NEW."noteToSelf" THEN
                    'Personal notes updated: ' || listing_name
                ELSE 'Food pairing updated: ' || listing_name
            END;
            
            INSERT INTO "myCellarItemsChangelog" (
                "cellarItemID", "changeType", "fieldName", "oldValue", "newValue",
                "changeDescription", "changeDate"
            ) VALUES (
                NEW."id", 'NOTES_UPDATED', 'notes', 
                json_build_object('noteToSelf', OLD."noteToSelf", 'suggestedFoodPairing', OLD."suggestedFoodPairing")::text,
                json_build_object('noteToSelf', NEW."noteToSelf", 'suggestedFoodPairing', NEW."suggestedFoodPairing")::text,
                change_desc, CURRENT_TIMESTAMP
            );
        END IF;

        -- Archive status changed
        IF OLD."archiveStatus" != NEW."archiveStatus" THEN
            change_desc := CASE 
                WHEN NEW."archiveStatus" = TRUE THEN 
                    CASE 
                        -- Check if collection was also set to NULL (indicates collection deletion)
                        WHEN OLD."collectionID" IS NOT NULL AND NEW."collectionID" IS NULL THEN
                            'Bottle archived due to collection deletion: ' || listing_name
                        ELSE 
                            'Bottle archived: ' || listing_name
                    END
                ELSE 'Bottle restored from archive: ' || listing_name
            END;
            
            INSERT INTO "myCellarItemsChangelog" (
                "cellarItemID", "changeType", "fieldName", "oldValue", "newValue",
                "changeDescription", "changeDate"
            ) VALUES (
                NEW."id", 'ARCHIVE_CHANGED', 'archiveStatus', 
                OLD."archiveStatus"::text, NEW."archiveStatus"::text, change_desc, CURRENT_TIMESTAMP
            );
        END IF;

        -- Financial information updated
        IF OLD."purchasePrice" IS DISTINCT FROM NEW."purchasePrice" OR
           OLD."currentValueEstimation" IS DISTINCT FROM NEW."currentValueEstimation" OR
           OLD."purchaseCurrency" IS DISTINCT FROM NEW."purchaseCurrency" OR
           OLD."currentValueCurrency" IS DISTINCT FROM NEW."currentValueCurrency" THEN
            
            change_desc := 'Financial information updated: ' || listing_name;
            
            INSERT INTO "myCellarItemsChangelog" (
                "cellarItemID", "changeType", "fieldName", "oldValue", "newValue",
                "changeDescription", "changeDate"
            ) VALUES (
                NEW."id", 'FINANCIAL_UPDATED', 'financial', 
                json_build_object(
                    'purchasePrice', OLD."purchasePrice", 
                    'purchaseCurrency', OLD."purchaseCurrency",
                    'currentValueEstimation', OLD."currentValueEstimation",
                    'currentValueCurrency', OLD."currentValueCurrency"
                )::text,
                json_build_object(
                    'purchasePrice', NEW."purchasePrice", 
                    'purchaseCurrency', NEW."purchaseCurrency",
                    'currentValueEstimation', NEW."currentValueEstimation",
                    'currentValueCurrency', NEW."currentValueCurrency"
                )::text,
                change_desc, CURRENT_TIMESTAMP
            );
        END IF;

        -- Purchase information updated (dates, location)
        IF OLD."purchaseDate" IS DISTINCT FROM NEW."purchaseDate" OR
           OLD."deliveryDate" IS DISTINCT FROM NEW."deliveryDate" OR
           OLD."purchasePlaceName" IS DISTINCT FROM NEW."purchasePlaceName" OR
           OLD."purchaseAddress" IS DISTINCT FROM NEW."purchaseAddress" THEN
            
            change_desc := 'Purchase information updated: ' || listing_name;
            
            INSERT INTO "myCellarItemsChangelog" (
                "cellarItemID", "changeType", "fieldName", "oldValue", "newValue",
                "changeDescription", "changeDate"
            ) VALUES (
                NEW."id", 'PURCHASE_UPDATED', 'purchase_info', 
                json_build_object(
                    'purchaseDate', OLD."purchaseDate",
                    'deliveryDate', OLD."deliveryDate",
                    'purchasePlaceName', OLD."purchasePlaceName",
                    'purchaseAddress', OLD."purchaseAddress"
                )::text,
                json_build_object(
                    'purchaseDate', NEW."purchaseDate",
                    'deliveryDate', NEW."deliveryDate",
                    'purchasePlaceName', NEW."purchasePlaceName",
                    'purchaseAddress', NEW."purchaseAddress"
                )::text,
                change_desc, CURRENT_TIMESTAMP
            );
        END IF;

        RETURN NEW;
    END IF;

    -- Handle DELETE (item removed)
    -- Note: With new archival system, direct deletions should be rare
    -- Items are typically archived instead of deleted when collections are removed
    IF TG_OP = 'DELETE' THEN
        change_desc := 'Cellar item removed: ' || listing_name || 
                      ' (was ' || OLD."status" || ', ' || OLD."consumption" || ')';
        
        -- Try to insert changelog entry, but handle constraint violations gracefully
        BEGIN
            INSERT INTO "myCellarItemsChangelog" (
                "cellarItemID", "changeType", "changeDescription", 
                "oldValue", "changeDate"
            ) VALUES (
                OLD."id", 'DELETED', change_desc,
                json_build_object(
                    'quantityVariantID', OLD."quantityVariantID",
                    'status', OLD."status",
                    'consumption', OLD."consumption",
                    'currentLocation', OLD."currentLocation"
                )::text,
                CURRENT_TIMESTAMP
            );
        EXCEPTION 
            WHEN foreign_key_violation THEN
                -- If FK constraint fails, log to system instead
                RAISE NOTICE 'Could not log deletion of item % to changelog due to FK constraint', OLD."id";
        END;
        
        RETURN OLD;
    END IF;

    RETURN NULL;
END;
$$ language 'plpgsql';

-- Create the trigger
CREATE TRIGGER trigger_log_cellar_item_changes
    AFTER INSERT OR UPDATE OR DELETE ON "myCellarItems"
    FOR EACH ROW
    EXECUTE FUNCTION log_cellar_item_changes();

-- ========= COLLECTION DELETION ARCHIVAL TRIGGER =========
-- Function to archive cellar items when their collection is deleted
CREATE OR REPLACE FUNCTION archive_items_on_collection_delete()
RETURNS TRIGGER AS $$
DECLARE
    archived_count INTEGER := 0;
    item_record RECORD;
BEGIN
    -- Update items that belonged to the deleted collection
    -- Set collectionID to NULL and archiveStatus to TRUE
    FOR item_record IN 
        SELECT "id", "listingID" 
        FROM "myCellarItems" 
        WHERE "collectionID" = OLD."id" AND "archiveStatus" = FALSE
    LOOP
        UPDATE "myCellarItems" 
        SET 
            "collectionID" = NULL,
            "archiveStatus" = TRUE,
            "updatedDate" = CURRENT_TIMESTAMP
        WHERE "id" = item_record."id";
        
        archived_count := archived_count + 1;
        
        -- Log the archival in the changelog
        INSERT INTO "myCellarItemsChangelog" (
            "cellarItemID", "changeType", "changeDescription", 
            "oldValue", "newValue", "changeDate"
        ) VALUES (
            item_record."id", 
            'COLLECTION_DELETED', 
            'Item archived due to collection deletion: ' || OLD."collectionName",
            OLD."id"::text,
            'NULL',
            CURRENT_TIMESTAMP
        );
    END LOOP;
    
    -- Log the collection deletion summary
    IF archived_count > 0 THEN
        RAISE NOTICE 'Collection % deleted: % items archived', OLD."collectionName", archived_count;
    END IF;
    
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- Create trigger for collection deletion
CREATE TRIGGER trigger_archive_items_on_collection_delete
    BEFORE DELETE ON "myCellarCollections"
    FOR EACH ROW
    EXECUTE FUNCTION archive_items_on_collection_delete();

-- NEWLY ADDED TABLES for Explore Page - BY CP --

-- ========= "listingsLikes" =========
CREATE TABLE "listingsLikes" (
    "id" SERIAL PRIMARY KEY,
    "userId" INTEGER,
    "userType" VARCHAR(50), -- e.g., 'producer', 'venue', 'user'
    "listingId" INTEGER REFERENCES "listings"("id") ON DELETE CASCADE,
    "createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -- ========= "88BContentLikes" =========
-- CREATE TABLE "88BContentLikes" (
--     "id" SERIAL PRIMARY KEY,
--     "userId" INTEGER,
--     "userType" VARCHAR(50), -- e.g., 'producer', 'venue', 'user'
--     "contentId" INTEGER REFERENCES "88BContent"("id") ON DELETE CASCADE,
--     "createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );

-- ========= "listingsComments" =========
CREATE TABLE "listingsComments" (
    "id" SERIAL PRIMARY KEY,
    "userId" INTEGER,
    "userType" VARCHAR(50), -- e.g., 'producer', 'venue', 'user'
    "listingId" INTEGER REFERENCES "listings"("id") ON DELETE CASCADE,
    "parentId" INTEGER REFERENCES "listingsComments"("id") ON DELETE CASCADE,
    "comment" TEXT NOT NULL,
    "createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ========= "listingReviewsComments" =========
CREATE TABLE "listingReviewsComments" (
    "id" SERIAL PRIMARY KEY,
    "userId" INTEGER,
    "userType" VARCHAR(50), -- e.g., 'producer', 'venue', 'user'
    "reviewId" INTEGER REFERENCES "reviews"("id") ON DELETE CASCADE,
    "parentId" INTEGER REFERENCES "listingReviewsComments"("id") ON DELETE CASCADE,
    "comment" TEXT NOT NULL,
    "createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ========= "producerReviewsComments" =========
CREATE TABLE "producerReviewsComments" (
    "id" SERIAL PRIMARY KEY,
    "userId" INTEGER,
    "userType" VARCHAR(50), -- e.g., 'producer', 'venue', 'user'
    "reviewId" INTEGER REFERENCES "producerReviews"("id") ON DELETE CASCADE,
    "parentId" INTEGER REFERENCES "producerReviewsComments"("id") ON DELETE CASCADE,
    "comment" TEXT NOT NULL,
    "createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ========= "venueReviewsComments" ===========
CREATE TABLE "venueReviewsComments" (
    "id" SERIAL PRIMARY KEY,
    "userId" INTEGER,
    "userType" VARCHAR(50), -- e.g., 'producer', 'venue', 'user'
    "reviewId" INTEGER REFERENCES "venueReviews"("id") ON DELETE CASCADE,
    "parentId" INTEGER REFERENCES "venueReviewsComments"("id") ON DELETE CASCADE,
    "comment" TEXT NOT NULL,
    "createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ========= "producerUpdateComments" =========
CREATE TABLE "producerUpdateComments" (
    "id" SERIAL PRIMARY KEY,
    "userId" INTEGER,
    "userType" VARCHAR(50), -- e.g., 'producer', 'venue', 'user'
    "producerUpdateId" INTEGER REFERENCES "producersUpdates"("id") ON DELETE CASCADE,
    "parentId" INTEGER REFERENCES "producerUpdateComments"("id") ON DELETE CASCADE,
    "comment" TEXT NOT NULL,
    "createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ========= "venueUpdateComments" =========
CREATE TABLE "venueUpdateComments" (
    "id" SERIAL PRIMARY KEY,
    "userId" INTEGER,
    "userType" VARCHAR(50), -- e.g., 'producer', 'venue', 'user'
    "venueUpdateId" INTEGER REFERENCES "venuesUpdates"("id") ON DELETE CASCADE,
    "parentId" INTEGER REFERENCES "venueUpdateComments"("id") ON DELETE CASCADE,
    "comment" TEXT NOT NULL,
    "createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -- ========= "88BContentComments" =========
-- CREATE TABLE "88BContentComments" (
--     "id" SERIAL PRIMARY KEY,
--     "userId" INTEGER,
--     "userType" VARCHAR(50), -- e.g., 'producer', 'venue', 'user'
--     "contentId" INTEGER REFERENCES "88BContent"("id") ON DELETE CASCADE,
--     "parentId" INTEGER REFERENCES "88BContentComments"("id") ON DELETE CASCADE,
--     "comment" TEXT NOT NULL,
--     "createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );

-- ========= "userFestivalTastedList" =========  if record exists = checked/tasted
CREATE TABLE "userFestivalTastedList" (
    "id" SERIAL PRIMARY KEY,
    "userId" INTEGER REFERENCES "users"("id") ON DELETE CASCADE,
    "venueId" INTEGER REFERENCES "venues"("id") ON DELETE SET NULL,
    "itemID" INTEGER REFERENCES "listings"("id") ON DELETE CASCADE,
    "variant" SMALLINT DEFAULT NULL, -- will copy the menuItems variant value- to keep track of vintage of drink tasted
    "tastedDate" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "notes" TEXT DEFAULT '',
    UNIQUE ("userId", "venueId", "itemID", "variant") -- Prevent duplicate tastings for same user/venue/item/variant combination
);

-- ========= POLLING FEATURE TABLES =========

-- ========= "pollQuestions" for creator to determine each question =========
CREATE TABLE "pollQuestions" (
    "id" SERIAL PRIMARY KEY,
    "creatorId" INTEGER NOT NULL, -- The actual ID of the creator
    "creatorType" VARCHAR(20) NOT NULL CHECK ("creatorType" IN ('user', 'venue', 'producer')), -- Type of creator
    "title" VARCHAR(255) NOT NULL,
    "questionText" TEXT NOT NULL,
    "questionType" VARCHAR(50) NOT NULL CHECK ("questionType" IN ('multiple_choice_single_selection', 'multiple_choice_multi_selection', 'rating_scale')),
    "isActive" BOOLEAN DEFAULT TRUE, -- whether poll is active (accepting responses) or closed (not accepting new responses) 
    "isVisible" BOOLEAN DEFAULT TRUE, -- Whether poll is visible (if isActive is true, it's accepting responses and you can see responses and if isActive is false, you can just see the responses) or hidden (whether isActive is true or false, the public cannot see the poll)
    "expiresAt" TIMESTAMP DEFAULT NULL, -- Optional expiration date after which poll will not acccept  responses anymore
    "createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "orderIndex" INTEGER NOT NULL, -- Order of questions for the same creator (ie with the same creatorId and creatorType),
    UNIQUE ("creatorId", "creatorType", "orderIndex") -- Ensure unique ordering within each creator
);


-- ========= "pollOptions" for creator to determine - only relevant for multiple_choice_single_selection and multiple_choice_multi_selection =========
CREATE TABLE "pollOptions" (
    "id" SERIAL PRIMARY KEY,
    "pollId" INTEGER REFERENCES "pollQuestions"("id") ON DELETE CASCADE, -- The poll this option belongs to, foreign key referencing row in "pollQuestions"
    "optionText" VARCHAR(500) NOT NULL,
    "optionOrder" INTEGER NOT NULL, -- Order of options within the question
    UNIQUE ("pollId", "optionOrder") -- Ensure unique ordering within each poll
);

-- ========= "pollResponses" for respondents to select =========
CREATE TABLE "pollResponses" (
    "id" SERIAL PRIMARY KEY,
    "pollId" INTEGER REFERENCES "pollQuestions"("id") ON DELETE CASCADE,-- The poll this response belongs to, foreign key referencing row in "pollQuestions"
    "respondentId" INTEGER REFERENCES "users"("id") ON DELETE CASCADE, -- only ordinary users are allowed to participate in polls
    "selectedOptionIds" INTEGER[] DEFAULT NULL, -- Array of selected option IDs in pollOptions (only relevant for multiple_choice_single_selection and multiple_choice_multi_selection questions)
    "ratingValue" INTEGER DEFAULT NULL, -- For rating_scale questions from 1 to 5 (only relevant for rating_scale questions)
    CONSTRAINT check_response_data CHECK (
        ("selectedOptionIds" IS NOT NULL AND "ratingValue" IS NULL) OR
        ("selectedOptionIds" IS NULL AND "ratingValue" IS NOT NULL)
    ),
    UNIQUE ("pollId", "respondentId") -- Ensure each user can only have one response per poll
);

-- ========= POLLING FEATURE TRIGGERS =========

-- Function to automatically deactivate expired polls
CREATE OR REPLACE FUNCTION deactivate_expired_polls()
RETURNS TRIGGER AS $$
BEGIN
    -- Check if poll has expired and is still active
    IF NEW."expiresAt" IS NOT NULL AND 
       NEW."expiresAt" <= CURRENT_TIMESTAMP AND 
       NEW."isActive" = TRUE THEN
        NEW."isActive" = FALSE;
        NEW."updatedAt" = CURRENT_TIMESTAMP;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger to automatically deactivate expired polls on UPDATE
CREATE TRIGGER trigger_deactivate_expired_polls
    BEFORE UPDATE ON "pollQuestions"
    FOR EACH ROW
    EXECUTE FUNCTION deactivate_expired_polls();

-- Create indexes for better performance
CREATE INDEX idx_poll_questions_creator ON "pollQuestions" ("creatorId", "creatorType");
CREATE INDEX idx_poll_questions_active_visible ON "pollQuestions" ("isActive", "isVisible");
CREATE INDEX idx_poll_questions_expires_at ON "pollQuestions" ("expiresAt") WHERE "expiresAt" IS NOT NULL;
CREATE INDEX idx_poll_questions_created_at ON "pollQuestions" ("createdAt");
CREATE INDEX idx_poll_options_poll_order ON "pollOptions" ("pollId", "optionOrder");
CREATE INDEX idx_poll_responses_poll ON "pollResponses" ("pollId");
CREATE INDEX idx_poll_responses_user ON "pollResponses" ("respondentId");

-- ========= EVENT_FESTIVAL FEATURE: Add eventID column to venues =========
-- Add eventID foreign key to venues table after events table exists
ALTER TABLE "venues" 
ADD COLUMN "eventID" INTEGER REFERENCES "events"("id") ON DELETE SET NULL;

-- ========= INDEXES FOR EVENT_FESTIVAL FEATURE =========
-- Index for performance when filtering events by location and date
CREATE INDEX idx_events_location_dates 
ON "events"("eventLocation", "eventStartDate", "eventEndDate") 
WHERE "eventOwnerType" = 'venue';

-- Index for venue-event relationship lookups
CREATE INDEX idx_venues_event_id 
ON "venues"("eventID") 
WHERE "specialStatus" = 'EVENT_FESTIVAL';

-- Compound index for the main upcoming events query (location + dates + signup status)
CREATE INDEX idx_events_upcoming_query 
ON "events"("eventLocation", "eventStartDate", "eventEndDate", "signupOpen");

