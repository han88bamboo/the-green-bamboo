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
        return emoji + "Imperial"
    elif proof_points >= 400:
        return  emoji + "Over Proof"
    elif proof_points >= 200:
        return  emoji + "Full Proof"
    elif proof_points >= 101:
        return  emoji + "Aperitif"
    else:
        return  emoji + "Highball"


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


###############################################################################################################



