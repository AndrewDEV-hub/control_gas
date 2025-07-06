from models import db, Estacion
from app import app

with app.app_context():
    estaciones = [
        {"nombre": "Chaparral", "ubicacion": "Av. 18 de Noviembre"},
        {"nombre": "Oasis", "ubicacion": "Av. Simon Bolivar"},
        {"nombre": "Iriarte", "ubicacion": "Av. Panamericana"},
        {"nombre": "Paitití", "ubicacion": "Av. Panamericana"},
        {"nombre": "Pompeya", "ubicacion": "Av. Pedro Ignacio Muiba"},
    ]
    for est in estaciones:
        if not Estacion.query.filter_by(nombre=est["nombre"]).first():
            db.session.add(Estacion(nombre=est["nombre"], ubicacion=est["ubicacion"]))
    db.session.commit()
    print("Estaciones creadas")