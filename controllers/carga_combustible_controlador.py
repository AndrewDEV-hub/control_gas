from flask import Blueprint, request, jsonify
from models import db, CargaCombustible
from models import PersonaVehiculo, CargaCombustible, db
from datetime import datetime


carga_combustible_bp = Blueprint('carga_combustible', __name__)

def litros_cargados_en_mes(persona_id):
    hoy = datetime.now()
    primer_dia = hoy.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    vehiculos_ids = [pv.vehiculo_id for pv in PersonaVehiculo.query.filter_by(persona_id=persona_id).all()]
    if not vehiculos_ids:
        return 0
    total = db.session.query(db.func.sum(CargaCombustible.cantidad)).filter(
        CargaCombustible.vehiculo_id.in_(vehiculos_ids),
        CargaCombustible.fecha >= primer_dia
    ).scalar()
    return total or 0


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

@carga_combustible_bp.route('/cargas_combustible', methods=['POST'])
def registrar_carga():
    data = request.get_json()
    vehiculo_id = data['vehiculo_id']
    cantidad = int(data['cantidad'])
    persona_vehiculo = PersonaVehiculo.query.filter_by(vehiculo_id=vehiculo_id).first()
    if not persona_vehiculo:
        return jsonify({"error": "No se encontró la persona asociada"}), 400
    persona_id = persona_vehiculo.persona_id
    total_cargado = litros_cargados_en_mes(persona_id)
    if total_cargado + cantidad > 119:
        return jsonify({"error": f"El límite mensual de 119L para esta persona ya fue alcanzado. Restante: {max(0, 119 - total_cargado)}L"}), 400
    carga = CargaCombustible(
        vehiculo_id=vehiculo_id,
        estacion_id=data['estacion_id'],
        cantidad=cantidad
    )
    db.session.add(carga)
    db.session.commit()
    return jsonify({'id': carga.id}), 201