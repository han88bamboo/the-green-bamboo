# Routes: /getClubs (GET), /getClubPosts (GET), /getClubPostDetails (GET), 
#         /getUserLikesPost (GET), /getUserLikesComments (GET)
#         /createClubs (POST), /addPost (POST), /addComment (POST), 
#         /addClubMembers (PUT), /editPost (PUT), /editComment (PUT)
#         /likePost (PUT), /likeComment (PUT)
# -----------------------------------------------------------------------------------------

import os
import json
from flask import Blueprint, g, jsonify, request
import datetime

# Use to upload image to S3
import s3Images

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

# -----------------------------------------------------------------------------------------
# [GET] getClubs
# Purpose: Get 20 clubs information each time this is called. 
# Used: ClubSearchPage.vue [views folder]
@blueprint.route('/getClubs/<id>', methods=['GET']) # id is the starting ID to retrieve from (inclusive)
def getClubs(id):
    conn = g.db
    cur = conn.cursor()
    return_data = {}

    try:

        # Step 1: Get the 20 clubs
        # ID: Used to define the starting ID to retrieve from
        cur.execute('SELECT * FROM "clubs" WHERE id >= %s ORDER BY id ASC LIMIT 20', (id,))
        clubs_info = cur.fetchall()

        if not clubs_info:
            return jsonify({
                'error': 'No clubs found in database'
            }), 404
        
        # Step 2: Get the total number of members in each of the 20 clubs 
        for club in clubs_info:
            club_id = club['id']
            # Get the total number of members in each club
            cur.execute('SELECT COUNT(*) AS "totalMembers" FROM "clubMembers" WHERE "clubID" = %s AND "joinStatus" = TRUE', (club_id,))
            num_members = cur.fetchone()
            # Add club summary into return data
            club['totalMembers'] = num_members['totalMembers']
            return_data[club_id] = club


        return jsonify({
            'clubs_info': clubs_info
        }), 200

    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred retrieving the request."
            }
        ), 500
    
    finally:
        cur.close()


# -----------------------------------------------------------------------------------------
# [GET] getClubPosts
# Purpose: Get the latest 10 posts in the club. 
# Used: ClubPost.vue [components folder]
@blueprint.route('/getClubPosts/<clubID>/<offset>', methods=['GET']) # offset is the number of records to skip before fetching the next set of records
def getClubPosts(clubID, offset):
    conn = g.db
    cur = conn.cursor()

    # list to track if user information has been retrieved (reason being, a single user can post multiple post, this may help to reduce data being sent over to the frontend)
    users_retrieved_list = []

    # filtered post list to be returned (for event where posterID is null - to exclude posts with no poster)
    filtered_post_list = []

    try:

        # check if club exists
        cur.execute('SELECT * FROM "clubs" WHERE id = %s', (clubID,))
        club = cur.fetchone()

        if not club:
            return jsonify({
                'error': f'No such club exist for club id: {clubID}'
            })

        # Step 1: Get the top 10 latest post in that club
        cur.execute('SELECT * FROM "clubPosts" WHERE "clubID" = %s ORDER BY "postDate" DESC LIMIT 10 OFFSET %s', (clubID, offset,))
        post_info = cur.fetchall() # returns empty list if no result found

        if not post_info:
            return jsonify({
                'error': 'No post yet'
            }), 404
        
        # Step 2: Get the number of likes for each post and the poster's id, displayName, photo
        for post in post_info:
            posterID = post['posterID']
            postID = post['id']

            # Check if posterID is null
            if not posterID:
                # Move to the next post if the posterID is null
                continue

            if posterID not in users_retrieved_list:
                cur.execute('SELECT "id", "displayName", "photo" FROM "users" WHERE id = %s', (posterID,))
                poster_info = cur.fetchone()
                users_retrieved_list.append(posterID)
            
            # Add poster info into post
            post['posterInfo'] = poster_info

            cur.execute('SELECT COUNT(*) AS "totalLikes" FROM "clubPostsLikes" WHERE "postID" = %s', (postID,))
            total_likes = cur.fetchone()

            # Add total likes into post
            post['totalLikes'] = total_likes['totalLikes']

            # Add post into filtered_post_list
            filtered_post_list.append(post)

        return jsonify({
            'data': filtered_post_list
        }), 200

    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred retrieving the request."
            }
        ), 500

    finally:
        cur.close()


# -----------------------------------------------------------------------------------------
# [GET] getClubPostDetails
# Purpose: Get the latest 20 comments for a specific post
# Used: SpecificClubPost.vue [components folder]
@blueprint.route('/getClubPostDetails/<postID>/<offset>', methods=['GET']) # offset is the number of records to skip before fetching the next set of records
def getClubPostDetails(postID, offset):
    conn = g.db
    cur = conn.cursor()

    # list to track if user information has been retrieved (reason being, a single user can post multiple post, this may help to reduce data being sent over to the frontend)
    users_retrieved_list = []

    # filtered comment list to be returned (for event where commenterID is null - to exclude comments with no commenter)
    filtered_comment_list = []

    try:
        # check if post exist
        cur.execute('SELECT * FROM "clubPostComments" WHERE "postID" = %s', (postID,))
        post = cur.fetchone()

        if not post:
            return jsonify({
                'error': f"No such post for this post id {postID}"
            }), 404

        # Step 1: Get the latest 20 comments for the specific post
        cur.execute('SELECT * FROM "clubPostComments" WHERE "postID" = %s ORDER BY "commentDate" DESC LIMIT 20 OFFSET %s', (postID, offset,))
        comments_info = cur.fetchall()

        if not comments_info:
            return jsonify({
                'error': 'No comments for this post yet'
            }), 404
        
        # Step 2: Get the total likes, commenter's id, displayName and photo
        for comment in comments_info:
            commenterID = comment['commenterID']

            # Check if commenterID is null
            if not commenterID:
                # Skip to the next comment if commenterID is null
                continue

            if commenterID not in users_retrieved_list:
                cur.execute('SELECT "id", "displayName", "photo" FROM "users" WHERE id = %s', (commenterID,))
                commenter_info = cur.fetchone()
                users_retrieved_list.append(commenterID)

            # Add commenter info into comment
            comment['commenterInfo'] = commenter_info

            cur.execute('SELECT COUNT(*) AS "totalLikes" FROM "clubPostCommentsLikes" WHERE "commentID" = %s', (comment['id'],))
            total_likes = cur.fetchone()

            # Add total likes into comment
            comment['totalLikes'] = total_likes['totalLikes']

            # Add comment into filtered_comment_list
            filtered_comment_list.append(comment)

        return jsonify({
            'data': comments_info
        }), 200


    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred retrieving the request."
            }
        ), 500
    
    finally:
        cur.close()


# -----------------------------------------------------------------------------------------
# [GET] getUserLikesPost
# Purpose: Get the posts that a specific user has liked in a specific club
# Used: ClubPost.vue [components folder]
@blueprint.route('/getUserLikesPost/<userID>/<clubID>', methods=['GET'])
def getUserLikesPost(userID, clubID):
    conn = g.db
    cur = conn.cursor()

    try: 
        cur.execute('SELECT "postID" FROM "clubPostsLikes" WHERE "userID" = %s AND "clubID" = %s' , (userID, clubID,))
        liked_posts = cur.fetchall()

        if not liked_posts:
            return jsonify({
                'error': 'No liked posts found'
            }), 404
    
        return jsonify({
            'liked_posts': liked_posts
        }), 200

    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred retrieving the request."
            }
        ), 500
    
    finally:
        cur.close()


# -----------------------------------------------------------------------------------------
# [GET] getUserLikesComments
# Purpose: Get the comments that a specific user has liked in a specific post
# Used: SpecificClubPost.vue [components folder]
@blueprint.route('/getUserLikesComments/<userID>/<postID>', methods=['GET'])
def getUserLikesComments(userID, postID):
    conn = g.db
    cur = conn.cursor()

    try:
        cur.execute('SELECT "commentID" FROM "clubPostCommentsLikes" WHERE "userID" = %s AND "postID" = %s', (userID, postID,))
        liked_comments = cur.fetchall()

        if not liked_comments:
            return jsonify({
                'error': 'No liked comments found'
            }), 404

        return jsonify({
            'liked_comments': liked_comments
        }), 200

    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred retrieving the request."
            }
        ), 500
    
    finally:
        cur.close()


# -----------------------------------------------------------------------------------------
# [POST] createClubs
# Purpose: Create a new club
# Used: CreateClub.vue [views folder]
@blueprint.route('/createClubs', methods=['POST'])
def createClub():
    conn = g.db
    cur = conn.cursor()

    try:
        data = request.get_json()

        # Get all the required data
        creator_id = data['creatorID']
        club_name = data['clubName']
        club_desc = data['clubDesc']
        is_invite_only = data['isInviteOnly']
        
        # Step 1: Get today's date
        date_created = datetime.now()

        # Step 2: Check if the banner image is provided
        if 'image64' in data:
            image64 = s3Images.uploadBase64ImageToS3(data['image64'])
        else:
            image64 = None

        # Step 3: Insert the new club into the database
        cur.execute('INSERT INTO "clubs" ("clubName", "clubDesc", "isInviteOnly", "clubLink", "clubBanner", "dateCreated") VALUES (%s, %s, %s, %s, %s, %s) RETURNING id', 
                    (club_name, club_desc, is_invite_only, '', image64, date_created,))
        club_id = cur.fetchone()['id']

        # Step 4: Insert the club admin into the clubMembers table
        cur.execute('INSERT INTO "clubMembers" ("clubID", "memberID", "joinDate", "isAdmin", "joinStatus") VALUES (%s, %s, %s, TRUE, TRUE)', 
                    (club_id, creator_id, date_created,))
        conn.commit()

        return jsonify({
            'message': 'Club created successfully',
            'clubID': club_id
        }), 201

    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the club."
            }
        ), 500
    
    finally:
        cur.close()


# -----------------------------------------------------------------------------------------
# [POST] addPost
# Purpose: Add a new post to the club
# Used: SpecificClubPost.vue [components folder]
@blueprint.route('/addPost', methods=['POST'])
def addPost():
    conn = g.db
    cur = conn.cursor()

    try:
        data = request.get_json()

        # Get all the required data
        poster_id = data['posterID']
        club_id = data['clubID']
        post_content = data['postContent']

        # Step 1: Get today's date
        post_date = datetime.now()

        # Step 2: Check if the post has an image
        if 'image64' in data:
            image64 = s3Images.uploadBase64ImageToS3(data['image64'])
        else:
            image64 = None

        # Step 3: Insert the new post into the database
        cur.execute('INSERT INTO "clubPosts" ("clubID", "postDate", "postContent", "postPhoto", "posterID") VALUES (%s, %s, %s, %s, %s) RETURNING id', 
                    (club_id, post_date, post_content, image64, poster_id,))
        post_id = cur.fetchone()['id']
        conn.commit()

        return jsonify({
            'message': 'Post added successfully',
            'postID': post_id
        }), 201

    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred adding the post."
            }
        ), 500
    
    finally:
        cur.close()


# -----------------------------------------------------------------------------------------
# [POST] addComment
# Purpose: Add a new comment to the post
# Used: SpecificClubPost.vue [components folder]
@blueprint.route('/addComment', methods=['POST'])
def addComment():
    conn = g.db
    cur = conn.cursor()

    try:
        data = request.get_json()

        # Get all the required data
        commenter_id = data['commenterID']
        post_id = data['postID']
        comment_content = data['commentContent']

        # Step 1: Get today's date
        comment_date = datetime.now()

        # Step 2: Insert the new comment into the database
        cur.execute('INSERT INTO "clubPostComments" ("postID", "commentDate", "commentContent", "commenterID") VALUES (%s, %s, %s, %s) RETURNING id', 
                    (post_id, comment_date, comment_content, commenter_id,))
        comment_id = cur.fetchone()['id']
        conn.commit()

        return jsonify({
            'message': 'Comment added successfully',
            'commentID': comment_id
        }), 201

    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred adding the comment."
            }
        ), 500
    
    finally:
        cur.close()

