from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from datetime import timedelta
import os
import logging
from config import EXPIRE_TOKEN_TIME
from routes.auth import auth
from routes.usuario import usuarios
from routes.recover_password import recover_password
from routes.register import register
from routes.settings import settings
# Configurar logginga
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)
app.debug = True
os.environ['FLASK_DEBUG'] = '1'
# Configuración más específica de CORS para permitir solicitudes desde cualquier origen
cors_config = {
    "origins": ["*"],
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"]
}
CORS(app, resources={r"/*": cors_config})

# Configuración de claves secretas
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'tu-clave-secreta-para-tokens')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'tu-clave-secreta')
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get('SECURITY_PASSWORD_SALT', 'password-reset-salt')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=EXPIRE_TOKEN_TIME["ACCESS_TOKEN_MINUTES"])
jwt = JWTManager(app)

# Configuración de Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')

mail = Mail(app)

# Configurar directorio de archivos estáticos
client_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dist', 'public')
client_public_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'client', 'public')

# Verificar si existen los directorios y establecer el directorio estático
if os.path.exists(client_public_dir):
    app.logger.info(f"Usando directorio client/public como fuente de archivos estáticos: {client_public_dir}")
    app.static_folder = client_public_dir
else:
    if not os.path.exists(client_dir):
        app.logger.warning(f"El directorio dist/public no existe: {client_dir}")
        os.makedirs(client_dir, exist_ok=True)
        app.logger.info(f"Se creó el directorio dist/public: {client_dir}")
    
    app.logger.info(f"Usando directorio dist/public como fuente de archivos estáticos: {client_dir}")
    app.static_folder = client_dir

# Exponer las rutas a nivel global
app.config['CLIENT_PUBLIC_DIR'] = client_public_dir
app.config['CLIENT_DIR'] = client_dir

# Registrar blueprints
app.register_blueprint(auth, url_prefix='/api/auth')
app.register_blueprint(usuarios, url_prefix='/api/usuarios')
app.register_blueprint(recover_password, url_prefix='/api/recover')
app.register_blueprint(register, url_prefix='/api/register')
app.register_blueprint(settings, url_prefix='/api')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    # Definir directorios para acceso local en esta función
    public_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'client', 'public')
    dist_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dist', 'public')
    
    if path.startswith('api/'):
        return {"message": "API endpoint not found"}, 404
    
    # Manejo especial para las rutas de reseteo de contraseña
    if path.startswith('reset-password/'):
        # Servir nuestra página HTML independiente para reseteo de contraseña
        try:
            app.logger.info(f"Sirviendo página de reseteo de contraseña para token: {path.split('/')[-1]}")
            
            # Directorio público del cliente
            if os.path.exists(os.path.join(public_dir, 'reset-password.html')):
                return send_from_directory(public_dir, 'reset-password.html')
            
            # Directorio del cliente compilado
            if os.path.exists(os.path.join(dist_dir, 'reset-password.html')):
                return send_from_directory(dist_dir, 'reset-password.html')
                
            # Si no encuentra la página específica, usar el index.html
            if os.path.exists(os.path.join(public_dir, 'index.html')):
                return send_from_directory(public_dir, 'index.html')
            
            return send_from_directory(dist_dir, 'index.html')
        except Exception as e:
            app.logger.error(f"Error al servir página de reseteo: {str(e)}")
            return {"message": "Error serving reset password page"}, 500
    
    try:
        # Primero buscar en el directorio client/public
        if path and os.path.exists(os.path.join(public_dir, path)):
            app.logger.debug(f"Sirviendo archivo estático desde client/public: {path}")
            return send_from_directory(public_dir, path)
        
        # Luego buscar en el directorio dist/public
        if path and os.path.exists(os.path.join(dist_dir, path)):
            app.logger.debug(f"Sirviendo archivo estático desde dist/public: {path}")
            return send_from_directory(dist_dir, path)
        
        # Si no se encuentra el archivo pero existe index.html en client/public, servirlo
        if os.path.exists(os.path.join(public_dir, 'index.html')):
            app.logger.debug(f"Sirviendo index.html desde client/public como fallback")
            return send_from_directory(public_dir, 'index.html')
        
        # Como último recurso, servir index.html desde dist/public
        app.logger.debug(f"Sirviendo index.html desde dist/public como fallback")
        return send_from_directory(dist_dir, 'index.html')
    except Exception as e:
        app.logger.error(f"Error sirviendo archivo: {str(e)}")
        return {"message": "File not found"}, 404

@app.route('/api/test', methods=['GET'])
def test_api():
    return jsonify({
        "status": "success",
        "message": "API Flask funcionando correctamente"
    })

if __name__ == '__main__':
    print(f"Iniciando servidor Flask en http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)