-- DROP TABLES IF EXISTS -- 
DROP TABLE IF EXISTS "accountRequests";
DROP TABLE IF EXISTS "badges";
DROP TABLE IF EXISTS "colours";
DROP TABLE IF EXISTS "countries";
DROP TABLE IF EXISTS "drinkTypes";
DROP TABLE IF EXISTS "flavourTags";
DROP TABLE IF EXISTS "languages";
DROP TABLE IF EXISTS "listings";
DROP TABLE IF EXISTS "modRequests";
DROP TABLE IF EXISTS "observationTags";
DROP TABLE IF EXISTS "producers";
DROP TABLE IF EXISTS "producersQuestionAnswers";
DROP TABLE IF EXISTS "producersUpdates";
DROP TABLE IF EXISTS "producersProfileViews";
DROP TABLE IF EXISTS "producersProfileViewsViews";
DROP TABLE IF EXISTS "requestEdits";
DROP TABLE IF EXISTS "requestInaccuracy";
DROP TABLE IF EXISTS "requestListings";
DROP TABLE IF EXISTS "reviews";
DROP TABLE IF EXISTS "reviewsUserVotes";
DROP TABLE IF EXISTS "servingTypes";
DROP TABLE IF EXISTS "specialColours";
DROP TABLE IF EXISTS "subTags";
DROP TABLE IF EXISTS "tokens";
DROP TABLE IF EXISTS "users";
DROP TABLE IF EXISTS "usersDrinkLists";
DROP TABLE IF EXISTS "usersfollowLists";
DROP TABLE IF EXISTS "venues";
DROP TABLE IF EXISTS "venuesMenu";
DROP TABLE IF EXISTS "venuesOpeningHours";
DROP TABLE IF EXISTS "venuesQuestionAnswers";
DROP TABLE IF EXISTS "venuesUpdates";
DROP TABLE IF EXISTS "venuesProfileViews";
DROP TABLE IF EXISTS "venuesProfileViewsViews";

-- CREATE TABLES -- 
-- ========= "accountRequests" =========
CREATE TABLE "accountRequests" (
    "id" SERIAL PRIMARY KEY,
    "businessName" VARCHAR(255),
    "businessType" VARCHAR(255),
    "businessDesc" TEXT,
    "country" VARCHAR(255),
    "pricing" VARCHAR(255),
    "businessLink" VARCHAR(255),
    "firstName" VARCHAR(255),
    "lastName" VARCHAR(255),
    "relationship" VARCHAR(255),
    "email" VARCHAR(255),
    "contact" VARCHAR(255),
    "referenceDocument" VARCHAR(255),
    "photo" TEXT,
    "joinDate" TIMESTAMP,
    "isPending" BOOLEAN,
    "isApproved" BOOLEAN
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
    "subTag" VARCHAR(255)
);

-- ========= "badges" =========
CREATE TABLE "badges" (
    "id" SERIAL PRIMARY KEY,
    "badgeName" VARCHAR(255),
    "badgePhoto" TEXT,
    "badgeDesc" TEXT
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
    "mainDrinks" TEXT[],
    "photo" TEXT,
    "hashedPassword" VARCHAR(255),
    "claimStatus" BOOLEAN,
    "statusOB" VARCHAR(255),
    -- "questionAnswers" INTEGER REFERENCES "producersQuestionAnswers"("id") ON DELETE SET NULL, -- Alternative ON DELETE CASCADE to delete all related child records[!] reference "producersQuestionAnswers" as FK
    -- "updates" INTEGER REFERENCES "producersUpdates"("id") ON DELETE SET NULL, -- Alternative ON DELETE CASCADE to delete all related child records[!] reference "producersUpdates" as FK
    "username" VARCHAR(255),
    "producerLink" VARCHAR(255),
    "stripeCustomerId" VARCHAR(255)
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
    -- "openingHours" SERIAL, -- [!] reference "venuesOpeningHours"
    -- "questionAnswers" SERIAL, -- [!] reference "venuesQuestionAnswers"
    -- "updates" SERIAL, -- [!] reference "venuesUpdates"
    "reservationDetails" VARCHAR(255),
    "username" VARCHAR(255),
    "publicHolidays" VARCHAR(255),
    "stripeCustomerId" VARCHAR(255),
    "pin" VARCHAR(255)
);

-- ========= "users" =========
CREATE TABLE "users" (
    "id" SERIAL PRIMARY KEY,
    "username" VARCHAR(255),
    "displayName" VARCHAR(255),
    "choiceDrinks" TEXT[],
    "modType" TEXT[],
    "photo" TEXT,
    "hashedPassword" VARCHAR(255),
    -- "drinkLists" SERIAL, -- [!] reference "usersDrinkLists" not needed since user followlist ref users
    "joinDate" TIMESTAMP,
    -- "followLists" SERIAL, -- [!] reference "usersFollowLists"
    "firstName" VARCHAR(255),
    "lastName" VARCHAR(255),
    "email" VARCHAR(255),
    "isAdmin" BOOLEAN,
    "birthday" TIMESTAMP,
    "pin" VARCHAR(255)
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

-- ========= "producersProfileViews" =========
CREATE TABLE "producersProfileViews" (
    "id" SERIAL PRIMARY KEY,
    "date" TIMESTAMP, 
    "count" INTEGER, -- do i need this?
    "producerId" INTEGER REFERENCES "producers"("id") ON DELETE SET NULL -- [!] reference "producers" FK
    -- "views" INTEGER REFERENCES "producersProfileViewsViews"("id") ON DELETE SET NULL  -- [!] reference "producersProfileViewsViews" FK
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
    "listingName" VARCHAR(255),
    "producerID" INTEGER REFERENCES "producers"("id") ON DELETE SET NULL, -- [!] reference "producers" FK
    "bottler" VARCHAR(255),
    "originCountry" VARCHAR(255),
    "drinkType" VARCHAR(255),
    "abv" FLOAT,
    "officialDesc" TEXT,
    "allowMod" BOOLEAN,
    "addedDate" TIMESTAMP,
    "typeCategory" VARCHAR(255),
    "age" VARCHAR(255),
    "reviewLink" VARCHAR(255),
    "sourceLink" VARCHAR(255),
    "photo" TEXT 
);

-- ========= "modRequests" =========
CREATE TABLE "modRequests" (
    "id" SERIAL PRIMARY KEY,
    "userID" INTEGER REFERENCES "users"("id") ON DELETE SET NULL,
    "drinkType" VARCHAR(255),
    "modDesc" TEXT,
    "reviewStatus" BOOLEAN
);

-- ========= [NEW!] "usersFollowLists" =========
CREATE TABLE "usersFollowLists" (
    "id" SERIAL PRIMARY KEY, 
    "userId" INTEGER REFERENCES "users"("id") ON DELETE SET NULL, -- [!] reference "users"("id")
    "users" TEXT[], -- Contains "users"("id")s
    "producers" TEXT[], -- Contains "producers"("id")s
    "venues" TEXT[] -- Contains "venues"("id")s
);

-- ========= [NEW!] "usersDrinkLists" =========
CREATE TABLE "usersDrinkLists" (
    "id" SERIAL PRIMARY KEY,
    "userId" INTEGER REFERENCES "users"("id") ON DELETE SET NULL,  -- [!] reference "users" FK
    "drinksIHaveTried" TEXT[], -- Contains "listings"("id")s
    "drinksIWantToTry" TEXT[] -- Contains "listings"("id")s
);

-- ========= "reviews" =========
CREATE TABLE "reviews" (
    "id" SERIAL PRIMARY KEY,
    "userID" INTEGER REFERENCES "users"("id") ON DELETE SET NULL, -- [!] reference "users"("id")
    "reviewTarget" INTEGER REFERENCES "listings"("id") ON DELETE SET NULL, -- [!] reference "listings"("id")
    "rating" INT,
    "reviewDesc" TEXT,
    "reviewType" VARCHAR(255),
    "createdDate" TIMESTAMP,
    "language" VARCHAR(255),
    "finish" VARCHAR(255),
    "willRecommend" BOOLEAN,
    "wouldBuyAgain" BOOLEAN,
    -- "userVotes" SERIAL, -- [!] reference "reviewsUserVotes" FK
    "taggedUsers" TEXT[], -- Contains "users"("id")s
    "flavourTag" TEXT[], -- Contains "flavourTags"("id")s
    "photo" TEXT,
    "colour" VARCHAR(7),
    "aroma" VARCHAR(255),
    "location" INTEGER REFERENCES "venues"("id") ON DELETE SET NULL, -- [!] references "venues" FK
    "taste" VARCHAR(255),
    "observationTag" TEXT[], -- Contains "observationTags"("id")s
    "address" VARCHAR(255)
);

-- ========= [NEW!] "reviewsUserVotes" =========
CREATE TABLE "reviewsUserVotes" (
    "id" SERIAL PRIMARY KEY,
    "upvotes" TEXT[], -- Contain "users"("id")s
    "downvotes" TEXT[], -- Contain "users"("id")s
    "reviewId" INTEGER REFERENCES "reviews"("id") on DELETE SET NULL -- [!] reference "reviews" FK
);

-- ========= "tokens" =========
CREATE TABLE "tokens" (
    "id" SERIAL PRIMARY KEY,
    "token" VARCHAR(255),
    "userId" INTEGER REFERENCES "users"("id") ON DELETE SET NULL, -- [!] reference "users" FK
    "requestId" INTEGER REFERENCES "accountRequests"("id") ON DELETE SET NULL, -- [!] reference "accountRequests" FK
    "expiry" TIMESTAMP
);

-- ========= [NEW!] "venuesMenu" =========
CREATE TABLE "venuesMenu" (
    "id" SERIAL PRIMARY KEY,
    "sectionName" VARCHAR(255),
    "sectionOrder" VARCHAR(255),
    "sectionMenu" TEXT[], -- [!] Contains listings(id)
    "venueId" INTEGER REFERENCES "venues"("id") ON DELETE SET NULL -- [!] References venues FK
);

-- ========= [NEW!] "venuesOpeningHours" =========
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

-- ========= [NEW!] "venuesQuestionAnswers" =========
CREATE TABLE "venuesQuestionAnswers" (
    "id" SERIAL PRIMARY KEY,
    "question" VARCHAR(255),
    "answer" VARCHAR(255),
    "date" TIMESTAMP,
    "userId" INTEGER REFERENCES "users"("id") ON DELETE SET NULL,
    "venueId" INTEGER REFERENCES "venues"("id") ON DELETE SET NULL -- [!] References venues FK
);

-- ========= [NEW!] "venuesUpdates" =========
CREATE TABLE "venuesUpdates" (
    "id" SERIAL PRIMARY KEY,
    "date" TIMESTAMP,
    "text" VARCHAR(255),
    "photo" TEXT,
    "venueId" INTEGER REFERENCES "venues"("id") ON DELETE SET NULL -- [!] References venues FK
    -- need add likes?
);

-- -- ========= [NEW!] "venuesProfileViewsViews" =========
-- CREATE TABLE "venuesProfileViewsViews" (
--     "id" SERIAL PRIMARY KEY,
--     "date" TIMESTAMP,
--     "count" INT
-- );

-- ========= [NEW!] "venuesProfileViews" =========
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
    "userId" INTEGER REFERENCES "users"("id") ON DELETE SET NULL, -- [!] References users FK
    "photo" TEXT,
    "originCountry" VARCHAR(255),
    "producerId" INTEGER REFERENCES "producers"("id") ON DELETE SET NULL, -- [!] References producers FK
    "producerNew" VARCHAR(255),
    "typeCategory" VARCHAR(255),
    "abv" VARCHAR(255),
    "age" VARCHAR(255),
    "reviewLink" VARCHAR(255)
);

-- ========= "requestEdits" =========
CREATE TABLE "requestEdits" (
    "id" SERIAL PRIMARY KEY,
    "editDesc" TEXT,
    "listingId" INTEGER REFERENCES "listings"("id") ON DELETE SET NULL, -- [!] References listings FK
    "userId" INTEGER REFERENCES "users"("id") ON DELETE SET NULL, -- [!] References users FK
    "brandRelation" VARCHAR(255),
    "reviewStatus" BOOLEAN,
    "duplicateLink" VARCHAR(255),
    "sourceLink" VARCHAR(255)
);