#!/usr/bin/env python
import os
import mysql.connector

def execute_sql_script(conn, script):
    """Ejecuta un script SQL con delimitadores personalizados para procedimientos almacenados"""
    cursor = conn.cursor()
    
    # Dividir el script en procedimientos individuales
    delimiter = "DELIMITER //"
    procedures = script.split(delimiter)
    
    # El primer elemento puede ser vacío o contener comentarios iniciales
    if procedures[0].strip() and not procedures[0].strip().startswith('--'):
        # Ejecutar cualquier comando inicial sin delimitador personalizado
        cursor.execute(procedures[0])
    
    # Procesar cada procedimiento
    for i in range(1, len(procedures)):
        proc = procedures[i].strip()
        if not proc:
            continue
            
        # Obtener el cuerpo del procedimiento hasta el delimitador de cierre
        end_delimiter = "DELIMITER ;"
        if end_delimiter in proc:
            parts = proc.split(end_delimiter)
            proc_body = parts[0]
        else:
            proc_body = proc
            
        # Reemplazar los delimitadores intermedios
        proc_body = proc_body.replace("END //", "END")
        
        # Ejecutar el procedimiento
        try:
            cursor.execute(proc_body)
            print(f"Procedimiento almacenado creado con éxito.")
        except Exception as e:
            print(f"Error al crear procedimiento: {str(e)}")
    
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
        
        # Procedimientos que faltan por implementar
        missing_procedures_sql = """
DELIMITER //

-- Procedimiento para validar token de recuperación
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
END //

-- Procedimiento para actualizar contraseña
CREATE PROCEDURE sp_actualizar_password(
    IN p_user_id INT,
    IN p_new_password VARCHAR(255)
)
BEGIN
    UPDATE users 
    SET password = p_new_password, 
        updated_at = NOW() 
    WHERE id = p_user_id;
END //

-- Procedimiento para invalidar token
CREATE PROCEDURE sp_invalidar_token(
    IN p_token VARCHAR(255)
)
BEGIN
    UPDATE password_reset_tokens 
    SET used_at = NOW() 
    WHERE token = p_token;
END //

-- Procedimiento para editar usuario
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
END //

-- Procedimiento para eliminar usuario
CREATE PROCEDURE eliminar_usuario(
    IN p_id INT
)
BEGIN
    DELETE FROM users WHERE id = p_id;
    SELECT ROW_COUNT() as affected_rows;
END //

-- Procedimiento para buscar usuario por ID
CREATE PROCEDURE buscar_usuario_por_id(
    IN p_id INT
)
BEGIN
    SELECT id, nombre, apellido, email, fecha_nacimiento 
    FROM users 
    WHERE id = p_id;
END //

-- Procedimiento para obtener todos los usuarios
CREATE PROCEDURE obtener_todos_usuarios()
BEGIN
    SELECT id, nombre, apellido, email, fecha_nacimiento 
    FROM users
    ORDER BY apellido, nombre;
END //

DELIMITER ;
        """
        
        print("Creando procedimientos almacenados adicionales...")
        execute_sql_script(conn, missing_procedures_sql)
        
        # Verificar los procedimientos creados
        cursor = conn.cursor()
        cursor.execute("SHOW PROCEDURE STATUS WHERE Db = %s", (database,))
        procedures = cursor.fetchall()
        
        print("\nProcedimientos almacenados en la base de datos:")
        for proc in procedures:
            print(f"- {proc[1]}")
        
        cursor.close()
        conn.close()
        
        print("\nCreación de procedimientos almacenados completada con éxito.")
        return True
        
    except Exception as e:
        print(f"Error al crear procedimientos almacenados: {str(e)}")
        return False

if __name__ == "__main__":
    create_missing_procedures()