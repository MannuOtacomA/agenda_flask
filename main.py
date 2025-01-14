from flask import Flask, render_template, request, redirect, flash, url_for
from model.hospitalDao import Hospital, listar, guardar, eliminar, editar, listar_por_id
from model.medicoDao import Medico, listar as lm, guardar as gm, eliminar as elim, editar as em, listar_por_id as lporid, listar_h_id_nom
from model.consultorioDao import Consultorio, listar as liscon, guardar as guacon, eliminar as elicon, editar as edicon, listar_por_id as lisporiddcon, listar_h_id_nom  as lismhosidnom, listar_con_nom_hos
from model.horarioDao import Horario, listar, guardar as guardarHorario, listar_por_id_h, listar_medicos, listar_consultorios_horario, listar_codificacion_horario, editar_horario, eliminar_horario
from  model.reportesDao import consultar_usos_consultorios, listar_consultorios_reporte, consultar_horas_medicos, listar_medicos_reporte, consultar_horas_medicos_detalle, listar_consultorios_reporte


app = Flask(__name__)
app.secret_key = 'clave_secreta_para_flash'  # Necesario para usar sesiones

@app.route("/")
def index():
    return render_template("index.html")


#----------HOSPITAL
@app.route("/hospital")
def index_hospital():
    hospital = listar()
    return render_template("modulos/hospital/index.html", listaHospital=hospital)

#crear
@app.route("/hospital/create")
def hospital_create():
    return render_template("modulos/hospital/create.html")

@app.route("/hospital/create/guardar", methods=["POST"])
def hospital_guardar():
    hospital = Hospital(
        nombre = request.form["nombre"],
        direccion = request.form["direccion"],
        telefono = request.form["telefono"]
    )
    guardar(hospital)
    return redirect("/hospital")

#eliminar
@app.route("/hospital/delete/<int:id>")
def hospital_delete(id):
    eliminar(id)
    return redirect("/hospital")

#retorna dato x id y carga en el form
@app.route("/hospital/edit/<int:id>")
def hospital_edit(id):
    hospital = listar_por_id(id)
    return render_template("/modulos/hospital/edit.html", listaHospital=hospital)

#actualizar
@app.route("/hospital/edit/actualizar", methods=["POST"])
def hospital_actualizar():
    id = request.form["txtId"]
    hospital = Hospital(
        nombre=request.form["nombre"],
        direccion=request.form["direccion"],
        telefono=request.form["telefono"]
    )
    editar(hospital,id)
    return redirect("/hospital")

#----------MEDICO
@app.route("/medico")
def index_medico():
    datos = lm()
    return render_template("modulos/medico/index.html", lista=datos)

#carga frm create
@app.route("/medico/create")
def medico_create():
    daros = listar_h_id_nom()
    return render_template("modulos/medico/create.html", listaIdNom = daros)
#guardar
@app.route("/medico/create/guardar", methods=["POST"])
def medico_guardar():
    medico = Medico(
        nombre = request.form["nombre"],
        especialidad = request.form["especialidad"],
        telefono = request.form["telefono"],
        id_hospital = request.form["hospital"]
    )
    gm(medico)
    return redirect("/medico")

#retorna dato x id y carga en el form
@app.route("/medico/edit/<int:id>")
def medico_edit(id):
    # Obtener la lista de hospitales
    datos_id_nom = listar_h_id_nom()
    # Obtener los datos del médico por ID
    datos = lporid(id)
    return render_template("/modulos/medico/edit.html",
                           listaHospital=datos, listaHospital_id_nom= datos_id_nom)

#actualizar
@app.route("/medico/edit/actualizar", methods=["POST"])
def medico_actualizar():
    id = request.form["txtId"]
    medico = Medico(
        nombre=request.form["nombre"],
        especialidad=request.form["especialidad"],
        telefono=request.form["telefono"],
        id_hospital=request.form["hospital"]
    )
    #editar as em,
    em(medico,id)
    return redirect("/medico")

#eliminar
@app.route("/medico/delete/<int:id>")
def medico_delete(id):
    elim(id)
    return redirect("/medico")


#----------CONSULTORIO
@app.route("/consultorio")
def index_consultorio():
    datos = listar_con_nom_hos()  # Listar todos los consultorios con nom hosp
    return render_template("modulos/consultorio/index.html", lista=datos)

@app.route("/consultorio/create")
def consultorio_create():
    hospitales = lismhosidnom()  # Obtener hospitales para el combobox
    return render_template("modulos/consultorio/create.html", listaIdNom=hospitales)

@app.route("/consultorio/create/guardar", methods=["POST"])
def consultorio_guardar():
    nombre = request.form["nombre"]
    id_hospital = request.form["hospital"]
    consultorio = Consultorio(nombre=nombre, id_hospital=id_hospital)
    guacon(consultorio)  # Llamar la función guardar
    return redirect("/consultorio")

@app.route("/consultorio/edit/<int:id>")
def consultorio_edit(id):
    datos = lisporiddcon(id)  # Obtener el consultorio por ID
    hospitales = lismhosidnom()  # Obtener hospitales para el combobox
    return render_template("modulos/consultorio/edit.html", listaConsultorio=datos, listaHospital_id_nom=hospitales)

@app.route("/consultorio/edit/actualizar", methods=["POST"])
def consultorio_actualizar():
    id = request.form["txtId"]
    nombre = request.form["nombre"]
    id_hospital = request.form["hospital"]
    consultorio = Consultorio(nombre=nombre, id_hospital=id_hospital)
    edicon(consultorio, id)  # Llamar la función editar
    return redirect("/consultorio")

@app.route("/consultorio/delete/<int:id>")
def consultorio_delete(id):
    elicon(id)  # Eliminar el consultorio
    return redirect("/consultorio")


#----------HORARIO
#listar
@app.route("/horario")
def index_horario():
    #datos = listar()  # Listar todos los horarios con datos asociados
    #return render_template("modulos/horario/index.html", lista=datos)
    horarios = listar_horarios_por_fecha()  # Obtener datos de horarios
    return render_template("modulos/horario/index.html", horarios=horarios)


#create
@app.route("/horario/create")
def horario_create():
    medicos = listar_medicos()  # Obtener médicos para el combobox
    consultorios = listar_consultorios_horario()  # Obtener consultorios para el combobox
    codificaciones = listar_codificacion_horario()  # Obtener codificaciones para el combobox
    return render_template("modulos/horario/create.html", listaMedicos=medicos, listaConsultorios=consultorios, listaCodificaciones=codificaciones)

#guardar
@app.route("/horario/create/guardar", methods=["POST"])
def horario_guardar():
    id_medico = request.form["medico"]
    id_consultorio = request.form["consultorio"]
    id_codificacion = request.form["codificacion"]
    fecha = request.form["fecha"]
    #crea tipo dato horario y guarda
    horario = Horario(id_medico=id_medico, id_consultorio=id_consultorio, id_codificacion=id_codificacion, fecha=fecha)
    resultado = guardarHorario(horario)  # Guardar el horario
    # Verifica si el resultado no es None
    if resultado is None:
        flash("Error desconocido al guardar el horario.", "danger")
    else:
        flash(resultado["message"], resultado["status"])
    return redirect("/horario")

#cargar frm edit
@app.route("/horario/edit/<int:id>")
def horario_edit(id):
    # Obtener el horario por ID
    datos = listar_por_id_h (id)
    # Obtener las listas para los select
    medicos = listar_medicos()
    consultorios = listar_consultorios_horario()
    codificaciones = listar_codificacion_horario()
    return render_template("modulos/horario/edit.html",
                           listaHorario=datos, listaMedicos=medicos,
                           listaConsultorios=consultorios, listaCodificaciones=codificaciones)

#actualizar
@app.route("/horario/edit/actualizar", methods=["POST"])
def horario_actualizar():
    id = request.form["txtId"]
    id_medico = request.form["medico"]
    id_consultorio = request.form["consultorio"]
    id_codificacion = request.form["codificacion"]
    fecha = request.form["fecha"]

    horario = Horario(id_medico=id_medico, id_consultorio=id_consultorio, id_codificacion=id_codificacion, fecha=fecha)
    resultado = editar_horario(horario, id)  # Implementar función editar en el modelo
    # Verifica si el resultado no es None
    if resultado is None:
        flash("Error desconocido al guardar el horario.", "danger")
    else:
        flash(resultado["message"], resultado["status"])
    return redirect("/horario")

#eliminar
@app.route("/horario/delete/<int:id>")
def horario_delete(id):
    resultado = eliminar_horario(id)  # Implementar función eliminar en el modelo
    # Verifica si el resultado no es None
    if resultado is None:
        flash("Error desconocido al guardar el horario.", "danger")
    else:
        flash(resultado["message"], resultado["status"])
    return redirect("/horario")


#----------reporte
@app.route("/reportes")
def index_reportes():
    datos = listar_consultorios_reporte()
    return render_template("modulos/reportes/index.html", listaConsultorios=datos)

#reportes  uso de consultorio
@app.route("/reportes", methods=["GET", "POST"])
def reporte_usos_consultorios():
    resultados = []
    consultorios = listar_consultorios_reporte()  # Obtener lista de consultorios para el filtro
    if request.method == "POST":
        fecha_inicio = request.form.get("fecha_inicio")
        fecha_fin = request.form.get("fecha_fin")
        id_consultorio = request.form.get("consultorio")
        id_consultorio = id_consultorio if id_consultorio else None  # Convertir vacío a None

        reporte = consultar_usos_consultorios(fecha_inicio, fecha_fin, id_consultorio)

        if reporte["status"] == "success":
            resultados = reporte["data"]
        else:
            flash(reporte["message"], "danger")

    return render_template(
        "modulos/reportes/index.html",
        resultados=resultados,
        listaConsultorios=consultorios  # Pasar lista de consultorios al template
    )


#reporte horas medico
@app.route("/reporte_horas_medicos")
def index_horas_medicos():
    datos = listar_medicos_reporte()
    return render_template("modulos/reportes/reporte_horas_medicos.html", listaMedicos=datos)

#reporte
@app.route("/reporte_horas_medicos", methods=["GET", "POST"])
def crear_reporte_horas_medicos():
    resultados = []
    medicos = listar_medicos_reporte()  # Obtener lista de médicos para el filtro
    if request.method == "POST":
        fecha_inicio = request.form.get("fecha_inicio")
        fecha_fin = request.form.get("fecha_fin")
        id_medico = request.form.get("medico")
        id_medico = id_medico if id_medico else None  # Convertir vacío a None

        reporte = consultar_horas_medicos(fecha_inicio, fecha_fin, id_medico)

        if reporte["status"] == "success":
            resultados = reporte["data"]
        else:
            flash(reporte["message"], "danger")

    return render_template(
        "modulos/reportes/reporte_horas_medicos.html",
        resultados=resultados,
        listaMedicos=medicos  # Pasar lista de médicos al template
    )

#reporte horas medico detalle
@app.route("/reporte_horas_medicos_detalle")
def index_horas_medicos_detalle():
    datos = listar_medicos_reporte()
    datosConsultorio = listar_consultorios_reporte()
    return render_template("modulos/reportes/reporte_horas_medicos_detalle.html", listaMedicos=datos, listaConsultorios=datosConsultorio)

#
@app.route("/reporte_horas_medicos_detalle", methods=["GET", "POST"])
def crear_reporte_horas_medicos_detalle():
    resultados = []
    medicos = listar_medicos_reporte()  # Obtener lista de médicos para el filtro
    consultorios = listar_consultorios_reporte()  # Obtener lista de médicos para el filtro
    if request.method == "POST":
        fecha_inicio = request.form.get("fecha_inicio")
        fecha_fin = request.form.get("fecha_fin")
        id_medico = request.form.get("medico")
        id_medico = id_medico if id_medico else None  # Convertir vacío a None

        reporte = consultar_horas_medicos_detalle(fecha_inicio, fecha_fin, id_medico)

        if reporte["status"] == "success":
            resultados = reporte["data"]
        else:
            flash(reporte["message"], "danger")

    return render_template(
        "modulos/reportes/reporte_horas_medicos_detalle.html",
        resultados=resultados,
        listaMedicos=medicos,  # Pasar lista de médicos al template
        listaConsultorios=consultorios # Pasar lista de consulrtorios al template
    )


#iniciar la app
if __name__=="__main__":
    app.run(debug=True)