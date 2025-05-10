#!/usr/bin/env python
import os
import mysql.connector
from datetime import datetime

def count_records(table_name):
    try:
        # Obtener variables de entorno
        host = os.environ.get('MYSQL_HOST')
        user = os.environ.get('MYSQL_USER')
        password = os.environ.get('MYSQL_PASSWORD')
        database = os.environ.get('MYSQL_DATABASE')
        port = os.environ.get('MYSQL_PORT')
        
        # Establecer conexión
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port
        )
        
        # Ejecutar consulta para contar registros
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        
        print(f"Tabla {table_name}: {count} registros")
        
        cursor.close()
        conn.close()
        return count
    
    except Exception as e:
        print(f"Error al contar registros en {table_name}: {str(e)}")
        return -1

def sample_data(table_name, limit=5):
    try:
        # Obtener variables de entorno
        host = os.environ.get('MYSQL_HOST')
        user = os.environ.get('MYSQL_USER')
        password = os.environ.get('MYSQL_PASSWORD')
        database = os.environ.get('MYSQL_DATABASE')
        port = os.environ.get('MYSQL_PORT')
        
        # Establecer conexión
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port
        )
        
        # Obtener nombres de columnas
        cursor = conn.cursor()
        cursor.execute(f"DESCRIBE {table_name}")
        columns = [column[0] for column in cursor.fetchall()]
        
        # Obtener una muestra de datos
        cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit}")
        rows = cursor.fetchall()
        
        if rows:
            print(f"\nMuestra de datos en {table_name}:")
            for i, row in enumerate(rows):
                print(f"\nRegistro {i+1}:")
                for j, value in enumerate(row):
                    # Formatear fechas para mejor legibilidad
                    if isinstance(value, datetime):
                        value = value.strftime('%Y-%m-%d %H:%M:%S')
                    print(f"  {columns[j]}: {value}")
        else:
            print(f"\nNo hay datos en la tabla {table_name}")
        
        cursor.close()
        conn.close()
        return True
    
    except Exception as e:
        print(f"Error al obtener muestra de datos de {table_name}: {str(e)}")
        return False

def main():
    tables = ["users", "conditions", "metrics", "alerts", "educational_resources", "password_reset_tokens"]
    
    print("=== Conteo de registros ===")
    for table in tables:
        count = count_records(table)
        if count > 0:
            sample_data(table, 2)  # Mostrar 2 registros como ejemplo
        print("\n" + "=" * 50)

if __name__ == "__main__":
    main()