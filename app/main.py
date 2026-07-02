from fastapi import FastAPI
from sqlalchemy import text

from app.db.database import engine

app = FastAPI()


@app.get("/")
def root():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))

        return {
            "message": "Database Connected",
            "postgres_version": result.scalar()
        }