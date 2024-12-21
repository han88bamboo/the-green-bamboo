import base64
import boto3
from botocore.exceptions import NoCredentialsError
from botocore.exceptions import ClientError
import uuid
import requests

import os

from dotenv import load_dotenv
load_dotenv()

# bucket_name = 'tf-drinkx-prod-fe-images'
# region='ap-southeast-1'
bucket_name = 'drinkximages'
region='us-east-1'

def uploadBase64ImageToS3(base64_string):

    credentials = { 
        'aws_access_key_id': os.getenv('AWS_ACCESS_KEY_ID'),
        'aws_secret_access_key': os.getenv('AWS_SECRET_ACCESS_KEY')
    }


    # Decode the base64 string
    try:
        image_data = base64.b64decode(base64_string)
    except base64.binascii.Error as e:
        print(f"Error decoding base64 string: {e}")
        return base64_string

    # Initialize a session using Amazon S3
    #Create an S3 client using boto3, which will automatically use the credentials provided by the IAM role associated with the ECS task.
    # s3 = boto3.client('s3')
    s3 = boto3.client('s3', region_name=region, **credentials)

    object_key = f'{uuid.uuid4()}.jpg'
    try:
        # Upload the image to S3
        s3.put_object(Bucket=bucket_name, Key=object_key, Body=image_data, ContentType='image/jpg')

        # Generate the URL to the uploaded image
        url = f"https://{bucket_name}.s3.{region}.amazonaws.com/{object_key}"
        return url
    except NoCredentialsError:
        print("Credentials not available")
        return base64_string


# Function to convert URLs into image and store them as our own picture in our s3 bucket
def uploadURLtoS3(url):
    try:
        response = requests.get(url, stream=True)
        
        s3 = boto3.client('s3')
        object_key = f'{uuid.uuid4()}.jpg'
        s3.upload_fileobj(response.raw, Bucket=bucket_name, Key=object_key, ExtraArgs={"ContentType": response.headers["Content-Type"]})
        s3_url = f"https://{bucket_name}.s3.{region}.amazonaws.com/{object_key}"
        return s3_url
    except requests.exceptions.RequestException as e:
        print(f"Failed to download the image: {e}")
    except NoCredentialsError:
        print("AWS credentials not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return ''

def deleteImageFromS3(url):

    credentials = { 
        'aws_access_key_id': os.getenv('AWS_ACCESS_KEY_ID'),
        'aws_secret_access_key': os.getenv('AWS_SECRET_ACCESS_KEY')
    }

    # Get the key from the url by stripping https://testbucketdrinkx.s3.amazonaws.com/xxxx
    # object_key = url[48:]
    
    if('https://drinkximages.s3.us-east-1.amazonaws.com/' in url):
        object_key =  url.replace('https://drinkximages.s3.us-east-1.amazonaws.com/','')
    else:
        object_key = 'None'

    # if('https://tf-drinkx-prod-fe-images.s3.ap-southeast-1.amazonaws.com/' in url):
    #     object_key =  url.replace('https://drinkximages.s3.us-east-1.amazonaws.com/','')
    # else:
    #     object_key = 'None'

    # Initialize a session using Amazon S3
    s3 = boto3.client('s3', region_name=region, **credentials)
    # s3 = boto3.client('s3')

    try:
        # Upload the image to S3
        if s3.head_object(Bucket=bucket_name, Key=object_key):
            return s3.delete_object(Bucket=bucket_name, Key=object_key)
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            print(f"Key: '{object_key}' does not exist!")
        else:
            print("Something else went wrong")
            raise
        return None
    except NoCredentialsError:
        print("Credentials not available")
        return None
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
# deleteImageFromS3('https://drinkximages.s3.us-east-1.amazonaws.com/b6ef0fed-58a9-4c6c-bdca-0f4f87d5b1de.jpg')