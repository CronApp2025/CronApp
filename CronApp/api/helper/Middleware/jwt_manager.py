
from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from ..token_manager import token_manager

def jwt_required_custom(optional=False, refresh=False):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                verify_jwt_in_request(optional=optional, refresh=refresh)
                jwt = get_jwt()
                
                if not jwt:
                    return jsonify({"msg": "Token no proporcionado"}), 401
                    
                if token_manager.is_blacklisted(jwt.get('jti', '')):
                    return jsonify({"msg": "Token ha sido revocado"}), 401
                    
                return fn(*args, **kwargs)
            except Exception as e:
                print(f"Error en validación de token: {str(e)}")
                if optional:
                    return fn(*args, **kwargs)
                return jsonify({"msg": "Token inválido", "error": str(e)}), 401
        return decorator
    return wrapper
