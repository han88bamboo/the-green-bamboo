import base64
import boto3
from botocore.exceptions import NoCredentialsError
import uuid

import os

from dotenv import load_dotenv
load_dotenv()

bucket_name = 'tf-drinkx-prod-fe-images'

def uploadBase64ImageToS3(base64_string):
    region='ap-southeast-1'
    # Decode the base64 string
    credentials = { 
        'aws_access_key_id': os.getenv('AWS_ACCESS_KEY_ID'),
        'aws_secret_access_key': os.getenv('AWS_SECRET_ACCESS_KEY')
    }
    try:
        image_data = base64.b64decode(base64_string)
    except base64.binascii.Error as e:
        print(f"Error decoding base64 string: {e}")
        return base64_string

    # Initialize a session using Amazon S3
    s3_client = boto3.client('s3', region_name=region, **credentials)
    object_key = f'images/{uuid.uuid4()}.jpg'
    try:
        # Upload the image to S3
        s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=image_data, ContentType='image/jpg')

        # Generate the URL to the uploaded image
        url = f"https://{bucket_name}.s3.{region}.amazonaws.com/{object_key}"
        return url
    except NoCredentialsError:
        print("Credentials not available")
        return base64_string


def deleteImageFromS3(url):
    region='ap-southeast-1'
    credentials = { 
        'aws_access_key_id': os.getenv('AWS_ACCESS_KEY_ID'),
        'aws_secret_access_key': os.getenv('AWS_SECRET_ACCESS_KEY')
    }
    # Get the key from the url by stripping https://testbucketdrinkx.s3.amazonaws.com/xxxx
    object_key = url[48:]
    # object_key = 'images/1c186607-f6a5-4004-b1b3-e891b45da03e.jpg'

    # Initialize a session using Amazon S3
    s3_client = boto3.client('s3', region_name=region, **credentials)
    try:
        # Upload the image to S3
        return s3_client.delete_object(Bucket=bucket_name, Key=object_key)

    except NoCredentialsError:
        print("Credentials not available")
        return None


# Example usage
# This is an example base64 string for an image (you should use your actual base64 string)
# base64_String =''
# url = uploadBase64ImageToS3(base64_String)
# isDeleted = deleteImageFromS3(bucket_name)
# if url:
#     print(f"Image URL: {url}")
# if isDeleted:
#     print(f"Image URL: {isDeleted}")