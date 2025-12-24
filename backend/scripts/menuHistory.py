# Port: 5306
# Routes: /getMenuHistory (GET), /getSnapshotDetails (GET), /updateSnapshotVersionName (PATCH)
# -----------------------------------------------------------------------------------------

import os
from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import traceback
import logging

# Import the database manager for connection pooling
from app import db_manager

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

# Initialize logger
logger = logging.getLogger(__name__)

# Configuration constants
AGGREGATION_WINDOW_HOURS = 3  # Rolling window for version aggregation

# -----------------------------------------------------------------------------------------
# Helper function: Create or update a menu snapshot
# This is called from editVenueProfile.py after menu saves
# -----------------------------------------------------------------------------------------

def create_or_update_menu_snapshot(cursor, venue_id: int) -> dict:
    """
    Create a new menu snapshot or update existing one within the 3-hour aggregation window.
    
    This function captures the entire current state of a venue's menu (sections, subsections, 
    and items) as a point-in-time snapshot. If a snapshot was already taken within the last 
    3 hours, it will be updated instead of creating a new version.
    
    Args:
        cursor: Database cursor (must be within an active transaction)
        venue_id: The ID of the venue whose menu to snapshot
        
    Returns:
        dict with keys:
            - success: bool
            - version_id: int (the snapshot version ID)
            - is_new_version: bool (True if new version created, False if existing updated)
            - sections_count: int
            - items_count: int
            - message: str
    """
    try:
        current_time = datetime.now()
        window_start = current_time - timedelta(hours=AGGREGATION_WINDOW_HOURS)
        
        # Check if there's an existing snapshot within the aggregation window
        cursor.execute(
            '''
            SELECT "id", "snapshotTimestamp", "aggregationWindowStart"
            FROM "venueMenuVersionSnapshots"
            WHERE "venueId" = %s
            AND "aggregationWindowStart" >= %s
            ORDER BY "snapshotTimestamp" DESC
            LIMIT 1
            ''',
            (venue_id, window_start)
        )
        existing_snapshot = cursor.fetchone()
        
        if existing_snapshot:
            # Update existing snapshot - delete old section/item snapshots and recreate
            version_id = existing_snapshot['id']
            is_new_version = False
            original_window_start = existing_snapshot['aggregationWindowStart']
            
            # Delete existing item snapshots (cascade will handle this, but being explicit)
            cursor.execute(
                '''
                DELETE FROM "venueMenuItemSnapshots"
                WHERE "versionSnapshotId" = %s
                ''',
                (version_id,)
            )
            
            # Delete existing section snapshots
            cursor.execute(
                '''
                DELETE FROM "venueMenuSectionSnapshots"
                WHERE "versionSnapshotId" = %s
                ''',
                (version_id,)
            )
            
            # Update the version snapshot timestamp
            cursor.execute(
                '''
                UPDATE "venueMenuVersionSnapshots"
                SET "snapshotTimestamp" = %s
                WHERE "id" = %s
                ''',
                (current_time, version_id)
            )
            
            logger.info(f"Updating existing snapshot {version_id} for venue {venue_id}")
        else:
            # Create new version snapshot
            is_new_version = True
            original_window_start = current_time
            
            # Generate version name like "December Menu 1", "December Menu 2", etc.
            month_name = current_time.strftime('%B')  # Full month name (e.g., "December")
            
            # Count existing snapshots with this month name pattern for this venue
            cursor.execute(
                '''
                SELECT COUNT(*) as count
                FROM "venueMenuVersionSnapshots"
                WHERE "venueId" = %s
                AND "versionName" LIKE %s
                ''',
                (venue_id, f'{month_name} Menu %')
            )
            existing_count = cursor.fetchone()['count']
            version_name = f"{month_name} Menu {existing_count + 1}"
            
            cursor.execute(
                '''
                INSERT INTO "venueMenuVersionSnapshots" 
                ("venueId", "versionName", "snapshotTimestamp", "aggregationWindowStart")
                VALUES (%s, %s, %s, %s)
                RETURNING "id"
                ''',
                (venue_id, version_name, current_time, current_time)
            )
            version_id = cursor.fetchone()['id']
            
            logger.info(f"Created new snapshot version {version_id} '{version_name}' for venue {venue_id}")
        
        # ===== Capture all sections (main sections and subsections) =====
        cursor.execute(
            '''
            SELECT 
                "id",
                "sectionName",
                "isSubSection",
                "parentSectionId",
                "sectionOrder",
                "sectionDescription",
                "isVisible",
                "subscribersEnabled"
            FROM "venuesMenu"
            WHERE "venueId" = %s
            ORDER BY "sectionOrder"
            ''',
            (venue_id,)
        )
        sections = cursor.fetchall()
        
        # Skip empty menus
        if not sections:
            logger.info(f"No sections found for venue {venue_id}, snapshot will be empty")
            return {
                'success': True,
                'version_id': version_id,
                'is_new_version': is_new_version,
                'sections_count': 0,
                'items_count': 0,
                'message': 'Empty menu snapshot created'
            }
        
        # Create section snapshots and build mapping from original ID to snapshot ID
        section_snapshot_mapping = {}  # original_section_id -> section_snapshot_id
        sections_count = 0
        
        for section in sections:
            cursor.execute(
                '''
                INSERT INTO "venueMenuSectionSnapshots"
                ("versionSnapshotId", "originalSectionId", "sectionName", "isSubSection",
                 "parentSectionId", "sectionOrder", "sectionDescription", "isVisible", "subscribersEnabled")
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING "id"
                ''',
                (
                    version_id,
                    section['id'],
                    section['sectionName'],
                    section['isSubSection'],  # Boolean from venuesMenu
                    section['parentSectionId'],  # Store original parent ID (not FK)
                    section['sectionOrder'],  # Keep as VARCHAR to match source table
                    section['sectionDescription'],
                    section['isVisible'],  # Capture visibility state
                    section['subscribersEnabled']  # Capture subscription state
                )
            )
            section_snapshot_id = cursor.fetchone()['id']
            section_snapshot_mapping[section['id']] = section_snapshot_id
            sections_count += 1
        
        # ===== Capture all menu items with their full data =====
        # Only capture menuItems columns directly - no JOIN to listings (itemName fetched at retrieval time)
        cursor.execute(
            '''
            SELECT 
                mi."id",
                mi."sectionId",
                mi."itemID",
                mi."itemOrder",
                mi."itemPrice",
                mi."itemPriceCurrency",
                mi."itemAvailability",
                mi."itemServingType",
                mi."variant",
                mi."new",
                mi."staffPick"
            FROM "menuItems" mi
            WHERE mi."sectionId" IN (
                SELECT "id" FROM "venuesMenu" WHERE "venueId" = %s
            )
            ORDER BY mi."sectionId", mi."itemOrder"
            ''',
            (venue_id,)
        )
        items = cursor.fetchall()
        
        items_count = 0
        for item in items:
            # Get the section snapshot ID for this item
            section_snapshot_id = section_snapshot_mapping.get(item['sectionId'])
            if section_snapshot_id is None:
                logger.warning(f"Item {item['id']} has sectionId {item['sectionId']} not in mapping, skipping")
                continue
            
            cursor.execute(
                '''
                INSERT INTO "venueMenuItemSnapshots"
                ("versionSnapshotId", "sectionSnapshotId", "originalItemId", "originalSectionId",
                 "itemOrder", "itemPrice", "itemAvailability", "itemID", "itemServingType",
                 "variant", "new", "staffPick", "itemPriceCurrency")
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''',
                (
                    version_id,
                    section_snapshot_id,
                    item['id'],  # originalItemId
                    item['sectionId'],  # originalSectionId
                    item['itemOrder'],
                    item['itemPrice'],
                    item['itemAvailability'],
                    item['itemID'],  # FK to listings
                    item['itemServingType'],
                    item['variant'],
                    item['new'],
                    item['staffPick'],
                    item['itemPriceCurrency']
                )
            )
            items_count += 1
        
        logger.info(f"Snapshot {version_id} completed: {sections_count} sections, {items_count} items")
        
        return {
            'success': True,
            'version_id': version_id,
            'is_new_version': is_new_version,
            'sections_count': sections_count,
            'items_count': items_count,
            'message': f"{'New' if is_new_version else 'Updated'} snapshot created successfully"
        }
        
    except Exception as e:
        logger.error(f"Error creating menu snapshot for venue {venue_id}: {str(e)}")
        logger.error(traceback.format_exc())
        # Re-raise to let the caller's transaction rollback handle this
        raise


# -----------------------------------------------------------------------------------------
# [GET] Get menu history versions for a venue
# - Returns list of snapshot versions with metadata (no items loaded yet - lazy loading)
# - Possible return codes: 200 (Success), 404 (Venue not found), 500 (Error)
# -----------------------------------------------------------------------------------------

@blueprint.route('/getMenuHistory', methods=['GET'])
def getMenuHistory():
    venue_id = request.args.get('venueId', type=int)
    
    if not venue_id:
        return jsonify({
            "code": 400,
            "message": "venueId is required"
        }), 400
    
    try:
        with db_manager.get_cursor() as cursor:
            # Verify venue exists
            cursor.execute('SELECT "id", "venueName" FROM "venues" WHERE "id" = %s', (venue_id,))
            venue = cursor.fetchone()
            
            if not venue:
                return jsonify({
                    "code": 404,
                    "message": "Venue not found"
                }), 404
            
            # Get all snapshots with section/item counts (for display)
            cursor.execute(
                '''
                SELECT 
                    v."id",
                    v."versionName",
                    v."snapshotTimestamp",
                    v."aggregationWindowStart",
                    v."createdAt",
                    (SELECT COUNT(*) FROM "venueMenuSectionSnapshots" WHERE "versionSnapshotId" = v."id") as "sectionsCount",
                    (SELECT COUNT(*) FROM "venueMenuItemSnapshots" WHERE "versionSnapshotId" = v."id") as "itemsCount"
                FROM "venueMenuVersionSnapshots" v
                WHERE v."venueId" = %s
                ORDER BY v."snapshotTimestamp" DESC
                ''',
                (venue_id,)
            )
            snapshots = cursor.fetchall()
            
            # Format response
            history = []
            for snapshot in snapshots:
                history.append({
                    'versionId': snapshot['id'],
                    'versionName': snapshot['versionName'],
                    'snapshotTimestamp': snapshot['snapshotTimestamp'].isoformat() if snapshot['snapshotTimestamp'] else None,
                    'aggregationWindowStart': snapshot['aggregationWindowStart'].isoformat() if snapshot['aggregationWindowStart'] else None,
                    'createdAt': snapshot['createdAt'].isoformat() if snapshot['createdAt'] else None,
                    'sectionsCount': snapshot['sectionsCount'],
                    'itemsCount': snapshot['itemsCount']
                })
            
            return jsonify({
                "code": 200,
                "data": {
                    "venueId": venue_id,
                    "venueName": venue['venueName'],
                    "history": history,
                    "totalVersions": len(history)
                }
            }), 200
            
    except Exception as e:
        logger.error(f"Error fetching menu history for venue {venue_id}: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            "code": 500,
            "message": f"An error occurred: {str(e)}"
        }), 500


# -----------------------------------------------------------------------------------------
# [GET] Get snapshot details with sections (lazy load items on accordion expand)
# - Returns section structure for a specific snapshot version
# - Possible return codes: 200 (Success), 404 (Snapshot not found), 500 (Error)
# -----------------------------------------------------------------------------------------

@blueprint.route('/getSnapshotDetails', methods=['GET'])
def getSnapshotDetails():
    version_id = request.args.get('versionId', type=int)
    include_items = request.args.get('includeItems', 'false').lower() == 'true'
    section_id = request.args.get('sectionId', type=int)  # Optional: load items for specific section only
    
    if not version_id:
        return jsonify({
            "code": 400,
            "message": "versionId is required"
        }), 400
    
    try:
        with db_manager.get_cursor() as cursor:
            # Get snapshot metadata
            cursor.execute(
                '''
                SELECT v.*, ve."venueName"
                FROM "venueMenuVersionSnapshots" v
                JOIN "venues" ve ON v."venueId" = ve."id"
                WHERE v."id" = %s
                ''',
                (version_id,)
            )
            snapshot = cursor.fetchone()
            
            if not snapshot:
                return jsonify({
                    "code": 404,
                    "message": "Snapshot version not found"
                }), 404
            
            # Get all sections for this snapshot
            cursor.execute(
                '''
                SELECT 
                    s.*,
                    (SELECT COUNT(*) FROM "venueMenuItemSnapshots" WHERE "sectionSnapshotId" = s."id") as "itemCount"
                FROM "venueMenuSectionSnapshots" s
                WHERE s."versionSnapshotId" = %s
                ORDER BY s."sectionOrder"
                ''',
                (version_id,)
            )
            sections = cursor.fetchall()
            
            # Build hierarchical structure (main sections with subsections nested)
            sections_map = {}
            main_sections = []
            
            for section in sections:
                section_data = {
                    'sectionSnapshotId': section['id'],
                    'originalSectionId': section['originalSectionId'],
                    'sectionName': section['sectionName'],
                    'isSubSection': section['isSubSection'] if 'isSubSection' in section else False,
                    'sectionOrder': section['sectionOrder'],
                    'sectionDescription': section['sectionDescription'],
                    'isVisible': section['isVisible'] if 'isVisible' in section else True,
                    'subscribersEnabled': section['subscribersEnabled'] if 'subscribersEnabled' in section else False,
                    'itemCount': section['itemCount'],
                    'subsections': [],
                    'items': []  # Will be loaded lazily if requested
                }
                
                sections_map[section['originalSectionId']] = section_data
                
                if not section_data['isSubSection']:
                    main_sections.append(section_data)
            
            # Link subsections to their parents
            for section in sections:
                is_subsection = section['isSubSection'] if 'isSubSection' in section else False
                if is_subsection and section['parentSectionId']:
                    parent = sections_map.get(section['parentSectionId'])
                    if parent:
                        parent['subsections'].append(sections_map[section['originalSectionId']])
            
            # If items requested, load them
            if include_items:
                if section_id:
                    # Load items for specific section only (lazy loading on accordion expand)
                    # JOIN to listings, producers, and servingTypes for display
                    cursor.execute(
                        '''
                        SELECT i.*, l."listingName" as "itemName", l."officialDesc" as "itemDescription",
                               p."producerName" as "itemProducer",
                               st."servingType" as "itemServingTypeName"
                        FROM "venueMenuItemSnapshots" i
                        LEFT JOIN "listings" l ON i."itemID" = l."id"
                        LEFT JOIN "producers" p ON l."producerID" = p."id"
                        LEFT JOIN "servingTypes" st ON i."itemServingType" = st."id"
                        JOIN "venueMenuSectionSnapshots" s ON i."sectionSnapshotId" = s."id"
                        WHERE s."versionSnapshotId" = %s
                        AND s."originalSectionId" = %s
                        ORDER BY i."itemOrder"
                        ''',
                        (version_id, section_id)
                    )
                else:
                    # Load all items
                    # JOIN to listings, producers, and servingTypes for display
                    cursor.execute(
                        '''
                        SELECT i.*, l."listingName" as "itemName", l."officialDesc" as "itemDescription",
                               p."producerName" as "itemProducer",
                               st."servingType" as "itemServingTypeName"
                        FROM "venueMenuItemSnapshots" i
                        LEFT JOIN "listings" l ON i."itemID" = l."id"
                        LEFT JOIN "producers" p ON l."producerID" = p."id"
                        LEFT JOIN "servingTypes" st ON i."itemServingType" = st."id"
                        WHERE i."versionSnapshotId" = %s
                        ORDER BY i."sectionSnapshotId", i."itemOrder"
                        ''',
                        (version_id,)
                    )
                
                items = cursor.fetchall()
                
                # Map items to their sections using sectionSnapshotId -> originalSectionId
                section_snapshot_to_original = {}
                for section in sections:
                    section_snapshot_to_original[section['id']] = section['originalSectionId']
                
                for item in items:
                    original_section_id = section_snapshot_to_original.get(item['sectionSnapshotId'])
                    if original_section_id and original_section_id in sections_map:
                        sections_map[original_section_id]['items'].append({
                            'itemSnapshotId': item['id'],
                            'originalItemId': item['originalItemId'],
                            'itemID': item['itemID'],  # listingId for restore
                            'itemName': item['itemName'] or 'Unknown Item',  # From JOIN to listings
                            'itemDescription': item['itemDescription'] or '',  # From JOIN to listings
                            'itemProducer': item['itemProducer'],  # From JOIN to producers (can be None)
                            'itemOrder': item['itemOrder'],
                            'itemPrice': float(item['itemPrice']) if item['itemPrice'] else None,
                            'itemPriceCurrency': item['itemPriceCurrency'],
                            'variant': item['variant'],
                            'itemAvailability': item['itemAvailability'],
                            'itemServingType': item['itemServingType'],  # Original integer ID (for restore)
                            'itemServingTypeName': item['itemServingTypeName'],  # Display name from JOIN (for UI)
                            'new': item['new'],
                            'staffPick': item['staffPick']
                        })
            
            return jsonify({
                "code": 200,
                "data": {
                    "versionId": version_id,
                    "venueId": snapshot['venueId'],
                    "venueName": snapshot['venueName'],
                    "snapshotTimestamp": snapshot['snapshotTimestamp'].isoformat() if snapshot['snapshotTimestamp'] else None,
                    "sections": main_sections
                }
            }), 200
            
    except Exception as e:
        logger.error(f"Error fetching snapshot details for version {version_id}: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            "code": 500,
            "message": f"An error occurred: {str(e)}"
        }), 500


# NOTE: /restoreFromSnapshot endpoint has been removed.
# Restore functionality is now handled entirely in the frontend by adding 
# sections/items to the staged editMenu state. The user must click "Save"
# to persist restored items to the database.


# -----------------------------------------------------------------------------------------
# [PATCH] Update snapshot version name
# - Allows renaming a snapshot version
# - Possible return codes: 200 (Success), 400 (Invalid input), 404 (Not found), 500 (Error)
# -----------------------------------------------------------------------------------------

@blueprint.route('/updateSnapshotVersionName', methods=['PATCH'])
def updateSnapshotVersionName():
    data = request.get_json()
    
    if not data:
        return jsonify({
            "code": 400,
            "message": "Request body is required"
        }), 400
    
    version_id = data.get('versionId')
    version_name = data.get('versionName', '').strip()
    
    if not version_id:
        return jsonify({
            "code": 400,
            "message": "versionId is required"
        }), 400
    
    if not version_name:
        return jsonify({
            "code": 400,
            "message": "versionName is required and cannot be empty"
        }), 400
    
    if len(version_name) > 100:
        return jsonify({
            "code": 400,
            "message": "versionName must be 100 characters or less"
        }), 400
    
    try:
        with db_manager.get_cursor() as cursor:
            # Check if snapshot exists
            cursor.execute(
                'SELECT "id", "venueId" FROM "venueMenuVersionSnapshots" WHERE "id" = %s',
                (version_id,)
            )
            snapshot = cursor.fetchone()
            
            if not snapshot:
                return jsonify({
                    "code": 404,
                    "message": "Snapshot version not found"
                }), 404
            
            # Update the version name
            cursor.execute(
                '''
                UPDATE "venueMenuVersionSnapshots"
                SET "versionName" = %s
                WHERE "id" = %s
                ''',
                (version_name, version_id)
            )
            
            logger.info(f"Updated snapshot {version_id} version name to '{version_name}'")
            
            return jsonify({
                "code": 200,
                "message": "Version name updated successfully",
                "data": {
                    "versionId": version_id,
                    "versionName": version_name
                }
            }), 200
            
    except Exception as e:
        logger.error(f"Error updating snapshot version name for {version_id}: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            "code": 500,
            "message": f"An error occurred: {str(e)}"
        }), 500
