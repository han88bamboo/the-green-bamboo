#!/bin/bash

# CloudWatch Logs Setup Script for Drink-X Backend
# This script helps you configure CloudWatch logging for your Flask application

echo "=== Drink-X CloudWatch Logging Setup ==="
echo ""

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI is not installed. Please install it first:"
    echo "   curl 'https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip' -o 'awscliv2.zip'"
    echo "   unzip awscliv2.zip"
    echo "   sudo ./aws/install"
    echo ""
    echo "After installation, run: aws configure"
    exit 1
fi

# Check AWS configuration
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS CLI is not configured. Please run: aws configure"
    echo "You'll need your AWS Access Key ID, Secret Access Key, and region"
    exit 1
fi

echo "✅ AWS CLI is installed and configured"

# Create CloudWatch Log Group
LOG_GROUP_NAME="/aws/ec2/drink-x-backend"
echo ""
echo "Creating CloudWatch Log Group: $LOG_GROUP_NAME"

if aws logs describe-log-groups --log-group-name-prefix $LOG_GROUP_NAME --query 'logGroups[?logGroupName==`'$LOG_GROUP_NAME'`]' --output text | grep -q $LOG_GROUP_NAME; then
    echo "✅ Log group already exists: $LOG_GROUP_NAME"
else
    aws logs create-log-group --log-group-name $LOG_GROUP_NAME
    if [ $? -eq 0 ]; then
        echo "✅ Created log group: $LOG_GROUP_NAME"
    else
        echo "❌ Failed to create log group"
        exit 1
    fi
fi

# Set retention policy (optional)
echo "Setting log retention to 30 days..."
aws logs put-retention-policy --log-group-name $LOG_GROUP_NAME --retention-in-days 30

echo ""
echo "=== CloudWatch Logs Configuration Complete ==="
echo ""
echo "Log Group Name: $LOG_GROUP_NAME"
echo ""
echo "Next steps:"
echo "1. Update your environment variables:"
echo "   export AWS_DEFAULT_REGION=your-region"
echo "   export CLOUDWATCH_LOG_GROUP=$LOG_GROUP_NAME"
echo ""
echo "2. Your application will now send logs to CloudWatch"
echo "3. View logs in AWS Console -> CloudWatch -> Log groups -> $LOG_GROUP_NAME"
echo ""
echo "🎉 Setup complete!"