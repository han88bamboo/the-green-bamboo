import json
import logging
from datetime import datetime

from flask import g


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
            "request_id": getattr(g, "request_id", "unknown"),
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
            "request_id": getattr(g, "request_id", "unknown"),
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
            "request_id": getattr(g, "request_id", "unknown"),
        }
        if traceback_str:
            context["traceback"] = traceback_str
        self.logger.error(json.dumps(context))

    def log_database_operation(
        self, operation, query=None, params=None, success=True, error=None
    ):
        """Log database operations"""
        context = {
            "event": "database_operation",
            "operation": operation,
            "success": success,
            "timestamp": datetime.now().isoformat(),
            "request_id": getattr(g, "request_id", "unknown"),
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
