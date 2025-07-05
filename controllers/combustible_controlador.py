from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Persona, Vehiculo, PersonaVehiculo, Estacion, CargaCombustible, FuncionarioPublico, VehiculoInstitucional

combustible_bp = Blueprint('combustible', __name__)

@combustible_bp.route("/cargar_combustible", methods=["GET", "POST"])
def cargar_combustible():
    if request.method == "POST":
        nombre = request.form["nombre"]
        ci = request.form["ci"]
        numero_crasis = request.form["numero_crasis"]
        placa = request.form["placa"]
        tipo = request.form["tipo"]
        funcionario = "funcionario" in request.form
        institucional = "institucional" in request.form
        nombre_institucion = request.form.get("nombre_institucion")
        estacion_nombre = request.form["estacion"]
        ubicacion = request.form["ubicacion"]
        cantidad = request.form["cantidad"]

        # Persona
        persona = Persona.query.filter_by(ci=ci).first()
        if not persona:
            persona = Persona(ci=ci, nombre=nombre)
            db.session.add(persona)
            db.session.commit()

        # Vehículo
        vehiculo = Vehiculo.query.filter_by(placa=placa).first()
        if not vehiculo:
            vehiculo = Vehiculo(numero_crasis=numero_crasis, placa=placa, tipo=tipo)
            db.session.add(vehiculo)
            db.session.commit()

        # Relación Persona-Vehículo
        if not PersonaVehiculo.query.filter_by(persona_id=persona.id, vehiculo_id=vehiculo.id).first():
            db.session.add(PersonaVehiculo(persona_id=persona.id, vehiculo_id=vehiculo.id))
            db.session.commit()

        # Funcionario público
        if funcionario and not FuncionarioPublico.query.filter_by(persona_id=persona.id).first():
            db.session.add(FuncionarioPublico(persona_id=persona.id, numero_credencial=""))
            db.session.commit()

        # Vehículo institucional
        if institucional and not VehiculoInstitucional.query.filter_by(vehiculo_id=vehiculo.id).first():
            db.session.add(VehiculoInstitucional(vehiculo_id=vehiculo.id, nombre_institucion=nombre_institucion or ""))
            db.session.commit()

        # Estación
        estacion = Estacion.query.filter_by(nombre=estacion_nombre, ubicacion=ubicacion).first()
        if not estacion:
            estacion = Estacion(nombre=estacion_nombre, ubicacion=ubicacion)
            db.session.add(estacion)
            db.session.commit()

        # Carga de combustible
        carga = CargaCombustible(
            vehiculo_id=vehiculo.id,
            estacion_id=estacion.id,
            cantidad=cantidad
        )
        db.session.add(carga)
        db.session.commit()

        return redirect(url_for("test_db"))

    return render_template("cargar_combustible.html")