#a
from contextlib import contextmanager
import mysql.connector
from api.config import DB_CONFIG
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

def fetch_one_dict_from_result(result):
    """Fetch one row from a MySQL result as dictionary"""
    row = result.fetchone()
    if not row:
        return None
    return dict(zip(result.column_names, row))

def fetch_all_dict_from_result(result):
    """Fetch all rows from a MySQL result as list of dictionaries"""
    rows = result.fetchall()
    if not rows:
        return []
    return [dict(zip(result.column_names, row)) for row in rows]
