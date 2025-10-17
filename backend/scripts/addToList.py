# Port: 5070
# Routes: /updateListing/<id> (PUT), /deleteListing/<id> (DELETE)
# Dataclass: listings
# -----------------------------------------------------------------------------------------

import os
import json
from bson import json_util
from flask import Blueprint, g, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from bson.objectid import ObjectId
from datetime import datetime

from psycopg2.extras import RealDictCursor # ADDED BY SMU GROUP 3

# Import the database manager for connection pooling
from app import db_manager



file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

def parse_json(data):
    return json.loads(json_util.dumps(data))

# -----------------------------------------------------------------------------------------
# [PUT] adds a listing to have tried list 
# - Update "Drinks I Have Tried List" with specified id from the "listings" collection
# - Possible return codes: 200 (List Updated), 440 (Failed to add to list)
@blueprint.route("/addToTried/", methods=['PUT'])
def addToTried():
    addedListing = request.get_json()
    listingID = int(addedListing["listingID"])
    userID = int(addedListing["userID"])
    addedDate = addedListing["date"]  # Date when the drink was added
    listNameTried = "Drinks I Have Tried"
    listNameWant = "Drinks I Want To Try"

    try:
        with db_manager.get_cursor() as cursor:
            # Get or create "Drinks I Have Tried" list ID
            cursor.execute("""
                INSERT INTO "usersDrinkLists" ("userId", "listName")
                VALUES (%s, %s)
                ON CONFLICT ("userId", "listName") DO NOTHING
                RETURNING "id";
            """, (userID, listNameTried))
            tried_list_id = cursor.fetchone()

            if tried_list_id is None:  
                cursor.execute("""
                    SELECT "id" FROM "usersDrinkLists"
                    WHERE "userId" = %s AND "listName" = %s;
                """, (userID, listNameTried))
                tried_list_id = cursor.fetchone()['id']
            else:
                tried_list_id = tried_list_id['id']

            # Remove listing from "Drinks I Want To Try"
            cursor.execute("""
                DELETE FROM "usersDrinkListItems"
                WHERE "listId" = (
                    SELECT "id" FROM "usersDrinkLists"
                    WHERE "userId" = %s AND "listName" = %s
                ) AND "drinkId" = %s;
            """, (userID, listNameWant, listingID))

            # Add listing to "Drinks I Have Tried" with addedDate
            cursor.execute("""
                INSERT INTO "usersDrinkListItems" ("listId", "drinkId", "addedDate")
                VALUES (%s, %s, %s)
                ON CONFLICT ("listId", "drinkId") DO UPDATE
                SET "addedDate" = EXCLUDED."addedDate";
            """, (tried_list_id, listingID, addedDate))

        return jsonify(
            {
                "code": 200,
                "data": listingID,
                "message": "Listing was added to 'Drinks I Have Tried'."
            }
        ), 200

    except Exception as e:
        print(e)
        return jsonify(
            {
                "code": 440,
                "data": str(e),
                "message": "Listing was not added."
            }
        ), 440

# -----------------------------------------------------------------------------------------
# [PUT] Adds a listing to "Drinks I Want To Try" list
# - Removes from "Drinks I Have Tried" list if it exists
# - Prevents duplicates in the target list
# - Possible return codes: 210 (Success), 450 (Failure)
@blueprint.route("/addToWant/", methods=['PUT'])
def addToWant():
    addedListing = request.get_json()
    listingID = int(addedListing["listingID"])
    userID = int(addedListing["userID"])
    addedDate = addedListing["date"]
    listNameTried = "Drinks I Have Tried"
    listNameWant = "Drinks I Want To Try"

    try:
        with db_manager.get_cursor() as cursor:
            # Get or create "Drinks I Want To Try" list ID
            cursor.execute("""
                INSERT INTO "usersDrinkLists" ("userId", "listName")
                VALUES (%s, %s)
                ON CONFLICT ("userId", "listName") DO NOTHING
                RETURNING "id";
            """, (userID, listNameWant))
            want_list_id = cursor.fetchone()

            if want_list_id is None:
                cursor.execute("""
                    SELECT "id" FROM "usersDrinkLists"
                    WHERE "userId" = %s AND "listName" = %s;
                """, (userID, listNameWant))
                want_list_id = cursor.fetchone()['id']
            else:
                want_list_id = want_list_id['id']

            # Remove listing from "Drinks I Have Tried"
            cursor.execute("""
                DELETE FROM "usersDrinkListItems"
                WHERE "listId" = (
                    SELECT "id" FROM "usersDrinkLists"
                    WHERE "userId" = %s AND "listName" = %s
                ) AND "drinkId" = %s;
            """, (userID, listNameTried, listingID))

            # Add listing to "Drinks I Want To Try" with addedDate
            cursor.execute("""
                INSERT INTO "usersDrinkListItems" ("listId", "drinkId", "addedDate")
                VALUES (%s, %s, %s)
                ON CONFLICT ("listId", "drinkId") DO UPDATE
                SET "addedDate" = EXCLUDED."addedDate";
            """, (want_list_id, listingID, addedDate))

        return jsonify(
            {
                "code": 210,
                "data": listingID,
                "message": "Listing was added to 'Drinks I Want To Try'."
            }
        ), 210

    except Exception as e:
        print(e)
        return jsonify(
            {
                "code": 450,
                "data": str(e),
                "message": "Listing was not added."
            }
        ), 450