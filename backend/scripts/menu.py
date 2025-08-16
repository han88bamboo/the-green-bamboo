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
        # Debug: Print request details
        # print("Request method:", request.method)
        # print("Request headers:", dict(request.headers))
        # print("Request args:", dict(request.args))
        # print("Request JSON:", request.get_json())

        data = request.get_json()  # Expecting your JSON array
        venue_id = data.get("venueID")  # Extract venueID from the JSON data
        # data = data.get("updatedMenu")

        # print(f"Raw data: {data}")
        # print(f"Venue ID: {venue_id}")
        
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
        print(f"About to delete sections for venue_id: {venue_id}")
        cur.execute('DELETE FROM "venuesMenu" WHERE "venueId" = %s', (venue_id,))
        deleted_count = cur.rowcount
        print(f"Deleted {deleted_count} rows")
        
        # --- Insert/update top-level sections ---
        for section in menu_data:
            cur.execute("""
                INSERT INTO "venuesMenu" ("id", "sectionName", "sectionOrder", "venueId", "parentSectionId")
                VALUES (%s, %s, %s, NULL)
                ON CONFLICT ("id") DO UPDATE
                SET "sectionName" = EXCLUDED."sectionName",
                    "sectionOrder" = EXCLUDED."sectionOrder",
                    "venueId" = EXCLUDED."venueId";
            """, (
                # section.get("id"),
                section.get("sectionName"),
                section.get("sectionOrder"),
                venue_id
            ))

            # --- Insert/update sub-sections ---
            sub_sections = section.get("subSections", [])
            for idx, sub in enumerate(sub_sections):
                # Check if sub-section has an ID, otherwise let database generate one
                if sub.get("id"):
                    cur.execute("""
                        INSERT INTO "venuesMenu" ("id", "sectionName", "sectionOrder", "venueId", "parentSectionId")
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT ("id") DO UPDATE
                        SET "sectionName" = EXCLUDED."sectionName",
                            "sectionOrder" = EXCLUDED."sectionOrder",
                            "venueId" = EXCLUDED."venueId",
                            "parentSectionId" = EXCLUDED."parentSectionId";
                    """, (
                        # sub.get("id"),
                        sub.get("sectionName"),
                        idx,             # sub-section order
                        venue_id,
                        section.get("id")
                    ))
                else:
                    cur.execute("""
                        INSERT INTO "venuesMenu" ("sectionName", "sectionOrder", "venueId", "parentSectionId")
                        VALUES (%s, %s, %s, %s);
                    """, (
                        sub.get("sectionName"),
                        idx,             # sub-section order
                        venue_id,
                        section.get("id")
                    ))
        
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
