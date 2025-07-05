from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
import os
from dotenv import load_dotenv
from models import db

load_dotenv()
app = Flask(__name__)

# Usa la variable de entorno DATABASE_URL que pondrás en Vercel
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db) 

# Importa los modelos después de inicializar db
from models import Persona

@app.route("/test_db")
def test_db():
    persona = Persona.query.first()
    if persona:
        return f"Conectado a la base de datos. Primera persona: {persona.nombre}"
    else:
        return "Conectado a la base de datos, pero no hay personas."