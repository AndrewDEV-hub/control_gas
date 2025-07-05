from flask import Blueprint, request, jsonify
from models import db, Estacion

estacion_bp = Blueprint('estacion', __name__)

@estacion_bp.route('/estaciones', methods=['POST'])
def crear_estacion():
    data = request.get_json()
    estacion = Estacion(nombre=data['nombre'], ubicacion=data['ubicacion'])
    db.session.add(estacion)
    db.session.commit()
    return jsonify({'id': estacion.id, 'nombre': estacion.nombre, 'ubicacion': estacion.ubicacion}), 201

@estacion_bp.route('/estaciones', methods=['GET'])
def listar_estaciones():
    estaciones = Estacion.query.all()
    return jsonify([{'id': e.id, 'nombre': e.nombre, 'ubicacion': e.ubicacion} for e in estaciones])
@estacion_bp.route('/estaciones/<int:id>', methods=['GET'])
def obtener_estacion(id):
    estacion = Estacion.query.get_or_404(id)
    return jsonify({'id': estacion.id, 'nombre': estacion.nombre, 'ubicacion': estacion.ubicacion})

@estacion_bp.route('/estaciones/<int:id>', methods=['PUT'])
def actualizar_estacion(id):
    estacion = Estacion.query.get_or_404(id)
    data = request.get_json()
    if 'nombre' in data:
        estacion.nombre = data['nombre']
    if 'ubicacion' in data:
        estacion.ubicacion = data['ubicacion']
    db.session.commit()
    return jsonify({'id': estacion.id, 'nombre': estacion.nombre, 'ubicacion': estacion.ubicacion})

@estacion_bp.route('/estaciones/<int:id>', methods=['DELETE'])
def eliminar_estacion(id):
    estacion = Estacion.query.get_or_404(id)
    db.session.delete(estacion)
    db.session.commit()
    return jsonify({'message': 'Estación eliminada'})