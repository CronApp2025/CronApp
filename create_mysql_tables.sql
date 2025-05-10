-- Script para crear las tablas en MySQL
-- Basado en el esquema definido en shared/schema.ts

-- Eliminar tablas si existen para evitar conflictos
DROP TABLE IF EXISTS password_reset_tokens;
DROP TABLE IF EXISTS metrics;
DROP TABLE IF EXISTS alerts;
DROP TABLE IF EXISTS educational_resources;
DROP TABLE IF EXISTS conditions;
DROP TABLE IF EXISTS users;

-- Crear tabla de usuarios
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(255) NOT NULL,
  apellido VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  password VARCHAR(255),
  fecha_nacimiento DATE NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Crear tabla de condiciones médicas
CREATE TABLE conditions (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  name VARCHAR(255) NOT NULL,
  type VARCHAR(255) NOT NULL,
  icon VARCHAR(255) DEFAULT 'activity',
  diagnosed_date DATE NOT NULL,
  last_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Crear tabla de métricas médicas
CREATE TABLE metrics (
  id INT AUTO_INCREMENT PRIMARY KEY,
  condition_id INT NOT NULL,
  `key` VARCHAR(255) NOT NULL,
  value VARCHAR(255) NOT NULL,
  unit VARCHAR(255),
  risk_level VARCHAR(50),
  date_recorded TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (condition_id) REFERENCES conditions(id) ON DELETE CASCADE
);

-- Crear tabla de alertas de riesgo
CREATE TABLE alerts (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  alert_type VARCHAR(255) NOT NULL,
  description TEXT NOT NULL,
  risk_level INT NOT NULL,
  is_resolved BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Crear tabla de recursos educativos
CREATE TABLE educational_resources (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  description TEXT NOT NULL,
  category VARCHAR(100) NOT NULL,
  resource_type VARCHAR(100) NOT NULL,
  url TEXT,
  is_new BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Crear tabla de tokens para restablecer contraseña
CREATE TABLE password_reset_tokens (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  token VARCHAR(255) NOT NULL UNIQUE,
  expires_at TIMESTAMP NOT NULL,
  used_at TIMESTAMP NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Mensajes de confirmación
SELECT 'Todas las tablas han sido creadas correctamente' AS Mensaje;