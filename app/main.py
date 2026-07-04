from fastapi import FastAPI
from sqlalchemy import text
from app.api import user

from app.db.database import engine
from app.api import user

app = FastAPI()
app.include_router(user.router)


@app.get("/")
def root():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))

        return {
            "message": "Database Connected",
            "postgres_version": result.scalar()
        }