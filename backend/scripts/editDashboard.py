# Port: 5000
# Routes: /editTop3 (POST)
# -----------------------------------------------------------------------------------------

import os
from flask import Blueprint, g, jsonify, request
from psycopg2.extras import RealDictCursor

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

# -----------------------------------------------------------------------------------------

# Helper function to update database 
def update_user_listings(cursor, user_id, category_name, selected_listings, selected_drink_ids):
    # Step 1: Get current values
    cursor.execute(f'SELECT "{category_name}" FROM "users" WHERE "id" = %s', (user_id,))
    result = cursor.fetchone()
    current_listings = result[category_name] if result and result[category_name] else []


    # Step 2: If same, do nothing
    if set(current_listings) == set(selected_listings):
        return True  # No changes needed

    # Step 3: Remove old entries if any
    for drink in current_listings:
        success = remove_listing_from_table(cursor, category_name, drink)
        if not success:
            return {"error": f"Error removing old {category_name}"}

    # Step 4: If new selection is empty, stop here
    if len(selected_listings) == 0:
        return True

    # Step 5: Add new entries
    cursor.execute('''
        SELECT "id", "listingName", "drinkType", "typeCategory"
        FROM "listings"
        WHERE "id" IN %s
    ''', (tuple(selected_drink_ids),))
    new_items = cursor.fetchall()

    for drink in new_items:
        success = add_listing_to_table(cursor, category_name, drink['id'], drink['listingName'], drink['drinkType'], drink['typeCategory'])
        if not success:
            return {"error": f"Error adding new {category_name}"}

    return True


# Helper function to check if listing exists in the specified table
# if listing exists, add 1 to the counter 
# else, add the listing to the table with a counter of 1
def add_listing_to_table(cursor, table_name, listing_id, listing_name, drink_type, type_category):

    try:

        # Check if the listing already exists in the table
        cursor.execute(f'SELECT * FROM "{table_name}" WHERE "listingID" = %s', (listing_id,))
        existing_listing = cursor.fetchone()

        if existing_listing:
            # If it exists, increment the counter
            cursor.execute(f'''
                UPDATE "{table_name}" 
                SET "counter" = "counter" + 1 
                WHERE "listingID" = %s
            ''', (listing_id,))
        else:
            # If it doesn't exist, insert a new record with a counter of 1
            cursor.execute(f'''
                INSERT INTO "{table_name}" ("listingID", "listingName", "drinkType", "typeCategory", "counter") 
                VALUES (%s, %s, %s, %s, 1)
            ''', (listing_id, listing_name, drink_type, type_category))
    
        # Commit the changes
        g.db.commit()

        # Return True to indicate success
        return True
    
    except Exception as e:
        g.db.rollback()

        print(f"Error adding listing to {table_name}: {e}")
        # Return False to indicate failure
        return False


# Helper function to remove listing from the specified table
def remove_listing_from_table(cursor, table_name, listing_name):
    try:
        # Check if the listing exists in the table
        cursor.execute(f'SELECT * FROM "{table_name}" WHERE "listingName" = %s', (listing_name,))
        existing_listing = cursor.fetchone()

        if existing_listing:
            # If it exists, decrement the counter
            cursor.execute(f'''
                UPDATE "{table_name}" 
                SET "counter" = "counter" - 1 
                WHERE "listingName" = %s
            ''', (listing_name,))
            
            # If the counter reaches 0, delete the listing from the table
            cursor.execute(f'''
                DELETE FROM "{table_name}" 
                WHERE "listingName" = %s AND "counter" <= 0
            ''', (listing_name,))
        
        # Commit the changes
        g.db.commit()

        # Return True to indicate success
        return True
    
    except Exception as e:
        g.db.rollback()

        print(f"Error removing listing from {table_name}: {e}")
        # Return False to indicate failure
        return False



# Helper function to get top 5 Grails, Up & Coming, and GOATs
def fetch_top_5(cursor, table, drink_type=None, type_category=None):

    if drink_type in ['Whisky', 'Whiskey']:
        drink_type = ['Whisky', 'Whiskey']  

    
    # If drink_type is a string, convert it to a list
    if isinstance(drink_type, str):
        drink_type = [drink_type]

    try:
        if drink_type and drink_type != "Show All Types":
            # If only drink type is provided, filter by drink type
            if type_category == "Show All":
                cursor.execute(f'''
                    SELECT "listingID", "listingName", "drinkType", "typeCategory", "counter"
                    FROM "{table}"
                    WHERE "drinkType" IN %s
                    ORDER BY "counter" DESC
                    LIMIT 5
                ''', (tuple(drink_type),))
            else:
                # If a specific type category is provided, filter by both drink type and type category
                cursor.execute(f'''
                    SELECT "listingID", "listingName", "drinkType", "typeCategory", "counter"
                    FROM "{table}"
                    WHERE "drinkType" IN %s AND "typeCategory" = %s
                    ORDER BY "counter" DESC
                    LIMIT 5
                ''', (tuple(drink_type), type_category,))
        else:
            # If drink type is Show All Types, fetch top 5 without filtering by drink type
            cursor.execute(f'''
                SELECT "listingID", "listingName", "drinkType", "typeCategory", "counter"
                FROM "{table}"
                ORDER BY "counter" DESC
                LIMIT 5
            ''')
        rows = cursor.fetchall()
        
        # Loop through the rows and get the rating for each listing
        for row in rows:

            # Get the listing details
            cursor.execute('''
                SELECT "producerID", photo
                FROM listings
                WHERE listings.id = %s
            ''', (row['listingID'],))

            listing_details = cursor.fetchone()
             

            row['producerID'] = listing_details['producerID'] if listing_details else None
            row['photo'] =listing_details['photo'] if listing_details else None

            # Get the producer name
            cursor.execute('''
                SELECT "producerName"
                FROM producers
                WHERE id = %s
            ''', (row['producerID'],))

            producer = cursor.fetchone()
            row['producerName'] = producer['producerName'] if producer else None

            # Get the rating
            cursor.execute('''
                SELECT AVG("rating") AS "averageRating"
                FROM "reviews"
                WHERE "reviewTarget" = %s
            ''', (row['listingID'],))

            rating = cursor.fetchone()

            if rating and rating['averageRating'] is not None:
                row['averageRating'] = round(rating['averageRating'], 2)
            else:
                row['averageRating'] = None

        return rows
    
    except Exception as e:
        raise Exception(f"Error fetching top 5 for {table}: {e}")


# ==========================================================================================

# [POST] Update user's Grails, Up & Coming, and GOATs selections
@blueprint.route("/editTop3", methods=['POST'])
def editTop3():
    """
    Update a user's Grails, Up & Coming, and GOATs drink selections.
    
    Request body should include:
    - userID: User ID
    - selectedGrails: Array of drink names for Grails section
    - selectedUpAndComing: Array of drink names for Up & Coming section
    - selectedGOATs: Array of drink names for GOATs section
    - selectedCategory: Category selected during the update
    - selectedDrinkIDs: Array of drink IDs corresponding to the selected drinks pending update
    
    Returns:
    - 201: User's selections updated successfully
    - 400: Missing user ID
    - 404: User not found
    - 410: Error updating Grails, Up & Coming, or GOATs
    - 500: Server error
    """
    conn = g.db
    
    try:
        data = request.json
        user_id = data.get('userID')
        selected_grails = data.get('selectedGrails', [])
        selected_up_and_coming = data.get('selectedUpAndComing', [])
        selected_goats = data.get('selectedGOATs', [])
        selected_category = data.get('selectedCategory')
        selected_drink_ids = data.get('selectedDrinkIDs', [])
        
        if not user_id:
            return jsonify({"code": 400, "message": "User ID is required"}), 400
        
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            # Check if user exists
            cursor.execute('SELECT * FROM "users" WHERE "id" = %s', (user_id,))
            user = cursor.fetchone()
            
            if not user:
                return jsonify({"code": 404, "message": "User not found"}), 404
            
            # Step 1: Update grails
            if selected_category == "Grail":
                grails_result = update_user_listings(cursor, user_id, "grails", selected_grails, selected_drink_ids)
                if isinstance(grails_result, dict) and "error" in grails_result:
                    return jsonify({"code": 410, "message": grails_result["error"]}), 410

            # Step 2: Update up and coming
            elif selected_category == "Up & Coming":
                upcoming_result = update_user_listings(cursor, user_id, "upAndComing", selected_up_and_coming, selected_drink_ids)
                if isinstance(upcoming_result, dict) and "error" in upcoming_result:
                    return jsonify({"code": 410, "message": upcoming_result["error"]}), 410

            # Step 3: Update goats
            else:
                goats_result = update_user_listings(cursor, user_id, "goats", selected_goats, selected_drink_ids)
                if isinstance(goats_result, dict) and "error" in goats_result:
                    return jsonify({"code": 410, "message": goats_result["error"]}), 410

                     
            # Step 4: Update the user's selections
            cursor.execute('''
                UPDATE "users" 
                SET "grails" = %s, 
                    "upAndComing" = %s, 
                    "goats" = %s
                WHERE "id" = %s
            ''', (selected_grails, selected_up_and_coming, selected_goats, user_id))
            
            conn.commit()
               
            return jsonify({"code": 201, "message": "User selections updated successfully"}), 201
            
    except Exception as e:
        print(str(e))
        return jsonify({"code": 500, "message": "An error occurred updating user selections.", "error": e}), 500
    

# [GET] Get top 5 Grails, Up & Coming, and GOATs based on drink type
@blueprint.route("/getTop5", methods=['GET'])
def getTop5():
    conn = g.db
    cursor = conn.cursor()

    drink_type = request.args.get('type')
    type_category = request.args.get('typeCat')

    try:
        grails_data = fetch_top_5(cursor, "grails", drink_type, type_category)
        up_and_coming_data = fetch_top_5(cursor, "upAndComing", drink_type, type_category)
        goats_data = fetch_top_5(cursor, "goats", drink_type, type_category)

        return jsonify({
            "code": 200,
            "data": {
                "grails": grails_data,
                "upAndComing": up_and_coming_data,
                "goats": goats_data
            },
            "message": "Top 5 data retrieved successfully."
        }), 200

    except Exception as e:
        print(str(e))
        return jsonify({
            "code": 500,
            "message": "An error occurred retrieving Top 5 data."
        }), 500

    finally:
        cursor.close() 



