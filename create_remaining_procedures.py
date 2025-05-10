#!/usr/bin/env python
import os
import mysql.connector

def create_procedure(conn, procedure_name, procedure_sql):
    """Crea un único procedimiento almacenado"""
    cursor = conn.cursor()
    try:
        # Primero eliminar el procedimiento si ya existe
        cursor.execute(f"DROP PROCEDURE IF EXISTS {procedure_name}")
        
        # Crear el procedimiento
        cursor.execute(procedure_sql)
        print(f"Procedimiento '{procedure_name}' creado con éxito.")
        return True
    except Exception as e:
        print(f"Error al crear procedimiento '{procedure_name}': {str(e)}")
        return False
    finally:
        cursor.close()

def create_remaining_procedures():
    """Crea los procedimientos almacenados restantes mencionados en procedures.py"""
    # Obtener variables de entorno
    host = os.environ.get('MYSQL_HOST')
    user = os.environ.get('MYSQL_USER')
    password = os.environ.get('MYSQL_PASSWORD')
    database = os.environ.get('MYSQL_DATABASE')
    port = os.environ.get('MYSQL_PORT')
    
    try:
        # Establecer conexión
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port
        )
        
        # Procedimientos para almacenamiento de token y login
        procedures = [
            ("agregar_usuario", """
CREATE PROCEDURE agregar_usuario(
    IN p_nombre VARCHAR(255),
    IN p_apellido VARCHAR(255),
    IN p_email VARCHAR(255),
    IN p_password VARCHAR(255),
    IN p_fecha_nacimiento DATE
)
BEGIN
    INSERT INTO users (nombre, apellido, email, password, fecha_nacimiento)
    VALUES (p_nombre, p_apellido, p_email, p_password, p_fecha_nacimiento);
    
    SELECT id, nombre, apellido, email, fecha_nacimiento 
    FROM users 
    WHERE id = LAST_INSERT_ID();
END
            """),
            
            ("login", """
CREATE PROCEDURE login(
    IN p_email VARCHAR(255)
)
BEGIN
    SELECT id, nombre, apellido, email, password, fecha_nacimiento
    FROM users
    WHERE email = p_email;
END
            """),
            
            ("sp_solicitar_recuperacion", """
CREATE PROCEDURE sp_solicitar_recuperacion(
    IN p_email VARCHAR(255)
)
BEGIN
    SELECT id, nombre, email
    FROM users
    WHERE email = p_email;
END
            """),
            
            ("sp_guardar_token_recuperacion", """
CREATE PROCEDURE sp_guardar_token_recuperacion(
    IN p_user_id INT,
    IN p_token VARCHAR(255),
    IN p_expires_at TIMESTAMP
)
BEGIN
    INSERT INTO password_reset_tokens (user_id, token, expires_at)
    VALUES (p_user_id, p_token, p_expires_at);
END
            """)
        ]
        
        print("Creando procedimientos almacenados adicionales...")
        for name, sql in procedures:
            create_procedure(conn, name, sql)
        
        # Verificar los procedimientos creados
        cursor = conn.cursor()
        cursor.execute("SHOW PROCEDURE STATUS WHERE Db = %s", (database,))
        all_procedures = cursor.fetchall()
        
        print("\nTodos los procedimientos almacenados en la base de datos:")
        for proc in all_procedures:
            print(f"- {proc[1]}")
        
        cursor.close()
        conn.close()
        
        print("\nCreación de todos los procedimientos almacenados completada.")
        return True
        
    except Exception as e:
        print(f"Error general al crear procedimientos adicionales: {str(e)}")
        return False

if __name__ == "__main__":
    create_remaining_procedures()