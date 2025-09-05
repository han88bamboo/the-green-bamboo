# Cellar Schema Migration Summary

## Overview
The cellar system has been migrated from a quantity-based model to an individual item tracking model. This change affects how consumption status and inventory are managed.

## Key Changes

### Database Schema Changes
1. **Column Change**: `quantityOwned` → `quantityVariantID`
2. **Data Model**: Each row now represents one physical bottle/item instead of a collection of items
3. **Consumption Tracking**: Each item can have its own consumption status (Unopened/Opened/Empty)

### Fixed Issues

#### Database Schema (01-postgresql_data3.sql)
- ✅ Fixed constraint: `check_quantity_positive CHECK ("quantityOwned" >= 0)` → `check_quantity_variant_positive CHECK ("quantityVariantID" >= 1)`

#### Backend Code (getData.py)
- ✅ Updated `getCellarData` endpoint to use `quantityVariantID` instead of `quantityOwned`
- ✅ Updated collections query to count items instead of summing quantities
- ✅ Updated summary calculations to count individual items
- ✅ Updated `getCellarDashboard` endpoint for new schema
- ✅ Modified breakdown calculations to work with individual items
- ✅ Updated valid sort fields to include `quantityVariantID`
- ✅ Added documentation comments explaining the new data model

## Data Model Changes

### Before (Old Schema)
```sql
-- One record could represent multiple bottles
{
  "id": 1,
  "listingID": 123,
  "quantityOwned": 5,  -- 5 bottles of the same item
  "status": "In Possession",
  "consumption": "Unopened"  -- All 5 bottles have same status
}
```

### After (New Schema)
```sql
-- Each record represents one physical bottle
{
  "id": 1,
  "listingID": 123,
  "quantityVariantID": 1,  -- Variant identifier
  "status": "In Possession",
  "consumption": "Unopened"  -- This specific bottle's status
}
{
  "id": 2,
  "listingID": 123,
  "quantityVariantID": 1,
  "status": "In Possession", 
  "consumption": "Opened"    -- Different consumption status
}
```

## API Response Changes

### getCellarData Endpoint
- `quantityOwned` field removed from response
- `quantityVariantID` field added
- Summary counts now reflect individual items (each item = 1 bottle)
- Status and type breakdowns count individual items

### getCellarDashboard Endpoint  
- All aggregations now count individual items rather than summing quantities
- Financial calculations remain per-item (no quantity multiplication)
- Breakdown statistics reflect individual item counts

## Migration Considerations

### For Existing Data
You'll need to create a migration script to:
1. Convert existing records with `quantityOwned > 1` into multiple individual records
2. Assign appropriate `quantityVariantID` values
3. Set individual consumption status for each item

### For Frontend Applications
- Update UI to display individual items rather than quantity aggregations
- Modify forms to add/edit individual bottles
- Update inventory management to handle per-item consumption tracking

## Benefits of New Schema

1. **Granular Tracking**: Each bottle can have different consumption states
2. **Better History**: Individual item history and changes can be tracked
3. **Flexible Management**: Users can mark specific bottles as opened, empty, etc.
4. **Accurate Inventory**: More precise tracking of actual bottle conditions

## Potential Issues to Address

1. **Performance**: More records means potentially larger datasets - consider indexing strategy
2. **UI Complexity**: Frontend may need to group similar items for display purposes
3. **Migration Complexity**: Existing data needs careful conversion
4. **API Compatibility**: Consumers of the API may need updates for the new response structure

## Recommendations

1. **Create Migration Script**: Convert existing quantity-based records to individual items
2. **Update Frontend**: Modify UI to handle individual item tracking
3. **Add Grouping Logic**: For display purposes, group similar items by listing and variant
4. **Performance Testing**: Test with larger datasets to ensure query performance
5. **API Versioning**: Consider versioning the API to maintain backward compatibility during transition
