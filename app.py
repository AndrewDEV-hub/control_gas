from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
import os
from dotenv import load_dotenv
from models import db
from controllers import blueprints



load_dotenv()
app = Flask(__name__)

# Verifica y muestra la variable de entorno
db_url = os.environ.get('DATABASE_URL')
if not db_url:
    raise RuntimeError("DATABASE_URL no está definida. Configúrala en Vercel.")

# Usa la variable de entorno DATABASE_URL que pondrás en Vercel
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db) 

# Registra todos los blueprints
for bp in blueprints:
    app.register_blueprint(bp)


@app.route("/", methods=["GET", "POST"])
def index():
    from models import Persona, db
    if request.method == "POST":
        ci = request.form.get("ci")
        nombre = request.form.get("nombre")
        if ci and nombre:
            persona = Persona(ci=ci, nombre=nombre)
            db.session.add(persona)
            db.session.commit()
        return redirect(url_for("index"))
    personas = Persona.query.all()
    return render_template("index.html", personas=personas)

@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar_persona(id):
    from models import Persona, db
    persona = Persona.query.get(id)
    if persona:
        db.session.delete(persona)
        db.session.commit()
    return redirect(url_for("index"))


@app.route("/test_db")
def test_db():
    from models import Persona
    try:
        persona = Persona.query.first()
        if persona:
            return f"Conectado a la base de datos. Primera persona: {persona.nombre}"
        else:
            return "Conectado a la base de datos, pero no hay personas."
    except Exception as e:
        return f"Error al conectar a la base de datos: {str(e)}", 500

app = app
    
