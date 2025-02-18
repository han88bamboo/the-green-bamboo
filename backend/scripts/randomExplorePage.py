import random
from flask import Flask, jsonify, Blueprint
import os
import psycopg2
from dotenv import load_dotenv

app = Flask(__name__)

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

# Get a new database connection
def get_db_connection():
    load_dotenv()
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT")
    )


# Fetch unique dates from addedDate column
def get_random_date():
    """Fetches a fresh random date from available listing dates each time."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT DISTINCT DATE("addedDate") FROM "listings"')
    dates = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    if not dates:
        return None  # Return None if no dates exist
    
    return random.choice([date[0] for date in dates])  # Pick a fresh random date

# Fetch bottles listed on a fresh randomly chosen existing date
def fetch_random_bottles():
    random_date = get_random_date()

    if not random_date:
        return []  # Return empty list if no dates exist
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM "listings"
        WHERE DATE("addedDate") = %s
        ORDER BY RANDOM()
        LIMIT 20
    """, (random_date,))
    
    bottles = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return bottles

@blueprint.route("/explore", methods=["GET"])
def get_explore_bottles():
    """Fetches a random set of bottles from a fresh random date each request."""
    bottles = fetch_random_bottles()
    return jsonify(bottles)

