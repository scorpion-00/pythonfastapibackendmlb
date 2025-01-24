from bson import ObjectId
from typing import List, Optional
from fastapi import HTTPException
from app.models.models import User
from pymongo.database import Database
from pymongo.errors import DuplicateKeyError
from app.db.db import get_database

class UserService:
    def __init__(self, database: Database):
        self.db = database
        self.collection = self.db["users"]  

    def create_user(self, user_data: dict) -> User:
        try:
            # Generate new ObjectId and convert to string
            user_data["_id"] = str(ObjectId())
            
            # Initialize empty lists if not provided
            user_data.setdefault("followers_ids", [])
            user_data.setdefault("followings_ids", [])
            user_data.setdefault("posts_ids", [])

            # Create unique indexes
            self.collection.create_index("username", unique=True)
            self.collection.create_index("email", unique=True)

            # Insert into database
            self.collection.insert_one(user_data)
            
            # Retrieve and return the created user
            created_user = self.collection.find_one({"_id": user_data["_id"]})
            if not created_user:
                raise HTTPException(status_code=500, detail="User creation failed")
            
            return User(**created_user)
            
        except DuplicateKeyError as e:
            # More specific error message based on the duplicate field
            field = "email" if "email" in str(e) else "username"
            raise HTTPException(
                status_code=400,
                detail=f"User with this {field} already exists"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error creating user: {str(e)}"
            )

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        try:
            user = self.collection.find_one({"_id": user_id})
            if not user:
                return None
            return User(**user)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error fetching user: {str(e)}"
            )

    def update_user(self, user_id: str, update_data: dict) -> Optional[User]:
        try:
            # Remove empty fields and _id from update_data
            update_data = {k: v for k, v in update_data.items() 
                         if v is not None and k != "_id"}
            
            if not update_data:
                raise HTTPException(
                    status_code=400, 
                    detail="No valid update data provided"
                )

            # Check if user exists before update
            existing_user = self.get_user_by_id(user_id)
            if not existing_user:
                raise HTTPException(status_code=404, detail="User not found")

            result = self.collection.update_one(
                {"_id": user_id},
                {"$set": update_data}
            )

            if result.modified_count == 0:
                raise HTTPException(
                    status_code=400, 
                    detail="Update failed - no changes made"
                )

            # Retrieve and return the updated user
            updated_user = self.collection.find_one({"_id": user_id})
            return User(**updated_user)

        except DuplicateKeyError as e:
            field = "email" if "email" in str(e) else "username"
            raise HTTPException(
                status_code=400,
                detail=f"User with this {field} already exists"
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error updating user: {str(e)}"
            )

    def delete_user(self, user_id: str) -> bool:
        try:
            result = self.collection.delete_one({"_id": user_id})
            if result.deleted_count == 0:
                raise HTTPException(status_code=404, detail="User not found")
            return True
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error deleting user: {str(e)}"
            )

    def get_users(self, skip: int = 0, limit: int = 10) -> List[User]:
        try:
            users = []
            cursor = self.collection.find().skip(skip).limit(limit)
            for user in cursor:
                users.append(User(**user))
            return users
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error fetching users: {str(e)}"
            )

    @classmethod
    def get_instance(cls):
        """
        Factory method to create UserService instance with database connection
        """
        db = get_database()
        return cls(db)
