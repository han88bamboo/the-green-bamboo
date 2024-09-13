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
    conn = g.db
    addedListing = request.get_json()
    listingID = str(addedListing["listingID"])
    userID = int(addedListing["userID"])
    listNameTried = "Drinks I Have Tried"
    listNameWant = "Drinks I Want To Try"

    try:
        with conn.cursor() as cur:
            # Begin transaction
            conn.autocommit = False

            # Remove listingID from "Drinks I Want To Try" list
            cur.execute("""
                UPDATE "usersDrinkLists"
                SET "drinks" = array_remove("drinks", %s)
                WHERE "userId" = %s AND "listName" = %s;
            """, (listingID, userID, listNameWant))

            # Add listingID to "Drinks I Have Tried" list if not already present
            cur.execute("""
                UPDATE "usersDrinkLists"
                SET "drinks" = "drinks" || %s
                WHERE "userId" = %s AND "listName" = %s AND NOT (%s = ANY("drinks"));
            """, ([listingID], userID, listNameTried, listingID))

            # Ensure the list exists
            if cur.rowcount == 0:
                conn.rollback()
                return jsonify(
                    {
                        "code": 442,
                        "data": userID,
                        "message": "User or list not found, or item already exists."
                    }
                ), 442

            # Commit transaction
            conn.commit()
            conn.autocommit = True

        return jsonify(
            {
                "code": 200,
                "data": listingID,
                "message": "Listing was added to 'Drinks I Have Tried' list."
            }
        ), 200

    except Exception as e:
        conn.rollback()
        conn.autocommit = True
        return jsonify(
            {
                "code": 440,
                "data": str(e),
                "message": "Listing was not added to the list."
            }
        ), 440

# -----------------------------------------------------------------------------------------
# [PUT] Adds a listing to "Drinks I Want To Try" list
# - Removes from "Drinks I Have Tried" list if it exists
# - Prevents duplicates in the target list
# - Possible return codes: 210 (Success), 450 (Failure)
@blueprint.route("/addToWant/", methods=['PUT'])
def addToWant():
    conn = g.db
    addedListing = request.get_json()
    listingID = str(addedListing["listingID"])
    userID = int(addedListing["userID"])
    listNameTried = "Drinks I Have Tried"
    listNameWant = "Drinks I Want To Try"

    try:
        with conn.cursor() as cur:
            # Begin transaction
            conn.autocommit = False

            # Remove listingID from "Drinks I Have Tried" list
            cur.execute("""
                UPDATE "usersDrinkLists"
                SET "drinks" = array_remove("drinks", %s)
                WHERE "userId" = %s AND "listName" = %s;
            """, (listingID, userID, listNameTried))

            # Add listingID to "Drinks I Want To Try" list if not already present
            cur.execute("""
                UPDATE "usersDrinkLists"
                SET "drinks" = "drinks" || %s
                WHERE "userId" = %s AND "listName" = %s AND NOT (%s = ANY("drinks"));
            """, ([listingID], userID, listNameWant, listingID))

            # Ensure the list exists
            if cur.rowcount == 0:
                conn.rollback()
                return jsonify(
                    {
                        "code": 452,
                        "data": userID,
                        "message": "User or list not found, or item already exists."
                    }
                ), 452

            # Commit transaction
            conn.commit()
            conn.autocommit = True

        return jsonify(
            {
                "code": 210,
                "data": listingID,
                "message": "Listing was added to 'Drinks I Want To Try' list."
            }
        ), 210

    except Exception as e:
        conn.rollback()
        conn.autocommit = True
        return jsonify(
            {
                "code": 450,
                "data": str(e),
                "message": "Listing was not added to the list."
            }
        ), 450