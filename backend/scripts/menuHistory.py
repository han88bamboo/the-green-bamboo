# Port: 5306
# Routes: /getMenuHistory (GET), /getSnapshotDetails (GET), /restoreFromSnapshot (POST)
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
            
            cursor.execute(
                '''
                INSERT INTO "venueMenuVersionSnapshots" 
                ("venueId", "snapshotTimestamp", "aggregationWindowStart")
                VALUES (%s, %s, %s)
                RETURNING "id"
                ''',
                (venue_id, current_time, current_time)
            )
            version_id = cursor.fetchone()['id']
            
            logger.info(f"Created new snapshot version {version_id} for venue {venue_id}")
        
        # ===== Capture all sections (main sections and subsections) =====
        cursor.execute(
            '''
            SELECT 
                "id",
                "sectionName",
                CASE WHEN "parentSectionId" IS NULL THEN 'section' ELSE 'subsection' END as "sectionType",
                "parentSectionId",
                "sectionOrder",
                "sectionDescription"
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
            # Cast sectionOrder from VARCHAR to INTEGER for snapshot table
            section_order_int = int(section['sectionOrder']) if section['sectionOrder'] else 0
            
            cursor.execute(
                '''
                INSERT INTO "venueMenuSectionSnapshots"
                ("versionSnapshotId", "originalSectionId", "sectionName", "sectionType",
                 "parentSectionId", "sectionOrder", "sectionDescription")
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING "id"
                ''',
                (
                    version_id,
                    section['id'],
                    section['sectionName'],
                    section['sectionType'],
                    section['parentSectionId'],  # Store original parent ID (not FK)
                    section_order_int,  # Convert VARCHAR to INTEGER
                    section['sectionDescription']
                )
            )
            section_snapshot_id = cursor.fetchone()['id']
            section_snapshot_mapping[section['id']] = section_snapshot_id
            sections_count += 1
        
        # ===== Capture all menu items with their full data =====
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
                mi."staffPick",
                l."listingName",
                l."officialDesc"
            FROM "menuItems" mi
            LEFT JOIN "listings" l ON mi."itemID" = l."id"
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
                 "listingId", "itemName", "itemDescription", "itemOrder",
                 "price", "currency", "vintage", "isAvailable", "isFeatured")
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''',
                (
                    version_id,
                    section_snapshot_id,
                    item['id'],
                    item['sectionId'],
                    item['itemID'],  # listingId (can be NULL for custom items)
                    item['listingName'],  # itemName from listing
                    item['officialDesc'],  # itemDescription from listing (officialDesc in listings table)
                    item['itemOrder'],
                    item['itemPrice'],
                    item['itemPriceCurrency'],
                    item['variant'],  # vintage
                    item['itemAvailability'],
                    item['staffPick']  # Using staffPick as isFeatured
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
                    'sectionType': section['sectionType'],
                    'sectionOrder': section['sectionOrder'],
                    'sectionDescription': section['sectionDescription'],
                    'itemCount': section['itemCount'],
                    'subsections': [],
                    'items': []  # Will be loaded lazily if requested
                }
                
                sections_map[section['originalSectionId']] = section_data
                
                if section['sectionType'] == 'section':
                    main_sections.append(section_data)
            
            # Link subsections to their parents
            for section in sections:
                if section['sectionType'] == 'subsection' and section['parentSectionId']:
                    parent = sections_map.get(section['parentSectionId'])
                    if parent:
                        parent['subsections'].append(sections_map[section['originalSectionId']])
            
            # If items requested, load them
            if include_items:
                if section_id:
                    # Load items for specific section only (lazy loading on accordion expand)
                    cursor.execute(
                        '''
                        SELECT i.*
                        FROM "venueMenuItemSnapshots" i
                        JOIN "venueMenuSectionSnapshots" s ON i."sectionSnapshotId" = s."id"
                        WHERE s."versionSnapshotId" = %s
                        AND s."originalSectionId" = %s
                        ORDER BY i."itemOrder"
                        ''',
                        (version_id, section_id)
                    )
                else:
                    # Load all items
                    cursor.execute(
                        '''
                        SELECT i.*
                        FROM "venueMenuItemSnapshots" i
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
                            'listingId': item['listingId'],
                            'itemName': item['itemName'],
                            'itemDescription': item['itemDescription'],
                            'itemOrder': item['itemOrder'],
                            'price': float(item['price']) if item['price'] else None,
                            'currency': item['currency'],
                            'vintage': item['vintage'],
                            'isAvailable': item['isAvailable'],
                            'isFeatured': item['isFeatured']
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


# -----------------------------------------------------------------------------------------
# [POST] Restore items from a snapshot
# - Adds selected sections/items to current menu (never deletes, add-only)
# - Restored items get "(Restored from Menu History)" suffix
# - Skips duplicates with message
# - Possible return codes: 201 (Restored), 400 (Bad request), 500 (Error)
# -----------------------------------------------------------------------------------------

@blueprint.route('/restoreFromSnapshot', methods=['POST'])
def restoreFromSnapshot():
    data = request.get_json()
    
    version_id = data.get('versionId')
    venue_id = data.get('venueId')
    restore_type = data.get('restoreType')  # 'full', 'section', 'subsection', 'item'
    target_section_id = data.get('targetSectionId')  # Current menu section to restore INTO
    
    # IDs of what to restore from snapshot
    section_ids_to_restore = data.get('sectionIds', [])  # For section/subsection restore
    item_ids_to_restore = data.get('itemIds', [])  # For item restore
    
    if not version_id or not venue_id:
        return jsonify({
            "code": 400,
            "message": "versionId and venueId are required"
        }), 400
    
    if not restore_type:
        return jsonify({
            "code": 400,
            "message": "restoreType is required (full, section, subsection, item)"
        }), 400
    
    try:
        with db_manager.get_cursor() as cursor:
            # Verify snapshot exists and belongs to this venue
            cursor.execute(
                '''
                SELECT * FROM "venueMenuVersionSnapshots"
                WHERE "id" = %s AND "venueId" = %s
                ''',
                (version_id, venue_id)
            )
            snapshot = cursor.fetchone()
            
            if not snapshot:
                return jsonify({
                    "code": 404,
                    "message": "Snapshot not found or does not belong to this venue"
                }), 404
            
            restored_sections = []
            restored_items = []
            skipped_items = []
            
            RESTORE_SUFFIX = " (Restored from Menu History)"
            
            if restore_type == 'full':
                # Restore entire menu - all sections and items
                cursor.execute(
                    '''
                    SELECT * FROM "venueMenuSectionSnapshots"
                    WHERE "versionSnapshotId" = %s
                    ORDER BY "sectionOrder"
                    ''',
                    (version_id,)
                )
                sections_to_restore = cursor.fetchall()
                
                # Create sections and track mapping
                result = _restore_sections_and_items(
                    cursor, venue_id, version_id, sections_to_restore, 
                    None, RESTORE_SUFFIX
                )
                restored_sections = result['restored_sections']
                restored_items = result['restored_items']
                skipped_items = result['skipped_items']
                
            elif restore_type == 'section':
                # Restore specific main sections (with their subsections and items)
                if not section_ids_to_restore:
                    return jsonify({
                        "code": 400,
                        "message": "sectionIds required for section restore"
                    }), 400
                
                # Get the sections and their subsections
                cursor.execute(
                    '''
                    SELECT * FROM "venueMenuSectionSnapshots"
                    WHERE "versionSnapshotId" = %s
                    AND ("originalSectionId" = ANY(%s) OR "parentSectionId" = ANY(%s))
                    ORDER BY "sectionOrder"
                    ''',
                    (version_id, section_ids_to_restore, section_ids_to_restore)
                )
                sections_to_restore = cursor.fetchall()
                
                result = _restore_sections_and_items(
                    cursor, venue_id, version_id, sections_to_restore,
                    None, RESTORE_SUFFIX
                )
                restored_sections = result['restored_sections']
                restored_items = result['restored_items']
                skipped_items = result['skipped_items']
                
            elif restore_type == 'subsection':
                # Restore specific subsections into a target section
                if not section_ids_to_restore or not target_section_id:
                    return jsonify({
                        "code": 400,
                        "message": "sectionIds and targetSectionId required for subsection restore"
                    }), 400
                
                cursor.execute(
                    '''
                    SELECT * FROM "venueMenuSectionSnapshots"
                    WHERE "versionSnapshotId" = %s
                    AND "originalSectionId" = ANY(%s)
                    ORDER BY "sectionOrder"
                    ''',
                    (version_id, section_ids_to_restore)
                )
                sections_to_restore = cursor.fetchall()
                
                result = _restore_sections_and_items(
                    cursor, venue_id, version_id, sections_to_restore,
                    target_section_id, RESTORE_SUFFIX
                )
                restored_sections = result['restored_sections']
                restored_items = result['restored_items']
                skipped_items = result['skipped_items']
                
            elif restore_type == 'item':
                # Restore specific items into a target section
                if not item_ids_to_restore or not target_section_id:
                    return jsonify({
                        "code": 400,
                        "message": "itemIds and targetSectionId required for item restore"
                    }), 400
                
                # Verify target section exists
                cursor.execute(
                    'SELECT "id" FROM "venuesMenu" WHERE "id" = %s AND "venueId" = %s',
                    (target_section_id, venue_id)
                )
                if not cursor.fetchone():
                    return jsonify({
                        "code": 404,
                        "message": "Target section not found"
                    }), 404
                
                # Get items to restore
                cursor.execute(
                    '''
                    SELECT * FROM "venueMenuItemSnapshots"
                    WHERE "versionSnapshotId" = %s
                    AND "id" = ANY(%s)
                    ''',
                    (version_id, item_ids_to_restore)
                )
                items = cursor.fetchall()
                
                for item in items:
                    result = _restore_single_item(cursor, item, target_section_id)
                    if result['restored']:
                        restored_items.append(result['item_name'])
                    else:
                        skipped_items.append({
                            'name': result['item_name'],
                            'reason': result['reason']
                        })
            else:
                return jsonify({
                    "code": 400,
                    "message": f"Invalid restoreType: {restore_type}"
                }), 400
            
            return jsonify({
                "code": 201,
                "message": "Restore completed successfully",
                "data": {
                    "restoredSections": restored_sections,
                    "restoredItems": restored_items,
                    "skippedItems": skipped_items,
                    "totalRestored": len(restored_sections) + len(restored_items),
                    "totalSkipped": len(skipped_items)
                }
            }), 201
            
    except Exception as e:
        logger.error(f"Error restoring from snapshot {version_id}: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            "code": 500,
            "message": f"An error occurred: {str(e)}"
        }), 500


def _restore_sections_and_items(cursor, venue_id, version_id, sections_to_restore, 
                                 force_parent_id, restore_suffix):
    """
    Helper to restore sections and their items.
    
    Args:
        cursor: DB cursor
        venue_id: Target venue ID
        version_id: Snapshot version ID
        sections_to_restore: List of section snapshot records
        force_parent_id: If set, all sections become subsections of this parent
        restore_suffix: Suffix to append to restored section names
    
    Returns:
        dict with restored_sections, restored_items, skipped_items
    """
    restored_sections = []
    restored_items = []
    skipped_items = []
    
    # Build mapping from original section IDs to new section IDs
    section_id_mapping = {}  # originalSectionId -> new section ID
    
    # First pass: create all sections
    for section in sections_to_restore:
        # Determine parent
        if force_parent_id:
            parent_id = force_parent_id
        elif section['sectionType'] == 'section':
            parent_id = None
        else:
            # Subsection - need to find parent's new ID
            parent_id = section_id_mapping.get(section['parentSectionId'])
            if parent_id is None and section['parentSectionId']:
                # Parent not restored yet or doesn't exist, skip this subsection
                logger.warning(f"Skipping subsection {section['sectionName']} - parent not found")
                continue
        
        # Get max section order for placement
        cursor.execute(
            '''
            SELECT COALESCE(MAX(CAST("sectionOrder" AS INTEGER)), 0) + 1 as next_order
            FROM "venuesMenu"
            WHERE "venueId" = %s
            ''',
            (venue_id,)
        )
        next_order = cursor.fetchone()['next_order']
        
        # Create section with restored suffix
        restored_name = section['sectionName'] + restore_suffix
        
        cursor.execute(
            '''
            INSERT INTO "venuesMenu"
            ("sectionName", "sectionOrder", "venueId", "parentSectionId", 
             "isVisible", "sectionDescription", "subscribersEnabled")
            VALUES (%s, %s, %s, %s, TRUE, %s, FALSE)
            RETURNING "id"
            ''',
            (restored_name, str(next_order), venue_id, parent_id, section['sectionDescription'])
        )
        new_section_id = cursor.fetchone()['id']
        section_id_mapping[section['originalSectionId']] = new_section_id
        restored_sections.append(restored_name)
    
    # Second pass: restore items for each section
    for section in sections_to_restore:
        new_section_id = section_id_mapping.get(section['originalSectionId'])
        if new_section_id is None:
            continue
        
        # Get items for this section from snapshot
        cursor.execute(
            '''
            SELECT * FROM "venueMenuItemSnapshots"
            WHERE "sectionSnapshotId" = %s
            ORDER BY "itemOrder"
            ''',
            (section['id'],)
        )
        items = cursor.fetchall()
        
        for item in items:
            result = _restore_single_item(cursor, item, new_section_id)
            if result['restored']:
                restored_items.append(result['item_name'])
            else:
                skipped_items.append({
                    'name': result['item_name'],
                    'reason': result['reason']
                })
    
    return {
        'restored_sections': restored_sections,
        'restored_items': restored_items,
        'skipped_items': skipped_items
    }


def _restore_single_item(cursor, item_snapshot, target_section_id):
    """
    Restore a single item from snapshot to a target section.
    
    Returns:
        dict with keys: restored (bool), item_name (str), reason (str if not restored)
    """
    item_name = item_snapshot['itemName'] or f"Item #{item_snapshot['originalItemId']}"
    listing_id = item_snapshot['listingId']
    vintage = item_snapshot['vintage']
    
    if listing_id is None:
        # Custom item without listing - skip
        return {
            'restored': False,
            'item_name': item_name,
            'reason': 'Custom item without listing ID cannot be restored'
        }
    
    # Check if this exact item (listingId + variant) already exists in target section
    cursor.execute(
        '''
        SELECT "id" FROM "menuItems"
        WHERE "sectionId" = %s
        AND "itemID" = %s
        AND COALESCE("variant", -1) = COALESCE(%s, -1)
        ''',
        (target_section_id, listing_id, vintage)
    )
    existing = cursor.fetchone()
    
    if existing:
        return {
            'restored': False,
            'item_name': item_name,
            'reason': 'Item already exists in target section'
        }
    
    # Get next item order
    cursor.execute(
        '''
        SELECT COALESCE(MAX("itemOrder"), 0) + 1 as next_order
        FROM "menuItems"
        WHERE "sectionId" = %s
        ''',
        (target_section_id,)
    )
    next_order = cursor.fetchone()['next_order']
    
    # Insert the item
    cursor.execute(
        '''
        INSERT INTO "menuItems"
        ("itemOrder", "itemPrice", "itemAvailability", "itemID", 
         "itemServingType", "sectionId", "variant", "new", 
         "staffPick", "itemPriceCurrency")
        VALUES (%s, %s, %s, %s, NULL, %s, %s, FALSE, %s, %s)
        RETURNING "id"
        ''',
        (
            next_order,
            item_snapshot['price'],
            item_snapshot['isAvailable'],
            listing_id,
            target_section_id,
            vintage,
            item_snapshot['isFeatured'],  # staffPick
            item_snapshot['currency']
        )
    )
    
    return {
        'restored': True,
        'item_name': item_name,
        'reason': None
    }
