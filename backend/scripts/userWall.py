# Routes: /getWallPosts (GET), /getUserWallLikesDislikes (GET),
#         /addWallPost (POST), /addWallPostComment (POST),
#         /likeUnlikeWallPost (PUT), /dislikeUndislikeWallPost (PUT),
#         /editWallPost (PUT), /editWallPostComment (PUT),
#         /removeWallPost (DELETE), /removeWallPostComment (DELETE)
# -----------------------------------------------------------------------------------------

import os
from flask import Blueprint, g, jsonify, request
from datetime import datetime
from scripts import pointsHelperFunc, badge_helpers, notifications
import re

# Import the database manager for connection pooling
from app import db_manager

# Use to upload image to S3
import s3Images

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)


# -----------------------------------------------------------------------------------------
# Helper function to retrieve user information by user ID
def getUserInfoByID(cur, user_id):
    """
    Get user information by user ID.
    Returns: dict with id, displayName, photo, username
    """
    cur.execute('SELECT id, "displayName", photo, username FROM "users" WHERE id = %s', (user_id,))
    user_info = cur.fetchone()
    
    if user_info:
        return {
            'id': user_info['id'],
            'displayName': user_info['displayName'],
            'photo': user_info['photo'],
            'username': user_info['username']
        }
    return None


# -----------------------------------------------------------------------------------------
# [GET] getWallPosts
# Purpose: Get the latest 10 posts on a user's wall with pagination
# Used: UserPersonalWall.vue [views folder inside Users folder]
# Input: 
#   1. Wall Owner ID (the user whose wall we're viewing)
#   2. Last seen ID (for pagination, use '0' for initial load)
# Output: Possible return codes [200 - Retrieval success, 404 - No posts found, 500 - An error occurred]
@blueprint.route('/getWallPosts/<wallOwnerID>/<last_seen_id>', methods=['GET'])
def getWallPosts(wallOwnerID, last_seen_id):
    # Dictionary to track if user information has been retrieved
    users_retrieved_list = {}
    
    # Filtered post list to be returned
    filtered_post_list = []
    
    try:
        with db_manager.get_cursor() as cursor:
            # Check if wall owner exists
            cursor.execute('SELECT * FROM "users" WHERE id = %s', (wallOwnerID,))
            user = cursor.fetchone()
            
            if not user:
                return jsonify({
                    'error': f'No such user exists for user id: {wallOwnerID}'
                }), 404
            
            # Set the limit
            limit = 10
            
            # Step 1: Get the latest posts on this user's wall
            if last_seen_id == '0':
                cursor.execute(
                    'SELECT * FROM "userWallPosts" WHERE "wallOwnerID" = %s ORDER BY "postDate" DESC LIMIT %s',
                    (wallOwnerID, limit,)
                )
            else:
                cursor.execute(
                    'SELECT * FROM "userWallPosts" WHERE "wallOwnerID" = %s AND "id" < %s ORDER BY "postDate" DESC LIMIT %s',
                    (wallOwnerID, last_seen_id, limit,)
                )
            
            post_info = cursor.fetchall()
            
            if not post_info:
                return jsonify({
                    'error': 'No posts yet'
                }), 404
            
            # Step 2: Get additional info for each post
            for post in post_info:
                poster_id = post['posterUserID']
                post_id = post['id']
                
                # Check if posterID is null
                if not poster_id:
                    continue
                
                # Get the poster's information
                if poster_id not in users_retrieved_list:
                    poster_info = getUserInfoByID(cursor, poster_id)
                    
                    if not poster_info:
                        continue
                    
                    users_retrieved_list[poster_id] = poster_info
                    post['posterInfo'] = poster_info
                else:
                    post['posterInfo'] = users_retrieved_list[poster_id]
                
                # Get wall owner info if different from poster
                wall_owner_id = post['wallOwnerID']
                if wall_owner_id not in users_retrieved_list:
                    wall_owner_info = getUserInfoByID(cursor, wall_owner_id)
                    if wall_owner_info:
                        users_retrieved_list[wall_owner_id] = wall_owner_info
                        post['wallOwnerInfo'] = wall_owner_info
                else:
                    post['wallOwnerInfo'] = users_retrieved_list[wall_owner_id]
                
                # Get the total number of likes for each post
                cursor.execute(
                    'SELECT COUNT(*) as "totalLikes" FROM "userWallPostLikes" WHERE "postID" = %s',
                    (post_id,)
                )
                total_likes = cursor.fetchone()
                post['totalLikes'] = total_likes['totalLikes'] if total_likes else 0
                
                # Get the total number of dislikes for each post
                cursor.execute(
                    'SELECT COUNT(*) as "totalDislikes" FROM "userWallPostDislikes" WHERE "postID" = %s',
                    (post_id,)
                )
                total_dislikes = cursor.fetchone()
                post['totalDislikes'] = total_dislikes['totalDislikes'] if total_dislikes else 0
                
                # Get the total number of comments for each post
                cursor.execute(
                    'SELECT COUNT(*) as "totalComments" FROM "userWallPostComments" WHERE "postID" = %s',
                    (post_id,)
                )
                total_comments = cursor.fetchone()
                post['totalComments'] = total_comments['totalComments'] if total_comments else 0
                
                # Get location (venue) info if provided
                if post.get('location'):
                    cursor.execute(
                        'SELECT id, "venueName" FROM "venues" WHERE id = %s',
                        (post['location'],)
                    )
                    venue_info = cursor.fetchone()
                    post['locationInfo'] = venue_info if venue_info else None
                
                # Get tagged users info
                if post.get('taggedUsers') and len(post['taggedUsers']) > 0:
                    tagged_users_info = []
                    for tagged_user_id in post['taggedUsers']:
                        if tagged_user_id in users_retrieved_list:
                            tagged_users_info.append(users_retrieved_list[tagged_user_id])
                        else:
                            tagged_info = getUserInfoByID(cursor, tagged_user_id)
                            if tagged_info:
                                users_retrieved_list[tagged_user_id] = tagged_info
                                tagged_users_info.append(tagged_info)
                    post['taggedUsersInfo'] = tagged_users_info
                
                # Add post to filtered list
                filtered_post_list.append(post)
            
            return jsonify({
                'data': filtered_post_list
            }), 200
    
    except Exception as e:
        print(str(e))
        return jsonify({
            "code": 500,
            "message": "An error occurred retrieving the posts."
        }), 500


# -----------------------------------------------------------------------------------------
# [GET] getUserWallLikesDislikes
# Purpose: Get the posts that a specific user has liked and disliked on a specific wall
# Used: UserPersonalWall.vue [views folder inside Users folder]
# Output: Possible return codes [200 - Retrieval success, 500 - An error occurred]
@blueprint.route('/getUserWallLikesDislikes/<userID>/<wallOwnerID>', methods=['GET'])
def getUserWallLikesDislikes(userID, wallOwnerID):
    try:
        with db_manager.get_cursor() as cursor:
            # Get liked posts
            cursor.execute(
                '''SELECT "postID" FROM "userWallPostLikes" l
                   JOIN "userWallPosts" p ON l."postID" = p.id
                   WHERE l."userID" = %s AND p."wallOwnerID" = %s''',
                (userID, wallOwnerID,)
            )
            liked_posts = cursor.fetchall()
            
            # Get disliked posts
            cursor.execute(
                '''SELECT "postID" FROM "userWallPostDislikes" d
                   JOIN "userWallPosts" p ON d."postID" = p.id
                   WHERE d."userID" = %s AND p."wallOwnerID" = %s''',
                (userID, wallOwnerID,)
            )
            disliked_posts = cursor.fetchall()
            
            # Format the liked_posts into a list of postID
            liked_posts = [post['postID'] for post in liked_posts] if liked_posts else []
            
            # Format the disliked_posts into a list of postID
            disliked_posts = [post['postID'] for post in disliked_posts] if disliked_posts else []
            
            return jsonify({
                'liked_posts': liked_posts,
                'disliked_posts': disliked_posts
            }), 200
    
    except Exception as e:
        print(str(e))
        return jsonify({
            "code": 500,
            "message": "An error occurred retrieving the likes/dislikes."
        }), 500


# -----------------------------------------------------------------------------------------
# [GET] getWallPostComments
# Purpose: Get comments for a specific wall post
# Used: UserPersonalWall.vue or post detail view
# Input: Post ID, Last seen ID for pagination
# Output: Possible return codes [200 - Retrieval success, 404 - No comments, 500 - An error occurred]
@blueprint.route('/getWallPostComments/<postID>/<last_seen_id>', methods=['GET'])
def getWallPostComments(postID, last_seen_id):
    users_retrieved_list = {}
    
    try:
        with db_manager.get_cursor() as cursor:
            # Check if post exists
            cursor.execute('SELECT * FROM "userWallPosts" WHERE id = %s', (postID,))
            post = cursor.fetchone()
            
            if not post:
                return jsonify({
                    'error': 'No such post exists'
                }), 404
            
            limit = 20
            
            # Get comments
            if last_seen_id == '0':
                cursor.execute(
                    '''SELECT * FROM "userWallPostComments" 
                       WHERE "postID" = %s 
                       ORDER BY "commentDate" DESC LIMIT %s''',
                    (postID, limit,)
                )
            else:
                cursor.execute(
                    '''SELECT * FROM "userWallPostComments" 
                       WHERE "postID" = %s AND id < %s 
                       ORDER BY "commentDate" DESC LIMIT %s''',
                    (postID, last_seen_id, limit,)
                )
            
            comments = cursor.fetchall()
            
            if not comments:
                return jsonify({
                    'data': []
                }), 200
            
            # Add commenter info to each comment
            for comment in comments:
                commenter_id = comment['commenterID']
                
                if commenter_id not in users_retrieved_list:
                    commenter_info = getUserInfoByID(cursor, commenter_id)
                    if commenter_info:
                        users_retrieved_list[commenter_id] = commenter_info
                        comment['commenterInfo'] = commenter_info
                else:
                    comment['commenterInfo'] = users_retrieved_list[commenter_id]
            
            return jsonify({
                'data': comments
            }), 200
    
    except Exception as e:
        print(str(e))
        return jsonify({
            "code": 500,
            "message": "An error occurred retrieving the comments."
        }), 500


# -----------------------------------------------------------------------------------------
# [POST] addWallPost
# Purpose: Add a new post to a user's wall
# Used: UserPersonalWall.vue [views folder inside Users folder]
# Input:
#   1. Wall Owner ID (whose wall this is)
#   2. Poster User ID (who is making the post)
#   3. Post Content
#   4. Post Photos (optional)
#   5. Tagged Users (optional) - array of user IDs
#   6. Location (optional) - venue ID
# Output: Possible return codes [201 - Post added successfully, 400 - Missing required data, 500 - An error occurred]
@blueprint.route('/addWallPost', methods=['POST'])
def addWallPost():
    try:
        data = request.get_json()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Get all the required data
        wall_owner_id = data.get('wallOwnerID')
        poster_user_id = data.get('posterUserID')
        post_content = data.get('postContent')
        
        # Check if all the required data is provided
        if not wall_owner_id or not poster_user_id or not post_content:
            return jsonify({
                'code': 400,
                'message': 'Missing required data'
            }), 400
        
        # Step 1: Get today's date
        post_date = datetime.now()
        
        # List to store the image urls
        image_urls = []
        
        # Step 2: Check if the post has images
        if 'images' in data and data['images']:
            # Loop through the images and upload them to S3
            for image in data['images']:
                if not image:
                    continue
                
                base64_string = re.sub(r'^data:image\/[a-zA-Z]+;base64,', '', image)
                image64 = s3Images.uploadBase64ImageToS3(base64_string)
                image_urls.append(image64)
            
            # Make the postPhotos as a text string starting with { and ending with }
            post_photos = '{' + ','.join(f'"{url}"' for url in image_urls) + '}'
        else:
            post_photos = '{}'
        
        # Get optional fields
        tagged_users = data.get('taggedUsers', [])
        location = data.get('location')
        
        with db_manager.get_cursor() as cursor:
            # Check if wall owner exists
            cursor.execute('SELECT id FROM "users" WHERE id = %s', (wall_owner_id,))
            if not cursor.fetchone():
                return jsonify({
                    'code': 404,
                    'message': 'Wall owner does not exist'
                }), 404
            
            # Check if poster exists
            cursor.execute('SELECT id FROM "users" WHERE id = %s', (poster_user_id,))
            if not cursor.fetchone():
                return jsonify({
                    'code': 404,
                    'message': 'Poster user does not exist'
                }), 404
            
            # Step 3: Insert the new post into the database
            cursor.execute(
                '''INSERT INTO "userWallPosts" 
                   ("wallOwnerID", "posterUserID", "postDate", "postContent", "postPhotos", "taggedUsers", "location") 
                   VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id''',
                (wall_owner_id, poster_user_id, post_date, post_content, post_photos, tagged_users, location)
            )
            post_id = cursor.fetchone()['id']
            
            # Award points for posting (only for regular users)
            points_earned = 0
            badge_result = None
            
            # Check if user has reached maximum proof points
            if not pointsHelperFunc.check_max_proof_points(poster_user_id):
                # Award points for the post (using rule id 7 for club posts, adjust if needed)
                cursor.execute('SELECT "proofPoints" FROM "pointSystemRules" WHERE id = %s', (7,))
                points_rule = cursor.fetchone()
                
                if points_rule:
                    points_earned = points_rule['proofPoints']
                    
                    # Update user's points
                    cursor.execute(
                        'UPDATE "pointsRecorder" SET "currentPoints" = "currentPoints" + %s WHERE "userID" = %s AND "userType" = %s',
                        (points_earned, poster_user_id, 'user')
                    )
                    
                    print(f"Added {points_earned} points to user {poster_user_id} for adding a wall post")
            
            # Send notification to wall owner if poster is different from wall owner
            if wall_owner_id != poster_user_id:
                # Get poster's username
                cursor.execute('SELECT username, "displayName" FROM "users" WHERE id = %s', (poster_user_id,))
                poster_info = cursor.fetchone()
                poster_name = poster_info['displayName'] if poster_info else 'Someone'
                
                # Get wall owner's username for the link
                cursor.execute('SELECT username FROM "users" WHERE id = %s', (wall_owner_id,))
                wall_owner_info = cursor.fetchone()
                wall_owner_username = wall_owner_info['username'] if wall_owner_info else ''
                
                notification_data = {
                    "userId": wall_owner_id,
                    "userType": "user",
                    "notiTabs": "forYou",
                    "notiType": "wall_post",
                    "image": None,
                    "link": f"/profile/user/{wall_owner_id}/{wall_owner_username}/all-wall-posts",
                    "message": f"{poster_name} posted on your wall",
                    "createdAt": current_time
                }
                notifications.add_notification_to_db(notification_data)
            
            # Send notifications to tagged users
            if tagged_users:
                cursor.execute('SELECT username, "displayName" FROM "users" WHERE id = %s', (poster_user_id,))
                poster_info = cursor.fetchone()
                poster_name = poster_info['displayName'] if poster_info else 'Someone'
                
                for tagged_user_id in tagged_users:
                    if tagged_user_id != poster_user_id:  # Don't notify self
                        cursor.execute('SELECT username FROM "users" WHERE id = %s', (wall_owner_id,))
                        wall_owner_info = cursor.fetchone()
                        wall_owner_username = wall_owner_info['username'] if wall_owner_info else ''
                        
                        notification_data = {
                            "userId": tagged_user_id,
                            "userType": "user",
                            "notiTabs": "forYou",
                            "notiType": "wall_post_tag",
                            "image": None,
                            "link": f"/profile/user/{wall_owner_id}/{wall_owner_username}/all-wall-posts",
                            "message": f"{poster_name} tagged you in a wall post",
                            "createdAt": current_time
                        }
                        notifications.add_notification_to_db(notification_data)
        
        # Prepare the response
        response_data = {
            'code': 201,
            'message': 'Post added successfully',
            'postID': post_id
        }
        
        if points_earned > 0:
            response_data['pointsEarned'] = points_earned
        
        if badge_result:
            response_data['badgeAwarded'] = badge_result
        
        return jsonify(response_data), 201
    
    except Exception as e:
        print(f"Error adding wall post: {str(e)}")
        return jsonify({
            "code": 500,
            "message": "An error occurred adding the post."
        }), 500


# -----------------------------------------------------------------------------------------
# [POST] addWallPostComment
# Purpose: Add a comment to a wall post
# Used: UserPersonalWall.vue
# Input:
#   1. Commenter ID (user ID)
#   2. Post ID
#   3. Comment Content
# Output: Possible return codes [201 - Comment added successfully, 400 - Missing required data, 404 - Post not found, 500 - An error occurred]
@blueprint.route('/addWallPostComment', methods=['POST'])
def addWallPostComment():
    try:
        data = request.get_json()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Get all the required data
        commenter_id = data.get('commenterID')
        post_id = data.get('postID')
        comment_content = data.get('commentContent')
        
        # Check if all the required data is provided
        if not commenter_id or not post_id or not comment_content:
            return jsonify({
                'code': 400,
                'message': 'Missing required data'
            }), 400
        
        # Get today's date
        comment_date = datetime.now()
        
        with db_manager.get_cursor() as cursor:
            # Check if post exists
            cursor.execute('SELECT * FROM "userWallPosts" WHERE id = %s', (post_id,))
            post = cursor.fetchone()
            
            if not post:
                return jsonify({
                    'code': 404,
                    'message': 'No such post exists'
                }), 404
            
            # Insert the comment
            cursor.execute(
                '''INSERT INTO "userWallPostComments" 
                   ("postID", "commentDate", "commentContent", "commenterID") 
                   VALUES (%s, %s, %s, %s) RETURNING id''',
                (post_id, comment_date, comment_content, commenter_id)
            )
            comment_id = cursor.fetchone()['id']
            
            # Get commenter info
            commenter_info = getUserInfoByID(cursor, commenter_id)
            
            # Notify post owner if commenter is different
            poster_id = post['posterUserID']
            if poster_id != commenter_id:
                commenter_name = commenter_info['displayName'] if commenter_info else 'Someone'
                
                # Get wall owner info for the link
                wall_owner_id = post['wallOwnerID']
                cursor.execute('SELECT username FROM "users" WHERE id = %s', (wall_owner_id,))
                wall_owner_info = cursor.fetchone()
                wall_owner_username = wall_owner_info['username'] if wall_owner_info else ''
                
                notification_data = {
                    "userId": poster_id,
                    "userType": "user",
                    "notiTabs": "forYou",
                    "notiType": "wall_post_comment",
                    "image": None,
                    "link": f"/profile/user/{wall_owner_id}/{wall_owner_username}/all-wall-posts",
                    "message": f"{commenter_name} commented on your wall post",
                    "createdAt": current_time
                }
                notifications.add_notification_to_db(notification_data)
            
            # Award points for commenting
            points_earned = 0
            if not pointsHelperFunc.check_max_proof_points(commenter_id):
                cursor.execute('SELECT "proofPoints" FROM "pointSystemRules" WHERE id = %s', (10,))
                points_rule = cursor.fetchone()
                
                if points_rule:
                    points_earned = points_rule['proofPoints']
                    cursor.execute(
                        'UPDATE "pointsRecorder" SET "currentPoints" = "currentPoints" + %s WHERE "userID" = %s AND "userType" = %s',
                        (points_earned, commenter_id, 'user')
                    )
        
        # Prepare response
        response_data = {
            'code': 201,
            'message': 'Comment added successfully',
            'comment_obj': {
                "commentContent": comment_content,
                "commentDate": comment_date.isoformat(),
                "commenterID": commenter_id,
                "commenterInfo": commenter_info,
                "id": comment_id,
                "postID": post_id
            }
        }
        
        if points_earned > 0:
            response_data['pointsEarned'] = points_earned
        
        return jsonify(response_data), 201
    
    except Exception as e:
        print(f"Error adding comment: {str(e)}")
        return jsonify({
            "code": 500,
            "message": "An error occurred adding the comment."
        }), 500


# -----------------------------------------------------------------------------------------
# [PUT] likeUnlikeWallPost
# Purpose: Like or Unlike a wall post (toggle)
# Used: UserPersonalWall.vue
# Input:
#   1. User ID (who is liking)
#   2. Post ID
# Output: Possible return codes [200 - Post liked/unliked successfully, 400 - Missing required data, 404 - Post not found, 500 - An error occurred]
@blueprint.route('/likeUnlikeWallPost', methods=['PUT'])
def likeUnlikeWallPost():
    try:
        data = request.get_json()
        
        user_id = data.get('userID')
        post_id = data.get('postID')
        
        if not user_id or not post_id:
            return jsonify({
                'error': 'Missing required data'
            }), 400
        
        with db_manager.get_cursor() as cursor:
            # Check if post exists
            cursor.execute('SELECT * FROM "userWallPosts" WHERE id = %s', (post_id,))
            post = cursor.fetchone()
            
            if not post:
                return jsonify({
                    'error': 'No such post exists'
                }), 404
            
            # Check if user has already liked the post
            cursor.execute(
                'SELECT * FROM "userWallPostLikes" WHERE "userID" = %s AND "postID" = %s',
                (user_id, post_id,)
            )
            liked = cursor.fetchone()
            
            if liked:
                # Unlike the post
                cursor.execute(
                    'DELETE FROM "userWallPostLikes" WHERE "userID" = %s AND "postID" = %s',
                    (user_id, post_id,)
                )
                return jsonify({
                    'message': 'Post unliked successfully',
                    'liked': False
                }), 200
            
            # Like the post
            cursor.execute(
                'INSERT INTO "userWallPostLikes" ("userID", "postID") VALUES (%s, %s)',
                (user_id, post_id,)
            )
            
            # If user had disliked, remove the dislike
            cursor.execute(
                'DELETE FROM "userWallPostDislikes" WHERE "userID" = %s AND "postID" = %s',
                (user_id, post_id,)
            )
            
            return jsonify({
                'message': 'Post liked successfully',
                'liked': True
            }), 200
    
    except Exception as e:
        print(str(e))
        return jsonify({
            "code": 500,
            "message": "An error occurred liking the post."
        }), 500


# -----------------------------------------------------------------------------------------
# [PUT] dislikeUndislikeWallPost
# Purpose: Dislike or Un-dislike a wall post (toggle)
# Used: UserPersonalWall.vue
# Input:
#   1. User ID (who is disliking)
#   2. Post ID
# Output: Possible return codes [200 - Post disliked/un-disliked successfully, 400 - Missing required data, 404 - Post not found, 500 - An error occurred]
@blueprint.route('/dislikeUndislikeWallPost', methods=['PUT'])
def dislikeUndislikeWallPost():
    try:
        data = request.get_json()
        
        user_id = data.get('userID')
        post_id = data.get('postID')
        
        if not user_id or not post_id:
            return jsonify({
                'error': 'Missing required data'
            }), 400
        
        with db_manager.get_cursor() as cursor:
            # Check if post exists
            cursor.execute('SELECT * FROM "userWallPosts" WHERE id = %s', (post_id,))
            post = cursor.fetchone()
            
            if not post:
                return jsonify({
                    'error': 'No such post exists'
                }), 404
            
            # Check if user has already disliked the post
            cursor.execute(
                'SELECT * FROM "userWallPostDislikes" WHERE "userID" = %s AND "postID" = %s',
                (user_id, post_id,)
            )
            disliked = cursor.fetchone()
            
            if disliked:
                # Un-dislike the post
                cursor.execute(
                    'DELETE FROM "userWallPostDislikes" WHERE "userID" = %s AND "postID" = %s',
                    (user_id, post_id,)
                )
                return jsonify({
                    'message': 'Post un-disliked successfully',
                    'disliked': False
                }), 200
            
            # Dislike the post
            cursor.execute(
                'INSERT INTO "userWallPostDislikes" ("userID", "postID") VALUES (%s, %s)',
                (user_id, post_id,)
            )
            
            # If user had liked, remove the like
            cursor.execute(
                'DELETE FROM "userWallPostLikes" WHERE "userID" = %s AND "postID" = %s',
                (user_id, post_id,)
            )
            
            return jsonify({
                'message': 'Post disliked successfully',
                'disliked': True
            }), 200
    
    except Exception as e:
        print(str(e))
        return jsonify({
            "code": 500,
            "message": "An error occurred disliking the post."
        }), 500


# -----------------------------------------------------------------------------------------
# [PUT] editWallPost
# Purpose: Edit a wall post
# Used: UserPersonalWall.vue
# Input:
#   1. Post ID
#   2. Post Content
#   3. Editor ID (user who is editing - must be poster or wall owner)
#   4. Images (optional)
# Output: Possible return codes [200 - Post edited successfully, 400 - Missing required data, 403 - No permission, 404 - Post not found, 500 - An error occurred]
@blueprint.route('/editWallPost', methods=['PUT'])
def editWallPost():
    try:
        data = request.get_json()
        
        post_id = data.get('postID')
        post_content = data.get('postContent')
        editor_id = data.get('editorID')
        
        if not post_id or not post_content or not editor_id:
            return jsonify({
                'error': 'Missing required data'
            }), 400
        
        with db_manager.get_cursor() as cursor:
            # Check if post exists and get details
            cursor.execute('SELECT * FROM "userWallPosts" WHERE id = %s', (post_id,))
            post = cursor.fetchone()
            
            if not post:
                return jsonify({
                    'error': 'No such post exists'
                }), 404
            
            # Check if editor is the poster or wall owner
            if post['posterUserID'] != editor_id and post['wallOwnerID'] != editor_id:
                return jsonify({
                    'error': 'You do not have permission to edit this post'
                }), 403
            
            # Handle images
            image_urls = []
            
            # Check if post photo that is already in S3 is still in the post photos
            if 'postPhotos' in post and post['postPhotos'] and post['postPhotos'] != '{}':
                post_photos = post['postPhotos']
                images_to_keep = data.get('images', [])
                
                for url in post_photos:
                    if url not in images_to_keep:
                        # Delete the image from S3
                        s3Images.deleteImageFromS3(url)
            
            # Process images
            if 'images' in data and len(data['images']) > 0:
                for image in data['images']:
                    if not image:
                        continue
                    
                    # Check if the image is already in S3
                    if 's3' in image:
                        image_urls.append(image)
                    else:
                        base64_string = re.sub(r'^data:image\/[a-zA-Z]+;base64,', '', image)
                        image64 = s3Images.uploadBase64ImageToS3(base64_string)
                        image_urls.append(image64)
                
                post_photos = '{' + ','.join(f'"{url}"' for url in image_urls) + '}'
            else:
                post_photos = '{}'
            
            # Update the post
            cursor.execute(
                'UPDATE "userWallPosts" SET "postContent" = %s, "postPhotos" = %s WHERE id = %s',
                (post_content, post_photos, post_id,)
            )
            
            return jsonify({
                'message': 'Post edited successfully'
            }), 200
    
    except Exception as e:
        print(str(e))
        return jsonify({
            "code": 500,
            "message": "An error occurred editing the post."
        }), 500


# -----------------------------------------------------------------------------------------
# [PUT] editWallPostComment
# Purpose: Edit a comment on a wall post
# Used: UserPersonalWall.vue
# Input:
#   1. Comment ID
#   2. Comment Content
#   3. Editor ID (must be the commenter)
# Output: Possible return codes [200 - Comment edited successfully, 400 - Missing required data, 403 - No permission, 404 - Comment not found, 500 - An error occurred]
@blueprint.route('/editWallPostComment', methods=['PUT'])
def editWallPostComment():
    try:
        data = request.get_json()
        
        comment_id = data.get('commentID')
        comment_content = data.get('commentContent')
        editor_id = data.get('editorID')
        
        if not comment_id or not comment_content or not editor_id:
            return jsonify({
                'error': 'Missing required data'
            }), 400
        
        with db_manager.get_cursor() as cursor:
            # Check if comment exists
            cursor.execute('SELECT * FROM "userWallPostComments" WHERE id = %s', (comment_id,))
            comment = cursor.fetchone()
            
            if not comment:
                return jsonify({
                    'error': 'No such comment exists'
                }), 404
            
            # Check if editor is the commenter
            if comment['commenterID'] != editor_id:
                # Also check if editor is the wall owner (they can edit/delete comments on their wall)
                cursor.execute(
                    'SELECT "wallOwnerID" FROM "userWallPosts" WHERE id = %s',
                    (comment['postID'],)
                )
                post = cursor.fetchone()
                
                if not post or post['wallOwnerID'] != editor_id:
                    return jsonify({
                        'error': 'You do not have permission to edit this comment'
                    }), 403
            
            # Update the comment
            cursor.execute(
                'UPDATE "userWallPostComments" SET "commentContent" = %s WHERE id = %s',
                (comment_content, comment_id,)
            )
            
            return jsonify({
                'message': 'Comment edited successfully'
            }), 200
    
    except Exception as e:
        print(str(e))
        return jsonify({
            "code": 500,
            "message": "An error occurred editing the comment."
        }), 500


# -----------------------------------------------------------------------------------------
# [DELETE] removeWallPost
# Purpose: Remove a wall post
# Used: UserPersonalWall.vue
# Input:
#   1. Post ID
#   2. Remover ID (must be poster or wall owner)
# Output: Possible return codes [200 - Post removed successfully, 400 - Missing required data, 403 - No permission, 404 - Post not found, 500 - An error occurred]
@blueprint.route('/removeWallPost', methods=['DELETE'])
def removeWallPost():
    try:
        data = request.get_json()
        
        post_id = data.get('postID')
        remover_id = data.get('removerID')
        
        if not post_id or not remover_id:
            return jsonify({
                'error': 'Missing required data'
            }), 400
        
        with db_manager.get_cursor() as cursor:
            # Check if post exists
            cursor.execute('SELECT * FROM "userWallPosts" WHERE id = %s', (post_id,))
            post = cursor.fetchone()
            
            if not post:
                return jsonify({
                    'error': 'No such post exists'
                }), 404
            
            # Check if remover is the poster or wall owner
            if post['posterUserID'] != remover_id and post['wallOwnerID'] != remover_id:
                return jsonify({
                    'error': 'You do not have permission to remove this post'
                }), 403
            
            # Delete images from S3 if any
            if post.get('postPhotos') and post['postPhotos'] != '{}':
                for url in post['postPhotos']:
                    try:
                        s3Images.deleteImageFromS3(url)
                    except:
                        pass  # Continue even if image deletion fails
            
            # Delete all comments for the post
            cursor.execute('DELETE FROM "userWallPostComments" WHERE "postID" = %s', (post_id,))
            
            # Delete all likes for the post
            cursor.execute('DELETE FROM "userWallPostLikes" WHERE "postID" = %s', (post_id,))
            
            # Delete all dislikes for the post
            cursor.execute('DELETE FROM "userWallPostDislikes" WHERE "postID" = %s', (post_id,))
            
            # Delete the post
            cursor.execute('DELETE FROM "userWallPosts" WHERE id = %s', (post_id,))
            
            return jsonify({
                'message': 'Post removed successfully'
            }), 200
    
    except Exception as e:
        print(str(e))
        return jsonify({
            "code": 500,
            "message": "An error occurred removing the post."
        }), 500


# -----------------------------------------------------------------------------------------
# [DELETE] removeWallPostComment
# Purpose: Remove a comment from a wall post
# Used: UserPersonalWall.vue
# Input:
#   1. Comment ID
#   2. Remover ID (must be commenter or wall owner)
# Output: Possible return codes [200 - Comment removed successfully, 400 - Missing required data, 403 - No permission, 404 - Comment not found, 500 - An error occurred]
@blueprint.route('/removeWallPostComment', methods=['DELETE'])
def removeWallPostComment():
    try:
        data = request.get_json()
        
        comment_id = data.get('commentID')
        remover_id = data.get('removerID')
        
        if not comment_id or not remover_id:
            return jsonify({
                'error': 'Missing required data'
            }), 400
        
        with db_manager.get_cursor() as cursor:
            # Check if comment exists
            cursor.execute('SELECT * FROM "userWallPostComments" WHERE id = %s', (comment_id,))
            comment = cursor.fetchone()
            
            if not comment:
                return jsonify({
                    'error': 'No such comment exists'
                }), 404
            
            # Check if remover is the commenter
            is_commenter = comment['commenterID'] == remover_id
            
            # Check if remover is the wall owner
            cursor.execute(
                'SELECT "wallOwnerID" FROM "userWallPosts" WHERE id = %s',
                (comment['postID'],)
            )
            post = cursor.fetchone()
            is_wall_owner = post and post['wallOwnerID'] == remover_id
            
            if not is_commenter and not is_wall_owner:
                return jsonify({
                    'error': 'You do not have permission to remove this comment'
                }), 403
            
            # Delete the comment
            cursor.execute('DELETE FROM "userWallPostComments" WHERE id = %s', (comment_id,))
            
            return jsonify({
                'message': 'Comment removed successfully'
            }), 200
    
    except Exception as e:
        print(str(e))
        return jsonify({
            "code": 500,
            "message": "An error occurred removing the comment."
        }), 500
