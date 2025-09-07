-- Migration: Add variantGroupID column to myCellarItems table
-- Date: 2025-09-08
-- Purpose: Add variantGroupID column to support grouping items with same listing/variant/format/volume

-- Add the variantGroupID column
ALTER TABLE "myCellarItems" 
ADD COLUMN "variantGroupID" INTEGER REFERENCES "myCellarItems"("id") ON DELETE SET NULL;

-- Add index for performance
CREATE INDEX idx_cellar_variant_group ON "myCellarItems" ("variantGroupID");

-- Update existing records to set variantGroupID
-- For master records (quantityVariantID = 1), set variantGroupID to their own ID
UPDATE "myCellarItems" 
SET "variantGroupID" = "id" 
WHERE "quantityVariantID" = 1;

-- For individual bottles (quantityVariantID > 1), set variantGroupID to their master's ID
UPDATE "myCellarItems" AS individual
SET "variantGroupID" = master."id"
FROM "myCellarItems" AS master
WHERE individual."quantityVariantID" > 1
  AND master."quantityVariantID" = 1
  AND master."listingID" = individual."listingID"
  AND (master."variant" = individual."variant" OR (master."variant" IS NULL AND individual."variant" IS NULL))
  AND master."collectionID" = individual."collectionID";

-- Verify the update
SELECT 
    "id",
    "listingID",
    "variant", 
    "quantityVariantID",
    "variantGroupID",
    "drinkFormat",
    "volumeNumber",
    "volumeUnit"
FROM "myCellarItems" 
ORDER BY "listingID", "variant", "quantityVariantID";
