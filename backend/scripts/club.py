# Routes: /getClubs (GET), /getClubwSearch (GET), /getSpecificClubInfo (GET),
#         /getClubPosts (GET), /getClubPostDetails (GET), /checkUserMembership (GET),
#         /getUserLikesPost (GET), /getUserLikesComments (GET), /getUserClubs (GET),
#         /createClubs (POST), /addClubMembers (POST), /joinClub (POST), 
#         /addPost (POST), /addComment (POST), 
#         /acceptClubInvite (PUT), /editPost (PUT), /editComment (PUT)
#         /likeUnlikePost (PUT), /likeUnlikeComment (PUT), /makeAdmin (PUT), 
#         /updateClubInfo (PUT),
#         /removeMembers (DELETE), /removePost (DELETE), /removeComment (DELETE),
#         /leaveClub (DELETE), /deleteClub (DELETE)
# -----------------------------------------------------------------------------------------

import os
from flask import Blueprint, g, jsonify, request
from datetime import datetime

# Use to upload image to S3
import s3Images

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

# Helper function to retrieve the user's id and user type
def getUserInfo(cur, member_id):
    
    # Get the user's id and user type from the clubMembers table
    cur.execute('SELECT "userID", "userType" FROM "clubMembers" WHERE id = %s', (member_id,))
    member_info = cur.fetchone()

    # Check the user type and get the user information
    # For type = user:  "id", "displayName", "photo"
    # For type = producer: "id", "producerName", "photo"
    # For type = venue: "id", "venueName", "photo"

    if member_info['userType'] == 'user':
        cur.execute('SELECT "id", "displayName", "photo" FROM "users" WHERE id = %s', (member_info['userID'],))
        user_info = cur.fetchone()
    elif member_info['userType'] == 'producer':
        cur.execute('SELECT "id", "producerName", "photo" FROM "producers" WHERE id = %s', (member_info['userID'],))
        user_info = cur.fetchone()
    else:
        cur.execute('SELECT "id", "venueName", "photo" FROM "venues" WHERE id = %s', (member_info['userID'],))
        user_info = cur.fetchone()

    # Check if the user exist
    if not user_info:
        return None

    # Add the user type into the user_info
    user_info['userType'] = member_info['userType']

    return user_info

# -----------------------------------------------------------------------------------------
# [GET] getClubs
# Purpose: Get 20 clubs information each time this is called. 
# Used: BrowseClubs.vue [views folder inside Users folder]
# Output: Possible return codes [200 - Retreival success, 404 - No clubs found in database, 500 - An error occurred retrieving the request]
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
# [GET] getClubwSearch
# Purpose: Get 20 clubs information each time this is called. This is used when the user is searching for a specific club using the search bar.
# Used: BrowseClubs.vue [views folder inside Users folder]
# Output: Possible return codes [200 - Retreival success, 404 - No clubs found in database, 500 - An error occurred retrieving the request]
@blueprint.route('/getClubwSearch/<id>/<search>', methods=['GET']) # id is the starting ID to retrieve from (inclusive)
def getClubwSearch(id, search):
    conn = g.db
    cur = conn.cursor()
    return_data = {}

    try:

        # Step 1: Get the 20 clubs
        # ID: Used to define the starting ID to retrieve from
        cur.execute('SELECT * FROM "clubs" WHERE "clubName" ILIKE %s ORDER BY id ASC LIMIT 20 OFFSET %s', (f'%{search}%', id,))
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
# [GET] getSpecificClubInfo
# Purpose: Get the information of a specific club
# Used: ClubView.vue [views folder inside Users folder]
# Output: Possible return codes [200 - Retreival success, 404 - No such club found in database, 500 - An error occurred retrieving the request]
@blueprint.route('/getSpecificClubInfo/<clubID>', methods=['GET'])
def getSpecificClubInfo(clubID):
    conn = g.db
    cur = conn.cursor()

    try:
        # Step 1: Get the club information
        cur.execute('SELECT * FROM "clubs" WHERE id = %s', (clubID,))
        club_info = cur.fetchone()

        if not club_info:
            return jsonify({
                'error': f'No such club found for club id: {clubID}'
            }), 404
        
        # Step 2: Get the total number of members in the club
        cur.execute('SELECT COUNT(*) AS "totalMembers" FROM "clubMembers" WHERE "clubID" = %s AND "joinStatus" = TRUE', (clubID,))
        num_members = cur.fetchone()
        club_info['totalMembers'] = num_members['totalMembers']

        return jsonify({
            'club_info': club_info
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
# Used: ClubView.vue [views folder inside Users folder]
# Input: 
#   1. Club ID, 
#   2. Offset (number of records to skip before fetching the next set of records) [initially set to 0, then increment by 10 on the frontend]
# Output: Possible return codes [200 - Retreival success, 404 - No post/club found in database, 500 - An error occurred retrieving the request]
@blueprint.route('/getClubPosts/<clubID>/<offset>', methods=['GET']) # offset is the number of records to skip before fetching the next set of records
def getClubPosts(clubID, offset):
    conn = g.db
    cur = conn.cursor()

    # Dictionary to track if user information has been retrieved (reason being, a single user can post multiple post, this may help to reduce data being sent over to the frontend)
    users_retrieved_list = {}

    # filtered post list to be returned (for event where posterID is null - to exclude posts with no poster)
    filtered_post_list = []

    try:

        # check if club exists
        cur.execute('SELECT * FROM "clubs" WHERE id = %s', (clubID,))
        club = cur.fetchone()

        if not club:
            return jsonify({
                'error': f'No such club exist for club id: {clubID}'
            }), 404

        # Step 1: Get the top 10 latest post in that club
        cur.execute('SELECT * FROM "clubPosts" WHERE "clubID" = %s ORDER BY "postDate" DESC LIMIT 10 OFFSET %s', (clubID, offset,))
        post_info = cur.fetchall() # returns empty list if no result found

        if not post_info:
            return jsonify({
                'error': 'No post yet'
            }), 404
        
        # Step 2: Get the number of likes and number of comments for each post and the poster's id, displayName, photo
        for post in post_info:
            posterID = post['posterID'] # This is the club member's ID
            postID = post['id']

            # Check if posterID is null
            if not posterID:
                # Move to the next post if the posterID is null
                continue

            # Get the poster's user ID and user type from the clubMembers table
            if posterID not in users_retrieved_list:
                poster_info = getUserInfo(cur, posterID)

                if not poster_info:
                    # Skip to the next post if the poster info is not found
                    continue

                users_retrieved_list[posterID] = poster_info
                # Add poster info into post
                post['posterInfo'] = poster_info
            else:
                post['posterInfo'] = users_retrieved_list[posterID]

            # Get the total number of likes for each post
            cur.execute('SELECT COUNT(*) AS "totalLikes" FROM "clubPostsLikes" WHERE "postID" = %s', (postID,))
            total_likes = cur.fetchone()

            # Add total likes into post
            post['totalLikes'] = total_likes['totalLikes']

            # Get the total number of comments for each post
            cur.execute('SELECT COUNT(*) AS "totalComments" FROM "clubPostComments" WHERE "postID" = %s', (postID,))
            total_comments = cur.fetchone()

            # Add total comments into post
            post['totalComments'] = total_comments['totalComments']

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

    # Dictionary to track if user information has been retrieved (reason being, a single user can post multiple post, this may help to reduce data being sent over to the frontend)
    users_retrieved_list = {}

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

            # Get the commenter's user ID and user type from the clubMembers table
            if commenterID not in users_retrieved_list:
                commenter_info = getUserInfo(cur, commenterID)

                if not commenter_info:
                    # Skip to the next comment if the commenter info is not found
                    continue

                users_retrieved_list[commenterID] = commenter_info
                # Add commenter info into comment
                comment['commenterInfo'] = commenter_info
            else:
                comment['commenterInfo'] = users_retrieved_list[commenterID]

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
# [GET] checkUserMembership
# Purpose: Check if a user is a member of a specific club
# Used: ClubView.vue [views folder inside Users folder]
# Output: Possible return codes [200 - User is a member, 404 - User is not a member, 500 - An error occurred retrieving the request]
@blueprint.route('/checkUserMembership/<userID>/<userType>/<clubID>', methods=['GET'])
def checkUserMembership(userID, userType, clubID):
    conn = g.db
    cur = conn.cursor()

    try:
        cur.execute('SELECT * FROM "clubMembers" WHERE "clubID" = %s AND "userID" = %s AND "userType" = %s AND "joinStatus" = TRUE', (clubID, userID, userType,))
        member = cur.fetchone()

        if not member:
            return jsonify({
                'error': 'User is not a member'
            }), 404
        
        return jsonify({
            'isMember': member.get('joinStatus'),
            'isAdmin': member.get('isAdmin'),
            'memberID': member.get('id')
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
# Used: ClubView.vue [views folder inside Users folder]
# Output: Possible return codes [200 - Retreival success, 404 - No liked posts found, 500 - An error occurred retrieving the request]
@blueprint.route('/getUserLikesPost/<memberID>/<clubID>', methods=['GET'])
def getUserLikesPost(memberID, clubID):
    conn = g.db
    cur = conn.cursor()

    try: 
        cur.execute('SELECT "postID" FROM "clubPostsLikes" WHERE "memberID" = %s AND "clubID" = %s' , (memberID, clubID,))
        liked_posts = cur.fetchall()

        if not liked_posts:
            return jsonify({
                'error': 'No liked posts found'
            }), 404
        
        # Format the liked_posts into a list of postID
        liked_posts = [post['postID'] for post in liked_posts]
    
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
# Output: Possible return codes [200 - Retreival success, 404 - No liked comments found, 500 - An error occurred retrieving the request]
@blueprint.route('/getUserLikesComments/<memberID>/<postID>', methods=['GET'])
def getUserLikesComments(memberID, postID):
    conn = g.db
    cur = conn.cursor()

    try:
        cur.execute('SELECT "commentID" FROM "clubPostCommentsLikes" WHERE "memberID" = %s AND "postID" = %s', (memberID, postID,))
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
# [GET] getUserClubs
# Purpose: Get the clubs that a specific user is a member of
# Used: BrowseClubs.vue [views folder inside Users folder]
# Output: Possible return codes [200 - Retreival success, 404 - No clubs found, 500 - An error occurred retrieving the request]
@blueprint.route('/getUserClubs/<userID>/<userType>', methods=['GET'])
def getUserClubs(userID, userType):
    conn = g.db
    cur = conn.cursor()

    try:
        cur.execute('SELECT "clubID" FROM "clubMembers" WHERE "userID" = %s AND "userType" = %s AND "joinStatus" = TRUE', (userID, userType,))
        user_clubs = cur.fetchall()

        if not user_clubs:
            return jsonify({
                'error': 'No clubs found'
            }), 404
        
        # Format the user_clubs into a list of clubID
        user_clubs = [club['clubID'] for club in user_clubs]

        return jsonify({
            'user_clubs': user_clubs
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
# Used: CreateClub.vue [views folder inside Users folder]
# Input:
#   1. Creator ID (i.e., the user's ID in the 'users', 'producers' or 'venues' table)
#   2. Creator Type
#   3. Club Name
#   4. Club Description
#   5. Is Invite Only (boolean: True = Private, False = Public)
# Output: Possible return codes [201 - Club created successfully, 500 - An error occurred creating the club]
@blueprint.route('/createClubs', methods=['POST'])
def createClub():
    conn = g.db
    cur = conn.cursor()

    try:
        data = request.get_json()

        # Get all the required data
        creator_id = data['creatorID']
        creator_type = data['creatorType']
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
        cur.execute('INSERT INTO "clubMembers" ("clubID", "userID", "userType", "joinDate", "isAdmin", "joinStatus") VALUES (%s, %s, %s, %s, TRUE, TRUE)', 
                    (club_id, creator_id, creator_type, date_created,))
        conn.commit()

        return jsonify({
            'message': 'Club created successfully',
            'clubID': club_id
        }), 201

    except Exception as e:
        print(str(e))
        # Rollback the transaction if an error occurred
        conn.rollback()
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the club."
            }
        ), 500
    
    finally:
        cur.close()


# -----------------------------------------------------------------------------------------
# [POST] addClubMembers
# Purpose: Add new members to the club
# Used: 
# Input: 
#   1. A list of new member objects containing the user's ID, user type and isAdmin status (e.g., [{'userID': 1, 'userType': 'user', 'isAdmin': true}, {'userID': 2, 'userType': 'producer', isAdmin: false}])
#   2. Club ID
# Output: Possible return codes [201 - New member added successfully, 404 - No such club exist, 500 - An error occurred adding the new member]
@blueprint.route('/addClubMembers', methods=['POST'])
def addClubMembers():
    conn = g.db
    cur = conn.cursor()

    try:
        data = request.get_json()

        # Get all the required data
        club_id = data['clubID']

        # List of members to be added to the club
        new_members_list = data['new_members']

        join_date = datetime.now()

        # Step 1: Check if the club exist
        cur.execute('SELECT * FROM "clubs" WHERE id = %s', (club_id,))
        club = cur.fetchone()

        if not club:
            return jsonify({
                'error': 'No such club exist'
            }), 404

        # Step 2: Insert the new member into the clubMembers table
        for user in new_members_list:
            user_id = user['userID']
            is_admin = user['isAdmin']
            user_type = user['userType']

            # Check if the user exist
            if user_type == 'user':
                cur.execute('SELECT * FROM "users" WHERE id = %s', (user_id,))
                user = cur.fetchone()
            elif user_type == 'producer':
                cur.execute('SELECT * FROM "producers" WHERE id = %s', (user_id,))
                user = cur.fetchone()
            else:
                cur.execute('SELECT * FROM "venues" WHERE id = %s', (user_id,))
                user = cur.fetchone()
            
            # Skip to the next member if the user does not exist
            if not user:
                continue

            cur.execute('INSERT INTO "clubMembers" ("clubID", "userID", "userType", "joinDate", "isAdmin", "joinStatus") VALUES (%s, %s, %s, %s, FALSE)', (club_id, user_id, user_type, join_date, is_admin,))
            conn.commit()

        return jsonify({
            'message': 'New member added to the club'
        }), 201

    except Exception as e:
        print(str(e))
        # Rollback the transaction if an error occurred
        conn.rollback()
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred adding the new member."
            }
        ), 500
    
    finally:
        cur.close()


# -----------------------------------------------------------------------------------------
# [POST] joinClub
# Purpose: Join a club (not through invite and only for public clubs)
# Used: 
#   1. ClubView.vue [views folder inside Users folder]
#   2. BrowseClubs.vue [views folder inside Users folder]
# Input:
#   1. Club ID
#   2. User ID (i.e., the user's ID in the 'users', 'producers' or 'venues' table)
#   3. User Type
# Output: Possible return codes [201 - User joined the club successfully, 404 - No such club exist, 409 - User is already a member, 500 - An error occurred joining the club]
@blueprint.route('/joinClub', methods=['POST'])
def joinClub():
    conn = g.db
    cur = conn.cursor()

    try:
        data = request.get_json()

        # Get all the required data
        club_id = data['clubID']
        user_id = data['userID']
        user_type = data['userType']

        # Step 1: Check if the club exist
        cur.execute('SELECT * FROM "clubs" WHERE id = %s', (club_id,))
        club = cur.fetchone()

        if not club:
            return jsonify({
                'error': 'No such club exist'
            }), 404
        
        # Step 2: Check if the user is already a member of the club
        cur.execute('SELECT * FROM "clubMembers" WHERE "clubID" = %s AND "userID" = %s AND "userType" = %s', (club_id, user_id, user_type,))
        member = cur.fetchone()

        if member:
            return jsonify({
                'error': 'User is already a member of the club'
            }), 409

        # Step 3: Insert the user into the clubMembers table
        join_date = datetime.now()
        cur.execute('INSERT INTO "clubMembers" ("clubID", "userID", "userType", "joinDate", "isAdmin", "joinStatus") VALUES (%s, %s, %s, %s, FALSE, TRUE)', (club_id, user_id, user_type, join_date,))
        conn.commit()

        # Get the member's ID in the clubMembers table
        cur.execute('SELECT id FROM "clubMembers" WHERE "clubID" = %s AND "userID" = %s AND "userType" = %s', (club_id, user_id, user_type,))
        return jsonify({
            'message': 'User joined the club successfully',
            'memberID': cur.fetchone()['id']
        }), 201

    except Exception as e:
        print(str(e))
        # Rollback the transaction if an error occurred
        conn.rollback()
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred joining the club."
            }
        ), 500
    
    finally:
        cur.close()


# -----------------------------------------------------------------------------------------
# [POST] addPost
# Purpose: Add a new post to the club
# Used: ClubView.vue [views folder inside Users folder]
# Input:
#   1. Poster ID (i.e., the member's ID in the clubMembers table)
#   2. Club ID
#   3. Post Content
#   4. Post Photo (optional)
# Output: Possible return codes [201 - Post added successfully, 500 - An error occurred adding the post]
@blueprint.route('/addPost', methods=['POST'])
def addPost():
    conn = g.db
    cur = conn.cursor()

    try:
        data = request.get_json()

        # Get all the required data
        poster_id = data['posterID'] # The member's ID in the clubMembers table
        club_id = data['clubID']
        post_content = data['postContent']

        # Step 1: Get today's date
        post_date = datetime.now()

        # List to store the image urls
        image_urls = []

        # Step 2: Check if the post has images
        if 'images' in data:

            # Loop through the images and upload them to S3
            for image in data['images']:
                image64 = s3Images.uploadBase64ImageToS3(image)
                image_urls.append(image64)

            # Make the postPhotos as a text string starting with { and ending with }
            post_photos = '{' + ','.join(f'"{url}"' for url in image_urls) + '}'
        else:
            post_photos = '{}'

        # Step 3: Insert the new post into the database
        cur.execute('INSERT INTO "clubPosts" ("clubID", "postDate", "postContent", "postPhotos", "posterID") VALUES (%s, %s, %s, %s, %s) RETURNING id', 
                    (club_id, post_date, post_content, post_photos, poster_id,))
        post_id = cur.fetchone()['id']
        conn.commit()

        return jsonify({
            'message': 'Post added successfully',
            'postID': post_id
        }), 201

    except Exception as e:
        print(str(e))
        # Rollback the transaction if an error occurred
        conn.rollback()
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
# Input:
#   1. Commenter ID (i.e., the member's ID in the clubMembers table)
#   2. Post ID
#   3. Comment Content
# Output: Possible return codes [201 - Comment added successfully, 404 - No such post exist, 500 - An error occurred adding the comment]
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

        # Step 2: Check if the post exist
        cur.execute('SELECT * FROM "clubPosts" WHERE id = %s', (post_id,))
        post = cur.fetchone()

        if not post:
            return jsonify({
                'error': 'No such post exist'
            }), 404

        # Step 3: Insert the new comment into the database
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
        # Rollback the transaction if an error occurred
        conn.rollback()
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred adding the comment."
            }
        ), 500
    
    finally:
        cur.close()


# -----------------------------------------------------------------------------------------
# [PUT] acceptClubInvite
# Purpose: Join a club after accepting friend's invite to the club (i.e., change joinStatus to TRUE)
# Used: 
# Input: 
#   1. User ID
#   2. UserType
#   2. Club ID
# Output: Possible return codes [200 - User joined the club successfully, 404 - No such club/user exist or user not yet invited to the club, 500 - An error occurred joining the club]
@blueprint.route('/acceptClubInvite', methods=['PUT'])
def acceptClubInvite():
    conn = g.db
    cur = conn.cursor()

    try:
        data = request.get_json()

        # Get all the required data
        user_id = data['userID']
        user_type = data['userType']
        club_id = data['clubID']

        # Step 1: Check if the club exist
        cur.execute('SELECT * FROM "clubs" WHERE id = %s', (club_id,))
        club = cur.fetchone()

        if not club:
            return jsonify({
                'error': 'No such club exist'
            }), 404

        # Step 2: Check if the user exist 
        if user_type == 'user':
            cur.execute('SELECT * FROM "users" WHERE id = %s', (user_id,))
            user = cur.fetchone()
        elif user_type == 'producer':
            cur.execute('SELECT * FROM "producers" WHERE id = %s', (user_id,))
            user = cur.fetchone()
        else:
            cur.execute('SELECT * FROM "venues" WHERE id = %s', (user_id,))
            user = cur.fetchone()

        if not user:
            return jsonify({
                'error': 'No such user exist'
            }), 404
        
        # Step 3: Check if the user has been invited to the club
        cur.execute('SELECT * FROM "clubMembers" WHERE "clubID" = %s AND "userID" = %s AND "userType" = %s', (club_id, user_id, user_type,))
        member = cur.fetchone()

        if not member:
            return jsonify({
                'error': 'User has not been invited to the club'
            }), 404

        # Step 4: Update the joinStatus to TRUE
        cur.execute('UPDATE "clubMembers" SET "joinStatus" = TRUE WHERE "clubID" = %s AND id = %s', (club_id, member['id'],))
        conn.commit()

        return jsonify({
            'message': 'User joined the club successfully'
        }), 200

    except Exception as e:
        print(str(e))
        # Rollback the transaction if an error occurred
        conn.rollback()
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred joining the club."
            }
        ), 500
    
    finally:
        cur.close()


#   -----------------------------------------------------------------------------------------
# [PUT] editPost
# Purpose: Edit a post 
# Used: ClubView.vue [views folder inside Users folder]
# Input:
#   1. Post ID
#   2. Post Content
#   3. Editor ID (i.e., the member ID who edited the post)
#   4. Post Photos (optional)
# Output: Possible return codes [200 - Post edited successfully, 403 - No permission to edit post, 404 - No such post exist, 500 - An error occurred editing the post]
@blueprint.route('/editPost', methods=['PUT'])
def editPost():
    conn = g.db
    cur = conn.cursor()

    try:
        data = request.get_json()

        # Get all the required data
        post_id = data['postID']
        post_content = data['postContent']
        editor_id = data['editorID'] 

        # List to store the image urls
        image_urls = []

        # Step 1: Check if the editor is the creator of the post
        cur.execute('SELECT * FROM "clubPosts" WHERE id = %s AND "posterID" = %s', (post_id, editor_id,))
        isCreator = cur.fetchone()

        if not isCreator:
            # Step 2: Check if the editor is an admin of the club
            cur.execute('SELECT * FROM "clubMembers" WHERE "clubID" = (SELECT "clubID" FROM "clubPosts" WHERE id = %s) AND id = %s AND "isAdmin" = TRUE', (post_id, editor_id,))
            isAdmin = cur.fetchone()

            if not isAdmin:
                return jsonify({
                    'error': 'You do not have the permission to edit this post'
                }), 403

        # Step 3: Check if the post exist
        cur.execute('SELECT * FROM "clubPosts" WHERE id = %s', (post_id,))
        post = cur.fetchone()

        if not post:
            return jsonify({
                'error': 'No such post exist'
            }), 404
        
        # Step 4: Check if the post photo is provided
        if len(data['images']) > 0:

            # Loop through the images and upload them to S3
            for image in data['images']:
                image64 = s3Images.uploadBase64ImageToS3(image)
                image_urls.append(image64)

            # Make the postPhotos as a text string starting with { and ending with }
            post_photos = '{' + ','.join(f'"{url}"' for url in image_urls) + '}'
        else:
            post_photos = '{}'
            
        # Step 5: Update the post content and post photos
        cur.execute('UPDATE "clubPosts" SET "postContent" = %s, "postPhotos" = %s WHERE id = %s', (post_content, post_photos, post_id,))
        conn.commit()

        return jsonify({
            'message': 'Post edited successfully'
        }), 200
    
    except Exception as e:
        print(str(e))
        # Rollback the transaction if an error occurred
        conn.rollback()
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred editing the post."
            }
        ), 500
    
    finally:
        cur.close()


# -----------------------------------------------------------------------------------------
# [PUT] editComment
# Purpose: Edit a comment
# Used: 
# Input:
#   1. Comment ID
#   2. Comment Content
#   3. Editor ID (i.e., the user who edited the comment)
# Output: Possible return codes [200 - Comment edited successfully, 403 - No permission to edit comment, 404 - No such comment exist, 500 - An error occurred editing the comment]
@blueprint.route('/editComment', methods=['PUT'])
def editComment():
    conn = g.db
    cur = conn.cursor()

    try:
        data = request.get_json()

        # Get all the required data
        comment_id = data['commentID']
        comment_content = data['commentContent']
        editor_id = data['editorID'] # The user who edited the comment

        # Step 1: Check if the editor is the creator of the comment
        cur.execute('SELECT * FROM "clubPostComments" WHERE id = %s AND "commenterID" = %s', (comment_id, editor_id,))
        isCreator = cur.fetchone()

        if not isCreator:
            # Step 2: Check if the editor is an admin of the club
            cur.execute('SELECT * FROM "clubMembers" WHERE "clubID" = (SELECT "clubID" FROM "clubPostComments" WHERE id = %s) AND "memberID" = %s AND "isAdmin" = TRUE', (comment_id, editor_id,))
            isAdmin = cur.fetchone()

            if not isAdmin:
                return jsonify({
                    'error': 'You do not have the permission to edit this comment'
                }), 403

        # Step 3: Check if the comment exist
        cur.execute('SELECT * FROM "clubPostComments" WHERE id = %s', (comment_id,))
        comment = cur.fetchone()

        if not comment:
            return jsonify({
                'error': 'No such comment exist'
            }), 404
        
        # Step 4: Update the comment content
        cur.execute('UPDATE "clubPostComments" SET "commentContent" = %s WHERE id = %s', (comment_content, comment_id,))
        conn.commit()

        return jsonify({
            'message': 'Comment edited successfully'
        }), 200
    
    except Exception as e:
        print(str(e))
        # Rollback the transaction if an error occurred
        conn.rollback()
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred editing the comment."
            }
        ), 500
    
    finally:
        cur.close()


# -----------------------------------------------------------------------------------------
# [PUT] likeUnlikePost
# Purpose: Like or Unlike a post
# Used: 
#   1. ClubView.vue [views folder inside Users folder]
# Input:
#   1. Member ID
#   2. Post ID
#   3. Club ID
# Output: Possible return codes [200 - Post liked/unliked successfully, 404 - No such user/post exist, 500 - An error occurred liking the post]
@blueprint.route('/likeUnlikePost', methods=['PUT'])
def likePost():
    conn = g.db
    cur = conn.cursor()

    try:
        data = request.get_json()

        # Get all the required data
        member_id = data['memberID']
        post_id = data['postID']
        club_id = data['clubID']

        # Step 1: Check if the member exist
        cur.execute('SELECT * FROM "clubMembers" WHERE id = %s', (member_id,))
        member = cur.fetchone()

        if not member:
            return jsonify({
                'error': 'No such member exist'
            }), 404

        # Step 2: Check if the post exist
        cur.execute('SELECT * FROM "clubPosts" WHERE id = %s', (post_id,))
        post = cur.fetchone()

        if not post:
            return jsonify({
                'error': 'No such post exist'
            }), 404
        
        # Step 3: Check if the member has already liked the post
        cur.execute('SELECT * FROM "clubPostsLikes" WHERE "clubID" = %s AND "memberID" = %s AND "postID" = %s', (club_id, member_id, post_id,))
        liked = cur.fetchone()

        if liked:
            # Unlike the post
            cur.execute('DELETE FROM "clubPostsLikes" WHERE "clubID" = %s AND "memberID" = %s AND "postID" = %s', (club_id, member_id, post_id,))
            conn.commit()

            return jsonify({
                'message': 'Post unliked successfully',
                "liked": False
            }), 200

        # Step 4: Insert the like into the clubPostsLikes table
        cur.execute('INSERT INTO "clubPostsLikes" ("clubID", "memberID", "postID") VALUES (%s, %s, %s)', (club_id, member_id, post_id,))
        conn.commit()

        return jsonify({
            'message': 'Post liked successfully',
            "liked": True
        }), 200
    
    except Exception as e:
        print(str(e))
        # Rollback the transaction if an error occurred
        conn.rollback()
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred liking the post."
            }
        ), 500
    
    finally:
        cur.close()


# -----------------------------------------------------------------------------------------
# [PUT] likeUnlikeComment
# Purpose: Like or Unlike a comment
# Used: 
# Input:
#   1. Post ID
#   2. Comment ID
#   3. Member ID
# Output: Possible return codes [200 - Comment liked/unliked successfully, 404 - No such user/comment exist, 500 - An error occurred liking the comment]
@blueprint.route('/likeUnlikeComment', methods=['PUT'])
def likeUnlikeComment():
    conn = g.db
    cur = conn.cursor()

    try:
        # Get all the required data
        data = request.get_json()
        post_id = data['postID']
        comment_id = data['commentID']
        member_id = data['memberID']

        # Step 1: Check if the member exist
        cur.execute('SELECT * FROM "clubMembers" WHERE id = %s', (member_id,))
        member = cur.fetchone()

        if not member:
            return jsonify({
                'error': 'No such member exist'
            }), 404

        # Step 2: Check if the comment exist
        cur.execute('SELECT * FROM "clubPostComments" WHERE id = %s', (comment_id,))
        comment = cur.fetchone()

        if not comment:
            return jsonify({
                'error': 'No such comment exist'
            }), 404
        
        # Step 3: Check if the member has already liked the comment
        cur.execute('SELECT * FROM "clubPostCommentsLikes" WHERE "postID" = %s AND "memberID" = %s AND "commentID" = %s', (post_id, member_id, comment_id,))
        liked = cur.fetchone()

        if liked:
            # Unlike the comment
            cur.execute('DELETE FROM "clubPostCommentsLikes" WHERE "postID" = %s AND "memberID" = %s AND "commentID" = %s', (post_id, member_id, comment_id,))
            conn.commit()

            return jsonify({
                'message': 'Comment unliked successfully'
            }), 200

        # Step 4: Insert the like into the clubPostCommentsLikes table
        cur.execute('INSERT INTO "clubPostCommentsLikes" ("postID", "memberID", "commentID") VALUES (%s, %s, %s)', (post_id, member_id, comment_id,))
        conn.commit()

        return jsonify({
            'message': 'Comment liked successfully'
        }), 200

    except Exception as e:
        print(str(e))
        # Rollback the transaction if an error occurred
        conn.rollback()
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred liking the comment."
            }
        ), 500
    
    finally:
        cur.close()


# -----------------------------------------------------------------------------------------
# [PUT] makeAdmin
# Purpose: Make a member an admin of the club
# Used:
# Input:
#   1. Member ID (i.e., the member ID who is being made an admin)
#   2. Club ID
#   3. Admin ID (i.e., the member ID who is making the member an admin)
# Output: Possible return codes [200 - Member is now an admin, 403 - No permission to make member an admin, 404 - No such club/member exist, 500 - An error occurred making the member an admin]
@blueprint.route('/makeAdmin', methods=['PUT'])
def makeAdmin():
    conn = g.db
    cur = conn.cursor()

    try:
        data = request.get_json()

        # Get all the required data
        member_id = data['memberID']
        club_id = data['clubID']
        admin_id = data['adminID']

        # Step 1: Check if the club exist
        cur.execute('SELECT * FROM "clubs" WHERE id = %s', (club_id,))
        club = cur.fetchone()

        if not club:
            return jsonify({
                'error': 'No such club exist'
            }), 404

        # Step 2: Check if the user who is making someone an admin is an admin of the club
        cur.execute('SELECT * FROM "clubMembers" WHERE "clubID" = %s AND "memberID" = %s AND "isAdmin" = TRUE', (club_id, admin_id,))
        isAdmin = cur.fetchone()

        if not isAdmin:
            return jsonify({
                'error': 'You do not have the permission to make a member an admin of this club'
            }), 403

        # Step 3: Check if the member exist
        cur.execute('SELECT * FROM "clubMembers" WHERE id = %s', (member_id,))
        member = cur.fetchone()

        if not member:
            return jsonify({
                'error': 'No such member exist'
            }), 404

        # Step 4: Make the member an admin
        cur.execute('UPDATE "clubMembers" SET "isAdmin" = TRUE WHERE "clubID" = %s AND id = %s', (club_id, member_id,))
        conn.commit()

        return jsonify({
            'message': 'Member is now an admin'
        }), 200

    except Exception as e:
        print(str(e))
        # Rollback the transaction if an error occurred
        conn.rollback()
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred making the member an admin."
            }
        ), 500
    
    finally:
        cur.close()


# -----------------------------------------------------------------------------------------
# [PUT] updateClubInfo
# Purpose: Update the club information
# Used: ClubSettings.vue [views folder inside User folder]
# Input:
#   1. Club ID
#   2. Club Name 
#   3. Club Description
#   4. Is Invite Only (boolean: True = Private, False = Public)
#   5. Club Banner (optional)
#   6. Editor ID (i.e., the user who is updating the club information)
# Output: Possible return codes [200 - Club information updated successfully, 403 - No permission to edit the club information, 404 - No such club exist, 500 - An error occurred updating the club information]
@blueprint.route('/updateClubInfo', methods=['PUT'])
def updateClubInfo():
    conn = g.db
    cur = conn.cursor()

    try:
        data = request.get_json()

        # Get all the required data
        club_id = data['clubID']
        club_name = data['clubName']
        club_desc = data['clubDesc']
        is_invite_only = data['isInviteOnly']
        editor_id = data['editorID']

        # Step 1: Check if the club exist
        cur.execute('SELECT * FROM "clubs" WHERE id = %s', (club_id,))
        club = cur.fetchone()

        if not club:
            return jsonify({
                'error': 'No such club exist'
            }), 404

        # Step 2: Check if the user who is updating the club information is an admin of the club
        cur.execute('SELECT * FROM "clubMembers" WHERE "clubID" = %s AND "memberID" = %s AND "isAdmin" = TRUE', (club_id, editor_id,))
        isAdmin = cur.fetchone()

        if not isAdmin:
            return jsonify({
                'error': 'You do not have the permission to edit the club information'
            }), 403

        # Step 3: Check if the club banner is provided
        if 'image64' in data:
            image64 = s3Images.uploadBase64ImageToS3(data['image64'])

            # Update the club banner
            cur.execute('UPDATE "clubs" SET "clubBanner" = %s WHERE id = %s', (image64, club_id,))
            conn.commit()

        # Step 4: Update the club information
        cur.execute('UPDATE "clubs" SET "clubName" = %s, "clubDesc" = %s, "isInviteOnly" = %s WHERE id = %s', (club_name, club_desc, is_invite_only, club_id,))
        conn.commit()

        return jsonify({
            'message': 'Club information updated successfully'
        }), 200
    
    except Exception as e:
        print(str(e))
        # Rollback the transaction if an error occurred
        conn.rollback()
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred updating the club information."
            }
        ), 500
    
    finally:
        cur.close()


# -----------------------------------------------------------------------------------------
# [DELETE] removeMembers
# Purpose: Remove members from the club
# Used:
# Input:
#   1. A list of member IDs to be removed from the club
#   2. Club ID
#   3, Remover ID (i.e., the user who is removing the members)
# Output: Possible return codes [200 - Members removed successfully, 403 - No permission to remove members, 404 - No such club exist, 500 - An error occurred removing the members]
@blueprint.route('/removeMembers', methods=['DELETE'])
def removeMembers():
    conn = g.db
    cur = conn.cursor()

    try:
        data = request.get_json()

        # Get all the required data
        club_id = data['clubID']
        members_list = data['members']
        remover_id = data['removerID']

        # Step 1: Check if the club exist
        cur.execute('SELECT * FROM "clubs" WHERE id = %s', (club_id,))
        club = cur.fetchone()

        if not club:
            return jsonify({
                'error': 'No such club exist'
            }), 404
        
        # Step 2: Check if the remover is an admin of the club
        cur.execute('SELECT * FROM "clubMembers" WHERE "clubID" = %s AND "memberID" = %s AND "isAdmin" = TRUE', (club_id, remover_id,))
        isAdmin = cur.fetchone()

        if not isAdmin:
            return jsonify({
                'error': 'You do not have the permission to remove members from this club'
            }), 403

        # Step 3: Remove the members from the club
        for member_id in members_list:
            # Check if the member exist
            cur.execute('SELECT * FROM "clubMembers" WHERE id = %s', (member_id,))
            member = cur.fetchone()

            if not member: # Skip to the next member if the user does not exist
                continue

            # Check if the user is an existing member of the club
            cur.execute('SELECT * FROM "clubMembers" WHERE "clubID" = %s AND id = %s', (club_id, member_id,))
            member = cur.fetchone()

            if not member: # Skip to the next member if the user is not an existing member of the club
                continue

            cur.execute('DELETE FROM "clubMembers" WHERE "clubID" = %s AND id = %s', (club_id, member_id,))
            conn.commit()

        return jsonify({
            'message': 'Members removed successfully'
        }), 200

    except Exception as e:
        print(str(e))
        # Rollback the transaction if an error occurred
        conn.rollback()
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred removing the members."
            }
        ), 500
    
    finally:
        cur.close()


# -----------------------------------------------------------------------------------------
# [DELETE] removePost
# Purpose: Remove a post
# Used: ClubView.vue [views folder inside Users folder]
# Input:
#   1. Post ID
#   2. Remover ID (i.e., the member ID who is removing the post)
# Output: Possible return codes [200 - Post removed successfully, 403 - No permission to remove post, 404 - No such post exist, 500 - An error occurred removing the post]
@blueprint.route('/removePost', methods=['DELETE'])
def removePost():
    conn = g.db
    cur = conn.cursor()

    try:
        # Get all the required data
        data = request.get_json()

        post_id = data['postID']
        remover_id = data['removerID']

        # Step 1: Check if the remover is the creator of the post
        cur.execute('SELECT * FROM "clubPosts" WHERE id = %s AND "posterID" = %s', (post_id, remover_id,))
        isCreator = cur.fetchone()

        if not isCreator:
            # Step 2: Check if the remover is an admin of the club
            cur.execute('SELECT * FROM "clubMembers" WHERE "clubID" = (SELECT "clubID" FROM "clubPosts" WHERE id = %s) AND "memberID" = %s AND "isAdmin" = TRUE', (post_id, remover_id,))
            isAdmin = cur.fetchone()

            if not isAdmin:
                return jsonify({
                    'error': 'You do not have the permission to remove this post'
                }), 403
        
        # Step 3: Check if the post exist
        cur.execute('SELECT * FROM "clubPosts" WHERE id = %s', (post_id,))
        post = cur.fetchone()

        if not post:
            return jsonify({
                'error': 'No such post exist'
            }), 404

        # Step 4: Remove all the likes for the comments in the post
        cur.execute('DELETE FROM "clubPostCommentsLikes" WHERE "postID" = %s', (post_id,))

        # Step 5: Remove all the comments for the post
        cur.execute('DELETE FROM "clubPostComments" WHERE "postID" = %s', (post_id,))

        # Step 6: Remove all the likes for the post
        cur.execute('DELETE FROM "clubPostsLikes" WHERE "postID" = %s', (post_id,))
        
        # Step 7: Remove the post
        cur.execute('DELETE FROM "clubPosts" WHERE id = %s', (post_id,))
        conn.commit()

        return jsonify({
            'message': 'Post removed successfully'
        }), 200
    
    except Exception as e:
        print(str(e))
        # Rollback the transaction if an error occurred
        conn.rollback()
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred removing the post."
            }
        ), 500
    
    finally:
        cur.close()


# -----------------------------------------------------------------------------------------
# [DELETE] removeComment
# Purpose: Remove a comment
# Used: 
# Input:
#   1. Comment ID
#   2. Remover ID (i.e., the member ID who is removing the comment)
# Output: Possible return codes [200 - Comment removed successfully, 403 - No permission to remove comment, 404 - No such comment exist, 500 - An error occurred removing the comment]
@blueprint.route('/removeComment', methods=['DELETE'])
def removeComment():
    conn = g.db
    cur = conn.cursor()

    try:
        # Get all the required data
        data = request.get_json()

        comment_id = data['commentID']
        remover_id = data['removerID']

        # Step 1: Check if the remover is the creator of the comment
        cur.execute('SELECT * FROM "clubPostComments" WHERE id = %s AND "commenterID" = %s', (comment_id, remover_id,))
        isCreator = cur.fetchone()

        if not isCreator:
            # Step 2: Check if the remover is an admin of the club
            cur.execute('SELECT * FROM "clubMembers" WHERE "clubID" = (SELECT "clubID" FROM "clubPostComments" WHERE id = %s) AND "memberID" = %s AND "isAdmin" = TRUE', (comment_id, remover_id,))
            isAdmin = cur.fetchone()

            if not isAdmin:
                return jsonify({
                    'error': 'You do not have the permission to remove this comment'
                }), 403

        # Step 3: Check if the comment exist
        cur.execute('SELECT * FROM "clubPostComments" WHERE id = %s', (comment_id,))
        comment = cur.fetchone()

        if not comment:
            return jsonify({
                'error': 'No such comment exist'
            }), 404
        
        # Step 4: Remove all the likes for the comment
        cur.execute('DELETE FROM "clubPostCommentsLikes" WHERE "commentID" = %s', (comment_id,))

        # Step 5: Remove the comment
        cur.execute('DELETE FROM "clubPostComments" WHERE id = %s', (comment_id,))
        conn.commit()

        return jsonify({
            'message': 'Comment removed successfully'
        }), 200
    
    except Exception as e:
        print(str(e))
        # Rollback the transaction if an error occurred
        conn.rollback()
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred removing the comment."
            }
        ), 500
    
    finally:
        cur.close()


# -----------------------------------------------------------------------------------------
# [DELETE] leaveClub
# Purpose: Leave the club
# Used: ClubView.vue [views folder inside Users folder]
# Input:
#   1. Member ID
#   2. Club ID
# Output: Possible return codes [200 - Member left the club successfully, 404 - No such club/member exist, 500 - An error occurred leaving the club]
@blueprint.route('/leaveClub', methods=['DELETE'])
def leaveClub():
    conn = g.db
    cur = conn.cursor()

    try:
        data = request.get_json()

        # Get all the required data
        member_id = data['memberID']
        club_id = data['clubID']

        # Step 1: Check if the club exist
        cur.execute('SELECT * FROM "clubs" WHERE id = %s', (club_id,))
        club = cur.fetchone()

        if not club:
            return jsonify({
                'error': 'No such club exist'
            }), 404

        # Step 2: Check if the member exist
        cur.execute('SELECT * FROM "clubMembers" WHERE id = %s', (member_id,))
        member = cur.fetchone()

        if not member:
            return jsonify({
                'error': 'No such member exist'
            }), 404
        
        # Step 3: Remove comments, likes and posts of the member
        cur.execute('DELETE FROM "clubPostCommentsLikes" WHERE "memberID" = %s', (member_id,))
        cur.execute('DELETE FROM "clubPostComments" WHERE "commenterID" = %s', (member_id,))
        cur.execute('DELETE FROM "clubPostsLikes" WHERE "memberID" = %s', (member_id,))
        cur.execute('DELETE FROM "clubPosts" WHERE "posterID" = %s', (member_id,))
        
        # Step 4: Leave the club
        cur.execute('DELETE FROM "clubMembers" WHERE "clubID" = %s AND id = %s', (club_id, member_id,))
        conn.commit()

        return jsonify({
            'message': 'Member left the club successfully'
        }), 200

    except Exception as e:
        print(str(e))
        # Rollback the transaction if an error occurred
        conn.rollback()
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred leaving the club."
            }
        ), 500
    
    finally:
        cur.close()


# -----------------------------------------------------------------------------------------
# [DELETE] deleteClub
# Purpose: Delete the club
# Used: ClubSettings.vue [views folder inside User folder]
# Input:
#   1. Club ID
# Output: Possible return codes [200 - Club deleted successfully, 404 - No such club exist, 500 - An error occurred deleting the club]
@blueprint.route('/deleteClub', methods=['DELETE'])
def deleteClub():
    conn = g.db
    cur = conn.cursor()

    try:
        data = request.get_json()

        # Get all the required data
        club_id = data['clubID']

        # Step 1: Check if the club exist
        cur.execute('SELECT * FROM "clubs" WHERE id = %s', (club_id,))
        club = cur.fetchone()

        if not club:
            return jsonify({
                'error': 'No such club exist'
            }), 404
        
        # Step 2: Remove all the club members
        cur.execute('DELETE FROM "clubMembers" WHERE "clubID" = %s', (club_id,))

        # Step 3: Remove all the post in the club
        cur.execute('DELETE FROM "clubPosts" WHERE "clubID" = %s', (club_id,))

        # Step 4: Remove all the likes for the post, comments for deleted posts and likes for the comments where the post ID is null
        cur.execute('DELETE FROM "clubPostsLikes" WHERE "clubID" = %s', (club_id,))
        cur.execute('DELETE FROM "clubPostComments" WHERE "postID" IS NULL')
        cur.execute('DELETE FROM "clubPostCommentsLikes" WHERE "postID" IS NULL')

        # Step 5: Remove the club
        cur.execute('DELETE FROM "clubs" WHERE id = %s', (club_id,))
        conn.commit()

        return jsonify({
            'message': 'Club deleted successfully'
        }), 200

    except Exception as e:
        print(str(e))
        # Rollback the transaction if an error occurred
        conn.rollback()
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred deleting the club."
            }
        ), 500
    
    finally:
        cur.close()
