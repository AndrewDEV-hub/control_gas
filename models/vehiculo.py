from . import db

class Vehiculo(db.Model):
    __tablename__ = 'vehiculos'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    numero_crasis = db.Column(db.Text, nullable=False)
    placa = db.Column(db.Text, unique=True, nullable=False)
    tipo = db.Column(db.Text, nullable=False)
    foto = db.Column(db.Text, nullable=True)
    verificado = db.Column(db.Boolean, default=False, nullable=False)
    qr_url = db.Column(db.Text, nullable=True)