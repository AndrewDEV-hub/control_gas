from ..app import db

class PersonaVehiculo(db.Model):
    __tablename__ = 'personas_vehiculos'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    persona_id = db.Column(db.BigInteger, db.ForeignKey('personas.id'))
    vehiculo_id = db.Column(db.BigInteger, db.ForeignKey('vehiculos.id'))
    __table_args__ = (db.UniqueConstraint('persona_id', 'vehiculo_id'),)