from flask import Blueprint, request, jsonify
from models import db, Vehiculo
import qrcode
import io
from flask import render_template
import requests
from flask import send_file
from models import Vehiculo, PersonaVehiculo, Persona
from werkzeug.utils import secure_filename
SUPABASE_URL = "https://wgczmcheqqffemfxfudc.supabase.co"
SUPABASE_BUCKET = "vehiculos"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndnY3ptY2hlcXFmZmVtZnhmdWRjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTY5MTcwNCwiZXhwIjoyMDY3MjY3NzA0fQ.n_nzBLg53_UtOBOJZEC8soyr6hclBa68TzudMeDT29E" 
vehiculo_bp = Blueprint('vehiculo', __name__)

@vehiculo_bp.route('/vehiculos', methods=['POST'])
def crear_vehiculo():
    data = request.get_json()
    vehiculo = Vehiculo(
        numero_crasis=data['numero_crasis'],
        placa=data['placa'],
        tipo=data['tipo'],
        foto=data.get('foto')  # <-- Debe estar así
    )
    db.session.add(vehiculo)
    db.session.commit()
    return jsonify({
        'id': vehiculo.id,
        'placa': vehiculo.placa,
        'tipo': vehiculo.tipo,
        'foto': vehiculo.foto,
        'verificado': vehiculo.verificado 
    }), 201

@vehiculo_bp.route('/vehiculos', methods=['GET'])
def listar_vehiculos():
    vehiculos = Vehiculo.query.all()
    resultado = []
    for v in vehiculos:
        persona_vehiculo = PersonaVehiculo.query.filter_by(vehiculo_id=v.id).first()
        ci = None
        if persona_vehiculo:
            persona = Persona.query.get(persona_vehiculo.persona_id)
            if persona:
                ci = persona.ci
        resultado.append({
            'id': v.id,
            'numero_crasis': v.numero_crasis,
            'placa': v.placa,
            'tipo': v.tipo,
            'foto': v.foto,
            'verificado': v.verificado,
            'qr_url': v.qr_url,
            'ci': ci
        })
    return jsonify(resultado)

@vehiculo_bp.route('/vehiculos/<int:id>', methods=['GET'])
def obtener_vehiculo(id):
    vehiculo = Vehiculo.query.get_or_404(id)
    persona_vehiculo = PersonaVehiculo.query.filter_by(vehiculo_id=id).first()
    ci = None
    if persona_vehiculo:
        persona = Persona.query.get(persona_vehiculo.persona_id)
        if persona:
            ci = persona.ci
    return jsonify({
        'id': vehiculo.id,
        'numero_crasis': vehiculo.numero_crasis,
        'placa': vehiculo.placa,
        'tipo': vehiculo.tipo,
        'foto': vehiculo.foto,
        'qr_url': vehiculo.qr_url,
        'ci': ci
    })

@vehiculo_bp.route('/vehiculos/<int:id>', methods=['PUT'])
def actualizar_vehiculo(id):
    vehiculo = Vehiculo.query.get_or_404(id)
    data = request.get_json()
    if 'numero_crasis' in data:
        vehiculo.numero_crasis = data['numero_crasis']
    if 'placa' in data:
        vehiculo.placa = data['placa']
    if 'tipo' in data:
        vehiculo.tipo = data['tipo']
    if 'foto' in data:
        vehiculo.foto = data['foto']  # <-- NUEVO
    db.session.commit()
    return jsonify({
        'id': vehiculo.id,
        'numero_crasis': vehiculo.numero_crasis,
        'placa': vehiculo.placa,
        'tipo': vehiculo.tipo,
        'foto': vehiculo.foto
    })

@vehiculo_bp.route('/vehiculos/<int:id>', methods=['DELETE'])
def eliminar_vehiculo(id):
    vehiculo = Vehiculo.query.get_or_404(id)
    db.session.delete(vehiculo)
    db.session.commit()
    return jsonify({'message': 'Vehículo eliminado'})

@vehiculo_bp.route('/vehiculos/<int:id>/verificar', methods=['PUT'])
def verificar_vehiculo(id):
    vehiculo = Vehiculo.query.get_or_404(id)
    vehiculo.verificado = True
    db.session.commit()
    return jsonify({'message': 'Vehículo verificado'})

@vehiculo_bp.route('/vehiculos/<int:vehiculo_id>/generar_qr', methods=['POST'])
def generar_qr(vehiculo_id):
    vehiculo = Vehiculo.query.get_or_404(vehiculo_id)
    persona_vehiculo = PersonaVehiculo.query.filter_by(vehiculo_id=vehiculo_id).first()
    if not persona_vehiculo:
        return jsonify({'error': 'No hay persona asociada'}), 400
    persona = Persona.query.get(persona_vehiculo.persona_id)
    if not persona:
        return jsonify({'error': 'No se encontró la persona'}), 400

    filename = f"qr_{vehiculo.placa}.png"
    storage_path = f"qr/{filename}"
    public_url = f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/{storage_path}"

    # Si ya existe un QR, verifica si el archivo existe en Supabase Storage
    if vehiculo.qr_url:
        # HEAD request para verificar existencia
        check_url = f"{SUPABASE_URL}/storage/v1/object/{SUPABASE_BUCKET}/{storage_path}"
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
        }
        check_response = requests.head(check_url, headers=headers)
        if check_response.status_code == 200:
            # El archivo existe, devuelve la info
            return jsonify({
                'qr_url': vehiculo.qr_url,
                'placa': vehiculo.placa,
                'ci': persona.ci
            })
        # Si no existe, continúa para generar uno nuevo

    # Genera un nuevo QR
    qr_data = f"Placa:{vehiculo.placa}\nCI:{persona.ci}"
    img = qrcode.make(qr_data)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "image/png"
    }
    upload_url = f"{SUPABASE_URL}/storage/v1/object/{SUPABASE_BUCKET}/{storage_path}"
    response = requests.put(upload_url, headers=headers, data=buffer.read())

    if response.status_code not in (200, 201):
        return jsonify({'error': 'Error al subir QR a Supabase Storage', 'details': response.text}), 500

    vehiculo.qr_url = public_url
    db.session.commit()
    return jsonify({
        'qr_url': vehiculo.qr_url,
        'placa': vehiculo.placa,
        'ci': persona.ci
    })
@vehiculo_bp.route('/usuario_qr') 
def usuario_qr():
    return render_template('usuario_qr.html')

@vehiculo_bp.route('/usuario_qr_login', methods=['POST'])
def usuario_qr_login():
    data = request.get_json()
    placa = data.get('placa')
    ci = data.get('ci')
    vehiculo = Vehiculo.query.filter_by(placa=placa).first()
    if not vehiculo:
        return jsonify({'error': 'Vehículo no encontrado'}), 404
    persona_vehiculo = PersonaVehiculo.query.filter_by(vehiculo_id=vehiculo.id).first()
    if not persona_vehiculo:
        return jsonify({'error': 'No hay persona asociada'}), 404
    persona = Persona.query.get(persona_vehiculo.persona_id)
    if not persona or str(persona.ci) != str(ci):
        return jsonify({'error': 'Credenciales incorrectas'}), 401
    if not vehiculo.qr_url:
        return jsonify({'error': 'QR no generado aún, solicita al registrador.'}), 400
    return jsonify({'qr_url': vehiculo.qr_url})
@vehiculo_bp.route('/vehiculos/buscar_por_placa_ci')
def buscar_por_placa_ci():
    placa = request.args.get('placa')
    ci = request.args.get('ci')
    vehiculo = Vehiculo.query.filter_by(placa=placa).first()
    if not vehiculo:
        return jsonify({'error': 'Vehículo no encontrado'}), 404
    persona_vehiculo = PersonaVehiculo.query.filter_by(vehiculo_id=vehiculo.id).first()
    if not persona_vehiculo:
        return jsonify({'error': 'No hay persona asociada'}), 404
    persona = Persona.query.get(persona_vehiculo.persona_id)
    if not persona or str(persona.ci) != str(ci):
        return jsonify({'error': 'Credenciales incorrectas'}), 404
    # Calcula datos adicionales si lo necesitas
    return jsonify({
        'nombre': persona.nombre,
        'ci': persona.ci,
        'es_funcionario': hasattr(persona, 'funcionario_publico'),
        'numero_credencial': getattr(persona, 'numero_credencial', ''),
        'numero_crasis': vehiculo.numero_crasis,
        'placa': vehiculo.placa,
        'tipo': vehiculo.tipo,
        'es_institucional': False,  # Completa según tu lógica
        'nombre_institucion': '',   # Completa según tu lógica
        'foto': vehiculo.foto,
        'vehiculo_id': vehiculo.id,
        'verificado': vehiculo.verificado,
        'total_cargado_mes': 0,     # Calcula si lo necesitas
        'restante_mes': 0,          # Calcula si lo necesitas
        'qr_url': vehiculo.qr_url
    })