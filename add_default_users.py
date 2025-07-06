from models import db, Usuario
from app import app

with app.app_context():
    if not Usuario.query.filter_by(nombre="registrador").first():
        db.session.add(Usuario(nombre="registrador", rol="registrador", password="12345"))
    if not Usuario.query.filter_by(nombre="supervisor").first():
        db.session.add(Usuario(nombre="supervisor", rol="supervisor", password="12345"))
    db.session.commit()
    print("Usuarios creados")