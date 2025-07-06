from .persona_controlador import persona_bp
from .vehiculo_controlador import vehiculo_bp
from .estacion_controlador import estacion_bp
from .usuario_controlador import usuario_bp
from .carga_combustible_controlador import carga_combustible_bp
from .funcionario_publico_controlador import funcionario_publico_bp
from .vehiculo_institucional import vehiculo_institucional_bp
from .persona_vehiculo_controlador import persona_vehiculo_bp
from .auth_controlador import auth_bp

blueprints = [
    persona_bp,
    vehiculo_bp,
    estacion_bp,
    usuario_bp,
    carga_combustible_bp,
    funcionario_publico_bp,
    vehiculo_institucional_bp,
    persona_vehiculo_bp,
    auth_bp
]