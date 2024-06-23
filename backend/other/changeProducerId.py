# ===== MODIFY PRODUCER ID TYPE IN DATABASE =====
# ===============================================
# USE THIS TO CHANGE ANY INCONSISTENCIES IN THE WAY THAT THE PRODUCER ID IS STORED IN THE DATABASE
# Can be repurposed by changing the convert_producer_id function to convert any other field in the database (change the field name in the function)

import bson
import json
from bson import json_util
from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)  # Allow all requests

load_dotenv()
app.config["MONGO_URI"] = os.getenv('MONGO_DB_URL')
db = PyMongo(app).db
collection = db["listings"]

def convert_producer_id(document):
    if 'producerID' in document:
        producer_id = document['producerID']
        # Check if producerID is nested incorrectly
        if isinstance(producer_id, dict) and '$oid' in producer_id:
            # If nested incorrectly, extract the correct $oid value
            correct_oid = producer_id['$oid']
            # Ensure correct_oid is converted to ObjectId type
            converted_oid = ObjectId(correct_oid)
            converted_id = {
                "producerID": converted_oid
            }
            return converted_id
        else:
            # If already in correct format, return the document unchanged
            return document
    else:
        return document

def update_documents(collection):
    documents = collection.find({})
    for doc in documents:
        converted_doc = convert_producer_id(doc)
        # Update the document in MongoDB
        collection.update_one({'_id': doc['_id']}, {'$set': converted_doc})
        print(f"Updated document with _id: {doc['_id']}")

if __name__ == "__main__":
    update_documents(collection)