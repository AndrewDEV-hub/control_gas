from . import db

class VehiculoInstitucional(db.Model):
    __tablename__ = 'vehiculos_institucionales'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    vehiculo_id = db.Column(db.BigInteger, db.ForeignKey('vehiculos.id'))
    nombre_institucion = db.Column(db.Text, nullable=False)