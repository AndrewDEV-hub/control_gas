from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .persona import Persona
from .vehiculo import Vehiculo
from .persona_vehiculo import PersonaVehiculo
from .usuario import Usuario
from .estacion import Estacion
from .carga_combustible import CargaCombustible
from .funcionario_publico import FuncionarioPublico
from .vehiculo_institucional import VehiculoInstitucional