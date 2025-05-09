from sqlalchemy import create_engine
import socket

def test_postgres_connection():
    # Define the connection string
    connection_string = "postgresql+psycopg2://bn_airflow:bitnami1@localhost:5432/bitnami_airflow"

    # print(f"Host address: {socket.gethostbyname('postgresql-1')}")
    
    try:
        # Create the engine
        engine = create_engine(connection_string)
        
        # Test the connection
        with engine.connect() as connection:
            print("Connection to PostgreSQL database was successful!")
    
    except Exception as e:
        print(f"An error occurred while connecting to the database: {e}")

if __name__ == "__main__":
    test_postgres_connection()