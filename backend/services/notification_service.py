import boto3
from jinja2 import Environment, FileSystemLoader
from flask import current_app
from datetime import datetime
import os

class EmailService:
    def __init__(self):
        self.ses_client = boto3.client(
            'ses',
            region_name=current_app.config['AWS_REGION'],
            aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY']
        )
        self.from_email = current_app.config['FROM_EMAIL']
        self.from_name = current_app.config.get('FROM_NAME', current_app.config['APP_NAME'])
        
        # Setup Jinja2 environment for email templates
        template_dir = os.path.join(current_app.root_path, 'templates', 'emails')
        self.jinja_env = Environment(loader=FileSystemLoader(template_dir))
        
        # Add custom filters
        self.jinja_env.filters['format_date'] = self.format_date
        self.jinja_env.filters['truncate_text'] = self.truncate_text
    

    @staticmethod
    def format_date(date, format='%B %d, %Y'):
        """Format datetime for email display"""
        if isinstance(date, str):
            date = datetime.fromisoformat(date)
        return date.strftime(format)
    

    @staticmethod
    def truncate_text(text, length=200):
        """Truncate text with ellipsis"""
        if len(text) <= length:
            return text
        return text[:length].rsplit(' ', 1)[0] + '...'
    

    def _get_base_context(self):
        """Get common context variables for all emails"""
        return {
            'app_name': current_app.config['APP_NAME'],
            'app_url': current_app.config['FRONTEND_URL'],
            'support_email': current_app.config.get('SUPPORT_EMAIL', 'support@example.com'),
            'social_twitter': current_app.config.get('SOCIAL_TWITTER', '#'),
            'social_instagram': current_app.config.get('SOCIAL_INSTAGRAM', '#'),
            'social_facebook': current_app.config.get('SOCIAL_FACEBOOK', '#'),
            'current_year': datetime.now().year
        }
    

    def render_template(self, template_name, **context):
        """Render email template with context"""
        base_context = self._get_base_context()
        full_context = {**base_context, **context}
        
        template = self.jinja_env.get_template(template_name)
        return template.render(**full_context)
    

    def send_email(self, to_email, subject, html_body, text_body=None, reply_to=None):
        """Generic email sender using SES"""
        source = f"{self.from_name} <{self.from_email}>"
        
        message = {
            'Subject': {'Data': subject, 'Charset': 'UTF-8'},
            'Body': {
                'Html': {'Data': html_body, 'Charset': 'UTF-8'}
            }
        }
        
        if text_body:
            message['Body']['Text'] = {'Data': text_body, 'Charset': 'UTF-8'}
        
        params = {
            'Source': source,
            'Destination': {'ToAddresses': [to_email]},
            'Message': message,
            'ConfigurationSetName': current_app.config.get('SES_CONFIGURATION_SET', 'EmailTracking')
        }
        
        if reply_to:
            params['ReplyToAddresses'] = [reply_to]
        
        try:
            response = self.ses_client.send_email(**params)
            return response
        except Exception as e:
            current_app.logger.error(f"Failed to send email to {to_email}: {str(e)}")
            raise
    

    def send_comment_notification(self, recipient, comment):
        """Send notification when someone comments on user's review"""
        html = self.render_template(
            'comment_notification.html',
            recipient_name=recipient.name,
            commenter_name=comment.author.name,
            comment_text=comment.text,
            comment_time=comment.created_at,
            review_title=comment.review.title,
            review_url=f"{current_app.config['FRONTEND_URL']}/reviews/{comment.review.id}",
            unsubscribe_url=f"{current_app.config['FRONTEND_URL']}/settings/notifications?token={recipient.unsubscribe_token}"
        )
        
        subject = f"{comment.author.name} commented on your review"
        
        return self.send_email(
            to_email=recipient.email,
            subject=subject,
            html_body=html
        )
    

    def send_upvote_notification(self, recipient, upvoter, review):
        """Send notification when someone upvotes user's review"""
        html = self.render_template(
            'upvote_notification.html',
            recipient_name=recipient.name,
            upvoter_name=upvoter.name,
            review_title=review.title,
            review_excerpt=review.content[:150],
            total_upvotes=review.upvotes_count,
            review_url=f"{current_app.config['FRONTEND_URL']}/reviews/{review.id}",
            unsubscribe_url=f"{current_app.config['FRONTEND_URL']}/settings/notifications?token={recipient.unsubscribe_token}"
        )
        
        subject = f"🎉 {upvoter.name} upvoted your review!"
        
        return self.send_email(
            to_email=recipient.email,
            subject=subject,
            html_body=html
        )
    

    def send_tag_notification(self, recipient, review):
        """Send notification when user is tagged in a review"""
        html = self.render_template(
            'tag_notification.html',
            recipient_name=recipient.name,
            author_name=review.author.name,
            review_title=review.title,
            review_excerpt=review.content[:200],
            review_date=review.created_at,
            category=review.category.name if review.category else 'General',
            review_url=f"{current_app.config['FRONTEND_URL']}/reviews/{review.id}",
            unsubscribe_url=f"{current_app.config['FRONTEND_URL']}/settings/notifications?token={recipient.unsubscribe_token}"
        )
        
        subject = f"{review.author.name} tagged you in a review"
        
        return self.send_email(
            to_email=recipient.email,
            subject=subject,
            html_body=html
        )
    

    def send_new_review_notification(self, recipient, review):
        """Send notification when someone you follow posts a review"""
        html = self.render_template(
            'new_review_notification.html',
            recipient_name=recipient.name,
            author_name=review.author.name,
            review_title=review.title,
            review_excerpt=review.content[:200],
            review_date=review.created_at,
            category=review.category.name if review.category else 'General',
            rating=review.rating if hasattr(review, 'rating') else None,
            review_url=f"{current_app.config['FRONTEND_URL']}/reviews/{review.id}",
            unsubscribe_url=f"{current_app.config['FRONTEND_URL']}/settings/notifications?token={recipient.unsubscribe_token}"
        )
        
        subject = f"📝 {review.author.name} posted a new review"
        
        return self.send_email(
            to_email=recipient.email,
            subject=subject,
            html_body=html
        )
    

    def send_inactive_reminder(self, user, stats=None):
        """Send reminder to inactive users"""
        # Gather stats if not provided
        if stats is None:
            stats = {
                'new_reviews_count': self._count_new_reviews_since(user.last_active_at),
                'new_comments_count': self._count_new_comments_on_user_reviews(user.id, user.last_active_at),
                'new_upvotes_count': self._count_new_upvotes_on_user_reviews(user.id, user.last_active_at),
                'trending_reviews': self._get_trending_reviews(limit=1)
            }
        
        # Get personalized content recommendations
        personalized_content = self._get_personalized_recommendations(user)
        
        html = self.render_template(
            'inactive_reminder.html',
            user_name=user.name,
            new_reviews_count=stats['new_reviews_count'],
            new_comments_count=stats['new_comments_count'],
            new_upvotes_count=stats['new_upvotes_count'],
            trending_reviews=stats.get('trending_reviews', []),
            personalized_content=personalized_content,
            unsubscribe_url=f"{current_app.config['FRONTEND_URL']}/settings/notifications?token={user.unsubscribe_token}"
        )
        
        subject = f"We miss you, {user.name}! See what's new"
        
        return self.send_email(
            to_email=user.email,
            subject=subject,
            html_body=html
        )
    

    def send_welcome_email(self, user):
        """Send welcome email to new users"""
        html = self.render_template(
            'welcome.html',
            user_name=user.name,
            unsubscribe_url=f"{current_app.config['FRONTEND_URL']}/settings/notifications?token={user.unsubscribe_token}"
        )
        
        subject = f"Welcome to {current_app.config['APP_NAME']}, {user.name}!"
        
        return self.send_email(
            to_email=user.email,
            subject=subject,
            html_body=html
        )
    

    # Helper methods for stats
    def _count_new_reviews_since(self, since_date):
        """Count new reviews since date"""
        from app.models import Review
        return Review.query.filter(Review.created_at > since_date).count()
    

    def _count_new_comments_on_user_reviews(self, user_id, since_date):
        """Count new comments on user's reviews"""
        from app.models import Comment, Review
        return Comment.query.join(Review).filter(
            Review.author_id == user_id,
            Comment.created_at > since_date,
            Comment.author_id != user_id  
        ).count()
    

    def _count_new_upvotes_on_user_reviews(self, user_id, since_date):
        """Count new upvotes on user's reviews"""
        from app.models import Upvote, Review
        return Upvote.query.join(Review).filter(
            Review.author_id == user_id,
            Upvote.created_at > since_date
        ).count()
    

    def _get_trending_reviews(self, limit=5):
        """Get trending reviews"""
        from app.models import Review
        return Review.query.order_by(
            Review.upvotes_count.desc(),
            Review.created_at.desc()
        ).limit(limit).all()
    
    
    def _get_personalized_recommendations(self, user, limit=3):
        """Get personalized content recommendations"""
        # This would be more sophisticated in production
        # For now, return reviews from followed users or popular categories
        from app.models import Review
        
        recommendations = []
        followed_reviews = Review.query.join(
            'author'
        ).filter(
            Review.author_id.in_([f.id for f in user.following])
        ).order_by(Review.created_at.desc()).limit(limit).all()
        
        for review in followed_reviews:
            recommendations.append({
                'title': review.title,
                'description': f"By {review.author.name} • {review.created_at.strftime('%B %d')}",
                'url': f"{current_app.config['FRONTEND_URL']}/reviews/{review.id}"
            })
        
        return recommendations