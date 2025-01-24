from fastapi.middleware.cors import CORSMiddleware
from app.api import info_routes, user_routes
from fastapi import FastAPI
from app.db.db import MongoDB
import logging

app = FastAPI()

app.include_router(info_routes.router)
app.include_router(user_routes.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db_client():
    try:
        # Only attempt connection if not already connected
        if MongoDB.client is None:
            await MongoDB.connect_to_database()
    except Exception as e:
        logging.error(f"Database connection failed: {e}")
        # Consider fallback strategy or raise a critical error

@app.on_event("shutdown")
async def shutdown_db_client():
    try:
        await MongoDB.close_database_connection()
    except Exception as e:
        logging.error(f"Database disconnection failed: {e}")

@app.get("/")
async def default_root():
    return {"message": "API is running"}