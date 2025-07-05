from flask import Blueprint, request, jsonify
from models import db, FuncionarioPublico

funcionario_publico_bp = Blueprint('funcionario_publico', __name__)

@funcionario_publico_bp.route('/funcionarios_publicos', methods=['POST'])
def crear_funcionario_publico():
    data = request.get_json()
    funcionario = FuncionarioPublico(
        persona_id=data['persona_id'],
        numero_credencial=data['numero_credencial']
    )
    db.session.add(funcionario)
    db.session.commit()
    return jsonify({'id': funcionario.id}), 201

@funcionario_publico_bp.route('/funcionarios_publicos', methods=['GET'])
def listar_funcionarios_publicos():
    funcionarios = FuncionarioPublico.query.all()
    return jsonify([
        {
            'id': f.id,
            'persona_id': f.persona_id,
            'numero_credencial': f.numero_credencial
        } for f in funcionarios
    ])