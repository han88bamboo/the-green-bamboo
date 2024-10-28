import os
from flask import g
from flask_mail import Message
import logging

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

import boto3
from botocore.exceptions import ClientError
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

logger = logging.getLogger(__name__)

AWS_REGION = os.getenv("AWS_REGION", "ap-southeast-1")
os.environ["AWS_DEFAULT_REGION"] = AWS_REGION
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", None)
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", None)
AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN", None)


def send_email(
    subject: str,
    recipient: str,
    body: str,
):
    mail = g.mail
    sender = "Drink-X <noreply@drink-x.com>"
    msg = Message(subject, sender=sender, recipients=[recipient],)
    msg.body = body
    mail.send(msg)


def send_email_aws(
    region_name: str = None,
    profile_name: str = None,
    subject: str =  None,
    recipient: str =  None,
    body: str =  None,
):
    if not region_name:
        region_name = AWS_REGION

    SENDER = "Drink-X <noreply@drink-x.com>"
    RECIPIENT = recipient
    SUBJECT = subject
    BODY_TEXT = body
    CHARSET = "utf-8"

    session = boto3.session.Session(
        region_name=region_name,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        aws_session_token=AWS_SESSION_TOKEN,
    )
    client = session.client(service_name="sesv2", region_name=region_name)

    try:
        logger.info(
            f"Sending mail using AWS SES [region={region_name}, profile={profile_name}]"
        )

        msg = MIMEMultipart('mixed')
        msg['Subject'] = SUBJECT 
        msg['From'] = SENDER 
        msg['To'] = RECIPIENT
        
        msg_body = MIMEMultipart('alternative')
        textpart = MIMEText(BODY_TEXT.encode(CHARSET), 'plain', CHARSET)
        msg_body.attach(textpart)
        msg.attach(msg_body)

        strmsg = str(msg)
        body = bytes (strmsg, 'utf-8')

        client = boto3.client('sesv2')
        response = client.send_email(
            FromEmailAddress=SENDER,
            Destination={
                'ToAddresses': [RECIPIENT]
            },
            Content={
                'Raw': {
                    'Data': body
                }
            }
        )
        logger.info(response)
    except ClientError as e:
        logger.error(f"Failed to send mail: {e}")
        raise e
