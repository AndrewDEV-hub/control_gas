from ..app import db

class FuncionarioPublico(db.Model):
    __tablename__ = 'funcionarios_publicos'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    persona_id = db.Column(db.BigInteger, db.ForeignKey('personas.id'))
    numero_credencial = db.Column(db.Text, nullable=False)