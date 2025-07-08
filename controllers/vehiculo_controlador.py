from flask import Blueprint, request, jsonify
from models import db, Vehiculo

vehiculo_bp = Blueprint('vehiculo', __name__)

@vehiculo_bp.route('/vehiculos', methods=['POST'])
def crear_vehiculo():
    data = request.get_json()
    vehiculo = Vehiculo(
        numero_crasis=data['numero_crasis'],
        placa=data['placa'],
        tipo=data['tipo'],
        foto=data.get('foto')  # <-- Debe estar así
    )
    db.session.add(vehiculo)
    db.session.commit()
    return jsonify({
        'id': vehiculo.id,
        'placa': vehiculo.placa,
        'tipo': vehiculo.tipo,
        'foto': vehiculo.foto,
        'verificado': vehiculo.verificado 
    }), 201

@vehiculo_bp.route('/vehiculos', methods=['GET'])
def listar_vehiculos():
    vehiculos = Vehiculo.query.all()
    return jsonify([
        {
            'id': v.id,
            'numero_crasis': v.numero_crasis,
            'placa': v.placa,
            'tipo': v.tipo,
            'foto': v.foto,
            'verificado': v.verificado
        } for v in vehiculos
    ])

@vehiculo_bp.route('/vehiculos/<int:id>', methods=['GET'])
def obtener_vehiculo(id):
    vehiculo = Vehiculo.query.get_or_404(id)
    return jsonify({
        'id': vehiculo.id,
        'numero_crasis': vehiculo.numero_crasis,
        'placa': vehiculo.placa,
        'tipo': vehiculo.tipo,
        'foto': vehiculo.foto
    })

@vehiculo_bp.route('/vehiculos/<int:id>', methods=['PUT'])
def actualizar_vehiculo(id):
    vehiculo = Vehiculo.query.get_or_404(id)
    data = request.get_json()
    if 'numero_crasis' in data:
        vehiculo.numero_crasis = data['numero_crasis']
    if 'placa' in data:
        vehiculo.placa = data['placa']
    if 'tipo' in data:
        vehiculo.tipo = data['tipo']
    if 'foto' in data:
        vehiculo.foto = data['foto']  # <-- NUEVO
    db.session.commit()
    return jsonify({
        'id': vehiculo.id,
        'numero_crasis': vehiculo.numero_crasis,
        'placa': vehiculo.placa,
        'tipo': vehiculo.tipo,
        'foto': vehiculo.foto
    })

@vehiculo_bp.route('/vehiculos/<int:id>', methods=['DELETE'])
def eliminar_vehiculo(id):
    vehiculo = Vehiculo.query.get_or_404(id)
    db.session.delete(vehiculo)
    db.session.commit()
    return jsonify({'message': 'Vehículo eliminado'})

@vehiculo_bp.route('/vehiculos/<int:id>/verificar', methods=['PUT'])
def verificar_vehiculo(id):
    vehiculo = Vehiculo.query.get_or_404(id)
    vehiculo.verificado = True
    db.session.commit()
    return jsonify({'message': 'Vehículo verificado'})