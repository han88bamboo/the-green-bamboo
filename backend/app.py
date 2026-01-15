import os
import importlib
from datetime import datetime
import json
import traceback

import urllib
import stripe
from flask import Flask, g, request
from flask import jsonify
from flask_cors import CORS
from flask_mail import Mail
import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from contextlib import contextmanager

import logging.config
import logging

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

# CloudWatch-friendly structured logging helper
class StructuredLogger:
    def __init__(self, logger_name):
        self.logger = logging.getLogger(logger_name)
    
    def log_request_start(self, endpoint, method, params=None):
        """Log the start of a request with context"""
        context = {
            "event": "request_start",
            "endpoint": endpoint,
            "method": method,
            "timestamp": datetime.now().isoformat(),
            "request_id": getattr(g, 'request_id', 'unknown')
        }
        if params:
            context["params"] = params
        self.logger.info(json.dumps(context))
    
    def log_request_success(self, endpoint, duration_ms=None, result_count=None):
        """Log successful request completion"""
        context = {
            "event": "request_success",
            "endpoint": endpoint,
            "timestamp": datetime.now().isoformat(),
            "request_id": getattr(g, 'request_id', 'unknown')
        }
        if duration_ms:
            context["duration_ms"] = duration_ms
        if result_count is not None:
            context["result_count"] = result_count
        self.logger.info(json.dumps(context))
    
    def log_request_error(self, endpoint, error, error_type=None, traceback_str=None):
        """Log request errors with full context"""
        context = {
            "event": "request_error",
            "endpoint": endpoint,
            "error": str(error),
            "error_type": error_type or type(error).__name__,
            "timestamp": datetime.now().isoformat(),
            "request_id": getattr(g, 'request_id', 'unknown')
        }
        if traceback_str:
            context["traceback"] = traceback_str
        self.logger.error(json.dumps(context))
    
    def log_database_operation(self, operation, query=None, params=None, success=True, error=None):
        """Log database operations"""
        context = {
            "event": "database_operation",
            "operation": operation,
            "success": success,
            "timestamp": datetime.now().isoformat(),
            "request_id": getattr(g, 'request_id', 'unknown')
        }
        if query:
            context["query"] = query[:200] + "..." if len(query) > 200 else query
        if params:
            context["params"] = str(params)
        if error:
            context["error"] = str(error)
        
        if success:
            self.logger.info(json.dumps(context))
        else:
            self.logger.error(json.dumps(context))

# Global structured logger instance
structured_logger = StructuredLogger(__name__)

# Allow all requests
app = Flask(__name__)
CORS(app)

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
        params=dict(request.args) if request.args else None
    )

@app.errorhandler(Exception)
def handle_exception(e):
    # Log the unhandled exception with full context
    structured_logger.log_request_error(
        endpoint=request.endpoint or request.path,
        error=e,
        traceback_str=traceback.format_exc()
    )
    
    response = jsonify({"error": str(e), "request_id": getattr(g, 'request_id', 'unknown')})
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
            maxconn=80,     # POOL PARAMETER: Maximum connections allowed in pool
            host=config['POSTGRES_HOST'],
            port=config['POSTGRES_PORT'],
            database=config['POSTGRES_DB'],
            user=config['POSTGRES_USER'],
            password=config['POSTGRES_PASSWORD'],
            cursor_factory=RealDictCursor  # Makes query results return as dicts instead of tuples
        )
        
        # Log successful pool initialization
        logger.info(f"charsiucharlie_connection_pooling_debug: Database connection pool initialized successfully")
        logger.info(f"charsiucharlie_connection_pooling_debug: Pool config - min:5, max:80, host:{config['POSTGRES_HOST']}, db:{config['POSTGRES_DB']}")
        self.log_pool_status("INIT")
        
        # Store reference to the manager in the Flask app for global access
        app.db_manager = self
    
    def check_pool_health(self):
        """
        Check pool health and log warnings if needed.
        Returns True if healthy, False if issues detected.
        """
        pool_status = self.get_pool_status()
        
        if 'error' in pool_status:
            logger.error(f"Pool health check failed: {pool_status}")
            return False
        
        used = pool_status.get('used', 0)
        maxconn = pool_status.get('maxconn', 0)
        
        if isinstance(maxconn, int) and maxconn > 0:
            utilization = used / maxconn
            
            if utilization >= 0.9:
                logger.warning(f"High pool utilization: {utilization:.1%} ({used}/{maxconn})")
                return False
            elif utilization >= 0.75:
                logger.info(f"Moderate pool utilization: {utilization:.1%} ({used}/{maxconn})")
        
        return True

    def log_pool_status(self, context=""):
        """
        Log current pool status for monitoring and debugging.
        """
        pool_status = self.get_pool_status()
        if context:
            context = f"[{context}] "
        
        if 'error' in pool_status:
            logger.warning(f"charsiucharlie_connection_pooling_debug: {context}Pool monitoring error: {pool_status}")
        else:
            logger.info(
                f"charsiucharlie_connection_pooling_debug: {context}Pool Status - "
                f"Available: {pool_status.get('available', 'N/A')}, "
                f"Used: {pool_status.get('used', 'N/A')}, "
                f"Utilization: {pool_status.get('pool_utilization', 'N/A')}"
            )

    def get_pool_status(self):
        """
        Get current connection pool status for monitoring.
        Returns dict with pool statistics.
        """
        if not self.pool:
            return {"status": "Pool not initialized"}
        
        # Access pool internals for monitoring
        # Note: These are internal psycopg2 attributes, handle carefully
        try:
            minconn = getattr(self.pool, 'minconn', 'Unknown')
            maxconn = getattr(self.pool, 'maxconn', 'Unknown')
            
            # Get current pool state
            with self.pool._lock:  # Thread-safe access to pool state
                available = len(self.pool._pool)
                used = len(self.pool._used)
            
            return {
                "minconn": minconn,
                "maxconn": maxconn,
                "available": available,
                "used": used,
                "total_created": available + used,
                "pool_utilization": f"{(used / maxconn * 100):.1f}%" if maxconn != 'Unknown' else 'Unknown'
            }
        except Exception as e:
            logger.warning(f"Could not get pool status: {e}")
            return {"status": "Pool status unavailable", "error": str(e)}

    def _is_connection_alive(self, conn):
        """
        Test if a connection is still alive and responsive.
        Uses a lightweight query that doesn't affect application state.
        """
        try:
            # Use a simple SELECT 1 query to test connection health
            with conn.cursor() as test_cursor:
                test_cursor.execute('SELECT 1')
                test_cursor.fetchone()
            return True
        except Exception as e:
            logger.debug(f"charsiucharlie_connection_pooling_debug: Connection health check failed: {type(e).__name__}: {e}")
            return False

    @contextmanager
    def get_connection(self):
        """
        ENHANCED CONNECTION CHECKOUT/RELEASE with stale connection detection:
        
        This context manager handles the critical connection lifecycle:
        1. Checks out a connection from the pool (getconn())
        2. Tests connection health before use (handles Aurora timeouts)
        3. Automatically retries with fresh connection if stale detected
        4. Handles safe rollback (only on live connections)
        5. Automatically returns connection to pool when done (putconn())
        
        AWS Aurora closes idle connections after 5 minutes, but psycopg2 pool
        doesn't detect this until query execution. This implementation proactively
        detects stale connections and replaces them automatically.
        """
        request_id = getattr(g, 'request_id', 'unknown')
        max_retries = 2
        
        # Log pool status before getting connection
        pool_status = self.get_pool_status()
        logger.debug(f"charsiucharlie_connection_pooling_debug: REQ-{request_id} Pool status before checkout: {pool_status}")
        
        conn = None
        for attempt in range(max_retries + 1):
            try:
                conn = self.pool.getconn()  # CHECK OUT: Get connection from pool
                logger.debug(f"charsiucharlie_connection_pooling_debug: REQ-{request_id} Successfully checked out connection from pool (attempt {attempt + 1})")
                
                # Test connection health before use - critical for handling Aurora timeouts
                if not self._is_connection_alive(conn):
                    logger.warning(f"charsiucharlie_connection_pooling_debug: REQ-{request_id} Stale connection detected on attempt {attempt + 1}, discarding")
                    try:
                        conn.close()  # Force close the stale connection
                    except:
                        pass  # Ignore errors when closing stale connection
                    
                    # Remove stale connection from pool permanently  
                    try:
                        self.pool.putconn(conn, close=True)
                    except:
                        pass  # Ignore putconn errors for stale connections
                    
                    if attempt < max_retries:
                        logger.info(f"charsiucharlie_connection_pooling_debug: REQ-{request_id} Retrying with fresh connection (attempt {attempt + 2})")
                        continue  # Try again with a fresh connection
                    else:
                        raise psycopg2.OperationalError("charsiucharlie_connection_pooling_debug: Unable to get healthy connection after retries")
                
                # Connection is healthy, proceed
                logger.debug(f"charsiucharlie_connection_pooling_debug: REQ-{request_id} Connection health check passed, proceeding with query")
                break
                
            except Exception as e:
                logger.error(f"charsiucharlie_connection_pooling_debug: REQ-{request_id} Failed to get connection on attempt {attempt + 1}: {type(e).__name__}: {e}")
                if attempt >= max_retries:
                    logger.error(f"charsiucharlie_connection_pooling_debug: REQ-{request_id} Pool status during final failure: {self.get_pool_status()}")
                    raise
                continue
        
        try:
            yield conn  # Provide connection to calling code
        except Exception as e:
            # SAFE ROLLBACK: Only attempt rollback if connection is still alive
            # This prevents the secondary "connection already closed" error
            if self._is_connection_alive(conn):
                try:
                    conn.rollback()  # ROLLBACK: Undo any uncommitted changes on error
                    logger.debug(f"charsiucharlie_connection_pooling_debug: REQ-{request_id} Successfully rolled back transaction")
                except Exception as rollback_error:
                    logger.error(f"charsiucharlie_connection_pooling_debug: REQ-{request_id} Rollback failed on live connection: {rollback_error}")
            else:
                logger.warning(f"charsiucharlie_connection_pooling_debug: REQ-{request_id} Skipping rollback - connection already closed")
            
            logger.error(f"charsiucharlie_connection_pooling_debug: REQ-{request_id} Database error - Type: {type(e).__name__}, Message: {str(e)}")
            logger.error(f"charsiucharlie_connection_pooling_debug: REQ-{request_id} Pool status during error: {self.get_pool_status()}")
            raise
        finally:
            try:
                # Check if connection is still valid before returning to pool
                if self._is_connection_alive(conn):
                    self.pool.putconn(conn)  # RELEASE: Return healthy connection to pool for reuse
                    logger.debug(f"charsiucharlie_connection_pooling_debug: REQ-{request_id} Successfully returned healthy connection to pool")
                else:
                    logger.warning(f"charsiucharlie_connection_pooling_debug: REQ-{request_id} Connection died during operation, removing from pool")
                    self.pool.putconn(conn, close=True)  # Remove dead connection from pool
            except Exception as e:
                logger.error(f"charsiucharlie_connection_pooling_debug: REQ-{request_id} Failed to return connection to pool: {type(e).__name__}: {e}")
                logger.error(f"charsiucharlie_connection_pooling_debug: REQ-{request_id} Pool status after putconn failure: {self.get_pool_status()}")
                # Don't re-raise here as it would mask the original exception
    
    @contextmanager
    def get_cursor(self, commit=True):
        """
        HIGH-LEVEL CURSOR CONTEXT MANAGER with enhanced error handling:
        This eliminates the need for explicit "sessions" by handling:
        1. Connection management (via enhanced get_connection() with health checks)
        2. Cursor creation and cleanup
        3. Automatic commits (unless commit=False)
        4. Automatic rollbacks on errors
        5. Automatic retry on stale connections (handled by get_connection())
        
        TRANSACTION MANAGEMENT:
        - Each get_cursor() call is its own transaction
        - Auto-commits on success (unless commit=False)
        - Auto-rollbacks on exceptions
        - No need for explicit session management
        """
        request_id = getattr(g, 'request_id', 'unknown')
        logger.debug(f"charsiucharlie_connection_pooling_debug: REQ-{request_id} Starting cursor context (commit={commit})")
        
        with self.get_connection() as conn:  # Get pooled connection (with health checks)
            cursor = conn.cursor()  # Create cursor from connection
            try:
                yield cursor  # Provide cursor to calling code
                if commit:
                    conn.commit()  # AUTO-COMMIT: Transaction is committed automatically
                    logger.debug(f"charsiucharlie_connection_pooling_debug: REQ-{request_id} Transaction committed successfully")
            except Exception as e:
                conn.rollback()  # AUTO-ROLLBACK: Undo changes on any error (connection guaranteed live by get_connection)
                logger.error(f"charsiucharlie_connection_pooling_debug: REQ-{request_id} Cursor operation failed, transaction rolled back: {type(e).__name__}: {e}")
                raise
            finally:
                cursor.close()  # Always close cursor to free resources
                logger.debug(f"charsiucharlie_connection_pooling_debug: REQ-{request_id} Cursor closed")

# SINGLETON PATTERN: Single global instance shared across all modules
# This instance will be initialized with the Flask app during startup
db_manager = DatabaseManager()

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

# Add database pool monitoring endpoint
@app.route('/health/db-pool', methods=['GET'])
def db_pool_health():
    """
    Database pool health check endpoint.
    Returns current pool status and health metrics.
    """
    try:
        pool_status = db_manager.get_pool_status()
        
        # Determine health status
        if pool_status.get('status') == 'Pool not initialized':
            health_status = 'unhealthy'
        elif pool_status.get('error'):
            health_status = 'degraded'
        else:
            used = pool_status.get('used', 0)
            maxconn = pool_status.get('maxconn', 0)
            if isinstance(maxconn, int) and used / maxconn > 0.9:
                health_status = 'warning'  # Pool utilization > 90%
            else:
                health_status = 'healthy'
        
        return jsonify({
            'status': health_status,
            'pool_stats': pool_status,
            'timestamp': str(datetime.now())
        })
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': str(datetime.now())
        }), 500


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

# Initialize background scheduler for scheduled tasks (e.g., story notifications)
# Only start scheduler in main process (not in reloader child process)
import os as _os
if _os.environ.get('WERKZEUG_RUN_MAIN') == 'true' or not app.debug:
    try:
        from scripts.scheduled_tasks import init_scheduler
        init_scheduler(app)
        logger.info("Background scheduler initialized for scheduled tasks.")
    except Exception as scheduler_err:
        logger.error(f"Failed to initialize scheduler: {scheduler_err}")

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
