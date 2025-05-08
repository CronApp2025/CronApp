# db.py
import os
import psycopg2
from psycopg2.extras import DictCursor
from config import DB_CONFIG, DATABASE_URL

def get_connection():
    """
    Obtiene una conexión a la base de datos PostgreSQL usando las credenciales 
    definidas en las variables de entorno o en config.py
    """
    try:
        # Intentar usar la URL de conexión directamente
        if DATABASE_URL:
            conn = psycopg2.connect(DATABASE_URL)
            print("Conexión establecida con éxito usando DATABASE_URL")
            return conn
        # Si no hay URL, usar los parámetros individuales
        else:
            conn = psycopg2.connect(
                host=DB_CONFIG['host'],
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password'],
                dbname=DB_CONFIG['database'],
                port=DB_CONFIG['port']
            )
            print("Conexión establecida con éxito usando parámetros individuales")
            return conn
    except Exception as e:
        print(f"Error de conexión a la base de datos: {str(e)}")
        print(f"DATABASE_URL: {DATABASE_URL}")
        print(f"DB_CONFIG: {DB_CONFIG}")
        raise

# Prueba de conexión
def test_db_connection():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print(f"Prueba de conexión exitosa: {result}")
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al probar la conexión: {str(e)}")
        return False