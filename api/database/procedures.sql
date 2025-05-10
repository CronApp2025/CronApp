
DELIMITER //

-- Procedimiento para agregar usuario
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
END //

-- Procedimiento para login
CREATE PROCEDURE login(
    IN p_email VARCHAR(255)
)
BEGIN
    SELECT id, nombre, apellido, email, password, fecha_nacimiento
    FROM users
    WHERE email = p_email;
END //

-- Procedimiento para solicitar recuperación de contraseña
CREATE PROCEDURE sp_solicitar_recuperacion(
    IN p_email VARCHAR(255)
)
BEGIN
    SELECT id, nombre, email
    FROM users
    WHERE email = p_email;
END //

-- Procedimiento para guardar token de recuperación
CREATE PROCEDURE sp_guardar_token_recuperacion(
    IN p_user_id INT,
    IN p_token VARCHAR(255),
    IN p_expires_at TIMESTAMP
)
BEGIN
    INSERT INTO password_reset_tokens (user_id, token, expires_at)
    VALUES (p_user_id, p_token, p_expires_at);
END //

DELIMITER ;
