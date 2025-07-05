from flask import Blueprint, request, jsonify
from models import db, Persona

persona_bp = Blueprint('persona', __name__)

@persona_bp.route('/personas', methods=['POST'])
def crear_persona():
    data = request.get_json()
    persona = Persona(ci=data['ci'], nombre=data['nombre'])
    db.session.add(persona)
    db.session.commit()
    return jsonify({'id': persona.id, 'ci': persona.ci, 'nombre': persona.nombre}), 201

@persona_bp.route('/personas', methods=['GET'])
def listar_personas():
    personas = Persona.query.all()
    return jsonify([{'id': p.id, 'ci': p.ci, 'nombre': p.nombre} for p in personas])

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