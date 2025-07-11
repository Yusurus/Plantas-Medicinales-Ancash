import mysql.connector
import os
from dotenv import load_dotenv

DIRECTORIO_ROSTROS = "data/rostros_conocidos"

load_dotenv()


def get_connection():
    return mysql.connector.connect(
        # es necesario tener un archivo .env con las variables de entorno
        host=os.environ.get("MYSQL_HOST"),
        user=os.environ.get("MYSQL_USER"),
        password=os.environ.get("MYSQL_PASSWORD"),
        database=os.environ.get("MYSQL_DB"),
        port=os.environ.get("MYSQL_PORT"),
        charset="utf8mb4",
        collation="utf8mb4_general_ci",
    )


def verificar_base_datos_rostros():
    if not os.path.isdir(DIRECTORIO_ROSTROS):
        print(f"Error: El directorio '{DIRECTORIO_ROSTROS}' no existe.")
        return False
    print(f"Base de datos de rostros lista: {DIRECTORIO_ROSTROS}")
    return True
