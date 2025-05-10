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

def create_missing_procedures():
    """Crea los procedimientos almacenados que faltan en la base de datos"""
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
        
        # Definir los procedimientos individualmente
        procedures = [
            ("sp_validar_token_recuperacion", """
CREATE PROCEDURE sp_validar_token_recuperacion(
    IN p_token VARCHAR(255)
)
BEGIN
    SELECT t.id, t.user_id as id_usuario, t.token, t.expires_at,
           t.used_at IS NOT NULL as usado,
           NOW() > t.expires_at as expirado,
           u.email
    FROM password_reset_tokens t
    JOIN users u ON t.user_id = u.id
    WHERE t.token = p_token;
END
            """),
            
            ("sp_actualizar_password", """
CREATE PROCEDURE sp_actualizar_password(
    IN p_user_id INT,
    IN p_new_password VARCHAR(255)
)
BEGIN
    UPDATE users 
    SET password = p_new_password, 
        updated_at = NOW() 
    WHERE id = p_user_id;
END
            """),
            
            ("sp_invalidar_token", """
CREATE PROCEDURE sp_invalidar_token(
    IN p_token VARCHAR(255)
)
BEGIN
    UPDATE password_reset_tokens 
    SET used_at = NOW() 
    WHERE token = p_token;
END
            """),
            
            ("editar_usuario", """
CREATE PROCEDURE editar_usuario(
    IN p_id INT,
    IN p_nombre VARCHAR(255),
    IN p_apellido VARCHAR(255),
    IN p_email VARCHAR(255),
    IN p_fecha_nacimiento DATE
)
BEGIN
    UPDATE users 
    SET nombre = p_nombre,
        apellido = p_apellido,
        email = p_email,
        fecha_nacimiento = p_fecha_nacimiento,
        updated_at = NOW()
    WHERE id = p_id;
    
    SELECT id, nombre, apellido, email, fecha_nacimiento 
    FROM users 
    WHERE id = p_id;
END
            """),
            
            ("eliminar_usuario", """
CREATE PROCEDURE eliminar_usuario(
    IN p_id INT
)
BEGIN
    DELETE FROM users WHERE id = p_id;
    SELECT ROW_COUNT() as affected_rows;
END
            """),
            
            ("buscar_usuario_por_id", """
CREATE PROCEDURE buscar_usuario_por_id(
    IN p_id INT
)
BEGIN
    SELECT id, nombre, apellido, email, fecha_nacimiento 
    FROM users 
    WHERE id = p_id;
END
            """),
            
            ("obtener_todos_usuarios", """
CREATE PROCEDURE obtener_todos_usuarios()
BEGIN
    SELECT id, nombre, apellido, email, fecha_nacimiento 
    FROM users
    ORDER BY apellido, nombre;
END
            """)
        ]
        
        print("Creando procedimientos almacenados adicionales...")
        for name, sql in procedures:
            create_procedure(conn, name, sql)
        
        # Verificar los procedimientos creados
        cursor = conn.cursor()
        cursor.execute("SHOW PROCEDURE STATUS WHERE Db = %s", (database,))
        procedures = cursor.fetchall()
        
        print("\nProcedimientos almacenados en la base de datos:")
        for proc in procedures:
            print(f"- {proc[1]}")
        
        cursor.close()
        conn.close()
        
        print("\nCreación de procedimientos almacenados completada.")
        return True
        
    except Exception as e:
        print(f"Error general al crear procedimientos almacenados: {str(e)}")
        return False

if __name__ == "__main__":
    create_missing_procedures()