from flask import Flask, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
import os
from dotenv import load_dotenv
from models import db
from controllers import blueprints
from controllers.cliente_controlador import cliente_bp

load_dotenv()
app = Flask(__name__)

db_url = os.environ.get('DATABASE_URL')
if not db_url:
    raise RuntimeError("DATABASE_URL no está definida. Configúrala en Vercel.")

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "supersecreto"  # Cambia esto en producción
app.register_blueprint(cliente_bp)

db.init_app(app)
migrate = Migrate(app, db) 

for bp in blueprints:
    app.register_blueprint(bp)

@app.route("/")
def index():
    if 'usuario_id' not in session:
        return redirect(url_for('auth.login'))
    # Mostrar vista según el rol
    if session.get('usuario_rol') == "registrador":
        return render_template("registrador.html")
    # Puedes agregar aquí la vista del supervisor si lo deseas
    # elif session.get('usuario_rol') == "supervisor":
    #     return render_template("supervisor.html")
    return render_template("index.html")

app = app