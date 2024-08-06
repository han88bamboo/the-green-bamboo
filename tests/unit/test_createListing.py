import sys
import os

# Add the path to the 'backend' directory to sys.path
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../', 'backend')
sys.path.append(backend_dir)

# Now you can import the 'data' module
import data

import unittest
from flask import Flask
from flask.testing import FlaskClient
from unittest.mock import patch
from mongomock import MongoClient
from backend.scripts.createListing import createListings  # replace 'your_app_module' with the actual name of your Flask application module

class FlaskAppTests(unittest.TestCase):

    def setUp(self):
    # Create a separate Flask application instance for testing
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['MONGO_URI'] = "mongodb://localhost:27017/"
        self.app.config['MONGO_DBNAME'] = "test_database"

        # Mock the MongoDB connection and collection for testing
        self.mongo_client_patch = patch('backend.createListing.MongoClient')
        self.mongo_client_mock = self.mongo_client_patch.start()
        self.mongo_db_mock = self.mongo_client_mock.return_value['test_database']
        self.mongo_collection_mock = self.mongo_db_mock['your_collection']

        # Set up the Flask test client
        self.app.test_client_class = FlaskClient

        # Initialize the Flask test client
        self.app.testing = True
        self.client = self.app.test_client()

    def tearDown(self):
        # Stop the patch after the test
        self.mongo_client_patch.stop()

    def test_create_listings(self):
        # Test your createListings function here
        # You can use self.app, self.mongo_db_mock, and self.mongo_collection_mock in your tests
        # For example:
        response = self.client.post('/createListing', json={
            "listingName": "Testerr",
            "producerID": {
                "$oid": "defaultProducer"
            },
            "bottler": "OB",
            "originCountry": "Test",
            "drinkType": "Test",
            "typeCategory": "Test",
            "abv": "12%",
            "age": "12",
            "sourceLink": "Test",
            "reviewLink": "Test",
            "officialDesc": "TEst",
            "photo": "default photo"
        })
        self.assertEqual(response.status_code, 201)

if __name__ == '__main__':
    unittest.main()