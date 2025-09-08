import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DatabaseService:
    """Service for MongoDB database operations"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseService, cls).__new__(cls)
            # Initialize database connection
            mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/isp_routing')
            cls._instance.client = MongoClient(mongo_uri)
            cls._instance.db = cls._instance.client.get_database()
        return cls._instance
    
    def get_collection(self, collection_name):
        """Get a collection from the database"""
        return self.db[collection_name]
    
    def close_connection(self):
        """Close the database connection"""
        if hasattr(self, 'client'):
            self.client.close()
