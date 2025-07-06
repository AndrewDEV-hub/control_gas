from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from models import Usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()
    if request.method == 'POST':
        nombre = request.form.get('usuario')
        password = request.form.get('password')
        usuario = Usuario.query.filter_by(nombre=nombre).first()
        if usuario and usuario.password == password:
            session['usuario_id'] = usuario.id
            session['usuario_nombre'] = usuario.nombre
            session['usuario_rol'] = usuario.rol
            return redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))