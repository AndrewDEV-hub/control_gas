from flask import Blueprint, request, jsonify
from models import db, Usuario

usuario_bp = Blueprint('usuario', __name__)

@usuario_bp.route('/usuarios', methods=['POST'])
def crear_usuario():
    data = request.get_json()
    usuario = Usuario(nombre=data['nombre'], rol=data['rol'])
    db.session.add(usuario)
    db.session.commit()
    return jsonify({'id': usuario.id, 'nombre': usuario.nombre, 'rol': usuario.rol}), 201

@usuario_bp.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([{'id': u.id, 'nombre': u.nombre, 'rol': u.rol} for u in usuarios])