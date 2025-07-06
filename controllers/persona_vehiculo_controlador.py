from flask import Blueprint, request, jsonify
from models import db, PersonaVehiculo, Persona, Vehiculo

persona_vehiculo_bp = Blueprint('persona_vehiculo', __name__)

@persona_vehiculo_bp.route('/personas_vehiculos', methods=['POST'])
def asociar_persona_vehiculo():
    data = request.get_json()
    persona_id = data.get('persona_id')
    vehiculo_id = data.get('vehiculo_id')

    # Validar existencia
    persona = Persona.query.get(persona_id)
    vehiculo = Vehiculo.query.get(vehiculo_id)
    if not persona or not vehiculo:
        return jsonify({'error': 'Persona o vehículo no existe'}), 400

    # Validar máximo 2 personas por vehículo
    personas_asociadas = PersonaVehiculo.query.filter_by(vehiculo_id=vehiculo_id).count()
    if personas_asociadas >= 2:
        return jsonify({'error': 'Este vehículo ya tiene 2 personas asociadas'}), 400

    # Validar máximo 2 vehículos por persona
    vehiculos_asociados = PersonaVehiculo.query.filter_by(persona_id=persona_id).count()
    if vehiculos_asociados >= 2:
        return jsonify({'error': 'Esta persona ya está asociada a 2 vehículos'}), 400

    # Validar que no exista ya la relación
    existe = PersonaVehiculo.query.filter_by(persona_id=persona_id, vehiculo_id=vehiculo_id).first()
    if existe:
        return jsonify({'error': 'Ya existe esta relación'}), 400

    relacion = PersonaVehiculo(persona_id=persona_id, vehiculo_id=vehiculo_id)
    db.session.add(relacion)
    db.session.commit()
    return jsonify({'message': 'Relación creada'}), 201

@persona_vehiculo_bp.route('/personas_vehiculos', methods=['GET'])
def listar_personas_vehiculos():
    relaciones = PersonaVehiculo.query.all()
    return jsonify([
        {
            'id': r.id,
            'persona_id': r.persona_id,
            'vehiculo_id': r.vehiculo_id
        } for r in relaciones
    ])