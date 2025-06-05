import mysql.connector
import os

DIRECTORIO_ROSTROS = "data/rostros_conocidos"

def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='12admin34',
        database='bdplantas'
    )

def verificar_base_datos_rostros():
    if not os.path.isdir(DIRECTORIO_ROSTROS):
        print(f"Error: El directorio '{DIRECTORIO_ROSTROS}' no existe.")
        return False
    print(f"Base de datos de rostros lista: {DIRECTORIO_ROSTROS}")
    return True
