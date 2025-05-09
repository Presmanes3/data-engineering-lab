import time
import psycopg2
import sys
from dotenv import load_dotenv
import os

# Cargar el archivo .env
load_dotenv()

# Reutilizamos las variables de entorno
DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
DATABASE_PORT = int(os.getenv("DATABASE_PORT", 5432))
POSTGRESQL_USERNAME = os.getenv("POSTGRESQL_USERNAME")
POSTGRESQL_PASSWORD = os.getenv("POSTGRESQL_PASSWORD")
MLFLOW_DATABASE_NAME = os.getenv("MLFLOW_DATABASE_NAME")  # Diferente de POSTGRESQL_DATABASE
INIT_SQL_FILE = os.getenv("INIT_INIT_SQL_FILE")

print(f"DATABASE_HOST: {DATABASE_HOST}")
print(f"DATABASE_PORT: {DATABASE_PORT}")
print(f"POSTGRESQL_USERNAME: {POSTGRESQL_USERNAME}")
print(f"POSTGRESQL_PASSWORD: {POSTGRESQL_PASSWORD}")
print(f"MLFLOW_DATABASE_NAME: {MLFLOW_DATABASE_NAME}")
print(f"INIT_SQL_FILE: {INIT_SQL_FILE}")

def wait_for_postgres():
    print("Esperando a PostgreSQL...")
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
            print("Conectado a PostgreSQL!")
            break
        except psycopg2.OperationalError:
            time.sleep(2)

def list_databases():
    print("Listando bases de datos existentes:")
    try:
        conn = psycopg2.connect(
            host=DATABASE_HOST,
            port=DATABASE_PORT,
            user=POSTGRESQL_USERNAME,
            password=POSTGRESQL_PASSWORD,
            dbname="postgres"
        )
        cur = conn.cursor()
        cur.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
        for row in cur.fetchall():
            print("-", row[0])
        cur.close()
        conn.close()
    except Exception as e:
        print("Error al listar bases de datos:", e)

def create_database_if_not_exists(dbname):
    print(f"Verificando si la base de datos '{dbname}' existe...")
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
            print(f"Creando base de datos '{dbname}'...")
            cur.execute(f"CREATE DATABASE {dbname};")
            print("Base de datos creada correctamente.")
        else:
            print("La base de datos ya existe.")
        cur.close()
        conn.close()
    except Exception as e:
        print("Error al crear la base de datos:", e)
        sys.exit(1)

def execute_INIT_SQL_FILE():
    print(f"Ejecutando {INIT_SQL_FILE} ...")
    try:
        conn = psycopg2.connect(
            host=DATABASE_HOST,
            port=DATABASE_PORT,
            user=POSTGRESQL_USERNAME,
            password=POSTGRESQL_PASSWORD,
            dbname=MLFLOW_DATABASE_NAME
        )
        conn.autocommit = True
        cur = conn.cursor()
        with open(INIT_SQL_FILE, 'r') as f:
            sql = f.read()
            cur.execute(sql)
        cur.close()
        conn.close()
        print("SQL ejecutado correctamente.")
    except Exception as e:
        print("Error al ejecutar SQL:", e)
        sys.exit(1)

if __name__ == "__main__":
    wait_for_postgres()
    list_databases()
    create_database_if_not_exists(MLFLOW_DATABASE_NAME)
    execute_INIT_SQL_FILE()
