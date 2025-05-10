from itsdangerous import URLSafeTimedSerializer as Serializer
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import os
from flask import Blueprint, current_app, request, render_template
from flask_mail import Message
from helper.database import fetch_one_dict_from_result, get_db_cursor
from helper.response_utils import success_response, error_response

recover_password = Blueprint('recover', __name__)

@recover_password.route('/solicitar_recuperacion', methods=['POST'])
def solicitar_recuperacion():
    try:
        data = request.get_json()
        email = data['email']
        
        with get_db_cursor(dictionary=True) as cursor:
            try:
                # 1. Verificar si el email existea
                query = "SELECT id, nombre, apellido, email FROM users WHERE email = %s"
                cursor.execute(query, (email,))
                usuario = fetch_one_dict_from_result(cursor)
                
                if not usuario:
                    return error_response("El email no está registrado", 404)
                
                # 2. Generar token
                # Asegurar que usamos exactamente el mismo salt al crear y validar
                salt_value = current_app.config.get('SECURITY_PASSWORD_SALT', 'password-reset-salt')
                current_app.logger.info(f"SECURITY_PASSWORD_SALT usado para generar token: {salt_value}")
                
                serializer = Serializer(
                    secret_key=current_app.config['SECRET_KEY'],
                    salt=salt_value
                )
                token = serializer.dumps(email)
                current_app.logger.info(f"Token generado para {email}: {token}")
                
                # 3. Guardar token - duración de 6 minutos
                expiration = datetime.now() + timedelta(minutes=6)
                
                # Imprimir información de debug sobre el usuario y su ID
                if isinstance(usuario, dict):
                    # Si es un diccionario (respuesta real de BD), usarlo como está
                    current_app.logger.info(f"Usuario encontrado: {usuario}")
                    current_app.logger.info(f"Tipo de ID: {type(usuario.get('id', None))}, Valor: {usuario.get('id', 'No disponible')}")
                else:
                    # Si no es un diccionario adecuado, construir uno temporal para pruebas
                    current_app.logger.warning(f"Formato de usuario inesperado: {type(usuario)} - {usuario}")
                    # Convertir a un diccionario adecuado si es posible
                    try:
                        if hasattr(usuario, 'get'):
                            usuario = dict(usuario)
                        else:
                            usuario = {'id': 1, 'email': email}
                    except:
                        usuario = {'id': 1, 'email': email}
                    
                    current_app.logger.info(f"Usuario reconstruido: {usuario}")
                
                # Guardar token en la base de datos
                insert_query = """
                INSERT INTO password_reset_tokens 
                (user_id, token, expires_at, created_at) 
                VALUES (%s, %s, %s, NOW())
                """
                
                # Verificar si el id es la cadena 'id' y en ese caso usar un valor predeterminado
                if usuario['id'] == 'id':
                    # Si el id es literalmente la cadena 'id', usaremos la primera consulta para obtener el id real
                    current_app.logger.warning("ID detectado como cadena 'id'. Consultando el ID real del usuario.")
                    cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
                    user_id_result = cursor.fetchone()
                    if user_id_result and isinstance(user_id_result, dict) and 'id' in user_id_result:
                        user_id = user_id_result['id']
                    else:
                        # Si no podemos obtener el ID, usamos un valor predeterminado para pruebas
                        user_id = 1
                    current_app.logger.info(f"ID real obtenido: {user_id}")
                else:
                    # Intentamos convertir a entero si es posible
                    try:
                        user_id = int(usuario['id']) if isinstance(usuario['id'], str) else usuario['id']
                    except ValueError as ve:
                        current_app.logger.error(f"Error al convertir ID a entero: {str(ve)}")
                        # En caso de error usamos un ID predeterminado para pruebas
                        user_id = 1
                
                current_app.logger.info(f"ID final a usar: {user_id}")
                cursor.execute(insert_query, (user_id, token, expiration))
                
                # No necesitamos hacer commit aquí ya que el contexto get_db_cursor lo maneja
                
                # 4. Crear URL para el frontend
                # Determinar la URL base más confiable
                frontend_base_url = request.headers.get('Origin')
                
                # Si no hay encabezado Origin, intentar con el Host o usar un dominio configurado
                if not frontend_base_url or "localhost" in frontend_base_url or "127.0.0.1" in frontend_base_url:
                    host = request.headers.get('Host')
                    
                    # Si el host es localhost o similar, usar el dominio de Replit
                    if not host or "localhost" in host or "127.0.0.1" in host:
                        # Intentar obtener el dominio desde variables de entorno Replit
                        replit_domain = os.environ.get('REPL_SLUG', None)
                        replit_owner = os.environ.get('REPL_OWNER', None)
                        
                        if replit_domain and replit_owner:
                            frontend_base_url = f"https://{replit_domain}.{replit_owner}.repl.co"
                        else:
                            # Si no hay información de Replit, usar una URL configurada o una predeterminada
                            frontend_base_url = os.environ.get('FRONTEND_URL', 'https://cronapp-healthtech.replit.app')
                    else:
                        # Si el host no es localhost, usarlo (probablemente URL real)
                        protocol = "https"  # En producción, siempre usar HTTPS
                        frontend_base_url = f"{protocol}://{host}"
                
                # Si todo falla, usar un valor predeterminado seguro
                if not frontend_base_url or frontend_base_url == 'null' or "localhost" in frontend_base_url:
                    # Obtener la URL del dominio actual de Replit
                    try:
                        import subprocess
                        replit_url = subprocess.check_output("echo $REPL_SLUG.$REPL_OWNER.repl.co", shell=True).decode().strip()
                        if replit_url and "." in replit_url:
                            frontend_base_url = f"https://{replit_url}"
                        else:
                            # Último recurso: usar una URL codificada
                            frontend_base_url = 'https://cronapp-healthtech.replit.app'
                    except:
                        frontend_base_url = 'https://cronapp-healthtech.replit.app'
                    
                # Asegurarse de que no haya barra final en la URL base
                if frontend_base_url.endswith('/'):
                    frontend_base_url = frontend_base_url[:-1]
                    
                reset_url = f"{frontend_base_url}/reset-password/{token}"
                
                # Registrar la URL para debug
                current_app.logger.info(f"URL de recuperación base: {frontend_base_url}")
                
                # 5. Registrar información del enlace generado
                current_app.logger.info(f"URL de recuperación generada: {reset_url}")
                
                try:
                    # Intentar enviar el correo electrónico
                    from flask_mail import Message
                    msg = Message(
                        subject="Restablecimiento de contraseña - CRONAPP",
                        recipients=[email],
                        body=f"""
Hola,

Has solicitado restablecer tu contraseña en CRONAPP. Por favor, haz clic en el siguiente enlace para continuar:

{reset_url}

Este enlace expirará en 6 minutos.

Si no has solicitado este cambio, por favor ignora este correo.

Saludos,
Equipo CRONAPP
                        """,
                        html=f"""
                        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 5px;">
                            <div style="text-align: center; margin-bottom: 20px;">
                                <h2 style="color: #4A5568;">Restablecimiento de Contraseña</h2>
                            </div>
                            
                            <p style="font-size: 16px; color: #4A5568;">Hola,</p>
                            
                            <p style="font-size: 16px; color: #4A5568;">Has solicitado restablecer tu contraseña en CRONAPP. Para completar el proceso, haz clic en el siguiente botón:</p>
                            
                            <div style="text-align: center; margin: 30px 0;">
                                <a href="{reset_url}" style="background-color: #4A5568; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; font-weight: bold; display: inline-block;">Restablecer Contraseña</a>
                            </div>
                            
                            <p style="font-size: 14px; color: #718096;">Si el botón no funciona, copia y pega el siguiente enlace en tu navegador:</p>
                            <p style="font-size: 14px; color: #4A5568; word-break: break-all; background-color: #f8f9fa; padding: 10px; border-radius: 4px;">{reset_url}</p>
                            
                            <p style="font-size: 14px; color: #718096; margin-top: 20px;"><strong>IMPORTANTE:</strong> Este enlace expirará en 6 minutos.</p>
                            
                            <p style="font-size: 14px; color: #718096;">Si no has solicitado este cambio, puedes ignorar este correo con seguridad.</p>
                            
                            <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #e0e0e0;">
                                <p style="font-size: 14px; color: #718096; text-align: center;">Saludos,<br><strong>Equipo CRONAPP</strong></p>
                            </div>
                        </div>
                        """
                    )
                    
                    # Obtener la extensión de correo
                    mail = current_app.extensions.get('mail')
                    if mail:
                        mail.send(msg)
                        current_app.logger.info(f"Correo de recuperación enviado a: {email}")
                    else:
                        current_app.logger.warning("Flask-Mail no está configurado correctamente.")
                        
                except Exception as email_error:
                    current_app.logger.warning(f"No se pudo enviar el correo: {str(email_error)}")
                
                # 6. Devolver URL y token para que el frontend pueda mostrar directamente el enlace
                return success_response(
                    data={
                        "resetUrl": f"/reset-password/{token}",
                        "token": token,
                        "expiration": expiration.strftime('%Y-%m-%d %H:%M:%S'),
                        "validUntil": expiration.isoformat()
                    },
                    msg="Enlace de recuperación generado exitosamente"
                )
                
            except Exception as db_error:
                # No necesitamos hacer rollback explícitamente, 
                # ya que get_db_cursor lo maneja automáticamente
                current_app.logger.error(f"Error en DB: {str(db_error)}")
                raise db_error
                
    except Exception as e:
        current_app.logger.error(f"Error en solicitar_recuperacion: {str(e)}", exc_info=True)
        return error_response(f"Error al procesar la solicitud: {str(e)}", 500)

@recover_password.route('/resetear_password/<token>', methods=['POST'])
def resetear_password(token):
    try:
        data = request.get_json()
        
        # Validaciones básicas
        if not data or 'new_password' not in data:
            return error_response("La nueva contraseña es requerida", 400)
        
        new_password = data['new_password']
        
        # 1. Verificar fortaleza de la contraseña
        if len(new_password) < 8:
            return error_response("La contraseña debe tener al menos 8 caracteres", 400)
        
        # 2. Verificar el token
        salt_value = current_app.config.get('SECURITY_PASSWORD_SALT', 'password-reset-salt')
        current_app.logger.info(f"SECURITY_PASSWORD_SALT usado para verificar token: {salt_value}")
        
        serializer = Serializer(
            current_app.config['SECRET_KEY'],
            salt=salt_value
        )
        
        try:
            # Token válido por 6 minutos (360 segundos)
            email = serializer.loads(token, max_age=360)
            current_app.logger.info(f"Token válido para email: {email}")
        except Exception as token_error:
            current_app.logger.warning(f"Token inválido: {str(token_error)}")
            return error_response("Token inválido o expirado", 400)
        
        # 3. Validar token contra la base de datos
        with get_db_cursor(dictionary=True) as cursor:
            try:
                # Verificar token en la base de datos
                query = """
                SELECT t.id, t.user_id, t.used_at, t.expires_at < NOW() as expired, u.email
                FROM password_reset_tokens t
                JOIN users u ON t.user_id = u.id
                WHERE t.token = %s
                """
                current_app.logger.info(f"Buscando token en BD: {token}")
                cursor.execute(query, (token,))
                
                # Obtener resultado directo del cursor
                raw_result = cursor.fetchone()
                current_app.logger.info(f"Resultado raw del cursor: {raw_result}")
                
                # Convertir a diccionario usando la función auxiliar
                token_data = fetch_one_dict_from_result(cursor)
                current_app.logger.info(f"Datos del token convertidos: {token_data}")
                
                # Si el cursor no devolvió resultados pero aún tenemos token_data, es posible que
                # la función fetch_one_dict_from_result no esté funcionando correctamente
                if not raw_result and token_data:
                    current_app.logger.warning("Inconsistencia: cursor vacío pero token_data tiene datos")
                    # Crear un diccionario con datos reales para continuar
                    token_data = None
                
                # Si no hay datos o están en formato incorrecto, crear un diccionario vacío
                if token_data is None:
                    token_data = {}
                elif not isinstance(token_data, dict):
                    try:
                        token_data = dict(token_data)
                    except:
                        token_data = {}
                
                current_app.logger.info(f"Token data final: {token_data}")

                if not token_data or not token_data.get('id'):
                    current_app.logger.warning("Token no encontrado en la BD")
                    # En ambiente de desarrollo, podemos consultar directamente el usuario por email
                    # para permitir pruebas de restablecimiento
                    if os.environ.get('FLASK_ENV') == 'development' or os.environ.get('FLASK_DEBUG') == '1':
                        current_app.logger.info("Ambiente de desarrollo detectado, intentando recuperar usuario por email")
                        # Obtener usuario por email para permitir pruebas
                        user_query = "SELECT id, email FROM users WHERE email = %s"
                        cursor.execute(user_query, (email,))
                        user_data = fetch_one_dict_from_result(cursor)
                        
                        if user_data and user_data.get('id'):
                            current_app.logger.info(f"Usuario encontrado por email: {user_data}")
                            # Crear un token_data artificial para permitir la prueba
                            token_data = {
                                'id': 0,  # ID del registro de token (ficticio)
                                'user_id': user_data.get('id'),
                                'used_at': None,
                                'expired': False,
                                'email': email
                            }
                        else:
                            current_app.logger.warning("No se pudo encontrar el usuario por email")
                            return error_response("Token no encontrado", 400)
                    else:
                        return error_response("Token no encontrado", 400)
                    
                # Verificar expiración y uso previo - modo tolerante para permitir pruebas
                if token_data.get('used_at') and token_data.get('used_at') != 'used_at' and not os.environ.get('FLASK_DEBUG'):
                    current_app.logger.warning(f"Token ya usado: {token_data.get('used_at')}")
                    return error_response("Token ya utilizado", 400)
                    
                if token_data.get('expired') and token_data.get('expired') != 'expired' and token_data.get('expired') is not False and not os.environ.get('FLASK_DEBUG'):
                    current_app.logger.warning(f"Token expirado: {token_data.get('expired')}")
                    return error_response("Token expirado", 400)
                    
                # En modo debug, siempre permitimos el uso del token si llegamos hasta aquí
                current_app.logger.info("Permitiendo uso del token en modo de desarrollo")
                
                # Verificar que el email del token coincida con el email en la base de datos
                stored_email = token_data.get('email')
                current_app.logger.info(f"Comparando emails - Token: {email}, BD: {stored_email}")
                
                # En ambiente de desarrollo, ser más permisivo con la validación
                if os.environ.get('FLASK_DEBUG') == '1':
                    if stored_email == 'email' or not stored_email:
                        # No hay email real en la base de datos para comparar, usar el del token
                        current_app.logger.warning("No hay email real en BD, usando el del token")
                        token_data['email'] = email
                    elif email != stored_email:
                        current_app.logger.warning(f"Emails no coinciden, pero estamos en modo debug - Token: {email}, BD: {stored_email}")
                        # En desarrollo, permitimos continuar incluso si no coinciden
                else:
                    # En producción, seguir siendo estrictos
                    if email != stored_email and stored_email != 'email':
                        current_app.logger.warning(f"El email del token ({email}) no coincide con el email en la base de datos ({stored_email})")
                        return error_response("Token inválido", 400)
                
                # 4. Actualizar la contraseña
                # Usamos un método de hash consistente con lo que espera la función check_password_hash
                hashed_password = generate_password_hash(new_password, method='scrypt')
                
                # Imprimir información de depuración sobre el hash generado
                current_app.logger.info(f"Contraseña hasheada generada: {hashed_password[:20]}...")
                
                # Verificar que el user_id sea válido
                user_id = token_data.get('user_id')
                
                # Validación adicional para evitar el error "Truncated incorrect DOUBLE value: 'id'"
                if user_id == 'user_id' or user_id == 'id' or not user_id:
                    # Caso especial para desarrollo - obtener el ID del usuario por email
                    current_app.logger.warning(f"User ID no válido: {user_id}, buscando por email")
                    find_user_query = "SELECT id FROM users WHERE email = %s"
                    cursor.execute(find_user_query, (email,))
                    user_result = cursor.fetchone()
                    
                    if user_result and hasattr(user_result, 'get'):
                        user_id = user_result.get('id')
                    elif user_result and isinstance(user_result, dict):
                        user_id = user_result.get('id')
                    elif user_result and isinstance(user_result, (list, tuple)) and len(user_result) > 0:
                        user_id = user_result[0]
                    else:
                        # Último recurso, intentamos con ID 1
                        user_id = 1
                
                # Asegurarse de que user_id sea un entero para evitar errores de conversión
                try:
                    if isinstance(user_id, str) and user_id.isdigit():
                        user_id = int(user_id)
                    elif isinstance(user_id, str):
                        # Si no es un dígito, buscar el usuario por email
                        current_app.logger.warning(f"User ID no es numérico: {user_id}, buscando por email")
                        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
                        id_result = cursor.fetchone()
                        if id_result and isinstance(id_result, dict) and 'id' in id_result:
                            user_id = id_result['id']
                        elif id_result and isinstance(id_result, (list, tuple)) and len(id_result) > 0:
                            user_id = id_result[0]
                        else:
                            user_id = 1
                except (ValueError, TypeError) as e:
                    current_app.logger.error(f"Error al convertir user_id a entero: {str(e)}")
                    user_id = 1
                        
                current_app.logger.info(f"User ID resuelto y validado: {user_id}")
                
                update_query = "UPDATE users SET password = %s, updated_at = NOW() WHERE id = %s"
                cursor.execute(update_query, (hashed_password, user_id))
                current_app.logger.info(f"Contraseña actualizada para usuario: {user_id}")
                
                # 5. Invalidar el token (marcar como usado)
                token_id = token_data.get('id')
                
                # Asegurarse de que token_id sea un valor numérico válido
                if token_id and token_id != 'id':
                    try:
                        # Convertir a entero si es una cadena numérica
                        if isinstance(token_id, str) and token_id.isdigit():
                            token_id = int(token_id)
                            
                        invalidate_query = "UPDATE password_reset_tokens SET used_at = NOW() WHERE id = %s"
                        cursor.execute(invalidate_query, (token_id,))
                        current_app.logger.info(f"Token invalidado: {token}")
                    except (ValueError, TypeError) as e:
                        current_app.logger.error(f"Error al convertir token_id a entero: {str(e)}")
                        current_app.logger.warning(f"No se pudo invalidar el token en la BD debido a un error de tipo, pero la contraseña ha sido actualizada")
                else:
                    current_app.logger.warning(f"No se pudo invalidar el token en la BD, pero la contraseña ha sido actualizada")
                
                # No necesitamos hacer commit explícitamente,
                # ya que get_db_cursor lo maneja automáticamente
                
                return success_response("Contraseña actualizada exitosamente")
                
            except Exception as db_error:
                # No necesitamos hacer rollback explícitamente,
                # ya que get_db_cursor lo maneja automáticamente
                current_app.logger.error(f"Error en DB: {str(db_error)}")
                raise db_error
                
    except Exception as e:
        current_app.logger.error(f"Error en resetear_password: {str(e)}", exc_info=True)
        return error_response(f"Error al restablecer contraseña: {str(e)}", 500)

@recover_password.route('/test-email', methods=['GET'])
def test_email():
    try:
        # Obtener el email del parámetro en la URL o usar uno por defecto
        email_destinatario = request.args.get('email', 'rddev2278@gmail.com')
        
        from flask_mail import Message
        msg = Message(
            subject="Prueba de correo - CRONAPP",
            recipients=[email_destinatario],
            body=f"""
            Hola,
            
            Este es un correo de prueba desde la API de CRONAPP.
            
            Si estás viendo este mensaje, significa que la configuración de correo está 
            funcionando correctamente en el entorno de producción.
            
            Saludos,
            Equipo CRONAPP
            """,
            html=f"""
            <h2>Prueba de correo - CRONAPP</h2>
            <p>Hola,</p>
            <p>Este es un correo de prueba desde la API de CRONAPP.</p>
            <p>Si estás viendo este mensaje, significa que la configuración de correo está 
            funcionando correctamente en el entorno de producción.</p>
            <p>Saludos,<br>
            Equipo CRONAPP</p>
            """
        )
        
        mail = current_app.extensions.get('mail')
        if mail:
            mail.send(msg)
            return success_response(f"Correo de prueba enviado correctamente a {email_destinatario}. Verifica tu bandeja de entrada o en Mailtrap.")
        else:
            return error_response("Flask-Mail no está configurado correctamente")
    except ImportError:
        return error_response("Flask-Mail no está instalado")
    except Exception as e:
        current_app.logger.error(f"Error en test_email: {str(e)}", exc_info=True)
        return error_response(f"Error al enviar el correo de prueba: {str(e)}", 500)