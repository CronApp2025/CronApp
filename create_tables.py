#!/usr/bin/env python
import os
import mysql.connector
import logging

# Configurar logging a
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_mysql_connection():
    """Obtiene una conexión a la base de datos MySQL usando las variables de entorno"""
    try:
        conn = mysql.connector.connect(
            host=os.environ.get('MYSQL_HOST'),
            user=os.environ.get('MYSQL_USER'),
            password=os.environ.get('MYSQL_PASSWORD'),
            database=os.environ.get('MYSQL_DATABASE'),
            port=os.environ.get('MYSQL_PORT')
        )
        logger.info(f"Conexión establecida con éxito a la base de datos MySQL en {os.environ.get('MYSQL_HOST')}:{os.environ.get('MYSQL_PORT')}")
        return conn
    except Exception as e:
        logger.error(f"Error de conexión a la base de datos: {str(e)}")
        raise

def execute_sql_script(file_path):
    """Lee y ejecuta un archivo SQL"""
    try:
        # Leer el archivo SQL
        with open(file_path, 'r') as sql_file:
            sql_script = sql_file.read()
        
        # Dividir el script en comandos individuales
        conn = get_mysql_connection()
        cursor = conn.cursor()
        
        # Dividir por ; pero ignorar los ; dentro de las cadenas
        # Este es un enfoque simple, para scripts complejos podría necesitar mejoras
        commands = sql_script.split(';')
        
        for command in commands:
            # Limpiar espacios en blanco y saltos de línea
            command = command.strip()
            if command:
                try:
                    logger.info(f"Ejecutando: {command[:100]}...")  # Mostrar primeros 100 caracteres
                    cursor.execute(command)
                    if cursor.with_rows:
                        results = cursor.fetchall()
                        for row in results:
                            logger.info(f"Resultado: {row}")
                except Exception as e:
                    logger.error(f"Error ejecutando comando SQL: {str(e)}")
                    logger.error(f"Comando que falló: {command}")
                    raise
        
        # Confirmar cambios
        conn.commit()
        logger.info("Ejecución del script SQL completada con éxito")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Error al ejecutar el script SQL: {str(e)}")
        if 'conn' in locals() and conn.is_connected():
            conn.rollback()
            conn.close()
        return False

if __name__ == "__main__":
    # Probar la conexión
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        logger.info(f"Prueba de conexión exitosa: {result}")
        cursor.close()
        conn.close()
        
        # Ejecutar el script SQL para crear las tablas
        sql_file_path = 'create_mysql_tables.sql'
        if os.path.exists(sql_file_path):
            success = execute_sql_script(sql_file_path)
            if success:
                logger.info("¡Todas las tablas han sido creadas correctamente!")
            else:
                logger.error("No se pudieron crear todas las tablas.")
        else:
            logger.error(f"El archivo {sql_file_path} no existe.")
    
    except Exception as e:
        logger.error(f"Error general: {str(e)}")