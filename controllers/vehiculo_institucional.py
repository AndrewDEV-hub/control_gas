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

@vehiculo_institucional_bp.route('/vehiculos_institucionales/<int:id>', methods=['GET'])
def obtener_vehiculo_institucional(id):
    vi = VehiculoInstitucional.query.get_or_404(id)
    return jsonify({
        'id': vi.id,
        'vehiculo_id': vi.vehiculo_id,
        'nombre_institucion': vi.nombre_institucion
    })

@vehiculo_institucional_bp.route('/vehiculos_institucionales/<int:id>', methods=['PUT'])
def actualizar_vehiculo_institucional(id):
    vi = VehiculoInstitucional.query.get_or_404(id)
    data = request.get_json()
    if 'vehiculo_id' in data:
        vi.vehiculo_id = data['vehiculo_id']
    if 'nombre_institucion' in data:
        vi.nombre_institucion = data['nombre_institucion']
    db.session.commit()
    return jsonify({
        'id': vi.id,
        'vehiculo_id': vi.vehiculo_id,
        'nombre_institucion': vi.nombre_institucion
    })

@vehiculo_institucional_bp.route('/vehiculos_institucionales/<int:id>', methods=['DELETE'])
def eliminar_vehiculo_institucional(id):
    vi = VehiculoInstitucional.query.get_or_404(id)
    db.session.delete(vi)
    db.session.commit()
    return jsonify({'message': 'Vehículo institucional eliminado'})