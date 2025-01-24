from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from pymongo.database import Database
from typing import Optional
import logging
import os
from dotenv import load_dotenv

load_dotenv()

class MongoDB:
    client: Optional[AsyncIOMotorClient] = None
    sync_client: Optional[MongoClient] = None
    db: Optional[Database] = None

    class Collections:
        USERS = "users"
        POSTS = "posts"

    @classmethod
    def connect_to_database(cls, db_name: Optional[str] = None):
        """Creates synchronous database connection"""
        try:
            if cls.sync_client is None:
                mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
                cls.sync_client = MongoClient(mongodb_url)
                cls.sync_client.admin.command('ping')
                logging.info("Successfully connected to MongoDB.")

            if cls.db is None:
                db_name = db_name or os.getenv("MONGODB_DB", "your_default_db")
                cls.db = cls.sync_client[db_name]
                logging.info(f"Connected to database: {db_name}")

            return cls.db

        except Exception as e:
            logging.error(f"Could not connect to MongoDB: {str(e)}")
            raise

def get_database() -> Database:
    """Get database instance"""
    return MongoDB.connect_to_database()
