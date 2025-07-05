from flask import Blueprint, request, jsonify
from models import db, Vehiculo

vehiculo_bp = Blueprint('vehiculo', __name__)

@vehiculo_bp.route('/vehiculos', methods=['POST'])
def crear_vehiculo():
    data = request.get_json()
    vehiculo = Vehiculo(numero_crasis=data['numero_crasis'], placa=data['placa'], tipo=data['tipo'])
    db.session.add(vehiculo)
    db.session.commit()
    return jsonify({'id': vehiculo.id, 'placa': vehiculo.placa, 'tipo': vehiculo.tipo}), 201

@vehiculo_bp.route('/vehiculos', methods=['GET'])
def listar_vehiculos():
    vehiculos = Vehiculo.query.all()
    return jsonify([{'id': v.id, 'numero_crasis': v.numero_crasis, 'placa': v.placa, 'tipo': v.tipo} for v in vehiculos])