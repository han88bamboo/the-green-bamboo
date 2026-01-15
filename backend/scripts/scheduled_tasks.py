# -----------------------------------------------------------------------------------------
# SCHEDULED TASKS - Background Jobs
# -----------------------------------------------------------------------------------------
# This module handles scheduled/cron tasks that run periodically.
# 
# Tasks:
#   - process_scheduled_stories: Checks for stories whose publicationDate has arrived
#     and sends notifications to subscribers.
#
# Setup:
#   - Uses APScheduler with BackgroundScheduler
#   - Scheduler is initialized when this module is imported
#   - Tasks run on specified intervals
# -----------------------------------------------------------------------------------------

import os
import logging
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

# Import the database manager for connection pooling
from app import db_manager

# Import notification helper
from scripts import notifications

logger = logging.getLogger(__name__)

# Global scheduler instance
scheduler = None


def process_scheduled_stories():
    """
    Checks for stories that were scheduled and whose publicationDate has now passed.
    Sends notifications to topic/newsletter subscribers for newly published stories.
    
    This runs every 5 minutes to catch stories that become published.
    
    Logic:
    1. Find stories where:
       - publicationDate is not NULL
       - publicationDate <= NOW()
       - notificationSent is FALSE or NULL (new column to track)
    2. For each such story, send notifications to subscribers
    3. Mark notificationSent = TRUE to avoid duplicate notifications
    
    Note: Since we don't have a notificationSent column, we'll use a different approach:
    - We'll track processed story IDs in a separate table or use a timestamp check
    - For now, we check stories published in the last 10 minutes that haven't been notified
    """
    try:
        logger.info("process_scheduled_stories: Starting scheduled story check...")
        
        with db_manager.get_cursor() as cursor:
            # Find stories that:
            # 1. Have a publicationDate that has passed (scheduled stories now published)
            # 2. Were not notified yet (notificationSent is NULL or FALSE)
            # 3. Have a topic or newsletter (otherwise no subscribers to notify)
            cursor.execute('''
                SELECT 
                    id,
                    "storyTitle",
                    "topicID",
                    "newsletterID",
                    "publicationDate"
                FROM "stories"
                WHERE "publicationDate" IS NOT NULL
                  AND "publicationDate" <= NOW()
                  AND ("notificationSent" IS NULL OR "notificationSent" = FALSE)
                  AND ("topicID" IS NOT NULL OR "newsletterID" IS NOT NULL)
                ORDER BY "publicationDate" ASC
                LIMIT 100
            ''')
            
            stories = cursor.fetchall()
            
            if not stories:
                logger.info("process_scheduled_stories: No scheduled stories to process.")
                return
            
            logger.info(f"process_scheduled_stories: Found {len(stories)} stories to notify.")
            
            for story in stories:
                story_id = story['id']
                story_title = story['storyTitle']
                topic_id = story['topicID']
                newsletter_id = story['newsletterID']
                
                try:
                    # Send notifications
                    notifications_sent = notifications.notify_story_subscribers(
                        cursor=cursor,
                        story_id=story_id,
                        story_title=story_title,
                        topic_id=topic_id,
                        newsletter_id=newsletter_id
                    )
                    
                    # Mark as notified to prevent duplicate notifications
                    cursor.execute('''
                        UPDATE "stories"
                        SET "notificationSent" = TRUE
                        WHERE id = %s
                    ''', (story_id,))
                    
                    logger.info(f"process_scheduled_stories: Processed story {story_id}, sent {notifications_sent} notifications.")
                    
                except Exception as e:
                    logger.error(f"process_scheduled_stories: Error processing story {story_id}: {str(e)}")
                    continue
        
        logger.info("process_scheduled_stories: Completed scheduled story check.")
        
    except Exception as e:
        logger.error(f"process_scheduled_stories: Error - {str(e)}")


def init_scheduler(app):
    """
    Initialize and start the background scheduler.
    Should be called once during app startup.
    
    Args:
        app: Flask application instance
    """
    global scheduler
    
    if scheduler is not None:
        logger.warning("Scheduler already initialized, skipping...")
        return
    
    try:
        scheduler = BackgroundScheduler()
        
        # Add job to process scheduled stories every 5 minutes
        scheduler.add_job(
            func=process_scheduled_stories,
            trigger=IntervalTrigger(minutes=5),
            id='process_scheduled_stories',
            name='Process scheduled stories and send notifications',
            replace_existing=True
        )
        
        # Start the scheduler
        scheduler.start()
        logger.info("Background scheduler started successfully.")
        
        # Register shutdown on app context teardown
        @app.teardown_appcontext
        def shutdown_scheduler(exception=None):
            global scheduler
            if scheduler and scheduler.running:
                scheduler.shutdown(wait=False)
                logger.info("Background scheduler shut down.")
        
    except Exception as e:
        logger.error(f"Failed to initialize scheduler: {str(e)}")


def shutdown_scheduler():
    """Manually shutdown the scheduler if needed."""
    global scheduler
    if scheduler and scheduler.running:
        scheduler.shutdown(wait=False)
        scheduler = None
        logger.info("Background scheduler shut down manually.")
