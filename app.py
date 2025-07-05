from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
import os
from dotenv import load_dotenv
from models import db
from controllers.combustible_controlador import combustible_bp



load_dotenv()
app = Flask(__name__)

# Verifica y muestra la variable de entorno
db_url = os.environ.get('DATABASE_URL')
if not db_url:
    raise RuntimeError("DATABASE_URL no está definida. Configúrala en Vercel.")

# Usa la variable de entorno DATABASE_URL que pondrás en Vercel
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.register_blueprint(combustible_bp)

db.init_app(app)
migrate = Migrate(app, db) 

# Importa los modelos después de inicializar db
from models import Persona



@app.route("/")
def test_db():
    try:
        persona = Persona.query.first()
        if persona:
            return f"Conectado a la base de datos. Primera persona: {persona.nombre}"
        else:
            return "Conectado a la base de datos, pero no hay personas."
    except Exception as e:
        return f"Error al conectar a la base de datos: {str(e)}", 500

app = app
    
