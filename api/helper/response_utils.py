# helpers/response_utils.pya
from flask import jsonify
import json
from flask import Response

def build_response(success, msg=None, data=None, status_code=200):
    response = {
        'success': success,
        'msg': msg,
        'data': data if data is not None else []
    }
    json_str = json.dumps(response, ensure_ascii=False, default=str)
    return Response(json_str, mimetype='application/json'), status_code

def success_response(data=None, msg="Operación exitosa"):
    return build_response(True, msg, data, 200)

def error_response(msg="Error inesperado", status_code=400, data=[]):
    return build_response(False, msg.replace("1644 (45000): ","").replace("1062 (23000): ",""), data, status_code)