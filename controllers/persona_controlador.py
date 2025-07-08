from flask import Blueprint, request, jsonify
from models import db, Persona
from datetime import datetime
from models import db, Persona, PersonaVehiculo, CargaCombustible

persona_bp = Blueprint('persona', __name__)

def litros_cargados_en_mes(persona_id):
    hoy = datetime.now()
    primer_dia = hoy.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    # Busca todos los vehículos asociados a la persona
    vehiculos_ids = [pv.vehiculo_id for pv in PersonaVehiculo.query.filter_by(persona_id=persona_id).all()]
    if not vehiculos_ids:
        return 0
    # Suma todas las cargas de esos vehículos en el mes
    total = db.session.query(db.func.sum(CargaCombustible.cantidad)).filter(
        CargaCombustible.vehiculo_id.in_(vehiculos_ids),
        CargaCombustible.fecha >= primer_dia
    ).scalar()
    return total or 0

@persona_bp.route('/personas', methods=['POST'])
def crear_persona():
    data = request.get_json()
    ci = data['ci']
    persona = Persona.query.filter_by(ci=ci).first()
    if persona:
        # Ya existe, retorna su id o úsala para asociar el vehículo
        return jsonify({'id': persona.id, 'mensaje': 'Persona ya existe'}), 200
    # Si no existe, créala normalmente
    persona = Persona(
        nombre=data['nombre'],
        ci=ci,
        # ...otros campos...
    )
    db.session.add(persona)
    db.session.commit()
    return jsonify({'id': persona.id}), 201

@persona_bp.route('/personas', methods=['GET'])
def listar_personas():
    personas = Persona.query.all()
    resultado = []
    for persona in personas:
        total_cargado = litros_cargados_en_mes(persona.id)
        restante = max(0, 119 - total_cargado)
        resultado.append({
            'id': persona.id,
            'nombre': persona.nombre,
            'ci': persona.ci,
            # ...otros campos...
            'total_cargado_mes': total_cargado,
            'restante_mes': restante
        })
    return jsonify(resultado)

# Obtener una persona por ID
@persona_bp.route('/personas/<int:id>', methods=['GET'])
def obtener_persona(id):
    persona = Persona.query.get_or_404(id)
    return jsonify({'id': persona.id, 'ci': persona.ci, 'nombre': persona.nombre})

# Actualizar una persona
@persona_bp.route('/personas/<int:id>', methods=['PUT'])
def actualizar_persona(id):
    persona = Persona.query.get_or_404(id)
    data = request.get_json()
    if 'ci' in data:
        persona.ci = data['ci']
    if 'nombre' in data:
        persona.nombre = data['nombre']
    db.session.commit()
    return jsonify({'id': persona.id, 'ci': persona.ci, 'nombre': persona.nombre})

# Eliminar una persona
@persona_bp.route('/personas/<int:id>', methods=['DELETE'])
def eliminar_persona(id):
    persona = Persona.query.get_or_404(id)
    db.session.delete(persona)
    db.session.commit()
    return jsonify({'message': 'Persona eliminada'})