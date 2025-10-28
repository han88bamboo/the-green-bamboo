"""
Logging helpers for CloudWatch structured logging
"""
import logging
import json
import traceback
import time
from datetime import datetime
from functools import wraps
from flask import g, request, jsonify

def get_structured_logger(module_name):
    """Get a structured logger for a specific module"""
    from app import StructuredLogger
    return StructuredLogger(module_name)

def log_endpoint_execution(func):
    """
    Decorator to automatically log endpoint execution with detailed context
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Create logger for this module
        logger = get_structured_logger(func.__module__)
        
        # Start timing
        start_time = time.time()
        endpoint_name = f"{func.__module__}.{func.__name__}"
        
        # Log start with parameters
        params = {}
        if args:
            params['args'] = [str(arg) for arg in args]
        if kwargs:
            params['kwargs'] = {k: str(v) for k, v in kwargs.items()}
        if request.args:
            params['query_params'] = dict(request.args)
        if request.json:
            params['body'] = request.json
        
        logger.log_request_start(endpoint_name, request.method, params)
        
        try:
            # Execute the function
            result = func(*args, **kwargs)
            
            # Calculate duration
            duration_ms = int((time.time() - start_time) * 1000)
            
            # Determine result count if possible
            result_count = None
            if hasattr(result, '__len__'):
                try:
                    if isinstance(result, tuple) and len(result) >= 2:
                        # Flask response tuple (data, status_code)
                        data = result[0]
                        if hasattr(data, 'get_json'):
                            json_data = data.get_json()
                            if isinstance(json_data, list):
                                result_count = len(json_data)
                            elif isinstance(json_data, dict) and 'data' in json_data:
                                if isinstance(json_data['data'], list):
                                    result_count = len(json_data['data'])
                except:
                    pass
            
            logger.log_request_success(endpoint_name, duration_ms, result_count)
            return result
            
        except Exception as e:
            # Calculate duration even for errors
            duration_ms = int((time.time() - start_time) * 1000)
            
            # Log detailed error
            logger.log_request_error(
                endpoint_name, 
                e, 
                type(e).__name__, 
                traceback.format_exc()
            )
            
            # Re-raise the exception
            raise
    
    return wrapper

def log_database_query(logger, operation, query, params=None):
    """Helper to log database queries"""
    logger.log_database_operation(operation, query, params, success=True)

def log_database_error(logger, operation, query, error, params=None):
    """Helper to log database errors"""
    logger.log_database_operation(operation, query, params, success=False, error=error)

def create_error_response(message, code=500, include_request_id=True):
    """Create standardized error response"""
    response_data = {
        "code": code,
        "message": message
    }
    if include_request_id:
        response_data["request_id"] = getattr(g, 'request_id', 'unknown')
    
    return jsonify(response_data), code

def log_step(logger, step_name, details=None):
    """Log individual steps within an endpoint"""
    context = {
        "event": "execution_step",
        "step": step_name,
        "timestamp": datetime.now().isoformat(),
        "request_id": getattr(g, 'request_id', 'unknown')
    }
    if details:
        context["details"] = details
    
    logger.logger.info(json.dumps(context))