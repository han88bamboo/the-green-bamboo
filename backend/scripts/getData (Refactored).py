
import os
import json
import random # ADDED BY SMU GROUP 3
import feedparser
import re
import requests
import hashlib
import traceback
from urllib.parse import unquote
from bs4 import BeautifulSoup
from flask import Blueprint, g, jsonify, request
from psycopg2.extras import RealDictCursor # ADDED BY SMU GROUP 3
from decimal import Decimal
from datetime import datetime, timezone, date, timedelta
from scripts import pointsHelperFunc
from scripts import pointsHelperFunc

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)


@blueprint.route("/getListingsByIDs", methods=['GET', 'POST'])
def getListingsByIDs():
    conn = g.db

    try:
        # Handle both GET and POST requests
        if request.method == 'POST':
            # For POST requests, get IDs from JSON body
            data = request.get_json()
            listing_ids = data.get('listingIDs', []) if data else []
        else:
            # For GET requests, get IDs from query parameters
            raw_ids = request.args.getlist('ids')
            listing_ids = [int(i) for i in raw_ids]

        if not listing_ids:
            return jsonify([]), 200

        # Ensure all IDs are integers
        listing_ids = [int(i) for i in listing_ids]

        sql = """
            SELECT l."id", l."listingName", l."drinkType", l."typeCategory",
                l."originCountry", l."bottler", l."photo", l."producerID",
                p."producerName"
            FROM listings l
            LEFT JOIN producers p ON l."producerID" = p."id"
            WHERE l."id" IN %s;
        """

        with conn.cursor() as cursor:
            cursor.execute(sql, (tuple(listing_ids),))
            rows = cursor.fetchall()

        result = [
            {
                "id": row["id"], 
                "listingName": row["listingName"], 
                "drinkType": row.get("drinkType", ""),
                "typeCategory": row.get("typeCategory", ""),
                "originCountry": row.get("originCountry", ""),
                "bottler": row.get("bottler", ""),
                "photo": row.get("photo", ""),
                "producerID": row.get("producerID", ""),
                "producerName": row.get("producerName", ""),
            } 
            for row in rows
        ]

        return jsonify(result), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# [GET] Get Listing names by dynamic search term
@blueprint.route("/getListingNamesDynamicSearch/<searchTerm>")
def getListingNamesDynamicSearch(searchTerm):
    conn = g.db
    cursor = conn.cursor()

    try:
        # Searches for listings by name, starting from the lastID
        cursor.execute(""" 
            SELECT 
                l."id", 
                l."listingName", 
                l."photo",
                p."producerName",
                l."drinkType",
                l."typeCategory",
                l."abv",
                l."originCountry",
                l."officialDesc",
                COALESCE((SELECT AVG(r."rating") FROM "reviews" r WHERE r."reviewTarget" = l."id"), 0) as "avgRating",
                (similarity(unaccent(l."listingName"), unaccent(%s)) + 3 * similarity(unaccent(p."producerName"), unaccent(%s))) AS combined_sim_score
            FROM "listings" l
            JOIN "producers" p ON l."producerID" = p."id"
            WHERE unaccent(l."listingName") %% unaccent(%s)
            
            UNION
            
            SELECT 
                l."id", 
                l."listingName", 
                l."photo",
                p."producerName",
                l."drinkType",
                l."typeCategory",
                l."abv",
                l."originCountry",
                l."officialDesc",
                COALESCE((SELECT AVG(r."rating") FROM "reviews" r WHERE r."reviewTarget" = l."id"), 0) as "avgRating",
                (similarity(unaccent(l."listingName"), unaccent(%s)) + 3 * similarity(unaccent(p."producerName"), unaccent(%s))) AS combined_sim_score
            FROM "listings" l
            JOIN "producers" p ON l."producerID" = p."id"
            WHERE unaccent(p."producerName") %% unaccent(%s)
            
            ORDER BY combined_sim_score DESC
            LIMIT 50
        """, (searchTerm, searchTerm, searchTerm, searchTerm, searchTerm, searchTerm))

        listings_data = cursor.fetchall()

        # Convert the fetched data to a list of dictionaries
        for listing in listings_data:
            listing_dict = {
                "id": listing["id"],
                "listingName": listing["listingName"],
                "producerName": listing["producerName"],
                "photo": listing["photo"],
                "drinkType": listing["drinkType"],
                "typeCategory": listing["typeCategory"],
                "abv": listing["abv"],
                "originCountry": listing["originCountry"],
                "officialDesc": listing["officialDesc"],
                "avgRating": listing["avgRating"],
                "similarity": listing["combined_sim_score"]
            }
            # Convert Decimal to float if necessary
            for key, value in listing_dict.items():
                if isinstance(value, Decimal):
                    listing_dict[key] = float(value)
            listing.update(listing_dict)

        if not listings_data:
            return jsonify([])

        return jsonify(listings_data)

    except Exception as e:
        print(f"Error fetching listing names by dynamic search: {str(e)}")
        return jsonify({"code": 500, "message": "An error occurred while fetching listing names."}), 500

# [GET] Get producer names by dynamic search term
@blueprint.route("/getProducerNamesDynamicSearch/<searchTerm>")
def getProducerNamesDynamicSearch(searchTerm):
    conn = g.db
    cursor = conn.cursor()

    try:
        # Searches for producers by name with similarity
        cursor.execute(""" 
            SELECT 
                p."id", 
                p."producerName",
                p."originCountry",
                p."photo",
                similarity(unaccent(p."producerName"), unaccent(%s)) AS sim_score
            FROM "producers" p
            WHERE unaccent(p."producerName") %% unaccent(%s)
            ORDER BY sim_score DESC
            LIMIT 20
        """, (searchTerm, searchTerm))

        producers_data = cursor.fetchall()

        # Convert the fetched data to a list of dictionaries
        for producer in producers_data:
            producer_dict = {
                "id": producer["id"],
                "producerName": producer["producerName"],
                "originCountry": producer["originCountry"],
                "photo": producer["photo"],
                "similarity": producer["sim_score"]
            }
            # Convert Decimal to float if necessary
            for key, value in producer_dict.items():
                if isinstance(value, Decimal):
                    producer_dict[key] = float(value)
            producer.update(producer_dict)

        if not producers_data:
            return jsonify([])

        return jsonify(producers_data)

    except Exception as e:
        print(f"Error in getProducerNamesDynamicSearch: {str(e)}")
        return jsonify({"code": 500, "message": "An error occurred while searching producers."}), 500

# [GET] Get Listing names by dynamic search term filtered by producer
@blueprint.route("/getListingNamesByProducer/<searchTerm>/<int:producerId>")
def getListingNamesByProducer(searchTerm, producerId):
    conn = g.db
    cursor = conn.cursor()

    try:

        # First, lower the similarity threshold to 0.15 for more permissive matching
        cursor.execute("SET pg_trgm.similarity_threshold = 0.15")

        # Searches for listings by name from a specific producer
        cursor.execute(""" 
            SELECT 
                l."id", 
                l."listingName", 
                l."photo",
                p."producerName",
                l."drinkType",
                l."typeCategory",
                l."abv",
                l."originCountry",
                l."officialDesc",
                COALESCE((SELECT AVG(r."rating") FROM "reviews" r WHERE r."reviewTarget" = l."id"), 0) as "avgRating",
                similarity(unaccent(l."listingName"), unaccent(%s)) AS sim_score
            FROM "listings" l
            JOIN "producers" p ON l."producerID" = p."id"
            WHERE l."producerID" = %s
            AND unaccent(l."listingName") %% unaccent(%s)
            ORDER BY sim_score DESC
            LIMIT 30
        """, (searchTerm, producerId, searchTerm))

        listings_data = cursor.fetchall()

        # Convert the fetched data to a list of dictionaries
        for listing in listings_data:
            listing_dict = {
                "id": listing["id"],
                "listingName": listing["listingName"],
                "producerName": listing["producerName"],
                "photo": listing["photo"],
                "drinkType": listing["drinkType"],
                "typeCategory": listing["typeCategory"],
                "abv": listing["abv"],
                "originCountry": listing["originCountry"],
                "officialDesc": listing["officialDesc"],
                "avgRating": listing["avgRating"],
                "similarity": listing["sim_score"]
            }
            # Convert Decimal to float if necessary
            for key, value in listing_dict.items():
                if isinstance(value, Decimal):
                    listing_dict[key] = float(value)
            listing.update(listing_dict)

        if not listings_data:
            return jsonify([])

        return jsonify(listings_data)

    except Exception as e:
        print(f"Error in getListingNamesByProducer: {str(e)}")
        return jsonify({"code": 500, "message": "An error occurred while searching listings by producer."}), 500
    finally:
        # Make sure to reset the threshold back to default (0.3)
        # This will run even if there's an exception in the try block
        try:
            cursor.execute("SET pg_trgm.similarity_threshold TO DEFAULT")
        except:
            pass  # Ignore any errors during cleanup

# [GET] Specific Producer
@blueprint.route("/getProducer/<int:id>")
def getProducer(id):
    conn = g.db
    cur = conn.cursor()

    try:
        # Query to get a specific producer and related data
        query = """
            SELECT 
                p.id, p."producerName", p."producerDesc", p."originCountry", p."mainDrinks", p.photo, 
                p."claimStatus", p."statusOB", p.username, p."producerLink", 
                p."yearFounded", p."activeStatus", p.owner, p.location, p."openForTours", p.website,
                p."stripeCustomerId", p."claimStatusCheckDate", p."isIndependentBottler",
                COALESCE((
                    SELECT json_agg(json_build_object(
                        'id', qa.id,
                        'question', qa.question,
                        'answer', qa.answer,
                        'date', qa.date,
                        'userId', qa."userId",
                        'producerId', qa."producerId"
                    ))
                    FROM "producersQuestionAnswers" qa
                    WHERE qa."producerId" = p.id
                ), '[]') AS "questionsAnswers",
                COALESCE((
                    SELECT row_to_json(oh)
                    FROM "producersOpeningHours" oh
                    WHERE oh."producerId" = p.id
                ), '{}'::json) AS "openingHours",
                COALESCE((
                    SELECT json_agg(json_build_object(
                        'id', u.id,
                        'date', u.date,
                        'text', u.text,
                        'photo', u.photo,
                        'producerId', u."producerId",
                        'likes', COALESCE((
                            SELECT json_agg(json_build_object('userId', l."userId", 'userType', l."userType"))
                            FROM "producerUpdateLikes" l
                            WHERE l."updateId" = u.id
                        ), '[]')
                    ))
                    FROM "producersUpdates" u
                    WHERE u."producerId" = p.id
                ), '[]') AS updates
            FROM producers p
            WHERE p.id = %s
        """

        cur.execute(query, (id,))
        producer_data = cur.fetchone()

        if producer_data is None:
            return jsonify({"message": "Producer not found"}), 404

        producer = dict(producer_data)
        producer['questionsAnswers'] = producer['questionsAnswers'] if producer['questionsAnswers'] else []
        producer['openingHours'] = producer['openingHours'] if producer['openingHours'] else {}
        producer['updates'] = producer['updates'] if producer['updates'] else []

        return jsonify(producer), 200

    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred retrieving the producer."
            }
        ), 500

    finally:
        cur.close()

# [GET] Get average rating for a specific listing based on reviews
@blueprint.route("/getListingReviewsRating/<listing_id>")
def getListingReviewsRating(listing_id):
    conn = g.db
    cursor = conn.cursor()

    if listing_id is None:
        return jsonify({
            "code": 400,
            "message": "Listing ID is required."
        }), 400

    try:
        # Fetch the average rating for the listing
        cursor.execute("""
            SELECT AVG("rating") AS "averageRating"
            FROM "reviews"
            WHERE "reviewTarget" = %s AND "reviewType" = 'Listing'
        """, (listing_id,))

        avg_rating = cursor.fetchone()

        if avg_rating is None or avg_rating['averageRating'] is None:
            return jsonify({
                "code": 200,
                "averageRating": "-",
                "reviewCount": 0
            }), 200
        
        # Fetch the number of reviews for the listing
        cursor.execute("""
            SELECT COUNT(*) AS "reviewCount"
            FROM "reviews"
            WHERE "reviewTarget" = %s AND "reviewType" = 'Listing'
        """, (listing_id,))
        review_count = cursor.fetchone()

        return jsonify({
            "code": 200,
            "averageRating": round(avg_rating['averageRating'], 1),
            "reviewCount": review_count['reviewCount'] or 0
        }), 200
    
    except Exception as e:
        print(f"Error fetching average rating for listing {listing_id}: {str(e)}")
        return jsonify({
            "code": 500,
            "message": "An error occurred while fetching the average rating."
        }), 500


# # =======================================================

# # -----------------------------------------------------------------------------------------

# # ================== POSTGRESQL FORMAT ==================

# # ----------------------
# # [OLD] TO BE DELETED:
# ----------------------

# [GET] Venues
@blueprint.route("/getVenues")
def getVenues():
    conn = g.db
    cur = conn.cursor()

    try:
        # Query to get venues and related data
        query = """
            SELECT 
                v.id, v.address, v."claimStatus", v."hashedPassword", v."venueName", v."venueDesc", 
                v."originLocation", v.photo, v."publicHolidays", v."reservationDetails", v."claimStatusCheckDate",
                v."yearOpened", v."openForReservations", v.website,
                v.username, v."venueType", v."stripeCustomerId", v.pin,
                -- Build the menu JSON
                COALESCE((
                    SELECT json_agg(json_build_object(
                        'sectionOrder',vm."sectionOrder",
                        'sectionName', vm."sectionName",
                        'sectionId', vm.id,
                        'sectionMenu', COALESCE((
                            SELECT json_agg(json_build_object(
                                'itemOrder', mi."itemOrder",
                                'itemPrice', mi."itemPrice",
                                'itemAvailability', mi."itemAvailability",
                                'itemID', mi."itemID",
                                'itemServingType', mi."itemServingType"
                            ) ORDER BY mi."itemOrder")
                            FROM "menuItems" mi
                            WHERE mi."sectionId" = vm.id
                        ), '[]')
                    ) ORDER BY vm."sectionOrder")
                    FROM "venuesMenu" vm
                    WHERE vm."venueId" = v.id
                ), '[]') AS menu,
                -- Build openingHours JSON
                COALESCE((
                    SELECT row_to_json(oh)
                    FROM "venuesOpeningHours" oh
                    WHERE oh."venueId" = v.id
                ), '{}'::json) AS "openingHours",
                -- Build questionsAnswers JSON
                COALESCE((
                    SELECT json_agg(json_build_object(
                        'id', qa.id,
                        'question', qa.question,
                        'answer', qa.answer,
                        'date', qa.date,
                        'userId', qa."userId"
                    ))
                    FROM "venuesQuestionAnswers" qa
                    WHERE qa."venueId" = v.id
                ), '[]') AS "questionsAnswers",
                -- Build updates JSON
                COALESCE((
                    SELECT json_agg(json_build_object(
                        'id', u.id,
                        'date', u.date,
                        'text', u.text,
                        'photo', u.photo,
                        'venueId', u."venueId",
                        'likes', COALESCE((
                            SELECT json_agg(json_build_object('userId', l."userId", 'userType', l."userType"))
                            FROM "venueUpdateLikes" l
                            WHERE l."updateId" = u.id
                        ), '[]')
                    ) ORDER BY u.date DESC)
                    FROM "venuesUpdates" u
                    WHERE u."venueId" = v.id
                ), '[]') AS updates
            FROM venues v
            ORDER BY v.id
        """

        cur.execute(query)
        venues_data = cur.fetchall()

        if not venues_data:
            return jsonify([])

        venues_list = []
        for row in venues_data:
            venue = dict(row)
            venue['menu'] = venue['menu'] if venue['menu'] else []
            venue['openingHours'] = venue['openingHours'] if venue['openingHours'] else {}
            venue['questionsAnswers'] = venue['questionsAnswers'] if venue['questionsAnswers'] else []
            venue['updates'] = venue['updates'] if venue['updates'] else []
            venues_list.append(venue)

        return jsonify(venues_list), 200

    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred retrieving venues."
            }
        ), 500

    finally:
        cur.close()


# [GET] Get venues by IDs
@blueprint.route("/getVenuesByIds", methods=['POST'])
def getVenuesByIds():
    conn = g.db
    venue_ids = request.json.get('venueIDs', [])

    if not venue_ids or len(venue_ids) == 0:
        return jsonify({
            "code": 404,
            "message": "At least one venue ID is required."
        }), 404

    try:
        with conn.cursor() as cursor:
            # Retrieve venue information based on the provided IDs
            cursor.execute('SELECT * FROM "venues" WHERE "id" IN %s', (tuple(venue_ids),))
            venues_data = cursor.fetchall()

            if not venues_data:
                return jsonify([]), 404
            
            venues_list = []
            for row in venues_data:
                venue = {
                "id": row["id"],
                "venueName": row["venueName"],
                "originLocation": row["originLocation"],
                "photo": row["photo"],
                "website": row["website"],
                "address": row["address"]
                }
                venues_list.append(venue)

        return jsonify(venues_list), 200

    except Exception as e:
        print(str(e))
        return jsonify({"code": 500, "message": "An error occurred while fetching venues by IDs."}), 500

# [GET] Specific Venue
@blueprint.route("/venue/<id>")
def venue(id):
    conn = g.db
    cur = conn.cursor()

    try:
        # Query to get a specific venue and related data
        query = """
            SELECT 
                v.id, v.address, v."claimStatus", v."venueName", v."venueDesc", 
                v."originLocation", v.photo, v."publicHolidays", v."reservationDetails", v."claimStatusCheckDate",
                v."yearOpened", v."openForReservations", v.website, v.instagram, v.facebook, v.tiktok, 
                v.email, v."phoneNumber", v."whatsappNumber",
                v.username, v."venueType", 
                -- Build amenities JSON
                COALESCE((
                    SELECT row_to_json(va)
                    FROM "venueAmenities" va
                    WHERE va."venueId" = v.id
                ), '{}'::json) AS amenities,
                -- Build openingHours JSON
                COALESCE((
                    SELECT row_to_json(oh)
                    FROM "venuesOpeningHours" oh
                    WHERE oh."venueId" = v.id
                ), '{}'::json) AS "openingHours",
                -- Build questionsAnswers JSON
                COALESCE((
                    SELECT json_agg(json_build_object(
                        'id', qa.id,
                        'question', qa.question,
                        'answer', qa.answer,
                        'date', qa.date,
                        'userId', qa."userId"
                    ))
                    FROM "venuesQuestionAnswers" qa
                    WHERE qa."venueId" = v.id
                ), '[]') AS "questionsAnswers"
            FROM venues v
            WHERE v.id = %s
            GROUP BY v.id
        """

        cur.execute(query, (id,))
        venue_data = cur.fetchone()

        if venue_data is None:
            return jsonify({"message": "Venue not found"}), 404

        venue = dict(venue_data)
        # venue['menu'] = venue['menu'] if venue['menu'] else []
        venue['amenities'] = venue['amenities'] if venue['amenities'] else {}
        venue['openingHours'] = venue['openingHours'] if venue['openingHours'] else {}
        venue['questionsAnswers'] = venue['questionsAnswers'] if venue['questionsAnswers'] else []
        # venue['updates'] = venue['updates'] if venue['updates'] else []

        return jsonify(venue), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred retrieving the venue."
            }
        ), 500

    finally:
        cur.close()


# [GET] Specific Venue
@blueprint.route("/getVenueMenu/<section_id>")
def getVenueMenu(section_id):
    """Optimized version with performance improvements and better error handling"""
    
    # Input validation
    if not section_id:
        return jsonify({"code": 400, "message": "Menu category is mandatory."}), 400
    
    # Parse and validate query parameters
    try:
        page = max(1, int(request.args.get("page", 1)))
        limit = min(100, max(1, int(request.args.get("limit", 20))))  # Cap at 100
        search = request.args.get("search", "").strip()
    except ValueError:
        return jsonify({"code": 400, "message": "Invalid pagination parameters"}), 400
    
    offset = (page - 1) * limit
    
    conn = g.db
    cur = conn.cursor()
    
    try:
        # Build WHERE conditions (use proper parameterization)
        where_conditions = ['"sectionId" = %s']
        params = [section_id]
        
        if search:
            # Search across multiple fields for better UX
            where_conditions.append('(LOWER(mi."variant") LIKE %s OR LOWER(mi."itemID") LIKE %s)')
            search_param = f"%{search.lower()}%"
            params.extend([search_param, search_param])
        
        where_clause = " AND ".join(where_conditions)
        
        # Use a single query with window function for better performance
        # This eliminates the need for a separate COUNT query
        # sql = f"""
        #     SELECT 
        #         mi."id", mi."sectionId", mi."itemID", mi."itemOrder", lst."listingName", lst."photo", 
        #         lst."bottler", lst."drinkType", lst."abv", mi."itemPrice", mi."itemAvailability", 
        #         mi."itemServingType", srvTyp."servingType", mi."variant", COUNT(*) OVER() as total_count
        #     FROM "menuItems" mi
        #     INNER JOIN "listings" lst
        #         ON mi."itemID" = lst."id"
        #     LEFT JOIN "servingTypes" srvTyp
        #         ON mi."itemServingType" = srvTyp."id"
        #     WHERE {where_clause}
        #     ORDER BY mi."itemOrder" ASC -- , mi."id" ASC  Add secondary sort for consistency
        #     LIMIT %s OFFSET %s;
        # """
        sql = f"""
            SELECT 
                mi."id", 
                mi."sectionId", 
                mi."itemID", 
                mi."itemOrder", 
                lst."listingName", 
                lst."photo", 
                lst."bottler", 
                lst."drinkType", 
                lst."abv", 
                mi."itemPrice", 
                mi."itemAvailability", 
                mi."itemServingType", 
                srvTyp."servingType", 
                mi."variant", 
                COALESCE(ROUND(AVG(r."rating"), 1), 0) as "averageRating",
                COUNT(r."rating") as "reviewCount",
                COUNT(*) OVER() as total_count
            FROM "menuItems" mi
            INNER JOIN "listings" lst
                ON mi."itemID" = lst."id"
            LEFT JOIN "servingTypes" srvTyp
                ON mi."itemServingType" = srvTyp."id"
            LEFT JOIN "reviews" r
                ON lst."id" = r."reviewTarget"
            WHERE {where_clause}
            GROUP BY 
                mi."id", 
                mi."sectionId", 
                mi."itemID", 
                mi."itemOrder", 
                lst."listingName", 
                lst."photo", 
                lst."bottler", 
                lst."drinkType", 
                lst."abv", 
                mi."itemPrice", 
                mi."itemAvailability", 
                mi."itemServingType", 
                srvTyp."servingType", 
                mi."variant"
            ORDER BY mi."itemOrder" ASC
            LIMIT %s OFFSET %s;
        """
        
        cur.execute(sql, params + [limit, offset])
        rows = cur.fetchall()
        
        if not rows:
            total_items = 0
            menu_items = []
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
                    "itemAvailability": row['itemAvailability'],
                    "variant": row['variant'],
                    "servingType": row['itemServingType'],
                    "servingTypeText": row['servingType'],
                    "itemPrice": float(row['itemPrice']) if row['itemPrice'] is not None else None,
                    "averageRating": row['averageRating'],
                }
                for row in rows
            ]
        
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
        
    except Exception as e:
        # # Log the actual error for debugging
        # import logging
        # logging.error(f"Database error in get_menu_items: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Return generic error to client
        return jsonify({
            "code": 500,
            "message": "An error occurred retrieving menu items."
        }), 500
        
    finally:
        if cur:
            cur.close()


# [GET] Specific Venue Menu by Search Term
@blueprint.route("/getVenueMenuBySearch/<venue_id>")
def getVenueMenuBySearch(venue_id):
    """Get all menu items for a venue by search term, preserving menu structure."""
    
    search_term = request.args.get("searchTerm", "").strip()

    if not search_term:
        return jsonify({"menu": []})

    # Add this debug check
    if not hasattr(g, 'db') or g.db is None:
        print("ERROR: No database connection available")
        return jsonify({"code": 500, "message": "Database connection error"}), 500

    conn = g.db
    cur = conn.cursor()

    try:
        # Get all sections for the venue first
        cur.execute('SELECT id, "sectionName", "sectionOrder", "parentSectionId" FROM "venuesMenu" WHERE "venueId" = %s ORDER BY "sectionOrder"', (venue_id,))
        all_sections_rows = cur.fetchall()
        
        sections = {s['id']: {**s, 'sectionMenu': [], 'subSections': [], 'isExpanded': True} for s in all_sections_rows if not s['parentSectionId']}
        subsections = {s['id']: {**s, 'sectionMenu': [], 'isExpanded': True} for s in all_sections_rows if s['parentSectionId']}

        # Get all matching menu items
        sql = '''
            SELECT 
                mi."sectionId",
                mi.id AS "menuItemId",
                mi."itemID",
                mi."itemOrder",
                l."listingName",
                l.photo,
                l.bottler,
                l."drinkType",
                l.abv,
                mi."itemPrice",
                mi."itemAvailability",
                mi."itemServingType",
                st."servingType",
                mi.variant
            FROM "menuItems" mi
            JOIN "venuesMenu" vm ON mi."sectionId" = vm.id
            JOIN listings l ON mi."itemID" = l.id
            LEFT JOIN "servingTypes" st ON mi."itemServingType" = st.id
            WHERE vm."venueId" = %s AND (
                LOWER(l."listingName") LIKE %s OR
                LOWER(l."drinkType") LIKE %s
            )
        '''
        search_like = f"%{search_term.lower()}%"
        cur.execute(sql, (venue_id, search_like, search_like))
        
        rows = cur.fetchall()

        for row in rows:
            item = {
                "id": row['menuItemId'],
                "sectionId": row['sectionId'],
                "itemID": row['itemID'],
                "itemOrder": row['itemOrder'],
                "name": row['listingName'],
                "photo": row['photo'],
                "bottler": row['bottler'],
                "drinkType": row['drinkType'],
                "abv": row['abv'],
                "itemAvailability": row['itemAvailability'],
                "variant": row['variant'],
                "servingType": row['itemServingType'],
                "servingTypeText": row['servingType'],
                "itemPrice": float(row['itemPrice']) if row['itemPrice'] is not None else None,
            }
            if row['sectionId'] in subsections:
                subsections[row['sectionId']]['sectionMenu'].append(item)
            elif row['sectionId'] in sections:
                sections[row['sectionId']]['sectionMenu'].append(item)

        # Assemble the final menu
        final_menu = []
        for sec_id, sec_data in sections.items():
            for sub_id, sub_data in subsections.items():
                if sub_data['parentSectionId'] == sec_id:
                    if sub_data['sectionMenu']: # Only add subsection if it has items
                        sec_data['subSections'].append(sub_data)
            
            if sec_data['sectionMenu'] or sec_data['subSections']: # Only add section if it has items or subsections with items
                final_menu.append(sec_data)
        
        return jsonify({"menu": final_menu})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"code": 500, "message": "An error occurred retrieving menu items."}), 500
    finally:
        if cur:
            cur.close()

# [GET] Specific Venue
@blueprint.route("/getVenue/<id>")
def getVenue(id):
    conn = g.db
    cur = conn.cursor()

    try:
        # Query to get a specific venue and related data
        query = """
            SELECT 
                v.id, v.address, v."claimStatus", v."venueName", v."venueDesc", 
                v."originLocation", v.photo, v."publicHolidays", v."reservationDetails", v."claimStatusCheckDate",
                v."yearOpened", v."openForReservations", v.website, v.instagram, v.facebook, v.tiktok, 
                v.email, v."phoneNumber", v."whatsappNumber", v."pdfMenuUrl",
                v.username, v."venueType", v."stripeCustomerId", v.pin,
                -- Build amenities JSON
                COALESCE((
                    SELECT row_to_json(va)
                    FROM "venueAmenities" va
                    WHERE va."venueId" = v.id
                ), '{}'::json) AS amenities,
                -- Build the menu JSON
                COALESCE((
                    SELECT json_agg(json_build_object(
                        'sectionOrder', vm."sectionOrder",
                        'sectionName', vm."sectionName",
                        'sectionId', vm.id,
                        'sectionMenu', COALESCE((
                            SELECT json_agg(json_build_object(
                                'itemOrder', mi."itemOrder",
                                'itemVintage', mi."variant",
                                'itemPrice', mi."itemPrice",
                                'itemAvailability', mi."itemAvailability",
                                'itemID', mi."itemID",
                                'itemServingType', mi."itemServingType"
                            ) ORDER BY mi."itemOrder")
                            FROM "menuItems" mi
                            WHERE mi."sectionId" = vm.id
                        ), '[]')
                    ) ORDER BY vm."sectionOrder")
                    FROM "venuesMenu" vm
                    WHERE vm."venueId" = v.id
                ), '[]') AS menu,
                -- Build openingHours JSON
                COALESCE((
                    SELECT row_to_json(oh)
                    FROM "venuesOpeningHours" oh
                    WHERE oh."venueId" = v.id
                ), '{}'::json) AS "openingHours",
                -- Build questionsAnswers JSON
                COALESCE((
                    SELECT json_agg(json_build_object(
                        'id', qa.id,
                        'question', qa.question,
                        'answer', qa.answer,
                        'date', qa.date,
                        'userId', qa."userId"
                    ))
                    FROM "venuesQuestionAnswers" qa
                    WHERE qa."venueId" = v.id
                ), '[]') AS "questionsAnswers",
                -- Build updates JSON
                COALESCE((
                    SELECT json_agg(json_build_object(
                        'id', u.id,
                        'date', u.date,
                        'text', u.text,
                        'photo', u.photo,
                        'venueId', u."venueId",
                        'likes', COALESCE((
                            SELECT json_agg(json_build_object('userId', l."userId", 'userType', l."userType"))
                            FROM "venueUpdateLikes" l
                            WHERE l."updateId" = u.id
                        ), '[]')
                    ) ORDER BY u.date DESC)
                    FROM "venuesUpdates" u
                    WHERE u."venueId" = v.id
                ), '[]') AS updates
            FROM venues v
            WHERE v.id = %s
            GROUP BY v.id
        """

        cur.execute(query, (id,))
        venue_data = cur.fetchone()

        if venue_data is None:
            return jsonify({"message": "Venue not found"}), 404

        venue = dict(venue_data)
        venue['menu'] = venue['menu'] if venue['menu'] else []
        venue['openingHours'] = venue['openingHours'] if venue['openingHours'] else {}
        venue['questionsAnswers'] = venue['questionsAnswers'] if venue['questionsAnswers'] else []
        venue['updates'] = venue['updates'] if venue['updates'] else []
        venue['amenities'] = venue['amenities'] if venue['amenities'] else {}

        return jsonify(venue), 200

    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred retrieving the venue."
            }
        ), 500

    finally:
        cur.close()

# [GET] Specific Producer
@blueprint.route("/getVenueByRequestId/<id>")
def getVenueByRequestId(id):
    conn = g.db
    cur = conn.cursor()

    try:
        # Query to get a specific venue by requestId and related data
        query = """
            SELECT 
                v.id, v.address, v."claimStatus", v."hashedPassword", v."venueName", v."venueDesc", 
                v."originLocation", v.photo, v."publicHolidays", v."reservationDetails", v."claimStatusCheckDate",
                v."yearOpened", v."openForReservations", v.website,
                v.username, v."venueType", v."stripeCustomerId", v.pin,
                -- Build the menu JSON
                COALESCE((
                    SELECT json_agg(json_build_object(
                        'sectionOrder', vm."sectionOrder",
                        'sectionName', vm."sectionName",
                        'sectionId', vm.id,
                        'sectionMenu', COALESCE((
                            SELECT json_agg(json_build_object(
                                'itemOrder', mi."itemOrder",
                                'itemPrice', mi."itemPrice",
                                'itemAvailability', mi."itemAvailability",
                                'itemID', mi."itemID",
                                'itemServingType', mi."itemServingType"
                            ) ORDER BY mi."itemOrder")
                            FROM "menuItems" mi
                            WHERE mi."sectionId" = vm.id
                        ), '[]')
                    ) ORDER BY vm."sectionOrder")
                    FROM "venuesMenu" vm
                    WHERE vm."venueId" = v.id
                ), '[]') AS menu,
                -- Build openingHours JSON
                COALESCE((
                    SELECT row_to_json(oh)
                    FROM "venuesOpeningHours" oh
                    WHERE oh."venueId" = v.id
                ), '{}'::json) AS "openingHours",
                -- Build questionsAnswers JSON
                COALESCE((
                    SELECT json_agg(json_build_object(
                        'id', qa.id,
                        'question', qa.question,
                        'answer', qa.answer,
                        'date', qa.date,
                        'userId', qa."userId"
                    ))
                    FROM "venuesQuestionAnswers" qa
                    WHERE qa."venueId" = v.id
                ), '[]') AS "questionsAnswers",
                -- Build updates JSON
                COALESCE((
                    SELECT json_agg(json_build_object(
                        'id', u.id,
                        'date', u.date,
                        'text', u.text,
                        'photo', u.photo,
                        'venueId', u."venueId",
                        'likes', COALESCE((
                            SELECT json_agg(json_build_object('userId', l."userId", 'userType', l."userType"))
                            FROM "venueUpdateLikes" l
                            WHERE l."updateId" = u.id
                        ), '[]')
                    ) ORDER BY u.date DESC)
                    FROM "venuesUpdates" u
                    WHERE u."venueId" = v.id
                ), '[]') AS updates
            FROM venues v
            WHERE v.id = %s
            GROUP BY v.id
        """

        cur.execute(query, (id,))
        venue_data = cur.fetchone()

        if venue_data is None:
            return jsonify({"message": "Venue not found"}), 404

        venue = dict(venue_data)
        venue['menu'] = venue['menu'] if venue['menu'] else []
        venue['openingHours'] = venue['openingHours'] if venue['openingHours'] else {}
        venue['questionsAnswers'] = venue['questionsAnswers'] if venue['questionsAnswers'] else []
        venue['updates'] = venue['updates'] if venue['updates'] else []

        return jsonify(venue), 200
    
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred retrieving the venue."
            }
        ), 500
    
    finally:
        cur.close()

# -----------------------------------------------------------------------------------------
# [GET] Specific Listing
@blueprint.route("/getListing/<id>")
def getListing(id):
    conn = g.db

    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM "listings" WHERE "id" = %s', (id,))
        listing_data = cursor.fetchone()

    if listing_data is None:
        return jsonify([])
    
    return jsonify(listing_data)




