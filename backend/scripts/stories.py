# -----------------------------------------------------------------------------------------
# STORIES FEATURE - Backend API Endpoints
# -----------------------------------------------------------------------------------------
# Routes for Stories feature (long-form content publishing system similar to Medium/Substack)
# 
# TOPICS Routes:
#   /createTopic (POST) - Create a new topic for categorizing stories
#   /getTopics/<offset> (GET) - Get paginated list of topics
#   /getTopicswSearch/<offset>/<search> (GET) - Search topics
#   /getSpecificTopicInfo/<topicID> (GET) - Get specific topic details
#   /subscribeTopic (POST) - Subscribe to a topic
#   /unsubscribeTopic (DELETE) - Unsubscribe from a topic
#   /getTopicStories/<topicID>/<offset> (GET) - Get stories under a topic
#
# NEWSLETTERS Routes:
#   /createNewsletter (POST) - Create a new newsletter
#   /getNewsletters/<offset> (GET) - Get paginated list of newsletters
#   /getNewsletterswSearch/<offset>/<search> (GET) - Search newsletters
#   /getSpecificNewsletterInfo/<newsletterID> (GET) - Get specific newsletter details
#   /getNewsletterStories/<newsletterID>/<offset> (GET) - Get stories in a newsletter
#   /getUserNewsletters/<userID>/<userType> (GET) - Get user's newsletters (for dropdown)
#   /subscribeNewsletter (POST) - Subscribe to a newsletter
#   /unsubscribeNewsletter (DELETE) - Unsubscribe from a newsletter
#
# STORIES Routes:
#   /createStory (POST) - Create a new story
#   /getStory/<storyID> (GET) - Get a specific story
#   /editStory (PUT) - Edit an existing story
#   /deleteStory (DELETE) - Delete a story
#   /getUserStories/<userID>/<userType>/<offset> (GET) - Get user's stories
#   /likeStory (POST) - Like a story
#   /unlikeStory (DELETE) - Unlike a story
#
# COMMENTS Routes:
#   /createStoryComment (POST) - Create a comment on a story
#   /getStoryComments/<storyID>/<offset> (GET) - Get comments for a story
#   /likeStoryComment (POST) - Like a comment
#   /dislikeStoryComment (POST) - Dislike a comment
#   /deleteStoryComment (DELETE) - Delete a comment
#
# Database Tables Used:
#   - topics
#   - topicSubscribers
#   - newsletters
#   - newsletterPatrons
#   - stories
#   - storyPatrons
#   - storiesLikes
#   - storyComments
#   - storyCommentsLikes
#   - storyCommentsDislikes
#   - storyHashtags
# -----------------------------------------------------------------------------------------

import os
import re
from flask import Blueprint, request, jsonify
from datetime import datetime
from scripts import notifications

# Import the database manager for connection pooling
from app import db_manager

# Use to upload image to S3
import s3Images

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)


# -----------------------------------------------------------------------------------------
# HELPER FUNCTIONS
# -----------------------------------------------------------------------------------------

def normalize_name_for_uniqueness(name):
    """
    Strip emojis and lowercase for case-insensitive uniqueness comparison.
    "Wine Stories 🍷" and "wine stories 🥂" would both become "wine stories"
    """
    # Remove emojis using regex
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002600-\U000026FF"  # misc symbols
        "\U00002700-\U000027BF"  # dingbats
        "\U0001F900-\U0001F9FF"  # supplemental symbols
        "\U0001FA00-\U0001FAFF"  # chess, extended-A
        "\U0001F018-\U0001F270"  # various
        "]+",
        flags=re.UNICODE
    )
    stripped = emoji_pattern.sub('', name)
    return stripped.strip().lower()


def validate_topic_name(name):
    """
    Validate topic name:
    - Length: 4-255 characters
    Returns: (is_valid: bool, error_message: str or None)
    """
    if not name or len(name.strip()) < 4:
        return False, "Topic name must be at least 4 characters."
    if len(name) > 255:
        return False, "Topic name cannot exceed 255 characters."
    return True, None


def validate_newsletter_name(name):
    """
    Validate newsletter name:
    - Length: 4-255 characters
    Returns: (is_valid: bool, error_message: str or None)
    """
    if not name or len(name.strip()) < 4:
        return False, "Newsletter name must be at least 4 characters."
    if len(name) > 255:
        return False, "Newsletter name cannot exceed 255 characters."
    return True, None


def validate_story_title(title):
    """
    Validate story title:
    - Length: 1-500 characters
    Returns: (is_valid: bool, error_message: str or None)
    """
    if not title or len(title.strip()) < 1:
        return False, "Story title is required."
    if len(title) > 500:
        return False, "Story title cannot exceed 500 characters."
    return True, None


def get_creator_info(cursor, creator_id, creator_type):
    """
    Get username, displayName, and photo for story/topic/newsletter creator.
    Returns dict with creatorUsername, creatorDisplayName, creatorPhoto or None if not found.
    """
    if creator_type == 'user':
        cursor.execute(
            'SELECT "username", "displayName", "photo" FROM "users" WHERE id = %s',
            (creator_id,)
        )
    elif creator_type == 'producer':
        cursor.execute(
            'SELECT "username", "producerName" as "displayName", "photo" FROM "producers" WHERE id = %s',
            (creator_id,)
        )
    elif creator_type == 'venue':
        cursor.execute(
            'SELECT "username", "venueName" as "displayName", "photo" FROM "venues" WHERE id = %s',
            (creator_id,)
        )
    else:
        return None
    
    result = cursor.fetchone()
    if result:
        return {
            'creatorUsername': result.get('username'),
            'creatorDisplayName': result.get('displayName'),
            'creatorPhoto': result.get('photo')
        }
    return None


def get_user_info_by_id(cursor, user_id, user_type):
    """
    Retrieve user information using the user's ID and user type.
    Returns dict with id, displayName, photo, username, userType or None if not found.
    """
    if user_type == 'user':
        cursor.execute(
            'SELECT "id", "displayName", "photo", "username" FROM "users" WHERE id = %s',
            (user_id,)
        )
    elif user_type == 'producer':
        cursor.execute(
            'SELECT "id", "producerName" as "displayName", "photo", "username" FROM "producers" WHERE id = %s',
            (user_id,)
        )
    elif user_type == 'venue':
        cursor.execute(
            'SELECT "id", "venueName" as "displayName", "photo", "username" FROM "venues" WHERE id = %s',
            (user_id,)
        )
    else:
        return None
    
    user_info = cursor.fetchone()
    if user_info:
        user_info = dict(user_info)
        user_info['userType'] = user_type
        return user_info
    return None


def get_story_preview_photos(cursor, topic_id=None, newsletter_id=None, limit=3):
    """
    Get up to 3 recent stories with photos for topic/newsletter preview.
    Returns list of dicts with 'title' and 'photo' keys.
    """
    if topic_id:
        cursor.execute('''
            SELECT "storyTitle" as "title", "storyPhotos"[1] as "photo"
            FROM "stories"
            WHERE "topicID" = %s
              AND "storyPhotos" IS NOT NULL 
              AND array_length("storyPhotos", 1) > 0
            ORDER BY "publishingDate" DESC
            LIMIT %s
        ''', (topic_id, limit))
    elif newsletter_id:
        cursor.execute('''
            SELECT "storyTitle" as "title", "storyPhotos"[1] as "photo"
            FROM "stories"
            WHERE "newsletterID" = %s
              AND "storyPhotos" IS NOT NULL 
              AND array_length("storyPhotos", 1) > 0
            ORDER BY "publishingDate" DESC
            LIMIT %s
        ''', (newsletter_id, limit))
    else:
        return []
    
    results = cursor.fetchall()
    return [{'title': r['title'], 'photo': r['photo']} for r in results] if results else []


def process_hashtags(cursor, hashtags_list):
    """
    Process hashtags: insert new ones into storyHashtags table if they don't exist.
    Returns the list of hashtags (normalized).
    
    TODO: Revisit hashtag feature - consider implementing similar to varietal tags in listings table
    """
    if not hashtags_list:
        return []
    
    normalized_hashtags = []
    for tag in hashtags_list:
        # Normalize: strip whitespace, lowercase
        normalized = tag.strip().lower()
        if not normalized:
            continue
        normalized_hashtags.append(normalized)
        
        # Insert into storyHashtags if not exists
        cursor.execute('''
            INSERT INTO "storyHashtags" ("hashtag")
            VALUES (%s)
            ON CONFLICT ("hashtag") DO NOTHING
        ''', (normalized,))
    
    return normalized_hashtags


# =========================================================================================
# TOPICS ENDPOINTS
# =========================================================================================

# -----------------------------------------------------------------------------------------
# [POST] createTopic
# Purpose: Create a new topic for categorizing stories
# Used: CreateTopic.vue
# Input:
#   1. creatorID - the user's ID in the 'users', 'producers' or 'venues' table
#   2. creatorType - 'user', 'producer' or 'venue'
#   3. topicName - name of the topic (4-255 chars)
#   4. topicDesc - description (optional)
#   5. drinkTypes - array of drink types like ['Wine', 'Whisky'] (optional)
#   6. image64 - base64 banner image (optional)
# Output: Possible return codes:
#   201 - Topic created successfully
#   400 - Validation error
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/createTopic', methods=['POST'])
def create_topic():
    # TODO: Implement createTopic endpoint
    # - Validate topic name (4-255 chars)
    # - Check for duplicate topic name (case-insensitive, global)
    # - Upload banner image to S3 if provided
    # - Insert into topics table
    # - Return created topic ID
    return jsonify({
        'code': 501,
        'message': 'createTopic endpoint not yet implemented'
    }), 501


# -----------------------------------------------------------------------------------------
# [GET] getTopics/<offset>
# Purpose: Get paginated list of topics with creator info and preview stories
# Used: BrowseStoryTopics.vue
# Input: offset (path param) - starting position (0, 12, 24, ...)
# Output:
#   200 - List of topics with creator info and preview stories
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/getTopics/<offset>', methods=['GET'])
def get_topics(offset):
    # TODO: Implement getTopics endpoint
    # - Query topics table with pagination (12 per page)
    # - Join with creator info (users/producers/venues)
    # - Get story count per topic
    # - Get subscriber count per topic  
    # - Get preview stories with photos (up to 3)
    # - Sort by most recent (dateCreated DESC)
    return jsonify({
        'code': 501,
        'message': 'getTopics endpoint not yet implemented'
    }), 501


# -----------------------------------------------------------------------------------------
# [GET] getTopicswSearch/<offset>/<search>
# Purpose: Search topics by name
# Used: BrowseStoryTopics.vue
# Input: offset, search (path params)
# Output:
#   200 - List of matching topics
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/getTopicswSearch/<offset>/<search>', methods=['GET'])
def get_topics_with_search(offset, search):
    # TODO: Implement getTopicswSearch endpoint
    # - Same as getTopics but with WHERE clause for search
    # - Use ILIKE for case-insensitive search on topicName
    return jsonify({
        'code': 501,
        'message': 'getTopicswSearch endpoint not yet implemented'
    }), 501


# -----------------------------------------------------------------------------------------
# [GET] getSpecificTopicInfo/<topicID>
# Purpose: Get detailed info for a specific topic
# Used: SpecificStoryTopic.vue
# Input: topicID (path param)
# Output:
#   200 - Topic details with creator info, subscriber count, story count
#   404 - Topic not found
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/getSpecificTopicInfo/<topicID>', methods=['GET'])
def get_specific_topic_info(topicID):
    # TODO: Implement getSpecificTopicInfo endpoint
    # - Query topic by ID
    # - Get creator info
    # - Count subscribers
    # - Count stories
    # - Return full topic details
    return jsonify({
        'code': 501,
        'message': 'getSpecificTopicInfo endpoint not yet implemented'
    }), 501


# -----------------------------------------------------------------------------------------
# [POST] subscribeTopic
# Purpose: Subscribe to a topic (instant, no approval needed)
# Used: SpecificStoryTopic.vue
# Input:
#   1. topicID - the topic to subscribe to
#   2. userID - the user subscribing
#   3. userType - 'user', 'producer', or 'venue'
# Output:
#   201 - Subscribed successfully
#   400 - Already subscribed or missing data
#   404 - Topic not found
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/subscribeTopic', methods=['POST'])
def subscribe_topic():
    # TODO: Implement subscribeTopic endpoint
    # - Verify topic exists
    # - Check if already subscribed
    # - Insert into topicSubscribers table
    return jsonify({
        'code': 501,
        'message': 'subscribeTopic endpoint not yet implemented'
    }), 501


# -----------------------------------------------------------------------------------------
# [DELETE] unsubscribeTopic
# Purpose: Unsubscribe from a topic
# Used: SpecificStoryTopic.vue
# Input:
#   1. topicID - the topic to unsubscribe from
#   2. userID - the user unsubscribing
#   3. userType - 'user', 'producer', or 'venue'
# Output:
#   200 - Unsubscribed successfully
#   400 - Not subscribed or missing data
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/unsubscribeTopic', methods=['DELETE'])
def unsubscribe_topic():
    # TODO: Implement unsubscribeTopic endpoint
    # - Check if subscribed
    # - Delete from topicSubscribers table
    return jsonify({
        'code': 501,
        'message': 'unsubscribeTopic endpoint not yet implemented'
    }), 501


# -----------------------------------------------------------------------------------------
# [GET] getTopicStories/<topicID>/<offset>
# Purpose: Get paginated stories under a specific topic
# Used: SpecificStoryTopic.vue
# Input: topicID, offset (path params)
# Output:
#   200 - List of stories under the topic
#   404 - Topic not found
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/getTopicStories/<topicID>/<offset>', methods=['GET'])
def get_topic_stories(topicID, offset):
    # TODO: Implement getTopicStories endpoint
    # - Verify topic exists
    # - Query stories where topicID matches
    # - Include creator info for each story
    # - Include like count
    # - Include comment count
    # - Sort by publishingDate DESC (most recent first)
    # - Paginate (12 per page)
    return jsonify({
        'code': 501,
        'message': 'getTopicStories endpoint not yet implemented'
    }), 501


# =========================================================================================
# NEWSLETTERS ENDPOINTS
# =========================================================================================

# -----------------------------------------------------------------------------------------
# [POST] createNewsletter
# Purpose: Create a new newsletter for the user's stories
# Used: CreateNewsletter.vue, UserStories.vue (modal)
# Input:
#   1. creatorUserID - the user's ID
#   2. creatorUserType - 'user', 'producer' or 'venue'
#   3. newsletterName - name of the newsletter (4-255 chars)
#   4. newsletterDesc - description (optional)
#   5. image64 - base64 banner image (optional)
#   6. isFree - boolean (default true for MVP)
#   7. subscriptionPrice - decimal (ignored for MVP, all treated as free)
# Output:
#   201 - Newsletter created successfully
#   400 - Validation error or duplicate name
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/createNewsletter', methods=['POST'])
def create_newsletter():
    # TODO: Implement createNewsletter endpoint
    # - Validate newsletter name (4-255 chars)
    # - Check for duplicate newsletter name (case-insensitive, global)
    # - Upload banner image to S3 if provided
    # - Insert into newsletters table
    # - Return created newsletter ID
    return jsonify({
        'code': 501,
        'message': 'createNewsletter endpoint not yet implemented'
    }), 501


# -----------------------------------------------------------------------------------------
# [GET] getNewsletters/<offset>
# Purpose: Get paginated list of newsletters with creator info
# Used: BrowseStoryNewsletters.vue
# Input: offset (path param) - starting position (0, 12, 24, ...)
# Output:
#   200 - List of newsletters with creator info and preview stories
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/getNewsletters/<offset>', methods=['GET'])
def get_newsletters(offset):
    # TODO: Implement getNewsletters endpoint
    # - Query newsletters table with pagination (12 per page)
    # - Join with creator info (users/producers/venues)
    # - Get story count per newsletter
    # - Get patron count per newsletter
    # - Get preview stories with photos (up to 3)
    # - Sort by most recent (dateCreated DESC)
    return jsonify({
        'code': 501,
        'message': 'getNewsletters endpoint not yet implemented'
    }), 501


# -----------------------------------------------------------------------------------------
# [GET] getNewsletterswSearch/<offset>/<search>
# Purpose: Search newsletters by name
# Used: BrowseStoryNewsletters.vue
# Input: offset, search (path params)
# Output:
#   200 - List of matching newsletters
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/getNewsletterswSearch/<offset>/<search>', methods=['GET'])
def get_newsletters_with_search(offset, search):
    # TODO: Implement getNewsletterswSearch endpoint
    # - Same as getNewsletters but with WHERE clause for search
    # - Use ILIKE for case-insensitive search on newsletterName
    return jsonify({
        'code': 501,
        'message': 'getNewsletterswSearch endpoint not yet implemented'
    }), 501


# -----------------------------------------------------------------------------------------
# [GET] getSpecificNewsletterInfo/<newsletterID>
# Purpose: Get detailed info for a specific newsletter
# Used: SpecificStoryNewsletter.vue
# Input: newsletterID (path param)
# Output:
#   200 - Newsletter details with creator info, patron count, story count
#   404 - Newsletter not found
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/getSpecificNewsletterInfo/<newsletterID>', methods=['GET'])
def get_specific_newsletter_info(newsletterID):
    # TODO: Implement getSpecificNewsletterInfo endpoint
    # - Query newsletter by ID
    # - Get creator info
    # - Count patrons (subscribers)
    # - Count stories
    # - Return full newsletter details
    return jsonify({
        'code': 501,
        'message': 'getSpecificNewsletterInfo endpoint not yet implemented'
    }), 501


# -----------------------------------------------------------------------------------------
# [GET] getNewsletterStories/<newsletterID>/<offset>
# Purpose: Get paginated stories in a specific newsletter
# Used: SpecificStoryNewsletter.vue
# Input: newsletterID, offset (path params)
# Output:
#   200 - List of stories in the newsletter
#   404 - Newsletter not found
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/getNewsletterStories/<newsletterID>/<offset>', methods=['GET'])
def get_newsletter_stories(newsletterID, offset):
    # TODO: Implement getNewsletterStories endpoint
    # - Verify newsletter exists
    # - Query stories where newsletterID matches
    # - Include creator info for each story
    # - Include like count
    # - Include comment count
    # - Sort by publishingDate DESC (most recent first)
    # - Paginate (12 per page)
    return jsonify({
        'code': 501,
        'message': 'getNewsletterStories endpoint not yet implemented'
    }), 501


# -----------------------------------------------------------------------------------------
# [GET] getUserNewsletters/<userID>/<userType>
# Purpose: Get all newsletters created by a specific user (for dropdown in create story modal)
# Used: UserStories.vue, SpecificStoryTopic.vue, SpecificStoryNewsletter.vue (create story modal)
# Input: userID, userType (path params)
# Output:
#   200 - List of user's newsletters (id, name)
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/getUserNewsletters/<userID>/<userType>', methods=['GET'])
def get_user_newsletters(userID, userType):
    # TODO: Implement getUserNewsletters endpoint
    # - Query newsletters where creatorUserID and creatorUserType match
    # - Return id and newsletterName for dropdown
    return jsonify({
        'code': 501,
        'message': 'getUserNewsletters endpoint not yet implemented'
    }), 501


# -----------------------------------------------------------------------------------------
# [POST] subscribeNewsletter
# Purpose: Subscribe to a newsletter
# Used: SpecificStoryNewsletter.vue
# Input:
#   1. newsletterID - the newsletter to subscribe to
#   2. userID - the user subscribing
#   3. userType - 'user', 'producer', or 'venue'
# Output:
#   201 - Subscribed successfully
#   400 - Already subscribed or missing data
#   404 - Newsletter not found
#   500 - Server error
# Note: For MVP, all newsletters are free. Stripe integration for paid newsletters coming later.
# -----------------------------------------------------------------------------------------
@blueprint.route('/subscribeNewsletter', methods=['POST'])
def subscribe_newsletter():
    # TODO: Implement subscribeNewsletter endpoint
    # - Verify newsletter exists
    # - Check if already subscribed (patron)
    # - Insert into newsletterPatrons table
    # - For MVP: isFree=true assumed, no payment processing
    # TODO: Add Stripe integration for paid newsletters
    return jsonify({
        'code': 501,
        'message': 'subscribeNewsletter endpoint not yet implemented'
    }), 501


# -----------------------------------------------------------------------------------------
# [DELETE] unsubscribeNewsletter
# Purpose: Unsubscribe from a newsletter
# Used: SpecificStoryNewsletter.vue
# Input:
#   1. newsletterID - the newsletter to unsubscribe from
#   2. userID - the user unsubscribing
#   3. userType - 'user', 'producer', or 'venue'
# Output:
#   200 - Unsubscribed successfully
#   400 - Not subscribed or missing data
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/unsubscribeNewsletter', methods=['DELETE'])
def unsubscribe_newsletter():
    # TODO: Implement unsubscribeNewsletter endpoint
    # - Check if subscribed (patron)
    # - Delete from newsletterPatrons table
    return jsonify({
        'code': 501,
        'message': 'unsubscribeNewsletter endpoint not yet implemented'
    }), 501


# =========================================================================================
# STORIES ENDPOINTS
# =========================================================================================

# -----------------------------------------------------------------------------------------
# [POST] createStory
# Purpose: Create a new story
# Used: UserStories.vue, SpecificStoryTopic.vue, SpecificStoryNewsletter.vue (create story modal)
# Input:
#   1. creatorUserID - the user's ID
#   2. creatorUserType - 'user', 'producer' or 'venue'
#   3. storyTitle - title of the story (max 500 chars)
#   4. storyContent - HTML content from rich text editor
#   5. images - array of base64 images (optional, max 5)
#   6. listingIDs - array of listing IDs to link (optional, max 5)
#   7. topicID - topic to post under (optional)
#   8. newsletterID - newsletter to add to (optional)
#   9. hashtags - array of hashtag strings (optional)
#   10. freeOrPaid - 'free' or 'paid' (default 'free' for MVP)
# Output:
#   201 - Story created successfully
#   400 - Validation error
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/createStory', methods=['POST'])
def create_story():
    # TODO: Implement createStory endpoint
    # - Validate story title (1-500 chars)
    # - Validate images (max 5)
    # - Validate listingIDs (max 5, verify they exist)
    # - Upload images to S3
    # - Process hashtags (normalize, insert into storyHashtags table)
    # - Insert into stories table
    # - Return created story ID
    # TODO: Add notification to topic subscribers (if topicID provided)
    # TODO: Add notification to newsletter patrons (if newsletterID provided)
    return jsonify({
        'code': 501,
        'message': 'createStory endpoint not yet implemented'
    }), 501


# -----------------------------------------------------------------------------------------
# [GET] getStory/<storyID>
# Purpose: Get a specific story with full content
# Used: SpecificStory.vue
# Input: storyID (path param)
# Optional query params:
#   - userID, userType - to check if user has liked the story
# Output:
#   200 - Full story details with creator info, linked listings, comments preview
#   404 - Story not found
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/getStory/<storyID>', methods=['GET'])
def get_story(storyID):
    # TODO: Implement getStory endpoint
    # - Query story by ID
    # - Get creator info
    # - Get linked listings info (from listings table)
    # - Get like count
    # - Get comment count
    # - Get topic info (if topicID not null)
    # - Get newsletter info (if newsletterID not null)
    # - Check if requesting user has liked (if userID/userType provided)
    # - For paid stories: check if user is patron or story purchaser
    #   - If not, return truncated content with "Subscribe to read" flag
    return jsonify({
        'code': 501,
        'message': 'getStory endpoint not yet implemented'
    }), 501


# -----------------------------------------------------------------------------------------
# [PUT] editStory
# Purpose: Edit an existing story (author only)
# Used: SpecificStory.vue
# Input:
#   1. storyID - the story to edit
#   2. userID - the user editing
#   3. userType - 'user', 'producer', or 'venue'
#   4. storyTitle - new title (optional)
#   5. storyContent - new content (optional)
#   6. images - new images array (optional)
#   7. listingIDs - new linked listings (optional)
#   8. hashtags - new hashtags (optional)
# Output:
#   200 - Story updated successfully
#   400 - Validation error
#   403 - Not the author
#   404 - Story not found
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/editStory', methods=['PUT'])
def edit_story():
    # TODO: Implement editStory endpoint
    # - Verify story exists
    # - Verify user is the author (creatorUserID + creatorUserType match)
    # - Validate updated fields
    # - Upload new images to S3 if provided
    # - Update story record
    # - Set editedAt timestamp
    return jsonify({
        'code': 501,
        'message': 'editStory endpoint not yet implemented'
    }), 501


# -----------------------------------------------------------------------------------------
# [DELETE] deleteStory
# Purpose: Delete a story (author only)
# Used: SpecificStory.vue
# Input:
#   1. storyID - the story to delete
#   2. userID - the user deleting
#   3. userType - 'user', 'producer', or 'venue'
# Output:
#   200 - Story deleted successfully
#   403 - Not the author
#   404 - Story not found
#   500 - Server error
# Note: Cascade deletes comments, likes, storyPatrons records
# -----------------------------------------------------------------------------------------
@blueprint.route('/deleteStory', methods=['DELETE'])
def delete_story():
    # TODO: Implement deleteStory endpoint
    # - Verify story exists
    # - Verify user is the author
    # - Delete story (cascades to comments, likes, storyPatrons)
    return jsonify({
        'code': 501,
        'message': 'deleteStory endpoint not yet implemented'
    }), 501


# -----------------------------------------------------------------------------------------
# [GET] getUserStories/<userID>/<userType>/<offset>
# Purpose: Get paginated stories by a specific user
# Used: UserStories.vue
# Input: userID, userType, offset (path params)
# Output:
#   200 - List of user's stories (sorted by publishingDate DESC)
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/getUserStories/<userID>/<userType>/<offset>', methods=['GET'])
def get_user_stories(userID, userType, offset):
    # TODO: Implement getUserStories endpoint
    # - Query stories where creatorUserID and creatorUserType match
    # - Include like count
    # - Include comment count
    # - Include topic info (if topicID not null)
    # - Include newsletter info (if newsletterID not null)
    # - Sort by publishingDate DESC
    # - Paginate (12 per page)
    return jsonify({
        'code': 501,
        'message': 'getUserStories endpoint not yet implemented'
    }), 501


# -----------------------------------------------------------------------------------------
# [POST] likeStory
# Purpose: Like a story (no dislikes for stories)
# Used: SpecificStory.vue, SpecificStoryTopic.vue, SpecificStoryNewsletter.vue
# Input:
#   1. storyID - the story to like
#   2. userID - the user liking
#   3. userType - 'user', 'producer', or 'venue'
# Output:
#   201 - Liked successfully
#   400 - Already liked or missing data
#   404 - Story not found
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/likeStory', methods=['POST'])
def like_story():
    # TODO: Implement likeStory endpoint
    # - Verify story exists
    # - Check if already liked
    # - Insert into storiesLikes table
    return jsonify({
        'code': 501,
        'message': 'likeStory endpoint not yet implemented'
    }), 501


# -----------------------------------------------------------------------------------------
# [DELETE] unlikeStory
# Purpose: Remove like from a story
# Used: SpecificStory.vue, SpecificStoryTopic.vue, SpecificStoryNewsletter.vue
# Input:
#   1. storyID - the story to unlike
#   2. userID - the user unliking
#   3. userType - 'user', 'producer', or 'venue'
# Output:
#   200 - Unliked successfully
#   400 - Not liked or missing data
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/unlikeStory', methods=['DELETE'])
def unlike_story():
    # TODO: Implement unlikeStory endpoint
    # - Check if liked
    # - Delete from storiesLikes table
    return jsonify({
        'code': 501,
        'message': 'unlikeStory endpoint not yet implemented'
    }), 501


# =========================================================================================
# STORY COMMENTS ENDPOINTS
# =========================================================================================

# -----------------------------------------------------------------------------------------
# [POST] createStoryComment
# Purpose: Create a comment on a story (any logged-in user can comment)
# Used: SpecificStory.vue
# Input:
#   1. storyID - the story to comment on
#   2. userID - the user commenting
#   3. userType - 'user', 'producer', or 'venue'
#   4. commentContent - the comment text
#   5. parentCommentID - ID of parent comment if reply (optional, for 1 level nesting)
# Output:
#   201 - Comment created successfully
#   400 - Missing data or validation error
#   404 - Story or parent comment not found
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/createStoryComment', methods=['POST'])
def create_story_comment():
    # TODO: Implement createStoryComment endpoint
    # - Verify story exists
    # - If parentCommentID provided, verify parent comment exists and belongs to same story
    # - Insert into storyComments table
    # - Return created comment ID
    return jsonify({
        'code': 501,
        'message': 'createStoryComment endpoint not yet implemented'
    }), 501


# -----------------------------------------------------------------------------------------
# [GET] getStoryComments/<storyID>/<offset>
# Purpose: Get paginated comments for a story
# Used: SpecificStory.vue
# Input: storyID, offset (path params)
# Optional query params:
#   - userID, userType - to check if user has liked/disliked comments
# Output:
#   200 - List of comments with commenter info, likes, dislikes, replies
#   404 - Story not found
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/getStoryComments/<storyID>/<offset>', methods=['GET'])
def get_story_comments(storyID, offset):
    # TODO: Implement getStoryComments endpoint
    # - Query top-level comments (parentCommentID IS NULL) for the story
    # - For each comment, get replies (parentCommentID = comment.id)
    # - Include commenter info for each comment
    # - Include like count and dislike count
    # - Check if requesting user has liked/disliked (if userID/userType provided)
    # - Sort by commentDate DESC
    # - Paginate (20 per page)
    return jsonify({
        'code': 501,
        'message': 'getStoryComments endpoint not yet implemented'
    }), 501


# -----------------------------------------------------------------------------------------
# [POST] likeStoryComment
# Purpose: Like a comment (removes dislike if exists)
# Used: SpecificStory.vue
# Input:
#   1. commentID - the comment to like
#   2. userID - the user liking
#   3. userType - 'user', 'producer', or 'venue'
# Output:
#   201 - Liked successfully
#   400 - Missing data
#   404 - Comment not found
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/likeStoryComment', methods=['POST'])
def like_story_comment():
    # TODO: Implement likeStoryComment endpoint
    # - Verify comment exists
    # - Remove existing dislike if any
    # - Toggle like: if already liked, remove; else add
    # - Insert/delete from storyCommentsLikes table
    return jsonify({
        'code': 501,
        'message': 'likeStoryComment endpoint not yet implemented'
    }), 501


# -----------------------------------------------------------------------------------------
# [POST] dislikeStoryComment
# Purpose: Dislike a comment (removes like if exists)
# Used: SpecificStory.vue
# Input:
#   1. commentID - the comment to dislike
#   2. userID - the user disliking
#   3. userType - 'user', 'producer', or 'venue'
# Output:
#   201 - Disliked successfully
#   400 - Missing data
#   404 - Comment not found
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/dislikeStoryComment', methods=['POST'])
def dislike_story_comment():
    # TODO: Implement dislikeStoryComment endpoint
    # - Verify comment exists
    # - Remove existing like if any
    # - Toggle dislike: if already disliked, remove; else add
    # - Insert/delete from storyCommentsDislikes table
    return jsonify({
        'code': 501,
        'message': 'dislikeStoryComment endpoint not yet implemented'
    }), 501


# -----------------------------------------------------------------------------------------
# [DELETE] deleteStoryComment
# Purpose: Delete a comment (comment author only)
# Used: SpecificStory.vue
# Input:
#   1. commentID - the comment to delete
#   2. userID - the user deleting
#   3. userType - 'user', 'producer', or 'venue'
# Output:
#   200 - Comment deleted successfully
#   403 - Not the author
#   404 - Comment not found
#   500 - Server error
# Note: Cascade deletes likes, dislikes, and child replies
# -----------------------------------------------------------------------------------------
@blueprint.route('/deleteStoryComment', methods=['DELETE'])
def delete_story_comment():
    # TODO: Implement deleteStoryComment endpoint
    # - Verify comment exists
    # - Verify user is the author (userID + userType match)
    # - Delete comment (cascades to likes, dislikes, child comments)
    return jsonify({
        'code': 501,
        'message': 'deleteStoryComment endpoint not yet implemented'
    }), 501
