# Port: 5200
# Routes: /getTextSections (GET), /addTextSection (POST), /updateTextSection (POST), /deleteTextSection (POST), /reorderTextSections (POST), /uploadSectionImage (POST)

import os
import s3Images
from flask import Blueprint, g, request, jsonify
from datetime import datetime
import re

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

@blueprint.route('/getTextSections/<int:producer_id>', methods=['GET'])
def getTextSections(producer_id):
    conn = g.db
    cur = conn.cursor()
    
    try:
        cur.execute("""
            SELECT id, "sectionTitle", "richTextContent", "sectionOrder" 
            FROM "producerTextSections" 
            WHERE "producerId" = %s 
            ORDER BY "sectionOrder" ASC
        """, (producer_id,))
        
        sections = cur.fetchall()
        return jsonify({
            "code": 200,
            "data": sections
        }), 200
        
    except Exception as e:
        print(str(e))
        return jsonify({
            "code": 500,
            "message": "Error fetching text sections"
        }), 500
    finally:
        cur.close()

@blueprint.route('/addTextSection', methods=['POST'])
def addTextSection():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()
    
    try:
        cur.execute("""
            INSERT INTO "producerTextSections" ("producerId", "sectionTitle", "richTextContent", "sectionOrder")
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (data['producerId'], data['sectionTitle'], data['richTextContent'], data['sectionOrder']))
        
        section_id = cur.fetchone()['id']
        conn.commit()
        
        return jsonify({
            "code": 201,
            "message": "Text section added successfully",
            "sectionId": section_id
        }), 201
        
    except Exception as e:
        print(str(e))
        conn.rollback()
        return jsonify({
            "code": 500,
            "message": "Error adding text section"
        }), 500
    finally:
        cur.close()

@blueprint.route('/updateTextSection', methods=['POST'])
def updateTextSection():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()
    
    try:
        cur.execute("""
            UPDATE "producerTextSections" 
            SET "sectionTitle" = %s, "richTextContent" = %s, "updatedDate" = CURRENT_TIMESTAMP
            WHERE id = %s AND "producerId" = %s
        """, (data['sectionTitle'], data['richTextContent'], data['sectionId'], data['producerId']))
        
        conn.commit()
        
        return jsonify({
            "code": 200,
            "message": "Text section updated successfully"
        }), 200
        
    except Exception as e:
        print(str(e))
        conn.rollback()
        return jsonify({
            "code": 500,
            "message": "Error updating text section"
        }), 500
    finally:
        cur.close()

@blueprint.route('/deleteTextSection', methods=['POST'])
def deleteTextSection():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()
    
    try:
        cur.execute("""
            DELETE FROM "producerTextSections" 
            WHERE id = %s AND "producerId" = %s
        """, (data['sectionId'], data['producerId']))
        
        conn.commit()
        
        return jsonify({
            "code": 200,
            "message": "Text section deleted successfully"
        }), 200
        
    except Exception as e:
        print(str(e))
        conn.rollback()
        return jsonify({
            "code": 500,
            "message": "Error deleting text section"
        }), 500
    finally:
        cur.close()

@blueprint.route('/reorderTextSections', methods=['POST'])
def reorderTextSections():
    conn = g.db
    cur = conn.cursor()
    data = request.get_json()
    
    try:
        for section in data['sections']:
            cur.execute("""
                UPDATE "producerTextSections" 
                SET "sectionOrder" = %s 
                WHERE id = %s AND "producerId" = %s
            """, (section['sectionOrder'], section['id'], data['producerId']))
        
        conn.commit()
        
        return jsonify({
            "code": 200,
            "message": "Sections reordered successfully"
        }), 200
        
    except Exception as e:
        print(str(e))
        conn.rollback()
        return jsonify({
            "code": 500,
            "message": "Error reordering sections"
        }), 500
    finally:
        cur.close()

@blueprint.route('/uploadSectionImage', methods=['POST'])
def uploadSectionImage():
    data = request.get_json()
    
    try:
        # Validate image format and size
        base64_string = data['image64']
        
        # Upload to S3
        image_url = s3Images.uploadBase64ImageToS3(base64_string)
        
        return jsonify({
            "code": 200,
            "imageUrl": image_url
        }), 200
        
    except Exception as e:
        print(str(e))
        return jsonify({
            "code": 500,
            "message": "Error uploading image"
        }), 500