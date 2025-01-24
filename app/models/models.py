from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

# User Model
class User(BaseModel):
    id: str = Field(..., alias="_id")  
    username: str = Field(..., unique=True, index=True)
    name: Optional[str]
    email: EmailStr = Field(..., unique=True, index=True)
    phone: Optional[str]
    img_data: Optional[str]
    # followers_ids: List[str] = []  # References to other user IDs
    followings_ids: List[str] = []  # References to Players IDs
    posts_ids: List[str] = []  # References to Post IDs

# Request Models
class UserCreate(BaseModel):
    username: str
    name: Optional[str]
    email: EmailStr
    phone: Optional[str]
    img_data: Optional[str]

class UserUpdate(BaseModel):
    username: Optional[str]
    name: Optional[str]
    # email: Optional[EmailStr]
    phone: Optional[str]
    img_data: Optional[str]

# Post Model
class Post(BaseModel):
    id: str = Field(..., alias="_id")
    post_id: str = Field(..., unique=True, index=True)
    user_id: str = Field(..., index=True)  # Foreign key to User
    post_data: str
    post_type: str # image or video.
    caption: Optional[str]
    likes: List[str] = []  # List of User IDs
    comments: List[dict] = []  # [{user_id: str, comment: str, created_at: datetime}]
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Comment(BaseModel):
    user_id: str  # Foreign key to User
    comment: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Following(BaseModel):
    user_id: str  # Foreign key to User
    following_player_id: str
    player_image_url: str


