# Test the connection to the PostgreSQL database
# Command to run file: python3 backend/postgresql/test_connection.py

# ======================================================================

import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

connection = None

try:
    # Connect to the PostgreSQL database using the URL from the .env file
    connection = psycopg2.connect(os.getenv("POSTGRESQL_DB_URL"))
    cursor = connection.cursor()
    
    # Test the connection
    cursor.execute("SELECT 1;")
    print("Connection to PostgreSQL DB successful!")
    
except Exception as error:
    print(f"Error connecting to PostgreSQL DB: {error}")

finally:
    if connection:
        cursor.close()
        connection.close()