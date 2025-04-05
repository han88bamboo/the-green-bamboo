# Files which adds or deducts points
# club.py / createReview.py / deleteReview.py / editProducerProfile.py / editVenueProfile.py


# Routes: 
#   [pointSystemRules] 
#   /getPointSystemRules (GET), 
#   /createPointSystemRule (POST), 
#   /updatePointSystemRule/<id> (PUT), 
#   /deletePointSystemRule/<id> (DELETE)
# 
#   [pointsRecorder]
#   /getPointsForUser/<id>/<userType> (GET), 
#   /createPointsForUser (POST)
# -----------------------------------------------------------------------------------------

import os
from flask import Blueprint, g, jsonify, request

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)


# -----------------------------------------------------------------------------------------
# [GET] /getPointSystemRules
@blueprint.route('/getPointSystemRules', methods=['GET'])
def getPointSystemRules():

    conn = g.db
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM "pointSystemRules"')
    rules = cursor.fetchall()

    if not rules:
        return jsonify({"message": "No point system rules found"}), 404

    cursor.close()

    return jsonify(rules), 200


# -----------------------------------------------------------------------------------------
# [POST] /createPointSystemRule
@blueprint.route('/createPointSystemRule', methods=['POST'])
def createPointSystemRule():

    conn = g.db
    cursor = conn.cursor()

    data = request.json

    # Check if all required fields are present
    if 'rule_name' not in data or 'rule_desc' not in data or 'rule_category' not in data or 'points' not in data:
        return jsonify({"message": "Missing required fields"}), 400
    
    # Check if user is admin
    if data['userType'] != 'admin':
        return jsonify({"message": "Unauthorized"}), 401
    
    try:
        # Check if rule already exists (rule_name)
        cursor.execute('SELECT * FROM "pointSystemRules" WHERE "ruleName" = %s', (data['rule_name'],))

        if cursor.fetchone():
            return jsonify({"message": "Point system rule already exists"}), 409
        
        # Create point system rule
        cursor.execute('INSERT INTO "pointSystemRules" ("ruleName", "ruleDesc", "ruleCategory", "proofPoints") VALUES (%s, %s, %s)', (data['rule_name'], data['rule_desc'], data['rule_category'], data['proof_points']))
        conn.commit()

        return jsonify({"message": "Point system rule created"}), 201
    
    except Exception as e:
        # Rollback if error occurs
        conn.rollback()
        return jsonify({"message": str(e)}), 500
    
    finally:
        cursor.close()


# -----------------------------------------------------------------------------------------
# [PUT] /updatePointSystemRule/<id>
@blueprint.route('/updatePointSystemRule/<id>', methods=['PUT'])
def updatePointSystemRule(id):

    conn = g.db
    cursor = conn.cursor()

    data = request.json

    # Check if all required fields are present
    if 'rule_name' not in data or 'rule_desc' not in data or 'rule_category' not in data or 'points' not in data:
        return jsonify({"message": "Missing required fields"}), 400
    
    # Check if user is admin
    if data['userType'] != 'admin':
        return jsonify({"message": "Unauthorized"}), 401
    
    try:
        # Check if rule exists
        cursor.execute('SELECT * FROM "pointSystemRules" WHERE "ruleId" = %s', (id,))

        if not cursor.fetchone():
            return jsonify({"message": "Point system rule not found"}), 404
        
        # Update point system rule
        cursor.execute('UPDATE "pointSystemRules" SET "ruleName" = %s, "ruleDesc" = %s, "ruleCategory" = %s, "proofPoints" = %s WHERE "ruleId" = %s', (data['rule_name'], data['rule_desc'], data['rule_category'], data['proof_points'], id))
        conn.commit()

        return jsonify({"message": "Point system rule updated"}), 201
    
    except Exception as e:
        # Rollback if error occurs
        conn.rollback()
        return jsonify({"message": str(e)}), 500
    
    finally:
        cursor.close()


# -----------------------------------------------------------------------------------------
# [DELETE] /deletePointSystemRule/<id>
@blueprint.route('/deletePointSystemRule/<id>', methods=['DELETE'])
def deletePointSystemRule(id):

    conn = g.db
    cursor = conn.cursor()

    data = request.json

    # Check if user is admin
    if data['userType'] != 'admin':
        return jsonify({"message": "Unauthorized"}), 401
    
    # Check if rule exists
    cursor.execute('SELECT * FROM "pointSystemRules" WHERE "ruleId" = %s', (id,))

    if not cursor.fetchone():
        return jsonify({"message": "Point system rule not found"}), 404
    
    # Delete point system rule
    cursor.execute('DELETE FROM "pointSystemRules" WHERE "ruleId" = %s', (id,))
    conn.commit()

    cursor.close()

    return jsonify({"message": "Point system rule deleted"}), 200


# -----------------------------------------------------------------------------------------
# [GET] /getPointsForUser/<id>/<userType>
@blueprint.route('/getPointsForUser/<id>/<userType>', methods=['GET'])
def getPointsForUser(id, userType):

    conn = g.db
    cursor = conn.cursor()
    
    # Get points for user
    cursor.execute('SELECT * FROM "pointsRecorder" WHERE "userID" = %s AND "userType" = %s', (id, userType,))
    user_points = cursor.fetchone()

    if not user_points:
        return jsonify({"message": "User points not found"}), 404

    # Get the review id for reviews made by user
    cursor.execute('SELECT id FROM "reviews" WHERE "userID" = %s', (id,))
    review_ids = cursor.fetchall()

    
    # Loop through each review id and compile number of upvotes and downvotes for each review
    total_review_upvotes = 0
    total_review_downvotes = 0

    if review_ids:
        for review_id in review_ids:

            r_id = review_id['id']
            cursor.execute('SELECT "upvotes", "downvotes" FROM "reviewsUserVotes" WHERE "reviewId" = %s', (r_id,))
            votes = cursor.fetchone()

            if votes:
                total_review_upvotes += len(votes['upvotes'])
                total_review_downvotes += len(votes['downvotes'])
            else:
                # If no votes, set to 0
                total_review_upvotes += 0
                total_review_downvotes += 0
    
    print("Total review upvotes: ", total_review_upvotes)
    print("Total review downvotes: ", total_review_downvotes)

    # Get the producer review id for producer reviews made by user
    cursor.execute('SELECT id FROM "producerReviews" WHERE "userID" = %s', (id,))
    producer_review_ids = cursor.fetchall()

    
    # Loop through each producer review id and compile number of upvotes and downvotes for each producer review
    total_producer_review_upvotes = 0
    total_producer_review_downvotes = 0

    if producer_review_ids:
        for producer_review_id in producer_review_ids:
            pr_id = producer_review_id['id']
            cursor.execute('SELECT "upvotes", "downvotes" FROM "producerReviewsUserVotes" WHERE "reviewId" = %s', (pr_id,))
            votes = cursor.fetchone()

            if votes:
                total_producer_review_upvotes += len(votes['upvotes'])
                total_producer_review_downvotes += len(votes['downvotes'])
            else:
                total_producer_review_upvotes += 0
                total_producer_review_downvotes += 0

    print("Total producer review upvotes: ", total_producer_review_upvotes)
    print("Total producer review downvotes: ", total_producer_review_downvotes)

    # Get the member ids of the user 
    cursor.execute('SELECT id FROM "clubMembers" WHERE "userID" = %s', (id,))
    member_ids = cursor.fetchall()

    # Loop through each member id and compile number of likes and dislikes for posts and comments made 
    total_member_likes = 0
    total_member_dislikes = 0

    if member_ids:
        for member_id in member_ids:

            m_id = member_id['id']

            # Get total likes for club posts
            cursor.execute('SELECT COUNT(id) FROM "clubPostsLikes" WHERE "memberID" = %s', (m_id,))
            total_member_likes += cursor.fetchone()['count']

            # Get total dislikes for club posts
            cursor.execute('SELECT COUNT(id) FROM "clubPostsDislikes" WHERE "memberID" = %s', (m_id,))
            total_member_dislikes += cursor.fetchone()['count']

            # Get total likes for club comments
            cursor.execute('SELECT COUNT(id) FROM "clubPostCommentsLikes" WHERE "memberID" = %s', (m_id,))
            total_member_likes += cursor.fetchone()['count']

            # Get total dislikes for club comments
            cursor.execute('SELECT COUNT(id) FROM "clubPostCommentsDislikes" WHERE "memberID" = %s', (m_id,))
            total_member_dislikes += cursor.fetchone()['count']
        
    print("Total member likes: ", total_member_likes)
    print("Total member dislikes: ", total_member_dislikes)

    # Get the proofPoints for upvotes and downvotes
    cursor.execute('SELECT "proofPoints" FROM "pointSystemRules" WHERE id = 8')
    upvote_points = cursor.fetchone()['proofPoints']

    cursor.execute('SELECT "proofPoints" FROM "pointSystemRules" WHERE id = 9')
    downvote_points = cursor.fetchone()['proofPoints']

    overall_total_upvotes = total_review_upvotes + total_producer_review_upvotes + total_member_likes
    overall_total_downvotes = total_review_downvotes + total_producer_review_downvotes + total_member_dislikes

    # Calculate total points
    total_points = user_points['currentPoints'] + (overall_total_upvotes * upvote_points) + (overall_total_downvotes * downvote_points)

    cursor.close()

    return jsonify(total_points), 200


# -----------------------------------------------------------------------------------------
# [POST] /createPointsForUser
@blueprint.route('/createPointsForUser', methods=['POST'])
def createPointsForUser():

    conn = g.db
    cursor = conn.cursor()

    data = request.json

    # Check if all required fields are present
    if 'user_id' not in data or 'user_type' not in data:
        return jsonify({"message": "Missing required fields, user id and user type must be provided."}), 400
        

    try: 
        # Check if user already has points
        cursor.execute('SELECT * FROM "userPoints" WHERE "userID" = %s AND "userType" = %s', (data['user_id'], data['user_type'],))

        if cursor.fetchone():
            return jsonify({"message": "User already has points"}), 409
        
        # Create points for user
        cursor.execute('INSERT INTO "userPoints" ("userID", "userType", "points") VALUES (%s, %s, 0)', (data['user_id'], data['user_type'],))
        conn.commit()

        return jsonify({"message": "User points created"}), 201
    
    except Exception as e:
        # Rollback if error occurs
        conn.rollback()
        return jsonify({"message": str(e)}), 500
    
    finally:
        cursor.close()

    
