from flask import Blueprint, render_template, request, redirect, session
from models import PersonaVehiculo

cliente_bp = Blueprint('cliente', __name__)

@cliente_bp.route('/login_cliente', methods=['GET', 'POST'])
def login_cliente():
    error = None
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        password = request.form.get('password')
        print("Intento login:", usuario, password)  # <-- Agrega esto
        relacion = PersonaVehiculo.query.filter_by(usuario_cliente=usuario, password_cliente=password).first()
        print("Relacion encontrada:", relacion)  # <-- Y esto
        if relacion:
            session['cliente_rel_id'] = relacion.id
            return redirect('/mi_qr')
        else:
            error = "Usuario o contraseña incorrectos"
    return render_template('login_cliente.html', error=error)

@cliente_bp.route('/mi_qr')
def mi_qr():
    rel_id = session.get('cliente_rel_id')
    if not rel_id:
        return redirect('/login_cliente')
    relacion = PersonaVehiculo.query.get(rel_id)
    if not relacion or not relacion.qr_url:
        return "QR no generado aún. Solicite al registrador.", 404
    return render_template('cliente_qr.html',
                           qr_url=relacion.qr_url,
                           usuario_cliente=relacion.usuario_cliente,
                           password_cliente=relacion.password_cliente)
    
@cliente_bp.route('/logout_cliente')
def logout_cliente():
    session.pop('cliente_rel_id', None)
    return redirect('/login_cliente')