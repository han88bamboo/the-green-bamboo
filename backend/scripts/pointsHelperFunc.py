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
max_number_of_clubs = 1
min_points = 200

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

    # Check if the user has reached the minimum proof points to create a club
    if current_points['currentPoints'] >= min_points:
        
        # Check if the user has reached the maximum number of clubs they can create
        cur.execute('SELECT COUNT(*) FROM "clubs" WHERE "createdByID" = %s AND "createdByType" = %s', (user_id, 'user',))
        club_count = cur.fetchone()

        if not club_count and club_count['count'] < max_number_of_clubs:
            return (True)
        else:
            return (False, 'max clubs reached', max_number_of_clubs)
    else:
        return (False, 'insufficient points', min_points)



