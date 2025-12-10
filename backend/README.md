# JOB IT backend

Provides the API services to 

# Install all dependencies.
- Run `pip install -r requirements-dev.txt`

# How to run app. Using Docker with PostgreSQL.
- Install Docker Desktop
- Run `docker compose up --build`
- Run `docker compose down` to stop all services

# How to run locally without postgres or docker.
- in database/core.py change the DATABASE_URL to sqlite
- run `uvicorn src.main:app --reload`

# How to run tests.
- Run `pytest` to run all tests
