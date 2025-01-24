from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.database import Database
from typing import Optional
import logging
from pymongo.errors import ConnectionFailure
import os
from dotenv import load_dotenv

load_dotenv()

class MongoDB:
    client: Optional[AsyncIOMotorClient] = None
    db: Optional[Database] = None

    class Collections:
        USERS = "users"
        POSTS = "posts"

    @classmethod
    async def connect_to_database(cls, db_name: Optional[str] = None):
        """
        Creates database connection
        """
        try:
            if cls.client is None:
                mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
                cls.client = AsyncIOMotorClient(mongodb_url)
                # Ping the server to confirm connection
                await cls.client.admin.command('ping')
                logging.info("Successfully connected to MongoDB.")

            if cls.db is None:
                db_name = db_name or os.getenv("MONGODB_DB", "your_default_db")
                cls.db = cls.client[db_name]
                logging.info(f"Connected to database: {db_name}")

            return cls.db

        except ConnectionFailure as e:
            logging.error(f"Could not connect to MongoDB: {str(e)}")
            raise

    @classmethod
    async def close_database_connection(cls):
        """
        Closes database connection
        """
        try:
            if cls.client is not None:
                cls.client.close()
                cls.client = None
                cls.db = None
                logging.info("MongoDB connection closed.")
        except Exception as e:
            logging.error(f"Error closing MongoDB connection: {str(e)}")
            raise

    @classmethod
    def get_db(cls) -> Database:
        """
        Returns database instance
        """
        if cls.db is None:
            raise ConnectionError("Database not initialized. Call connect_to_database first.")
        return cls.db

async def get_database() -> Database:
    """
    Dependency function to get database instance
    """
    if MongoDB.db is None:
        await MongoDB.connect_to_database()
    return MongoDB.get_db()