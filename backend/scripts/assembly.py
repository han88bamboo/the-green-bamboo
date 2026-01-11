# Routes: /createAssembly (POST), /getAssemblies/<offset> (GET), /getAssemblywSearch/<offset>/<search> (GET),
#         /addAssemblyMembers (POST), /acceptAssemblyInvite (POST), /declineAssemblyInvite (DELETE),
#         /getUserInvitedAssemblies/<userID>/<userType> (GET), /getInvitedAssemblyMembers/<assemblyID>/<last_seen_id> (GET),
#         /getSpecificAssemblyInfo/<assemblyID> (GET), /getAssemblyPosts/<assemblyID>/<offset> (GET),
#         /getAssemblyMembers/<assemblyID>/<offset> (GET), /joinAssembly (POST), /leaveAssembly (DELETE),
#         /createAssemblyPost (POST), /voteAssemblyPost (PUT), /pinAssemblyPost (PUT),
#         /deleteAssemblyPost (DELETE), /editAssemblyPost (PUT), /removeAssemblyMember (DELETE)
# -----------------------------------------------------------------------------------------

import os
import re
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
    "Wine Enthusiasts 🍷" and "wine enthusiasts 🥂" would both become "wine enthusiasts"
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


def validate_assembly_name(name):
    """
    Validate assembly name:
    - Length: 4-50 characters
    - Character validation is done on frontend only
    - Backend only checks length and duplicate names
    Returns: (is_valid: bool, error_message: str or None)
    """
    if not name or len(name.strip()) < 4:
        return False, "Assembly name must be at least 4 characters."
    if len(name) > 50:
        return False, "Assembly name cannot exceed 50 characters."
    
    return True, None


def get_creator_info(cursor, creator_id, creator_type):
    """
    Get username, displayName, and photo for assembly creator.
    Returns dict with creatorUsername, creatorDisplayName, creatorPhoto or None if not found.
    
    Note: This function requires an existing cursor to be passed in.
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


def get_assembly_preview_posts(cursor, assembly_id, limit=3):
    """
    Get up to 3 recent posts with photos for assembly preview.
    Returns list of dicts with 'title' and 'photo' keys.
    """
    cursor.execute('''
        SELECT "postTitle" as "title", "postPhotos"[1] as "photo"
        FROM "assemblyPosts"
        WHERE "assemblyID" = %s
          AND "postPhotos" IS NOT NULL 
          AND array_length("postPhotos", 1) > 0
        ORDER BY "postDate" DESC
        LIMIT %s
    ''', (assembly_id, limit))
    
    results = cursor.fetchall()
    return [{'title': r['title'], 'photo': r['photo']} for r in results] if results else []


def get_user_info_by_id(cursor, user_id, user_type):
    """
    Retrieve user information using the user's ID and user type.
    Returns dict with id, displayName, photo, username, userType or None if not found.
    
    Note: This function requires an existing cursor to be passed in.
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


def get_member_user_info(cursor, member_id):
    """
    Get user info from an assemblyMembers record ID.
    Returns dict with user info or None if not found.
    
    Note: This function requires an existing cursor to be passed in.
    It reuses the cursor for the subsequent get_user_info_by_id call.
    """
    cursor.execute(
        'SELECT "userID", "userType" FROM "assemblyMembers" WHERE id = %s',
        (member_id,)
    )
    member = cursor.fetchone()
    if not member:
        return None
    
    return get_user_info_by_id(cursor, member['userID'], member['userType'])


# -----------------------------------------------------------------------------------------
# [POST] createAssembly
# Purpose: Create a new assembly, add creator as admin member, and send invitations to friends
# Used: CreateAssembly.vue
# Input:
#   1. creatorID - the user's ID in the 'users', 'producers' or 'venues' table
#   2. creatorType - 'user', 'producer' or 'venue'
#   3. assemblyName - name of the assembly (4-50 chars, emojis allowed)
#   4. assemblyDesc - description (optional, max 500 chars)
#   5. drinkTypes - array of drink types like ['Wine', 'Whisky'] (optional)
#   6. image64 - base64 banner image (optional)
#   7. invitedFriends - array of objects [{userID, userType}] to invite (optional)
# Output: Possible return codes:
#   201 - Assembly created successfully
#   400 - Validation error (missing data, invalid name, duplicate name)
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/createAssembly', methods=['POST'])
def create_assembly():
    try:
        data = request.get_json()
        
        # Get required fields
        creator_id = data.get('creatorID')
        creator_type = data.get('creatorType')
        assembly_name = data.get('assemblyName', '').strip()
        
        # Get optional fields
        assembly_desc = data.get('assemblyDesc', '').strip() or None
        drink_types = data.get('drinkTypes', [])  # Array of drink types
        invited_friends = data.get('invitedFriends', [])  # Array of {userID, userType} objects to invite
        
        # Validate description length (max 500 chars)
        if assembly_desc and len(assembly_desc) > 500:
            return jsonify({
                'code': 400,
                'message': 'Description cannot exceed 500 characters.'
            }), 400
        
        # Validate required fields
        if not creator_id or not creator_type:
            return jsonify({
                'code': 400,
                'message': 'Missing required fields: creatorID and creatorType are required.'
            }), 400
        
        if creator_type not in ['user', 'producer', 'venue']:
            return jsonify({
                'code': 400,
                'message': 'Invalid creatorType. Must be user, producer, or venue.'
            }), 400
        
        # Validate assembly name
        is_valid, error_message = validate_assembly_name(assembly_name)
        if not is_valid:
            return jsonify({
                'code': 400,
                'message': error_message
            }), 400
        
        # Normalize name for uniqueness check
        normalized_name = normalize_name_for_uniqueness(assembly_name)
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with db_manager.get_cursor() as cursor:
            # Check for duplicate assembly name (case-insensitive, ignoring emojis)
            # Using PostgreSQL regexp_replace to strip non-alphanumeric chars for comparison
            cursor.execute('''
                SELECT id FROM "assemblies" 
                WHERE LOWER(REGEXP_REPLACE("assemblyName", '[^\w\s]', '', 'g')) = %s
            ''', (normalized_name,))
            
            existing = cursor.fetchone()
            if existing:
                return jsonify({
                    'code': 400,
                    'data': {
                        'assemblyName': assembly_name
                    },
                    'message': 'An assembly with this name already exists.'
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
            
            # Step 1: Insert new assembly (totalMembers starts at 1 for the creator only)
            cursor.execute('''
                INSERT INTO "assemblies" 
                ("assemblyName", "assemblyDesc", "drinkTypes", "isInviteOnly", "assemblyBanner", 
                 "dateCreated", "totalMembers", "totalPosts", "createdByID", "createdByType")
                VALUES (%s, %s, %s, FALSE, %s, %s, 1, 0, %s, %s)
                RETURNING id
            ''', (assembly_name, assembly_desc, drink_types_array, banner_url, date_created, 
                  creator_id, creator_type))
            
            assembly_id = cursor.fetchone()['id']
            
            # Step 2: Add creator as admin member and get their memberID
            cursor.execute('''
                INSERT INTO "assemblyMembers" 
                ("assemblyID", "userID", "userType", "joinDate", "isAdmin")
                VALUES (%s, %s, %s, %s, TRUE)
                RETURNING id
            ''', (assembly_id, creator_id, creator_type, date_created))
            
            creator_member_id = cursor.fetchone()['id']
            
            # Step 3: Send invitations to friends (add to assemblyInvites, NOT assemblyMembers)
            if invited_friends and len(invited_friends) > 0:
                for friend in invited_friends:
                    # Support both old format (just ID) and new format ({userID, userType})
                    if isinstance(friend, dict):
                        friend_id = friend.get('userID')
                        friend_type = friend.get('userType', 'user')
                    else:
                        # Backwards compatibility: if just an ID is passed, assume 'user' type
                        friend_id = friend
                        friend_type = 'user'
                    
                    # Skip if no friend ID
                    if not friend_id:
                        continue
                    
                    # Verify the invitee exists
                    invitee_info = get_user_info_by_id(cursor, friend_id, friend_type)
                    if not invitee_info:
                        continue
                    
                    # Insert invite into assemblyInvites table
                    cursor.execute('''
                        INSERT INTO "assemblyInvites" 
                        ("assemblyID", "inviteeUserID", "inviteeUserType", "inviterMemberID", "inviteDate")
                        VALUES (%s, %s, %s, %s, %s)
                    ''', (assembly_id, friend_id, friend_type, creator_member_id, date_created))
                    
                    # Send notification to invitee
                    notification_data = {
                        "userId": friend_id,
                        "userType": friend_type,
                        "notiTabs": "forYou",
                        "notiType": "assembly_invite",
                        "image": None,
                        # TODO: Update link to specific assembly page once it's ready
                        # e.g., f"/assemblies/{assembly_id}/{assembly_name}"
                        "link": f"/assemblies",
                        "message": f"You have been invited to join '{assembly_name}' assembly",
                        "createdAt": current_time
                    }
                    try:
                        notifications.add_notification_to_db(notification_data, cursor)
                    except Exception as notif_error:
                        print(f"Failed to send assembly invite notification: {notif_error}")
        
        return jsonify({
            'code': 201,
            'data': {
                'assemblyID': assembly_id,
                'message': 'Assembly created successfully'
            }
        }), 201
    
    except Exception as e:
        print(f"Error creating assembly: {str(e)}")
        return jsonify({
            'code': 500,
            'message': 'An error occurred creating the assembly.'
        }), 500


# -----------------------------------------------------------------------------------------
# [GET] getAssemblies
# Purpose: Get paginated list of assemblies with creator info and preview posts
# Used: BrowseAssemblies.vue
# Input: offset (path param) - starting position (0, 12, 24, ...)
# Output: 
#   200 - List of assemblies with creator info and preview posts
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/getAssemblies/<offset>', methods=['GET'])
def get_assemblies(offset):
    try:
        offset = int(offset)
        limit = 12  # Fixed page size
        
        with db_manager.get_cursor() as cursor:
            # Main query with LEFT JOINs to get creator info
            cursor.execute('''
                SELECT 
                    a."id",
                    a."assemblyName",
                    a."assemblyDesc",
                    a."drinkTypes",
                    a."isInviteOnly",
                    a."assemblyBanner",
                    a."dateCreated",
                    a."totalMembers",
                    a."totalPosts",
                    a."createdByID",
                    a."createdByType",
                    CASE 
                        WHEN a."createdByType" = 'user' THEN u."username"
                        WHEN a."createdByType" = 'producer' THEN p."username"
                        WHEN a."createdByType" = 'venue' THEN v."username"
                    END as "creatorUsername",
                    CASE 
                        WHEN a."createdByType" = 'user' THEN u."displayName"
                        WHEN a."createdByType" = 'producer' THEN p."producerName"
                        WHEN a."createdByType" = 'venue' THEN v."venueName"
                    END as "creatorDisplayName",
                    CASE 
                        WHEN a."createdByType" = 'user' THEN u."photo"
                        WHEN a."createdByType" = 'producer' THEN p."photo"
                        WHEN a."createdByType" = 'venue' THEN v."photo"
                    END as "creatorPhoto"
                FROM "assemblies" a
                LEFT JOIN "users" u ON a."createdByType" = 'user' AND a."createdByID" = u."id"
                LEFT JOIN "producers" p ON a."createdByType" = 'producer' AND a."createdByID" = p."id"
                LEFT JOIN "venues" v ON a."createdByType" = 'venue' AND a."createdByID" = v."id"
                ORDER BY a."totalMembers" DESC, a."dateCreated" DESC
                LIMIT %s OFFSET %s
            ''', (limit, offset))
            
            assemblies = cursor.fetchall()
            
            if not assemblies:
                return jsonify({
                    'code': 200,
                    'data': [],
                    'message': 'No assemblies found'
                }), 200
            
            # Get preview posts for each assembly
            result = []
            for assembly in assemblies:
                assembly_dict = dict(assembly)
                assembly_dict['previewPosts'] = get_assembly_preview_posts(
                    cursor, assembly['id'], limit=3
                )
                result.append(assembly_dict)
        
        return jsonify({
            'code': 200,
            'data': result
        }), 200
    
    except Exception as e:
        print(f"Error getting assemblies: {str(e)}")
        return jsonify({
            'code': 500,
            'message': 'An error occurred retrieving assemblies.'
        }), 500


# -----------------------------------------------------------------------------------------
# [GET] getAssemblywSearch
# Purpose: Search assemblies by name or description with pagination
# Used: BrowseAssemblies.vue
# Input: 
#   offset (path param) - starting position
#   search (path param) - search term
# Output: 
#   200 - List of matching assemblies with creator info and preview posts
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/getAssemblywSearch/<offset>/<search>', methods=['GET'])
def get_assemblies_with_search(offset, search):
    try:
        offset = int(offset)
        limit = 12  # Fixed page size
        search_term = f'%{search}%'
        
        with db_manager.get_cursor() as cursor:
            # Main query with search filter and LEFT JOINs to get creator info
            cursor.execute('''
                SELECT 
                    a."id",
                    a."assemblyName",
                    a."assemblyDesc",
                    a."drinkTypes",
                    a."isInviteOnly",
                    a."assemblyBanner",
                    a."dateCreated",
                    a."totalMembers",
                    a."totalPosts",
                    a."createdByID",
                    a."createdByType",
                    CASE 
                        WHEN a."createdByType" = 'user' THEN u."username"
                        WHEN a."createdByType" = 'producer' THEN p."username"
                        WHEN a."createdByType" = 'venue' THEN v."username"
                    END as "creatorUsername",
                    CASE 
                        WHEN a."createdByType" = 'user' THEN u."displayName"
                        WHEN a."createdByType" = 'producer' THEN p."producerName"
                        WHEN a."createdByType" = 'venue' THEN v."venueName"
                    END as "creatorDisplayName",
                    CASE 
                        WHEN a."createdByType" = 'user' THEN u."photo"
                        WHEN a."createdByType" = 'producer' THEN p."photo"
                        WHEN a."createdByType" = 'venue' THEN v."photo"
                    END as "creatorPhoto"
                FROM "assemblies" a
                LEFT JOIN "users" u ON a."createdByType" = 'user' AND a."createdByID" = u."id"
                LEFT JOIN "producers" p ON a."createdByType" = 'producer' AND a."createdByID" = p."id"
                LEFT JOIN "venues" v ON a."createdByType" = 'venue' AND a."createdByID" = v."id"
                WHERE (a."assemblyName" ILIKE %s OR a."assemblyDesc" ILIKE %s)
                ORDER BY a."totalMembers" DESC, a."dateCreated" DESC
                LIMIT %s OFFSET %s
            ''', (search_term, search_term, limit, offset))
            
            assemblies = cursor.fetchall()
            
            if not assemblies:
                return jsonify({
                    'code': 200,
                    'data': [],
                    'message': 'No assemblies found matching your search'
                }), 200
            
            # Get preview posts for each assembly
            result = []
            for assembly in assemblies:
                assembly_dict = dict(assembly)
                assembly_dict['previewPosts'] = get_assembly_preview_posts(
                    cursor, assembly['id'], limit=3
                )
                result.append(assembly_dict)
        
        return jsonify({
            'code': 200,
            'data': result
        }), 200
    
    except Exception as e:
        print(f"Error searching assemblies: {str(e)}")
        return jsonify({
            'code': 500,
            'message': 'An error occurred searching assemblies.'
        }), 500


# -----------------------------------------------------------------------------------------
# [POST] addAssemblyMembers
# Purpose: Invite new members to join the assembly (adds to assemblyInvites, not assemblyMembers)
#          Any existing member can invite friends. Invitees must accept to become members.
# Used: SpecificAssembly.vue (future), AssemblySettings.vue (future)
# Input:
#   1. assemblyID - the assembly to invite members to
#   2. inviterMemberID - the assemblyMembers.id of the person sending invites
#   3. newMembers - array of objects [{userID, userType}] to invite
# Output: Possible return codes:
#   201 - Invitations sent successfully
#   400 - Missing required data or no valid members to invite
#   404 - Assembly or inviter not found
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/addAssemblyMembers', methods=['POST'])
def add_assembly_members():
    try:
        data = request.get_json()
        
        assembly_id = data.get('assemblyID')
        inviter_member_id = data.get('inviterMemberID')
        new_members = data.get('newMembers', [])
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if not assembly_id:
            return jsonify({
                'code': 400,
                'message': 'Missing required data: assemblyID is required.'
            }), 400
        
        if not inviter_member_id:
            return jsonify({
                'code': 400,
                'message': 'Missing required data: inviterMemberID is required.'
            }), 400
        
        if not new_members or len(new_members) == 0:
            return jsonify({
                'code': 400,
                'message': 'No new members to invite.'
            }), 400
        
        with db_manager.get_cursor() as cursor:
            # Step 1: Check if the assembly exists
            cursor.execute('SELECT * FROM "assemblies" WHERE id = %s', (assembly_id,))
            assembly = cursor.fetchone()
            
            if not assembly:
                return jsonify({
                    'code': 404,
                    'message': 'Assembly not found.'
                }), 404
            
            assembly_name = assembly['assemblyName']
            
            # Step 2: Verify the inviter is a member
            cursor.execute(
                'SELECT * FROM "assemblyMembers" WHERE id = %s AND "assemblyID" = %s',
                (inviter_member_id, assembly_id)
            )
            inviter = cursor.fetchone()
            
            if not inviter:
                return jsonify({
                    'code': 404,
                    'message': 'Inviter is not a member of this assembly.'
                }), 404
            
            invite_date = datetime.now()
            invites_sent = 0
            
            # Step 3: Process each invite
            for member in new_members:
                user_id = member.get('userID')
                user_type = member.get('userType', 'user')
                
                if not user_id:
                    continue
                
                # Verify the invitee exists
                invitee_info = get_user_info_by_id(cursor, user_id, user_type)
                if not invitee_info:
                    continue
                
                # Check if user is already a member
                cursor.execute('''
                    SELECT id FROM "assemblyMembers" 
                    WHERE "assemblyID" = %s AND "userID" = %s AND "userType" = %s
                ''', (assembly_id, user_id, user_type))
                if cursor.fetchone():
                    continue  # Skip, already a member
                
                # Check if user already has a pending invite
                cursor.execute('''
                    SELECT id FROM "assemblyInvites" 
                    WHERE "assemblyID" = %s AND "inviteeUserID" = %s AND "inviteeUserType" = %s
                ''', (assembly_id, user_id, user_type))
                if cursor.fetchone():
                    continue  # Skip, already invited
                
                # Insert the invite
                cursor.execute('''
                    INSERT INTO "assemblyInvites" 
                    ("assemblyID", "inviteeUserID", "inviteeUserType", "inviterMemberID", "inviteDate")
                    VALUES (%s, %s, %s, %s, %s)
                ''', (assembly_id, user_id, user_type, inviter_member_id, invite_date))
                
                invites_sent += 1
                
                # Send notification to invitee
                notification_data = {
                    "userId": user_id,
                    "userType": user_type,
                    "notiTabs": "forYou",
                    "notiType": "assembly_invite",
                    "image": None,
                    # TODO: Update link to specific assembly page once it's ready
                    "link": f"/assemblies",
                    "message": f"You have been invited to join '{assembly_name}' assembly",
                    "createdAt": current_time
                }
                try:
                    notifications.add_notification_to_db(notification_data, cursor)
                except Exception as notif_error:
                    print(f"Failed to send assembly invite notification: {notif_error}")
        
        if invites_sent == 0:
            return jsonify({
                'code': 400,
                'message': 'No valid members to invite (all may already be members or have pending invites).'
            }), 400
        
        return jsonify({
            'code': 201,
            'message': f'Successfully sent {invites_sent} invitation(s).'
        }), 201
    
    except Exception as e:
        print(f"Error adding assembly members: {str(e)}")
        return jsonify({
            'code': 500,
            'message': 'An error occurred sending invitations.'
        }), 500


# -----------------------------------------------------------------------------------------
# [POST] acceptAssemblyInvite
# Purpose: Accept an invitation to join an assembly. In one transaction:
#          - Removes the invite from assemblyInvites
#          - Adds the user to assemblyMembers
#          - Updates totalMembers count
#          - Sends notification to the person who sent the invite
# Used: BrowseAssemblies.vue, SpecificAssembly.vue (future)
# Input:
#   1. userID - the user accepting the invite
#   2. userType - 'user', 'producer', or 'venue'
#   3. assemblyID - the assembly to join
# Output: Possible return codes:
#   201 - Successfully joined the assembly
#   400 - Missing required data
#   404 - Assembly/user not found or user not invited
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/acceptAssemblyInvite', methods=['POST'])
def accept_assembly_invite():
    try:
        data = request.get_json()
        
        user_id = data.get('userID')
        user_type = data.get('userType')
        assembly_id = data.get('assemblyID')
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if not user_id or not user_type or not assembly_id:
            return jsonify({
                'code': 400,
                'message': 'Missing required data: userID, userType, and assemblyID are required.'
            }), 400
        
        with db_manager.get_cursor() as cursor:
            # Step 1: Check if the assembly exists
            cursor.execute('SELECT * FROM "assemblies" WHERE id = %s', (assembly_id,))
            assembly = cursor.fetchone()
            
            if not assembly:
                return jsonify({
                    'code': 404,
                    'message': 'Assembly not found.'
                }), 404
            
            assembly_name = assembly['assemblyName']
            
            # Step 2: Check if the user exists
            user_info = get_user_info_by_id(cursor, user_id, user_type)
            if not user_info:
                return jsonify({
                    'code': 404,
                    'message': 'User not found.'
                }), 404
            
            # Step 3: Check if the user has been invited
            cursor.execute('''
                SELECT * FROM "assemblyInvites" 
                WHERE "assemblyID" = %s AND "inviteeUserID" = %s AND "inviteeUserType" = %s
            ''', (assembly_id, user_id, user_type))
            invite = cursor.fetchone()
            
            if not invite:
                return jsonify({
                    'code': 404,
                    'message': 'You have not been invited to this assembly.'
                }), 404
            
            inviter_member_id = invite['inviterMemberID']
            join_date = datetime.now()
            
            # Step 4: Remove the invite from assemblyInvites
            cursor.execute('''
                DELETE FROM "assemblyInvites" 
                WHERE "assemblyID" = %s AND "inviteeUserID" = %s AND "inviteeUserType" = %s
            ''', (assembly_id, user_id, user_type))
            
            # Step 5: Add the user to assemblyMembers
            cursor.execute('''
                INSERT INTO "assemblyMembers" 
                ("assemblyID", "userID", "userType", "joinDate", "isAdmin")
                VALUES (%s, %s, %s, %s, FALSE)
            ''', (assembly_id, user_id, user_type, join_date))
            
            # Step 6: Update totalMembers count
            cursor.execute('''
                UPDATE "assemblies" SET "totalMembers" = "totalMembers" + 1 WHERE id = %s
            ''', (assembly_id,))
            
            # Step 7: Send notification to the person who sent the invite
            if inviter_member_id:
                inviter_info = get_member_user_info(cursor, inviter_member_id)
                if inviter_info:
                    # Get the username of the person who accepted
                    accepter_username = user_info.get('username', 'Someone')
                    
                    notification_data = {
                        "userId": inviter_info['id'],
                        "userType": inviter_info['userType'],
                        "notiTabs": "forYou",
                        "notiType": "assembly_join",
                        "image": None,
                        # TODO: Update link to specific assembly page once it's ready
                        "link": f"/assemblies",
                        "message": f"@{accepter_username} accepted your invitation to join '{assembly_name}' assembly",
                        "createdAt": current_time
                    }
                    try:
                        notifications.add_notification_to_db(notification_data, cursor)
                    except Exception as notif_error:
                        print(f"Failed to send assembly join notification: {notif_error}")
        
        return jsonify({
            'code': 201,
            'message': 'Successfully joined the assembly.'
        }), 201
    
    except Exception as e:
        print(f"Error accepting assembly invite: {str(e)}")
        return jsonify({
            'code': 500,
            'message': 'An error occurred joining the assembly.'
        }), 500


# -----------------------------------------------------------------------------------------
# [DELETE] declineAssemblyInvite
# Purpose: Decline/reject an invitation to join an assembly
# Used: BrowseAssemblies.vue, SpecificAssembly.vue (future)
# Input:
#   1. userID - the user declining the invite
#   2. userType - 'user', 'producer', or 'venue'
#   3. assemblyID - the assembly invitation to decline
# Output: Possible return codes:
#   200 - Invite declined successfully
#   400 - Missing required data
#   404 - No such invite found
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/declineAssemblyInvite', methods=['DELETE'])
def decline_assembly_invite():
    try:
        data = request.get_json()
        
        user_id = data.get('userID')
        user_type = data.get('userType')
        assembly_id = data.get('assemblyID')
        
        if not user_id or not user_type or not assembly_id:
            return jsonify({
                'code': 400,
                'message': 'Missing required data: userID, userType, and assemblyID are required.'
            }), 400
        
        with db_manager.get_cursor() as cursor:
            # Check if the invite exists
            cursor.execute('''
                SELECT * FROM "assemblyInvites" 
                WHERE "assemblyID" = %s AND "inviteeUserID" = %s AND "inviteeUserType" = %s
            ''', (assembly_id, user_id, user_type))
            invite = cursor.fetchone()
            
            if not invite:
                return jsonify({
                    'code': 404,
                    'message': 'No invitation found for this assembly.'
                }), 404
            
            # Remove the invite
            cursor.execute('''
                DELETE FROM "assemblyInvites" 
                WHERE "assemblyID" = %s AND "inviteeUserID" = %s AND "inviteeUserType" = %s
            ''', (assembly_id, user_id, user_type))
        
        return jsonify({
            'code': 200,
            'message': 'Invitation declined successfully.'
        }), 200
    
    except Exception as e:
        print(f"Error declining assembly invite: {str(e)}")
        return jsonify({
            'code': 500,
            'message': 'An error occurred declining the invitation.'
        }), 500


# -----------------------------------------------------------------------------------------
# [GET] getUserInvitedAssemblies
# Purpose: Get a list of assemblies that a specific user has been invited to join
# Used: BrowseAssemblies.vue
# Input: userID, userType (path params)
# Output: Possible return codes:
#   200 - List of invited assemblies (may be empty)
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/getUserInvitedAssemblies/<userID>/<userType>', methods=['GET'])
def get_user_invited_assemblies(userID, userType):
    try:
        with db_manager.get_cursor() as cursor:
            # Get all pending invites for this user
            cursor.execute('''
                SELECT * FROM "assemblyInvites" 
                WHERE "inviteeUserID" = %s AND "inviteeUserType" = %s
            ''', (userID, userType))
            invites = cursor.fetchall()
            
            if not invites:
                return jsonify({
                    'code': 200,
                    'data': [],
                    'message': 'No pending invitations.'
                }), 200
            
            result = []
            for invite in invites:
                invite_dict = dict(invite)
                
                # Get assembly info
                cursor.execute('''
                    SELECT "id", "assemblyName", "assemblyDesc", "assemblyBanner", "totalMembers"
                    FROM "assemblies" WHERE id = %s
                ''', (invite['assemblyID'],))
                assembly = cursor.fetchone()
                
                if assembly:
                    invite_dict['assemblyInfo'] = dict(assembly)
                
                # Get inviter info
                if invite['inviterMemberID']:
                    inviter_info = get_member_user_info(cursor, invite['inviterMemberID'])
                    if inviter_info:
                        invite_dict['inviterInfo'] = inviter_info
                
                result.append(invite_dict)
            
            return jsonify({
                'code': 200,
                'data': result
            }), 200
    
    except Exception as e:
        print(f"Error getting user invited assemblies: {str(e)}")
        return jsonify({
            'code': 500,
            'message': 'An error occurred retrieving invitations.'
        }), 500


# -----------------------------------------------------------------------------------------
# [GET] getInvitedAssemblyMembers
# Purpose: Get the list of users who have been invited to join a specific assembly (pending invites)
#          Used by assembly admins to see pending invitations
# Used: AssemblySettings.vue (future)
# Input: assemblyID, last_seen_id (path params) - for pagination
#        last_seen_id: '0' for first page DESC, '1' for first page ASC, otherwise cursor-based
# Output: Possible return codes:
#   200 - List of pending invites
#   404 - No invites found
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/getInvitedAssemblyMembers/<assemblyID>/<last_seen_id>', methods=['GET'])
def get_invited_assembly_members(assemblyID, last_seen_id):
    try:
        limit = 10  # Number of results per page
        
        with db_manager.get_cursor() as cursor:
            # Paginated query
            if last_seen_id == '0':
                cursor.execute('''
                    SELECT * FROM "assemblyInvites" 
                    WHERE "assemblyID" = %s 
                    ORDER BY "id" DESC LIMIT %s
                ''', (assemblyID, limit))
            elif last_seen_id == '1':
                cursor.execute('''
                    SELECT * FROM "assemblyInvites" 
                    WHERE "assemblyID" = %s 
                    LIMIT %s
                ''', (assemblyID, limit))
            else:
                cursor.execute('''
                    SELECT * FROM "assemblyInvites" 
                    WHERE "assemblyID" = %s AND "id" < %s 
                    ORDER BY "id" DESC LIMIT %s
                ''', (assemblyID, last_seen_id, limit))
            
            invites = cursor.fetchall()
            
            if not invites:
                return jsonify({
                    'code': 404,
                    'message': 'No pending invites found.'
                }), 404
            
            result = []
            for invite in invites:
                invite_dict = dict(invite)
                
                # Get invitee info
                invitee_info = get_user_info_by_id(
                    cursor, 
                    invite['inviteeUserID'], 
                    invite['inviteeUserType']
                )
                if invitee_info:
                    invite_dict['inviteeInfo'] = invitee_info
                
                # Get inviter info
                if invite['inviterMemberID']:
                    inviter_info = get_member_user_info(cursor, invite['inviterMemberID'])
                    if inviter_info:
                        invite_dict['inviterInfo'] = inviter_info
                
                result.append(invite_dict)
            
            return jsonify({
                'code': 200,
                'data': result
            }), 200
    
    except Exception as e:
        print(f"Error getting invited assembly members: {str(e)}")
        return jsonify({
            'code': 500,
            'message': 'An error occurred retrieving pending invites.'
        }), 500


# -----------------------------------------------------------------------------------------
# [GET] getSpecificAssemblyInfo
# Purpose: Get detailed information about a specific assembly including:
#          - Assembly details (name, desc, banner, drinkTypes, etc.)
#          - Creator info
#          - Member count and post count
#          - Whether the current user is a member
#          - User's memberID if they are a member
#          - First few members for preview
# Used: SpecificAssembly.vue
# Input: assemblyID (path param), userID (query param, optional), userType (query param, optional)
# Output: Possible return codes:
#   200 - Assembly info retrieved successfully
#   404 - Assembly not found
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/getSpecificAssemblyInfo/<assemblyID>', methods=['GET'])
def get_specific_assembly_info(assemblyID):
    try:
        # Get optional user info from query params
        user_id = request.args.get('userID')
        user_type = request.args.get('userType')
        
        with db_manager.get_cursor() as cursor:
            # Step 1: Get the assembly information
            cursor.execute('''
                SELECT 
                    a."id",
                    a."assemblyName",
                    a."assemblyDesc",
                    a."drinkTypes",
                    a."isInviteOnly",
                    a."assemblyBanner",
                    a."dateCreated",
                    a."totalMembers",
                    a."totalPosts",
                    a."createdByID",
                    a."createdByType"
                FROM "assemblies" a
                WHERE a."id" = %s
            ''', (assemblyID,))
            
            assembly = cursor.fetchone()
            
            if not assembly:
                return jsonify({
                    'code': 404,
                    'message': 'Assembly not found.'
                }), 404
            
            assembly_dict = dict(assembly)
            
            # Step 2: Get creator info
            creator_info = get_creator_info(cursor, assembly['createdByID'], assembly['createdByType'])
            if creator_info:
                assembly_dict.update(creator_info)
            
            # Step 3: Check if user is a member and get their memberID
            assembly_dict['isMember'] = False
            assembly_dict['memberID'] = None
            assembly_dict['isAdmin'] = False
            
            if user_id and user_type:
                cursor.execute('''
                    SELECT id, "isAdmin" FROM "assemblyMembers" 
                    WHERE "assemblyID" = %s AND "userID" = %s AND "userType" = %s
                ''', (assemblyID, user_id, user_type))
                membership = cursor.fetchone()
                
                if membership:
                    assembly_dict['isMember'] = True
                    assembly_dict['memberID'] = membership['id']
                    assembly_dict['isAdmin'] = membership['isAdmin']
            
            # Step 4: Get first 8 members for preview (like ClubView)
            cursor.execute('''
                SELECT am.id, am."userID", am."userType", am."isAdmin", am."joinDate"
                FROM "assemblyMembers" am
                WHERE am."assemblyID" = %s
                ORDER BY am."isAdmin" DESC, am."joinDate" ASC
                LIMIT 8
            ''', (assemblyID,))
            
            members_preview = cursor.fetchall()
            member_preview_list = []
            
            for member in members_preview:
                member_dict = dict(member)
                member_info = get_user_info_by_id(cursor, member['userID'], member['userType'])
                if member_info:
                    member_dict['userInfo'] = member_info
                    member_preview_list.append(member_dict)
            
            assembly_dict['membersPreview'] = member_preview_list
            
            # Step 5: Get admin list
            cursor.execute('''
                SELECT am.id, am."userID", am."userType"
                FROM "assemblyMembers" am
                WHERE am."assemblyID" = %s AND am."isAdmin" = TRUE
            ''', (assemblyID,))
            
            admins = cursor.fetchall()
            admin_list = []
            
            for admin in admins:
                admin_info = get_user_info_by_id(cursor, admin['userID'], admin['userType'])
                if admin_info:
                    admin_info['memberID'] = admin['id']
                    admin_list.append(admin_info)
            
            assembly_dict['admins'] = admin_list
            
            return jsonify({
                'code': 200,
                'data': assembly_dict
            }), 200
    
    except Exception as e:
        print(f"Error getting specific assembly info: {str(e)}")
        return jsonify({
            'code': 500,
            'message': 'An error occurred retrieving assembly info.'
        }), 500


# -----------------------------------------------------------------------------------------
# [GET] getAssemblyPosts
# Purpose: Get paginated posts for an assembly with vote counts and comment previews
# Used: SpecificAssembly.vue
# Input: 
#   assemblyID (path param)
#   offset (path param) - for pagination (0, 25, 50, ...)
#   userID (query param, optional) - to check if user voted
#   userType (query param, optional)
#   sortBy (query param, optional) - 'newest' (default) or 'top' (by vote count)
# Output: 
#   200 - List of posts with poster info, vote counts, comment previews
#   404 - No posts found
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/getAssemblyPosts/<assemblyID>/<offset>', methods=['GET'])
def get_assembly_posts(assemblyID, offset):
    try:
        offset = int(offset)
        limit = 25  # Reddit-style page size
        
        # Get optional user info from query params
        user_id = request.args.get('userID')
        user_type = request.args.get('userType')
        sort_by = request.args.get('sortBy', 'newest')  # 'newest' or 'top'
        member_id = None
        
        with db_manager.get_cursor() as cursor:
            # Get user's memberID if logged in
            if user_id and user_type:
                cursor.execute('''
                    SELECT id FROM "assemblyMembers" 
                    WHERE "assemblyID" = %s AND "userID" = %s AND "userType" = %s
                ''', (assemblyID, user_id, user_type))
                member_record = cursor.fetchone()
                if member_record:
                    member_id = member_record['id']
            
            # Build ORDER BY clause based on sortBy parameter
            # Pinned posts always come first regardless of sort
            if sort_by == 'top':
                # Sort by vote count (likes - dislikes)
                order_clause = '''
                    ORDER BY ap."isPinned" DESC,
                    (SELECT COUNT(*) FROM "assemblyPostsLikes" WHERE "postID" = ap."id") -
                    (SELECT COUNT(*) FROM "assemblyPostsDislikes" WHERE "postID" = ap."id") DESC,
                    ap."postDate" DESC
                '''
            else:  # 'newest' or default
                # Sort by date (newest first)
                order_clause = 'ORDER BY ap."isPinned" DESC, ap."postDate" DESC'
            
            # Get posts with dynamic ordering
            query = f'''
                SELECT 
                    ap."id",
                    ap."assemblyID",
                    ap."postTitle",
                    ap."postContent",
                    ap."postPhotos",
                    ap."listingIDs",
                    ap."isPinned",
                    ap."postDate",
                    ap."posterID",
                    ap."editedAt"
                FROM "assemblyPosts" ap
                WHERE ap."assemblyID" = %s
                {order_clause}
                LIMIT %s OFFSET %s
            '''
            
            cursor.execute(query, (assemblyID, limit, offset))
            
            posts = cursor.fetchall()
            
            if not posts:
                return jsonify({
                    'code': 200,
                    'data': [],
                    'message': 'No posts found.'
                }), 200
            
            result = []
            
            for post in posts:
                post_dict = dict(post)
                post_id = post['id']
                poster_id = post['posterID']
                
                # Truncate content to 200 chars
                if post_dict['postContent']:
                    if len(post_dict['postContent']) > 200:
                        post_dict['postContentPreview'] = post_dict['postContent'][:200] + '...'
                    else:
                        post_dict['postContentPreview'] = post_dict['postContent']
                else:
                    post_dict['postContentPreview'] = ''
                
                # Get poster info
                if poster_id:
                    poster_info = get_member_user_info(cursor, poster_id)
                    if poster_info:
                        post_dict['posterInfo'] = poster_info
                
                # Get vote counts
                cursor.execute('SELECT COUNT(*) as count FROM "assemblyPostsLikes" WHERE "postID" = %s', (post_id,))
                likes = cursor.fetchone()['count']
                
                cursor.execute('SELECT COUNT(*) as count FROM "assemblyPostsDislikes" WHERE "postID" = %s', (post_id,))
                dislikes = cursor.fetchone()['count']
                
                post_dict['voteCount'] = likes - dislikes
                post_dict['likeCount'] = likes
                post_dict['dislikeCount'] = dislikes
                
                # Get user's vote status if they are a member
                post_dict['userVote'] = None
                if member_id:
                    cursor.execute('''
                        SELECT id FROM "assemblyPostsLikes" 
                        WHERE "postID" = %s AND "memberID" = %s
                    ''', (post_id, member_id))
                    if cursor.fetchone():
                        post_dict['userVote'] = 'up'
                    else:
                        cursor.execute('''
                            SELECT id FROM "assemblyPostsDislikes" 
                            WHERE "postID" = %s AND "memberID" = %s
                        ''', (post_id, member_id))
                        if cursor.fetchone():
                            post_dict['userVote'] = 'down'
                
                # Get comment count
                cursor.execute('SELECT COUNT(*) as count FROM "assemblyPostComments" WHERE "postID" = %s', (post_id,))
                post_dict['commentCount'] = cursor.fetchone()['count']
                
                # Get top 2 comments preview (by likes, then by date)
                cursor.execute('''
                    SELECT 
                        apc."id",
                        apc."commentContent",
                        apc."commentDate",
                        apc."commenterID",
                        (SELECT COUNT(*) FROM "assemblyPostCommentsLikes" WHERE "commentID" = apc."id") as likes,
                        (SELECT COUNT(*) FROM "assemblyPostCommentsDislikes" WHERE "commentID" = apc."id") as dislikes
                    FROM "assemblyPostComments" apc
                    WHERE apc."postID" = %s AND apc."parentCommentID" IS NULL
                    ORDER BY (
                        (SELECT COUNT(*) FROM "assemblyPostCommentsLikes" WHERE "commentID" = apc."id") -
                        (SELECT COUNT(*) FROM "assemblyPostCommentsDislikes" WHERE "commentID" = apc."id")
                    ) DESC, apc."commentDate" DESC
                    LIMIT 2
                ''', (post_id,))
                
                top_comments = cursor.fetchall()
                comments_preview = []
                
                for comment in top_comments:
                    comment_dict = dict(comment)
                    # Truncate comment to 100 chars
                    if comment_dict['commentContent'] and len(comment_dict['commentContent']) > 100:
                        comment_dict['commentContent'] = comment_dict['commentContent'][:100] + '...'
                    
                    # Get commenter info
                    if comment['commenterID']:
                        commenter_info = get_member_user_info(cursor, comment['commenterID'])
                        if commenter_info:
                            comment_dict['commenterInfo'] = commenter_info
                    
                    comment_dict['voteCount'] = comment['likes'] - comment['dislikes']
                    comments_preview.append(comment_dict)
                
                post_dict['commentsPreview'] = comments_preview
                
                # Get linked listings info if any
                if post_dict['listingIDs'] and len(post_dict['listingIDs']) > 0:
                    listings_info = []
                    for listing_id in post_dict['listingIDs'][:3]:  # Limit to 3 for preview
                        cursor.execute('''
                            SELECT "id", "listingName", "photo" 
                            FROM "listings" WHERE "id" = %s
                        ''', (listing_id,))
                        listing = cursor.fetchone()
                        if listing:
                            listings_info.append(dict(listing))
                    post_dict['linkedListings'] = listings_info
                
                result.append(post_dict)
            
            return jsonify({
                'code': 200,
                'data': result
            }), 200
    
    except Exception as e:
        print(f"Error getting assembly posts: {str(e)}")
        return jsonify({
            'code': 500,
            'message': 'An error occurred retrieving posts.'
        }), 500


# -----------------------------------------------------------------------------------------
# [GET] getAssemblyMembers
# Purpose: Get paginated list of all members in an assembly
# Used: SpecificAssembly.vue (members modal)
# Input: assemblyID (path param), offset (path param)
# Output: 
#   200 - List of members with user info
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/getAssemblyMembers/<assemblyID>/<offset>', methods=['GET'])
def get_assembly_members(assemblyID, offset):
    try:
        offset = int(offset)
        limit = 20
        
        with db_manager.get_cursor() as cursor:
            cursor.execute('''
                SELECT am.id, am."userID", am."userType", am."isAdmin", am."joinDate"
                FROM "assemblyMembers" am
                WHERE am."assemblyID" = %s
                ORDER BY am."isAdmin" DESC, am."joinDate" ASC
                LIMIT %s OFFSET %s
            ''', (assemblyID, limit, offset))
            
            members = cursor.fetchall()
            
            result = []
            for member in members:
                member_dict = dict(member)
                member_info = get_user_info_by_id(cursor, member['userID'], member['userType'])
                if member_info:
                    member_dict['userInfo'] = member_info
                    result.append(member_dict)
            
            return jsonify({
                'code': 200,
                'data': result
            }), 200
    
    except Exception as e:
        print(f"Error getting assembly members: {str(e)}")
        return jsonify({
            'code': 500,
            'message': 'An error occurred retrieving members.'
        }), 500


# -----------------------------------------------------------------------------------------
# [POST] joinAssembly
# Purpose: Join a public assembly (instant join, no approval needed)
# Used: SpecificAssembly.vue
# Input:
#   1. assemblyID - the assembly to join
#   2. userID - the user's ID
#   3. userType - 'user', 'producer', or 'venue'
# Output: Possible return codes:
#   201 - Successfully joined
#   400 - Missing data or already a member
#   404 - Assembly not found
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/joinAssembly', methods=['POST'])
def join_assembly():
    try:
        data = request.get_json()
        
        assembly_id = data.get('assemblyID')
        user_id = data.get('userID')
        user_type = data.get('userType')
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if not assembly_id or not user_id or not user_type:
            return jsonify({
                'code': 400,
                'message': 'Missing required data: assemblyID, userID, and userType are required.'
            }), 400
        
        with db_manager.get_cursor() as cursor:
            # Check if assembly exists
            cursor.execute('SELECT * FROM "assemblies" WHERE id = %s', (assembly_id,))
            assembly = cursor.fetchone()
            
            if not assembly:
                return jsonify({
                    'code': 404,
                    'message': 'Assembly not found.'
                }), 404
            
            assembly_name = assembly['assemblyName']
            
            # Check if user exists
            user_info = get_user_info_by_id(cursor, user_id, user_type)
            if not user_info:
                return jsonify({
                    'code': 404,
                    'message': 'User not found.'
                }), 404
            
            # Check if already a member
            cursor.execute('''
                SELECT id FROM "assemblyMembers" 
                WHERE "assemblyID" = %s AND "userID" = %s AND "userType" = %s
            ''', (assembly_id, user_id, user_type))
            
            if cursor.fetchone():
                return jsonify({
                    'code': 400,
                    'message': 'You are already a member of this assembly.'
                }), 400
            
            # Add as member
            join_date = datetime.now()
            cursor.execute('''
                INSERT INTO "assemblyMembers" 
                ("assemblyID", "userID", "userType", "joinDate", "isAdmin")
                VALUES (%s, %s, %s, %s, FALSE)
                RETURNING id
            ''', (assembly_id, user_id, user_type, join_date))
            
            member_id = cursor.fetchone()['id']
            
            # Update total members count
            cursor.execute('''
                UPDATE "assemblies" SET "totalMembers" = "totalMembers" + 1 WHERE id = %s
            ''', (assembly_id,))
            
            # Send notification to assembly creator
            creator_id = assembly['createdByID']
            creator_type = assembly['createdByType']
            
            joiner_username = user_info.get('username', 'Someone')
            
            notification_data = {
                "userId": creator_id,
                "userType": creator_type,
                "notiTabs": "forYou",
                "notiType": "assembly_join",
                "image": None,
                "link": f"/assemblies/{assembly_id}/{assembly_name.replace(' ', '-').lower()}",
                "message": f"@{joiner_username} joined your assembly: {assembly_name}",
                "createdAt": current_time
            }
            try:
                notifications.add_notification_to_db(notification_data, cursor)
            except Exception as notif_error:
                print(f"Failed to send assembly join notification: {notif_error}")
        
        return jsonify({
            'code': 201,
            'data': {'memberID': member_id},
            'message': 'Successfully joined the assembly.'
        }), 201
    
    except Exception as e:
        print(f"Error joining assembly: {str(e)}")
        return jsonify({
            'code': 500,
            'message': 'An error occurred joining the assembly.'
        }), 500


# -----------------------------------------------------------------------------------------
# [DELETE] leaveAssembly
# Purpose: Leave an assembly
# Used: SpecificAssembly.vue
# Input:
#   1. assemblyID - the assembly to leave
#   2. userID - the user's ID
#   3. userType - 'user', 'producer', or 'venue'
# Output: Possible return codes:
#   200 - Successfully left
#   400 - Missing data or not a member
#   403 - Cannot leave (last admin or creator)
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/leaveAssembly', methods=['DELETE'])
def leave_assembly():
    try:
        data = request.get_json()
        
        assembly_id = data.get('assemblyID')
        user_id = data.get('userID')
        user_type = data.get('userType')
        
        if not assembly_id or not user_id or not user_type:
            return jsonify({
                'code': 400,
                'message': 'Missing required data: assemblyID, userID, and userType are required.'
            }), 400
        
        with db_manager.get_cursor() as cursor:
            # Check if user is a member
            cursor.execute('''
                SELECT id, "isAdmin" FROM "assemblyMembers" 
                WHERE "assemblyID" = %s AND "userID" = %s AND "userType" = %s
            ''', (assembly_id, user_id, user_type))
            
            membership = cursor.fetchone()
            
            if not membership:
                return jsonify({
                    'code': 400,
                    'message': 'You are not a member of this assembly.'
                }), 400
            
            # Check if user is the creator (creator cannot leave)
            cursor.execute('''
                SELECT "createdByID", "createdByType" FROM "assemblies" WHERE id = %s
            ''', (assembly_id,))
            assembly = cursor.fetchone()
            
            if assembly and assembly['createdByID'] == int(user_id) and assembly['createdByType'] == user_type:
                return jsonify({
                    'code': 403,
                    'message': 'Assembly creator cannot leave. Transfer ownership or delete the assembly instead.'
                }), 403
            
            # If admin, check if they're the last admin
            if membership['isAdmin']:
                cursor.execute('''
                    SELECT COUNT(*) as count FROM "assemblyMembers" 
                    WHERE "assemblyID" = %s AND "isAdmin" = TRUE
                ''', (assembly_id,))
                admin_count = cursor.fetchone()['count']
                
                if admin_count <= 1:
                    return jsonify({
                        'code': 403,
                        'message': 'Cannot leave: you are the last admin. Promote another member to admin first.'
                    }), 403
            
            # Remove membership
            cursor.execute('''
                DELETE FROM "assemblyMembers" 
                WHERE "assemblyID" = %s AND "userID" = %s AND "userType" = %s
            ''', (assembly_id, user_id, user_type))
            
            # Update total members count
            cursor.execute('''
                UPDATE "assemblies" SET "totalMembers" = "totalMembers" - 1 WHERE id = %s
            ''', (assembly_id,))
        
        return jsonify({
            'code': 200,
            'message': 'Successfully left the assembly.'
        }), 200
    
    except Exception as e:
        print(f"Error leaving assembly: {str(e)}")
        return jsonify({
            'code': 500,
            'message': 'An error occurred leaving the assembly.'
        }), 500


# -----------------------------------------------------------------------------------------
# [POST] createAssemblyPost
# Purpose: Create a new post in an assembly (members only)
# Used: SpecificAssembly.vue (Create Post modal)
# Input:
#   1. assemblyID - the assembly to post in
#   2. memberID - the member's ID in assemblyMembers table
#   3. postTitle - title of the post (max 500 chars)
#   4. postContent - HTML content from Quill editor
#   5. images - array of base64 images (optional, max 5)
#   6. listingIDs - array of listing IDs to link (optional)
# Output: Possible return codes:
#   201 - Post created successfully
#   400 - Missing data or validation error
#   403 - Not a member
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/createAssemblyPost', methods=['POST'])
def create_assembly_post():
    try:
        data = request.get_json()
        
        assembly_id = data.get('assemblyID')
        member_id = data.get('memberID')
        post_title = data.get('postTitle', '').strip()
        post_content = data.get('postContent', '').strip()
        images = data.get('images', [])
        listing_ids = data.get('listingIDs', [])
        
        # Validation
        if not assembly_id or not member_id:
            return jsonify({
                'code': 400,
                'message': 'Missing required data: assemblyID and memberID are required.'
            }), 400
        
        if not post_title:
            return jsonify({
                'code': 400,
                'message': 'Post title is required.'
            }), 400
        
        if len(post_title) > 500:
            return jsonify({
                'code': 400,
                'message': 'Post title cannot exceed 500 characters.'
            }), 400
        
        if len(images) > 5:
            return jsonify({
                'code': 400,
                'message': 'Maximum 5 images allowed per post.'
            }), 400
        
        with db_manager.get_cursor() as cursor:
            # Verify member exists and belongs to this assembly
            cursor.execute('''
                SELECT id FROM "assemblyMembers" 
                WHERE id = %s AND "assemblyID" = %s
            ''', (member_id, assembly_id))
            
            if not cursor.fetchone():
                return jsonify({
                    'code': 403,
                    'message': 'You must be a member to post in this assembly.'
                }), 403
            
            # Upload images to S3
            image_urls = []
            for image in images:
                if not image:
                    continue
                base64_string = re.sub(r'^data:image\/[a-zA-Z]+;base64,', '', image)
                image_url = s3Images.uploadBase64ImageToS3(base64_string)
                if image_url:
                    image_urls.append(image_url)
            
            # Format arrays for PostgreSQL
            post_photos = '{' + ','.join(f'"{url}"' for url in image_urls) + '}' if image_urls else None
            listing_ids_array = listing_ids if listing_ids and len(listing_ids) > 0 else None
            
            post_date = datetime.now()
            
            # Insert the post
            cursor.execute('''
                INSERT INTO "assemblyPosts" 
                ("assemblyID", "postTitle", "postContent", "postPhotos", "listingIDs", "isPinned", "postDate", "posterID")
                VALUES (%s, %s, %s, %s, %s, FALSE, %s, %s)
                RETURNING id
            ''', (assembly_id, post_title, post_content or None, post_photos, listing_ids_array, post_date, member_id))
            
            post_id = cursor.fetchone()['id']
            
            # Update total posts count
            cursor.execute('''
                UPDATE "assemblies" SET "totalPosts" = "totalPosts" + 1 WHERE id = %s
            ''', (assembly_id,))
        
        return jsonify({
            'code': 201,
            'data': {'postID': post_id},
            'message': 'Post created successfully.'
        }), 201
    
    except Exception as e:
        print(f"Error creating assembly post: {str(e)}")
        return jsonify({
            'code': 500,
            'message': 'An error occurred creating the post.'
        }), 500


# -----------------------------------------------------------------------------------------
# [PUT] voteAssemblyPost
# Purpose: Upvote, downvote, or remove vote from a post (members only)
#          Handles switching votes in one action
# Used: SpecificAssembly.vue
# Input:
#   1. assemblyID - the assembly
#   2. postID - the post to vote on
#   3. memberID - the member's ID
#   4. voteType - 'up', 'down', or 'none' (to remove vote)
# Output: Possible return codes:
#   200 - Vote recorded/removed successfully
#   400 - Missing data
#   403 - Not a member
#   404 - Post not found
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/voteAssemblyPost', methods=['PUT'])
def vote_assembly_post():
    try:
        data = request.get_json()
        
        assembly_id = data.get('assemblyID')
        post_id = data.get('postID')
        member_id = data.get('memberID')
        vote_type = data.get('voteType')  # 'up', 'down', or 'none'
        
        if not assembly_id or not post_id or not member_id or not vote_type:
            return jsonify({
                'code': 400,
                'message': 'Missing required data.'
            }), 400
        
        if vote_type not in ['up', 'down', 'none']:
            return jsonify({
                'code': 400,
                'message': 'Invalid vote type. Must be "up", "down", or "none".'
            }), 400
        
        with db_manager.get_cursor() as cursor:
            # Verify member exists and belongs to this assembly
            cursor.execute('''
                SELECT id FROM "assemblyMembers" 
                WHERE id = %s AND "assemblyID" = %s
            ''', (member_id, assembly_id))
            
            if not cursor.fetchone():
                return jsonify({
                    'code': 403,
                    'message': 'You must be a member to vote.'
                }), 403
            
            # Verify post exists
            cursor.execute('SELECT id FROM "assemblyPosts" WHERE id = %s', (post_id,))
            if not cursor.fetchone():
                return jsonify({
                    'code': 404,
                    'message': 'Post not found.'
                }), 404
            
            # Check current vote status
            cursor.execute('''
                SELECT id FROM "assemblyPostsLikes" 
                WHERE "postID" = %s AND "memberID" = %s
            ''', (post_id, member_id))
            has_liked = cursor.fetchone()
            
            cursor.execute('''
                SELECT id FROM "assemblyPostsDislikes" 
                WHERE "postID" = %s AND "memberID" = %s
            ''', (post_id, member_id))
            has_disliked = cursor.fetchone()
            
            # Remove existing votes first
            if has_liked:
                cursor.execute('''
                    DELETE FROM "assemblyPostsLikes" 
                    WHERE "postID" = %s AND "memberID" = %s
                ''', (post_id, member_id))
            
            if has_disliked:
                cursor.execute('''
                    DELETE FROM "assemblyPostsDislikes" 
                    WHERE "postID" = %s AND "memberID" = %s
                ''', (post_id, member_id))
            
            # Add new vote if not removing
            new_vote = None
            if vote_type == 'up':
                # Only add if wasn't already liked (toggle off)
                if not has_liked:
                    cursor.execute('''
                        INSERT INTO "assemblyPostsLikes" ("assemblyID", "postID", "memberID")
                        VALUES (%s, %s, %s)
                    ''', (assembly_id, post_id, member_id))
                    new_vote = 'up'
            elif vote_type == 'down':
                # Only add if wasn't already disliked (toggle off)
                if not has_disliked:
                    cursor.execute('''
                        INSERT INTO "assemblyPostsDislikes" ("assemblyID", "postID", "memberID")
                        VALUES (%s, %s, %s)
                    ''', (assembly_id, post_id, member_id))
                    new_vote = 'down'
            
            # Get updated vote count
            cursor.execute('SELECT COUNT(*) as count FROM "assemblyPostsLikes" WHERE "postID" = %s', (post_id,))
            likes = cursor.fetchone()['count']
            
            cursor.execute('SELECT COUNT(*) as count FROM "assemblyPostsDislikes" WHERE "postID" = %s', (post_id,))
            dislikes = cursor.fetchone()['count']
            
            vote_count = likes - dislikes
        
        return jsonify({
            'code': 200,
            'data': {
                'voteCount': vote_count,
                'userVote': new_vote
            },
            'message': 'Vote recorded successfully.'
        }), 200
    
    except Exception as e:
        print(f"Error voting on assembly post: {str(e)}")
        return jsonify({
            'code': 500,
            'message': 'An error occurred recording your vote.'
        }), 500


# -----------------------------------------------------------------------------------------
# [PUT] pinAssemblyPost
# Purpose: Pin or unpin a post (admin only)
# Used: SpecificAssembly.vue
# Input:
#   1. postID - the post to pin/unpin
#   2. memberID - admin's member ID
#   3. isPinned - true to pin, false to unpin
# Output: Possible return codes:
#   200 - Post pinned/unpinned successfully
#   403 - Not an admin
#   404 - Post not found
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/pinAssemblyPost', methods=['PUT'])
def pin_assembly_post():
    try:
        data = request.get_json()
        
        post_id = data.get('postID')
        member_id = data.get('memberID')
        is_pinned = data.get('isPinned', False)
        
        if not post_id or not member_id:
            return jsonify({
                'code': 400,
                'message': 'Missing required data.'
            }), 400
        
        with db_manager.get_cursor() as cursor:
            # Get post's assembly
            cursor.execute('SELECT "assemblyID" FROM "assemblyPosts" WHERE id = %s', (post_id,))
            post = cursor.fetchone()
            
            if not post:
                return jsonify({
                    'code': 404,
                    'message': 'Post not found.'
                }), 404
            
            assembly_id = post['assemblyID']
            
            # Verify member is admin
            cursor.execute('''
                SELECT "isAdmin" FROM "assemblyMembers" 
                WHERE id = %s AND "assemblyID" = %s
            ''', (member_id, assembly_id))
            member = cursor.fetchone()
            
            if not member or not member['isAdmin']:
                return jsonify({
                    'code': 403,
                    'message': 'Only admins can pin posts.'
                }), 403
            
            # Update pin status
            cursor.execute('''
                UPDATE "assemblyPosts" SET "isPinned" = %s WHERE id = %s
            ''', (is_pinned, post_id))
        
        return jsonify({
            'code': 200,
            'message': f'Post {"pinned" if is_pinned else "unpinned"} successfully.'
        }), 200
    
    except Exception as e:
        print(f"Error pinning assembly post: {str(e)}")
        return jsonify({
            'code': 500,
            'message': 'An error occurred.'
        }), 500


# -----------------------------------------------------------------------------------------
# [DELETE] deleteAssemblyPost
# Purpose: Delete a post (poster or admin)
# Used: SpecificAssembly.vue
# Input:
#   1. postID - the post to delete
#   2. memberID - the member's ID (poster or admin)
# Output: Possible return codes:
#   200 - Post deleted successfully
#   403 - No permission
#   404 - Post not found
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/deleteAssemblyPost', methods=['DELETE'])
def delete_assembly_post():
    try:
        data = request.get_json()
        
        post_id = data.get('postID')
        member_id = data.get('memberID')
        
        if not post_id or not member_id:
            return jsonify({
                'code': 400,
                'message': 'Missing required data.'
            }), 400
        
        with db_manager.get_cursor() as cursor:
            # Get post info
            cursor.execute('''
                SELECT "assemblyID", "posterID", "postPhotos" FROM "assemblyPosts" WHERE id = %s
            ''', (post_id,))
            post = cursor.fetchone()
            
            if not post:
                return jsonify({
                    'code': 404,
                    'message': 'Post not found.'
                }), 404
            
            assembly_id = post['assemblyID']
            poster_id = post['posterID']
            
            # Check if user is the poster
            is_poster = (poster_id == int(member_id))
            
            # Check if user is admin
            cursor.execute('''
                SELECT "isAdmin" FROM "assemblyMembers" 
                WHERE id = %s AND "assemblyID" = %s
            ''', (member_id, assembly_id))
            member = cursor.fetchone()
            is_admin = member and member['isAdmin']
            
            if not is_poster and not is_admin:
                return jsonify({
                    'code': 403,
                    'message': 'You do not have permission to delete this post.'
                }), 403
            
            # Delete images from S3
            if post['postPhotos']:
                for photo_url in post['postPhotos']:
                    try:
                        s3Images.deleteImageFromS3(photo_url)
                    except Exception as s3_error:
                        print(f"Error deleting image from S3: {s3_error}")
            
            # Delete the post (cascades to likes, dislikes, comments)
            cursor.execute('DELETE FROM "assemblyPosts" WHERE id = %s', (post_id,))
            
            # Update total posts count
            cursor.execute('''
                UPDATE "assemblies" SET "totalPosts" = "totalPosts" - 1 WHERE id = %s
            ''', (assembly_id,))
        
        return jsonify({
            'code': 200,
            'message': 'Post deleted successfully.'
        }), 200
    
    except Exception as e:
        print(f"Error deleting assembly post: {str(e)}")
        return jsonify({
            'code': 500,
            'message': 'An error occurred deleting the post.'
        }), 500


# -----------------------------------------------------------------------------------------
# [PUT] editAssemblyPost
# Purpose: Edit a post (poster only)
# Used: SpecificAssembly.vue
# Input:
#   1. postID - the post to edit
#   2. memberID - poster's member ID
#   3. postTitle - updated title
#   4. postContent - updated content
#   5. images - array of image URLs (existing) or base64 (new)
#   6. listingIDs - array of listing IDs
# Output: Possible return codes:
#   200 - Post updated successfully
#   403 - No permission
#   404 - Post not found
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/editAssemblyPost', methods=['PUT'])
def edit_assembly_post():
    try:
        data = request.get_json()
        
        post_id = data.get('postID')
        member_id = data.get('memberID')
        post_title = data.get('postTitle', '').strip()
        post_content = data.get('postContent', '').strip()
        images = data.get('images', [])
        listing_ids = data.get('listingIDs', [])
        
        if not post_id or not member_id:
            return jsonify({
                'code': 400,
                'message': 'Missing required data.'
            }), 400
        
        if not post_title:
            return jsonify({
                'code': 400,
                'message': 'Post title is required.'
            }), 400
        
        if len(post_title) > 500:
            return jsonify({
                'code': 400,
                'message': 'Post title cannot exceed 500 characters.'
            }), 400
        
        with db_manager.get_cursor() as cursor:
            # Get post info
            cursor.execute('''
                SELECT "assemblyID", "posterID", "postPhotos" FROM "assemblyPosts" WHERE id = %s
            ''', (post_id,))
            post = cursor.fetchone()
            
            if not post:
                return jsonify({
                    'code': 404,
                    'message': 'Post not found.'
                }), 404
            
            # Check if user is the poster
            if post['posterID'] != int(member_id):
                return jsonify({
                    'code': 403,
                    'message': 'Only the post author can edit this post.'
                }), 403
            
            # Handle images - delete removed ones, upload new ones
            existing_photos = post['postPhotos'] or []
            new_image_urls = []
            
            for image in images:
                if not image:
                    continue
                # Check if it's an existing S3 URL
                if 's3' in image or 'amazonaws' in image or 'shopify' in image:
                    new_image_urls.append(image)
                else:
                    # Upload new image
                    base64_string = re.sub(r'^data:image\/[a-zA-Z]+;base64,', '', image)
                    image_url = s3Images.uploadBase64ImageToS3(base64_string)
                    if image_url:
                        new_image_urls.append(image_url)
            
            # Delete removed images from S3
            for old_url in existing_photos:
                if old_url not in new_image_urls:
                    try:
                        s3Images.deleteImageFromS3(old_url)
                    except Exception as s3_error:
                        print(f"Error deleting old image from S3: {s3_error}")
            
            # Format arrays for PostgreSQL
            post_photos = '{' + ','.join(f'"{url}"' for url in new_image_urls) + '}' if new_image_urls else None
            listing_ids_array = listing_ids if listing_ids and len(listing_ids) > 0 else None
            
            # Update the post with editedAt timestamp
            edited_at = datetime.now()
            cursor.execute('''
                UPDATE "assemblyPosts" 
                SET "postTitle" = %s, "postContent" = %s, "postPhotos" = %s, "listingIDs" = %s, "editedAt" = %s
                WHERE id = %s
            ''', (post_title, post_content or None, post_photos, listing_ids_array, edited_at, post_id))
        
        return jsonify({
            'code': 200,
            'message': 'Post updated successfully.'
        }), 200
    
    except Exception as e:
        print(f"Error editing assembly post: {str(e)}")
        return jsonify({
            'code': 500,
            'message': 'An error occurred updating the post.'
        }), 500


# -----------------------------------------------------------------------------------------
# [DELETE] removeAssemblyMember
# Purpose: Remove a member from assembly (admin only, with confirmation on frontend)
# Used: SpecificAssembly.vue
# Input:
#   1. assemblyID - the assembly
#   2. adminMemberID - admin's member ID (for verification)
#   3. targetMemberID - member to remove
# Output: Possible return codes:
#   200 - Member removed successfully
#   403 - No permission or trying to remove creator
#   404 - Member not found
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/removeAssemblyMember', methods=['DELETE'])
def remove_assembly_member():
    try:
        data = request.get_json()
        
        assembly_id = data.get('assemblyID')
        admin_member_id = data.get('adminMemberID')
        target_member_id = data.get('targetMemberID')
        
        if not assembly_id or not admin_member_id or not target_member_id:
            return jsonify({
                'code': 400,
                'message': 'Missing required data.'
            }), 400
        
        with db_manager.get_cursor() as cursor:
            # Verify admin status
            cursor.execute('''
                SELECT "isAdmin" FROM "assemblyMembers" 
                WHERE id = %s AND "assemblyID" = %s
            ''', (admin_member_id, assembly_id))
            admin = cursor.fetchone()
            
            if not admin or not admin['isAdmin']:
                return jsonify({
                    'code': 403,
                    'message': 'Only admins can remove members.'
                }), 403
            
            # Get target member info
            cursor.execute('''
                SELECT "userID", "userType" FROM "assemblyMembers" 
                WHERE id = %s AND "assemblyID" = %s
            ''', (target_member_id, assembly_id))
            target = cursor.fetchone()
            
            if not target:
                return jsonify({
                    'code': 404,
                    'message': 'Member not found.'
                }), 404
            
            # Check if target is the creator
            cursor.execute('''
                SELECT "createdByID", "createdByType" FROM "assemblies" WHERE id = %s
            ''', (assembly_id,))
            assembly = cursor.fetchone()
            
            if (assembly['createdByID'] == target['userID'] and 
                assembly['createdByType'] == target['userType']):
                return jsonify({
                    'code': 403,
                    'message': 'Cannot remove the assembly creator.'
                }), 403
            
            # Remove the member
            cursor.execute('DELETE FROM "assemblyMembers" WHERE id = %s', (target_member_id,))
            
            # Update member count
            cursor.execute('''
                UPDATE "assemblies" SET "totalMembers" = "totalMembers" - 1 WHERE id = %s
            ''', (assembly_id,))
        
        return jsonify({
            'code': 200,
            'message': 'Member removed successfully.'
        }), 200
    
    except Exception as e:
        print(f"Error removing assembly member: {str(e)}")
        return jsonify({
            'code': 500,
            'message': 'An error occurred removing the member.'
        }), 500


# -----------------------------------------------------------------------------------------
# [GET] getSpecificPost
# Purpose: Get full details of a specific post for the individual post page
# Used: SpecificAssemblyPost.vue
# Input: 
#   postID (path param)
#   userID (query param, optional) - to check if user voted
#   userType (query param, optional)
# Output: 
#   200 - Full post details with poster info, vote counts, linked listings
#   404 - Post not found
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/getSpecificPost/<postID>', methods=['GET'])
def get_specific_post(postID):
    try:
        # Get optional user info from query params
        user_id = request.args.get('userID')
        user_type = request.args.get('userType')
        member_id = None
        
        with db_manager.get_cursor() as cursor:
            # Get post details
            cursor.execute('''
                SELECT 
                    ap."id",
                    ap."assemblyID",
                    ap."postTitle",
                    ap."postContent",
                    ap."postPhotos",
                    ap."listingIDs",
                    ap."isPinned",
                    ap."postDate",
                    ap."editedAt",
                    ap."posterID",
                    a."assemblyName"
                FROM "assemblyPosts" ap
                JOIN "assemblies" a ON ap."assemblyID" = a."id"
                WHERE ap."id" = %s
            ''', (postID,))
            
            post = cursor.fetchone()
            
            if not post:
                return jsonify({
                    'code': 404,
                    'message': 'Post not found.'
                }), 404
            
            post_dict = dict(post)
            assembly_id = post['assemblyID']
            poster_id = post['posterID']
            
            # Get user's memberID if logged in
            if user_id and user_type:
                cursor.execute('''
                    SELECT id, "isAdmin" FROM "assemblyMembers" 
                    WHERE "assemblyID" = %s AND "userID" = %s AND "userType" = %s
                ''', (assembly_id, user_id, user_type))
                member_record = cursor.fetchone()
                if member_record:
                    member_id = member_record['id']
                    post_dict['isAdmin'] = member_record['isAdmin']
                    post_dict['isMember'] = True
                    post_dict['memberID'] = member_id
                else:
                    post_dict['isAdmin'] = False
                    post_dict['isMember'] = False
                    post_dict['memberID'] = None
            else:
                post_dict['isAdmin'] = False
                post_dict['isMember'] = False
                post_dict['memberID'] = None
            
            # Check if current user is the post author
            post_dict['isAuthor'] = (member_id == poster_id) if member_id and poster_id else False
            
            # Get poster info
            if poster_id:
                poster_info = get_member_user_info(cursor, poster_id)
                if poster_info:
                    post_dict['posterInfo'] = poster_info
            
            # Get vote counts
            cursor.execute('SELECT COUNT(*) as count FROM "assemblyPostsLikes" WHERE "postID" = %s', (postID,))
            likes = cursor.fetchone()['count']
            
            cursor.execute('SELECT COUNT(*) as count FROM "assemblyPostsDislikes" WHERE "postID" = %s', (postID,))
            dislikes = cursor.fetchone()['count']
            
            post_dict['voteCount'] = likes - dislikes
            post_dict['likeCount'] = likes
            post_dict['dislikeCount'] = dislikes
            
            # Get user's vote status if they are a member
            post_dict['userVote'] = None
            if member_id:
                cursor.execute('''
                    SELECT id FROM "assemblyPostsLikes" 
                    WHERE "postID" = %s AND "memberID" = %s
                ''', (postID, member_id))
                if cursor.fetchone():
                    post_dict['userVote'] = 'up'
                else:
                    cursor.execute('''
                        SELECT id FROM "assemblyPostsDislikes" 
                        WHERE "postID" = %s AND "memberID" = %s
                    ''', (postID, member_id))
                    if cursor.fetchone():
                        post_dict['userVote'] = 'down'
            
            # Get comment count
            cursor.execute('SELECT COUNT(*) as count FROM "assemblyPostComments" WHERE "postID" = %s', (postID,))
            post_dict['commentCount'] = cursor.fetchone()['count']
            
            # Get linked listings info if any
            if post_dict['listingIDs'] and len(post_dict['listingIDs']) > 0:
                listings_info = []
                for listing_id in post_dict['listingIDs']:
                    cursor.execute('''
                        SELECT l."id", l."listingName", l."photo", l."drinkType", l."abv",
                               p."producerName"
                        FROM "listings" l
                        LEFT JOIN "producers" p ON l."producerID" = p."id"
                        WHERE l."id" = %s
                    ''', (listing_id,))
                    listing = cursor.fetchone()
                    if listing:
                        listings_info.append(dict(listing))
                post_dict['linkedListings'] = listings_info
            else:
                post_dict['linkedListings'] = []
            
            return jsonify({
                'code': 200,
                'data': post_dict
            }), 200
    
    except Exception as e:
        print(f"Error getting specific post: {str(e)}")
        return jsonify({
            'code': 500,
            'message': 'An error occurred retrieving the post.'
        }), 500


# -----------------------------------------------------------------------------------------
# [GET] getPostComments
# Purpose: Get paginated comments for a post with nested replies
#          Root comments: 25 per page, newest first
#          Replies: 5 per parent, oldest first (load more available)
# Used: SpecificAssemblyPost.vue
# Input: 
#   postID (path param)
#   offset (path param) - for root comments pagination (0, 25, 50...)
#   userID (query param, optional) - to check if user voted
#   userType (query param, optional)
# Output: 
#   200 - List of comments with nested replies
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/getPostComments/<postID>/<offset>', methods=['GET'])
def get_post_comments(postID, offset):
    try:
        offset = int(offset)
        limit = 25  # Root comments per page
        replies_limit = 5  # Initial replies to show per comment
        
        # Get optional user info from query params
        user_id = request.args.get('userID')
        user_type = request.args.get('userType')
        member_id = None
        
        with db_manager.get_cursor() as cursor:
            # Get post info to verify it exists and get assembly context
            cursor.execute('SELECT "assemblyID", "posterID" FROM "assemblyPosts" WHERE id = %s', (postID,))
            post = cursor.fetchone()
            
            if not post:
                return jsonify({
                    'code': 404,
                    'message': 'Post not found.'
                }), 404
            
            assembly_id = post['assemblyID']
            post_author_id = post['posterID']
            
            # Get user's memberID if logged in
            is_admin = False
            if user_id and user_type:
                cursor.execute('''
                    SELECT id, "isAdmin" FROM "assemblyMembers" 
                    WHERE "assemblyID" = %s AND "userID" = %s AND "userType" = %s
                ''', (assembly_id, user_id, user_type))
                member_record = cursor.fetchone()
                if member_record:
                    member_id = member_record['id']
                    is_admin = member_record['isAdmin']
            
            # Get root comments (parentCommentID IS NULL), ordered by newest first
            cursor.execute('''
                SELECT 
                    apc."id",
                    apc."postID",
                    apc."parentCommentID",
                    apc."commentContent",
                    apc."commentDate",
                    apc."commenterID"
                FROM "assemblyPostComments" apc
                WHERE apc."postID" = %s AND apc."parentCommentID" IS NULL
                ORDER BY apc."commentDate" DESC
                LIMIT %s OFFSET %s
            ''', (postID, limit, offset))
            
            root_comments = cursor.fetchall()
            
            result = []
            
            for comment in root_comments:
                comment_dict = dict(comment)
                comment_id = comment['id']
                commenter_id = comment['commenterID']
                
                # Get commenter info
                if commenter_id:
                    commenter_info = get_member_user_info(cursor, commenter_id)
                    if commenter_info:
                        comment_dict['commenterInfo'] = commenter_info
                
                # Get vote counts for comment
                cursor.execute('SELECT COUNT(*) as count FROM "assemblyPostCommentsLikes" WHERE "commentID" = %s', (comment_id,))
                likes = cursor.fetchone()['count']
                
                cursor.execute('SELECT COUNT(*) as count FROM "assemblyPostCommentsDislikes" WHERE "commentID" = %s', (comment_id,))
                dislikes = cursor.fetchone()['count']
                
                comment_dict['voteCount'] = likes - dislikes
                
                # Get user's vote status if they are a member
                comment_dict['userVote'] = None
                if member_id:
                    cursor.execute('''
                        SELECT id FROM "assemblyPostCommentsLikes" 
                        WHERE "commentID" = %s AND "memberID" = %s
                    ''', (comment_id, member_id))
                    if cursor.fetchone():
                        comment_dict['userVote'] = 'up'
                    else:
                        cursor.execute('''
                            SELECT id FROM "assemblyPostCommentsDislikes" 
                            WHERE "commentID" = %s AND "memberID" = %s
                        ''', (comment_id, member_id))
                        if cursor.fetchone():
                            comment_dict['userVote'] = 'down'
                
                # Check if user can delete this comment
                # (is commenter, is admin, or is post author)
                comment_dict['canDelete'] = (
                    (member_id and commenter_id and member_id == commenter_id) or
                    is_admin or
                    (member_id and post_author_id and member_id == post_author_id)
                )
                
                # Get total reply count
                cursor.execute('''
                    SELECT COUNT(*) as count FROM "assemblyPostComments" 
                    WHERE "parentCommentID" = %s
                ''', (comment_id,))
                total_replies = cursor.fetchone()['count']
                comment_dict['totalReplies'] = total_replies
                
                # Get first 5 replies, ordered by oldest first (chronological for conversation flow)
                cursor.execute('''
                    SELECT 
                        apc."id",
                        apc."postID",
                        apc."parentCommentID",
                        apc."commentContent",
                        apc."commentDate",
                        apc."commenterID"
                    FROM "assemblyPostComments" apc
                    WHERE apc."parentCommentID" = %s
                    ORDER BY apc."commentDate" ASC
                    LIMIT %s
                ''', (comment_id, replies_limit))
                
                replies = cursor.fetchall()
                replies_list = []
                
                for reply in replies:
                    reply_dict = dict(reply)
                    reply_commenter_id = reply['commenterID']
                    
                    # Get reply commenter info
                    if reply_commenter_id:
                        reply_commenter_info = get_member_user_info(cursor, reply_commenter_id)
                        if reply_commenter_info:
                            reply_dict['commenterInfo'] = reply_commenter_info
                    
                    # Get vote counts for reply
                    cursor.execute('SELECT COUNT(*) as count FROM "assemblyPostCommentsLikes" WHERE "commentID" = %s', (reply['id'],))
                    reply_likes = cursor.fetchone()['count']
                    
                    cursor.execute('SELECT COUNT(*) as count FROM "assemblyPostCommentsDislikes" WHERE "commentID" = %s', (reply['id'],))
                    reply_dislikes = cursor.fetchone()['count']
                    
                    reply_dict['voteCount'] = reply_likes - reply_dislikes
                    
                    # Get user's vote status for reply
                    reply_dict['userVote'] = None
                    if member_id:
                        cursor.execute('''
                            SELECT id FROM "assemblyPostCommentsLikes" 
                            WHERE "commentID" = %s AND "memberID" = %s
                        ''', (reply['id'], member_id))
                        if cursor.fetchone():
                            reply_dict['userVote'] = 'up'
                        else:
                            cursor.execute('''
                                SELECT id FROM "assemblyPostCommentsDislikes" 
                                WHERE "commentID" = %s AND "memberID" = %s
                            ''', (reply['id'], member_id))
                            if cursor.fetchone():
                                reply_dict['userVote'] = 'down'
                    
                    # Check if user can delete this reply
                    reply_dict['canDelete'] = (
                        (member_id and reply_commenter_id and member_id == reply_commenter_id) or
                        is_admin or
                        (member_id and post_author_id and member_id == post_author_id)
                    )
                    
                    replies_list.append(reply_dict)
                
                comment_dict['replies'] = replies_list
                comment_dict['hasMoreReplies'] = total_replies > replies_limit
                comment_dict['remainingReplies'] = max(0, total_replies - replies_limit)
                
                result.append(comment_dict)
            
            # Get total root comments count to determine if there are more
            cursor.execute('''
                SELECT COUNT(*) as count FROM "assemblyPostComments"
                WHERE "postID" = %s AND "parentCommentID" IS NULL
            ''', (postID,))
            total_root_comments = cursor.fetchone()['count']
            
            new_offset = offset + len(result)
            has_more = new_offset < total_root_comments
            
            return jsonify({
                'code': 200,
                'data': result,
                'hasMore': has_more
            }), 200
    
    except Exception as e:
        print(f"Error getting post comments: {str(e)}")
        return jsonify({
            'code': 500,
            'message': 'An error occurred retrieving comments.'
        }), 500


# -----------------------------------------------------------------------------------------
# [GET] getMoreReplies
# Purpose: Load more replies for a specific comment (pagination for replies)
# Used: SpecificAssemblyPost.vue
# Input: 
#   commentID (path param)
#   offset (path param) - for replies pagination (5, 10, 15...)
#   userID (query param, optional)
#   userType (query param, optional)
# Output: 
#   200 - List of additional replies
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/getMoreReplies/<commentID>/<offset>', methods=['GET'])
def get_more_replies(commentID, offset):
    try:
        offset = int(offset)
        limit = 5  # Replies per load
        
        # Get optional user info from query params
        user_id = request.args.get('userID')
        user_type = request.args.get('userType')
        member_id = None
        
        with db_manager.get_cursor() as cursor:
            # Get comment info to verify it exists and get context
            cursor.execute('''
                SELECT apc."postID", ap."assemblyID", ap."posterID"
                FROM "assemblyPostComments" apc
                JOIN "assemblyPosts" ap ON apc."postID" = ap."id"
                WHERE apc."id" = %s
            ''', (commentID,))
            comment_info = cursor.fetchone()
            
            if not comment_info:
                return jsonify({
                    'code': 404,
                    'message': 'Comment not found.'
                }), 404
            
            assembly_id = comment_info['assemblyID']
            post_author_id = comment_info['posterID']
            
            # Get user's memberID if logged in
            is_admin = False
            if user_id and user_type:
                cursor.execute('''
                    SELECT id, "isAdmin" FROM "assemblyMembers" 
                    WHERE "assemblyID" = %s AND "userID" = %s AND "userType" = %s
                ''', (assembly_id, user_id, user_type))
                member_record = cursor.fetchone()
                if member_record:
                    member_id = member_record['id']
                    is_admin = member_record['isAdmin']
            
            # Get replies with offset, ordered by oldest first
            cursor.execute('''
                SELECT 
                    apc."id",
                    apc."postID",
                    apc."parentCommentID",
                    apc."commentContent",
                    apc."commentDate",
                    apc."commenterID"
                FROM "assemblyPostComments" apc
                WHERE apc."parentCommentID" = %s
                ORDER BY apc."commentDate" ASC
                LIMIT %s OFFSET %s
            ''', (commentID, limit, offset))
            
            replies = cursor.fetchall()
            result = []
            
            for reply in replies:
                reply_dict = dict(reply)
                reply_commenter_id = reply['commenterID']
                
                # Get reply commenter info
                if reply_commenter_id:
                    reply_commenter_info = get_member_user_info(cursor, reply_commenter_id)
                    if reply_commenter_info:
                        reply_dict['commenterInfo'] = reply_commenter_info
                
                # Get vote counts for reply
                cursor.execute('SELECT COUNT(*) as count FROM "assemblyPostCommentsLikes" WHERE "commentID" = %s', (reply['id'],))
                reply_likes = cursor.fetchone()['count']
                
                cursor.execute('SELECT COUNT(*) as count FROM "assemblyPostCommentsDislikes" WHERE "commentID" = %s', (reply['id'],))
                reply_dislikes = cursor.fetchone()['count']
                
                reply_dict['voteCount'] = reply_likes - reply_dislikes
                
                # Get user's vote status for reply
                reply_dict['userVote'] = None
                if member_id:
                    cursor.execute('''
                        SELECT id FROM "assemblyPostCommentsLikes" 
                        WHERE "commentID" = %s AND "memberID" = %s
                    ''', (reply['id'], member_id))
                    if cursor.fetchone():
                        reply_dict['userVote'] = 'up'
                    else:
                        cursor.execute('''
                            SELECT id FROM "assemblyPostCommentsDislikes" 
                            WHERE "commentID" = %s AND "memberID" = %s
                        ''', (reply['id'], member_id))
                        if cursor.fetchone():
                            reply_dict['userVote'] = 'down'
                
                # Check if user can delete this reply
                reply_dict['canDelete'] = (
                    (member_id and reply_commenter_id and member_id == reply_commenter_id) or
                    is_admin or
                    (member_id and post_author_id and member_id == post_author_id)
                )
                
                result.append(reply_dict)
            
            # Get total reply count to determine if there are more
            cursor.execute('''
                SELECT COUNT(*) as count FROM "assemblyPostComments"
                WHERE "parentCommentID" = %s
            ''', (commentID,))
            total_replies = cursor.fetchone()['count']
            
            new_offset = offset + len(result)
            has_more = new_offset < total_replies
            remaining_count = max(0, total_replies - new_offset)
            
            return jsonify({
                'code': 200,
                'data': result,
                'hasMore': has_more,
                'remainingCount': remaining_count
            }), 200
    
    except Exception as e:
        print(f"Error getting more replies: {str(e)}")
        return jsonify({
            'code': 500,
            'message': 'An error occurred retrieving replies.'
        }), 500


# -----------------------------------------------------------------------------------------
# [POST] createPostComment
# Purpose: Create a new comment or reply on a post (members only)
# Used: SpecificAssemblyPost.vue
# Input:
#   1. postID - the post to comment on
#   2. memberID - the member's ID in assemblyMembers table
#   3. commentContent - the comment text (max 5000 chars)
#   4. parentCommentID - (optional) if replying to a comment, the parent comment ID
# Output: Possible return codes:
#   201 - Comment created successfully
#   400 - Missing data or validation error
#   403 - Not a member
#   404 - Post or parent comment not found
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/createPostComment', methods=['POST'])
def create_post_comment():
    try:
        data = request.get_json()
        
        post_id = data.get('postID')
        member_id = data.get('memberID')
        comment_content = data.get('commentContent', '').strip()
        parent_comment_id = data.get('parentCommentID')  # Optional - for replies
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Validation
        if not post_id or not member_id:
            return jsonify({
                'code': 400,
                'message': 'Missing required data: postID and memberID are required.'
            }), 400
        
        if not comment_content:
            return jsonify({
                'code': 400,
                'message': 'Comment content is required.'
            }), 400
        
        if len(comment_content) > 5000:
            return jsonify({
                'code': 400,
                'message': 'Comment cannot exceed 5000 characters.'
            }), 400
        
        with db_manager.get_cursor() as cursor:
            # Verify post exists and get assembly info
            cursor.execute('''
                SELECT ap."assemblyID", ap."posterID", a."assemblyName"
                FROM "assemblyPosts" ap
                JOIN "assemblies" a ON ap."assemblyID" = a."id"
                WHERE ap."id" = %s
            ''', (post_id,))
            post = cursor.fetchone()
            
            if not post:
                return jsonify({
                    'code': 404,
                    'message': 'Post not found.'
                }), 404
            
            assembly_id = post['assemblyID']
            post_author_id = post['posterID']
            assembly_name = post['assemblyName']
            
            # Verify member exists and belongs to this assembly
            cursor.execute('''
                SELECT id FROM "assemblyMembers" 
                WHERE id = %s AND "assemblyID" = %s
            ''', (member_id, assembly_id))
            
            if not cursor.fetchone():
                return jsonify({
                    'code': 403,
                    'message': 'You must be a member to comment.'
                }), 403
            
            # If this is a reply, verify parent comment exists and belongs to this post
            # Also enforce 2-level nesting (no replies to replies)
            notify_user_id = None
            notify_user_type = None
            parent_commenter_username = None
            
            if parent_comment_id:
                cursor.execute('''
                    SELECT "postID", "parentCommentID", "commenterID"
                    FROM "assemblyPostComments" WHERE id = %s
                ''', (parent_comment_id,))
                parent_comment = cursor.fetchone()
                
                if not parent_comment:
                    return jsonify({
                        'code': 404,
                        'message': 'Parent comment not found.'
                    }), 404
                
                if parent_comment['postID'] != int(post_id):
                    return jsonify({
                        'code': 400,
                        'message': 'Parent comment does not belong to this post.'
                    }), 400
                
                # Enforce 2-level nesting - replies to replies should go to the root comment
                if parent_comment['parentCommentID'] is not None:
                    # This is a reply to a reply - flatten it to be under the root comment
                    parent_comment_id = parent_comment['parentCommentID']
                
                # Get parent commenter info for notification
                if parent_comment['commenterID']:
                    parent_commenter_info = get_member_user_info(cursor, parent_comment['commenterID'])
                    if parent_commenter_info and parent_commenter_info['id'] != member_id:
                        notify_user_id = parent_commenter_info['id']
                        notify_user_type = parent_commenter_info['userType']
                        parent_commenter_username = parent_commenter_info.get('username')
            
            comment_date = datetime.now()
            
            # Insert the comment
            cursor.execute('''
                INSERT INTO "assemblyPostComments" 
                ("postID", "parentCommentID", "commentContent", "commentDate", "commenterID")
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
            ''', (post_id, parent_comment_id, comment_content, comment_date, member_id))
            
            comment_id = cursor.fetchone()['id']
            
            # Get commenter info for response and notification
            commenter_info = get_member_user_info(cursor, member_id)
            commenter_username = commenter_info.get('username', 'Someone') if commenter_info else 'Someone'
            
            # Send notification
            if parent_comment_id and notify_user_id:
                # This is a reply - notify the parent commenter
                notification_data = {
                    "userId": notify_user_id,
                    "userType": notify_user_type,
                    "notiTabs": "forYou",
                    "notiType": "assembly_post_reply",
                    "image": None,
                    "link": f"/assemblies/{assembly_id}/{assembly_name.replace(' ', '-').lower()}/assembly-post/{post_id}/post#comment-{comment_id}",
                    "message": f"@{commenter_username} replied to your comment",
                    "createdAt": current_time
                }
                try:
                    notifications.add_notification_to_db(notification_data, cursor)
                except Exception as notif_error:
                    print(f"Failed to send reply notification: {notif_error}")
            else:
                # This is a root comment - notify the post author
                if post_author_id and post_author_id != member_id:
                    post_author_info = get_member_user_info(cursor, post_author_id)
                    if post_author_info:
                        # Get post title for notification preview (truncate to 50 chars)
                        cursor.execute('SELECT "postTitle" FROM "assemblyPosts" WHERE id = %s', (post_id,))
                        post_title_result = cursor.fetchone()
                        post_title = post_title_result['postTitle'][:50] + '...' if post_title_result and len(post_title_result['postTitle']) > 50 else (post_title_result['postTitle'] if post_title_result else 'a post')
                        
                        notification_data = {
                            "userId": post_author_info['id'],
                            "userType": post_author_info['userType'],
                            "notiTabs": "forYou",
                            "notiType": "assembly_post_comment",
                            "image": None,
                            "link": f"/assemblies/{assembly_id}/{assembly_name.replace(' ', '-').lower()}/assembly-post/{post_id}/post#comment-{comment_id}",
                            "message": f"@{commenter_username} commented on your post: '{post_title}'",
                            "createdAt": current_time
                        }
                        try:
                            notifications.add_notification_to_db(notification_data, cursor)
                        except Exception as notif_error:
                            print(f"Failed to send comment notification: {notif_error}")
            
            # TODO: Add @mention notification logic here when implementing mentions
            # Parse comment_content for @username patterns and send notifications
        
        return jsonify({
            'code': 201,
            'data': {
                'commentID': comment_id,
                'parentCommentID': parent_comment_id
            },
            'message': 'Comment created successfully.'
        }), 201
    
    except Exception as e:
        print(f"Error creating post comment: {str(e)}")
        return jsonify({
            'code': 500,
            'message': 'An error occurred creating the comment.'
        }), 500


# -----------------------------------------------------------------------------------------
# [PUT] votePostComment
# Purpose: Upvote, downvote, or remove vote from a comment (members only)
# Used: SpecificAssemblyPost.vue
# Input:
#   1. postID - the post the comment belongs to
#   2. commentID - the comment to vote on
#   3. memberID - the member's ID
#   4. voteType - 'up', 'down', or 'none' (to remove vote)
# Output: Possible return codes:
#   200 - Vote recorded/removed successfully
#   400 - Missing data
#   403 - Not a member
#   404 - Comment not found
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/votePostComment', methods=['PUT'])
def vote_post_comment():
    try:
        data = request.get_json()
        
        post_id = data.get('postID')
        comment_id = data.get('commentID')
        member_id = data.get('memberID')
        vote_type = data.get('voteType')  # 'up', 'down', or 'none'
        
        if not post_id or not comment_id or not member_id or not vote_type:
            return jsonify({
                'code': 400,
                'message': 'Missing required data.'
            }), 400
        
        if vote_type not in ['up', 'down', 'none']:
            return jsonify({
                'code': 400,
                'message': 'Invalid vote type. Must be "up", "down", or "none".'
            }), 400
        
        with db_manager.get_cursor() as cursor:
            # Verify comment exists and get assembly info
            cursor.execute('''
                SELECT apc."postID", ap."assemblyID"
                FROM "assemblyPostComments" apc
                JOIN "assemblyPosts" ap ON apc."postID" = ap."id"
                WHERE apc."id" = %s
            ''', (comment_id,))
            comment = cursor.fetchone()
            
            if not comment:
                return jsonify({
                    'code': 404,
                    'message': 'Comment not found.'
                }), 404
            
            assembly_id = comment['assemblyID']
            
            # Verify member exists and belongs to this assembly
            cursor.execute('''
                SELECT id FROM "assemblyMembers" 
                WHERE id = %s AND "assemblyID" = %s
            ''', (member_id, assembly_id))
            
            if not cursor.fetchone():
                return jsonify({
                    'code': 403,
                    'message': 'You must be a member to vote.'
                }), 403
            
            # Check current vote status
            cursor.execute('''
                SELECT id FROM "assemblyPostCommentsLikes" 
                WHERE "commentID" = %s AND "memberID" = %s
            ''', (comment_id, member_id))
            has_liked = cursor.fetchone()
            
            cursor.execute('''
                SELECT id FROM "assemblyPostCommentsDislikes" 
                WHERE "commentID" = %s AND "memberID" = %s
            ''', (comment_id, member_id))
            has_disliked = cursor.fetchone()
            
            # Remove existing votes first
            if has_liked:
                cursor.execute('''
                    DELETE FROM "assemblyPostCommentsLikes" 
                    WHERE "commentID" = %s AND "memberID" = %s
                ''', (comment_id, member_id))
            
            if has_disliked:
                cursor.execute('''
                    DELETE FROM "assemblyPostCommentsDislikes" 
                    WHERE "commentID" = %s AND "memberID" = %s
                ''', (comment_id, member_id))
            
            # Add new vote if not removing
            new_vote = None
            if vote_type == 'up':
                if not has_liked:
                    cursor.execute('''
                        INSERT INTO "assemblyPostCommentsLikes" ("postID", "commentID", "memberID")
                        VALUES (%s, %s, %s)
                    ''', (post_id, comment_id, member_id))
                    new_vote = 'up'
            elif vote_type == 'down':
                if not has_disliked:
                    cursor.execute('''
                        INSERT INTO "assemblyPostCommentsDislikes" ("postID", "commentID", "memberID")
                        VALUES (%s, %s, %s)
                    ''', (post_id, comment_id, member_id))
                    new_vote = 'down'
            
            # Get updated vote count
            cursor.execute('SELECT COUNT(*) as count FROM "assemblyPostCommentsLikes" WHERE "commentID" = %s', (comment_id,))
            likes = cursor.fetchone()['count']
            
            cursor.execute('SELECT COUNT(*) as count FROM "assemblyPostCommentsDislikes" WHERE "commentID" = %s', (comment_id,))
            dislikes = cursor.fetchone()['count']
            
            vote_count = likes - dislikes
        
        return jsonify({
            'code': 200,
            'data': {
                'voteCount': vote_count,
                'userVote': new_vote
            },
            'message': 'Vote recorded successfully.'
        }), 200
    
    except Exception as e:
        print(f"Error voting on comment: {str(e)}")
        return jsonify({
            'code': 500,
            'message': 'An error occurred recording your vote.'
        }), 500


# -----------------------------------------------------------------------------------------
# [DELETE] deletePostComment
# Purpose: Delete a comment (commenter, admin, or post author can delete)
# Used: SpecificAssemblyPost.vue
# Input:
#   1. commentID - the comment to delete
#   2. memberID - the member's ID (for permission check)
# Output: Possible return codes:
#   200 - Comment deleted successfully
#   403 - No permission
#   404 - Comment not found
#   500 - Server error
# -----------------------------------------------------------------------------------------
@blueprint.route('/deletePostComment', methods=['DELETE'])
def delete_post_comment():
    try:
        data = request.get_json()
        
        comment_id = data.get('commentID')
        member_id = data.get('memberID')
        
        if not comment_id or not member_id:
            return jsonify({
                'code': 400,
                'message': 'Missing required data.'
            }), 400
        
        with db_manager.get_cursor() as cursor:
            # Get comment info
            cursor.execute('''
                SELECT apc."commenterID", apc."postID", ap."assemblyID", ap."posterID"
                FROM "assemblyPostComments" apc
                JOIN "assemblyPosts" ap ON apc."postID" = ap."id"
                WHERE apc."id" = %s
            ''', (comment_id,))
            comment = cursor.fetchone()
            
            if not comment:
                return jsonify({
                    'code': 404,
                    'message': 'Comment not found.'
                }), 404
            
            assembly_id = comment['assemblyID']
            commenter_id = comment['commenterID']
            post_author_id = comment['posterID']
            
            # Check if user is the commenter
            is_commenter = (commenter_id == int(member_id))
            
            # Check if user is post author
            is_post_author = (post_author_id == int(member_id))
            
            # Check if user is admin
            cursor.execute('''
                SELECT "isAdmin" FROM "assemblyMembers" 
                WHERE id = %s AND "assemblyID" = %s
            ''', (member_id, assembly_id))
            member = cursor.fetchone()
            is_admin = member and member['isAdmin']
            
            if not is_commenter and not is_admin and not is_post_author:
                return jsonify({
                    'code': 403,
                    'message': 'You do not have permission to delete this comment.'
                }), 403
            
            # Delete the comment (cascades to likes, dislikes, and child replies)
            cursor.execute('DELETE FROM "assemblyPostComments" WHERE id = %s', (comment_id,))
        
        return jsonify({
            'code': 200,
            'message': 'Comment deleted successfully.'
        }), 200
    
    except Exception as e:
        print(f"Error deleting comment: {str(e)}")
        return jsonify({
            'code': 500,
            'message': 'An error occurred deleting the comment.'
        }), 500
