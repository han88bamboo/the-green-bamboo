import logging
import os
from psycopg2.extras import execute_values

from flask import Blueprint, g, request, jsonify
from psycopg2.extras import RealDictCursor # ADDED BY SMU GROUP 3

logger = logging.getLogger(__name__)

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
logger.info(project_root)

@blueprint.route("/", methods=['GET'])
def getVenues():
    conn = g.db
    """
    Cursor-based pagination endpoint for venues
    Query parameters:
    - cursor: cursor value (venue ID) for pagination
    - venueType: optional filter by venue type
    - venueMainType: optional filter by main type ID
    - venueSubType: optional filter by sub type ID
    """
    try:
        # Get query parameters
        cursor_id = request.args.get('cursor', type=int)
        venue_type = request.args.get('venueType', '', type=str)
        venue_main_type = request.args.get('venueMainType', type=int)
        venue_sub_type = request.args.get('venueSubType', type=int)
        min_rating = request.args.get('minRating', type=float)
        max_rating = request.args.get('maxRating', type=float)
        sort_by = request.args.get('sort', type=str)
        
        # Determine if this is the first load
        is_first_load = cursor_id is None
        limit = 20 if is_first_load else 10
        
        # Build dynamic WHERE clause
        where_conditions = []
        query_params = []
        
        # Add cursor condition for pagination
        if cursor_id:
            where_conditions.append('v.id < %s')
            query_params.append(cursor_id)
        
        # Add other filters
        if venue_type:
            where_conditions.append('v."venueType" = %s')
            query_params.append(venue_type)
        
        if venue_main_type:
            where_conditions.append('v."venueMainType" = %s')
            query_params.append(venue_main_type)
        
        if venue_sub_type:
            where_conditions.append('v."venueSubType" = %s')
            query_params.append(venue_sub_type)
        
        where_clause = f"WHERE {' AND '.join(where_conditions)}" if where_conditions else ""

        # Build dynamic HAVING clause for rating filters
        having_conditions = []
        if min_rating is not None:
            having_conditions.append('COALESCE(ROUND(AVG(vr.rating), 1), 0) >= %s')
            query_params.append(min_rating)
        
        if max_rating is not None:
            having_conditions.append('COALESCE(ROUND(AVG(vr.rating), 1), 0) <= %s')
            query_params.append(max_rating)
        
        having_clause = f"HAVING {' AND '.join(having_conditions)}" if having_conditions else ""

        # Determine order by clause
        order_by_clause = 'ORDER BY v.id DESC' # Default
        sort_map = {
            'Alphabetical (A - Z)': 'ORDER BY v."venueName" ASC',
            'Alphabetical (Z - A)': 'ORDER BY v."venueName" DESC',
            'Date (Newest - Oldest)': 'ORDER BY v."yearOpened" DESC, v.id DESC',
            'Date (Oldest - Newest)': 'ORDER BY v."yearOpened" ASC, v.id ASC',
            'Ratings (Highest - Lowest)': 'ORDER BY "averageRating" DESC, v.id DESC',
            'Ratings (Lowest - Highest)': 'ORDER BY "averageRating" ASC, v.id ASC'
        }
        if sort_by in sort_map:
            order_by_clause = sort_map[sort_by]

        # Query with one extra item to check if there are more results
        venues_query = f"""
            SELECT 
                v.id,
                v."venueName",
                v."address",
                v."venueType",
                v."originLocation",
                v."venueDesc",
                v."photo",
                v."claimStatus",
                v."yearOpened",
                v."openForReservations",
                v."website",
                v."instagram",
                v."facebook",
                v."tiktok",
                v."email",
                v."phoneNumber",
                v."whatsappNumber",
                vmt."venueMainType" AS "venueMainTypeName",
                vst."venueSubType" AS "venueSubTypeName",
                COALESCE(ROUND(AVG(vr.rating), 1), 0) AS "averageRating"
            FROM venues v
            LEFT JOIN "venueMainTypes" vmt ON v."venueMainType" = vmt.id
            LEFT JOIN "venueSubTypes" vst ON v."venueSubType" = vst.id
            LEFT JOIN "venueReviews" vr ON v.id = vr."venueID"
            {where_clause}
            GROUP BY 
                v.id,
                v."venueName",
                v."address",
                v."venueType",
                v."originLocation",
                v."venueDesc",
                v."photo",
                v."claimStatus",
                v."yearOpened",
                v."openForReservations",
                v."website",
                v."instagram",
                v."facebook",
                v."tiktok",
                v."email",
                v."phoneNumber",
                v."whatsappNumber",
                vmt."venueMainType",
                vst."venueSubType"
            {having_clause}
            {order_by_clause}
            LIMIT %s
        """
        
        # Add limit to query params (get one extra to check for next page)
        query_params.append(limit + 1)
        
        # Execute query
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(venues_query, query_params)
        venues = cursor.fetchall()
        cursor.close()
        
        # Check if there are more results
        has_next_page = len(venues) > limit
        if has_next_page:
            venues.pop()  # Remove the extra item
        
        # Get the next cursor (ID of the last item)
        next_cursor = venues[-1]['id'] if venues else None
        
        return jsonify({
            "success": True,
            "data": {
                "venues": venues,
                "pagination": {
                    "hasNextPage": has_next_page,
                    "nextCursor": next_cursor,
                    "itemsReturned": len(venues),
                    "isFirstLoad": is_first_load
                }
            }
        })
        
    except Exception as e:
        print(f"Error fetching venues: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "message": str(e)
        }), 500


@blueprint.route("/types", methods=['GET'])
def getVenueType():
    conn = g.db

    try: 
        query = """
        SELECT 
            COALESCE((
                SELECT json_agg(json_build_object(
                    'id', vmt.id,
                    'venueMainType', vmt."venueMainType"
                )) FROM "venueMainTypes" vmt
            ), '[]'::json) AS main_type,
            
            COALESCE((
                SELECT json_agg(json_build_object(
                    'id', vst.id,
                    'venueSubType', vst."venueSubType"
                )) FROM "venueSubTypes" vst
            ), '[]'::json) AS sub_type;
        """

        # open connection to execute sql query
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query)
            
            venue_types = cursor.fetchone()  # one row
            return jsonify(venue_types) 
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            "code": 500,
            "message": "An error occurred when getting venue types. " + str(e) 
        }), 500
