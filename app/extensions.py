# webhook-repo/app/extensions.py
from pymongo import MongoClient
import os

# Global variables to hold the MongoDB connection objects
mongo_client = None
db = None
events_collection = None

def init_db_connection(app):
    global mongo_client, db, events_collection
    MONGO_URI = app.config.get('MONGO_URI')
    DB_NAME = app.config.get('DB_NAME')
    COLLECTION_NAME = app.config.get('COLLECTION_NAME')

    # Provide default values if environment variables are not set
    if not MONGO_URI:
        print("Warning: MONGO_URI not set. Defaulting to 'mongodb://localhost:27017/'")
        MONGO_URI = 'mongodb://localhost:27017/'
    if not DB_NAME:
        print("Warning: DB_NAME not set. Defaulting to 'github_webhooks'")
        DB_NAME = 'github_webhooks'
    if not COLLECTION_NAME:
        print("Warning: COLLECTION_NAME not set. Defaulting to 'events'")
        COLLECTION_NAME = 'events'

    try:
        mongo_client = MongoClient(MONGO_URI)
        db = mongo_client[DB_NAME]
        events_collection = db[COLLECTION_NAME]
        # Ping MongoDB to confirm connection
        mongo_client.admin.command('ping')
        print("Successfully connected to MongoDB!")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        print("Please ensure MongoDB is running and MONGO_URI is correct in your .env file or environment.")
        exit(1) # Exit if cannot connect to DB

# Function to get the events collection, used by routes.py
def get_events_collection():
    return events_collection