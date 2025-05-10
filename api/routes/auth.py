from flask import request, jsonify, Blueprint
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from helper.Middleware.jwt_manager import jwt_required_custom
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
import random, string
from config import EXPIRE_TOKEN_TIME
from helper.database import get_db_cursor, fetch_one_dict_from_result
from database.procedures import *
from helper.response_utils import success_response, error_response
from helper.transaction import db_transaction
from flask_jwt_extended import get_jwt

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    try:
        print("Recibida solicitud de login")
        data = request.get_json()
        if not data:
            print("No se recibieron datos JSON")
            return error_response("No se recibieron datos JSON", 400)
            
        print(f"Datos recibidos: {data}")
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            print(f"Faltan datos: email={email}, password={'*' * len(password) if password else None}")
            return error_response("Email y contraseña son requeridos", 400)

        # Consultar usuario en la base de datos PostgreSQLa
        with get_db_cursor(dictionary=True) as cursor:
            # Usar consulta directa en lugar de procedimiento almacenado
            query = "SELECT id, nombre, apellido, email, password, fecha_nacimiento FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            user_data = fetch_one_dict_from_result(cursor)
            
            if not user_data:
                print(f"Usuario no encontrado para el email: {email}")
                return error_response("Credenciales inválidas", 401)
            
            # Verificar la contraseña
            stored_password = user_data.get('password', '')
            
            # Verificar diversos formatos de hash de Werkzeug
            if stored_password.startswith(('pbkdf2:', 'scrypt:', 'sha256:')): 
                # Werkzeug genera distintos formatos según la versión
                try:
                    is_valid = check_password_hash(stored_password, password)
                except Exception as e:
                    print(f"Error al verificar contraseña: {e}")
                    is_valid = False
            else:
                # Comparación simple para contraseñas sin hash (sólo para desarrollo)
                is_valid = stored_password == password
                
                # Si es válida, aprovechamos para actualizar a un formato seguro
                if is_valid and stored_password != '':
                    try:
                        secure_password = generate_password_hash(password)
                        update_query = "UPDATE users SET password = %s, updated_at = NOW() WHERE id = %s"
                        cursor.execute(update_query, (secure_password, user_data['id']))
                        # El commit se maneja automáticamente dentro del contexto get_db_cursor
                        print(f"Contraseña actualizada a formato seguro para usuario: {user_data['id']}")
                    except Exception as e:
                        print(f"Error al actualizar contraseña a formato seguro: {e}")
                
            if not is_valid:
                print("Contraseña incorrecta")
                return error_response("Credenciales inválidas", 401)
        
        print(f"Usuario encontrado: {user_data}")
        
        # Convertir fecha_nacimiento a string si es un objeto date
        if isinstance(user_data.get('fecha_nacimiento'), datetime):
            user_data['fecha_nacimiento'] = user_data['fecha_nacimiento'].strftime('%Y-%m-%d')
        
        # Eliminar la contraseña del objeto de usuario antes de devolverlo
        if 'password' in user_data:
            del user_data['password']
        
        access_token = build_token(
            user_id=user_data['id'],
            additional_claims={
                'email': user_data.get('email'),
                'nombre': user_data.get('nombre'),
                'apellido': user_data.get('apellido'),
                'fecha_nacimiento': user_data.get('fecha_nacimiento')                    
            }
        )
        
        refresh_token = create_refresh_token(identity=user_data['id'])
        
        response_data = {
            **user_data,
            'access_token': access_token,
            'refresh_token': refresh_token
        }
        
        access_exp_time = datetime.now() + timedelta(minutes=EXPIRE_TOKEN_TIME["ACCESS_TOKEN_MINUTES"])
        refresh_exp_time = datetime.now() + timedelta(days=7)
        
        print(f"Access token expira a las: {access_exp_time.strftime('%H:%M:%S')}")
        print(f"Refresh token expira a las: {refresh_exp_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        return success_response(data=response_data)

    except Exception as e:
        print(f"Error en login: {str(e)}")
        return error_response(f"Error en el login: {str(e)}")

@auth.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    try:
        current_user = get_jwt_identity()
        
        # Obtener datos del usuario desde la base de datos para incluir en el token
        with get_db_cursor(dictionary=True) as cursor:
            query = "SELECT id, nombre, apellido, email, fecha_nacimiento FROM users WHERE id = %s"
            cursor.execute(query, (current_user,))
            user_data = fetch_one_dict_from_result(cursor)
            
            if not user_data:
                return error_response("Usuario no encontrado", 404)
            
            # Convertir fecha_nacimiento a string si es un objeto date
            if isinstance(user_data.get('fecha_nacimiento'), datetime):
                user_data['fecha_nacimiento'] = user_data['fecha_nacimiento'].strftime('%Y-%m-%d')

            new_access_token = build_token(
                user_id=user_data['id'],
                additional_claims={
                    'email': user_data.get('email'),
                    'nombre': user_data.get('nombre'),
                    'apellido': user_data.get('apellido'),
                    'fecha_nacimiento': user_data.get('fecha_nacimiento')                    
                }
            )
            
            response_data = {
                'access_token': new_access_token
            }
            
            new_exp_time = datetime.now() + timedelta(minutes=EXPIRE_TOKEN_TIME["MINUTOS"])
            print(f"Nuevo access token expira a las: {new_exp_time.strftime('%H:%M:%S')}")
            
            return success_response(data=response_data)

    except Exception as e:
        print(f"Error al refrescar el token: {str(e)}")
        return error_response(f"Error al refrescar el token: {str(e)}")

@auth.route('/google', methods=['POST'])
def google_auth():
    """
    Endpoint para la autenticación con Google.
    Recibe los datos del usuario autenticado con Google y crea o actualiza el usuario en nuestra BD.
    """
    try:
        # Obtener datos enviados desde el frontend
        data = request.get_json()
        print("Datos recibidos de Google:", data)
        
        email = data.get('email')
        nombre = data.get('nombre', '')
        apellido = data.get('apellido', '')
        google_id = data.get('google_id', '')
        fecha_nacimiento = data.get('fecha_nacimiento', None)
        profile_picture = data.get('profile_picture', '')
        
        if not email:
            return error_response("Email es requerido", 400)
        
        # Verificar si el usuario ya existe por email
        with get_db_cursor(dictionary=True) as cursor:
            # Buscar usuario por email
            query = "SELECT id, nombre, apellido, email, fecha_nacimiento FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            user_data = fetch_one_dict_from_result(cursor)
            
            is_new_user = False
            
            # Si el usuario no existe, crearlo
            if not user_data:
                is_new_user = True
                
                # Generar una contraseña aleatoria segura para usuarios de Google
                temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
                hashed_password = generate_password_hash(temp_password)
                
                # Insertar el nuevo usuario
                insert_query = """
                INSERT INTO users (nombre, apellido, email, password, fecha_nacimiento, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
                RETURNING id, nombre, apellido, email, fecha_nacimiento
                """
                
                # Manejar fecha_nacimiento si está presente
                if fecha_nacimiento:
                    try:
                        # Intentar convertir a formato de fecha
                        datetime.strptime(fecha_nacimiento, '%Y-%m-%d')
                    except ValueError:
                        # Si falla, usar una fecha por defecto
                        fecha_nacimiento = '2000-01-01'
                else:
                    fecha_nacimiento = '2000-01-01'
                
                cursor.execute(insert_query, (nombre, apellido, email, hashed_password, fecha_nacimiento))
                # El commit se maneja automáticamente dentro del contexto get_db_cursor
                
                user_data = fetch_one_dict_from_result(cursor)
                if not user_data:
                    return error_response("Error al crear el usuario", 500)
        
        # Convertir fecha_nacimiento a string si es un objeto date
        if isinstance(user_data.get('fecha_nacimiento'), datetime):
            user_data['fecha_nacimiento'] = user_data['fecha_nacimiento'].strftime('%Y-%m-%d')
        
        # Generar tokens de acceso y refresco
        access_token = build_token(
            user_id=user_data['id'],
            additional_claims={
                'email': user_data.get('email'),
                'nombre': user_data.get('nombre'),
                'apellido': user_data.get('apellido'),
                'fecha_nacimiento': user_data.get('fecha_nacimiento')                    
            }
        )
        
        refresh_token = create_refresh_token(identity=user_data['id'])
        
        # Preparar respuesta para el frontend
        response_data = {
            **user_data,
            'access_token': access_token,
            'refresh_token': refresh_token,
            'is_new_user': is_new_user
        }
        
        return success_response(data=response_data)
            
    except Exception as e:
        print(f"Error en la autenticación con Google: {str(e)}")
        return error_response(f"Error en la autenticación con Google: {str(e)}")

@auth.route('/logout', methods=['POST'])
@jwt_required_custom()
def logout():
    try:
        jwt = get_jwt()
        # Importamos TokenManager
        from helper.token_manager import TokenManager
        token_manager = TokenManager()
        
        token_manager.add_to_blacklist(jwt['jti'])
        user_id = jwt.get('sub')
        if user_id:
            token_manager.remove_refresh_token(str(user_id))
        return success_response("Logout exitoso")
    except Exception as e:
        return error_response(f"Error en logout: {str(e)}")

@auth.route('/validate', methods=['POST'])
@jwt_required_custom()
def validate_token():
    try:
        jwt = get_jwt()
        return success_response(data={
            'valid': True,
            'id': jwt.get('user_id'),
            'email': jwt.get('email'),
            'nombre': jwt.get('nombre'),
            'apellido': jwt.get('apellido'),
            'fecha_nacimiento': jwt.get('fecha_nacimiento')
        })
    except Exception as e:
        print(f"Error validating token: {str(e)}")
        return error_response("Invalid token", 401)

def build_token(user_id, additional_claims=None, expires_delta=timedelta(minutes=15)):
    user_id = str(user_id)    
    claims = {
        'user_id': user_id,
    }
    if additional_claims:
        claims.update(additional_claims)

    token = create_access_token(
        identity=user_id,
        additional_claims=claims,
        expires_delta=expires_delta
    )    
    return token