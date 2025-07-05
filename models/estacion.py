from ..app import db

class Estacion(db.Model):
    __tablename__ = 'estaciones'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    nombre = db.Column(db.Text, nullable=False)
    ubicacion = db.Column(db.Text, nullable=False)