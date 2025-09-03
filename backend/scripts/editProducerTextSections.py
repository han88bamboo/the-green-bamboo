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
    try:
        data = request.get_json()
        
        if not data or 'image64' not in data:
            return jsonify({
                "code": 400,
                "message": "Missing image data"
            }), 400
        
        # Validate image format and size
        base64_string = data['image64']
        
        # Add some basic validation
        if not base64_string:
            return jsonify({
                "code": 400,
                "message": "Empty image data"
            }), 400
        
        try:
            # Upload to S3 - make sure this function exists and works
            image_url = s3Images.uploadBase64ImageToS3(base64_string)
            
            if not image_url:
                return jsonify({
                    "code": 500,
                    "message": "Failed to upload image to S3"
                }), 500
                
            return jsonify({
                "code": 200,
                "imageUrl": image_url,
                "message": "Image uploaded successfully"
            }), 200
            
        except Exception as s3_error:
            print(f"S3 upload error: {str(s3_error)}")
            return jsonify({
                "code": 500,
                "message": f"S3 upload failed: {str(s3_error)}"
            }), 500
        
    except Exception as e:
        print(f"Upload image error: {str(e)}")
        return jsonify({
            "code": 500,
            "message": f"Server error: {str(e)}"
        }), 500