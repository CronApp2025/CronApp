from contextlib import contextmanager
from flask import current_app
import sys
import os

# Importar con la ruta absoluta
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from db import get_connection

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
            cursor = conn.cursor(dictionary=True)
        else:
            cursor = conn.cursor()
        try:
            yield cursor
        finally:
            cursor.close()

def fetch_one_dict_from_result(cursor):
    """
    Convierte un registro de MySQL en un diccionario.
    Con cursor(dictionary=True) en MySQL Connector, ya devuelve diccionarios,
    pero mantenemos esta función para compatibilidad.
    """
    row = cursor.fetchone()
    if row is None:
        return None
    
    # Si ya es un diccionario, devolverlo directamente
    if isinstance(row, dict):
        return row
    
    # Si es una tupla, convertirla a diccionario con los nombres de columna
    if cursor.description:
        column_names = [col[0] for col in cursor.description]
        return dict(zip(column_names, row))
    
    return row

def fetch_all_dict_from_result(cursor):
    """
    Convierte todos los registros de MySQL en una lista de diccionarios.
    Con cursor(dictionary=True) en MySQL Connector, ya devuelve diccionarios,
    pero mantenemos esta función para compatibilidad.
    """
    rows = cursor.fetchall()
    
    # Si ya son diccionarios, devolverlos directamente
    if rows and isinstance(rows[0], dict):
        return rows
    
    # Si son tuplas, convertirlas a diccionarios con los nombres de columna
    if cursor.description:
        column_names = [col[0] for col in cursor.description]
        return [dict(zip(column_names, row)) for row in rows]
    
    return rows