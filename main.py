# bin change

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.api import info_routes, user_routes
from app.db.db import MongoDB

app = FastAPI()

# Include routers
app.include_router(info_routes.router)
app.include_router(user_routes.router)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database connection
MongoDB.connect_to_database()

@app.get("/")
def default_root():
    return {"message": "API is running"}
