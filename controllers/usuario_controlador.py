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
@usuario_bp.route('/usuarios/<int:id>', methods=['GET'])
def obtener_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    return jsonify({'id': usuario.id, 'nombre': usuario.nombre, 'rol': usuario.rol})

@usuario_bp.route('/usuarios/<int:id>', methods=['PUT'])
def actualizar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    data = request.get_json()
    if 'nombre' in data:
        usuario.nombre = data['nombre']
    if 'rol' in data:
        usuario.rol = data['rol']
    db.session.commit()
    return jsonify({'id': usuario.id, 'nombre': usuario.nombre, 'rol': usuario.rol})

@usuario_bp.route('/usuarios/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({'message': 'Usuario eliminado'})