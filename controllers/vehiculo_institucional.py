from flask import Blueprint, request, jsonify
from models import db, VehiculoInstitucional

vehiculo_institucional_bp = Blueprint('vehiculo_institucional', __name__)

@vehiculo_institucional_bp.route('/vehiculos_institucionales', methods=['POST'])
def crear_vehiculo_institucional():
    data = request.get_json()
    vi = VehiculoInstitucional(
        vehiculo_id=data['vehiculo_id'],
        nombre_institucion=data['nombre_institucion']
    )
    db.session.add(vi)
    db.session.commit()
    return jsonify({'id': vi.id}), 201

@vehiculo_institucional_bp.route('/vehiculos_institucionales', methods=['GET'])
def listar_vehiculos_institucionales():
    vis = VehiculoInstitucional.query.all()
    return jsonify([
        {
            'id': v.id,
            'vehiculo_id': v.vehiculo_id,
            'nombre_institucion': v.nombre_institucion
        } for v in vis
    ])