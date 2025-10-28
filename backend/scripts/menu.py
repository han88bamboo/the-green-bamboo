import logging
import os
import psycopg2
from psycopg2.extras import execute_values

from flask import Blueprint, g, request, jsonify
from psycopg2.extras import RealDictCursor # ADDED BY SMU GROUP 3
from datetime import datetime
from urllib.request import urlopen

# Import the database manager for connection pooling
from app import db_manager

logger = logging.getLogger(__name__)

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
logger.info(project_root)


@blueprint.route("/<int:venue_id>", methods=['GET'])
def getMenuSections(venue_id: int):
    request_id = getattr(g, 'request_id', 'unknown')
    
    # Single start log for request tracking
    logger.info(f"Charsiucharlie_debug REQ-{request_id} getMenuSections venue_id={venue_id}")
    
    try: 
        # Input validation
        if not venue_id or venue_id <= 0:
            logger.warning(f"Charsiucharlie_debug REQ-{request_id} Invalid venue_id={venue_id}")
            return jsonify({
                "code": 400, 
                "message": "Invalid venue ID", 
                "request_id": request_id
            }), 400
        
        query = """
            SELECT COALESCE((
                SELECT json_agg(json_build_object(
                    'id', vm.id,
                    'sectionName', vm."sectionName",
                    'sectionOrder', vm."sectionOrder",
                    'parentSectionId', vm."parentSectionId",
                    'isSubSection', vm."isSubSection",
                    'isVisible', vm."isVisible"
                ) ORDER BY vm."sectionOrder")
                FROM "venuesMenu" vm
                WHERE vm."venueId" = %s
            ), '[]'::json) AS menu
        """

        # Use connection pooling with db_manager
        with db_manager.get_cursor() as cursor:
            cursor.execute(query, (venue_id,))
            
            menu_sections = cursor.fetchone()  # one row
            
            # Check if venue exists
            if menu_sections is None:
                logger.warning(f"Charsiucharlie_debug REQ-{request_id} No menu found venue_id={venue_id}")
                return jsonify({
                    "code": 404, 
                    "message": f"No menu found for venue {venue_id}", 
                    "request_id": request_id
                }), 404
            
            menu_data = menu_sections.get('menu', [])
            return jsonify(menu_data)  # just the array

    except psycopg2.Error as db_error:
        logger.error(f"Charsiucharlie_debug REQ-{request_id} DB_ERROR venue_id={venue_id} error={str(db_error)}")
        return jsonify({
            "code": 500,
            "message": "Database error occurred",
            "request_id": request_id
        }), 500
        
    except Exception as e:
        logger.error(f"Charsiucharlie_debug REQ-{request_id} ERROR venue_id={venue_id} error={str(e)}", exc_info=True)
        return jsonify({
            "code": 500,
            "message": "An error occurred when getting the venue's menu.",
            "request_id": request_id
        }), 500


@blueprint.route("/", methods=['POST'])
@blueprint.route("", methods=['POST'])
def updateMenu():
    try:
        data = request.get_json()
        venue_id = data.get("venueID")
        
        # Handle both formats: direct array or wrapped in updatedMenu
        if isinstance(data, dict) and "updatedMenu" in data:
            menu_data = data.get("updatedMenu")
        elif isinstance(data, list):
            menu_data = data
        else:
            menu_data = None

        if not data or not venue_id:
            return jsonify({
                "code": 400,
                "message": "Missing menu data or venue_id."
            }), 400
        
        # Validate menu_data format (can be empty array)
        if menu_data is None or not isinstance(menu_data, list):
            return jsonify({
                "code": 400,
                "message": "Invalid menu data format. Expected an array."
            }), 400

        with db_manager.get_cursor() as cursor:
            # Delete existing menu items and sections for this venue
            # Delete menu items first due to foreign key constraints
            cursor.execute('''
                DELETE FROM "menuItems" 
                WHERE "sectionId" IN (
                    SELECT "id" FROM "venuesMenu" WHERE "venueId" = %s
                )
            ''', (venue_id,))
            
            # Delete existing menu sections for this venue
            cursor.execute('DELETE FROM "venuesMenu" WHERE "venueId" = %s', (venue_id,))
            
            # Prepare data for batch inserts
            sections_data = []
            
            # First, collect all sections
            for section in menu_data:
                if not isinstance(section, dict):
                    continue  # Skip invalid section data
                    
                sections_data.append((
                    section.get("sectionName"),
                    section.get("sectionOrder"),
                    venue_id,
                    None,  # parentSectionId is NULL for top-level sections
                    section.get("isVisible", True)  # Default to visible if not specified
                ))
            
            # Check if we have any valid sections to insert
            if not sections_data:
                # No sections to insert - this is valid (user wants to clear all sections)
                return jsonify({
                    "code": 200,
                    "message": "Venue menu updated successfully. All sections removed."
                }), 200
            
            # Batch insert sections and get their IDs
            section_ids = execute_values(
                cursor,
                """
                INSERT INTO "venuesMenu" ("sectionName", "sectionOrder", "venueId", "parentSectionId", "isVisible")
                VALUES %s
                RETURNING "id";
                """,
                sections_data,
                fetch=True
            )
            
            # Verify we got the expected number of section IDs
            if not section_ids or len(section_ids) != len(sections_data):
                raise Exception("Failed to insert sections or retrieve section IDs")
            
            # Create mapping of section index to generated ID
            section_id_map = {i: section_id["id"] for i, section_id in enumerate(section_ids)}
            
            # Now prepare subsections data and collect menu items for main sections
            subsections_data = []
            menu_items_data = []
            
            # Process main sections and their items
            for section_index, section in enumerate(menu_data):
                if not isinstance(section, dict):
                    continue  # Skip invalid section data
                    
                parent_id = section_id_map.get(section_index)
                if parent_id is None:
                    continue  # Skip if we don't have a parent ID
                
                # Process items for main sections
                section_menu = section.get("sectionMenu", [])
                if isinstance(section_menu, list):
                    for item in section_menu:
                        if isinstance(item, dict):
                            menu_items_data.append((
                                item.get("itemOrder", 0),
                                item.get("itemPrice"),
                                item.get("itemAvailability", True),
                                item.get("itemID"),
                                item.get("servingType"),
                                parent_id,
                                item.get("variant")
                            ))
                
                # Process subsections
                sub_sections = section.get("subSections", [])
                if isinstance(sub_sections, list):
                    for sub in sub_sections:
                        if isinstance(sub, dict):
                            subsections_data.append((
                                sub.get("sectionName"),
                                sub.get("sectionOrder"),
                                venue_id,
                                parent_id,
                                sub.get("isVisible", True)  # Default to visible if not specified
                            ))
            
            # Batch insert subsections if any exist and get their IDs
            subsection_id_map = {}
            if subsections_data:
                subsection_ids = execute_values(
                    cursor,
                    """
                    INSERT INTO "venuesMenu" ("sectionName", "sectionOrder", "venueId", "parentSectionId", "isVisible")
                    VALUES %s
                    RETURNING "id";
                    """,
                    subsections_data,
                    fetch=True
                )
                
                # Create mapping for subsection IDs
                subsection_id_map = {i: subsection_id["id"] for i, subsection_id in enumerate(subsection_ids)}
            
            # Process items for subsections
            subsection_index = 0
            for section_index, section in enumerate(menu_data):
                if not isinstance(section, dict):
                    continue
                    
                sub_sections = section.get("subSections", [])
                if isinstance(sub_sections, list):
                    for sub in sub_sections:
                        if isinstance(sub, dict):
                            subsection_id = subsection_id_map.get(subsection_index)
                            if subsection_id:
                                # Process items for this subsection
                                section_menu = sub.get("sectionMenu", [])
                                if isinstance(section_menu, list):
                                    for item in section_menu:
                                        if isinstance(item, dict):
                                            menu_items_data.append((
                                                item.get("itemOrder", 0),
                                                item.get("itemPrice"),
                                                item.get("itemAvailability", True),
                                                item.get("itemID"),
                                                item.get("servingType"),
                                                subsection_id,
                                                item.get("variant")
                                            ))
                            subsection_index += 1
            
            # Batch insert menu items if any exist
            if menu_items_data:
                execute_values(
                    cursor,
                    """
                    INSERT INTO "menuItems" ("itemOrder", "itemPrice", "itemAvailability", "itemID", "itemServingType", "sectionId", "variant")
                    VALUES %s;
                    """,
                    menu_items_data
                )

        return jsonify({
            "code": 200,
            "message": "Venue menu updated successfully."
        }), 200

    except Exception as e:
        print(e)
        import traceback
        traceback.print_exc()
        return jsonify({
            "code": 500,
            "message": "An error occurred when updating the venue's menu."
        }), 500

# [GET] Specific Venue
@blueprint.route("/getMenuItems/<section_id>")
def getMenuItems(section_id):
    """Optimized version with performance improvements and better error handling"""
    request_id = getattr(g, 'request_id', 'unknown')
    
    # Start log with section_id
    logger.info(f"Charsiucharlie_debug REQ-{request_id} getMenuItems section_id={section_id}")
    
    # Input validation
    if not section_id:
        logger.warning(f"Charsiucharlie_debug REQ-{request_id} Missing section_id")
        return jsonify({"code": 400, "message": "Menu category is mandatory.", "request_id": request_id}), 400
    
    # Parse and validate query parameters
    try:
        page = max(1, int(request.args.get("page", 1)))
        # limit = min(100, max(1, int(request.args.get("limit", 20))))  # Cap at 100
        limit = 1000  # Remove pagination - load all items
        search = request.args.get("search", "").strip()
    except ValueError:
        logger.warning(f"Charsiucharlie_debug REQ-{request_id} Invalid pagination params section_id={section_id}")
        return jsonify({"code": 400, "message": "Invalid pagination parameters", "request_id": request_id}), 400
    
    offset = 0  # (page - 1) * limit
    
    try:
        with db_manager.get_cursor() as cursor:
            # Build WHERE conditions (use proper parameterization)
            where_conditions = ['mi."sectionId" = %s']
            params = [section_id]
            
            where_clause = "".join(where_conditions)
            
            sql = f"""
            WITH flavor_tag_counts AS (
                SELECT 
                    r."reviewTarget",
                    st.id AS subTagId,
                    st."subTag",
                    st."familyTagId",
                    COUNT(*) AS tag_count
                FROM "reviews" r
                CROSS JOIN UNNEST(r."flavourTag") AS flavour_tag_id
                INNER JOIN "subTags" st ON st.id = flavour_tag_id::integer
                WHERE r."reviewTarget" IS NOT NULL 
                AND r."flavourTag" IS NOT NULL 
                AND array_length(r."flavourTag", 1) > 0
                GROUP BY r."reviewTarget", st.id, st."subTag", st."familyTagId"
            ),
            ranked_flavours AS (
                SELECT 
                    "reviewTarget",
                    "subTag",
                    "familyTagId",
                    tag_count,
                    ROW_NUMBER() OVER (
                        PARTITION BY "reviewTarget" 
                        ORDER BY tag_count DESC
                    ) AS rn
                FROM flavor_tag_counts
            ),  
            top_flavours AS (
                SELECT 
                    "reviewTarget",
                    JSON_AGG(
                        JSON_BUILD_OBJECT(
                            'tag', rf."subTag",
                            'count', rf.tag_count,
                            'hexcode', ft.hexcode,
                            'tagId', rf."familyTagId"  -- or keep both subTagId + familyTagId if needed
                        ) ORDER BY rf.tag_count DESC
                    ) AS top_tags
                FROM ranked_flavours rf
                INNER JOIN "flavourTags" ft ON ft.id = rf."familyTagId"
                WHERE rf.rn <= 3
                GROUP BY "reviewTarget"
            )
            SELECT 
                mi."id", mi."sectionId", mi."itemID", mi."itemOrder", 
                lst."listingName", lst."photo", lst."bottler", lst."drinkType", lst."abv", 
                lst."officialDesc", lst."originCountry", lst."typeCategory", lst."producerID",
                p."producerName",
                mi."itemPrice", mi."itemAvailability", mi."new", mi."staffPick", mi."itemServingType", 
                srvTyp."servingType", mi."variant",
                (SELECT AVG(r."rating") 
                FROM "reviews" r 
                WHERE r."reviewTarget" = lst."id") as "avgRating",
                COALESCE(tft.top_tags, '[]'::json) as "topFlavorTags", -- Top 3 flavor tags with hex codes
                COUNT(*) OVER() as total_count
            FROM "menuItems" mi
            INNER JOIN "listings" lst
                ON mi."itemID" = lst."id"
            INNER JOIN "producers" p
                ON lst."producerID" = p."id"
            LEFT JOIN "servingTypes" srvTyp
                ON mi."itemServingType" = srvTyp."id"
            LEFT JOIN top_flavours tft
                ON lst."id" = tft."reviewTarget"
            WHERE {where_clause}
            ORDER BY mi."itemOrder" ASC; -- , mi."id" ASC for tie-breaker
            """
            
            # Execute complex menu items query
            cursor.execute(sql, params)  # + [limit, offset]
            rows = cursor.fetchall()
            
            if not rows:
                total_items = 0
                menu_items = []
                logger.info(f"Charsiucharlie_debug REQ-{request_id} getMenuItems success section_id={section_id} items=0")
            else:
                # Get total count from the window function (access by key since using RealDictRow)
                # "description": row['officialDesc'],
                total_items = rows[0]['total_count']
                menu_items = [
                    {
                        "id": row['id'],
                        "sectionId": row['sectionId'], 
                        "itemID": row['itemID'],
                        "itemOrder": row['itemOrder'],
                        "name": row['listingName'],
                        "photo": row['photo'],
                        "bottler": row['bottler'], 
                        "drinkType": row['drinkType'],
                        "abv": row['abv'],
                        "description": row['officialDesc'],
                        "originCountry": row['originCountry'],
                        "typeCategory": row['typeCategory'],
                        "producerID": row['producerID'],
                        "producerName": row['producerName'],
                        "avgRating": "-" if row['avgRating'] is None else round(float(row['avgRating']), 1),
                        "itemAvailability": row['itemAvailability'],
                        "new": row['new'],
                        "staffPick": row['staffPick'],
                        "variant": row['variant'],
                        "servingType": row['itemServingType'],
                        "servingTypeText": row['servingType'],
                        "itemPrice": float(row['itemPrice']) if row['itemPrice'] is not None else None,
                        "topFlavorTags": row['topFlavorTags']
                    }
                    for row in rows
                ]
                # Log success with result count
                logger.info(f"Charsiucharlie_debug REQ-{request_id} getMenuItems success section_id={section_id} items={total_items}")
            
            # Calculate pagination info
            total_pages = (total_items + limit - 1) // limit
            has_next = page < total_pages
            has_prev = page > 1
            
            return jsonify({
                "code": 200,
                "data": menu_items,
                "pagination": {
                    "page": page,
                    "limit": limit,
                    "total_items": total_items,
                    "total_pages": total_pages,
                    "has_next": has_next,
                    "has_prev": has_prev
                }
            }), 200
        
    except psycopg2.Error as db_error:
        logger.error(f"Charsiucharlie_debug REQ-{request_id} DB_ERROR section_id={section_id} error={str(db_error)}")
        return jsonify({
            "code": 500,
            "message": "Database error occurred",
            "request_id": request_id
        }), 500
        
    except Exception as e:
        logger.error(f"Charsiucharlie_debug REQ-{request_id} ERROR section_id={section_id} error={str(e)}", exc_info=True)
        return jsonify({
            "code": 500,
            "message": "An error occurred retrieving menu items.",
            "request_id": request_id
        }), 500