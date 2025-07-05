from flask import Blueprint, request, jsonify
from models import db, Estacion

estacion_bp = Blueprint('estacion', __name__)

@estacion_bp.route('/estaciones', methods=['POST'])
def crear_estacion():
    data = request.get_json()
    estacion = Estacion(nombre=data['nombre'], ubicacion=data['ubicacion'])
    db.session.add(estacion)
    db.session.commit()
    return jsonify({'id': estacion.id, 'nombre': estacion.nombre, 'ubicacion': estacion.ubicacion}), 201

@estacion_bp.route('/estaciones', methods=['GET'])
def listar_estaciones():
    estaciones = Estacion.query.all()
    return jsonify([{'id': e.id, 'nombre': e.nombre, 'ubicacion': e.ubicacion} for e in estaciones])