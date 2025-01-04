from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import settings

DATABASE_URL = settings.DATABASE_URL

# Create database engine
engine = create_engine(DATABASE_URL, echo=True)

# Create session factory
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Declare the base class for models
Base = declarative_base()
