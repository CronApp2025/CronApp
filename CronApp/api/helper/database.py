from contextlib import contextmanager
from flask import current_app
import sys
import os

# Importar con la ruta absoluta
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from db import get_connection
from psycopg2.extras import DictCursor

@contextmanager
def get_db_connection():
    conn = None
    try:
        conn = get_connection() 
        yield conn
    except Exception as e:
        current_app.logger.error(f"Error de conexión: {str(e)}")
        raise
    finally:
        if conn:
            conn.close()

@contextmanager
def get_db_cursor(dictionary=True):
    with get_db_connection() as conn:
        if dictionary:
            cursor = conn.cursor(cursor_factory=DictCursor)
        else:
            cursor = conn.cursor()
        try:
            yield cursor
        finally:
            cursor.close()

def fetch_one_dict_from_result(cursor):
    """
    PostgreSQL con psycopg2.extras.DictCursor ya retorna resultados como diccionarios
    cuando se usa dictionary=True en get_db_cursor, pero mantenemos esta función
    para compatibilidad con el código existente.
    """
    row = cursor.fetchone()
    if row is None:
        return None
    return dict(row) if hasattr(row, 'keys') else row

def fetch_all_dict_from_result(cursor):
    """
    PostgreSQL con psycopg2.extras.DictCursor ya retorna resultados como diccionarios
    cuando se usa dictionary=True en get_db_cursor, pero mantenemos esta función
    para compatibilidad con el código existente.
    """
    rows = cursor.fetchall()
    return [dict(row) if hasattr(row, 'keys') else row for row in rows]