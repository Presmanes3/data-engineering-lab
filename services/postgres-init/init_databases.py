import time
import psycopg2
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
DATABASE_PORT = int(os.getenv("DATABASE_PORT", 5432))
POSTGRESQL_USERNAME = os.getenv("POSTGRESQL_USERNAME")
POSTGRESQL_PASSWORD = os.getenv("POSTGRESQL_PASSWORD")

# Definición de bases de datos y archivos SQL
DATABASES = {
    os.getenv("AIRFLOW_DATABASE_NAME", "bitnami_airflow"): "/app/sql/create_airflow_db.sql",
    os.getenv("MLFLOW_DATABASE_NAME", "bitnami_mlflow"): "/app/sql/create_mlflow_db.sql",
    os.getenv("SENSORS_DATABASE_NAME", "sensors"): "/app/sql/create_sensors_db.sql"
}

def wait_for_postgres():
    print("Waiting for PostgreSQL...")
    while True:
        try:
            conn = psycopg2.connect(
                host=DATABASE_HOST,
                port=DATABASE_PORT,
                user=POSTGRESQL_USERNAME,
                password=POSTGRESQL_PASSWORD,
                dbname="postgres"
            )
            conn.close()
            print("✅ PostgreSQL available.")
            break
        except psycopg2.OperationalError:
            time.sleep(2)

def create_database_if_not_exists(dbname):
    print(f"➡️ Verifying DB '{dbname}'...")
    try:
        conn = psycopg2.connect(
            host=DATABASE_HOST,
            port=DATABASE_PORT,
            user=POSTGRESQL_USERNAME,
            password=POSTGRESQL_PASSWORD,
            dbname="postgres"
        )
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (dbname,))
        if cur.fetchone() is None:
            print(f"📦 Creating DB '{dbname}'...")
            cur.execute(f"CREATE DATABASE {dbname};")
        else:
            print(f"🔁 DB '{dbname}' already exists.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error while creating DB '{dbname}': {e}")
        exit(1)

def run_sql_file(dbname, filepath):
    print(f"📄 Executing SQL in '{dbname}' from '{filepath}'...")
    if not os.path.exists(filepath):
        print(f"⚠️ SQL FIle not found : {filepath}")
        return
    try:
        conn = psycopg2.connect(
            host=DATABASE_HOST,
            port=DATABASE_PORT,
            user=POSTGRESQL_USERNAME,
            password=POSTGRESQL_PASSWORD,
            dbname=dbname
        )
        conn.autocommit = True
        with conn.cursor() as cur, open(filepath, "r") as f:
            cur.execute(f.read())
        conn.close()
        print(f"✅ SQL executed correctly in '{dbname}'.")
    except Exception as e:
        print(f"❌ Error while executing '{dbname}': {e}")
        exit(1)

if __name__ == "__main__":
    wait_for_postgres()
    for dbname, sql_path in DATABASES.items():
        create_database_if_not_exists(dbname)
        run_sql_file(dbname, sql_path)
