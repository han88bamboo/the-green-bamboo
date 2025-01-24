import psycopg2
from psycopg2 import OperationalError

def test_database_connection():
    # Replace these values with the credentials provided
    db_host = "drinkxprod.cxoa4asusd0j.ap-southeast-1.rds.amazonaws.com"
    db_name = "drinkx"
    db_user = "drinkxdbmaster"
    db_password = "E8ljq3bE4gIneUgRiAZPqC8c"
    db_port = "5432"  # Default PostgreSQL port

    try:
        # Establish the connection
        connection = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password,
            port=db_port
        )
        # Test if the connection is successful
        print("Connection to PostgreSQL database was successful!")
        connection.close()

    except OperationalError as e:
        # Handle connection errors
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_database_connection()