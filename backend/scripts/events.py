# Port: 5701
# Routes: 
#   [events] /getEvents (GET), /getSpecificEvent (GET), /getUserEvents (GET), /createEvent (POST), /updateEvent (PUT), /deleteEvent (DELETE)
#   [attendees] /getAttendees (GET), /addAttendee (POST), /removeAttendee (DELETE)
# -----------------------------------------------------------------------------------------

import os
from flask import Blueprint, g, jsonify, request
from datetime import datetime

# Use to upload image to S3
import s3Images

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)


# Helper function
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


# -----------------------------------------------------------------------------------------
# [GET] Get all events with lazy loading
# Purpose:
# Used:
# Output: Possible return codes [200 - Retrieval success, 404 - No events, 500 - Internal server error]
@blueprint.route('/getEvents/<offset>', methods=['GET'])
def getEvents(offset):

    conn = g.db
    cursor = conn.cursor()

    return_data = []

    try:
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
            event['eventEndDate'] = event['eventEndDate'].strftime('%Y-%m-%d')
            event['eventStartTime'] = event['eventStartTime'].strftime('%H:%M')
            event['eventEndTime'] = event['eventEndTime'].strftime('%H:%M')

            # Append the event into the return_data
            return_data.append(event)


        return jsonify({
            'events': return_data
        }), 200

    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# -----------------------------------------------------------------------------------------
# [GET] Get an event by event id
# Purpose: Get an event by event id
# Used: 
# Output: Possible return codes [200 - Retrieval success, 400 - Bad request, 404 - No such event/Event owner not found, 500 - Internal server error]
@blueprint.route('/getSpecificEvent/<event_id>', methods=['GET'])
def getSpecificEvent(event_id):

    conn = g.db
    cursor = conn.cursor()

    try:
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
        event['eventEndDate'] = event['eventEndDate'].strftime('%Y-%m-%d')
        event['eventStartTime'] = event['eventStartTime'].strftime('%H:%M')
        event['eventEndTime'] = event['eventEndTime'].strftime('%H:%M')

        return jsonify({
            'event': event
        }), 200

    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# -----------------------------------------------------------------------------------------
# [GET] Get all events by a user/producer/venue
# Purpose: Get all events by a user/producer/venue
# Used:
# Output: Possible return codes [200 - Retrieval success, 404 - User not found/No events, 500 - Internal server error]
@blueprint.route('/getUserEvents/<user_id>/<user_type>/<offset>', methods=['GET'])
def getUserEvents(user_id, user_type, offset):

    conn = g.db
    cursor = conn.cursor()

    return_data = []

    # Set the limit here
    limit = 5

    try:
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
            event['eventEndDate'] = event['eventEndDate'].strftime('%Y-%m-%d')
            event['eventStartTime'] = event['eventStartTime'].strftime('%H:%M')
            event['eventEndTime'] = event['eventEndTime'].strftime('%H:%M')

            # Append the event into the return_data
            return_data.append(event)


        return jsonify({
            'events': return_data
        }), 200

    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# -----------------------------------------------------------------------------------------
# [POST] Create an event
# Purpose: Create an event
# Used:
# Input:
#    1. eventName
#    2. eventDesc
#    3. eventStartDate
#    4. eventEndDate
#    5. eventStartTime
#    6. eventEndTime
#    7. eventBanners [Optional]
#    8. ticketed
#    9. eventLocation
#    10. eventLink [Optional]
#    11. eventOwnerID
#    12. eventOwnerType
# Output: Possible return codes [201 - Creation success, 400 - Missing required fields or required fields are empty / Event owner not found, 500 - Internal server error]
@blueprint.route('/createEvent', methods=['POST'])
def createEvent():

    conn = g.db
    cursor = conn.cursor()

    try:
        # Step 1: Get the input data
        data = request.json

        required_fields = ['eventName', 'eventDesc', 'eventStartDate', 'eventEndDate', 'eventStartTime', 'eventEndTime', 'ticketed', 'eventLocation', 'eventOwnerID', 'eventOwnerType']

        # Check if the required fields are present and not empty
        for field in required_fields:
            if field not in data or not data[field]:
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
                url = s3Images.uploadBase64ImageToS3(image)
                if url:
                    event_banner.append(url)

        # Convert the list to PostgreSQL array format before insertion
        if event_banner:
            event_banner_pg = "{" + ",".join([f'"{url}"' for url in event_banner]) + "}"  # Example: {"url1", "url2"}
        else:
            event_banner_pg = None  # NULL for no banners

        # Step 4: Convert datetime values to datetime objects
        data['eventStartDate'] = datetime.strptime(data['eventStartDate'], '%Y-%m-%d')
        data['eventEndDate'] = datetime.strptime(data['eventEndDate'], '%Y-%m-%d')

        # Check if eventLink is provided
        if 'eventLink' in data and not data['eventLink']:
            event_link = None
        else:
            event_link = data['eventLink']


        # Step 5: Insert the event into the database
        cursor.execute('INSERT INTO events (eventName, eventDesc, eventStartDate, eventEndDate, eventStartTime, eventEndTime, eventBanners, ticketed, eventLocation, eventLink, eventOwnerID, eventOwnerType) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', 
                       (data['eventName'], data['eventDesc'], data['eventStartDate'], data['eventEndDate'], data['eventStartTime'], data['eventEndTime'], event_banner_pg, data['ticketed'], data['eventLocation'], event_link, data['eventOwnerID'], data['eventOwnerType'],))
        conn.commit()

        return jsonify({'message': 'Event created successfully'}), 201

    except Exception as e:
        print(str(e))
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        cursor.close()


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
#    7. eventBanners [Optional if no change and no image provided during creation]
#    8. ticketed
#    9. eventLocation
#    10. eventLink [Optional]
#    11. eventOwnerID
#    12. eventOwnerType
# Output: Possible return codes [200 - Update success, 400 - Missing required fields or required fields are empty / No such event , 403 - Unauthorized to update the event, 500 - Internal server error]
@blueprint.route('/updateEvent', methods=['PUT'])
def updateEvent():

    conn = g.db
    cursor = conn.cursor()

    try:
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
        if event['eventOwnerID'] != data['eventOwnerID'] or event['eventOwnerType'] != data['eventOwnerType']:
            return jsonify({'error': 'Unauthorized to update this event'}), 403

        
        if 'eventBanners' in data and len(data['eventBanners']) > 0:
            
            # Upload each image (base64Image) to S3
            event_banner = []
            for image in data['eventBanners']:

                if not image:
                    continue

                # Check if the image is already in S3
                if 'http' in image:
                    event_banner.append(image)
                    continue
                else:
                    url = s3Images.uploadBase64ImageToS3(image)
                    if url:
                        event_banner.append(url)

            # Convert the list to PostgreSQL array format before insertion
            if event_banner:
                event_banner_pg = "{" + ",".join([f'"{url}"' for url in event_banner]) + "}"


        # Convert datetime values to datetime objects
        data['eventStartDate'] = datetime.strptime(data['eventStartDate'], '%Y-%m-%d')
        data['eventEndDate'] = datetime.strptime(data['eventEndDate'], '%Y-%m-%d')
        data['eventStartTime'] = datetime.strptime(data['eventStartTime'], '%H:%M')
        data['eventEndTime'] = datetime.strptime(data['eventEndTime'], '%H:%M')

        # Step 4: Update the event
        cursor.execute('UPDATE events SET eventName = %s, eventDesc = %s, eventStartDate = %s, eventEndDate = %s, eventStartTime = %s, eventEndTime = %s, eventBanners = %s, ticketed = %s, eventLocation = %s, eventLink = %s WHERE id = %s', 
                       (data['eventName'], data['eventDesc'], data['eventStartDate'], data['eventEndDate'], data['eventStartTime'], data['eventEndTime'], event_banner_pg, data['ticketed'], data['eventLocation'], data['eventLink'], data['eventID'],))
        conn.commit()

        return jsonify({'message': 'Event updated successfully'}), 200

    except Exception as e:
        print(str(e))
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


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

    conn = g.db
    cursor = conn.cursor()

    try:
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

        # Step 3: Check if the user who is deleting the event is the owner of the event
        if event['eventOwnerID'] != data['eventOwnerID'] or event['eventOwnerType'] != data['eventOwnerType']:
            return jsonify({'error': 'Unauthorized to delete this event'}), 403
        
        # Step 4: Delete all the attendees of the event
        cursor.execute('DELETE FROM eventAttendees WHERE eventID = %s', (data['eventID'],))
        conn.commit()

        # Step 5: Delete the event
        cursor.execute('DELETE FROM events WHERE id = %s', (data['eventID'],))
        conn.commit()

        return jsonify({'message': 'Event deleted successfully'}), 200

    except Exception as e:
        print(str(e))
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# -----------------------------------------------------------------------------------------
# [GET] Get all attendees of an event
# Purpose: Get all attendees of an event
# Used:
# Output: Possible return codes [200 - Retrieval success, 400 - Missing required fields or required fields are empty / No such event, 500 - Internal server error]
@blueprint.route('/getAttendees/<event_id>', methods=['GET'])
def getAttendees(event_id):

    conn = g.db
    cursor = conn.cursor()

    try:
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

            # Append the user information into the return_data
            return_data.append(user_info)

        return jsonify({
            'attendees': return_data
        }), 200

    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# -----------------------------------------------------------------------------------------
# [POST] Add an attendee to an event
# Purpose: Add an attendee to an event
# Used:
# Input:
#    1. eventID
#    2. userID
#    3. userType
# Output: Possible return codes [201 - Creation success, 400 - Missing required fields or required fields are empty / No such event / User not found, 500 - Internal server error]
@blueprint.route('/addAttendee', methods=['POST'])
def addAttendee():

    conn = g.db
    cursor = conn.cursor()

    try:
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

        # Step 4: Add the attendee to the event
        cursor.execute('INSERT INTO "eventAttendees" ("eventID", "userID", "attendeeType", "attendeeStatus") VALUES (%s, %s, %s, TRUE)', (data['eventID'], data['userID'], data['userType'],))
        conn.commit()

        return jsonify({'message': 'Attendee added successfully'}), 201

    except Exception as e:
        print(str(e))
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# -----------------------------------------------------------------------------------------
# [DELETE] Remove an attendee from an event
# Purpose: Remove an attendee from an event
# Used:
# Input:
#    1. eventID
#    2. userID
#    3. userType
# Output: Possible return codes [200 - Deletion success, 400 - Missing required fields or required fields are empty / No such event / User not found, 500 - Internal server error]
@blueprint.route('/removeAttendee', methods=['DELETE'])
def removeAttendee():

    conn = g.db
    cursor = conn.cursor()

    try:
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
        conn.commit()

        return jsonify({'message': 'Attendee removed successfully'}), 200

    except Exception as e:
        print(str(e))
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()

