import os

from sqlalchemy import create_engine
from src.models.sensor.reading import Base  


# PostgreSQL connection string
DATABASE_URL = "postgresql://postgres-user:postgres-pass@localhost:5432/postgres"
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")

def create_tables():
    print("[DB] Connecting to database...")
    engine = create_engine(DATABASE_URL)

    print("[DB] Creating tables if they don't exist...")
    Base.metadata.create_all(engine)

    print("[✓] Tables created successfully.")

if __name__ == "__main__":
    create_tables()
