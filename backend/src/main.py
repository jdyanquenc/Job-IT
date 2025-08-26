from fastapi import FastAPI # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore

from .database.core import engine, Base
from .entities.country import Country           # Import models to register them
from .entities.todo import Todo                 # Import models to register them
from .entities.user import User                 # Import models to register them
from .entities.user_profile import UserProfile  # Import models to register them
from .entities.company import Company           # Import models to register them
from .entities.job import JobEntry, JobDetail   # Import models to register them
from .api import register_routes
from .logging import configure_logging, LogLevels


configure_logging(LogLevels.info)

app = FastAPI()

# Allowed origins
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://buscoempleo.com.co"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Set-Cookie"],
)

""" Only uncomment below to create new tables, 
otherwise the tests will fail if not connected
"""
Base.metadata.create_all(bind=engine)


register_routes(app)