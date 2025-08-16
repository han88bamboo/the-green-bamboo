import logging
import os
from psycopg2.extras import execute_values

from flask import Blueprint, g, request, jsonify
from datetime import datetime
from urllib.request import urlopen

logger = logging.getLogger(__name__)

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
logger.info(project_root)


@blueprint.route("/", methods=['POST'])
@blueprint.route("", methods=['POST'])
def updateMenu():
    conn = g.db
    cur = conn.cursor()
    
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

        # Delete existing menu sections for this venue
        cur.execute('DELETE FROM "venuesMenu" WHERE "venueId" = %s', (venue_id,))
        
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
                None  # parentSectionId is NULL for top-level sections
            ))
        
        # Check if we have any valid sections to insert
        if not sections_data:
            # No sections to insert - this is valid (user wants to clear all sections)
            conn.commit()
            return jsonify({
                "code": 200,
                "message": "Venue menu updated successfully. All sections removed."
            }), 200
        
        # Batch insert sections and get their IDs
        section_ids = execute_values(
            cur,
            """
            INSERT INTO "venuesMenu" ("sectionName", "sectionOrder", "venueId", "parentSectionId")
            VALUES %s
            RETURNING "id";
            """,
            sections_data,
            fetch=True
        )
        
        # Verify we got the expected number of section IDs
        if not section_ids or len(section_ids) != len(sections_data):
            raise Exception("Failed to insert sections or retrieve section IDs")

        # for i in section_ids:
        #     print(i)
        
        # Create mapping of section index to generated ID
        section_id_map = {i: section_id["id"] for i, section_id in enumerate(section_ids)}
        
        # Now prepare subsections data
        subsections_data = []
        for section_index, section in enumerate(menu_data):
            if not isinstance(section, dict):
                continue  # Skip invalid section data
                
            parent_id = section_id_map.get(section_index)
            if parent_id is None:
                continue  # Skip if we don't have a parent ID
                
            sub_sections = section.get("subSections", [])
            
            if isinstance(sub_sections, list):
                for sub in sub_sections:
                    if isinstance(sub, dict):
                        subsections_data.append((
                            sub.get("sectionName"),
                            sub.get("sectionOrder"),
                            venue_id,
                            parent_id
                        ))
        
        # Batch insert subsections if any exist
        if subsections_data:
            execute_values(
                cur,
                """
                INSERT INTO "venuesMenu" ("sectionName", "sectionOrder", "venueId", "parentSectionId")
                VALUES %s;
                """,
                subsections_data
            )
        
        conn.commit()
        return jsonify({
            "code": 200,
            "message": "Venue menu updated successfully."
        }), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        conn.rollback()
        return jsonify({
            "code": 500,
            "message": "An error occurred when updating the venue's menu."
        }), 500
    finally:
        cur.close()