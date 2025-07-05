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