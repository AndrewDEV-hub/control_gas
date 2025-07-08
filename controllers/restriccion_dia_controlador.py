from flask import Blueprint, jsonify, request, session

restriccion_bp = Blueprint('restriccion', __name__)

# Variable global temporal (en producción usar BD)
restriccion_dia_activa = False

@restriccion_bp.route('/restriccion-dia', methods=['GET'])
def get_restriccion_dia():
    return jsonify({"activa": restriccion_dia_activa})

@restriccion_bp.route('/restriccion-dia', methods=['POST'])
def set_restriccion_dia():
    if session.get('usuario_rol') != 'supervisor':
        return jsonify({"error": "No autorizado"}), 403
    global restriccion_dia_activa
    restriccion_dia_activa = bool(request.json.get("activa"))
    return jsonify({"activa": restriccion_dia_activa})