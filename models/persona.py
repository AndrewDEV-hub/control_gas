from ..app import db

class Persona(db.Model):
    __tablename__ = 'personas'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    ci = db.Column(db.Text, unique=True, nullable=False)
    nombre = db.Column(db.Text, nullable=False)