from fastapi.middleware.cors import CORSMiddleware
from app.api import info_routes, user_routes
from fastapi import FastAPI
from app.db.db import MongoDB

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


MongoDB.connect_to_database()


@app.get("/")
async def default_root():
    return {"message": "API is running"}
