import logging
import os
from psycopg2.extras import execute_values

from flask import Blueprint, g, request, jsonify
from psycopg2.extras import RealDictCursor # ADDED BY SMU GROUP 3
from datetime import datetime
from urllib.request import urlopen

logger = logging.getLogger(__name__)

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
logger.info(project_root)

@blueprint.route("/<int:venue_id>/reviews", methods=['GET'])
def getVenueReviews(venue_id: int):
    conn = g.db

    try:
        per_page = int(request.args.get("limit", 20))
        last_id = request.args.get("last_id", None)

        query = """
        SELECT 
            r.id,
            r."userID",
            u.username,
            r."rating",
            r."reviewDesc",
            r."createdDate",
            r."photos"
        FROM "venueReviews" r
        LEFT JOIN "users" u ON u.id = r."userID"
        WHERE r."venueID" = %s
        {filter}
        ORDER BY r."createdDate" DESC
        LIMIT %s
        """.format(
            filter="AND r.id < %s" if last_id else ""
        )

        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            params = (venue_id, per_page) if not last_id else (venue_id, last_id, per_page)
            cursor.execute(query, params)
            rows = cursor.fetchall()

        return jsonify(rows)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"code": 500, "message": "Error getting reviews"}), 500