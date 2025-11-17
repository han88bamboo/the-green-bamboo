# Port: 5701
# Routes: 
#   [events]    /getEvents (GET), /getSpecificEvent (GET), /getUserEvents (GET), 
#               /getTrendingEvents (GET), /getUpcomingFollowingEvents (GET), /getUserPastEvents (GET),
#               /getUserUpcomingEvents (GET), /getRecentlyAddedEvents (GET), /searchEvents (GET),
#               /canCreateEvents (GET), /getUserOrganisingEvents (GET), /getUserAttendingEvents (GET),
#               /getOrganizerEventsWithAttendees (GET),
#               /createEvent (POST), 
#               /updateEvent (PUT), /lockSignups (PUT), /unlockSignups (PUT),
#               /deleteEvent (DELETE)
#   [attendees] /getAttendees (GET), /checkAttendance (GET), 
#               /addAttendee (POST), 
#               /removeAttendee (DELETE)
#               /updateAttendeeStatus (PUT)
# -----------------------------------------------------------------------------------------

import os
import json
from flask import Blueprint, g, jsonify, request
from datetime import datetime
import re
from scripts import badge_helpers, notifications, pointsHelperFunc

# Import the database manager for connection pooling
from app import db_manager

# Use to upload image to S3
import s3Images

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)


# Helper function to retrieve user's information using the user's id and user type
def getUserInfoByID(cur, user_id, user_type):
    
    # Check the user type and get the user information
    # For type = user:  "id", "displayName", "photo"
    # For type = producer: "id", "producerName", "photo"
    # For type = venue: "id", "venueName", "photo"

    if user_type == 'user':
        cur.execute('SELECT "id", "displayName", "photo" FROM "users" WHERE id = %s', (user_id,))
        user_info = cur.fetchone()
    elif user_type == 'producer':
        cur.execute('SELECT "id", "producerName", "photo" FROM "producers" WHERE id = %s', (user_id,))
        user_info = cur.fetchone()
    else:
        cur.execute('SELECT "id", "venueName", "photo" FROM "venues" WHERE id = %s', (user_id,))
        user_info = cur.fetchone()

    # Check if the user exist
    if not user_info:
        return None

    # Add the user type into the user_info
    user_info['userType'] = user_type

    return user_info

# Helper function to check if user can create more events
def canCreateMoreEvents(cur, user_id, user_type):

    max_events = 0

    # Determine the max events based on user type
    if user_type == 'user':
        max_events = 5 # Per month for users

    else:
        max_events = 20 # Per month for producers and venues


    # Check if the user has created any events this month
    cur.execute('SELECT COUNT(*) FROM events WHERE "eventOwnerID" = %s AND "eventOwnerType" = %s AND "createdDate" >= date_trunc(\'month\', CURRENT_DATE)', (user_id, user_type,))
    event_count = cur.fetchone()

    if event_count and event_count['count'] >= max_events:
        return (False, max_events)
    else:
        return (True, max_events)


# -----------------------------------------------------------------------------------------
# [GET] Get all events with lazy loading
# Purpose:
# Used:
# Output: Possible return codes [200 - Retrieval success, 404 - No events, 500 - Internal server error]
@blueprint.route('/getEvents/<offset>', methods=['GET'])
def getEvents(offset):

    return_data = []

    try:
        with db_manager.get_cursor() as cursor:
            # Get today's date
            today = datetime.now().date()

            # Set the limit here
            limit = 10

            # Step 1: Get the first 5 events from the database (starting from the latest, filtering out past events)
            if offset == '0':
                cursor.execute('SELECT * FROM events WHERE "eventStartDate" >= %s ORDER BY "eventStartDate" ASC, "eventStartTime" ASC LIMIT %s', (today, limit,))
            else:
                cursor.execute('SELECT * FROM events WHERE "eventStartDate" >= %s ORDER BY "eventStartDate" ASC, "eventStartTime" ASC LIMIT %s OFFSET %s', (today, limit, offset,))
            events = cursor.fetchall()

            if not events:
                return jsonify({'error': 'No events'}), 404
            
            # Step 2: Get the event owner information
            for event in events:
                owner_id = event['eventOwnerID']
                owner_type = event['eventOwnerType']

                owner_info = getUserInfoByID(cursor, owner_id, owner_type)

                # If owner information is not found, skip this event 
                if not owner_info:
                    continue

                # Else, add the owner information into the event
                event['ownerInfo'] = owner_info

                # Convert datetime objects to string
                event['eventStartDate'] = event['eventStartDate'].strftime('%Y-%m-%d')

                if event['eventEndDate'] is not None:
                    event['eventEndDate'] = event['eventEndDate'].strftime('%Y-%m-%d')
                
                if event['eventStartTime'] is not None:
                    event['eventStartTime'] = event['eventStartTime'].strftime('%H:%M')

                if event['eventEndTime'] is not None:
                    event['eventEndTime'] = event['eventEndTime'].strftime('%H:%M')

                # Append the event into the return_data
                return_data.append(event)

        return jsonify({
            'events': return_data
        }), 200

    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 500


# -----------------------------------------------------------------------------------------
# [GET] Get an event by event id
# Purpose: Get an event by event id
# Used: SpecificEventPage.vue (inside views folder)
# Output: Possible return codes [200 - Retrieval success, 400 - Bad request, 404 - No such event/Event owner not found, 500 - Internal server error]
@blueprint.route('/getSpecificEvent/<event_id>', methods=['GET'])
def getSpecificEvent(event_id):

    try:
        with db_manager.get_cursor() as cursor:
            # Step 1: Get the event information
            cursor.execute('SELECT * FROM events WHERE id = %s', (event_id,))
            event = cursor.fetchone()

            if not event:
                return jsonify({'error': 'No such event'}), 404

            # Step 2: Get the event owner information
            owner_id = event['eventOwnerID']
            owner_type = event['eventOwnerType']

            owner_info = getUserInfoByID(cursor, owner_id, owner_type)

            # If owner information is not found, return error
            if not owner_info:
                return jsonify({'error': 'Event owner not found'}), 500

            # Else, add the owner information into the event
            event['ownerInfo'] = owner_info

            # Convert datetime objects to string
            event['eventStartDate'] = event['eventStartDate'].strftime('%Y-%m-%d')

            if event['eventEndDate'] is not None:
                event['eventEndDate'] = event['eventEndDate'].strftime('%Y-%m-%d')
            
            if event['eventStartTime'] is not None:
                event['eventStartTime'] = event['eventStartTime'].strftime('%H:%M')

            if event['eventEndTime'] is not None:
                event['eventEndTime'] = event['eventEndTime'].strftime('%H:%M')

            return jsonify({
                'event': event
            }), 200

    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 500


# -----------------------------------------------------------------------------------------
# [GET] Get upcoming events by a user/producer/venue (up to 20)
# Purpose: Get upcoming events by a user/producer/venue in chronological order
# Used: 
#     1. VenueProfile.vue (inside views folder inside venues folder)
#     2. ProducerProfile.vue (inside views folder inside producers folder)
#     3. UserProfile.vue (inside views folder inside users folder)
#     4. SpecificEventPage.vue (inside views folder)
# Output: Possible return codes [200 - Retrieval success, 404 - User not found/No events, 500 - Internal server error]
@blueprint.route('/getUserEvents/<user_id>/<user_type>/<offset>', methods=['GET'])
def getUserEvents(user_id, user_type, offset):

    return_data = []

    # Set the limit here
    limit = 20

    try:
        with db_manager.get_cursor() as cursor:
            # Step 1: Get the user information
            user_info = getUserInfoByID(cursor, user_id, user_type)

            if not user_info:
                return jsonify({'error': 'User not found'}), 404
            
            today_date = datetime.now().date()

            # Step 2: Get the events by the user
            if offset == '0':
                cursor.execute('SELECT * FROM events WHERE "eventOwnerID" = %s AND "eventOwnerType" = %s AND "eventStartDate" >= %s ORDER BY "eventStartDate" ASC, "eventStartTime" ASC LIMIT %s', (user_id, user_type, today_date, limit,))
            else:
                cursor.execute('SELECT * FROM events WHERE "eventOwnerID" = %s AND "eventOwnerType" = %s AND "eventStartDate" >= %s ORDER BY "eventStartDate" ASC, "eventStartTime" ASC LIMIT %s OFFSET %s', (user_id, user_type, today_date, limit, offset,))
            events = cursor.fetchall()

            if not events:
                return jsonify({'error': 'No events'}), 404

            # Step 3: Get the event owner information
            for event in events:
                owner_id = event['eventOwnerID']
                owner_type = event['eventOwnerType']

                owner_info = getUserInfoByID(cursor, owner_id, owner_type)

                # If owner information is not found, skip this event
                if not owner_info:
                    continue

                # Else, add the owner information into the event
                event['ownerInfo'] = owner_info

                # Convert datetime objects to string
                event['eventStartDate'] = event['eventStartDate'].strftime('%Y-%m-%d')
                if event['eventEndDate'] is not None:
                    event['eventEndDate'] = event['eventEndDate'].strftime('%Y-%m-%d')
                
                if event['eventStartTime'] is not None:
                    event['eventStartTime'] = event['eventStartTime'].strftime('%H:%M')

                if event['eventEndTime'] is not None:
                    event['eventEndTime'] = event['eventEndTime'].strftime('%H:%M')

                # Append the event into the return_data
                return_data.append(event)

        return jsonify({
            'events': return_data
        }), 200

    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 500


# -----------------------------------------------------------------------------------------
# [GET] Get ALL events organized by user (both past and upcoming)
# Purpose: Get all events (past and upcoming) organized by a specific user/venue/producer
# Used: EventBox.vue modal for "See all events" functionality
# Output: Possible return codes [200 - Retrieval success, 404 - No events, 500 - Internal server error]
@blueprint.route('/getAllUserEvents/<user_id>/<user_type>/<offset>', methods=['GET'])
def getAllUserEvents(user_id, user_type, offset):
    return_data = []

    # Set a limit for pagination (only used when offset != '0')
    limit = 50

    try:
        with db_manager.get_cursor() as cursor:
            # Step 1: Get the user information
            user_info = getUserInfoByID(cursor, user_id, user_type)

            if not user_info:
                return jsonify({'error': 'User not found'}), 404

            # Step 2: Get ALL events by the user (no date filter)
            if offset == '0':
                # Get all events without limit when offset is 0
                cursor.execute('SELECT * FROM events WHERE "eventOwnerID" = %s AND "eventOwnerType" = %s ORDER BY "eventStartDate" ASC, "eventStartTime" ASC', (user_id, user_type,))
            else:
                cursor.execute('SELECT * FROM events WHERE "eventOwnerID" = %s AND "eventOwnerType" = %s ORDER BY "eventStartDate" ASC, "eventStartTime" ASC LIMIT %s OFFSET %s', (user_id, user_type, limit, offset,))
            
            events = cursor.fetchall()

            if not events:
                return jsonify({'error': 'No events'}), 404

            # Step 3: Get the event owner information
            for event in events:
                owner_id = event['eventOwnerID']
                owner_type = event['eventOwnerType']

                owner_info = getUserInfoByID(cursor, owner_id, owner_type)

                # If owner information is not found, skip this event
                if not owner_info:
                    continue

                # Else, add the owner information into the event
                event['ownerInfo'] = owner_info

                # Convert datetime objects to string
                if event['eventStartDate']:
                    event['eventStartDate'] = event['eventStartDate'].strftime('%Y-%m-%d')

                if event['eventEndDate']:
                    event['eventEndDate'] = event['eventEndDate'].strftime('%Y-%m-%d')

                # Append the event into the return_data
                return_data.append(event)

        return jsonify({
            'events': return_data
        }), 200

    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 500


# -----------------------------------------------------------------------------------------
# [GET] Get top trending events
# Purpose: Get top trending events (up to 30)
# Used: Events.vue (inside views/Users folder)
# Output: Possible return codes [200 - Retrieval success, 404 - No events, 500 - Internal server error]
@blueprint.route('/getTrendingEvents', methods=['GET'])
def getTrendingEvents():
    return_data = []

    try:
        with db_manager.get_cursor() as cursor:
            # Step 1: Get the top 30 upcoming events
            cursor.execute('SELECT * FROM events WHERE "eventStartDate" >= CURRENT_DATE ORDER BY "numAttendees" DESC LIMIT 30')
            events = cursor.fetchall()

            if not events:
                return jsonify({'error': 'No events'}), 404

            # Step 2: Extract relevant information
            for event in events:
                top_event = {}
                top_event['eventID'] = event['id']
                top_event['eventName'] = event['eventName']
                top_event['eventDesc'] = event['eventDesc']
                top_event['eventType'] = event['eventType']
                top_event['eventStartDate'] = event['eventStartDate'].strftime('%Y-%m-%d')

                if event['eventEndDate'] is not None:
                    top_event['eventEndDate'] = event['eventEndDate'].strftime('%Y-%m-%d')
                
                if event['eventStartTime'] is not None:
                    top_event['eventStartTime'] = event['eventStartTime'].strftime('%H:%M')

                if event['eventEndTime'] is not None:
                    top_event['eventEndTime'] = event['eventEndTime'].strftime('%H:%M')

                top_event['numAttendees'] = event['numAttendees']
                top_event['eventBanners'] = event['eventBanners']
            
                return_data.append(top_event)
            
            return jsonify({
                'events': return_data
            }), 200

    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 500


# -----------------------------------------------------------------------------------------
# [GET] Get past trending events (within last 24 months, ordered by attendees)
# Purpose: Get past trending events for Past Trending Events section
# Used: Events.vue (inside views/Users folder)
# Output: Possible return codes [200 - Retrieval success, 404 - No events, 500 - Internal server error]
@blueprint.route('/getPastTrendingEvents', methods=['GET'])
def getPastTrendingEvents():
    return_data = []

    try:
        with db_manager.get_cursor() as cursor:
            # Get past events from last 24 months, ordered by attendees
            cursor.execute('''
                SELECT * FROM events 
                WHERE "eventStartDate" < CURRENT_DATE 
                AND "eventStartDate" >= CURRENT_DATE - INTERVAL '24 months'
                ORDER BY "numAttendees" DESC
            ''')
            events = cursor.fetchall()

            if not events:
                return jsonify({'error': 'No past trending events'}), 404

            # Extract relevant information
            for event in events:
                past_event = {}
                past_event['eventID'] = event['id']
                past_event['eventName'] = event['eventName']
                past_event['eventDesc'] = event['eventDesc']
                past_event['eventType'] = event['eventType']
                past_event['eventStartDate'] = event['eventStartDate'].strftime('%Y-%m-%d')

                if event['eventEndDate'] is not None:
                    past_event['eventEndDate'] = event['eventEndDate'].strftime('%Y-%m-%d')
                
                if event['eventStartTime'] is not None:
                    past_event['eventStartTime'] = event['eventStartTime'].strftime('%H:%M')

                if event['eventEndTime'] is not None:
                    past_event['eventEndTime'] = event['eventEndTime'].strftime('%H:%M')

                past_event['numAttendees'] = event['numAttendees']
                past_event['eventBanners'] = event['eventBanners']
            
                return_data.append(past_event)
            
            return jsonify({
                'events': return_data
            }), 200

    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 500


# -----------------------------------------------------------------------------------------
# [GET] Get upcoming events by brands/venues/users that the user is following
# Purpose: Get upcoming events by brands/venues/users that the user is following
# Used: Events.vue (inside views/Users folder)
# Output: Possible return codes [200 - Retrieval success, 404 - No events, 500 - Internal server error]
@blueprint.route('/getUpcomingFollowingEvents/<user_id>/<user_type>', methods=['GET'])
def getUpcomingFollowingEvents(user_id, user_type):
    return_data = []    

    try:
        with db_manager.get_cursor() as cursor:
            # Step 1: Get user follow list
            cursor.execute('SELECT * FROM "usersFollowLists" WHERE "userId" = %s', (user_id,))
            follow_list = cursor.fetchone()

            if not follow_list:
                return jsonify({'error': 'No events'}), 404

            follow_users = follow_list['users']
            follow_producers = follow_list['producers']
            follow_venues = follow_list['venues'] 

            # Step 2: Get the upcoming events by the brands/venues/users that the user is following
            cursor.execute('''
                SELECT * FROM events 
                WHERE 
                    ("eventOwnerType" = 'user' AND "eventOwnerID" = ANY(%s::int[])) 
                    OR ("eventOwnerType" = 'producer' AND "eventOwnerID" = ANY(%s::int[])) 
                    OR ("eventOwnerType" = 'venue' AND "eventOwnerID" = ANY(%s::int[])) 
                AND "eventStartDate" >= CURRENT_DATE 
                ORDER BY "eventStartDate" ASC, "eventStartTime" ASC 
                LIMIT 5
            ''', (follow_users, follow_producers, follow_venues))

            events = cursor.fetchall()

            if not events:
                return jsonify({'error': 'No events'}), 404

            # Step 3: Format the return data
            for event in events:
                event_details = {}
                event_details['eventID'] = event['id']
                event_details['eventName'] = event['eventName']
                event_details['eventDesc'] = event['eventDesc']
                event_details['eventType'] = event['eventType']
                event_details['eventStartDate'] = event['eventStartDate'].strftime('%Y-%m-%d')

                if event['eventEndDate'] is not None:
                    event_details['eventEndDate'] = event['eventEndDate'].strftime('%Y-%m-%d')
                if event['eventStartTime'] is not None:
                    event_details['eventStartTime'] = event['eventStartTime'].strftime('%H:%M')
                if event['eventEndTime'] is not None:
                    event_details['eventEndTime'] = event['eventEndTime'].strftime('%H:%M')

                event_details['eventBanners'] = event['eventBanners']

                return_data.append(event_details)

            return jsonify({
                'events': return_data
            }), 200

    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 500


# -----------------------------------------------------------------------------------------
# [GET] Get past events by the user 
# Purpose: Get past events by the user
# Used: Events.vue (inside views/Users folder)
# Output: Possible return codes [200 - Retrieval success, 404 - No events, 500 - Internal server error]
@blueprint.route('/getUserPastEvents/<user_id>/<offset>', methods=['GET'])
def getUserPastEvents(user_id, offset):
    return_data = []

    # Set the limit here
    limit = 5

    try:
        with db_manager.get_cursor() as cursor:
            today_date = datetime.now().date()

            # Step 2: Get the past events by the user attended
            cursor.execute('SELECT * FROM "eventAttendees" WHERE "userID" = %s AND "eventDate" < %s ORDER BY "eventDate" DESC, "eventStartTime" DESC LIMIT %s OFFSET %s', (user_id, today_date, limit, offset,))
            events = cursor.fetchall()

            if not events:
                return jsonify({'error': 'No events'}), 404

            # Step 3: Get the event information
            for event in events:

                cursor.execute('SELECT * FROM events WHERE id = %s', (event['eventID'],))
                event_info = cursor.fetchone()

                if not event_info:
                    continue

                # Format the event information
                ev = {}
                ev['eventID'] = event_info['id']
                ev['eventName'] = event_info['eventName']
                ev['eventDesc'] = event_info['eventDesc']
                ev['eventType'] = event_info['eventType']
                ev['eventStartDate'] = event_info['eventStartDate'].strftime('%Y-%m-%d')

                if event_info['eventEndDate'] is not None:
                    ev['eventEndDate'] = event_info['eventEndDate'].strftime('%Y-%m-%d')
                if event_info['eventStartTime'] is not None:
                    ev['eventStartTime'] = event_info['eventStartTime'].strftime('%H:%M')
                if event_info['eventEndTime'] is not None:
                    ev['eventEndTime'] = event_info['eventEndTime'].strftime('%H:%M')
                    
                ev['eventBanners'] = event_info['eventBanners']

                # Append the event into the return_data
                return_data.append(ev)

            return jsonify({
                'events': return_data
            }), 200

    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 500


# -----------------------------------------------------------------------------------------
# [GET] Get upcoming events by the user
# Purpose: Get upcoming events by the user
# Used: Events.vue (inside views/Users folder)
# Output: Possible return codes [200 - Retrieval success, 404 - No events, 500 - Internal server error]
@blueprint.route('/getUserUpcomingEvents/<user_id>/<user_type>/<offset>', methods=['GET'])
def getUserUpcomingEvents(user_id, user_type, offset):
    return_data = []

    # Set the limit here
    limit = 5

    try:
        with db_manager.get_cursor() as cursor:
            # Get today's date
            today_date = datetime.now().date()

            # First select query is to get the events that the user is attending
            # Second select query is to get the events that the user is the owner of
            query = '''
                SELECT 
                    e.*,
                    'attending' AS role
                FROM "eventAttendees" ea
                JOIN "events" e ON ea."eventID" = e."id"
                WHERE ea."userID" = %s 
                AND ea."attendeeType" = %s
                AND e."eventStartDate" >= %s

                UNION

                SELECT 
                    e.*,
                    'owner' AS role
                FROM "events" e
                WHERE e."eventOwnerID" = %s
                AND e."eventOwnerType" = %s
                AND e."eventStartDate" >= %s

                ORDER BY "eventStartDate" ASC, "eventStartTime" ASC
                LIMIT %s OFFSET %s
            '''

            cursor.execute(query, (
                user_id, user_type, today_date,         # For attendee query
                user_id, user_type, today_date, # For owner query
                limit, offset                # LIMIT and OFFSET
            ))
            events = cursor.fetchall()


            if not events:
                return jsonify({'error': 'No events'}), 404
            
            # Step 2: Get the event information
            for event in events:

                cursor.execute('SELECT * FROM events WHERE id = %s', (event['id'],))
                event_info = cursor.fetchone()

                if not event_info:
                    continue

                # Format the event information
                ev = {}
                ev['eventID'] = event_info['id']
                ev['eventName'] = event_info['eventName']
                ev['eventDesc'] = event_info['eventDesc']
                ev['eventType'] = event_info['eventType']
                ev['eventStartDate'] = event_info['eventStartDate'].strftime('%Y-%m-%d')

                if event_info['eventEndDate'] is not None:
                    ev['eventEndDate'] = event_info['eventEndDate'].strftime('%Y-%m-%d')
                if event_info['eventStartTime'] is not None:
                    ev['eventStartTime'] = event_info['eventStartTime'].strftime('%H:%M')
                if event_info['eventEndTime'] is not None:
                    ev['eventEndTime'] = event_info['eventEndTime'].strftime('%H:%M')

                ev['eventBanners'] = event_info['eventBanners']

                # Append the event into the return_data
                return_data.append(ev)

        return jsonify({
            'events': return_data
        }), 200

    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 500


# -----------------------------------------------------------------------------------------
# [GET] Get recently added events
# Purpose: Get recently added events
# Used: Events.vue (inside views/Users folder)
# Output: Possible return codes [200 - Retrieval success, 404 - No events, 500 - Internal server error]
@blueprint.route('/getRecentlyAddedEvents', methods=['GET'])
def getRecentlyAddedEvents():
    return_data = []

    try:
        with db_manager.get_cursor() as cursor:
            # Step 1: Get the recently added events
            cursor.execute('SELECT * FROM events WHERE "eventEndDate" >= CURRENT_DATE ORDER BY "createdDate"  DESC LIMIT 5')
            events = cursor.fetchall()

            if not events:
                return jsonify({'error': 'No events'}), 404

            # Step 2: Extract relevant information
            for event in events:
                event_details = {}
                event_details['eventID'] = event['id']
                event_details['eventName'] = event['eventName']
                event_details['eventDesc'] = event['eventDesc']
                event_details['eventType'] = event['eventType']
                event_details['eventStartDate'] = event['eventStartDate'].strftime('%Y-%m-%d')

                if event['eventEndDate'] is not None:
                    event_details['eventEndDate'] = event['eventEndDate'].strftime('%Y-%m-%d')
                if event['eventStartTime'] is not None:
                    event_details['eventStartTime'] = event['eventStartTime'].strftime('%H:%M')
                if event['eventEndTime'] is not None:
                    event_details['eventEndTime'] = event['eventEndTime'].strftime('%H:%M')

                event_details['createdDate'] = event['createdDate'].strftime('%Y-%m-%d')
                event_details['eventBanners'] = event['eventBanners']
                
                return_data.append(event_details)
            
            return jsonify({
                'events': return_data
            }), 200

    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 500


# -----------------------------------------------------------------------------------------
# [GET] Search events by event name
# Purpose: Search events by event name
# Used: Events.vue (inside views/Users folder)
# Output: Possible return codes [200 - Retrieval success, 404 - No events, 500 - Internal server error]
@blueprint.route('/searchEvents/<search_query>/<offset>', methods=['GET'])
def searchEvents(search_query, offset):
    return_data = []

    try:
        with db_manager.get_cursor() as cursor:
            # Step 1: Search the events by event name
            cursor.execute('SELECT * FROM events WHERE "eventName" ILIKE %s LIMIT 10 OFFSET %s', (f'%{search_query}%', offset,))
            events = cursor.fetchall()

            if not events:
                return jsonify({'error': 'No events'}), 404

            # Step 2: Extract relevant information
            for event in events:
                event_details = {}
                event_details['eventID'] = event['id']
                event_details['eventName'] = event['eventName']
                event_details['eventDesc'] = event['eventDesc']
                event_details['eventType'] = event['eventType']
                event_details['eventStartDate'] = event['eventStartDate'].strftime('%Y-%m-%d')

                if event['eventEndDate'] is not None:
                    event_details['eventEndDate'] = event['eventEndDate'].strftime('%Y-%m-%d')
                if event['eventStartTime'] is not None:
                    event_details['eventStartTime'] = event['eventStartTime'].strftime('%H:%M')
                if event['eventEndTime'] is not None:
                    event_details['eventEndTime'] = event['eventEndTime'].strftime('%H:%M')

                event_details['eventBanners'] = event['eventBanners']
                event_details['numAttendees'] = event['numAttendees']

                return_data.append(event_details)

            return jsonify({
                'events': return_data
            }), 200

    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 500


# -----------------------------------------------------------------------------------------
# [GET] Check if user can create more events
# Purpose: Check if user can create more events
# Used: 
# Output: Possible return codes [200 - User can create more events, 400 - User cannot create more events, 500 - Internal server error]
@blueprint.route('/canCreateEvents/<user_id>/<user_type>', methods=['GET'])
def canCreateEvents(user_id, user_type):
    try:
        # Check for user type: user - needs to have minimum proof points
        if user_type == 'user':
            canCreateTuple = pointsHelperFunc.check_user_can_create_event(user_id)

            if not canCreateTuple[0]:
                if canCreateTuple[1] == 'insufficient points':
                    return jsonify({
                        'canCreate': False,
                        'reason': 'insufficient points',
                        'message': 'You need a minimum of 100 proof points to create events.',
                        'pointsNeeded': canCreateTuple[2]
                    }), 200
                
                else:
                    return jsonify({
                        'canCreate': False,
                        'reason': 'max events created',
                        'message': 'You have reached the limit of events you can create this month. This will reset again next month!',
                        'numEventsCreated': canCreateTuple[2]
                    }), 200
            
            # User can create an event
            return jsonify({
                'canCreate': True,
                'message': 'User can create more events as per the limit'
            }), 200

        # For producers and venues, use the existing logic
        else:
            with db_manager.get_cursor() as cursor:
                # Step 1: Check if the user can create more events
                can_create = canCreateMoreEvents(cursor, user_id, user_type)

                if not can_create[0]:
                    return jsonify({
                        'canCreate': False,
                        'message': 'You have reached the limit of events you can create this month. This will reset again next month!',
                        'limit': can_create[1]
                    }), 200

                return jsonify({
                    'canCreate': True,
                    'message': 'User can create more events as per the limit'
                }), 200

    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 500


# -----------------------------------------------------------------------------------------
# [POST] Create an event
# Purpose: Create an event
# Used: EventBox.vue (inside components folder)
# Input:
#    1. eventName
#    2. eventDesc
#    3. eventStartDate
#    4. eventEndDate
#    5. eventStartTime
#    6. eventEndTime
#    7. eventLimit
#    8. eventBanners [Optional]
#    9. ticketed
#    10. paidEvent 
#    11. eventLocation
#    12. paymentLink [Optional]
#    13. eventOwnerID
#    14. eventOwnerType
# Output: Possible return codes [201 - Creation success, 400 - Missing required fields or required fields are empty / Event owner not found, 500 - Internal server error]
@blueprint.route('/createEvent', methods=['POST'])
def createEvent():
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        with db_manager.get_cursor() as cursor:
            # Step 1: Get the input data
            data = request.json

            required_fields = ['eventName', 'eventDesc', 'eventType', 'eventStartDate', 'ticketed', 'eventOwnerID', 'eventOwnerType']

            # Check if the required fields are present and not empty
            for field in required_fields:
                if field not in data or data[field] is None or data[field] == '':
                    return jsonify({'error': f'Missing or empty required field: {field}'}), 400
                
            # Step 2: Check if the event owner exist
            owner_info = getUserInfoByID(cursor, data['eventOwnerID'], data['eventOwnerType'])

            if not owner_info:
                return jsonify({'error': 'Event owner not found'}), 400
            
            # Step 3: Check if event banners are present
            event_banner = []
            if 'eventBanners' in data and len(data['eventBanners']) > 0:

                # Upload each image (base64Image) to S3
                for image in data['eventBanners']:
                    base64_string = re.sub(r'^data:image\/[a-zA-Z]+;base64,', '', image)
                    url = s3Images.uploadBase64ImageToS3(base64_string)
                    if url:
                        event_banner.append(url)

            # Convert the list to PostgreSQL array format before insertion
            if event_banner:
                event_banner_pg = "{" + ",".join([f'"{url}"' for url in event_banner]) + "}"  # Example: {"url1", "url2"}
            else:
                event_banner_pg = None  # NULL for no banners
            
            # Step 4: Convert datetime values to datetime objects
            data['eventStartDate'] = datetime.strptime(data['eventStartDate'], '%Y-%m-%d')

            if data['eventEndDate'] != '' and data['eventEndDate'] is not None:
                data['eventEndDate'] = datetime.strptime(data['eventEndDate'], '%Y-%m-%d')
            else:
                data['eventEndDate'] = None

            if data['eventStartTime'] == '' or data['eventStartTime'] is None:
                data['eventStartTime'] = None

            if data['eventEndTime'] == '' or data['eventEndTime'] is None:
                data['eventEndTime'] = None


            # Check if paymentLink is provided
            if 'paymentLink' in data and not data['paymentLink']:
                payment_link = None
            else:
                payment_link = data['paymentLink']

            # Set the default value for eventLimit if not provided
            if data['eventLimit'] != '' and data['eventLimit'] is None:
                data['eventLimit'] = 1000000
            # If eventLimit is provided, convert it to int
            else:
                data['eventLimit'] = int(data['eventLimit'])

            # Handle passcodes - convert array with limits to JSONB format
            passcode_data = data.get('eventPasscodes', [])
            passcode = None
            
            if passcode_data and isinstance(passcode_data, list):
                valid_passcodes = []
                for item in passcode_data:
                    # Handle new format (objects with code and limit)
                    if isinstance(item, dict) and 'code' in item and 'limit' in item:
                        code = item['code'].strip() if item['code'] else ''
                        limit = item['limit']
                        if code and isinstance(limit, int) and limit > 0:
                            valid_passcodes.append({"code": code, "limit": limit})
                
                # Convert to JSON string for JSONB storage
                if valid_passcodes:
                    passcode = json.dumps(valid_passcodes)

            # Get today's date as the createdDate
            created_date = datetime.now().date()

            # Step 5: Insert the event into the database
            cursor.execute(
                '''
                INSERT INTO events
                  ("eventName", "eventDesc", "eventType",
                   "eventStartDate", "eventEndDate",
                   "eventStartTime", "eventEndTime",
                   "eventLimit", "eventBanners", ticketed,
                   "paidEvent", "eventLocation", "paymentLink",
                   "eventOwnerID", "eventOwnerType",
                   "numAttendees", "createdDate", passcode)
                VALUES (
                  %s, %s, %s,
                  %s, %s,
                  %s, %s,
                  %s, %s, %s,
                  %s, %s, %s,
                  %s, %s,
                  0, %s, %s
                )
                RETURNING id
                ''',
                (
                    data['eventName'], data['eventDesc'], data['eventType'],
                    data['eventStartDate'], data['eventEndDate'],
                    data['eventStartTime'], data['eventEndTime'],
                    data['eventLimit'], event_banner_pg, data['ticketed'],
                    data.get('paidEvent'), data.get('eventLocation'), payment_link,
                    data['eventOwnerID'], data['eventOwnerType'],
                    created_date, passcode
                )
            )
            new_event = cursor.fetchone()
            new_event_id = new_event['id']
            print("hello1")

            # Step 6: Notify all followers of the owner
            # Determine display name
            if data['eventOwnerType'] == 'user':
                owner_name = owner_info['displayName']
            elif data['eventOwnerType'] == 'producer':
                owner_name = owner_info['producerName']
            else:
                owner_name = owner_info['venueName']
            print("data: ", data)
            # Fetch followers from usersFollowLists
            key = str(data['eventOwnerID'])
            if data['eventOwnerType'] == 'producer':
                cursor.execute(
                    'SELECT "userId" FROM "usersFollowLists" WHERE %s = ANY(producers)',
                    (key,)
                )
            else:
                cursor.execute(
                    'SELECT "userId" FROM "usersFollowLists" WHERE %s = ANY(venues)',
                    (key,)
                )
            print("hello2")
            followers = cursor.fetchall()
            print("Followers fetched:", followers)

            for f in followers:
                notification_data = {
                    'userId': f['userId'],
                    'userType': 'user',
                    'notiTabs': 'venues & producers',
                    'notiType': 'event_created',
                    'image': None,
                    'link': f'/event/{new_event_id}/{data["eventName"]}',
                    'message': f'{owner_name} created a new event: {data["eventName"]}',
                    'createdAt': current_time,
                }
                print(notification_data)
                notifications.add_notification_to_db(notification_data)
            
            return jsonify({'message': 'Event created successfully'}), 201

    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 400


# -----------------------------------------------------------------------------------------
# [PUT] Update an event 
# Purpose: Update an event
# Used:
# Input: 
#    1. eventName
#    2. eventDesc
#    3. eventStartDate
#    4. eventEndDate
#    5. eventStartTime
#    6. eventEndTime
#    7. eventLimit
#    8. eventBanners [Optional if no change and no image provided during creation]
#    9. ticketed
#    10. paidEvent
#    11. eventLocation
#    12. eventLink [Optional]
#    13. eventOwnerID
#    14. eventOwnerType
# Output: Possible return codes [200 - Update success, 400 - Missing required fields or required fields are empty / No such event , 403 - Unauthorized to update the event, 500 - Internal server error]
@blueprint.route('/updateEvent', methods=['PUT'])
def updateEvent():

    try:
        with db_manager.get_cursor() as cursor:
            # Step 1: Get the input data
            data = request.json

            required_fields = ['eventID', 'eventOwnerID', 'eventOwnerType']

            # Check if the required fields are present and not empty
            for field in required_fields:
                if field not in data or not data[field]:
                    return jsonify({'error': f'Missing or empty required field: {field}'}), 400


            # Step 2: Check if the event exist
            cursor.execute('SELECT * FROM events WHERE id = %s', (data['eventID'],))
            event = cursor.fetchone()

            if not event:
                return jsonify({'error': 'No such event'}), 400

            # Step 3: Check if the user who is updating the event is the owner of the event
            if event['eventOwnerID'] != data['eventOwnerID'] and event['eventOwnerType'] != data['eventOwnerType']:
                return jsonify({'error': 'Unauthorized to update this event'}), 403

            # Step 4: Build update query (only update the fields that has been changed / provided)
            update_fields = []
            update_values = []

            if 'eventName' in data and data['eventName']:
                update_fields.append('"eventName" = %s')
                update_values.append(data['eventName'])
            if 'eventDesc' in data and data['eventDesc']:
                update_fields.append('"eventDesc" = %s')
                update_values.append(data['eventDesc'])
            if 'eventType' in data and data['eventType']:
                update_fields.append('"eventType" = %s')
                update_values.append(data['eventType'])
            if 'eventStartDate' in data and data['eventStartDate']:
                update_fields.append('"eventStartDate" = %s')
                update_values.append(datetime.strptime(data['eventStartDate'], '%Y-%m-%d'))
            if 'eventEndDate' in data and data['eventEndDate']:
                update_fields.append('"eventEndDate" = %s')
                update_values.append(datetime.strptime(data['eventEndDate'], '%Y-%m-%d'))
            if 'eventStartTime' in data and data['eventStartTime']:
                update_fields.append('"eventStartTime" = %s')
                update_values.append(datetime.strptime(data['eventStartTime'], '%H:%M'))
            if 'eventEndTime' in data and data['eventEndTime']:
                update_fields.append('"eventEndTime" = %s')
                update_values.append(datetime.strptime(data['eventEndTime'], '%H:%M'))
            if 'eventLimit' in data and data['eventLimit']:
                update_fields.append('"eventLimit" = %s')
                update_values.append(int(data['eventLimit']))
            if 'ticketed' in data and data['ticketed']:
                update_fields.append('ticketed = %s')
                update_values.append(data['ticketed'])
            if 'paidEvent' in data and data['paidEvent']:
                update_fields.append('"paidEvent" = %s')
                update_values.append(data['paidEvent'])
            if 'eventLocation' in data and data['eventLocation']:
                update_fields.append('"eventLocation" = %s')
                update_values.append(data['eventLocation'])
            if 'paymentLink' in data and data['paymentLink']:
                update_fields.append('"paymentLink" = %s')
                update_values.append(data['paymentLink'])
            if 'eventBanners' in data:
                if len(data['eventBanners']) == 0:
                    update_fields.append('"eventBanners" = %s')
                    update_values.append(None)
                
                # Loop through current eventBanners and check if they are not in the new eventBanners
                # If not, remove them from the eventBanners
                current_event_banners = event['eventBanners']

                if current_event_banners is not None:
                    for current_banner in current_event_banners:
                        if current_banner not in data['eventBanners']:
                            # Remove the banner from S3
                            s3Images.deleteImageFromS3(current_banner)

                # Upload each image (base64Image) to S3 in the new eventBanners
                event_banner = []
                for image in data['eventBanners']:
                    
                    if not image:
                        continue

                    # Check if the image is already in S3
                    if 'http' in image:
                        event_banner.append(image)
                        continue
                    else:

                        # Remove the base64 prefix if it exists
                        base64_string = re.sub(r'^data:image\/[a-zA-Z]+;base64,', '', image)
                        url = s3Images.uploadBase64ImageToS3(base64_string)
                        if url:
                            event_banner.append(url)

                # Convert the list to PostgreSQL array format before insertion
                if event_banner:
                    event_banner_pg = "{" + ",".join([f'"{url}"' for url in event_banner]) + "}"
                    update_fields.append('"eventBanners" = %s')
                    update_values.append(event_banner_pg)
            
            # Handle passcode updates - convert array with limits to JSONB format
            if 'eventPasscodes' in data:
                passcode_data = data.get('eventPasscodes')
                passcode = None
                
                if passcode_data and isinstance(passcode_data, list):
                    valid_passcodes = []
                    for item in passcode_data:
                        # Handle new format (objects with code and limit)
                        if isinstance(item, dict) and 'code' in item and 'limit' in item:
                            code = item['code'].strip() if item['code'] else ''
                            limit = item['limit']
                            if code and isinstance(limit, int) and limit > 0:
                                valid_passcodes.append({"code": code, "limit": limit})
                    
                    # Convert to JSON string for JSONB storage
                    if valid_passcodes:
                        passcode = json.dumps(valid_passcodes)
                
                update_fields.append('"passcode" = %s')
                update_values.append(passcode)

            # Step 4: Update the event
            if update_fields:
                update_query = ', '.join(update_fields)
                update_values.append(data['eventID'])
                cursor.execute(f'UPDATE events SET {update_query} WHERE id = %s', tuple(update_values))

            return jsonify({'message': 'Event updated successfully'}), 200

    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 500


# -----------------------------------------------------------------------------------------
# [DELETE] Delete an event
# Purpose: Delete an event
# Used:
# Input:
#    1. eventID
#    2. eventOwnerID
#    3. eventOwnerType
# Output: Possible return codes [200 - Deletion success, 400 - Missing required fields or required fields are empty / No such event, 403 - Unauthorized to delete the event, 500 - Internal server error]
@blueprint.route('/deleteEvent', methods=['DELETE'])
def deleteEvent():

    try:
        with db_manager.get_cursor() as cursor:
            # Step 1: Get the input data
            data = request.json

            required_fields = ['eventID', 'eventOwnerID', 'eventOwnerType']

            # Check if the required fields are present and not empty
            for field in required_fields:
                if field not in data or not data[field]:
                    return jsonify({'error': f'Missing or empty required field: {field}'}), 400

            # Step 2: Check if the event exist
            cursor.execute('SELECT * FROM events WHERE id = %s', (data['eventID'],))
            event = cursor.fetchone()

            if not event:
                return jsonify({'error': 'No such event'}), 400

            # Convert eventOwnerID to integer
            data['eventOwnerID'] = int(data['eventOwnerID'])

            # Step 3: Check if the user who is deleting the event is the owner of the event
            if event['eventOwnerID'] != data['eventOwnerID'] or event['eventOwnerType'] != data['eventOwnerType']:
                return jsonify({'error': 'Unauthorized to delete this event'}), 403
            
            # Step 4: Delete all the attendees of the event
            cursor.execute('DELETE FROM "eventAttendees" WHERE "eventID" = %s', (data['eventID'],))

            # Step 5: Delete the event
            cursor.execute('DELETE FROM events WHERE id = %s', (data['eventID'],))

            return jsonify({'message': 'Event deleted successfully'}), 200

    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 500


# -----------------------------------------------------------------------------------------
# [PUT] Lock event signups
# Purpose: Set signupOpen to false for an event, preventing new RSVPs and withdrawals
# Used: SpecificEventPage.vue (inside views folder)
# Output: Possible return codes [200 - Success, 400 - Missing required fields / No such event, 403 - Unauthorized, 500 - Internal server error]
@blueprint.route('/lockSignups', methods=['PUT'])
def lockSignups():

    try:
        with db_manager.get_cursor() as cursor:
            data = request.get_json()

            # Step 1: Check if all required fields are provided
            if not data or not data.get('eventID') or not data.get('eventOwnerID') or not data.get('eventOwnerType'):
                return jsonify({'error': 'Missing required fields'}), 400

            # Step 2: Check if the event exists
            cursor.execute('SELECT * FROM events WHERE id = %s', (data['eventID'],))
            event = cursor.fetchone()

            if not event:
                return jsonify({'error': 'No such event'}), 400

            # Convert eventOwnerID to integer for comparison
            data['eventOwnerID'] = int(data['eventOwnerID'])

            # Step 3: Check if the user who is locking signups is the owner of the event
            if event['eventOwnerID'] != data['eventOwnerID'] or event['eventOwnerType'] != data['eventOwnerType']:
                return jsonify({'error': 'Unauthorized to lock signups for this event'}), 403
            
            # Step 4: Check if signups are already locked
            if not event['signupOpen']:
                return jsonify({'error': 'Signups are already locked for this event'}), 400

            # Step 5: Lock the signups by setting signupOpen to false
            cursor.execute('UPDATE events SET "signupOpen" = false WHERE id = %s', (data['eventID'],))

            return jsonify({'message': 'Event signups locked successfully'}), 200

    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 500


# -----------------------------------------------------------------------------------------
# [PUT] Unlock event signups
# Purpose: Set signupOpen to true for an event, allowing new RSVPs and withdrawals
# Used: SpecificEventPage.vue (inside views folder)
# Output: Possible return codes [200 - Success, 400 - Missing required fields / No such event, 403 - Unauthorized, 500 - Internal server error]
@blueprint.route('/unlockSignups', methods=['PUT'])
def unlockSignups():

    try:
        with db_manager.get_cursor() as cursor:
            data = request.get_json()

            # Step 1: Check if all required fields are provided
            if not data or not data.get('eventID') or not data.get('eventOwnerID') or not data.get('eventOwnerType'):
                return jsonify({'error': 'Missing required fields'}), 400

            # Step 2: Check if the event exists
            cursor.execute('SELECT * FROM events WHERE id = %s', (data['eventID'],))
            event = cursor.fetchone()

            if not event:
                return jsonify({'error': 'No such event'}), 400

            # Convert eventOwnerID to integer for comparison
            data['eventOwnerID'] = int(data['eventOwnerID'])

            # Step 3: Check if the user who is unlocking signups is the owner of the event
            if event['eventOwnerID'] != data['eventOwnerID'] or event['eventOwnerType'] != data['eventOwnerType']:
                return jsonify({'error': 'Unauthorized to unlock signups for this event'}), 403
            
            # Step 4: Check if signups are already unlocked
            if event['signupOpen']:
                return jsonify({'error': 'Signups are already open for this event'}), 400

            # Step 5: Unlock the signups by setting signupOpen to true
            cursor.execute('UPDATE events SET "signupOpen" = true WHERE id = %s', (data['eventID'],))

            return jsonify({'message': 'Event signups unlocked successfully'}), 200

    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 500


# -----------------------------------------------------------------------------------------
# [GET] Get all attendees of an event
# Purpose: Get all attendees of an event
# Used: SpecifiEventPage.vue (inside views folder)
# Output: Possible return codes [200 - Retrieval success, 400 - Missing required fields or required fields are empty / No such event, 500 - Internal server error]
@blueprint.route('/getAttendees/<event_id>', methods=['GET'])
def getAttendees(event_id):

    try:
        with db_manager.get_cursor() as cursor:
            # Step 1: Get the event information
            cursor.execute('SELECT * FROM events WHERE id = %s', (event_id,))
            event = cursor.fetchone()

            if not event:
                return jsonify({'error': 'No such event'}), 400

            # Step 2: Get the attendees information
            cursor.execute('SELECT * FROM "eventAttendees" WHERE "eventID" = %s', (event_id,))
            attendees = cursor.fetchall()

            return_data = []

            for attendee in attendees:
                user_id = attendee['userID']
                user_type = attendee['attendeeType']

                user_info = getUserInfoByID(cursor, user_id, user_type)

                # If user information is not found, skip this attendee
                if not user_info:
                    continue

                # Adding the new tracking fields
                user_info['hasPaid'] = attendee.get('hasPaid', False)
                user_info['attendanceStatus'] = attendee.get('attendanceStatus', 'Not Checked In')
                user_info['rsvpDate'] = attendee.get('rsvpTimestamp')
                user_info['eventDate'] = attendee.get('eventDate')
                user_info['attendeeId'] = attendee['id']
                
                # Adding the new attendee contact information fields
                user_info['firstName'] = attendee.get('firstName')
                user_info['lastName'] = attendee.get('lastName')
                user_info['phoneNumber'] = attendee.get('phoneNumber')
                user_info['email'] = attendee.get('email')

                # Append the user information into the return_data
                return_data.append(user_info)

            return jsonify({
                'attendees': return_data
            }), 200

    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 500


# -----------------------------------------------------------------------------------------
# [GET] Check if a user is attending an event
# Purpose: Check if a user is attending an event
# Used: SpecifiEventPage.vue (inside views folder)
# Output: Possible return codes [200 - Retrieval success, 400 - Missing required fields or required fields are empty / No such event, 500 - Internal server error]
@blueprint.route('/checkAttendance/<event_id>/<user_id>/<user_type>', methods=['GET'])
def checkAttendance(event_id, user_id, user_type):

    try:
        with db_manager.get_cursor() as cursor:
            # Step 1: Get the event information
            cursor.execute('SELECT * FROM events WHERE id = %s', (event_id,))
            event = cursor.fetchone()

            if not event:
                return jsonify({'error': 'No such event'}), 400

            # Step 2: Check if the user is attending the event
            cursor.execute('SELECT * FROM "eventAttendees" WHERE "eventID" = %s AND "userID" = %s AND "attendeeType" = %s', (event_id, user_id, user_type,))
            attendee = cursor.fetchone()

            if not attendee:
                return jsonify({'attendance': False}), 200

            return jsonify({'attendance': True}), 200

    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 500


# -----------------------------------------------------------------------------------------
# [POST] Add an attendee to an event
# Purpose: Add an attendee to an event
# Used: SpecifiEventPage.vue (inside views folder)
# Input:
#    1. eventID
#    2. userID
#    3. userType
# Output: Possible return codes [201 - Creation success, 400 - Missing required fields or required fields are empty / No such event / User not found, 500 - Internal server error]
@blueprint.route('/addAttendee', methods=['POST'])
def addAttendee():
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        with db_manager.get_cursor() as cursor:
            # Step 1: Get the input data
            data = request.json

            required_fields = ['eventID', 'userID', 'userType']
            attendee_info_fields = ['firstName', 'lastName', 'phoneNumber', 'email']

            # Check if the required fields are present and not empty
            for field in required_fields:
                if field not in data or not data[field]:
                    return jsonify({'error': f'Missing or empty required field: {field}'}), 400

            # Check if attendee information fields are present (new feature)
            # These fields are optional for backward compatibility with existing RSVPs
            attendee_info = {}
            for field in attendee_info_fields:
                if field in data and data[field] and data[field].strip():
                    # Validate field length
                    if len(data[field].strip()) > 50:
                        return jsonify({'error': f'{field} must be 50 characters or less'}), 400
                    attendee_info[field] = data[field].strip()
                else:
                    attendee_info[field] = None

            # Step 2: Check if the event exist
            cursor.execute('SELECT * FROM events WHERE id = %s', (data['eventID'],))
            event = cursor.fetchone()

            if not event:
                return jsonify({'error': 'No such event'}), 400

            # Step 3: Check if the user exist
            user_info = getUserInfoByID(cursor, data['userID'], data['userType'])

            if not user_info:
                return jsonify({'error': 'User not found'}), 400

            # Step 3.5: Validate event passcode if required
            # passcode is now JSONB format: [{"code": "Merlion65", "limit": 50}, {"code": "Changi66", "limit": 30}] or None
            event_passcode = event.get('passcode')
            matched_passcode_code = None  # Store the master code that was matched
            
            # Check if event requires passcode: JSONB array exists and has valid passcode objects
            if event_passcode and isinstance(event_passcode, list) and len(event_passcode) > 0:
                # Check if any passcode object has a valid code
                has_valid_passcode = any(
                    isinstance(p, dict) and p.get('code') and str(p.get('code')).strip() 
                    for p in event_passcode
                )
                
                if has_valid_passcode:
                    # Get passcodes to try (array from frontend, or fallback to single passcode for backward compatibility)
                    user_passcodes = data.get('passcodes', [])
                    if not user_passcodes:
                        # Fallback to single passcode for backward compatibility
                        single_passcode = data.get('passcode', '')
                        user_passcodes = [single_passcode] if single_passcode else []
                    
                    if not user_passcodes or not any(pc.strip() for pc in user_passcodes):
                        return jsonify({'error': 'This event requires a passcode.'}), 400
                    
                    # Try each user passcode against each event passcode
                    passcode_found = False
                    matched_passcode_code = None
                    found_valid_but_limit_reached = False  # Track if we found valid passcode but hit limit
                    
                    for user_passcode in user_passcodes:
                        if not user_passcode.strip():
                            continue
                            
                        # Normalize user input (remove spaces and convert to lowercase)
                        normalized_user_passcode = ''.join(user_passcode.split()).lower()
                        
                        # Find matching passcode and check its usage limit
                        for passcode_obj in event_passcode:
                            if isinstance(passcode_obj, dict) and passcode_obj.get('code'):
                                master_code = str(passcode_obj['code']).strip()
                                passcode_limit = passcode_obj.get('limit', 0)
                                
                                # Normalize master code for comparison
                                normalized_master_code = ''.join(master_code.split()).lower()
                                
                                if normalized_user_passcode == normalized_master_code:
                                    # Check usage limit for this specific passcode
                                    cursor.execute('''
                                        SELECT COUNT(*) as usage_count
                                        FROM "eventAttendees" 
                                        WHERE "eventID" = %s AND "passcodeUsed" = %s
                                    ''', (data['eventID'], master_code))
                                    
                                    usage_result = cursor.fetchone()
                                    current_usage = usage_result['usage_count'] if usage_result else 0
                                    
                                    if current_usage >= passcode_limit:
                                        found_valid_but_limit_reached = True  # Mark that we found a valid passcode but it's at limit
                                        continue  # Try next passcode instead of failing immediately
                                    
                                    # Found valid passcode with available usage
                                    passcode_found = True
                                    matched_passcode_code = master_code  # Store the original master code
                                    break
                                    
                        if passcode_found:
                            break  # Exit outer loop if we found a valid passcode
                    
                    if not passcode_found:
                        # Prioritize limit reached message over generic wrong passcode message
                        if found_valid_but_limit_reached:
                            return jsonify({'error': 'This event has been fully signed up by your ticket class.'}), 400
                        else:
                            return jsonify({'error': 'Event passcode wrong'}), 400

            # Step 3.6: Check attendance limit for this event organizer on the same day
            cursor.execute('''
                SELECT COUNT(*) as attendance_count
                FROM "eventAttendees" ea
                JOIN events e ON ea."eventID" = e.id
                WHERE ea."userID" = %s 
                AND ea."attendeeType" = %s
                AND e."eventOwnerID" = %s
                AND e."eventOwnerType" = %s
                AND e."eventStartDate" = %s
                AND e."eventStartDate" >= CURRENT_DATE
                AND e.id != %s
            ''', (data['userID'], data['userType'], event['eventOwnerID'], event['eventOwnerType'], event['eventStartDate'], data['eventID']))
            
            attendance_result = cursor.fetchone()
            current_attendance_count = attendance_result['attendance_count'] if attendance_result else 0
            
            if current_attendance_count >= 2:
                return jsonify({'error': 'Maximum of 2 events from the same organiser on the same day reached'}), 400

            # Step 4: Check if the user is already an attendee
            cursor.execute('SELECT * FROM "eventAttendees" WHERE "eventID" = %s AND "userID" = %s AND "attendeeType" = %s', (data['eventID'], data['userID'], data['userType'],))
            attendee = cursor.fetchone()

            if attendee:
                return jsonify({'error': 'User is already an attendee'}), 400

            # Step 4.5: Check if event has reached its attendance limit
            if event['eventLimit'] and event['numAttendees'] >= event['eventLimit']:
                return jsonify({'error': 'Event is full. No more registrations allowed.'}), 400

            # Step 5: Add the attendee to the event
            cursor.execute('''
                INSERT INTO "eventAttendees" 
                ("eventID", "eventDate", "eventStartTime", "userID", "attendeeType", "attendeeStatus", "rsvpTimestamp", "firstName", "lastName", "phoneNumber", "email", "passcodeUsed") 
                VALUES (%s, %s, %s, %s, %s, TRUE, CURRENT_TIMESTAMP, %s, %s, %s, %s, %s)
            ''', (data['eventID'], event['eventStartDate'], event['eventStartTime'], data['userID'], data['userType'], 
                  attendee_info['firstName'], attendee_info['lastName'], attendee_info['phoneNumber'], attendee_info['email'], matched_passcode_code))

            # Step 6: Update the number of attendees in the event
            cursor.execute('UPDATE events SET "numAttendees" = "numAttendees" + 1 WHERE id = %s', (data['eventID'],))

            cursor.execute(
                'SELECT "eventName" FROM events WHERE id = %s',
                (data['eventID'],)
            )
            ev = cursor.fetchone()
            event_name = ev['eventName'] if ev and 'eventName' in ev else 'the event'

            # Build and send notification
            notification_data = {
                "userId":    data['userID'],
                "userType":  data['userType'],
                "notiTabs":  "forYou",
                "notiType":  "event_invite",
                "image":     None,
                "link":      f"/event/{data['eventID']}/{event_name}",
                "message":   f"You have been invited to '{event_name}' event",
                "createdAt": current_time
            }
            print("data for notification: ", notification_data)
            notifications.add_notification_to_db(notification_data)

            return jsonify({'message': 'Attendee added successfully'}), 201

    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 500


# -----------------------------------------------------------------------------------------
# [DELETE] Remove an attendee from an event
# Purpose: Remove an attendee from an event
# Used: SpecifiEventPage.vue (inside views folder)
# Input:
#    1. eventID
#    2. userID
#    3. userType
# Output: Possible return codes [200 - Deletion success, 400 - Missing required fields or required fields are empty / No such event / User not found, 500 - Internal server error]
@blueprint.route('/removeAttendee', methods=['DELETE'])
def removeAttendee():

    try:
        with db_manager.get_cursor() as cursor:
            # Step 1: Get the input data
            data = request.json

            required_fields = ['eventID', 'userID', 'userType']

            # Check if the required fields are present and not empty
            for field in required_fields:
                if field not in data or not data[field]:
                    return jsonify({'error': f'Missing or empty required field: {field}'}), 400

            # Step 2: Check if the event exist
            cursor.execute('SELECT * FROM events WHERE id = %s', (data['eventID'],))
            event = cursor.fetchone()

            if not event:
                return jsonify({'error': 'No such event'}), 400

            # Step 3: Check if the user exist
            user_info = getUserInfoByID(cursor, data['userID'], data['userType'])

            if not user_info:
                return jsonify({'error': 'User not found'}), 400

            # Step 4: Remove the attendee from the event
            cursor.execute('DELETE FROM "eventAttendees" WHERE "eventID" = %s AND "userID" = %s AND "attendeeType" = %s', (data['eventID'], data['userID'], data['userType'],))

            # Step 5: Update the number of attendees in the event
            cursor.execute('UPDATE events SET "numAttendees" = "numAttendees" - 1 WHERE id = %s', (data['eventID'],))

            return jsonify({'message': 'Attendee removed successfully'}), 200

    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 500

@blueprint.route('/updateAttendeeStatus', methods=['PUT'])
def updateAttendeeStatus():
    data = request.get_json()
    
    attendee_id = data.get('attendeeId')
    has_paid = data.get('hasPaid')
    attendance_status = data.get('attendanceStatus')
    event_owner_id = data.get('eventOwnerID')
    event_owner_type = data.get('eventOwnerType')
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with db_manager.get_cursor(commit=False) as cursor:
        try:
            # Verify the requester is the event owner
            cursor.execute('''
                SELECT e.* FROM events e 
                JOIN "eventAttendees" ea ON e.id = ea."eventID" 
                WHERE ea.id = %s AND e."eventOwnerID" = %s AND e."eventOwnerType" = %s
            ''', (attendee_id, event_owner_id, event_owner_type))
            
            if not cursor.fetchone():
                return jsonify({'error': 'Unauthorized'}), 403
            
            cursor.execute('''
                SELECT ea.*, e."eventName"
                FROM "eventAttendees" ea
                JOIN events e ON ea."eventID" = e.id
                WHERE ea.id = %s
            ''', (attendee_id,))
            
            attendee_info = cursor.fetchone()
            if not attendee_info:
                return jsonify({'error': 'Attendee not found'}), 404
            
            previous_attendance_status = attendee_info.get('attendanceStatus')
            
            update_fields = []
            update_values = []
            
            if has_paid is not None:
                update_fields.append('"hasPaid" = %s')
                update_values.append(has_paid)
                
            if attendance_status is not None:
                update_fields.append('"attendanceStatus" = %s')
                update_values.append(attendance_status)
            
            badge_result = None
            
            if update_fields:
                update_values.append(attendee_id)
                cursor.execute(f'''
                    UPDATE "eventAttendees" 
                    SET {", ".join(update_fields)}
                    WHERE id = %s
                ''', update_values)
                
                cursor.connection.commit()
                
                # Process badge if attendance status changed to "Checked In"
                if (attendance_status == "Checked In" and 
                    previous_attendance_status != "Checked In" and
                    attendee_info.get('attendeeType') == 'user'):
                    
                    user_id = attendee_info.get('userID')
                    if user_id:
                        badge_result = badge_helpers.process_event_attendance_badge(cursor.connection, cursor, user_id)

                    cursor.execute('SELECT username FROM users WHERE id = %s', (user_id,))
                    user_row = cursor.fetchone()
                    if user_row:
                        # Get the username of the user
                        user_username = user_row['username'] if user_row else "Someone"
                                
                    # Notify user of badge
                    if badge_result:
                        notification_data = {
                            "userId":   user_id,
                            "userType": "user",
                            "notiTabs": "forYou",
                            "notiType": "badge_earned",
                            "image":    None,
                            "link":     f"/profile/user/{user_id}/{user_username}",
                            "message":  f"Congratulations! You earned a badge: {badge_result['badgeName']}.",
                            "createdAt": current_time
                        }
                        print("notification data for badge: ", notification_data)
                        notifications.add_notification_to_db(notification_data)
            
            response_data = {'message': 'Attendee status updated successfully'}
            
            if badge_result:
                response_data['badgeAwarded'] = badge_result
                
            return jsonify(response_data), 200
            
        except Exception as e:
            print(f"Error updating attendee status: {str(e)}")
            return jsonify({'error': str(e)}), 500

@blueprint.route('/getUserOrganisingEvents/<user_id>/<user_type>', methods=['GET'])
def getUserOrganisingEvents(user_id, user_type):
    return_data = []

    try:
        with db_manager.get_cursor() as cursor:
            # Query to get all events that the user is organizing (both upcoming and past)
            query = '''
                SELECT e.*
                FROM "events" e
                WHERE e."eventOwnerID" = %s
                AND e."eventOwnerType" = %s
                ORDER BY e."eventStartDate" DESC, e."eventStartTime" DESC
            '''

            cursor.execute(query, (user_id, user_type))
            events = cursor.fetchall()

            if not events:
                return jsonify({'error': 'No events found'}), 404
            
            for event in events:
                ev = {}
                ev['eventID'] = event['id']
                ev['eventName'] = event['eventName']
                ev['eventDesc'] = event['eventDesc'].replace('<p>', '').replace('</p>', '') if event['eventDesc'] else ''

                ev['eventType'] = event['eventType']
                ev['eventStartDate'] = event['eventStartDate'].strftime('%Y-%m-%d')

                if event['eventEndDate'] is not None:
                    ev['eventEndDate'] = event['eventEndDate'].strftime('%Y-%m-%d')

                if event['eventStartTime'] is not None:
                    ev['eventStartTime'] = event['eventStartTime'].strftime('%H:%M')

                if event['eventEndTime'] is not None:
                    ev['eventEndTime'] = event['eventEndTime'].strftime('%H:%M')
                ev['eventBanners'] = event['eventBanners']
                ev['eventLocation'] = event['eventLocation']
                ev['numAttendees'] = event['numAttendees']
                ev['eventPasscode'] = event['passcode']
                ev['eventLimit'] = event['eventLimit']
                ev['signupOpen'] = event['signupOpen']  # Include signupOpen field for dashboard
                
                # Add missing fields needed for edit modal
                ev['ticketed'] = event['ticketed']
                ev['paidEvent'] = event['paidEvent']
                ev['paymentLink'] = event['paymentLink']
                ev['passcode'] = event['passcode']  # Also provide as 'passcode' for consistency

                return_data.append(ev)

            return jsonify({
                'events': return_data
            }), 200

    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 500


@blueprint.route('/getUserAttendingEvents/<user_id>/<user_type>', methods=['GET'])
def getUserAttendingEvents(user_id, user_type):
    return_data = []

    try:
        with db_manager.get_cursor() as cursor:
            # Query to get all events that the user is attending (both upcoming and past)
            # Only include events where attendeeStatus is True (confirmed attendance)
            query = '''
                SELECT 
                    e.*,
                    ea."attendeeStatus",
                    ea."hasPaid",
                    ea."attendanceStatus",
                    ea."rsvpTimestamp"
                FROM "eventAttendees" ea
                JOIN "events" e ON ea."eventID" = e."id"
                WHERE ea."userID" = %s 
                AND ea."attendeeType" = %s
                AND ea."attendeeStatus" = TRUE
                ORDER BY e."eventStartDate" DESC, e."eventStartTime" DESC
            '''

            cursor.execute(query, (user_id, user_type))
            events = cursor.fetchall()

            if not events:
                return jsonify({'error': 'No events found'}), 404
            
            for event in events:
                ev = {}
                ev['eventID'] = event['id']
                ev['eventName'] = event['eventName']
                ev['eventDesc'] = event['eventDesc']
                ev['eventType'] = event['eventType']
                ev['eventStartDate'] = event['eventStartDate'].strftime('%Y-%m-%d')
                ev['eventEndDate'] = event['eventEndDate'].strftime('%Y-%m-%d')
                ev['eventStartTime'] = event['eventStartTime'].strftime('%H:%M')
                ev['eventEndTime'] = event['eventEndTime'].strftime('%H:%M')
                ev['eventBanners'] = event['eventBanners']
                ev['eventLocation'] = event['eventLocation']
                ev['numAttendees'] = event['numAttendees']
                ev['attendeeStatus'] = event['attendeeStatus']
                ev['hasPaid'] = event['hasPaid']
                ev['attendanceStatus'] = event['attendanceStatus']
                ev['rsvpTimestamp'] = event['rsvpTimestamp'].strftime('%Y-%m-%d %H:%M:%S') if event['rsvpTimestamp'] else None

                return_data.append(ev)

            return jsonify({
                'events': return_data
            }), 200

    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 500


# -----------------------------------------------------------------------------------------
# [GET] Get organizer events with attendee counts and details
# Purpose: Get all events organized by a user/venue/producer with attendee counts and attendee information
# Used: EventOrganiserDashboard.vue 
# Output: Possible return codes [200 - Retrieval success, 404 - No events found, 500 - Internal server error]
@blueprint.route('/getOrganizerEventsWithAttendees/<user_id>/<user_type>', methods=['GET'])
def getOrganizerEventsWithAttendees(user_id, user_type):
    return_data = []

    try:
        with db_manager.get_cursor() as cursor:
            # Efficient single query using JOINs to get all events with their attendees and user info
            cursor.execute('''
                SELECT 
                    e.id as event_id,
                    ea.id as attendee_id,
                    ea."hasPaid",
                    ea."attendanceStatus",
                    ea."rsvpTimestamp",
                    ea."eventDate",
                    ea."firstName" as attendee_first_name,
                    ea."lastName" as attendee_last_name,
                    ea."phoneNumber",
                    ea."email",
                    ea."passcodeUsed",
                    ea."userID",
                    ea."attendeeType" as attendee_type,
                    -- User info from users table
                    u.id as user_id,
                    u."displayName",
                    u.photo as user_photo,
                    -- Producer info from producers table  
                    p.id as producer_id,
                    p."producerName",
                    p.photo as producer_photo,
                    -- Venue info from venues table
                    v.id as venue_id,
                    v."venueName", 
                    v.photo as venue_photo
                FROM events e
                LEFT JOIN "eventAttendees" ea ON e.id = ea."eventID"
                LEFT JOIN users u ON (ea."attendeeType" = 'user' AND ea."userID" = u.id)
                LEFT JOIN producers p ON (ea."attendeeType" = 'producer' AND ea."userID" = p.id)
                LEFT JOIN venues v ON (ea."attendeeType" = 'venue' AND ea."userID" = v.id)
                WHERE e."eventOwnerID" = %s AND e."eventOwnerType" = %s
                ORDER BY e."eventStartDate" DESC, e."eventStartTime" DESC, ea."rsvpTimestamp" ASC
            ''', (user_id, user_type))
            
            results = cursor.fetchall()

            if not results:
                return jsonify({'error': 'No events found'}), 404

            # Group results by event ID
            events_dict = {}
            
            for row in results:
                event_id = row['event_id']
                
                # Initialize event if not seen before
                if event_id not in events_dict:
                    events_dict[event_id] = {
                        'id': event_id,
                        'attendeeCount': 0,
                        'attendees': []
                    }
                
                # If this row has attendee data, process it
                if row['attendee_id'] is not None:
                    # Determine user info based on attendee type
                    if row['attendee_type'] == 'user' and row['user_id']:
                        user_info = {
                            'id': row['user_id'],
                            'displayName': row['displayName'],
                            'photo': row['user_photo'],
                            'userType': 'user'
                        }
                    elif row['attendee_type'] == 'producer' and row['producer_id']:
                        user_info = {
                            'id': row['producer_id'],
                            'producerName': row['producerName'],
                            'photo': row['producer_photo'],
                            'userType': 'producer'
                        }
                    elif row['attendee_type'] == 'venue' and row['venue_id']:
                        user_info = {
                            'id': row['venue_id'],
                            'venueName': row['venueName'],
                            'photo': row['venue_photo'],
                            'userType': 'venue'
                        }
                    else:
                        # Skip if user info not found
                        continue
                    
                    # Add attendee-specific information
                    user_info.update({
                        'attendeeId': row['attendee_id'],
                        'hasPaid': row['hasPaid'] or False,
                        'attendanceStatus': row['attendanceStatus'] or 'Not Checked In',
                        'rsvpDate': row['rsvpTimestamp'],
                        'eventDate': row['eventDate'],
                        'firstName': row['attendee_first_name'],
                        'lastName': row['attendee_last_name'],
                        'phoneNumber': row['phoneNumber'],
                        'email': row['email'],
                        'passcodeUsed': row['passcodeUsed']
                    })
                    
                    events_dict[event_id]['attendees'].append(user_info)
                    events_dict[event_id]['attendeeCount'] += 1

            # Convert to list format
            return_data = list(events_dict.values())

            return jsonify({
                'events': return_data,
                'totalEvents': len(return_data),
                'totalAttendees': sum(event['attendeeCount'] for event in return_data)
            }), 200

    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 500