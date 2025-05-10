#!/usr/bin/env pythona
import os
import mysql.connector

def test_mysql_connection():
    try:
        # Obtener variables de entorno
        host = os.environ.get('MYSQL_HOST')
        user = os.environ.get('MYSQL_USER')
        password = os.environ.get('MYSQL_PASSWORD')
        database = os.environ.get('MYSQL_DATABASE')
        port = os.environ.get('MYSQL_PORT')
        
        print(f"Intentando conectar a MySQL en {host}:{port}...")
        
        # Intentar establecer conexión
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port
        )
        
        # Ejecutar una consulta simple para verificar la conexión
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        
        print(f"Conexión exitosa a MySQL! Resultado: {result}")
        
        # Listar las tablas en la base de datos
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        if tables:
            print("Tablas en la base de datos:")
            for table in tables:
                print(f"- {table[0]}")
        else:
            print("No hay tablas en la base de datos.")
        
        cursor.close()
        conn.close()
        return True
    
    except Exception as e:
        print(f"Error al conectar a MySQL: {str(e)}")
        return False

if __name__ == "__main__":
    test_mysql_connection()