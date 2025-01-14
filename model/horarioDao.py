from model.conexion_db import ConexionDB
from flask import flash

# Modelo Horario
class Horario:
    def __init__(self, id_medico, id_consultorio, id_codificacion, fecha):
        self.id_horario = None
        self.id_medico = id_medico
        self.id_consultorio = id_consultorio
        self.id_codificacion = id_codificacion
        self.fecha = fecha

    def __str__(self):
        return f'Horario[Medico ID: {self.id_medico}, Consultorio ID: {self.id_consultorio}, Fecha: {self.fecha}]'


# Guardar un horario
def guardar(horario):
    if not horario.id_medico or not horario.id_consultorio or not horario.id_codificacion or not horario.fecha:
        return {"status": "danger", "message": "Por favor, completa todos los campos antes de guardar."}

    conexion = ConexionDB()
    sql = '''
    INSERT INTO horario (id_medico, id_consultorio, id_codificacion, fecha) 
    VALUES (%s, %s, %s, %s)
    '''
    try:
        conexion.cursor.execute(sql, (horario.id_medico, horario.id_consultorio, horario.id_codificacion, horario.fecha))
        conexion.cerrar()
        return {"status": "success", "message": "Horario guardado correctamente."}
    except Exception as e:
        conexion.cerrar()
        return {"status": "danger", "message": f"No se pudo guardar el horario: {e}"}


# Listar todos los horarios
def listar():
    conexion = ConexionDB()
    sql = '''
    SELECT h.id_horario, m.nombre, c.nombre, cod.sigla, cod.descripcion AS codificacion_nombre, cod.entrada, cod.salida, h.fecha
    FROM horario h
    JOIN medico m ON h.id_medico = m.id_medico
    JOIN consultorio c ON h.id_consultorio = c.id_consultorio
    JOIN codificacionhorarios cod ON h.id_codificacion = cod.id_codificacion
    '''
    try:
        conexion.cursor.execute(sql)
        registros = conexion.cursor.fetchall()
        conexion.cerrar()
        return registros
    except Exception as e:
        conexion.cerrar()
        return [], {"status": "danger", "message": f"No se pudo listar el horario: {e}"}


# Listar por ID
def listar_por_id_h(id):
    conexion = ConexionDB()
    sql = '''
    SELECT id_horario, id_medico, id_consultorio, id_codificacion, fecha
    FROM horario
    WHERE id_horario = %s
    '''
    try:
        conexion.cursor.execute(sql, (id,))
        registro = conexion.cursor.fetchone()
        conexion.cerrar()
        if registro:
            return registro
        else:
            return None, {"status": "danger", "message": f"No se encontró el horario con ID {id}"}
    except Exception as e:
        conexion.cerrar()
        #flash(f"No se pudo recuperar el horario con ID {id}: {e}", "danger")
        return None, {"status": "danger", "message": f"No se pudo recuperar el horario con ID {id}: {e}"}


# Listar médicos para llenar el combo
def listar_medicos():
    conexion = ConexionDB()
    sql = "SELECT id_medico, nombre FROM medico"
    try:
        conexion.cursor.execute(sql)
        registros = conexion.cursor.fetchall()
        conexion.cerrar()
        return registros
    except Exception as e:
        conexion.cerrar()
        #flash(f"No se pudo recuperar la lista de médicos: {e}", "danger")
        return [], {"status": "danger", "message": f"No se pudo recuperar la lista de médicos: {e}"}


# Listar consultorios para llenar el combo
def listar_consultorios_horario():
    conexion = ConexionDB()
    sql = "SELECT id_consultorio, nombre FROM consultorio"
    try:
        conexion.cursor.execute(sql)
        registros = conexion.cursor.fetchall()
        conexion.cerrar()
        return registros
    except Exception as e:
        conexion.cerrar()
        #flash(f"No se pudo recuperar la lista de consultorios: {e}", "danger")
        return [], {"status": "danger", "message": f"No se pudo recuperar la lista de consultorios: {e}"}


# Listar codificación de horarios para llenar el combo
def listar_codificacion_horario():
    conexion = ConexionDB()
    sql = "SELECT id_codificacion, sigla, descripcion, entrada, salida FROM codificacionhorarios"
    try:
        conexion.cursor.execute(sql)
        registros = conexion.cursor.fetchall()
        conexion.cerrar()
        return registros
    except Exception as e:
        conexion.cerrar()
        #flash(f"No se pudo recuperar la lista de codificaciones: {e}", "danger")
        return [], {"status": "danger", "message": f"No se pudo recuperar la lista de codificaciones: {e}"}


# Editar horario
def editar_horario(horario, id):
    conexion = ConexionDB()
    sql = '''
    UPDATE horario
    SET id_medico = %s, id_consultorio = %s, id_codificacion = %s, fecha = %s
    WHERE id_horario = %s
    '''
    try:
        # Ejecutar consulta SQL
        conexion.cursor.execute(sql, (horario.id_medico, horario.id_consultorio, horario.id_codificacion, horario.fecha, id))
        conexion.cerrar()
        return {"status": "success", "message": "El registro se actualizó correctamente."}
    except Exception as e:
        conexion.cerrar()
        return {"status": "danger", "message": f"No se pudo editar el registro: {e}"}


# Eliminar horario
def eliminar_horario(id):
    conexion = ConexionDB()
    sql = "DELETE FROM horario WHERE id_horario = %s"
    try:
        conexion.cursor.execute(sql, (id,))
        conexion.cerrar()
        return {"status": "success", "message": "Horario eliminado correctamente."}
    except Exception as e:
        conexion.cerrar()
        return {"status": "danger", "message": f"No se pudo eliminar el horario: {e}"}


#para mostrar en calendario
def listar_horarios_por_fecha():
    conexion = ConexionDB()
    sql = '''
    SELECT 
        h.fecha,
        m.nombre AS medico,
        c.nombre AS consultorio,
        ch.sigla AS codificacion_sigla,
        ch.descripcion AS codificacion_descripcion
    FROM horario h
    JOIN medico m ON h.id_medico = m.id_medico
    JOIN consultorio c ON h.id_consultorio = c.id_consultorio
    JOIN codificacionhorarios ch ON h.id_codificacion = ch.id_codificacion
    ORDER BY h.fecha;
    '''
    try:
        conexion.cursor.execute(sql)
        registros = conexion.cursor.fetchall()
        conexion.cerrar()
        return registros
    except Exception as e:
        conexion.cerrar()
        return [], {"status": "danger", "message": f"No se pudo listar los horarios: {e}"}
