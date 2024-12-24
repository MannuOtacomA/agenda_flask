from model.conexion_db import ConexionDB

def consultar_usos_consultorios(fecha_inicio, fecha_fin, id_consultorio=None):
    conexion = ConexionDB()
    sql = '''
    SELECT c.nombre AS consultorio, COUNT(h.id_horario) AS usos
    FROM Consultorio c
    LEFT JOIN Horario h 
        ON c.id_consultorio = h.id_consultorio 
        AND h.fecha BETWEEN %s AND %s
    WHERE (%s IS NULL OR c.id_consultorio = %s)
    GROUP BY c.nombre
    ORDER BY usos DESC
    '''
    try:
        # Ejecutar consulta con parámetros (fechas e ID de consultorio opcional)
        conexion.cursor.execute(sql, (fecha_inicio, fecha_fin, id_consultorio, id_consultorio))
        registros = conexion.cursor.fetchall()
        conexion.cerrar()
        return {"status": "success", "data": registros}
    except Exception as e:
        conexion.cerrar()
        return {"status": "danger", "message": f"Error en la consulta: {e}"}


# Listar consultorios para llenar el combo
def listar_consultorios_reporte():
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


def consultar_horas_medicos(fecha_inicio, fecha_fin, id_medico=None):
    conexion = ConexionDB()
    sql = '''
    SELECT m.nombre AS medico, SUM(ch.horas) AS total_horas_ocupacion
    FROM Horario h
    INNER JOIN Medico m ON h.id_medico = m.id_medico
    INNER JOIN CodificacionHorarios ch ON h.id_codificacion = ch.id_codificacion
    WHERE (%s IS NULL OR m.id_medico = %s)
      AND h.fecha BETWEEN %s AND %s
    GROUP BY m.nombre
    ORDER BY total_horas_ocupacion DESC;
    '''
    try:
        # Ejecutar consulta con parámetros
        conexion.cursor.execute(sql, (id_medico, id_medico, fecha_inicio, fecha_fin))
        registros = conexion.cursor.fetchall()
        conexion.cerrar()
        return {"status": "success", "data": registros}
    except Exception as e:
        conexion.cerrar()
        return {"status": "danger", "message": f"Error en la consulta: {e}"}


# Listar médicos para llenar el combo
def listar_medicos_reporte():
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


#horas medicos detalle
def consultar_horas_medicos_detalle(fecha_inicio, fecha_fin, id_medico=None, id_consultorio=None):
    conexion = ConexionDB()
    sql = '''
    SELECT 
        m.nombre AS medico,
        c.nombre AS consultorio,
        h.fecha,
        ch.entrada AS hora_inicio,
        ch.salida AS hora_fin,
        EXTRACT(EPOCH FROM (ch.salida - ch.entrada)) / 3600 AS horas_trabajadas,
        SUM(EXTRACT(EPOCH FROM (ch.salida - ch.entrada)) / 3600) OVER (PARTITION BY m.id_medico) AS total_horas_periodo
    FROM 
        Horario h
    INNER JOIN 
        Medico m ON h.id_medico = m.id_medico
    INNER JOIN 
        Consultorio c ON h.id_consultorio = c.id_consultorio
    INNER JOIN 
        CodificacionHorarios ch ON h.id_codificacion = ch.id_codificacion
    WHERE 
        (%s IS NULL OR m.id_medico = %s)
        AND (%s IS NULL OR c.id_consultorio = %s)
        AND h.fecha BETWEEN %s AND %s
    ORDER BY 
        h.fecha, ch.entrada
    '''
    try:
        # Ejecutar la consulta
        conexion.cursor.execute(sql, (id_medico, id_medico, id_consultorio, id_consultorio, fecha_inicio, fecha_fin))
        registros = conexion.cursor.fetchall()
        conexion.cerrar()
        return {"status": "success", "data": registros}
    except Exception as e:
        conexion.cerrar()
        return {"status": "danger", "message": f"Error en la consulta: {e}"}

# Listar cosnultorio para llenar el combo
def listar_consultorios_reporte():
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




"""
def consultar_usos_consultorios(fecha_inicio, fecha_fin):
    conexion = ConexionDB()
    sql = '''
    SELECT c.nombre AS consultorio, COUNT(h.id_horario) AS usos
    FROM Consultorio c
    LEFT JOIN Horario h ON c.id_consultorio = h.id_consultorio AND h.fecha BETWEEN %s AND %s
    GROUP BY c.nombre
    ORDER BY usos DESC
    '''
    try:
        conexion.cursor.execute(sql, (fecha_inicio, fecha_fin))
        registros = conexion.cursor.fetchall()
        conexion.cerrar()
        return {"status": "success", "data": registros}  # Retorno estructurado
    except Exception as e:
        conexion.cerrar()
        return {"status": "danger", "message": f"Error en la consulta: {e}"}
"""