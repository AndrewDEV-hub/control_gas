from ..app import db
from sqlalchemy.sql import func

class CargaCombustible(db.Model):
    __tablename__ = 'cargas_combustible'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    vehiculo_id = db.Column(db.BigInteger, db.ForeignKey('vehiculos.id'))
    estacion_id = db.Column(db.BigInteger, db.ForeignKey('estaciones.id'))
    fecha = db.Column(db.DateTime(timezone=True), server_default=func.now())
    cantidad = db.Column(db.Numeric, nullable=False)