
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv

# Load dotenv to read environment variables from a .env file
load_dotenv()

# Get the DATABASE URL from environment variable or use a default value
USERNAME = os.getenv("POSTGRESQL_USERNAME", "postgres-user")
PASSWORD = os.getenv("POSTGRESQL_PASSWORD", "postgres-pass")
SENSORS_DATABASE_NAME = os.getenv("POSTGRESQL_DATABASE_NAME", "sensors")
HOST = os.getenv("DATABASE_HOST", "postgresql")
PORT = os.getenv("DATABASE_PORT", "5432")
DATABASE_URL = os.getenv("DATABASE_URL", f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{SENSORS_DATABASE_NAME}")

# Create the engine
engine = create_engine(DATABASE_URL, echo=True)  # 'echo=True' para log de las consultas SQL

# Create the session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency used in routes to get the session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
