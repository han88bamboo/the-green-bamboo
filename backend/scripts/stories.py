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
import logging
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
            ORDER BY "publicationDate" DESC
            LIMIT %s
        ''', (topic_id, limit))
    elif newsletter_id:
        cursor.execute('''
            SELECT "storyTitle" as "title", "storyPhotos"[1] as "photo"
            FROM "stories"
            WHERE "newsletterID" = %s
              AND "storyPhotos" IS NOT NULL 
              AND array_length("storyPhotos", 1) > 0
            ORDER BY "publicationDate" DESC
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
# Purpose: Create a new topic for categorizing stories (Admin only)
# Used: CreateTopic.vue
# Input:
#   1. creatorID - the user's ID in the 'users' table (must be admin)
#   2. creatorType - must be 'user' (only users can be admins)
#   3. topicName - name of the topic (4-255 chars, emojis allowed)
#   4. topicDesc - description (optional, max 500 chars)
#   5. drinkTypes - array of drink types like ['Wine', 'Whisky'] (optional)
#   6. image64 - base64 banner image (optional)
# Output: Possible return codes:
#   201 - Topic created successfully
#   400 - Validation error (missing data, invalid name, duplicate name)
#   403 - Not authorized (not an admin)
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/createTopic', methods=['POST'])
def create_topic():
    try:
        data = request.get_json()
        
        # Get required fields
        creator_id = data.get('creatorID')
        creator_type = data.get('creatorType')
        topic_name = data.get('topicName', '').strip()
        
        # Get optional fields
        topic_desc = data.get('topicDesc', '').strip() or None
        drink_types = data.get('drinkTypes', [])  # Array of drink types
        
        # Validate required fields
        if not creator_id or not creator_type:
            return jsonify({
                'code': 400,
                'message': 'Missing required fields: creatorID and creatorType are required.'
            }), 400
        
        # Validate topic name length (4-255 chars) - frontend handles other validation
        if not topic_name or len(topic_name) < 4:
            return jsonify({
                'code': 400,
                'message': 'Topic name must be at least 4 characters.'
            }), 400
        if len(topic_name) > 255:
            return jsonify({
                'code': 400,
                'message': 'Topic name cannot exceed 255 characters.'
            }), 400
        
        # Validate description length (max 500 chars)
        if topic_desc and len(topic_desc) > 500:
            return jsonify({
                'code': 400,
                'message': 'Description cannot exceed 500 characters.'
            }), 400
        
        # Normalize name for uniqueness check
        normalized_name = normalize_name_for_uniqueness(topic_name)
        
        with db_manager.get_cursor() as cursor:
            # Check if user is admin (only admins can create topics)
            if creator_type != 'user':
                return jsonify({
                    'code': 403,
                    'message': 'Only admin users can create topics.'
                }), 403
            
            cursor.execute('''
                SELECT "isAdmin" FROM "users" WHERE "id" = %s
            ''', (creator_id,))
            user_data = cursor.fetchone()
            
            if not user_data:
                return jsonify({
                    'code': 404,
                    'message': 'User not found.'
                }), 404
            
            if not user_data['isAdmin']:
                return jsonify({
                    'code': 403,
                    'message': 'Only admin users can create topics.'
                }), 403
            
            # Check for duplicate topic name (case-insensitive, ignoring emojis)
            cursor.execute('''
                SELECT id FROM "topics" 
                WHERE LOWER(REGEXP_REPLACE("topicName", '[^\w\s]', '', 'g')) = %s
            ''', (normalized_name,))
            
            existing = cursor.fetchone()
            if existing:
                return jsonify({
                    'code': 400,
                    'data': {
                        'topicName': topic_name
                    },
                    'message': 'A topic with this name already exists.'
                }), 400
            
            # Upload banner image if provided
            banner_url = None
            if 'image64' in data and data['image64']:
                base64_string = re.sub(r'^data:image\/[a-zA-Z]+;base64,', '', data['image64'])
                banner_url = s3Images.uploadBase64ImageToS3(base64_string)
            
            # Get current timestamp
            date_created = datetime.now()
            
            # Convert drink_types list to PostgreSQL array format (or None if empty)
            drink_types_array = drink_types if drink_types and len(drink_types) > 0 else None
            
            # Insert new topic - createdByType is 'admin' for admin-created topics
            cursor.execute('''
                INSERT INTO "topics" 
                ("topicName", "topicDesc", "drinkTypes", "topicBanner", "dateCreated", "createdByID", "createdByType")
                VALUES (%s, %s, %s, %s, %s, NULL, 'admin')
                RETURNING id
            ''', (topic_name, topic_desc, drink_types_array, banner_url, date_created))
            
            topic_id = cursor.fetchone()['id']
        
        return jsonify({
            'code': 201,
            'data': {
                'topicID': topic_id,
                'message': 'Topic created successfully'
            }
        }), 201
    
    except Exception as e:
        print(f"Error creating topic: {str(e)}")
        return jsonify({
            'code': 500,
            'message': 'An error occurred creating the topic.'
        }), 500


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
    try:
        offset = int(offset)
        limit = 12  # Fixed page size
        
        with db_manager.get_cursor() as cursor:
            # Main query - topics with subscriber and story counts computed via subqueries
            # Creator info is only shown if NOT admin-created (createdByType != 'admin')
            cursor.execute('''
                SELECT 
                    t."id",
                    t."topicName",
                    t."topicDesc",
                    t."drinkTypes",
                    t."topicBanner",
                    t."dateCreated",
                    t."createdByID",
                    t."createdByType",
                    (SELECT COUNT(*) FROM "topicSubscribers" WHERE "topicID" = t."id") as "subscriberCount",
                    (SELECT COUNT(*) FROM "stories" WHERE "topicID" = t."id" AND "publicationDate" IS NOT NULL AND "publicationDate" <= NOW()) as "storyCount",
                    CASE 
                        WHEN t."createdByType" = 'user' THEN u."username"
                        WHEN t."createdByType" = 'producer' THEN p."username"
                        WHEN t."createdByType" = 'venue' THEN v."username"
                        ELSE NULL
                    END as "creatorUsername",
                    CASE 
                        WHEN t."createdByType" = 'user' THEN u."displayName"
                        WHEN t."createdByType" = 'producer' THEN p."producerName"
                        WHEN t."createdByType" = 'venue' THEN v."venueName"
                        ELSE NULL
                    END as "creatorDisplayName",
                    CASE 
                        WHEN t."createdByType" = 'user' THEN u."photo"
                        WHEN t."createdByType" = 'producer' THEN p."photo"
                        WHEN t."createdByType" = 'venue' THEN v."photo"
                        ELSE NULL
                    END as "creatorPhoto"
                FROM "topics" t
                LEFT JOIN "users" u ON t."createdByType" = 'user' AND t."createdByID" = u."id"
                LEFT JOIN "producers" p ON t."createdByType" = 'producer' AND t."createdByID" = p."id"
                LEFT JOIN "venues" v ON t."createdByType" = 'venue' AND t."createdByID" = v."id"
                ORDER BY t."dateCreated" DESC
                LIMIT %s OFFSET %s
            ''', (limit, offset))
            
            topics = cursor.fetchall()
            
            if not topics:
                return jsonify({
                    'code': 200,
                    'data': [],
                    'message': 'No topics found'
                }), 200
            
            # Get preview stories for each topic (up to 3 with photos)
            result = []
            for topic in topics:
                topic_dict = dict(topic)
                topic_dict['previewStories'] = get_story_preview_photos(
                    cursor, topic_id=topic['id'], limit=3
                )
                result.append(topic_dict)
        
        return jsonify({
            'code': 200,
            'data': result
        }), 200
    
    except Exception as e:
        print(f"Error getting topics: {str(e)}")
        return jsonify({
            'code': 500,
            'message': 'An error occurred retrieving topics.'
        }), 500


# -----------------------------------------------------------------------------------------
# [GET] getTopicswSearch/<offset>/<search>
# Purpose: Search topics by name or description
# Used: BrowseStoryTopics.vue
# Input: offset, search (path params)
# Output:
#   200 - List of matching topics
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/getTopicswSearch/<offset>/<search>', methods=['GET'])
def get_topics_with_search(offset, search):
    try:
        offset = int(offset)
        limit = 12  # Fixed page size
        search_term = f'%{search}%'
        
        with db_manager.get_cursor() as cursor:
            # Main query with search filter on topicName and topicDesc (like assemblies)
            cursor.execute('''
                SELECT 
                    t."id",
                    t."topicName",
                    t."topicDesc",
                    t."drinkTypes",
                    t."topicBanner",
                    t."dateCreated",
                    t."createdByID",
                    t."createdByType",
                    (SELECT COUNT(*) FROM "topicSubscribers" WHERE "topicID" = t."id") as "subscriberCount",
                    (SELECT COUNT(*) FROM "stories" WHERE "topicID" = t."id" AND "publicationDate" IS NOT NULL AND "publicationDate" <= NOW()) as "storyCount",
                    CASE 
                        WHEN t."createdByType" = 'user' THEN u."username"
                        WHEN t."createdByType" = 'producer' THEN p."username"
                        WHEN t."createdByType" = 'venue' THEN v."username"
                        ELSE NULL
                    END as "creatorUsername",
                    CASE 
                        WHEN t."createdByType" = 'user' THEN u."displayName"
                        WHEN t."createdByType" = 'producer' THEN p."producerName"
                        WHEN t."createdByType" = 'venue' THEN v."venueName"
                        ELSE NULL
                    END as "creatorDisplayName",
                    CASE 
                        WHEN t."createdByType" = 'user' THEN u."photo"
                        WHEN t."createdByType" = 'producer' THEN p."photo"
                        WHEN t."createdByType" = 'venue' THEN v."photo"
                        ELSE NULL
                    END as "creatorPhoto"
                FROM "topics" t
                LEFT JOIN "users" u ON t."createdByType" = 'user' AND t."createdByID" = u."id"
                LEFT JOIN "producers" p ON t."createdByType" = 'producer' AND t."createdByID" = p."id"
                LEFT JOIN "venues" v ON t."createdByType" = 'venue' AND t."createdByID" = v."id"
                WHERE (t."topicName" ILIKE %s OR t."topicDesc" ILIKE %s)
                ORDER BY t."dateCreated" DESC
                LIMIT %s OFFSET %s
            ''', (search_term, search_term, limit, offset))
            
            topics = cursor.fetchall()
            
            if not topics:
                return jsonify({
                    'code': 200,
                    'data': [],
                    'message': 'No topics found matching search criteria'
                }), 200
            
            # Get preview stories for each topic
            result = []
            for topic in topics:
                topic_dict = dict(topic)
                topic_dict['previewStories'] = get_story_preview_photos(
                    cursor, topic_id=topic['id'], limit=3
                )
                result.append(topic_dict)
        
        return jsonify({
            'code': 200,
            'data': result
        }), 200
    
    except Exception as e:
        print(f"Error searching topics: {str(e)}")
        return jsonify({
            'code': 500,
            'message': 'An error occurred searching topics.'
        }), 500


# -----------------------------------------------------------------------------------------
# [GET] getSpecificTopicInfo/<topicID>
# Purpose: Get detailed info for a specific topic
# Used: SpecificStoryTopic.vue
# Input: 
#   topicID (path param)
#   userID (query param, optional) - for checking isSubscribed
#   userType (query param, optional) - for checking isSubscribed
# Output:
#   200 - Topic details with creator info, subscriber count, story count, isSubscribed
#   404 - Topic not found
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/getSpecificTopicInfo/<topicID>', methods=['GET'])
def get_specific_topic_info(topicID):
    try:
        topic_id = int(topicID)
        
        # Get optional user params for isSubscribed check
        user_id = request.args.get('userID')
        user_type = request.args.get('userType')
        
        with db_manager.get_cursor() as cursor:
            # Get topic with computed counts and creator info
            cursor.execute('''
                SELECT 
                    t."id",
                    t."topicName",
                    t."topicDesc",
                    t."drinkTypes",
                    t."topicBanner",
                    t."dateCreated",
                    t."createdByID",
                    t."createdByType",
                    (SELECT COUNT(*) FROM "topicSubscribers" WHERE "topicID" = t."id") as "subscriberCount",
                    (SELECT COUNT(*) FROM "stories" WHERE "topicID" = t."id" AND "publicationDate" IS NOT NULL AND "publicationDate" <= NOW()) as "storyCount",
                    CASE 
                        WHEN t."createdByType" = 'user' THEN u."username"
                        WHEN t."createdByType" = 'producer' THEN p."username"
                        WHEN t."createdByType" = 'venue' THEN v."username"
                        ELSE NULL
                    END as "creatorUsername",
                    CASE 
                        WHEN t."createdByType" = 'user' THEN u."displayName"
                        WHEN t."createdByType" = 'producer' THEN p."producerName"
                        WHEN t."createdByType" = 'venue' THEN v."venueName"
                        ELSE NULL
                    END as "creatorDisplayName",
                    CASE 
                        WHEN t."createdByType" = 'user' THEN u."photo"
                        WHEN t."createdByType" = 'producer' THEN p."photo"
                        WHEN t."createdByType" = 'venue' THEN v."photo"
                        ELSE NULL
                    END as "creatorPhoto"
                FROM "topics" t
                LEFT JOIN "users" u ON t."createdByType" = 'user' AND t."createdByID" = u."id"
                LEFT JOIN "producers" p ON t."createdByType" = 'producer' AND t."createdByID" = p."id"
                LEFT JOIN "venues" v ON t."createdByType" = 'venue' AND t."createdByID" = v."id"
                WHERE t."id" = %s
            ''', (topic_id,))
            
            topic = cursor.fetchone()
            
            if not topic:
                return jsonify({
                    'code': 404,
                    'message': 'Topic not found'
                }), 404
            
            topic_dict = dict(topic)
            
            # Check if current user is subscribed
            topic_dict['isSubscribed'] = False
            if user_id and user_type:
                cursor.execute('''
                    SELECT id FROM "topicSubscribers"
                    WHERE "topicID" = %s AND "userID" = %s AND "userType" = %s
                ''', (topic_id, user_id, user_type))
                subscription = cursor.fetchone()
                topic_dict['isSubscribed'] = subscription is not None
            
            # Get preview stories (up to 3 with photos for sidebar)
            topic_dict['previewStories'] = get_story_preview_photos(
                cursor, topic_id=topic_id, limit=3
            )
        
        return jsonify({
            'code': 200,
            'data': topic_dict
        }), 200
    
    except ValueError:
        return jsonify({
            'code': 400,
            'message': 'Invalid topic ID'
        }), 400
    except Exception as e:
        print(f"Error getting topic info: {str(e)}")
        return jsonify({
            'code': 500,
            'message': 'An error occurred retrieving topic info.'
        }), 500


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
    try:
        data = request.get_json()
        
        # Validate required fields
        topic_id = data.get('topicID')
        user_id = data.get('userID')
        user_type = data.get('userType')
        
        if not all([topic_id, user_id, user_type]):
            return jsonify({
                'code': 400,
                'message': 'Missing required fields: topicID, userID, userType'
            }), 400
        
        # Validate userType
        if user_type not in ['user', 'producer', 'venue']:
            return jsonify({
                'code': 400,
                'message': 'Invalid userType. Must be user, producer, or venue.'
            }), 400
        
        with db_manager.get_cursor() as cursor:
            # Verify topic exists
            cursor.execute(
                "SELECT id FROM topics WHERE id = %s",
                (topic_id,)
            )
            if not cursor.fetchone():
                return jsonify({
                    'code': 404,
                    'message': 'Topic not found.'
                }), 404
            
            # Check if already subscribed
            cursor.execute(
                """
                SELECT id FROM "topicSubscribers"
                WHERE "topicID" = %s AND "userID" = %s AND "userType" = %s
                """,
                (topic_id, user_id, user_type)
            )
            if cursor.fetchone():
                return jsonify({
                    'code': 400,
                    'message': 'Already subscribed to this topic.'
                }), 400
            
            # Insert subscription (isAdmin defaults to false)
            cursor.execute(
                """
                INSERT INTO "topicSubscribers" ("topicID", "userID", "userType", "isAdmin")
                VALUES (%s, %s, %s, false)
                RETURNING id
                """,
                (topic_id, user_id, user_type)
            )
            new_subscription = cursor.fetchone()
            
            return jsonify({
                'code': 201,
                'message': 'Successfully subscribed to topic.',
                'subscriptionID': new_subscription['id']
            }), 201
            
    except Exception as e:
        logging.exception("subscribeTopic: Error - %s", str(e))
        return jsonify({
            'code': 500,
            'message': 'An error occurred while subscribing to topic.'
        }), 500


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
    try:
        data = request.get_json()
        
        # Validate required fields
        topic_id = data.get('topicID')
        user_id = data.get('userID')
        user_type = data.get('userType')
        
        if not all([topic_id, user_id, user_type]):
            return jsonify({
                'code': 400,
                'message': 'Missing required fields: topicID, userID, userType'
            }), 400
        
        # Validate userType
        if user_type not in ['user', 'producer', 'venue']:
            return jsonify({
                'code': 400,
                'message': 'Invalid userType. Must be user, producer, or venue.'
            }), 400
        
        with db_manager.get_cursor() as cursor:
            # Check if subscribed and delete
            cursor.execute(
                """
                DELETE FROM "topicSubscribers"
                WHERE "topicID" = %s AND "userID" = %s AND "userType" = %s
                RETURNING id
                """,
                (topic_id, user_id, user_type)
            )
            deleted = cursor.fetchone()
            
            if not deleted:
                return jsonify({
                    'code': 400,
                    'message': 'Not subscribed to this topic.'
                }), 400
            
            return jsonify({
                'code': 200,
                'message': 'Successfully unsubscribed from topic.'
            }), 200
            
    except Exception as e:
        logging.exception("unsubscribeTopic: Error - %s", str(e))
        return jsonify({
            'code': 500,
            'message': 'An error occurred while unsubscribing from topic.'
        }), 500


# -----------------------------------------------------------------------------------------
# [GET] getAllTopicsForDropdown
# Purpose: Get all topics for dropdown selection (lightweight, no pagination)
# Used: UserStories.vue (Create Story modal), SpecificStory.vue (editing)
# Input: None
# Output:
#   200 - List of topics with id and topicName only (sorted alphabetically)
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/getAllTopicsForDropdown', methods=['GET'])
def get_all_topics_for_dropdown():
    try:
        with db_manager.get_cursor() as cursor:
            cursor.execute('''
                SELECT id, "topicName"
                FROM "topics"
                ORDER BY "topicName" ASC
            ''')
            topics = cursor.fetchall()
        
        return jsonify({
            'code': 200,
            'data': [dict(t) for t in topics]
        }), 200
    
    except Exception as e:
        logging.exception("getAllTopicsForDropdown: Error - %s", str(e))
        return jsonify({
            'code': 500,
            'message': 'An error occurred retrieving topics.'
        }), 500


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
    try:
        # Validate topicID is a number
        try:
            topic_id = int(topicID)
            offset_val = int(offset)
        except ValueError:
            return jsonify({
                'code': 400,
                'message': 'Invalid topicID or offset. Must be numbers.'
            }), 400
        
        limit = 12  # Stories per page
        
        with db_manager.get_cursor() as cursor:
            # Verify topic exists
            cursor.execute(
                "SELECT id FROM topics WHERE id = %s",
                (topic_id,)
            )
            if not cursor.fetchone():
                return jsonify({
                    'code': 404,
                    'message': 'Topic not found.'
                }), 404
            
            # Get total count of published stories for this topic
            cursor.execute(
                """
                SELECT COUNT(*) as total
                FROM stories
                WHERE "topicID" = %s
                AND "publicationDate" <= NOW()
                """,
                (topic_id,)
            )
            total_count = cursor.fetchone()['total']
            
            # Get paginated published stories with creator info
            cursor.execute(
                """
                SELECT 
                    s.id,
                    s."storyTitle",
                    s."storyContent",
                    s."storyPhotos",
                    s."publicationDate",
                    s."creatorUserID",
                    s."creatorUserType",
                    CASE 
                        WHEN s."creatorUserType" = 'user' THEN u.username
                        WHEN s."creatorUserType" = 'producer' THEN p.username
                        WHEN s."creatorUserType" = 'venue' THEN v.username
                        ELSE NULL
                    END as "creatorUsername",
                    CASE 
                        WHEN s."creatorUserType" = 'user' THEN u.photo
                        WHEN s."creatorUserType" = 'producer' THEN p.photo
                        WHEN s."creatorUserType" = 'venue' THEN v.photo
                        ELSE NULL
                    END as "creatorPhoto",
                    (SELECT COUNT(*) FROM "storiesLikes" WHERE "storyID" = s.id) as "likeCount",
                    (SELECT COUNT(*) FROM "storyComments" WHERE "storyID" = s.id) as "commentCount"
                FROM stories s
                LEFT JOIN users u ON s."creatorUserType" = 'user' AND s."creatorUserID" = u.id
                LEFT JOIN producers p ON s."creatorUserType" = 'producer' AND s."creatorUserID" = p.id
                LEFT JOIN venues v ON s."creatorUserType" = 'venue' AND s."creatorUserID" = v.id
                WHERE s."topicID" = %s
                AND s."publicationDate" <= NOW()
                ORDER BY s."publicationDate" DESC
                LIMIT %s OFFSET %s
                """,
                (topic_id, limit, offset_val)
            )
            stories = cursor.fetchall()
            
            # Format stories for response
            formatted_stories = []
            for story in stories:
                # Get first photo from array for preview
                photo = None
                if story['storyPhotos'] and len(story['storyPhotos']) > 0:
                    photo = story['storyPhotos'][0]
                
                formatted_stories.append({
                    'id': story['id'],
                    'title': story['storyTitle'],
                    'content': story['storyContent'],
                    'photo': photo,
                    'publicationDate': story['publicationDate'].isoformat() if story['publicationDate'] else None,
                    'createdByID': story['creatorUserID'],
                    'createdByType': story['creatorUserType'],
                    'creatorUsername': story['creatorUsername'],
                    'creatorPhoto': story['creatorPhoto'],
                    'likeCount': story['likeCount'],
                    'commentCount': story['commentCount']
                })
            
            return jsonify({
                'code': 200,
                'stories': formatted_stories,
                'totalCount': total_count,
                'hasMore': (offset_val + limit) < total_count
            }), 200
            
    except Exception as e:
        logging.exception("getTopicStories: Error - %s", str(e))
        return jsonify({
            'code': 500,
            'message': 'An error occurred retrieving topic stories.'
        }), 500


# =========================================================================================
# NEWSLETTERS ENDPOINTS
# =========================================================================================

# -----------------------------------------------------------------------------------------
# [POST] createNewsletter
# Purpose: Create a new newsletter for the user's stories (any logged-in user can create)
# Used: CreateNewsletter.vue, UserStories.vue (modal)
# Input:
#   1. creatorUserID - the user's ID
#   2. creatorUserType - 'user', 'producer' or 'venue'
#   3. newsletterName - name of the newsletter (4-255 chars, emojis allowed)
#   4. newsletterDesc - description (optional, max 500 chars)
#   5. bannerImage64 - base64 banner image for hero sections (optional)
#   6. displayImage64 - base64 display photo for cards (optional)
# Output:
#   201 - Newsletter created successfully
#   400 - Validation error or duplicate name (per-creator unique)
#   500 - Server error
# Note: All newsletters are free for MVP. Stripe fields in newsletterPatrons table
#       are reserved for future paid newsletter functionality.
# -----------------------------------------------------------------------------------------
@blueprint.route('/createNewsletter', methods=['POST'])
def create_newsletter():
    try:
        data = request.get_json()
        
        # Get required fields
        creator_id = data.get('creatorUserID')
        creator_type = data.get('creatorUserType')
        newsletter_name = data.get('newsletterName', '').strip()
        
        # Get optional fields
        newsletter_desc = data.get('newsletterDesc', '').strip() or None
        
        # Validate required fields
        if not creator_id or not creator_type:
            return jsonify({
                'code': 400,
                'message': 'Missing required fields: creatorUserID and creatorUserType are required.'
            }), 400
        
        # Validate creator type
        if creator_type not in ['user', 'producer', 'venue']:
            return jsonify({
                'code': 400,
                'message': 'Invalid creatorUserType. Must be user, producer, or venue.'
            }), 400
        
        # Validate newsletter name (4-255 chars, emojis allowed)
        if not newsletter_name or len(newsletter_name) < 4:
            return jsonify({
                'code': 400,
                'message': 'Newsletter name must be at least 4 characters.'
            }), 400
        if len(newsletter_name) > 255:
            return jsonify({
                'code': 400,
                'message': 'Newsletter name cannot exceed 255 characters.'
            }), 400
        
        # Validate description length (max 500 chars)
        if newsletter_desc and len(newsletter_desc) > 500:
            return jsonify({
                'code': 400,
                'message': 'Description cannot exceed 500 characters.'
            }), 400
        
        # Normalize name for per-creator uniqueness check
        normalized_name = normalize_name_for_uniqueness(newsletter_name)
        
        with db_manager.get_cursor() as cursor:
            # Check for duplicate newsletter name (per-creator, case-insensitive, ignoring emojis)
            cursor.execute('''
                SELECT id FROM "newsletters" 
                WHERE "creatorUserID" = %s 
                  AND "creatorUserType" = %s
                  AND LOWER(REGEXP_REPLACE("newsletterName", '[^\w\s]', '', 'g')) = %s
            ''', (creator_id, creator_type, normalized_name))
            
            existing = cursor.fetchone()
            if existing:
                return jsonify({
                    'code': 400,
                    'data': {'newsletterName': newsletter_name},
                    'message': 'You already have a newsletter with this name.'
                }), 400
            
            # Upload banner image if provided
            banner_url = None
            if 'bannerImage64' in data and data['bannerImage64']:
                base64_string = re.sub(r'^data:image\/[a-zA-Z]+;base64,', '', data['bannerImage64'])
                banner_url = s3Images.uploadBase64ImageToS3(base64_string)
            
            # Upload display photo if provided
            display_photo_url = None
            if 'displayImage64' in data and data['displayImage64']:
                base64_string = re.sub(r'^data:image\/[a-zA-Z]+;base64,', '', data['displayImage64'])
                display_photo_url = s3Images.uploadBase64ImageToS3(base64_string)
            
            # Get current timestamp
            date_created = datetime.now()
            
            # Insert new newsletter (isFree=true for MVP)
            cursor.execute('''
                INSERT INTO "newsletters" 
                ("newsletterName", "newsletterDesc", "newsletterBanner", "newsletterDisplayPhoto", 
                 "dateCreated", "creatorUserID", "creatorUserType", "isFree")
                VALUES (%s, %s, %s, %s, %s, %s, %s, true)
                RETURNING id
            ''', (newsletter_name, newsletter_desc, banner_url, display_photo_url, 
                  date_created, creator_id, creator_type))
            
            newsletter_id = cursor.fetchone()['id']
        
        return jsonify({
            'code': 201,
            'data': {
                'newsletterID': newsletter_id,
                'message': 'Newsletter created successfully'
            }
        }), 201
    
    except Exception as e:
        logging.exception("createNewsletter: Error - %s", str(e))
        return jsonify({
            'code': 500,
            'message': 'An error occurred creating the newsletter.'
        }), 500


# -----------------------------------------------------------------------------------------
# [GET] getNewsletters/<offset>
# Purpose: Get paginated list of newsletters with creator info (server-side sorting)
# Used: BrowseStoryNewsletters.vue
# Input: 
#   offset (path param) - starting position (0, 12, 24, ...)
#   sortBy (query param) - 'recent' (default), 'alphabetical', or 'subscribers'
#   userID (query param, optional) - for checking isSubscribed on each newsletter
#   userType (query param, optional) - for checking isSubscribed
# Output:
#   200 - List of newsletters with creator info, subscriberCount, storyCount, isFree, isSubscribed
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/getNewsletters/<offset>', methods=['GET'])
def get_newsletters(offset):
    try:
        offset = int(offset)
        limit = 12  # Fixed page size
        
        # Get sort parameter (default: recent)
        sort_by = request.args.get('sortBy', 'recent')
        
        # Get optional user params for isSubscribed check
        user_id = request.args.get('userID')
        user_type = request.args.get('userType')
        
        # Determine ORDER BY clause based on sortBy
        if sort_by == 'alphabetical':
            order_clause = 'n."newsletterName" ASC'
        elif sort_by == 'subscribers':
            order_clause = '"subscriberCount" DESC, n."dateCreated" DESC'
        else:  # 'recent' (default)
            order_clause = 'n."dateCreated" DESC'
        
        with db_manager.get_cursor() as cursor:
            # Main query - newsletters with subscriber and story counts computed via subqueries
            query = f'''
                SELECT 
                    n."id",
                    n."newsletterName",
                    n."newsletterDesc",
                    n."newsletterBanner",
                    n."newsletterDisplayPhoto",
                    n."dateCreated",
                    n."creatorUserID",
                    n."creatorUserType",
                    n."isFree",
                    (SELECT COUNT(*) FROM "newsletterPatrons" WHERE "newsletterID" = n."id" AND "subscriptionStatus" = 'active') as "subscriberCount",
                    (SELECT COUNT(*) FROM "stories" WHERE "newsletterID" = n."id" AND "publicationDate" IS NOT NULL AND "publicationDate" <= NOW()) as "storyCount",
                    CASE 
                        WHEN n."creatorUserType" = 'user' THEN u."username"
                        WHEN n."creatorUserType" = 'producer' THEN p."username"
                        WHEN n."creatorUserType" = 'venue' THEN v."username"
                        ELSE NULL
                    END as "creatorUsername",
                    CASE 
                        WHEN n."creatorUserType" = 'user' THEN u."displayName"
                        WHEN n."creatorUserType" = 'producer' THEN p."producerName"
                        WHEN n."creatorUserType" = 'venue' THEN v."venueName"
                        ELSE NULL
                    END as "creatorDisplayName",
                    CASE 
                        WHEN n."creatorUserType" = 'user' THEN u."photo"
                        WHEN n."creatorUserType" = 'producer' THEN p."photo"
                        WHEN n."creatorUserType" = 'venue' THEN v."photo"
                        ELSE NULL
                    END as "creatorPhoto"
                FROM "newsletters" n
                LEFT JOIN "users" u ON n."creatorUserType" = 'user' AND n."creatorUserID" = u."id"
                LEFT JOIN "producers" p ON n."creatorUserType" = 'producer' AND n."creatorUserID" = p."id"
                LEFT JOIN "venues" v ON n."creatorUserType" = 'venue' AND n."creatorUserID" = v."id"
                ORDER BY {order_clause}
                LIMIT %s OFFSET %s
            '''
            
            cursor.execute(query, (limit, offset))
            newsletters = cursor.fetchall()
            
            if not newsletters:
                return jsonify({
                    'code': 200,
                    'data': [],
                    'message': 'No newsletters found'
                }), 200
            
            # Build result with isSubscribed check if user provided
            result = []
            for newsletter in newsletters:
                newsletter_dict = dict(newsletter)
                
                # Check if current user is subscribed
                newsletter_dict['isSubscribed'] = False
                if user_id and user_type:
                    cursor.execute('''
                        SELECT id FROM "newsletterPatrons"
                        WHERE "newsletterID" = %s AND "patronUserID" = %s AND "patronUserType" = %s
                        AND "subscriptionStatus" = 'active'
                    ''', (newsletter['id'], user_id, user_type))
                    subscription = cursor.fetchone()
                    newsletter_dict['isSubscribed'] = subscription is not None
                
                result.append(newsletter_dict)
        
        return jsonify({
            'code': 200,
            'data': result
        }), 200
    
    except Exception as e:
        logging.exception("getNewsletters: Error - %s", str(e))
        return jsonify({
            'code': 500,
            'message': 'An error occurred retrieving newsletters.'
        }), 500


# -----------------------------------------------------------------------------------------
# [GET] getNewsletterswSearch/<offset>/<search>
# Purpose: Search newsletters by name (server-side sorting)
# Used: BrowseStoryNewsletters.vue
# Input: 
#   offset, search (path params)
#   sortBy (query param) - 'recent' (default), 'alphabetical', or 'subscribers'
#   userID (query param, optional) - for checking isSubscribed
#   userType (query param, optional) - for checking isSubscribed
# Output:
#   200 - List of matching newsletters
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/getNewsletterswSearch/<offset>/<search>', methods=['GET'])
def get_newsletters_with_search(offset, search):
    try:
        offset = int(offset)
        limit = 12  # Fixed page size
        search_term = f'%{search}%'
        
        # Get sort parameter (default: recent)
        sort_by = request.args.get('sortBy', 'recent')
        
        # Get optional user params for isSubscribed check
        user_id = request.args.get('userID')
        user_type = request.args.get('userType')
        
        # Determine ORDER BY clause based on sortBy
        if sort_by == 'alphabetical':
            order_clause = 'n."newsletterName" ASC'
        elif sort_by == 'subscribers':
            order_clause = '"subscriberCount" DESC, n."dateCreated" DESC'
        else:  # 'recent' (default)
            order_clause = 'n."dateCreated" DESC'
        
        with db_manager.get_cursor() as cursor:
            # Main query with search filter on newsletterName and newsletterDesc
            query = f'''
                SELECT 
                    n."id",
                    n."newsletterName",
                    n."newsletterDesc",
                    n."newsletterBanner",
                    n."newsletterDisplayPhoto",
                    n."dateCreated",
                    n."creatorUserID",
                    n."creatorUserType",
                    n."isFree",
                    (SELECT COUNT(*) FROM "newsletterPatrons" WHERE "newsletterID" = n."id" AND "subscriptionStatus" = 'active') as "subscriberCount",
                    (SELECT COUNT(*) FROM "stories" WHERE "newsletterID" = n."id" AND "publicationDate" IS NOT NULL AND "publicationDate" <= NOW()) as "storyCount",
                    CASE 
                        WHEN n."creatorUserType" = 'user' THEN u."username"
                        WHEN n."creatorUserType" = 'producer' THEN p."username"
                        WHEN n."creatorUserType" = 'venue' THEN v."username"
                        ELSE NULL
                    END as "creatorUsername",
                    CASE 
                        WHEN n."creatorUserType" = 'user' THEN u."displayName"
                        WHEN n."creatorUserType" = 'producer' THEN p."producerName"
                        WHEN n."creatorUserType" = 'venue' THEN v."venueName"
                        ELSE NULL
                    END as "creatorDisplayName",
                    CASE 
                        WHEN n."creatorUserType" = 'user' THEN u."photo"
                        WHEN n."creatorUserType" = 'producer' THEN p."photo"
                        WHEN n."creatorUserType" = 'venue' THEN v."photo"
                        ELSE NULL
                    END as "creatorPhoto"
                FROM "newsletters" n
                LEFT JOIN "users" u ON n."creatorUserType" = 'user' AND n."creatorUserID" = u."id"
                LEFT JOIN "producers" p ON n."creatorUserType" = 'producer' AND n."creatorUserID" = p."id"
                LEFT JOIN "venues" v ON n."creatorUserType" = 'venue' AND n."creatorUserID" = v."id"
                WHERE (n."newsletterName" ILIKE %s OR n."newsletterDesc" ILIKE %s)
                ORDER BY {order_clause}
                LIMIT %s OFFSET %s
            '''
            
            cursor.execute(query, (search_term, search_term, limit, offset))
            newsletters = cursor.fetchall()
            
            if not newsletters:
                return jsonify({
                    'code': 200,
                    'data': [],
                    'message': 'No newsletters found matching search criteria'
                }), 200
            
            # Build result with isSubscribed check
            result = []
            for newsletter in newsletters:
                newsletter_dict = dict(newsletter)
                
                # Check if current user is subscribed
                newsletter_dict['isSubscribed'] = False
                if user_id and user_type:
                    cursor.execute('''
                        SELECT id FROM "newsletterPatrons"
                        WHERE "newsletterID" = %s AND "patronUserID" = %s AND "patronUserType" = %s
                        AND "subscriptionStatus" = 'active'
                    ''', (newsletter['id'], user_id, user_type))
                    subscription = cursor.fetchone()
                    newsletter_dict['isSubscribed'] = subscription is not None
                
                result.append(newsletter_dict)
        
        return jsonify({
            'code': 200,
            'data': result
        }), 200
    
    except Exception as e:
        logging.exception("getNewsletterswSearch: Error - %s", str(e))
        return jsonify({
            'code': 500,
            'message': 'An error occurred searching newsletters.'
        }), 500


# -----------------------------------------------------------------------------------------
# [GET] getSpecificNewsletterInfo/<newsletterID>
# Purpose: Get detailed info for a specific newsletter
# Used: SpecificStoryNewsletter.vue
# Input: 
#   newsletterID (path param)
#   userID (query param, optional) - for checking isSubscribed and isOwner
#   userType (query param, optional) - for checking isSubscribed and isOwner
# Output:
#   200 - Newsletter details with creator info, subscriberCount, storyCount, isFree, isSubscribed, isOwner
#   404 - Newsletter not found
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/getSpecificNewsletterInfo/<newsletterID>', methods=['GET'])
def get_specific_newsletter_info(newsletterID):
    try:
        newsletter_id = int(newsletterID)
        
        # Get optional user params for isSubscribed/isOwner check
        user_id = request.args.get('userID')
        user_type = request.args.get('userType')
        
        with db_manager.get_cursor() as cursor:
            # Get newsletter with computed counts and creator info
            cursor.execute('''
                SELECT 
                    n."id",
                    n."newsletterName",
                    n."newsletterDesc",
                    n."newsletterBanner",
                    n."newsletterDisplayPhoto",
                    n."dateCreated",
                    n."creatorUserID",
                    n."creatorUserType",
                    n."isFree",
                    (SELECT COUNT(*) FROM "newsletterPatrons" WHERE "newsletterID" = n."id" AND "subscriptionStatus" = 'active') as "subscriberCount",
                    (SELECT COUNT(*) FROM "stories" WHERE "newsletterID" = n."id" AND "publicationDate" IS NOT NULL AND "publicationDate" <= NOW()) as "storyCount",
                    CASE 
                        WHEN n."creatorUserType" = 'user' THEN u."username"
                        WHEN n."creatorUserType" = 'producer' THEN p."username"
                        WHEN n."creatorUserType" = 'venue' THEN v."username"
                        ELSE NULL
                    END as "creatorUsername",
                    CASE 
                        WHEN n."creatorUserType" = 'user' THEN u."displayName"
                        WHEN n."creatorUserType" = 'producer' THEN p."producerName"
                        WHEN n."creatorUserType" = 'venue' THEN v."venueName"
                        ELSE NULL
                    END as "creatorDisplayName",
                    CASE 
                        WHEN n."creatorUserType" = 'user' THEN u."photo"
                        WHEN n."creatorUserType" = 'producer' THEN p."photo"
                        WHEN n."creatorUserType" = 'venue' THEN v."photo"
                        ELSE NULL
                    END as "creatorPhoto"
                FROM "newsletters" n
                LEFT JOIN "users" u ON n."creatorUserType" = 'user' AND n."creatorUserID" = u."id"
                LEFT JOIN "producers" p ON n."creatorUserType" = 'producer' AND n."creatorUserID" = p."id"
                LEFT JOIN "venues" v ON n."creatorUserType" = 'venue' AND n."creatorUserID" = v."id"
                WHERE n."id" = %s
            ''', (newsletter_id,))
            
            newsletter = cursor.fetchone()
            
            if not newsletter:
                return jsonify({
                    'code': 404,
                    'message': 'Newsletter not found'
                }), 404
            
            newsletter_dict = dict(newsletter)
            
            # Check if current user is subscribed
            newsletter_dict['isSubscribed'] = False
            if user_id and user_type:
                cursor.execute('''
                    SELECT id FROM "newsletterPatrons"
                    WHERE "newsletterID" = %s AND "patronUserID" = %s AND "patronUserType" = %s
                    AND "subscriptionStatus" = 'active'
                ''', (newsletter_id, user_id, user_type))
                subscription = cursor.fetchone()
                newsletter_dict['isSubscribed'] = subscription is not None
            
            # Check if current user is the owner
            newsletter_dict['isOwner'] = False
            if user_id and user_type:
                newsletter_dict['isOwner'] = (
                    str(newsletter['creatorUserID']) == str(user_id) and
                    newsletter['creatorUserType'] == user_type
                )
        
        return jsonify({
            'code': 200,
            'data': newsletter_dict
        }), 200
    
    except ValueError:
        return jsonify({
            'code': 400,
            'message': 'Invalid newsletter ID'
        }), 400
    except Exception as e:
        logging.exception("getSpecificNewsletterInfo: Error - %s", str(e))
        return jsonify({
            'code': 500,
            'message': 'An error occurred retrieving newsletter info.'
        }), 500


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
    try:
        # Validate parameters
        try:
            newsletter_id = int(newsletterID)
            offset_val = int(offset)
        except ValueError:
            return jsonify({
                'code': 400,
                'message': 'Invalid newsletterID or offset. Must be numbers.'
            }), 400
        
        limit = 12  # Stories per page
        
        with db_manager.get_cursor() as cursor:
            # Verify newsletter exists
            cursor.execute(
                "SELECT id FROM newsletters WHERE id = %s",
                (newsletter_id,)
            )
            if not cursor.fetchone():
                return jsonify({
                    'code': 404,
                    'message': 'Newsletter not found.'
                }), 404
            
            # Get total count of published stories for this newsletter
            cursor.execute(
                """
                SELECT COUNT(*) as total
                FROM stories
                WHERE "newsletterID" = %s
                AND "publicationDate" <= NOW()
                """,
                (newsletter_id,)
            )
            total_count = cursor.fetchone()['total']
            
            # Get paginated published stories with creator info
            cursor.execute(
                """
                SELECT 
                    s.id,
                    s."storyTitle",
                    s."storyContent",
                    s."storyPhotos",
                    s."publicationDate",
                    s."creatorUserID",
                    s."creatorUserType",
                    CASE 
                        WHEN s."creatorUserType" = 'user' THEN u.username
                        WHEN s."creatorUserType" = 'producer' THEN p.username
                        WHEN s."creatorUserType" = 'venue' THEN v.username
                        ELSE NULL
                    END as "creatorUsername",
                    CASE 
                        WHEN s."creatorUserType" = 'user' THEN u.photo
                        WHEN s."creatorUserType" = 'producer' THEN p.photo
                        WHEN s."creatorUserType" = 'venue' THEN v.photo
                        ELSE NULL
                    END as "creatorPhoto",
                    (SELECT COUNT(*) FROM "storiesLikes" WHERE "storyID" = s.id) as "likeCount",
                    (SELECT COUNT(*) FROM "storyComments" WHERE "storyID" = s.id) as "commentCount"
                FROM stories s
                LEFT JOIN users u ON s."creatorUserType" = 'user' AND s."creatorUserID" = u.id
                LEFT JOIN producers p ON s."creatorUserType" = 'producer' AND s."creatorUserID" = p.id
                LEFT JOIN venues v ON s."creatorUserType" = 'venue' AND s."creatorUserID" = v.id
                WHERE s."newsletterID" = %s
                AND s."publicationDate" <= NOW()
                ORDER BY s."publicationDate" DESC
                LIMIT %s OFFSET %s
                """,
                (newsletter_id, limit, offset_val)
            )
            stories = cursor.fetchall()
            
            # Format stories for response
            formatted_stories = []
            for story in stories:
                # Get first photo from array for preview
                photo = None
                if story['storyPhotos'] and len(story['storyPhotos']) > 0:
                    photo = story['storyPhotos'][0]
                
                formatted_stories.append({
                    'id': story['id'],
                    'title': story['storyTitle'],
                    'content': story['storyContent'],
                    'photo': photo,
                    'publicationDate': story['publicationDate'].isoformat() if story['publicationDate'] else None,
                    'createdByID': story['creatorUserID'],
                    'createdByType': story['creatorUserType'],
                    'creatorUsername': story['creatorUsername'],
                    'creatorPhoto': story['creatorPhoto'],
                    'likeCount': story['likeCount'],
                    'commentCount': story['commentCount']
                })
            
            return jsonify({
                'code': 200,
                'stories': formatted_stories,
                'totalCount': total_count,
                'hasMore': (offset_val + limit) < total_count
            }), 200
            
    except Exception as e:
        logging.exception("getNewsletterStories: Error - %s", str(e))
        return jsonify({
            'code': 500,
            'message': 'An error occurred retrieving newsletter stories.'
        }), 500


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
    try:
        # Validate userType
        if userType not in ['user', 'producer', 'venue']:
            return jsonify({
                'code': 400,
                'message': 'Invalid userType. Must be user, producer, or venue.'
            }), 400
        
        with db_manager.get_cursor() as cursor:
            cursor.execute('''
                SELECT "id", "newsletterName", "newsletterDisplayPhoto", "newsletterBanner"
                FROM "newsletters"
                WHERE "creatorUserID" = %s AND "creatorUserType" = %s
                ORDER BY "dateCreated" DESC
            ''', (userID, userType))
            
            newsletters = cursor.fetchall()
            
            # Convert to list of dicts
            result = [dict(n) for n in newsletters] if newsletters else []
        
        return jsonify({
            'code': 200,
            'data': result
        }), 200
    
    except Exception as e:
        logging.exception("getUserNewsletters: Error - %s", str(e))
        return jsonify({
            'code': 500,
            'message': 'An error occurred retrieving user newsletters.'
        }), 500


# -----------------------------------------------------------------------------------------
# [POST] subscribeNewsletter
# Purpose: Subscribe to a newsletter (instant, no approval needed)
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
# Note: For MVP, all newsletters are free. Stripe fields in newsletterPatrons table
#       are reserved for future paid newsletter functionality.
# -----------------------------------------------------------------------------------------
@blueprint.route('/subscribeNewsletter', methods=['POST'])
def subscribe_newsletter():
    try:
        data = request.get_json()
        
        # Validate required fields
        newsletter_id = data.get('newsletterID')
        user_id = data.get('userID')
        user_type = data.get('userType')
        
        if not all([newsletter_id, user_id, user_type]):
            return jsonify({
                'code': 400,
                'message': 'Missing required fields: newsletterID, userID, userType'
            }), 400
        
        # Validate userType
        if user_type not in ['user', 'producer', 'venue']:
            return jsonify({
                'code': 400,
                'message': 'Invalid userType. Must be user, producer, or venue.'
            }), 400
        
        with db_manager.get_cursor() as cursor:
            # Verify newsletter exists
            cursor.execute(
                "SELECT id FROM newsletters WHERE id = %s",
                (newsletter_id,)
            )
            if not cursor.fetchone():
                return jsonify({
                    'code': 404,
                    'message': 'Newsletter not found.'
                }), 404
            
            # Check if already subscribed (active patron)
            cursor.execute(
                """
                SELECT id, "subscriptionStatus" FROM "newsletterPatrons"
                WHERE "newsletterID" = %s AND "patronUserID" = %s AND "patronUserType" = %s
                """,
                (newsletter_id, user_id, user_type)
            )
            existing = cursor.fetchone()
            
            if existing:
                if existing['subscriptionStatus'] == 'active':
                    return jsonify({
                        'code': 400,
                        'message': 'Already subscribed to this newsletter.'
                    }), 400
                else:
                    # Reactivate existing subscription
                    cursor.execute(
                        """
                        UPDATE "newsletterPatrons"
                        SET "subscriptionStatus" = 'active', "subscriptionDate" = NOW()
                        WHERE id = %s
                        RETURNING id
                        """,
                        (existing['id'],)
                    )
                    updated = cursor.fetchone()
                    return jsonify({
                        'code': 201,
                        'message': 'Successfully resubscribed to newsletter.',
                        'patronID': updated['id']
                    }), 201
            
            # Insert new subscription (Stripe fields left NULL for free newsletters)
            cursor.execute(
                """
                INSERT INTO "newsletterPatrons" 
                ("newsletterID", "patronUserID", "patronUserType", "subscriptionStatus")
                VALUES (%s, %s, %s, 'active')
                RETURNING id
                """,
                (newsletter_id, user_id, user_type)
            )
            new_patron = cursor.fetchone()
            
            return jsonify({
                'code': 201,
                'message': 'Successfully subscribed to newsletter.',
                'patronID': new_patron['id']
            }), 201
            
    except Exception as e:
        logging.exception("subscribeNewsletter: Error - %s", str(e))
        return jsonify({
            'code': 500,
            'message': 'An error occurred while subscribing to newsletter.'
        }), 500


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
    try:
        data = request.get_json()
        
        # Validate required fields
        newsletter_id = data.get('newsletterID')
        user_id = data.get('userID')
        user_type = data.get('userType')
        
        if not all([newsletter_id, user_id, user_type]):
            return jsonify({
                'code': 400,
                'message': 'Missing required fields: newsletterID, userID, userType'
            }), 400
        
        # Validate userType
        if user_type not in ['user', 'producer', 'venue']:
            return jsonify({
                'code': 400,
                'message': 'Invalid userType. Must be user, producer, or venue.'
            }), 400
        
        with db_manager.get_cursor() as cursor:
            # Update subscription status to 'cancelled' (soft delete for future analytics)
            cursor.execute(
                """
                UPDATE "newsletterPatrons"
                SET "subscriptionStatus" = 'cancelled'
                WHERE "newsletterID" = %s AND "patronUserID" = %s AND "patronUserType" = %s
                AND "subscriptionStatus" = 'active'
                RETURNING id
                """,
                (newsletter_id, user_id, user_type)
            )
            updated = cursor.fetchone()
            
            if not updated:
                return jsonify({
                    'code': 400,
                    'message': 'Not subscribed to this newsletter.'
                }), 400
            
            return jsonify({
                'code': 200,
                'message': 'Successfully unsubscribed from newsletter.'
            }), 200
            
    except Exception as e:
        logging.exception("unsubscribeNewsletter: Error - %s", str(e))
        return jsonify({
            'code': 500,
            'message': 'An error occurred while unsubscribing from newsletter.'
        }), 500


# -----------------------------------------------------------------------------------------
# [GET] getUserNewslettersForDropdown/<userID>/<userType>
# Purpose: Get newsletters owned by a user for dropdown selection
# Used: UserStories.vue (Create Story modal)
# Input: userID, userType (path params)
# Output:
#   200 - List of user's newsletters with id and newsletterName only (sorted alphabetically)
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/getUserNewslettersForDropdown/<userID>/<userType>', methods=['GET'])
def get_user_newsletters_for_dropdown(userID, userType):
    try:
        user_id = int(userID)
        
        if userType not in ['user', 'producer', 'venue']:
            return jsonify({
                'code': 400,
                'message': 'Invalid userType.'
            }), 400
        
        with db_manager.get_cursor() as cursor:
            cursor.execute('''
                SELECT id, "newsletterName"
                FROM "newsletters"
                WHERE "createdByID" = %s AND "createdByType" = %s
                ORDER BY "newsletterName" ASC
            ''', (user_id, userType))
            newsletters = cursor.fetchall()
        
        return jsonify({
            'code': 200,
            'data': [dict(n) for n in newsletters]
        }), 200
    
    except ValueError:
        return jsonify({
            'code': 400,
            'message': 'Invalid userID.'
        }), 400
    except Exception as e:
        logging.exception("getUserNewslettersForDropdown: Error - %s", str(e))
        return jsonify({
            'code': 500,
            'message': 'An error occurred retrieving newsletters.'
        }), 500


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
#   5. featureImage64 - base64 feature image for cards (optional, max 1)
#   6. listingIDs - array of listing IDs to link (optional, max 5)
#   7. topicID - topic to post under (optional)
#   8. newsletterID - newsletter to add to (optional)
#   9. hashtags - array of hashtag strings (optional)
#   10. publicationDate - ISO date string for scheduled publishing (optional, NULL = draft)
#   11. freeOrPaid - 'free' or 'paid' (default 'free' for MVP)
# Output:
#   201 - Story created successfully
#   400 - Validation error
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/createStory', methods=['POST'])
def create_story():
    try:
        data = request.get_json()
        
        # Get required fields
        creator_id = data.get('creatorUserID')
        creator_type = data.get('creatorUserType')
        story_title = data.get('storyTitle', '').strip()
        
        # Get optional fields
        story_content = data.get('storyContent', '').strip() or None
        feature_image_64 = data.get('featureImage64')  # Single feature image
        listing_ids = data.get('listingIDs', [])
        topic_id = data.get('topicID') or None
        newsletter_id = data.get('newsletterID') or None
        hashtags = data.get('hashtags', [])
        publication_date_str = data.get('publicationDate')  # ISO string or None for draft
        free_or_paid = data.get('freeOrPaid', 'free')
        
        # Validate required fields
        if not creator_id or not creator_type:
            return jsonify({
                'code': 400,
                'message': 'Missing required fields: creatorUserID and creatorUserType are required.'
            }), 400
        
        # Validate creator type
        if creator_type not in ['user', 'producer', 'venue']:
            return jsonify({
                'code': 400,
                'message': 'Invalid creatorUserType. Must be user, producer, or venue.'
            }), 400
        
        # Validate story title (1-500 chars)
        is_valid, error_msg = validate_story_title(story_title)
        if not is_valid:
            return jsonify({
                'code': 400,
                'message': error_msg
            }), 400
        
        # Validate listing IDs (max 5)
        if len(listing_ids) > 5:
            return jsonify({
                'code': 400,
                'message': 'Maximum 5 linked drinks allowed.'
            }), 400
        
        # Validate freeOrPaid
        if free_or_paid not in ['free', 'paid']:
            return jsonify({
                'code': 400,
                'message': 'freeOrPaid must be either "free" or "paid".'
            }), 400
        
        # Parse publication date (None = draft)
        publication_date = None
        if publication_date_str:
            try:
                publication_date = datetime.fromisoformat(publication_date_str.replace('Z', '+00:00'))
            except ValueError:
                return jsonify({
                    'code': 400,
                    'message': 'Invalid publicationDate format. Use ISO 8601 format.'
                }), 400
        
        with db_manager.get_cursor() as cursor:
            # Verify topic exists if provided
            if topic_id:
                cursor.execute('SELECT id FROM "topics" WHERE id = %s', (topic_id,))
                if not cursor.fetchone():
                    return jsonify({
                        'code': 400,
                        'message': 'Topic not found.'
                    }), 400
            
            # Verify newsletter exists and belongs to creator if provided
            if newsletter_id:
                cursor.execute('''
                    SELECT id FROM "newsletters" 
                    WHERE id = %s AND "creatorUserID" = %s AND "creatorUserType" = %s
                ''', (newsletter_id, creator_id, creator_type))
                if not cursor.fetchone():
                    return jsonify({
                        'code': 400,
                        'message': 'Newsletter not found or you are not the owner.'
                    }), 400
            
            # Upload feature image to S3 if provided
            feature_image_url = None
            if feature_image_64:
                base64_string = re.sub(r'^data:image\/[a-zA-Z]+;base64,', '', feature_image_64)
                feature_image_url = s3Images.uploadBase64ImageToS3(base64_string)
            
            # Format storyPhotos as PostgreSQL array (just the feature image for now)
            story_photos = None
            if feature_image_url:
                story_photos = [feature_image_url]
            
            # Process hashtags
            normalized_hashtags = process_hashtags(cursor, hashtags)
            
            # Get current timestamp for creationDate
            creation_date = datetime.now()
            
            # Insert story
            cursor.execute('''
                INSERT INTO "stories" 
                ("topicID", "newsletterID", "storyTitle", "storyContent", "storyPhotos", 
                 "listingIDs", "creationDate", "publicationDate", "freeOrPaid", "hashtags",
                 "creatorUserID", "creatorUserType")
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            ''', (
                topic_id, newsletter_id, story_title, story_content, story_photos,
                listing_ids if listing_ids else None, creation_date, publication_date,
                free_or_paid, normalized_hashtags if normalized_hashtags else None,
                creator_id, creator_type
            ))
            
            story_id = cursor.fetchone()['id']
            
            # TODO: Add notification to topic subscribers (if topicID provided and published now)
            # if topic_id and publication_date and publication_date <= datetime.now():
            #     notifications.notify_topic_subscribers(cursor, topic_id, story_id, story_title)
            
            # TODO: Add notification to newsletter patrons (if newsletterID provided and published now)
            # if newsletter_id and publication_date and publication_date <= datetime.now():
            #     notifications.notify_newsletter_patrons(cursor, newsletter_id, story_id, story_title)
        
        return jsonify({
            'code': 201,
            'data': {
                'storyID': story_id,
                'isDraft': publication_date is None,
                'message': 'Story created successfully' + (' as draft' if publication_date is None else '')
            }
        }), 201
    
    except Exception as e:
        logging.exception("createStory: Error - %s", str(e))
        return jsonify({
            'code': 500,
            'message': 'An error occurred creating the story.'
        }), 500


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
    try:
        story_id = int(storyID)
        
        # Get optional user params for like check
        user_id = request.args.get('userID')
        user_type = request.args.get('userType')
        
        with db_manager.get_cursor() as cursor:
            # Get story with creator info
            cursor.execute('''
                SELECT 
                    s."id",
                    s."topicID",
                    s."newsletterID",
                    s."storyTitle",
                    s."storyContent",
                    s."storyPhotos",
                    s."listingIDs",
                    s."creationDate",
                    s."publicationDate",
                    s."editedAt",
                    s."freeOrPaid",
                    s."hashtags",
                    s."creatorUserID",
                    s."creatorUserType",
                    t."topicName",
                    n."newsletterName",
                    (SELECT COUNT(*) FROM "storiesLikes" WHERE "storyID" = s."id") as "likeCount",
                    (SELECT COUNT(*) FROM "storyComments" WHERE "storyID" = s."id") as "commentCount",
                    CASE 
                        WHEN s."creatorUserType" = 'user' THEN u."username"
                        WHEN s."creatorUserType" = 'producer' THEN p."username"
                        WHEN s."creatorUserType" = 'venue' THEN v."username"
                        ELSE NULL
                    END as "creatorUsername",
                    CASE 
                        WHEN s."creatorUserType" = 'user' THEN u."displayName"
                        WHEN s."creatorUserType" = 'producer' THEN p."producerName"
                        WHEN s."creatorUserType" = 'venue' THEN v."venueName"
                        ELSE NULL
                    END as "creatorDisplayName",
                    CASE 
                        WHEN s."creatorUserType" = 'user' THEN u."photo"
                        WHEN s."creatorUserType" = 'producer' THEN p."photo"
                        WHEN s."creatorUserType" = 'venue' THEN v."photo"
                        ELSE NULL
                    END as "creatorPhoto"
                FROM "stories" s
                LEFT JOIN "topics" t ON s."topicID" = t."id"
                LEFT JOIN "newsletters" n ON s."newsletterID" = n."id"
                LEFT JOIN "users" u ON s."creatorUserType" = 'user' AND s."creatorUserID" = u."id"
                LEFT JOIN "producers" p ON s."creatorUserType" = 'producer' AND s."creatorUserID" = p."id"
                LEFT JOIN "venues" v ON s."creatorUserType" = 'venue' AND s."creatorUserID" = v."id"
                WHERE s."id" = %s
            ''', (story_id,))
            
            story = cursor.fetchone()
            
            if not story:
                return jsonify({
                    'code': 404,
                    'message': 'Story not found'
                }), 404
            
            story_dict = dict(story)
            
            # Check if story is a draft or scheduled (only visible to author)
            is_draft = story_dict['publicationDate'] is None
            is_scheduled = story_dict['publicationDate'] and story_dict['publicationDate'] > datetime.now()
            is_owner = False
            
            if user_id and user_type:
                is_owner = (
                    str(story_dict['creatorUserID']) == str(user_id) and
                    story_dict['creatorUserType'] == user_type
                )
            
            # If draft or scheduled and not owner, return 404
            if (is_draft or is_scheduled) and not is_owner:
                return jsonify({
                    'code': 404,
                    'message': 'Story not found'
                }), 404
            
            story_dict['isDraft'] = is_draft
            story_dict['isScheduled'] = is_scheduled
            story_dict['isOwner'] = is_owner
            
            # Check if user has liked
            story_dict['userLiked'] = False
            if user_id and user_type:
                cursor.execute('''
                    SELECT id FROM "storiesLikes"
                    WHERE "storyID" = %s AND "userID" = %s AND "userType" = %s
                ''', (story_id, user_id, user_type))
                story_dict['userLiked'] = cursor.fetchone() is not None
            
            # Get linked listings info if any
            story_dict['linkedListings'] = []
            if story_dict['listingIDs'] and len(story_dict['listingIDs']) > 0:
                # Build query for all listing IDs
                placeholders = ','.join(['%s'] * len(story_dict['listingIDs']))
                cursor.execute(f'''
                    SELECT 
                        l."id",
                        l."listingName",
                        l."photo",
                        l."drinkType",
                        l."abv",
                        l."originCountry",
                        p."producerName"
                    FROM "listings" l
                    LEFT JOIN "producers" p ON l."producerID" = p."id"
                    WHERE l."id" IN ({placeholders})
                ''', tuple(story_dict['listingIDs']))
                
                listings = cursor.fetchall()
                story_dict['linkedListings'] = [dict(l) for l in listings] if listings else []
            
            # Calculate estimated read time (words / 200 words per minute, round down)
            if story_dict['storyContent']:
                # Strip HTML tags for word count
                import re as regex_module
                text_content = regex_module.sub(r'<[^>]+>', '', story_dict['storyContent'])
                word_count = len(text_content.split())
                story_dict['readTime'] = max(1, word_count // 200)  # At least 1 minute
            else:
                story_dict['readTime'] = 1
            
            # Format dates for JSON
            if story_dict['creationDate']:
                story_dict['creationDate'] = story_dict['creationDate'].isoformat()
            if story_dict['publicationDate']:
                story_dict['publicationDate'] = story_dict['publicationDate'].isoformat()
            if story_dict['editedAt']:
                story_dict['editedAt'] = story_dict['editedAt'].isoformat()
        
        return jsonify({
            'code': 200,
            'data': story_dict
        }), 200
    
    except ValueError:
        return jsonify({
            'code': 400,
            'message': 'Invalid story ID'
        }), 400
    except Exception as e:
        logging.exception("getStory: Error - %s", str(e))
        return jsonify({
            'code': 500,
            'message': 'An error occurred retrieving the story.'
        }), 500


# -----------------------------------------------------------------------------------------
# [PUT] editStory
# Purpose: Update an existing story (author only)
# Used: SpecificStory.vue (inline editing)
# Input:
#   1. storyID - the story to edit
#   2. userID - the user editing
#   3. userType - 'user', 'producer', or 'venue'
#   Optional fields to update:
#   - title
#   - content (HTML)
#   - featureImage (base64, will be uploaded to S3)
#   - listingIDs (array of linked drink IDs)
#   - topicID (can be null to remove)
#   - newsletterID (can be null to remove)
#   - hashtags (array of strings)
#   - publicationDate (ISO string, null for draft)
# Output:
#   200 - Story updated successfully
#   400 - Missing data or validation error
#   403 - Not the author
#   404 - Story not found
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/editStory', methods=['PUT'])
def edit_story():
    try:
        data = request.get_json()
        
        story_id = data.get('storyID')
        user_id = data.get('userID')
        user_type = data.get('userType')
        
        if not all([story_id, user_id, user_type]):
            return jsonify({
                'code': 400,
                'message': 'Missing required fields: storyID, userID, userType'
            }), 400
        
        if user_type not in ['user', 'producer', 'venue']:
            return jsonify({
                'code': 400,
                'message': 'Invalid userType.'
            }), 400
        
        with db_manager.get_cursor() as cursor:
            # Get existing story
            cursor.execute('''
                SELECT id, "creatorUserID", "creatorUserType", "storyPhotos"
                FROM "stories"
                WHERE id = %s
            ''', (story_id,))
            
            story = cursor.fetchone()
            if not story:
                return jsonify({
                    'code': 404,
                    'message': 'Story not found.'
                }), 404
            
            # Check authorization
            if str(story['creatorUserID']) != str(user_id) or story['creatorUserType'] != user_type:
                return jsonify({
                    'code': 403,
                    'message': 'Not authorized to edit this story.'
                }), 403
            
            # Build update query dynamically
            update_fields = []
            update_values = []
            
            if 'title' in data:
                title = data['title']
                if not title or len(title.strip()) == 0:
                    return jsonify({
                        'code': 400,
                        'message': 'Title cannot be empty.'
                    }), 400
                update_fields.append('"title" = %s')
                update_values.append(title.strip())
            
            if 'content' in data:
                content = data['content']
                if not content or len(content.strip()) == 0:
                    return jsonify({
                        'code': 400,
                        'message': 'Content cannot be empty.'
                    }), 400
                update_fields.append('"content" = %s')
                update_values.append(content)
            
            if 'featureImage' in data:
                feature_image = data['featureImage']
                if feature_image:
                    # Upload new feature image to S3
                    image_url = s3Images.uploadBase64ImageToS3(feature_image, 'stories')
                    if not image_url:
                        return jsonify({
                            'code': 500,
                            'message': 'Failed to upload feature image.'
                        }), 500
                    update_fields.append('"storyPhotos" = %s')
                    update_values.append([image_url])  # storyPhotos array with 1 feature image
                else:
                    # Clearing feature image
                    update_fields.append('"storyPhotos" = %s')
                    update_values.append([])
            
            if 'listingIDs' in data:
                listing_ids = data['listingIDs']
                if not isinstance(listing_ids, list):
                    return jsonify({
                        'code': 400,
                        'message': 'listingIDs must be an array.'
                    }), 400
                update_fields.append('"listingIDs" = %s')
                update_values.append(listing_ids)
            
            if 'topicID' in data:
                topic_id = data['topicID']
                if topic_id:
                    # Verify topic exists
                    cursor.execute('SELECT id FROM "storyTopics" WHERE id = %s', (topic_id,))
                    if not cursor.fetchone():
                        return jsonify({
                            'code': 400,
                            'message': 'Invalid topicID.'
                        }), 400
                update_fields.append('"topicID" = %s')
                update_values.append(topic_id)  # Can be null
            
            if 'newsletterID' in data:
                newsletter_id = data['newsletterID']
                if newsletter_id:
                    # Verify newsletter exists
                    cursor.execute('SELECT id FROM "newsletters" WHERE id = %s', (newsletter_id,))
                    if not cursor.fetchone():
                        return jsonify({
                            'code': 400,
                            'message': 'Invalid newsletterID.'
                        }), 400
                update_fields.append('"newsletterID" = %s')
                update_values.append(newsletter_id)  # Can be null
            
            if 'hashtags' in data:
                hashtags = data['hashtags']
                if not isinstance(hashtags, list):
                    return jsonify({
                        'code': 400,
                        'message': 'hashtags must be an array.'
                    }), 400
                # Normalize hashtags
                normalized = []
                for tag in hashtags:
                    tag = tag.strip()
                    if tag.startswith('#'):
                        tag = tag[1:]
                    if tag:
                        normalized.append(tag.lower())
                update_fields.append('"hashtags" = %s')
                update_values.append(normalized)
            
            if 'publicationDate' in data:
                # publicationDate can be None (draft), a date string (scheduled/published)
                pub_date = data['publicationDate']
                if pub_date is not None:
                    try:
                        # Parse and validate the date
                        parsed_date = datetime.fromisoformat(pub_date.replace('Z', '+00:00'))
                        update_fields.append('"publicationDate" = %s')
                        update_values.append(parsed_date)
                    except (ValueError, AttributeError):
                        return jsonify({
                            'code': 400,
                            'message': 'Invalid publicationDate format. Use ISO format.'
                        }), 400
                else:
                    # Set to draft (null)
                    update_fields.append('"publicationDate" = %s')
                    update_values.append(None)
            
            if not update_fields:
                return jsonify({
                    'code': 400,
                    'message': 'No fields to update.'
                }), 400
            
            # Add editedAt timestamp
            update_fields.append('"editedAt" = %s')
            update_values.append(datetime.utcnow())
            
            # Build and execute update query
            update_query = f'''
                UPDATE "stories"
                SET {', '.join(update_fields)}
                WHERE id = %s
            '''
            update_values.append(story_id)
            
            cursor.execute(update_query, tuple(update_values))
        
        return jsonify({
            'code': 200,
            'message': 'Story updated successfully.'
        }), 200
    
    except Exception as e:
        logging.exception("editStory: Error - %s", str(e))
        return jsonify({
            'code': 500,
            'message': 'An error occurred updating the story.'
        }), 500


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
# Note: Cascades to delete likes, comments, comment likes/dislikes
# -----------------------------------------------------------------------------------------
@blueprint.route('/deleteStory', methods=['DELETE'])
def delete_story():
    try:
        data = request.get_json()
        
        story_id = data.get('storyID')
        user_id = data.get('userID')
        user_type = data.get('userType')
        
        if not all([story_id, user_id, user_type]):
            return jsonify({
                'code': 400,
                'message': 'Missing required fields: storyID, userID, userType'
            }), 400
        
        if user_type not in ['user', 'producer', 'venue']:
            return jsonify({
                'code': 400,
                'message': 'Invalid userType.'
            }), 400
        
        with db_manager.get_cursor() as cursor:
            # Get story
            cursor.execute('''
                SELECT id, "creatorUserID", "creatorUserType", title
                FROM "stories"
                WHERE id = %s
            ''', (story_id,))
            
            story = cursor.fetchone()
            if not story:
                return jsonify({
                    'code': 404,
                    'message': 'Story not found.'
                }), 404
            
            # Check authorization
            if str(story['creatorUserID']) != str(user_id) or story['creatorUserType'] != user_type:
                return jsonify({
                    'code': 403,
                    'message': 'Not authorized to delete this story.'
                }), 403
            
            # Delete story (cascades to likes, comments, comment likes/dislikes via ON DELETE CASCADE)
            cursor.execute('DELETE FROM "stories" WHERE id = %s', (story_id,))
        
        return jsonify({
            'code': 200,
            'message': 'Story deleted successfully.'
        }), 200
    
    except Exception as e:
        logging.exception("deleteStory: Error - %s", str(e))
        return jsonify({
            'code': 500,
            'message': 'An error occurred deleting the story.'
        }), 500


# -----------------------------------------------------------------------------------------
# [GET] getUserStories/<userID>/<userType>/<offset>
# Purpose: Get paginated stories by a specific user
# Used: UserStories.vue
# Input: userID, userType, offset (path params)
# Optional query params:
#   - viewerID, viewerType - to determine if viewing own profile (can see drafts)
# Output:
#   200 - List of user's stories (sorted by publicationDate DESC, drafts last)
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/getUserStories/<userID>/<userType>/<offset>', methods=['GET'])
def get_user_stories(userID, userType, offset):
    try:
        user_id = int(userID)
        offset_val = int(offset)
        limit = 12  # Stories per page
        
        # Validate userType
        if userType not in ['user', 'producer', 'venue']:
            return jsonify({
                'code': 400,
                'message': 'Invalid userType. Must be user, producer, or venue.'
            }), 400
        
        # Check if viewer is the owner (can see drafts/scheduled)
        viewer_id = request.args.get('viewerID')
        viewer_type = request.args.get('viewerType')
        is_own_profile = (
            viewer_id and viewer_type and
            str(user_id) == str(viewer_id) and
            userType == viewer_type
        )
        
        with db_manager.get_cursor() as cursor:
            # Build query based on whether viewing own profile
            if is_own_profile:
                # Owner can see all their stories (drafts, scheduled, published)
                where_clause = '''
                    WHERE s."creatorUserID" = %s AND s."creatorUserType" = %s
                '''
                # Sort: published first (by date DESC), then scheduled, then drafts
                order_clause = '''
                    ORDER BY 
                        CASE 
                            WHEN s."publicationDate" IS NULL THEN 2
                            WHEN s."publicationDate" > NOW() THEN 1
                            ELSE 0
                        END,
                        s."publicationDate" DESC NULLS LAST
                '''
            else:
                # Others can only see published stories
                where_clause = '''
                    WHERE s."creatorUserID" = %s 
                    AND s."creatorUserType" = %s
                    AND s."publicationDate" IS NOT NULL 
                    AND s."publicationDate" <= NOW()
                '''
                order_clause = 'ORDER BY s."publicationDate" DESC'
            
            # Get total count
            count_query = f'''
                SELECT COUNT(*) as total
                FROM "stories" s
                {where_clause}
            '''
            cursor.execute(count_query, (user_id, userType))
            total_count = cursor.fetchone()['total']
            
            # Get paginated stories
            query = f'''
                SELECT 
                    s."id",
                    s."storyTitle",
                    s."storyContent",
                    s."storyPhotos",
                    s."topicID",
                    s."newsletterID",
                    s."publicationDate",
                    s."creationDate",
                    s."creatorUserID",
                    s."creatorUserType",
                    t."topicName",
                    n."newsletterName",
                    CASE 
                        WHEN s."creatorUserType" = 'user' THEN u."username"
                        WHEN s."creatorUserType" = 'producer' THEN p."username"
                        WHEN s."creatorUserType" = 'venue' THEN v."username"
                        ELSE NULL
                    END as "creatorUsername",
                    CASE 
                        WHEN s."creatorUserType" = 'user' THEN u."displayName"
                        WHEN s."creatorUserType" = 'producer' THEN p."producerName"
                        WHEN s."creatorUserType" = 'venue' THEN v."venueName"
                        ELSE NULL
                    END as "creatorDisplayName",
                    CASE 
                        WHEN s."creatorUserType" = 'user' THEN u."photo"
                        WHEN s."creatorUserType" = 'producer' THEN p."photo"
                        WHEN s."creatorUserType" = 'venue' THEN v."photo"
                        ELSE NULL
                    END as "creatorPhoto"
                FROM "stories" s
                LEFT JOIN "topics" t ON s."topicID" = t."id"
                LEFT JOIN "newsletters" n ON s."newsletterID" = n."id"
                LEFT JOIN "users" u ON s."creatorUserType" = 'user' AND s."creatorUserID" = u."id"
                LEFT JOIN "producers" p ON s."creatorUserType" = 'producer' AND s."creatorUserID" = p."id"
                LEFT JOIN "venues" v ON s."creatorUserType" = 'venue' AND s."creatorUserID" = v."id"
                {where_clause}
                {order_clause}
                LIMIT %s OFFSET %s
            '''
            cursor.execute(query, (user_id, userType, limit, offset_val))
            stories = cursor.fetchall()
            
            # Format stories for response
            formatted_stories = []
            for story in stories:
                story_dict = dict(story)
                
                # Get feature photo (first photo)
                feature_photo = None
                if story_dict['storyPhotos'] and len(story_dict['storyPhotos']) > 0:
                    feature_photo = story_dict['storyPhotos'][0]
                
                # Generate preview excerpt (first 150 chars, strip HTML)
                preview_excerpt = ''
                if story_dict['storyContent']:
                    # Strip HTML tags
                    text_content = re.sub(r'<[^>]+>', '', story_dict['storyContent'])
                    preview_excerpt = text_content[:150].strip()
                    if len(text_content) > 150:
                        preview_excerpt += '...'
                
                # Determine status
                is_draft = story_dict['publicationDate'] is None
                is_scheduled = (
                    story_dict['publicationDate'] and 
                    story_dict['publicationDate'] > datetime.now()
                )
                
                formatted_stories.append({
                    'id': story_dict['id'],
                    'storyTitle': story_dict['storyTitle'],
                    'previewExcerpt': preview_excerpt,
                    'featurePhoto': feature_photo,
                    'publicationDate': story_dict['publicationDate'].isoformat() if story_dict['publicationDate'] else None,
                    'creationDate': story_dict['creationDate'].isoformat() if story_dict['creationDate'] else None,
                    'topicID': story_dict['topicID'],
                    'topicName': story_dict['topicName'],
                    'newsletterID': story_dict['newsletterID'],
                    'newsletterName': story_dict['newsletterName'],
                    'creatorUsername': story_dict['creatorUsername'],
                    'creatorDisplayName': story_dict['creatorDisplayName'],
                    'creatorPhoto': story_dict['creatorPhoto'],
                    'isDraft': is_draft,
                    'isScheduled': is_scheduled,
                })
            
            return jsonify({
                'code': 200,
                'data': formatted_stories,
                'totalCount': total_count,
                'hasMore': (offset_val + limit) < total_count
            }), 200
    
    except ValueError:
        return jsonify({
            'code': 400,
            'message': 'Invalid userID or offset'
        }), 400
    except Exception as e:
        logging.exception("getUserStories: Error - %s", str(e))
        return jsonify({
            'code': 500,
            'message': 'An error occurred retrieving user stories.'
        }), 500


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
    try:
        data = request.get_json()
        
        story_id = data.get('storyID')
        user_id = data.get('userID')
        user_type = data.get('userType')
        
        if not all([story_id, user_id, user_type]):
            return jsonify({
                'code': 400,
                'message': 'Missing required fields: storyID, userID, userType'
            }), 400
        
        if user_type not in ['user', 'producer', 'venue']:
            return jsonify({
                'code': 400,
                'message': 'Invalid userType. Must be user, producer, or venue.'
            }), 400
        
        with db_manager.get_cursor() as cursor:
            # Verify story exists and is published
            cursor.execute('''
                SELECT id FROM "stories" 
                WHERE id = %s AND "publicationDate" IS NOT NULL AND "publicationDate" <= NOW()
            ''', (story_id,))
            if not cursor.fetchone():
                return jsonify({
                    'code': 404,
                    'message': 'Story not found or not yet published.'
                }), 404
            
            # Check if already liked
            cursor.execute('''
                SELECT id FROM "storiesLikes"
                WHERE "storyID" = %s AND "userID" = %s AND "userType" = %s
            ''', (story_id, user_id, user_type))
            if cursor.fetchone():
                return jsonify({
                    'code': 400,
                    'message': 'Already liked this story.'
                }), 400
            
            # Insert like
            cursor.execute('''
                INSERT INTO "storiesLikes" ("storyID", "userID", "userType")
                VALUES (%s, %s, %s)
                RETURNING id
            ''', (story_id, user_id, user_type))
            like_id = cursor.fetchone()['id']
            
            # Get updated like count
            cursor.execute('''
                SELECT COUNT(*) as count FROM "storiesLikes" WHERE "storyID" = %s
            ''', (story_id,))
            like_count = cursor.fetchone()['count']
        
        return jsonify({
            'code': 201,
            'message': 'Story liked successfully.',
            'data': {'likeID': like_id, 'likeCount': like_count}
        }), 201
    
    except Exception as e:
        logging.exception("likeStory: Error - %s", str(e))
        return jsonify({
            'code': 500,
            'message': 'An error occurred while liking the story.'
        }), 500


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
    try:
        data = request.get_json()
        
        story_id = data.get('storyID')
        user_id = data.get('userID')
        user_type = data.get('userType')
        
        if not all([story_id, user_id, user_type]):
            return jsonify({
                'code': 400,
                'message': 'Missing required fields: storyID, userID, userType'
            }), 400
        
        if user_type not in ['user', 'producer', 'venue']:
            return jsonify({
                'code': 400,
                'message': 'Invalid userType. Must be user, producer, or venue.'
            }), 400
        
        with db_manager.get_cursor() as cursor:
            # Delete like
            cursor.execute('''
                DELETE FROM "storiesLikes"
                WHERE "storyID" = %s AND "userID" = %s AND "userType" = %s
                RETURNING id
            ''', (story_id, user_id, user_type))
            deleted = cursor.fetchone()
            
            if not deleted:
                return jsonify({
                    'code': 400,
                    'message': 'You have not liked this story.'
                }), 400
            
            # Get updated like count
            cursor.execute('''
                SELECT COUNT(*) as count FROM "storiesLikes" WHERE "storyID" = %s
            ''', (story_id,))
            like_count = cursor.fetchone()['count']
        
        return jsonify({
            'code': 200,
            'message': 'Story unliked successfully.',
            'data': {'likeCount': like_count}
        }), 200
    
    except Exception as e:
        logging.exception("unlikeStory: Error - %s", str(e))
        return jsonify({
            'code': 500,
            'message': 'An error occurred while unliking the story.'
        }), 500


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
    try:
        data = request.get_json()
        
        story_id = data.get('storyID')
        user_id = data.get('userID')
        user_type = data.get('userType')
        comment_content = data.get('commentContent', '').strip()
        parent_comment_id = data.get('parentCommentID')  # Optional for replies
        
        if not all([story_id, user_id, user_type]):
            return jsonify({
                'code': 400,
                'message': 'Missing required fields: storyID, userID, userType'
            }), 400
        
        if not comment_content:
            return jsonify({
                'code': 400,
                'message': 'Comment content is required.'
            }), 400
        
        if len(comment_content) > 5000:
            return jsonify({
                'code': 400,
                'message': 'Comment cannot exceed 5000 characters.'
            }), 400
        
        if user_type not in ['user', 'producer', 'venue']:
            return jsonify({
                'code': 400,
                'message': 'Invalid userType. Must be user, producer, or venue.'
            }), 400
        
        with db_manager.get_cursor() as cursor:
            # Verify story exists and is published
            cursor.execute('''
                SELECT id FROM "stories" 
                WHERE id = %s AND "publicationDate" IS NOT NULL AND "publicationDate" <= NOW()
            ''', (story_id,))
            if not cursor.fetchone():
                return jsonify({
                    'code': 404,
                    'message': 'Story not found or not yet published.'
                }), 404
            
            # If this is a reply, verify parent comment exists and belongs to this story
            if parent_comment_id:
                cursor.execute('''
                    SELECT id FROM "storyComments" 
                    WHERE id = %s AND "storyID" = %s AND "parentCommentID" IS NULL
                ''', (parent_comment_id, story_id))
                if not cursor.fetchone():
                    return jsonify({
                        'code': 404,
                        'message': 'Parent comment not found or cannot reply to a reply.'
                    }), 404
            
            # Insert comment
            cursor.execute('''
                INSERT INTO "storyComments" 
                ("storyID", "parentCommentID", "commentContent", "userID", "userType")
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id, "commentDate"
            ''', (story_id, parent_comment_id, comment_content, user_id, user_type))
            
            result = cursor.fetchone()
            comment_id = result['id']
            comment_date = result['commentDate']
            
            # Get commenter info to return with comment
            commenter_info = get_user_info_by_id(cursor, user_id, user_type)
        
        return jsonify({
            'code': 201,
            'message': 'Comment posted successfully.',
            'data': {
                'commentID': comment_id,
                'commentDate': comment_date.isoformat() if comment_date else None,
                'commenterInfo': commenter_info
            }
        }), 201
    
    except Exception as e:
        logging.exception("createStoryComment: Error - %s", str(e))
        return jsonify({
            'code': 500,
            'message': 'An error occurred while posting the comment.'
        }), 500


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
    try:
        story_id = int(storyID)
        offset_val = int(offset)
        limit = 20  # Root comments per page
        replies_limit = 5  # Initial replies per comment
        
        user_id = request.args.get('userID')
        user_type = request.args.get('userType')
        
        with db_manager.get_cursor() as cursor:
            # Verify story exists
            cursor.execute('SELECT id, "creatorUserID", "creatorUserType" FROM "stories" WHERE id = %s', (story_id,))
            story = cursor.fetchone()
            if not story:
                return jsonify({
                    'code': 404,
                    'message': 'Story not found.'
                }), 404
            
            story_author_id = story['creatorUserID']
            story_author_type = story['creatorUserType']
            
            # Get total comment count
            cursor.execute('SELECT COUNT(*) as total FROM "storyComments" WHERE "storyID" = %s', (story_id,))
            total_count = cursor.fetchone()['total']
            
            # Get root comments (parentCommentID IS NULL), ordered newest first
            cursor.execute('''
                SELECT 
                    c."id",
                    c."storyID",
                    c."parentCommentID",
                    c."commentContent",
                    c."commentDate",
                    c."userID",
                    c."userType"
                FROM "storyComments" c
                WHERE c."storyID" = %s AND c."parentCommentID" IS NULL
                ORDER BY c."commentDate" DESC
                LIMIT %s OFFSET %s
            ''', (story_id, limit, offset_val))
            
            root_comments = cursor.fetchall()
            result = []
            
            for comment in root_comments:
                comment_dict = dict(comment)
                comment_id = comment['id']
                
                # Get commenter info
                commenter_info = get_user_info_by_id(cursor, comment['userID'], comment['userType'])
                comment_dict['commenterInfo'] = commenter_info
                
                # Get like and dislike counts
                cursor.execute('SELECT COUNT(*) as count FROM "storyCommentsLikes" WHERE "commentID" = %s', (comment_id,))
                like_count = cursor.fetchone()['count']
                
                cursor.execute('SELECT COUNT(*) as count FROM "storyCommentsDislikes" WHERE "commentID" = %s', (comment_id,))
                dislike_count = cursor.fetchone()['count']
                
                comment_dict['likeCount'] = like_count
                comment_dict['dislikeCount'] = dislike_count
                comment_dict['voteCount'] = like_count - dislike_count
                
                # Check user's vote status
                comment_dict['userVote'] = None
                if user_id and user_type:
                    cursor.execute('''
                        SELECT id FROM "storyCommentsLikes" 
                        WHERE "commentID" = %s AND "userID" = %s AND "userType" = %s
                    ''', (comment_id, user_id, user_type))
                    if cursor.fetchone():
                        comment_dict['userVote'] = 'up'
                    else:
                        cursor.execute('''
                            SELECT id FROM "storyCommentsDislikes" 
                            WHERE "commentID" = %s AND "userID" = %s AND "userType" = %s
                        ''', (comment_id, user_id, user_type))
                        if cursor.fetchone():
                            comment_dict['userVote'] = 'down'
                
                # Check if user can delete (is commenter or story author)
                comment_dict['canDelete'] = False
                if user_id and user_type:
                    is_commenter = (str(comment['userID']) == str(user_id) and comment['userType'] == user_type)
                    is_story_author = (str(story_author_id) == str(user_id) and story_author_type == user_type)
                    comment_dict['canDelete'] = is_commenter or is_story_author
                
                # Get reply count
                cursor.execute('SELECT COUNT(*) as count FROM "storyComments" WHERE "parentCommentID" = %s', (comment_id,))
                comment_dict['replyCount'] = cursor.fetchone()['count']
                
                # Get first 5 replies (oldest first for conversation flow)
                cursor.execute('''
                    SELECT 
                        c."id",
                        c."storyID",
                        c."parentCommentID",
                        c."commentContent",
                        c."commentDate",
                        c."userID",
                        c."userType"
                    FROM "storyComments" c
                    WHERE c."parentCommentID" = %s
                    ORDER BY c."commentDate" ASC
                    LIMIT %s
                ''', (comment_id, replies_limit))
                
                replies = cursor.fetchall()
                replies_list = []
                
                for reply in replies:
                    reply_dict = dict(reply)
                    
                    # Get reply commenter info
                    reply_commenter_info = get_user_info_by_id(cursor, reply['userID'], reply['userType'])
                    reply_dict['commenterInfo'] = reply_commenter_info
                    
                    # Get reply votes
                    cursor.execute('SELECT COUNT(*) as count FROM "storyCommentsLikes" WHERE "commentID" = %s', (reply['id'],))
                    reply_likes = cursor.fetchone()['count']
                    cursor.execute('SELECT COUNT(*) as count FROM "storyCommentsDislikes" WHERE "commentID" = %s', (reply['id'],))
                    reply_dislikes = cursor.fetchone()['count']
                    
                    reply_dict['likeCount'] = reply_likes
                    reply_dict['dislikeCount'] = reply_dislikes
                    reply_dict['voteCount'] = reply_likes - reply_dislikes
                    
                    # Check user's vote on reply
                    reply_dict['userVote'] = None
                    if user_id and user_type:
                        cursor.execute('''
                            SELECT id FROM "storyCommentsLikes" 
                            WHERE "commentID" = %s AND "userID" = %s AND "userType" = %s
                        ''', (reply['id'], user_id, user_type))
                        if cursor.fetchone():
                            reply_dict['userVote'] = 'up'
                        else:
                            cursor.execute('''
                                SELECT id FROM "storyCommentsDislikes" 
                                WHERE "commentID" = %s AND "userID" = %s AND "userType" = %s
                            ''', (reply['id'], user_id, user_type))
                            if cursor.fetchone():
                                reply_dict['userVote'] = 'down'
                    
                    # Check if user can delete reply
                    reply_dict['canDelete'] = False
                    if user_id and user_type:
                        is_reply_commenter = (str(reply['userID']) == str(user_id) and reply['userType'] == user_type)
                        is_story_author = (str(story_author_id) == str(user_id) and story_author_type == user_type)
                        reply_dict['canDelete'] = is_reply_commenter or is_story_author
                    
                    # Format date
                    if reply_dict['commentDate']:
                        reply_dict['commentDate'] = reply_dict['commentDate'].isoformat()
                    
                    replies_list.append(reply_dict)
                
                comment_dict['replies'] = replies_list
                comment_dict['hasMoreReplies'] = len(replies_list) < comment_dict['replyCount']
                
                # Format date
                if comment_dict['commentDate']:
                    comment_dict['commentDate'] = comment_dict['commentDate'].isoformat()
                
                result.append(comment_dict)
        
        return jsonify({
            'code': 200,
            'data': result,
            'totalCount': total_count,
            'hasMore': (offset_val + limit) < total_count
        }), 200
    
    except ValueError:
        return jsonify({
            'code': 400,
            'message': 'Invalid storyID or offset'
        }), 400
    except Exception as e:
        logging.exception("getStoryComments: Error - %s", str(e))
        return jsonify({
            'code': 500,
            'message': 'An error occurred retrieving comments.'
        }), 500


# -----------------------------------------------------------------------------------------
# [POST] likeStoryComment
# Purpose: Like a comment (removes dislike if exists, toggles like)
# Used: SpecificStory.vue
# Input:
#   1. commentID - the comment to like
#   2. userID - the user liking
#   3. userType - 'user', 'producer', or 'venue'
# Output:
#   200 - Like toggled successfully
#   400 - Missing data
#   404 - Comment not found
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/likeStoryComment', methods=['POST'])
def like_story_comment():
    try:
        data = request.get_json()
        
        comment_id = data.get('commentID')
        user_id = data.get('userID')
        user_type = data.get('userType')
        
        if not all([comment_id, user_id, user_type]):
            return jsonify({
                'code': 400,
                'message': 'Missing required fields: commentID, userID, userType'
            }), 400
        
        if user_type not in ['user', 'producer', 'venue']:
            return jsonify({
                'code': 400,
                'message': 'Invalid userType.'
            }), 400
        
        with db_manager.get_cursor() as cursor:
            # Verify comment exists
            cursor.execute('SELECT id FROM "storyComments" WHERE id = %s', (comment_id,))
            if not cursor.fetchone():
                return jsonify({
                    'code': 404,
                    'message': 'Comment not found.'
                }), 404
            
            # Remove any existing dislike
            cursor.execute('''
                DELETE FROM "storyCommentsDislikes"
                WHERE "commentID" = %s AND "userID" = %s AND "userType" = %s
            ''', (comment_id, user_id, user_type))
            
            # Check if already liked (toggle)
            cursor.execute('''
                SELECT id FROM "storyCommentsLikes"
                WHERE "commentID" = %s AND "userID" = %s AND "userType" = %s
            ''', (comment_id, user_id, user_type))
            existing_like = cursor.fetchone()
            
            if existing_like:
                # Remove like (toggle off)
                cursor.execute('''
                    DELETE FROM "storyCommentsLikes" WHERE id = %s
                ''', (existing_like['id'],))
                action = 'unliked'
            else:
                # Add like
                cursor.execute('''
                    INSERT INTO "storyCommentsLikes" ("commentID", "userID", "userType")
                    VALUES (%s, %s, %s)
                ''', (comment_id, user_id, user_type))
                action = 'liked'
            
            # Get updated counts
            cursor.execute('SELECT COUNT(*) as count FROM "storyCommentsLikes" WHERE "commentID" = %s', (comment_id,))
            like_count = cursor.fetchone()['count']
            cursor.execute('SELECT COUNT(*) as count FROM "storyCommentsDislikes" WHERE "commentID" = %s', (comment_id,))
            dislike_count = cursor.fetchone()['count']
        
        return jsonify({
            'code': 200,
            'message': f'Comment {action}.',
            'data': {
                'likeCount': like_count,
                'dislikeCount': dislike_count,
                'voteCount': like_count - dislike_count,
                'userVote': 'up' if action == 'liked' else None
            }
        }), 200
    
    except Exception as e:
        logging.exception("likeStoryComment: Error - %s", str(e))
        return jsonify({
            'code': 500,
            'message': 'An error occurred.'
        }), 500


# -----------------------------------------------------------------------------------------
# [POST] dislikeStoryComment
# Purpose: Dislike a comment (removes like if exists, toggles dislike)
# Used: SpecificStory.vue
# Input:
#   1. commentID - the comment to dislike
#   2. userID - the user disliking
#   3. userType - 'user', 'producer', or 'venue'
# Output:
#   200 - Dislike toggled successfully
#   400 - Missing data
#   404 - Comment not found
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/dislikeStoryComment', methods=['POST'])
def dislike_story_comment():
    try:
        data = request.get_json()
        
        comment_id = data.get('commentID')
        user_id = data.get('userID')
        user_type = data.get('userType')
        
        if not all([comment_id, user_id, user_type]):
            return jsonify({
                'code': 400,
                'message': 'Missing required fields: commentID, userID, userType'
            }), 400
        
        if user_type not in ['user', 'producer', 'venue']:
            return jsonify({
                'code': 400,
                'message': 'Invalid userType.'
            }), 400
        
        with db_manager.get_cursor() as cursor:
            # Verify comment exists
            cursor.execute('SELECT id FROM "storyComments" WHERE id = %s', (comment_id,))
            if not cursor.fetchone():
                return jsonify({
                    'code': 404,
                    'message': 'Comment not found.'
                }), 404
            
            # Remove any existing like
            cursor.execute('''
                DELETE FROM "storyCommentsLikes"
                WHERE "commentID" = %s AND "userID" = %s AND "userType" = %s
            ''', (comment_id, user_id, user_type))
            
            # Check if already disliked (toggle)
            cursor.execute('''
                SELECT id FROM "storyCommentsDislikes"
                WHERE "commentID" = %s AND "userID" = %s AND "userType" = %s
            ''', (comment_id, user_id, user_type))
            existing_dislike = cursor.fetchone()
            
            if existing_dislike:
                # Remove dislike (toggle off)
                cursor.execute('''
                    DELETE FROM "storyCommentsDislikes" WHERE id = %s
                ''', (existing_dislike['id'],))
                action = 'undisliked'
            else:
                # Add dislike
                cursor.execute('''
                    INSERT INTO "storyCommentsDislikes" ("commentID", "userID", "userType")
                    VALUES (%s, %s, %s)
                ''', (comment_id, user_id, user_type))
                action = 'disliked'
            
            # Get updated counts
            cursor.execute('SELECT COUNT(*) as count FROM "storyCommentsLikes" WHERE "commentID" = %s', (comment_id,))
            like_count = cursor.fetchone()['count']
            cursor.execute('SELECT COUNT(*) as count FROM "storyCommentsDislikes" WHERE "commentID" = %s', (comment_id,))
            dislike_count = cursor.fetchone()['count']
        
        return jsonify({
            'code': 200,
            'message': f'Comment {action}.',
            'data': {
                'likeCount': like_count,
                'dislikeCount': dislike_count,
                'voteCount': like_count - dislike_count,
                'userVote': 'down' if action == 'disliked' else None
            }
        }), 200
    
    except Exception as e:
        logging.exception("dislikeStoryComment: Error - %s", str(e))
        return jsonify({
            'code': 500,
            'message': 'An error occurred.'
        }), 500


# -----------------------------------------------------------------------------------------
# [DELETE] deleteStoryComment
# Purpose: Delete a comment (comment author or story author only)
# Used: SpecificStory.vue
# Input:
#   1. commentID - the comment to delete
#   2. userID - the user deleting
#   3. userType - 'user', 'producer', or 'venue'
# Output:
#   200 - Comment deleted successfully
#   403 - Not authorized
#   404 - Comment not found
#   500 - Server error
# Note: Cascade deletes likes, dislikes, and child replies
# -----------------------------------------------------------------------------------------
@blueprint.route('/deleteStoryComment', methods=['DELETE'])
def delete_story_comment():
    try:
        data = request.get_json()
        
        comment_id = data.get('commentID')
        user_id = data.get('userID')
        user_type = data.get('userType')
        
        if not all([comment_id, user_id, user_type]):
            return jsonify({
                'code': 400,
                'message': 'Missing required fields: commentID, userID, userType'
            }), 400
        
        if user_type not in ['user', 'producer', 'venue']:
            return jsonify({
                'code': 400,
                'message': 'Invalid userType.'
            }), 400
        
        with db_manager.get_cursor() as cursor:
            # Get comment and story info
            cursor.execute('''
                SELECT c."id", c."userID", c."userType", c."storyID",
                       s."creatorUserID", s."creatorUserType"
                FROM "storyComments" c
                JOIN "stories" s ON c."storyID" = s."id"
                WHERE c."id" = %s
            ''', (comment_id,))
            
            comment = cursor.fetchone()
            if not comment:
                return jsonify({
                    'code': 404,
                    'message': 'Comment not found.'
                }), 404
            
            # Check authorization: comment author or story author
            is_comment_author = (str(comment['userID']) == str(user_id) and comment['userType'] == user_type)
            is_story_author = (str(comment['creatorUserID']) == str(user_id) and comment['creatorUserType'] == user_type)
            
            if not (is_comment_author or is_story_author):
                return jsonify({
                    'code': 403,
                    'message': 'Not authorized to delete this comment.'
                }), 403
            
            # Delete comment (cascades to likes, dislikes, and replies via ON DELETE CASCADE)
            cursor.execute('DELETE FROM "storyComments" WHERE id = %s', (comment_id,))
        
        return jsonify({
            'code': 200,
            'message': 'Comment deleted successfully.'
        }), 200
    
    except Exception as e:
        logging.exception("deleteStoryComment: Error - %s", str(e))
        return jsonify({
            'code': 500,
            'message': 'An error occurred deleting the comment.'
        }), 500
