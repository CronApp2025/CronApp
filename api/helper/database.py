#a
from contextlib import contextmanager
import mysql.connector
from config import DB_CONFIG
from mysql.connector import Error

@contextmanager
def get_db_cursor(dictionary=True):
    """Get database cursor with context management"""
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=dictionary)
        yield cursor
        conn.commit()
    except Error as e:
        if conn and conn.is_connected():
            conn.rollback()
        raise e
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

def fetch_one_dict_from_result(cursor):
    """Fetch one row from a MySQL cursor as dictionary"""
    row = cursor.fetchone()
    if not row:
        return None
    # Si ya es un diccionario, devolver directamente
    if isinstance(row, dict):
        return row
    # Si no, convertirlo en un diccionario
    return dict(zip(cursor.column_names, row))

def fetch_all_dict_from_result(cursor):
    """Fetch all rows from a MySQL cursor as list of dictionaries"""
    rows = cursor.fetchall()
    if not rows:
        return []
    # Si ya son diccionarios, devolver directamente
    if rows and isinstance(rows[0], dict):
        return rows
    # Si no, convertirlos en diccionarios
    return [dict(zip(cursor.column_names, row)) for row in rows]
