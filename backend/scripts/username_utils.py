"""
Username utility functions for ensuring uniqueness across the application.

This module provides functions to generate unique usernames with collision prevention
by adding numeric suffixes when necessary.
"""

def generate_unique_username(base_username, cursor):
    """
    Generate a unique username by checking database and adding numeric suffixes for collisions.
    
    This function takes a pre-sanitized username and ensures it's unique in the producers table
    by adding numeric suffixes (01, 02, etc.) when collisions are detected.
    
    Args:
        base_username (str): The pre-sanitized base username to check for uniqueness
        cursor: Database cursor for checking uniqueness in producers table
        
    Returns:
        str: A unique username that doesn't exist in the producers table
        
    Raises:
        Exception: If unable to generate unique username after 99 attempts
        ValueError: If base_username is empty or None
        
    Examples:
        >>> generate_unique_username("macallan", cursor)
        "macallan"  # if available
        
        >>> generate_unique_username("macallan", cursor) 
        "macallan01"  # if "macallan" exists
        
        >>> generate_unique_username("macallan", cursor)
        "macallan02"  # if "macallan" and "macallan01" exist
    """
    if not base_username:
        raise ValueError("Base username cannot be empty or None")
    
    print(f"DEBUG: Checking uniqueness for base username: '{base_username}'")
    
    # Check if base username is available
    cursor.execute('SELECT COUNT(*) as count FROM "producers" WHERE "username" = %s', (base_username,))
    result = cursor.fetchone()
    
    if result['count'] == 0:
        print(f"DEBUG: Base username '{base_username}' is available")
        return base_username
    
    # Base username exists, try numbered variants
    print(f"DEBUG: Base username '{base_username}' exists, trying numbered variants")
    counter = 1
    while counter <= 99:
        candidate = f"{base_username}{counter:02d}"
        cursor.execute('SELECT COUNT(*) as count FROM "producers" WHERE "username" = %s', (candidate,))
        result = cursor.fetchone()
        
        if result['count'] == 0:
            print(f"DEBUG: Generated unique username '{candidate}'")
            return candidate
            
        counter += 1
    
    # If we reach here, we couldn't generate a unique username
    raise Exception(f"Unable to generate unique username for '{base_username}' after 99 attempts")
