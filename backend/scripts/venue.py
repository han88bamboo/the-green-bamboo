import logging
import os
from psycopg2.extras import execute_values

from flask import Blueprint, g, request, jsonify
import logging
import os
from psycopg2.extras import execute_values

from flask import Blueprint, g, request, jsonify
from psycopg2.extras import RealDictCursor # ADDED BY SMU GROUP 3
from datetime import datetime
from urllib.request import urlopen
from scripts.pointsHelperFunc import *

logger = logging.getLogger(__name__)

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
logger.info(project_root)

@blueprint.route("/<int:venue_id>/reviews", methods=['GET'])
def getVenueReviews(venue_id: int):
    conn = g.db

    try:
        # Validate and sanitize inputs
        try:
            per_page = int(request.args.get("limit", 20))
            if per_page <= 0 or per_page > 100:  # Set reasonable limits
                return jsonify({"code": 400, "message": "Limit must be between 1 and 100"}), 400
        except ValueError:
            return jsonify({"code": 400, "message": "Invalid limit parameter"}), 400
        
        last_id = request.args.get("last_id", None)
        if last_id:
            try:
                last_id = int(last_id)
            except ValueError:
                return jsonify({"code": 400, "message": "Invalid last_id parameter"}), 400

        if last_id:
            query = """
            SELECT 
                r.id,
                r."userID",
                u."username",
                u."photo",
                r."rating",
                r."reviewDesc",
                r."createdDate",
                r."photos",
                pr."currentPoints"
            FROM "venueReviews" r
            LEFT JOIN "users" u ON u.id = r."userID"
            LEFT JOIN "pointsRecorder" pr ON pr."userID" = r."userID" AND pr."userType" = 'user'
            WHERE r."venueID" = %s AND r.id < %s
            ORDER BY r."createdDate" DESC
            LIMIT %s
            """
            params = (venue_id, int(last_id), per_page)
        else:
            query = """
            SELECT 
                r.id,
                r."userID",
                u."username",
                u."photo",
                r."rating",
                r."reviewDesc",
                r."createdDate",
                r."photos",
                pr."currentPoints"
            FROM "venueReviews" r
            LEFT JOIN "users" u ON u.id = r."userID"
            LEFT JOIN "pointsRecorder" pr ON pr."userID" = r."userID" AND pr."userType" = 'user'
            WHERE r."venueID" = %s
            ORDER BY r."createdDate" DESC
            LIMIT %s
            """
            params = (venue_id, per_page)

        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params)
            reviews = cursor.fetchall()

            # Debug: Check what we got
            print(f"Raw reviews data: {reviews}")
            print(f"First review type info: {type(reviews[0]) if reviews else 'No reviews'}")
            if reviews:
                for key, value in reviews[0].items():
                    print(f"  {key}: {type(value)} = {value}")

            stats_query = """
            SELECT
                COALESCE(AVG(rating), 0) as average_rating,
                COUNT(id) as total_reviews
            FROM "venueReviews"
            WHERE "venueID" = %s
            """
            cursor.execute(stats_query, (venue_id,))
            stats = cursor.fetchone()
            
            print(f"Stats data: {stats}")
            print(f"Average rating type: {type(stats['average_rating'])}")

        # Convert datetime objects to strings for JSON serialization and add user ranks
        serialized_reviews = []
        for review in reviews:
            serialized_review = dict(review)
            
            # Handle datetime serialization
            if 'createdDate' in serialized_review and serialized_review['createdDate']:
                serialized_review['createdDate'] = serialized_review['createdDate'].isoformat()
            
            # Handle photos if it's a string that needs parsing
            if 'photos' in serialized_review and serialized_review['photos']:
                # If photos is stored as JSON string, you might need to parse it
                # or ensure it's already in the right format
                pass
            
            # Add user rank information using the functions
            user_id = serialized_review.get('userID')
            current_points = serialized_review.get('currentPoints', 0)
            
            if user_id and current_points is not None:
                # Get rank using proof points (from the query result)
                rank_info = get_rank(current_points)
                serialized_review['proofRank'] = rank_info[0]  # Rank name with emoji
                serialized_review['rankColor'] = rank_info[1]  # Rank color
                serialized_review['proofPoints'] = current_points  # User's current points
                
                # Check if user has reached max proof points
                serialized_review['hasReachedMaxPoints'] = check_max_proof_points(user_id)
            else:
                # Fallback: get rank by user ID if points not available in query
                rank_info = get_rank_by_user_id(user_id) if user_id else None
                if rank_info:
                    serialized_review['proofRank'] = rank_info[0]
                    serialized_review['rankColor'] = rank_info[1]
                    serialized_review['hasReachedMaxPoints'] = check_max_proof_points(user_id)
                    # Get proof points separately for this case
                    conn_temp = g.db
                    cur_temp = conn_temp.cursor()
                    cur_temp.execute('SELECT "currentPoints" FROM "pointsRecorder" WHERE "userID" = %s AND "userType" = %s', (user_id, 'user'))
                    points_result = cur_temp.fetchone()
                    serialized_review['proofPoints'] = points_result['currentPoints'] if points_result else 0
                else:
                    serialized_review['proofRank'] = None
                    serialized_review['rankColor'] = None
                    serialized_review['proofPoints'] = 0
                    serialized_review['hasReachedMaxPoints'] = False
            
            # Remove currentPoints from the response as it's internal data
            serialized_review.pop('currentPoints', None)
            
            serialized_reviews.append(serialized_review)

        response_data = {
            "reviews": serialized_reviews,
            "average_rating": round(float(stats['average_rating']), 1),
            "total_reviews": stats['total_reviews']
        }
        
        print(f"Final response_data: {response_data}")
        return jsonify(response_data)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"code": 500, "message": "Error getting reviews"}), 500


@blueprint.route("/<int:venue_id>/bottle-reviews", methods=['GET'])
def getVenueBottleReviews(venue_id: int):
    conn = g.db
    try:
        # Validate and sanitize inputs
        try:
            per_page = int(request.args.get("limit", 10))
            if per_page <= 0 or per_page > 100:
                return jsonify({"code": 400, "message": "Limit must be between 1 and 100"}), 400
        except ValueError:
            return jsonify({"code": 400, "message": "Invalid limit parameter"}), 400
        
        last_id = request.args.get("last_id", None)
        if last_id:
            try:
                last_id = int(last_id)
            except ValueError:
                return jsonify({"code": 400, "message": "Invalid last_id parameter"}), 400

        if last_id:
            query = """
            SELECT
                r.id,
                r."userID",
                u.username,
                u.photo as "userPhoto",
                u.points as "userPoints",
                u.rank as "userRank",
                l."listingName" as "bottleName",
                r.rating,
                r."reviewDesc",
                r."createdDate",
                r.photo,
                r."listingID" as "reviewTarget"
            FROM reviews r
            JOIN users u ON r."userID" = u.id
            JOIN listings l ON r."reviewTarget" = l.id
            WHERE r."venueID" = %s AND r.id < %s
            ORDER BY r."createdDate" DESC
            LIMIT %s
            """
            params = (venue_id, last_id, per_page)
        else:
            query = """
            SELECT
                r.id,
                r."userID",
                u.username,
                u.photo as "userPhoto",
                u.points as "userPoints",
                u.rank as "userRank",
                l."listingName" as "bottleName",
                r.rating,
                r."reviewDesc",
                r."createdDate",
                r.photo,
                r."listingID" as "reviewTarget"
            FROM reviews r
            JOIN users u ON r."userID" = u.id
            JOIN listings l ON r."reviewTarget" = l.id
            WHERE r."venueID" = %s
            ORDER BY r."createdDate" DESC
            LIMIT %s
            """
            params = (venue_id, per_page)

        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params)
            reviews = cursor.fetchall()

            stats_query = """
            SELECT
                COALESCE(AVG(rating), 0) as average_rating,
                COUNT(id) as total_reviews
            FROM reviews
            WHERE "venueID" = %s
            """
            cursor.execute(stats_query, (venue_id,))
            stats = cursor.fetchone()

        serialized_reviews = []
        for review in reviews:
            serialized_review = dict(review)
            if 'createdDate' in serialized_review and serialized_review['createdDate']:
                serialized_review['createdDate'] = serialized_review['createdDate'].isoformat()
            serialized_reviews.append(serialized_review)

        response_data = {
            "reviews": serialized_reviews,
            "average_rating": round(float(stats['average_rating']), 1),
            "total_reviews": stats['total_reviews']
        }
        
        return jsonify(response_data)

    except Exception as e:
        logger.error(f"Error getting bottle reviews for venue {venue_id}: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"code": 500, "message": "Error getting bottle reviews"}), 500