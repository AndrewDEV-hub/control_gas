from flask import Blueprint, request, jsonify
from models import db, CargaCombustible

carga_combustible_bp = Blueprint('carga_combustible', __name__)

@carga_combustible_bp.route('/cargas_combustible', methods=['POST'])
def crear_carga_combustible():
    data = request.get_json()
    carga = CargaCombustible(
        vehiculo_id=data['vehiculo_id'],
        estacion_id=data['estacion_id'],
        cantidad=data['cantidad']
    )
    db.session.add(carga)
    db.session.commit()
    return jsonify({'id': carga.id}), 201

@carga_combustible_bp.route('/cargas_combustible', methods=['GET'])
def listar_cargas_combustible():
    cargas = CargaCombustible.query.all()
    return jsonify([
        {
            'id': c.id,
            'vehiculo_id': c.vehiculo_id,
            'estacion_id': c.estacion_id,
            'fecha': c.fecha.isoformat() if c.fecha else None,
            'cantidad': float(c.cantidad)
        } for c in cargas
    ])

@carga_combustible_bp.route('/cargas_combustible/<int:id>', methods=['GET'])
def obtener_carga_combustible(id):
    carga = CargaCombustible.query.get_or_404(id)
    return jsonify({
        'id': carga.id,
        'vehiculo_id': carga.vehiculo_id,
        'estacion_id': carga.estacion_id,
        'fecha': carga.fecha.isoformat() if carga.fecha else None,
        'cantidad': float(carga.cantidad)
    })

@carga_combustible_bp.route('/cargas_combustible/<int:id>', methods=['PUT'])
def actualizar_carga_combustible(id):
    carga = CargaCombustible.query.get_or_404(id)
    data = request.get_json()
    if 'vehiculo_id' in data:
        carga.vehiculo_id = data['vehiculo_id']
    if 'estacion_id' in data:
        carga.estacion_id = data['estacion_id']
    if 'cantidad' in data:
        carga.cantidad = data['cantidad']
    db.session.commit()
    return jsonify({
        'id': carga.id,
        'vehiculo_id': carga.vehiculo_id,
        'estacion_id': carga.estacion_id,
        'fecha': carga.fecha.isoformat() if carga.fecha else None,
        'cantidad': float(carga.cantidad)
    })

@carga_combustible_bp.route('/cargas_combustible/<int:id>', methods=['DELETE'])
def eliminar_carga_combustible(id):
    carga = CargaCombustible.query.get_or_404(id)
    db.session.delete(carga)
    db.session.commit()
    return jsonify({'message': 'Carga de combustible eliminada'})