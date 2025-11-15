from contextlib import contextmanager

import psycopg2
from flask import g
from psycopg2 import pool
from psycopg2.extras import RealDictCursor


class DatabaseManager:
    """
    Custom database manager that wraps psycopg2's ThreadedConnectionPool.
    This provides automatic connection pooling without requiring an ORM like SQLAlchemy.

    KEY DESIGN DECISIONS:
    - Uses psycopg2's built-in ThreadedConnectionPool (not SQLAlchemy's engine pooling)
    - Implements context managers for automatic connection/cursor cleanup
    - No need for explicit "sessions" - each context manager handles its own transaction
    """

    def __init__(self, app=None, logger=None):
        """
        Initialize database manager. Pool creation is deferred until init_app() is called.
        This supports Flask's application factory pattern.
        """
        self.pool = None  # Connection pool will be created in init_app()

        if app:
            self.init_app(app)

        self.logger = logger

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
            minconn=5,  # POOL PARAMETER: Minimum connections always kept alive
            maxconn=80,  # POOL PARAMETER: Maximum connections allowed in pool
            host=config["POSTGRES_HOST"],
            port=config["POSTGRES_PORT"],
            database=config["POSTGRES_DB"],
            user=config["POSTGRES_USER"],
            password=config["POSTGRES_PASSWORD"],
            cursor_factory=RealDictCursor,  # Makes query results return as dicts instead of tuples
        )

        # Log successful pool initialization
        self.logger.info(
            "charsiucharlie_connection_pooling_debug: Database connection pool initialized successfully"
        )
        self.logger.info(
            f"charsiucharlie_connection_pooling_debug: Pool config - min:5, max:80, host:{config['POSTGRES_HOST']}, db:{config['POSTGRES_DB']}"
        )
        self.log_pool_status("INIT")

        # Store reference to the manager in the Flask app for global access
        app.db_manager = self

    def check_pool_health(self):
        """
        Check pool health and log warnings if needed.
        Returns True if healthy, False if issues detected.
        """
        pool_status = self.get_pool_status()

        if "error" in pool_status:
            self.logger.error(f"Pool health check failed: {pool_status}")
            return False

        used = pool_status.get("used", 0)
        maxconn = pool_status.get("maxconn", 0)

        if isinstance(maxconn, int) and maxconn > 0:
            utilization = used / maxconn

            if utilization >= 0.9:
                self.logger.warning(
                    f"High pool utilization: {utilization:.1%} ({used}/{maxconn})"
                )
                return False
            elif utilization >= 0.75:
                self.logger.info(
                    f"Moderate pool utilization: {utilization:.1%} ({used}/{maxconn})"
                )

        return True

    def log_pool_status(self, context=""):
        """
        Log current pool status for monitoring and debugging.
        """
        pool_status = self.get_pool_status()
        if context:
            context = f"[{context}] "

        if "error" in pool_status:
            self.logger.warning(
                f"charsiucharlie_connection_pooling_debug: {context}Pool monitoring error: {pool_status}"
            )
        else:
            self.logger.info(
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
            minconn = getattr(self.pool, "minconn", "Unknown")
            maxconn = getattr(self.pool, "maxconn", "Unknown")

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
                "pool_utilization": f"{(used / maxconn * 100):.1f}%"
                if maxconn != "Unknown"
                else "Unknown",
            }
        except Exception as e:
            self.logger.warning(f"Could not get pool status: {e}")
            return {"status": "Pool status unavailable", "error": str(e)}

    def _is_connection_alive(self, conn):
        """
        Test if a connection is still alive and responsive.
        Uses a lightweight query that doesn't affect application state.
        """
        try:
            # Use a simple SELECT 1 query to test connection health
            with conn.cursor() as test_cursor:
                test_cursor.execute("SELECT 1")
                test_cursor.fetchone()
            return True
        except Exception as e:
            self.logger.debug(
                f"charsiucharlie_connection_pooling_debug: Connection health check failed: {type(e).__name__}: {e}"
            )
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
        request_id = getattr(g, "request_id", "unknown")
        max_retries = 2

        # Log pool status before getting connection
        pool_status = self.get_pool_status()
        self.logger.debug(
            f"charsiucharlie_connection_pooling_debug: REQ-{request_id} Pool status before checkout: {pool_status}"
        )

        conn = None
        for attempt in range(max_retries + 1):
            try:
                conn = self.pool.getconn()  # CHECK OUT: Get connection from pool
                self.logger.debug(
                    f"charsiucharlie_connection_pooling_debug: REQ-{request_id} Successfully checked out connection from pool (attempt {attempt + 1})"
                )

                # Test connection health before use - critical for handling Aurora timeouts
                if not self._is_connection_alive(conn):
                    self.logger.warning(
                        f"charsiucharlie_connection_pooling_debug: REQ-{request_id} Stale connection detected on attempt {attempt + 1}, discarding"
                    )
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
                        self.logger.info(
                            f"charsiucharlie_connection_pooling_debug: REQ-{request_id} Retrying with fresh connection (attempt {attempt + 2})"
                        )
                        continue  # Try again with a fresh connection
                    else:
                        raise psycopg2.OperationalError(
                            "charsiucharlie_connection_pooling_debug: Unable to get healthy connection after retries"
                        )

                # Connection is healthy, proceed
                self.logger.debug(
                    f"charsiucharlie_connection_pooling_debug: REQ-{request_id} Connection health check passed, proceeding with query"
                )
                break

            except Exception as e:
                self.logger.error(
                    f"charsiucharlie_connection_pooling_debug: REQ-{request_id} Failed to get connection on attempt {attempt + 1}: {type(e).__name__}: {e}"
                )
                if attempt >= max_retries:
                    self.logger.error(
                        f"charsiucharlie_connection_pooling_debug: REQ-{request_id} Pool status during final failure: {self.get_pool_status()}"
                    )
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
                    self.logger.debug(
                        f"charsiucharlie_connection_pooling_debug: REQ-{request_id} Successfully rolled back transaction"
                    )
                except Exception as rollback_error:
                    self.logger.error(
                        f"charsiucharlie_connection_pooling_debug: REQ-{request_id} Rollback failed on live connection: {rollback_error}"
                    )
            else:
                self.logger.warning(
                    f"charsiucharlie_connection_pooling_debug: REQ-{request_id} Skipping rollback - connection already closed"
                )

            self.logger.error(
                f"charsiucharlie_connection_pooling_debug: REQ-{request_id} Database error - Type: {type(e).__name__}, Message: {str(e)}"
            )
            self.logger.error(
                f"charsiucharlie_connection_pooling_debug: REQ-{request_id} Pool status during error: {self.get_pool_status()}"
            )
            raise
        finally:
            try:
                # Check if connection is still valid before returning to pool
                if self._is_connection_alive(conn):
                    self.pool.putconn(
                        conn
                    )  # RELEASE: Return healthy connection to pool for reuse
                    self.logger.debug(
                        f"charsiucharlie_connection_pooling_debug: REQ-{request_id} Successfully returned healthy connection to pool"
                    )
                else:
                    self.logger.warning(
                        f"charsiucharlie_connection_pooling_debug: REQ-{request_id} Connection died during operation, removing from pool"
                    )
                    self.pool.putconn(
                        conn, close=True
                    )  # Remove dead connection from pool
            except Exception as e:
                self.logger.error(
                    f"charsiucharlie_connection_pooling_debug: REQ-{request_id} Failed to return connection to pool: {type(e).__name__}: {e}"
                )
                self.logger.error(
                    f"charsiucharlie_connection_pooling_debug: REQ-{request_id} Pool status after putconn failure: {self.get_pool_status()}"
                )
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
        request_id = getattr(g, "request_id", "unknown")
        self.logger.debug(
            f"charsiucharlie_connection_pooling_debug: REQ-{request_id} Starting cursor context (commit={commit})"
        )

        with (
            self.get_connection() as conn
        ):  # Get pooled connection (with health checks)
            cursor = conn.cursor()  # Create cursor from connection
            try:
                yield cursor  # Provide cursor to calling code
                if commit:
                    conn.commit()  # AUTO-COMMIT: Transaction is committed automatically
                    self.logger.debug(
                        f"charsiucharlie_connection_pooling_debug: REQ-{request_id} Transaction committed successfully"
                    )
            except Exception as e:
                conn.rollback()  # AUTO-ROLLBACK: Undo changes on any error (connection guaranteed live by get_connection)
                self.logger.error(
                    f"charsiucharlie_connection_pooling_debug: REQ-{request_id} Cursor operation failed, transaction rolled back: {type(e).__name__}: {e}"
                )
                raise
            finally:
                cursor.close()  # Always close cursor to free resources
                self.logger.debug(
                    f"charsiucharlie_connection_pooling_debug: REQ-{request_id} Cursor closed"
                )
