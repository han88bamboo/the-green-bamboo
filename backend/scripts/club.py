# Port: 5700
# Routes: /getClubs (GET), /getClubPosts (GET), /getClubPostDetails (GET), 
#         /getUserLikesPost (GET), /getUserLikesComments (GET)
#         /createClubs (POST), /addPost (POST), /addComment (POST), 
#         /addClubMembers (PUT), /editPost (PUT), /editComment (PUT)
#         /likePost (PUT), /likeComment (PUT)
# -----------------------------------------------------------------------------------------

import os
import json
from flask import Blueprint, g, jsonify, request

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

# -----------------------------------------------------------------------------------------
# [GET] getClubs
# Purpose: Get 20 clubs information each time this is called. 
# Used: ClubSearchPage.vue [views folder]
@blueprint.route('/getClubs/<id>', methods=['GET'])
def getClubs(id):
    conn = g.db
    cur = conn.cursor()

    return_data = {}

    try:

        # Step 1: Get the 20 clubs
        # ID: Used to define the starting ID to retrieve from
        cur.execute('SELECT * FROM "clubs" WHERE id >= %s ORDER BY id ASC LIMIT 20', (id))
        clubs_info = cur.fetchall()

        if not clubs_info:
            return jsonify({
                'error': 'No clubs found in database'
            }), 404
        

        # Step 2: Get the total number of members in each of the 20 clubs 
        for club in clubs_info:
            club_id = club['id']

            # Get the total number of members in each club
            cur.execute('SELECT COUNT(*) AS "totalMembers" FROM "clubMembers" WHERE "clubID" = %s AND "joinStatus" = TRUE', (club_id))
            num_members = cur.fetchone()

            # Add club summary into return data
            club['totalMembers'] = num_members
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
@blueprint.route('/getClubPosts/<clubID>/<id>', methods=['GET'])
def getClubPosts(clubID, id):
    conn = g.db
    cur = conn.cursor()

    # list to track if user information has been retrieved (reason being, a single user can post multiple post, this may help to reduce data being sent over to the frontend)
    users_retrieved_list = []

    try:

        # check if club exists
        cur.execute('SELECT * FROM "clubs" WHERE clubID = %s', (clubID))
        club = cur.fetchone()

        if not club:
            return jsonify({
                'error': f'No such club exist for club id: {clubID}'
            })

        # Step 1: Get the top 10 latest post in that club
        cur.execute('SELECT * FROM "clubPosts" WHERE clubID = %s AND id >= %s ORDER BY postDate DESC LIMIT 10', (clubID, id))
        post_info = cur.fetchall() # returns empty list if no result found

        if not post_info:
            return jsonify({
                'error': 'No post yet'
            }), 404
        
        # Step 2: Get the number of likes for each post and the poster's id, displayName, photo
        for post in post_info:
            posterID = post['posterID']
            postID = post['id']

            if posterID not in users_retrieved_list:
                cur.execute('SELECT "id", "displayName", "photo" FROM "users" WHERE id = %s', (posterID))
                poster_info = cur.fetchone()
                users_retrieved_list.append(posterID)
            
            # Add poster info into post
            post['posterInfo'] = poster_info

            cur.execute('SELECT COUNT(*) FROM "clubPostsLikes" WHERE postID = %s', (postID))
            total_likes = cur.fetchone()

            # Add total likes into post
            post['totalLikes'] = total_likes

            return jsonify({
                'data': post_info
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
@blueprint.route('/getClubPostDetails/<postID>/<id>', methods=['GET'])
def getClubPostDetails(postID, id):
    conn = g.db
    cur = conn.cursor()

    # list to track if user information has been retrieved (reason being, a single user can post multiple post, this may help to reduce data being sent over to the frontend)
    users_retrieved_list = []

    try:
        # check if post exist
        cur.execute('SELECT * FROM "clubPostComments" WHERE postID = %s', (postID))
        post = cur.fetchone()

        if not post:
            return jsonify({
                'error': f"No such post for this post id {postID}"
            }), 404

        # Step 1: Get the latest 20 comments for the specific post
        cur.execute('SELECT * FROM "clubPostComments" WHERE postID = %s AND id >= %s ORDER BY commentDate DESC LIMIT 20', (postID, id))
        comments_info = cur.fetchall()

        if not comments_info:
            return jsonify({
                'error': 'No comments for this post yet'
            }), 404
        
        # Step 2: Get the total likes, commenter's id, displayName and photo
        for comment in comments_info:
            commenterID = comment['commenterID']

            if commenterID not in users_retrieved_list:
                cur.execute('SELECT "id", "displayName", "photo" FROM "users" WHERE id = %s', (commenterID))
                commenter_info = cur.fetchone()
                users_retrieved_list.append(commenterID)

                if not commenter_info:






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