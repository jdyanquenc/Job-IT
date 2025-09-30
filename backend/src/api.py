from fastapi import FastAPI
from src.auth.controller import router as auth_router
from src.users.controller import router as users_router
from src.jobs.controller import router as jobs_router
from src.companies.controller import router as companies_router
from src.profiles.controller import router as profiles_router

def register_routes(app: FastAPI):
    app.include_router(auth_router)
    app.include_router(users_router)
    app.include_router(jobs_router)
    app.include_router(companies_router)
    app.include_router(profiles_router)
