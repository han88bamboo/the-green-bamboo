import importlib
import logging
import logging.config
import os
import traceback
from datetime import datetime

import stripe
from database.databaseManager import DatabaseManager
from dotenv import load_dotenv
from flask import Flask, g, jsonify, request
from flask_compress import Compress
from flask_cors import CORS
from flask_mail import Mail
from logger.StructuredLogger import StructuredLogger

# Enhanced logging configuration for CloudWatch
logging.config.fileConfig(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "logging.conf",
        )
    ),
    disable_existing_loggers=False,
)

# Create structured logger for CloudWatch
logger = logging.getLogger(__name__)
# Global structured logger instance
structured_logger = StructuredLogger(__name__)

# Allow all requests
app = Flask(__name__)
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


# Connect to Mail Server
app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_PORT"] = os.getenv("MAIL_PORT", 587)
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = "Drink-X <noreply@drink-x.com>"
# app.config['MAIL_DEFAULT_SENDER'] = os.getenv("hellodrinkx@gmail.com")


app.config["COMPRESS_ALGORITHM"] = "gzip"
app.config["COMPRESS_MIMETYPES"] = [
    "text/html",
    "text/css",
    "text/xml",
    "application/json",
    "application/javascript",
]
app.config["COMPRESS_LEVEL"] = 6
app.config["COMPRESS_MIN_SIZE"] = 100  # MAKE SURE THIS IS <= YOUR JSON SIZE

CORS(app)
Compress(app)
mail = Mail(app)


# Add request ID for tracking
@app.before_request
def before_request_logging():
    import uuid

    g.request_id = str(uuid.uuid4())[:8]  # Short request ID
    g.request_start_time = datetime.now()

    # Log incoming request
    structured_logger.log_request_start(
        endpoint=request.endpoint or request.path,
        method=request.method,
        params=dict(request.args) if request.args else None,
    )


@app.errorhandler(Exception)
def handle_exception(e):
    # Log the unhandled exception with full context
    structured_logger.log_request_error(
        endpoint=request.endpoint or request.path,
        error=e,
        traceback_str=traceback.format_exc(),
    )

    response = jsonify(
        {"error": str(e), "request_id": getattr(g, "request_id", "unknown")}
    )
    response.status_code = 500
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


load_dotenv()

# SINGLETON PATTERN: Single global instance shared across all modules
# This instance will be initialized with the Flask app during startup
db_manager = DatabaseManager(app, logger)

# Initialize database manager with connection pooling
db_manager.init_app(app)


# Pool monitoring middleware
def monitor_pool_on_request():
    """
    Optional middleware to monitor pool status on each request.
    Only logs warnings/errors to avoid performance impact.
    """
    import random

    # Only check pool health on 1% of requests to avoid overhead
    if random.random() < 0.01:
        db_manager.check_pool_health()


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


# Add database pool monitoring endpoint
@app.route("/health/db-pool", methods=["GET"])
def db_pool_health():
    """
    Database pool health check endpoint.
    Returns current pool status and health metrics.
    """
    try:
        pool_status = db_manager.get_pool_status()

        # Determine health status
        if pool_status.get("status") == "Pool not initialized":
            health_status = "unhealthy"
        elif pool_status.get("error"):
            health_status = "degraded"
        else:
            used = pool_status.get("used", 0)
            maxconn = pool_status.get("maxconn", 0)
            if isinstance(maxconn, int) and used / maxconn > 0.9:
                health_status = "warning"  # Pool utilization > 90%
            else:
                health_status = "healthy"

        return jsonify(
            {
                "status": health_status,
                "pool_stats": pool_status,
                "timestamp": str(datetime.now()),
            }
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify(
            {"status": "error", "error": str(e), "timestamp": str(datetime.now())}
        ), 500


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
                    blueprint, url_prefix=f"/{script_name.replace('_', '-')}"
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
