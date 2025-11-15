from app.tasks.celery_app import celery
from app.services.email_service import EmailService
from app.models import db, EmailLog, User, UserEmailPreferences
from datetime import datetime, timedelta


@celery.task(bind=True, max_retries=3)
def send_comment_notification(self, comment_id, review_author_id):
    try:
        # Check user preferences
        prefs = UserEmailPreferences.query.filter_by(
            user_id=review_author_id
        ).first()
        
        if not prefs or not prefs.notify_on_comment:
            return "User has disabled comment notifications"
        
        # Fetch data
        comment = Comment.query.get(comment_id)
        review_author = User.query.get(review_author_id)
        
        # Send email
        email_service = EmailService()
        result = email_service.send_comment_notification(
            recipient=review_author,
            comment=comment
        )
        
        # Log the email
        log = EmailLog(
            user_id=review_author_id,
            email_type='comment_notification',
            recipient_email=review_author.email,
            subject=f"{comment.author.name} commented on your review",
            status='sent',
            ses_message_id=result['MessageId'],
            metadata={
                'comment_id': comment_id,
                'review_id': comment.review_id
            }
        )
        db.session.add(log)
        db.session.commit()
        
        return f"Email sent to {review_author.email}"
        
    except Exception as exc:
        # Retry with exponential backoff
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))


@celery.task(bind=True)
def send_tag_notifications(self, review_id, tagged_user_ids):
    """Send emails to all tagged users"""
    for user_id in tagged_user_ids:
        send_single_tag_notification.delay(review_id, user_id)


@celery.task(bind=True, max_retries=3)
def send_single_tag_notification(self, review_id, user_id):
    try:
        prefs = UserEmailPreferences.query.filter_by(user_id=user_id).first()
        if not prefs or not prefs.notify_on_tag:
            return
        
        review = Review.query.get(review_id)
        user = User.query.get(user_id)
        
        email_service = EmailService()
        result = email_service.send_tag_notification(
            recipient=user,
            review=review
        )
        
        log = EmailLog(
            user_id=user_id,
            email_type='tag_notification',
            recipient_email=user.email,
            subject=f"You were tagged in a review",
            status='sent',
            ses_message_id=result['MessageId'],
            metadata={'review_id': review_id}
        )
        db.session.add(log)
        db.session.commit()
        
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))


@celery.task
def send_inactive_user_reminders():
    """Periodic task to send emails to inactive users"""
    one_month_ago = datetime.utcnow() - timedelta(days=30)
    
    # Find users who haven't been active
    inactive_users = User.query.filter(
        User.last_active_at < one_month_ago,
        User.is_active == True
    ).all()
    
    for user in inactive_users:
        send_inactive_reminder.delay(user.id)
    
    return f"Queued {len(inactive_users)} inactive user emails"

@celery.task(bind=True, max_retries=3)
def send_inactive_reminder(self, user_id):
    try:
        prefs = UserEmailPreferences.query.filter_by(user_id=user_id).first()
        if not prefs or not prefs.notify_inactive_reminder:
            return
        
        user = User.query.get(user_id)
        email_service = EmailService()
        result = email_service.send_inactive_reminder(user)
        
        log = EmailLog(
            user_id=user_id,
            email_type='inactive_reminder',
            recipient_email=user.email,
            subject="We miss you!",
            status='sent',
            ses_message_id=result['MessageId'],
            metadata={}
        )
        db.session.add(log)
        db.session.commit()
        
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))


@celery.task(bind=True, max_retries=3)
def send_new_review_notification(self, review_id, follower_id):
    try:
        prefs = UserEmailPreferences.query.filter_by(user_id=follower_id).first()
        if not prefs or not prefs.notify_on_new_review_from_following:
            return
        
        review = Review.query.get(review_id)
        follower = User.query.get(follower_id)
        
        email_service = EmailService()
        result = email_service.send_new_review_notification(
            recipient=follower,
            review=review
        )
        
        log = EmailLog(
            user_id=follower_id,
            email_type='new_review_notification',
            recipient_email=follower.email,
            subject=f"{review.author.name} posted a new review",
            status='sent',
            ses_message_id=result['MessageId'],
            metadata={'review_id': review_id}
        )
        db.session.add(log)
        db.session.commit()
        
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))