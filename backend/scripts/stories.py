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
