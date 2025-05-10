#!/usr/bin/env python
import os
import mysql.connector

def describe_table(table_name):
    try:
        # Obtener variables de entorno
        host = os.environ.get('MYSQL_HOST')
        user = os.environ.get('MYSQL_USER')
        password = os.environ.get('MYSQL_PASSWORD')
        database = os.environ.get('MYSQL_DATABASE')
        port = os.environ.get('MYSQL_PORT')
        
        print(f"Describiendo tabla {table_name} en {host}:{port}...")
        
        # Establecer conexión
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port
        )
        
        # Ejecutar consulta para describir la tabla
        cursor = conn.cursor()
        cursor.execute(f"DESCRIBE {table_name}")
        columns = cursor.fetchall()
        
        print(f"\nEstructura de la tabla {table_name}:")
        print(f"{'Columna':<20} {'Tipo':<20} {'Nulo':<10} {'Key':<10} {'Default':<20} {'Extra':<20}")
        print("-" * 100)
        
        for column in columns:
            field, type_, null, key, default, extra = column
            print(f"{field:<20} {type_:<20} {null:<10} {key:<10} {str(default):<20} {extra:<20}")
        
        cursor.close()
        conn.close()
        return True
    
    except Exception as e:
        print(f"Error al describir la tabla {table_name}: {str(e)}")
        return False

def main():
    tables = ["users", "conditions", "metrics", "alerts", "educational_resources", "password_reset_tokens"]
    
    for table in tables:
        describe_table(table)
        print("\n" + "=" * 100 + "\n")

if __name__ == "__main__":
    main()