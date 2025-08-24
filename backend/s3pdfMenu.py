import base64
import boto3
from botocore.exceptions import NoCredentialsError
from botocore.exceptions import ClientError
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

# Get the purpose variable from the environment
purpose = os.getenv('PURPOSE')
print(f"Purpose: {purpose}")

# For deployment (comment out for local launch)
if purpose == 'production':
    bucket_name = 'tf-drinkx-prod-fe-images'
    region='ap-southeast-1'
else:
    bucket_name = 'drinkximages'
    region='us-east-1'


def uploadBase64PDFToS3(base64_string):
    credentials = None  # Initialize credentials to avoid reference error

    # For local development (comment out before deployment)
    if purpose == 'development':
        credentials = { 
            'aws_access_key_id': os.getenv('AWS_ACCESS_KEY_ID'),
            'aws_secret_access_key': os.getenv('AWS_SECRET_ACCESS_KEY')
        }

    # Decode the base64 string
    try:
        pdf_data = base64.b64decode(base64_string)
    except Exception as e:
        print(f"Error decoding base64 string: {e}")
        return None

    # Validate PDF file
    if not validatePDFFile(pdf_data):
        return None

    # Initialize S3 client
    if purpose == 'production':
        s3 = boto3.client('s3')
    else:
        s3 = boto3.client('s3', region_name=region, **credentials) if credentials else boto3.client('s3', region_name=region)

    # Generate unique filename for PDF
    object_key = f'menus/{uuid.uuid4()}.pdf'
    
    try:
        # Upload the PDF to S3
        s3.put_object(
            Bucket=bucket_name, 
            Key=object_key, 
            Body=pdf_data, 
            ContentType='application/pdf',
            ContentDisposition='inline'  # Allow viewing in browser
        )

        # Generate the URL to the uploaded PDF
        url = f"https://{bucket_name}.s3.{region}.amazonaws.com/{object_key}"
        return url
    except NoCredentialsError:
        print("Credentials not available")
        return None
    except Exception as e:
        print(f"Error uploading PDF to S3: {e}")
        return None


def deletePDFFromS3(url):
    credentials = None  # Initialize credentials to avoid reference error

    # For local development (comment out before deployment)
    if purpose == 'development':
        credentials = { 
            'aws_access_key_id': os.getenv('AWS_ACCESS_KEY_ID'),
            'aws_secret_access_key': os.getenv('AWS_SECRET_ACCESS_KEY')
        }

    # Extract object key from URL
    if('https://tf-drinkx-prod-fe-images.s3.ap-southeast-1.amazonaws.com/' in url):
        object_key = url.replace('https://tf-drinkx-prod-fe-images.s3.ap-southeast-1.amazonaws.com/','')
    elif('https://drinkximages.s3.us-east-1.amazonaws.com/' in url):
        object_key = url.replace('https://drinkximages.s3.us-east-1.amazonaws.com/','')
    else:
        print(f"URL format not recognized: {url}")
        return None

    # Initialize S3 client
    if purpose == 'production':
        s3 = boto3.client('s3')
    else:
        s3 = boto3.client('s3', region_name=region, **credentials) if credentials else boto3.client('s3', region_name=region)

    try:
        # Check if object exists and delete it
        s3.head_object(Bucket=bucket_name, Key=object_key)
        result = s3.delete_object(Bucket=bucket_name, Key=object_key)
        print(f"Successfully deleted PDF: {object_key}")
        return result
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            print(f"PDF file '{object_key}' does not exist!")
        else:
            print(f"Error deleting PDF: {e}")
        return None
    except NoCredentialsError:
        print("Credentials not available")
        return None


def validatePDFFile(pdf_data):
    """
    Validate that the uploaded file is actually a PDF
    """
    try:
        # Check PDF magic number (first 4 bytes should be %PDF)
        if pdf_data[:4] == b'%PDF':
            return True
        else:
            print("File is not a valid PDF")
            return False
    except Exception as e:
        print(f"Error validating PDF: {e}")
        return False


# Example usage
if __name__ == "__main__":
    # Example base64 string for a PDF (you should use your actual base64 string)
    # base64_pdf_string = ''
    # url = uploadBase64PDFToS3(base64_pdf_string)
    # if url:
    #     print(f"PDF URL: {url}")
    pass
