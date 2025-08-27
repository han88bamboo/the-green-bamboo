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
DROP TABLE IF EXISTS "specialColours" CASCADE;
DROP TABLE IF EXISTS "subTags" CASCADE;
DROP TABLE IF EXISTS "tokens" CASCADE;
DROP TABLE IF EXISTS "users" CASCADE;
DROP TABLE IF EXISTS "usersDrinkLists" CASCADE;
DROP TABLE IF EXISTS "usersDrinkListItems" CASCADE;
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
    "pdfMenuUrl" TEXT DEFAULT NULL
);

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
    -- Custom amenities
    "otherAmenities" TEXT,
    "createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
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
    "categoryExpert" VARCHAR(255) DEFAULT NULL -- Category expert designation (e.g., "Champagne Expert", "Whisky Expert", etc.)
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
    "drinkStyle" VARCHAR(255) -- added by tzh
);

-- create index 
-- CREATE INDEX idx_listings_search_vector 
-- ON "listings" USING GIN("searchVector");
-- Create a GIN index on listingName for trigram fuzzy search
CREATE INDEX idx_listings_name_trgm ON "listings" USING gin ("listingName" gin_trgm_ops);

-- Create index for producer-aware randomized sorting
CREATE INDEX idx_listings_producer_random_sort ON "listings" (ABS(HASHTEXT("id"::text || '-' || "producerID"::text)));

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
    "venues" TEXT[] -- Contains "venues"("id")s
);

-- ========= "usersDrinkLists" =========
CREATE TABLE "usersDrinkLists" (
    "id" SERIAL PRIMARY KEY,
    "userId" INTEGER REFERENCES "users"("id") ON DELETE SET NULL,  -- [!] reference "users" FK
    "listName" TEXT,
    "listDesc" TEXT,
    -- "drinks" TEXT[],-- Contains "listings"("id")s
    UNIQUE ("userId", "listName")
);

-- ========= "usersDrinkListItems" =========
CREATE TABLE "usersDrinkListItems" (
    "id" SERIAL PRIMARY KEY,
    "listId" INTEGER REFERENCES "usersDrinkLists"("id") ON DELETE CASCADE, -- [!] reference "usersDrinkLists" FK
    "drinkId" INTEGER REFERENCES "listings"("id") ON DELETE CASCADE,
    "addedDate" TIMESTAMP,
    UNIQUE ("listId", "drinkId")
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
    "observationTag" TEXT[], -- Contains "observationTags"("id")s
    "address" VARCHAR(255),
    "variant" SMALLINT DEFAULT NULL -- 2 bytes per row, Handles years from -32,768 to 32,767
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

-- ========= "venuesMenu" =========
CREATE TABLE "venuesMenu" (
    "id" SERIAL PRIMARY KEY,
    "sectionName" VARCHAR(255),
    "sectionOrder" VARCHAR(255),
    -- "sectionMenu" TEXT[], -- [!] Contains listings(id)
    "venueId" INTEGER REFERENCES "venues"("id") ON DELETE SET NULL -- [!] References venues FK
);

-- ========= "menuItems" =========
CREATE TABLE "menuItems" (
    "id" SERIAL PRIMARY KEY,
    "itemOrder" INTEGER,
    "itemPrice" DECIMAL(10,2),
    "itemAvailability" BOOLEAN,
    "itemID" INTEGER REFERENCES "listings"("id") ON DELETE SET NULL,
    "itemServingType" INTEGER REFERENCES "servingTypes"("id") ON DELETE SET NULL,
    "sectionId" INTEGER REFERENCES "venuesMenu"("id") ON DELETE CASCADE,
    "variant" SMALLINT DEFAULT NULL -- 2 bytes per row, Handles years from -32,768 to 32,767
);
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
    "venueID" INTEGER REFERENCES "venues"("id") ON DELETE SET NULL  -- added by tzh
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
    "createdDate" TIMESTAMP
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
    "rsvpTimestamp" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
    "counter" INTEGER
);

-- ========= "upAndComing" ==========
CREATE TABLE "upAndComing" (
    "id" SERIAL PRIMARY KEY,
    "listingName" VARCHAR(255),
    "listingID" INTEGER REFERENCES "listings"("id") ON DELETE SET NULL, -- [!] References listings FK
    "drinkType" VARCHAR(255),
    "typeCategory" VARCHAR(255),
    "counter" INTEGER
);

-- ========= "goats" ==========
CREATE TABLE "goats" (
    "id" SERIAL PRIMARY KEY,
    "listingName" VARCHAR(255),
    "listingID" INTEGER REFERENCES "listings"("id") ON DELETE SET NULL, -- [!] References listings FK
    "drinkType" VARCHAR(255),
    "typeCategory" VARCHAR(255),
    "counter" INTEGER
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

-- NEWLY ADDED TABLES for Explore Page - BY CP --

-- ========= "listingsLikes" =========
CREATE TABLE "listingsLikes" (
    "id" SERIAL PRIMARY KEY,
    "userId" INTEGER REFERENCES "users"("id") ON DELETE CASCADE,
    "userType" VARCHAR(50), -- e.g., 'producer', 'venue', 'user'
    "listingId" INTEGER REFERENCES "listings"("id") ON DELETE CASCADE,
    "createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ========= "88BContentLikes" =========
CREATE TABLE "88BContentLikes" (
    "id" SERIAL PRIMARY KEY,
    "userId" INTEGER REFERENCES "users"("id") ON DELETE CASCADE,
    "userType" VARCHAR(50), -- e.g., 'producer', 'venue', 'user'
    "contentId" INTEGER REFERENCES "88BContent"("id") ON DELETE CASCADE,
    "createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ========= "listingsComments" =========
CREATE TABLE "listingsComments" (
    "id" SERIAL PRIMARY KEY,
    "userId" INTEGER REFERENCES "users"("id") ON DELETE CASCADE,
    "userType" VARCHAR(50), -- e.g., 'producer', 'venue', 'user'
    "listingId" INTEGER REFERENCES "listings"("id") ON DELETE CASCADE,
    "parentId" INTEGER REFERENCES "listingsComments"("id") ON DELETE CASCADE,
    "comment" TEXT NOT NULL,
    "createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ========= "listingReviewsComments" =========
CREATE TABLE "listingReviewsComments" (
    "id" SERIAL PRIMARY KEY,
    "userId" INTEGER REFERENCES "users"("id") ON DELETE CASCADE,
    "userType" VARCHAR(50), -- e.g., 'producer', 'venue', 'user'
    "reviewId" INTEGER REFERENCES "reviews"("id") ON DELETE CASCADE,
    "parentId" INTEGER REFERENCES "listingReviewsComments"("id") ON DELETE CASCADE,
    "comment" TEXT NOT NULL,
    "createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ========= "producerUpdateComments" =========
CREATE TABLE "producerUpdateComments" (
    "id" SERIAL PRIMARY KEY,
    "userId" INTEGER REFERENCES "users"("id") ON DELETE CASCADE,
    "userType" VARCHAR(50), -- e.g., 'producer', 'venue', 'user'
    "producerUpdateId" INTEGER REFERENCES "producerUpdate"("id") ON DELETE CASCADE,
    "parentId" INTEGER REFERENCES "producerUpdateComments"("id") ON DELETE CASCADE,
    "comment" TEXT NOT NULL,
    "createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ========= "venueUpdateComments" =========
CREATE TABLE "venueUpdateComments" (
    "id" SERIAL PRIMARY KEY,
    "userId" INTEGER REFERENCES "users"("id") ON DELETE CASCADE,
    "userType" VARCHAR(50), -- e.g., 'producer', 'venue', 'user'
    "venueUpdateId" INTEGER REFERENCES "venueUpdate"("id") ON DELETE CASCADE,
    "parentId" INTEGER REFERENCES "venueUpdateComments"("id") ON DELETE CASCADE,
    "comment" TEXT NOT NULL,
    "createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ========= "88BContentComments" =========
CREATE TABLE "88BContentComments" (
    "id" SERIAL PRIMARY KEY,
    "userId" INTEGER REFERENCES "users"("id") ON DELETE CASCADE,
    "userType" VARCHAR(50), -- e.g., 'producer', 'venue', 'user'
    "contentId" INTEGER REFERENCES "88BContent"("id") ON DELETE CASCADE,
    "parentId" INTEGER REFERENCES "88BContentComments"("id") ON DELETE CASCADE,
    "comment" TEXT NOT NULL,
    "createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);