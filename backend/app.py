import os
import importlib

import urllib
import stripe
from flask import Flask, g
from flask_pymongo import PyMongo
from flask import jsonify
from flask_cors import CORS
from flask_mail import Mail
import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from contextlib import contextmanager

import logging.config

logging.config.fileConfig(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "logging.conf",
        )
    ),
    disable_existing_loggers=False,
)
logger = logging.getLogger(__name__)

# Allow all requests
app = Flask(__name__)
CORS(app)

@app.errorhandler(Exception)
def handle_exception(e):
    response = jsonify({"error": str(e)})
    response.status_code = 500
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

load_dotenv()

class DatabaseManager:
    """
    Custom database manager that wraps psycopg2's ThreadedConnectionPool.
    This provides automatic connection pooling without requiring an ORM like SQLAlchemy.
    
    KEY DESIGN DECISIONS:
    - Uses psycopg2's built-in ThreadedConnectionPool (not SQLAlchemy's engine pooling)
    - Implements context managers for automatic connection/cursor cleanup
    - No need for explicit "sessions" - each context manager handles its own transaction
    """
    
    def __init__(self, app=None):
        """
        Initialize database manager. Pool creation is deferred until init_app() is called.
        This supports Flask's application factory pattern.
        """
        self.pool = None  # Connection pool will be created in init_app()
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """
        CONNECTION POOL CREATION:
        This is where the actual connection pool is created and configured.
        Called once during app startup, not per request.
        """
        config = app.config
        
        # Create ThreadedConnectionPool - psycopg2's built-in pooling solution
        # This is NOT an ORM feature, it's pure psycopg2 connection management
        self.pool = pool.ThreadedConnectionPool(
            minconn=5,      # POOL PARAMETER: Minimum connections always kept alive
            maxconn=90,     # POOL PARAMETER: Maximum connections allowed in pool
            host=config['POSTGRES_HOST'],
            port=config['POSTGRES_PORT'],
            database=config['POSTGRES_DB'],
            user=config['POSTGRES_USER'],
            password=config['POSTGRES_PASSWORD'],
            cursor_factory=RealDictCursor  # Makes query results return as dicts instead of tuples
        )
        
        # Store reference to the manager in the Flask app for global access
        app.db_manager = self
    
    @contextmanager
    def get_connection(self):
        """
        CONNECTION CHECKOUT/RELEASE:
        This context manager handles the critical connection lifecycle:
        1. Checks out a connection from the pool (getconn())
        2. Automatically returns it to the pool when done (putconn())
        3. Handles rollback on exceptions
        
        The connection is reused by other requests after being returned to the pool.
        """
        conn = self.pool.getconn()  # CHECK OUT: Get connection from pool
        try:
            yield conn  # Provide connection to calling code
        except Exception as e:
            conn.rollback()  # ROLLBACK: Undo any uncommitted changes on error
            logger.error(f"Database error: {e}")
            raise
        finally:
            self.pool.putconn(conn)  # RELEASE: Return connection to pool for reuse
    
    @contextmanager
    def get_cursor(self, commit=True):
        """
        HIGH-LEVEL CURSOR CONTEXT MANAGER:
        This eliminates the need for explicit "sessions" by handling:
        1. Connection management (via get_connection())
        2. Cursor creation and cleanup
        3. Automatic commits (unless commit=False)
        4. Automatic rollbacks on errors
        
        TRANSACTION MANAGEMENT:
        - Each get_cursor() call is its own transaction
        - Auto-commits on success (unless commit=False)
        - Auto-rollbacks on exceptions
        - No need for explicit session management
        """
        with self.get_connection() as conn:  # Get pooled connection
            cursor = conn.cursor()  # Create cursor from connection
            try:
                yield cursor  # Provide cursor to calling code
                if commit:
                    conn.commit()  # AUTO-COMMIT: Transaction is committed automatically
            except Exception as e:
                conn.rollback()  # AUTO-ROLLBACK: Undo changes on any error
                raise
            finally:
                cursor.close()  # Always close cursor to free resources

# SINGLETON PATTERN: Single global instance shared across all modules
# This instance will be initialized with the Flask app during startup
db_manager = DatabaseManager()

# OLD CONNECTOR -----------------------------------------------------------------
# Connect to MongoDB
# app.config["MONGO_URI"] = os.getenv('MONGO_DB_URL')
# db = PyMongo(app).db

# NEW CONNECTOR ------------------------------------------------------------------
# Connect to Postgresql
app.config["POSTGRES_USER"] = os.getenv("POSTGRES_USER")
app.config["POSTGRES_PASSWORD"] = os.getenv("POSTGRES_PASSWORD")
app.config["POSTGRES_HOST"] = os.getenv("POSTGRES_HOST")
app.config["POSTGRES_PORT"] = os.getenv("POSTGRES_PORT")
app.config["POSTGRES_DB"] = os.getenv("POSTGRES_DB")

# Initialize database manager with connection pooling
db_manager.init_app(app)


# Connect to Mail Server
app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_PORT"] = os.getenv("MAIL_PORT", 587)
app.config["MAIL_USE_TLS"] = True
app.config['MAIL_USE_SSL'] = False
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = 'Drink-X <noreply@drink-x.com>'
# app.config['MAIL_DEFAULT_SENDER'] = os.getenv("hellodrinkx@gmail.com")

mail = Mail(app)

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
stripe.api_version = "2025-05-28.basil"

# Make `mail` accessible via Flask's `g` object
@app.before_request
def before_request():
    # OLD
    # g.db = db
    g.mail = mail

    # NEW: No longer needed - connection pooling handles database connections
    # Database connections are now managed by db_manager.get_cursor() context manager
    # print("before_request: Mail loaded into g")


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
# NEW: No longer needed - connection pooling automatically handles connection cleanup
# The ThreadedConnectionPool manages connection lifecycle and cleanup
# @app.teardown_request
# def teardown_request(exception):
#     db_conn = g.pop("db_conn", None)
#     if db_conn is not None:
#         db_conn.close()


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
PORT = int(os.getenv("PORT", 5000))
FLASK_DEBUG = bool(os.getenv("FLASK_DEBUG", False))


if __name__ == "__main__":
    logger.info(f"Starting Flask server at {HOST}:{PORT}")
    app.run(host=HOST, port=PORT, debug=FLASK_DEBUG)
