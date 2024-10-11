import os
import importlib
import stripe
from flask import Flask, g
from flask_pymongo import PyMongo
from flask_cors import CORS
from flask_mail import Mail
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Allow all requests
app = Flask(__name__)
CORS(app)

load_dotenv()

# OLD CONNECTOR -----------------------------------------------------------------
# Connect to MongoDB
# app.config["MONGO_URI"] = os.getenv('MONGO_DB_URL')
# db = PyMongo(app).db

# NEW CONNECTOR ------------------------------------------------------------------
# Connect to Postgresql
app.config["POSTGRES_URI"] = os.getenv("POSTGRES_URI")


# Function to get or create a PostgreSQL connection
def get_db_connection():
    if "db_conn" not in g:
        g.db_conn = psycopg2.connect(
            dsn=app.config["POSTGRES_URI"],
            cursor_factory=RealDictCursor,
        )
    return g.db_conn


# Connect to Mail Server
app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_PORT"] = os.getenv("MAIL_PORT")
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
mail = Mail(app)

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


# Make `db` accessible via Flask's `g` object
@app.before_request
def before_request():
    # OLD
    # g.db = db
    g.mail = mail

    # NEW
    g.db = get_db_connection()  # Example of storing a database connection in g
    # print("before_request: Data loaded into g")


# Function to dynamically register Blueprints from each script
def create_routes():
    scripts_path = os.path.join(os.path.dirname(__file__), "scripts")

    for script in os.listdir(scripts_path):
        if script.endswith(".py"):
            script_name = script[:-3]
            module = importlib.import_module(f"scripts.{script_name}")

            # Register Blueprints from the module if they exist
            if hasattr(module, "blueprint"):
                blueprint = getattr(module, "blueprint")
                app.register_blueprint(
                    blueprint, url_prefix=f'/{script_name.replace("_", "-")}'
                )
                print(f"Registered blueprint: /{script_name.replace('_', '-')}")


# FUNCTION TO CLOSE CONNECTION WITH POSTGRESQL
# NEW
@app.teardown_request
def teardown_request(exception):
    db_conn = g.pop("db_conn", None)
    if db_conn is not None:
        db_conn.close()


create_routes()

# for debugging
# Function to print all registered routes
# def print_routes(app):
#     print("\nRegistered Routes:")
#     for rule in app.url_map.iter_rules():
#         methods = ', '.join(rule.methods - {'HEAD', 'OPTIONS'})
#         print(f"{rule.endpoint:25s} {methods:20s} {rule}")

# print_routes(app)


HOST = os.getenv("HOST", "0.0.0.0")
PORT = os.getenv("PORT", 5000)
FLASK_DEBUG = os.getenv("FLASK_DEBUG", False)


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=FLASK_DEBUG)
