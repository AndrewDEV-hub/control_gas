from . import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    nombre = db.Column(db.Text, nullable=False)
    rol = db.Column(db.Text, nullable=False)