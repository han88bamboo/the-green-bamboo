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

        # Delete existing menu sections for this venue
        # print(f"About to delete sections for venue_id: {venue_id}")
        cur.execute('DELETE FROM "venuesMenu" WHERE "venueId" = %s', (venue_id,))
        # deleted_count = cur.rowcount
        # print(f"Deleted {deleted_count} rows")
        
        # Prepare data for batch inserts
        sections_data = []
        subsections_data = []
        
        # First, collect all sections
        for section in menu_data:
            sections_data.append((
                section.get("sectionName"),
                section.get("sectionOrder"),
                venue_id,
                None  # parentSectionId is NULL for top-level sections
            ))
        
        # Batch insert sections and get their IDs
        if sections_data:
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
            
            # Create mapping of section index to generated ID
            section_id_map = {i: section_id[0] for i, section_id in enumerate(section_ids)}
            
            # Now prepare subsections data
            for section_index, section in enumerate(menu_data):
                parent_id = section_id_map[section_index]
                sub_sections = section.get("subSections", [])
                
                for sub in sub_sections:
                    subsections_data.append((
                        sub.get("sectionName"),
                        sub.get("sectionOrder"),
                        venue_id,
                        parent_id
                    ))
            
            # Batch insert subsections
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
