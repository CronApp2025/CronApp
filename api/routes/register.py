
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from helper.validations import validate_email_format
from helper.database import get_db_cursor, fetch_one_dict_from_result
from helper.response_utils import success_response, error_response

register = Blueprint('register', __name__)

@register.route('/', methods=['POST'])
def register_usuario():
    try:
        data = request.get_json()
        print(f"Recibida solicitud de registro: {data}")

        # Validar campos requeridos
        required_fields = ['nombre', 'apellido', 'email', 'password', 'fecha_nacimiento']
        for field in required_fields:
            if field not in data:
                return error_response(f"El campo {field} es requerido", 400)

        # Validar formato de email
        if not validate_email_format(data['email']):
            return error_response("Formato de email inválido", 400)

        # Validar contraseña
        if len(data['password']) < 6:
            return error_response("La contraseña debe tener al menos 6 caracteres", 400)

        # Hash de la contraseña
        hashed_password = generate_password_hash(data['password'])

        with get_db_cursor(dictionary=True) as cursor:
            # Verificar si el email ya existe
            cursor.execute("SELECT id FROM users WHERE email = %s", (data['email'],))
            existing_user = cursor.fetchone()

            if existing_user:
                return error_response("El email ya está registrado", 400)

            # Insertar el nuevo usuario
            insert_query = """
            INSERT INTO users (nombre, apellido, email, password, fecha_nacimiento, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
            """

            cursor.execute(insert_query, (
                data['nombre'],
                data['apellido'],
                data['email'],
                hashed_password,
                data['fecha_nacimiento']
            ))

            # Obtener el ID del usuario insertado
            user_id = cursor.lastrowid

            # Obtener los datos del usuario creado
            cursor.execute("""
                SELECT id, nombre, apellido, email, fecha_nacimiento 
                FROM users WHERE id = %s
            """, (user_id,))
            new_user = cursor.fetchone()

            if not new_user:
                raise Exception("Error al crear el usuario")

            return success_response(
                data=new_user,
                msg="Usuario registrado exitosamente"
            )

    except Exception as e:
        print(f"Error en register_usuario: {str(e)}")
        return error_response(f"Error al registrar: {str(e)}", 500)
