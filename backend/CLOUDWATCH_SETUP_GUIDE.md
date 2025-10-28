# CloudWatch Logging Setup Guide for Drink-X

## Overview
This guide will help you set up comprehensive logging that sends structured logs to AWS CloudWatch, making it easier to debug issues when your application crashes.

## What We've Added

### 1. Structured Logging in `app.py`
- Request ID tracking for each API call
- Structured JSON logging for CloudWatch
- Enhanced error handling with detailed context
- Request timing and performance metrics

### 2. Logging Helpers (`logging_helpers.py`)
- Decorator for automatic endpoint logging
- Database query logging
- Step-by-step execution logging
- Standardized error responses

### 3. Enhanced Menu Endpoint (`scripts/menu.py`)
- Comprehensive logging at each step
- Input validation logging
- Database operation logging
- Performance timing
- Detailed error context

## Step-by-Step Setup Instructions

### Step 1: Update Your Environment
1. **Open Terminal** in VS Code (`Terminal` → `New Terminal`)
2. **Navigate to your backend directory**:
   ```bash
   cd /Users/han/Documents/GitHub/the-green-bamboo/backend
   ```

### Step 2: Install Additional Dependencies
1. **Add to your `requirements.txt`**:
   ```
   boto3==1.34.145
   watchtower==3.0.1
   ```
2. **Install the new dependencies**:
   ```bash
   pip install boto3 watchtower
   ```

### Step 3: AWS CloudWatch Setup
1. **Install AWS CLI** (if not already installed):
   ```bash
   # For Mac
   brew install awscli
   
   # For Windows (using Chocolatey)
   choco install awscli
   ```

2. **Configure AWS CLI**:
   ```bash
   aws configure
   ```
   You'll need:
   - AWS Access Key ID
   - AWS Secret Access Key
   - Default region (e.g., `us-east-1`)
   - Default output format: `json`

3. **Run the CloudWatch setup script**:
   ```bash
   chmod +x setup-cloudwatch.sh
   ./setup-cloudwatch.sh
   ```

### Step 4: Update Your Environment Variables
1. **Open your `.env` file** in VS Code
2. **Add these CloudWatch variables**:
   ```env
   # CloudWatch Logging
   AWS_DEFAULT_REGION=us-east-1
   CLOUDWATCH_LOG_GROUP=/aws/ec2/drink-x-backend
   CLOUDWATCH_LOG_STREAM=drink-x-backend-stream
   ```

### Step 5: Update Docker Configuration (if using Docker)
1. **Open `docker-compose-be.yml`**
2. **Add environment variables**:
   ```yaml
   services:
     backend:
       environment:
         - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
         - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
         - AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION}
         - CLOUDWATCH_LOG_GROUP=${CLOUDWATCH_LOG_GROUP}
   ```

## How to Use the New Logging

### For New Endpoints
1. **Import the logging helpers**:
   ```python
   from logging_helpers import get_structured_logger, log_endpoint_execution, log_step
   ```

2. **Add the decorator to your endpoint**:
   ```python
   @blueprint.route("/your-endpoint")
   @log_endpoint_execution
   def your_endpoint():
       # Your code here
   ```

3. **Add step logging throughout your function**:
   ```python
   def your_endpoint():
       logger = get_structured_logger(__name__)
       
       log_step(logger, "validate_input", {"param": value})
       # validation code
       
       log_step(logger, "database_query_start")
       # database code
       
       log_step(logger, "process_results", {"count": len(results)})
       # processing code
   ```

### For Existing Endpoints
You can gradually add logging to existing endpoints by:
1. Adding the `@log_endpoint_execution` decorator
2. Adding `log_step()` calls at key points
3. Using `log_database_query()` for database operations

## Viewing Logs in CloudWatch

1. **Open AWS Console** in your browser
2. **Navigate to CloudWatch**:
   - Go to `Services` → `CloudWatch`
   - Click `Log groups` in the left sidebar
   - Find your log group: `/aws/ec2/drink-x-backend`

3. **View Log Streams**:
   - Click on your log group
   - Click on the most recent log stream
   - View real-time logs

4. **Search and Filter**:
   - Use the search box to find specific errors
   - Filter by log level (ERROR, INFO, etc.)
   - Search by request_id to trace specific requests

## Log Structure
Each log entry will be JSON structured like this:
```json
{
  "timestamp": "2025-10-27T10:30:00",
  "level": "INFO",
  "event": "request_start",
  "endpoint": "menu.getMenuSections",
  "method": "GET",
  "request_id": "abc12345",
  "params": {"venue_id": 123}
}
```

## Troubleshooting Your Crash

When your site crashes:
1. **Check CloudWatch Logs** immediately
2. **Search for ERROR level logs** around the crash time
3. **Look for the request_id** of failing requests
4. **Follow the execution steps** to see where it failed
5. **Check database operation logs** for SQL errors

## Testing the Setup

1. **Make a test request** to your menu endpoint:
   ```bash
   curl http://localhost:5000/menu/123
   ```

2. **Check CloudWatch** for the logs
3. **Verify you see**:
   - Request start log
   - Step execution logs
   - Database query logs
   - Request completion log

## Common Issues

### Issue: Logs not appearing in CloudWatch
- Check AWS credentials are configured correctly
- Verify the log group exists in CloudWatch
- Check network connectivity to AWS

### Issue: Permission errors
- Ensure your AWS user has CloudWatch Logs permissions:
  - `logs:CreateLogGroup`
  - `logs:CreateLogStream`
  - `logs:PutLogEvents`

### Issue: Too many logs
- Adjust log levels in `logging.conf`
- Use `log_step()` selectively for key operations only

## Performance Impact
- Structured logging adds ~1-5ms per request
- CloudWatch upload is asynchronous
- Minimal impact on user experience
- Benefits far outweigh costs for debugging

Now when your application crashes, you'll have detailed logs showing exactly where and why it failed!