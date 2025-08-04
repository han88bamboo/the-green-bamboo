# Purpose: A file that contains the functions that helps endpoints in proof points related operations.

from flask import g

# Get the rank of the user using proof points
def get_rank(proof_points):
    """
    Get the rank of the user based on their proof points.

    Args:
        proof_points (int): The proof points of the user.

    Returns:
        str: The rank of the user.
    """

    emoji = "🧃 "

    if proof_points >= 800:
        return (emoji + "Imperial", "#027562")
    elif proof_points >= 400:
        return (emoji + "Over Proof", "#83A9E8")
    elif proof_points >= 200:
        return (emoji + "Full Proof", "#F0B358")
    elif proof_points >= 101:
        return (emoji + "Aperitif", "#6C348B")
    else:
        return (emoji + "Highball", "#B40138")


#############################################################################################################


# Get the rank of the user using User ID
def get_rank_by_user_id(user_id):
    """
    Get the rank of the user based on their user ID.

    Args:
        user_id (int): The ID of the user.

    Returns:
        str: The rank of the user.
    """
    # Retrieve the user's proof points from the database
    conn = g.db
    cur = conn.cursor()
    cur.execute('SELECT "currentPoints" FROM "pointsRecorder" WHERE "userID" = %s AND "userType" = %s', (user_id, 'user',))
    proof_points = cur.fetchone()

    # If no proof points are found, return None
    if proof_points is None:
        return None

    # Get the rank of the user using proof points
    return get_rank(proof_points['currentPoints'])


###############################################################################################################


# Check if the user has reached the max proof points to continue earning points 

# Variable to store if max proof point is active or inactive
max_proof_point_active = False

def check_max_proof_points(user_id):
    """
    Check if the user has reached the max proof points to continue earning points.

    Args:
        user_id (int): The ID of the user.

    Returns:
        bool: True if the user has reached the max proof points, False otherwise.
    """

    # If max proof points is inactive, return False so that the user can continue earning points
    if not max_proof_point_active:
        return False

    # Retrieve the max proof points from the database
    conn = g.db
    cur = conn.cursor()

    # Retrieve the max proof points from the database
    cur.execute('SELECT "proofPoints" FROM "pointSystemRules" WHERE id = %s', (1,))
    max_points = cur.fetchone()

    # Retrieve the user's proof points from the database
    cur.execute('SELECT "currentPoints" FROM "pointsRecorder" WHERE "userID" = %s AND "userType" = %s', (user_id, 'user',))
    current_points = cur.fetchone()

    # Check if the user has reached the max proof points
    if current_points['currentPoints'] >= max_points['proofPoints']:
        return True
    else:
        return False


###############################################################################################################


# Check if user has achieved the minumum proof points to create a club 
max_number_of_clubs = 3
min_points = 100

def check_user_can_create_club(user_id):
    """
    Check if the user has achieved the minimum proof points to create a club.

    Args:
        user_id (int): The ID of the user.

    Returns:
        bool: True if the user can create a club, False otherwise.
    """

    # Retrieve the minimum proof points from the database
    conn = g.db
    cur = conn.cursor()

    # Retrieve the user's current proof points from the database
    cur.execute('SELECT "currentPoints" FROM "pointsRecorder" WHERE "userID" = %s AND "userType" = %s', (user_id, 'user',))
    current_points = cur.fetchone()

    # Check if user exists in the points system
    if current_points is None:
        return (False, 'user not found', 0)


    # Check if the user has reached the minimum proof points to create a club
    if current_points['currentPoints'] >= min_points:
        
        # Check if the user has reached the maximum number of clubs they can create
        cur.execute('SELECT COUNT(*) FROM "clubs" WHERE "createdByID" = %s AND "createdByType" = %s', (user_id, 'user',))
        club_count = cur.fetchone()

        if club_count['count'] < max_number_of_clubs:
            return (True, None, None)
        else:
            return (False, 'max clubs reached', max_number_of_clubs)
    else:
        return (False, 'insufficient points', min_points)


###############################################################################################################

# Get the current proof points of the user using user ID
def get_current_proof_points(user_id):
    """
    Get the current proof points of the user based on their user ID.

    Args:
        user_id (int): The ID of the user.

    Returns:
        int: The current proof points of the user.
    """

    # Retrieve the user's proof points from the database
    conn = g.db
    cursor = conn.cursor()
    cursor.execute('SELECT "currentPoints" FROM "pointsRecorder" WHERE "userID" = %s AND "userType" = %s', (user_id, 'user',))
    user_points = cursor.fetchone()

    # If no proof points are found, return None
    if user_points is None:
        return None

    # Get the total likes and dislikes for reviews, posts, and comments 

    # Step 1: Listing Reviews 
    cursor.execute('SELECT id FROM "reviews" WHERE "userID" = %s', (user_id,))
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

    # Get the producer review id for producer reviews made by user
    cursor.execute('SELECT id FROM "producerReviews" WHERE "userID" = %s', (user_id,))
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


    # Get the venue review id for producer reviews made by user
    cursor.execute('SELECT id FROM "venueReviews" WHERE "userID" = %s', (user_id,))
    venue_review_ids = cursor.fetchall()

    # Loop through each venue review id and compile number of upvotes and downvotes for each venue review
    total_venue_review_upvotes = 0
    total_venue_review_downvotes = 0

    if venue_review_ids:
        for venue_review_id in venue_review_ids:
            vr_id = venue_review_id['id']
            cursor.execute('SELECT "upvotes", "downvotes" FROM "venueReviewsUserVotes" WHERE "reviewId" = %s', (vr_id,))
            votes = cursor.fetchone()

            if votes:
                total_venue_review_upvotes += len(votes['upvotes'])
                total_venue_review_downvotes += len(votes['downvotes'])
            else:
                total_venue_review_upvotes += 0
                total_venue_review_downvotes += 0

    # Get the member ids of the user 
    cursor.execute('SELECT id FROM "clubMembers" WHERE "userID" = %s', (user_id,))
    member_ids = cursor.fetchall()

    post_ids = []
    comment_ids = []

    # Get the post ids for posts ids and comments ids made by user
    for member_id in member_ids:
        m_id = member_id['id']
        cursor.execute('SELECT id FROM "clubPosts" WHERE "posterID" = %s', (m_id,))
        post_ids += cursor.fetchall()

        cursor.execute('SELECT id FROM "clubPostComments" WHERE "commenterID" = %s', (m_id,))
        comment_ids += cursor.fetchall()
    
    # Loop through each member id and compile number of likes and dislikes for posts and comments made 
    total_member_likes = 0
    total_member_dislikes = 0


    if post_ids:
        for post_id in post_ids:

            p_id = post_id['id']

            # Get total likes for club posts
            cursor.execute('SELECT COUNT(id) FROM "clubPostsLikes" WHERE "postID" = %s', (p_id,))
            total_member_likes += cursor.fetchone()['count']

            # Get total dislikes for club posts
            cursor.execute('SELECT COUNT(id) FROM "clubPostsDislikes" WHERE "postID" = %s', (p_id,))
            total_member_dislikes += cursor.fetchone()['count']

    if comment_ids:
        for comment_id in comment_ids:

            c_id = comment_id['id']

            # Get total likes for club post comments
            cursor.execute('SELECT COUNT(id) FROM "clubPostCommentsLikes" WHERE "commentID" = %s', (c_id,))
            total_member_likes += cursor.fetchone()['count']

            # Get total dislikes for club post comments
            cursor.execute('SELECT COUNT(id) FROM "clubPostCommentsDislikes" WHERE "commentID" = %s', (c_id,))
            total_member_dislikes += cursor.fetchone()['count']
        

    # Get the proofPoints for upvotes and downvotes
    cursor.execute('SELECT "proofPoints" FROM "pointSystemRules" WHERE id = 8')
    upvote_points = cursor.fetchone()['proofPoints']

    cursor.execute('SELECT "proofPoints" FROM "pointSystemRules" WHERE id = 9')
    downvote_points = cursor.fetchone()['proofPoints']

    overall_total_upvotes = total_review_upvotes + total_producer_review_upvotes + total_venue_review_upvotes + total_member_likes
    overall_total_downvotes = total_review_downvotes + total_producer_review_downvotes + total_venue_review_downvotes + total_member_dislikes

    # Calculate total points
    total_points = user_points['currentPoints'] + (overall_total_upvotes * upvote_points) + (overall_total_downvotes * downvote_points)

    return total_points
    # Return the total points of the user
