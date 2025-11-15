import boto3
from flask import current_app, render_template
from botocore.exceptions import ClientError

class EmailService:
    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.ses_client = boto3.client(
            'ses',
            region_name=app.config['AWS_REGION'],
            aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY']
        )
        self.from_email = app.config['FROM_EMAIL']
        self.frontend_url = app.config['FRONTEND_URL']

    # Helper to render email templates
    def _render(self, template, **context):
        return render_template(f"emails/{template}.html", **context)

    # Helper to generate review URL
    def _review_url(self, review_id):
        return f"{self.frontend_url}/reviews/{review_id}"

    # General method to send email
    def send_email(self, to_email, subject, html_body, text_body=None):
        message = {
            'Subject': {'Data': subject},
            'Body': {'Html': {'Data': html_body}}
        }
        if text_body:
            message['Body']['Text'] = {'Data': text_body}

        try:
            return self.ses_client.send_email(
                Source=self.from_email,
                Destination={'ToAddresses': [to_email]},
                Message=message,
                ConfigurationSetName='EmailTracking'
            )
        except ClientError as e:
            current_app.logger.error(f"SES error sending email: {e}")
            return {"error": str(e)}
    
    # notification email when a comment is made on a review
    def send_comment_notification(self, recipient, comment):
        html = self._render(
            "comment_notification",
            recipient_name=recipient.name,
            commenter_name=comment.author.name,
            comment_text=comment.text,
            review_title=comment.review.title,
            review_url=self._review_url(comment.review.id)
        )

        subject = f"{comment.author.name} commented on your review"

        return self.send_email(recipient.email, subject, html)
    
    # notification email when a user is tagged in a review
    def send_tag_notification(self, recipient, review):
        html = self._render(
            "tag_notification",
            recipient_name=recipient.name,
            author_name=review.author.name,
            review_title=review.title,
            review_url=self._review_url(review.id)
        )

        subject = f"You were tagged in a review by {review.author.name}"

        return self.send_email(recipient.email, subject, html)
    
    # notification email when a new review is posted
    def send_new_review_notification(self, recipient, review):
        html = self._render(
            "new_review_notification",
            recipient_name=recipient.name,
            author_name=review.author.name,
            review_title=review.title,
            review_excerpt=review.content[:200],
            review_url=self._review_url(review.id)
        )

        subject = f"{review.author.name} posted a new review"

        return self.send_email(recipient.email, subject, html)
    
    # notification email to inactive users
    def send_inactive_reminder(self, user):
        html = self._render(
            "inactive_reminder",
            user_name=user.name,
            app_url=self.frontend_url
        )

        subject = "We miss you! See what's new"
        return self.send_email(user.email, subject, html)