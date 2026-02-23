
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# This creates a SQLite database file named "people.db" in your project folder
DATABASE_URL = "sqlite:///./people.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # needed for SQLite with FastAPI
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
