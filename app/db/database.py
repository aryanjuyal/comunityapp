from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings


# Engine
# Responsible for communicating with PostgreSQL
engine = create_engine(
    settings.DATABASE_URL,
    echo=True
)


# Every request gets its own database session
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


# Parent class for all database models
class Base(DeclarativeBase):
    pass