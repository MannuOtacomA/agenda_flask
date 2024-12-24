from model.conexion_db import ConexionDB
from tkinter import messagebox

# Modelo Consultorio
class Consultorio:
    def __init__(self, nombre, id_hospital=None):
        self.id_consultorio = None
        self.nombre = nombre
        self.id_hospital = id_hospital  # Relación con el hospital

    def __str__(self):
        return f'Consultorio[{self.nombre}, Hospital ID: {self.id_hospital}]'

# Guardar
def guardar(consultorio):
    # Validación de que los campos no estén vacíos
    if not consultorio.nombre or not consultorio.id_hospital:
        titulo = "Campos Vacíos"
        mensaje = "Por favor, completa todos los campos antes de guardar."
        messagebox.showerror(titulo, mensaje)
        return  # No continuar con la ejecución si los campos están vacíos

    conexion = ConexionDB()
    sql = '''
    INSERT INTO consultorio (nombre, id_hospital) 
    VALUES (%s, %s)
    '''
    try:
        conexion.cursor.execute(sql, (consultorio.nombre, consultorio.id_hospital))
        conexion.cerrar()
        titulo = "Registro Exitoso"
        mensaje = "Los datos del consultorio se guardaron correctamente."
        messagebox.showinfo(titulo, mensaje)
    except Exception as e:
        conexion.cerrar()
        titulo = "Error de Registro"
        mensaje = f"No se pudo guardar el registro: {e}"
        messagebox.showerror(titulo, mensaje)

# Listar todos los consultorios
def listar():
    conexion = ConexionDB()
    sql = "SELECT * FROM consultorio"
    try:
        conexion.cursor.execute(sql)
        registros = conexion.cursor.fetchall()
        conexion.cerrar()
        return registros
    except Exception as e:
        conexion.cerrar()
        titulo = "Error al Listar"
        mensaje = f"No se pudo recuperar la lista de consultorios: {e}"
        messagebox.showerror(titulo, mensaje)
        return []

# Modificar la función listar para incluir el nombre del hospital
def listar_con_nom_hos():
    conexion = ConexionDB()
    sql = '''
    SELECT consultorio.id_consultorio, consultorio.nombre, hospital.nombre AS hospital_nombre
    FROM consultorio
    JOIN hospital ON consultorio.id_hospital = hospital.id_hospital
    '''
    try:
        conexion.cursor.execute(sql)
        registros = conexion.cursor.fetchall()
        conexion.cerrar()
        return registros
    except Exception as e:
        conexion.cerrar()
        titulo = "Error al Listar"
        mensaje = f"No se pudo recuperar la lista de consultorios: {e}"
        messagebox.showerror(titulo, mensaje)
        return []


# Listar todos los hospitales  para llenar combo
def listar_h_id_nom():
    conexion = ConexionDB()
    sql = "SELECT id_hospital, nombre FROM hospital"
    try:
        conexion.cursor.execute(sql)
        registros = conexion.cursor.fetchall()
        conexion.cerrar()
        return registros
    except Exception as e:
        conexion.cerrar()
        titulo = "Error al Listar"
        mensaje = f"No se pudo recuperar la lista de hospitales: {e}"
        messagebox.showerror(titulo, mensaje)
        return []

# Listar un consultorio por ID
def listar_por_id(id_consultorio):
    conexion = ConexionDB()
    sql = "SELECT * FROM consultorio WHERE id_consultorio = %s"
    try:
        conexion.cursor.execute(sql, (id_consultorio,))
        registro = conexion.cursor.fetchone()  # Esperamos un único resultado
        conexion.cerrar()

        if registro:
            return registro
        else:
            return None
    except Exception as e:
        conexion.cerrar()
        titulo = "Error al Listar por ID"
        mensaje = f"No se pudo recuperar el consultorio con ID {id_consultorio}: {e}"
        messagebox.showerror(titulo, mensaje)
        return None

# Editar un consultorio
def editar(consultorio, id_consultorio):
    conexion = ConexionDB()
    sql = '''
    UPDATE consultorio 
    SET nombre = %s, id_hospital = %s
    WHERE id_consultorio = %s
    '''
    try:
        conexion.cursor.execute(sql, (consultorio.nombre, consultorio.id_hospital, id_consultorio))
        conexion.cerrar()
        titulo = "Edición Exitosa"
        mensaje = "El registro se actualizó correctamente."
        messagebox.showinfo(titulo, mensaje)
    except Exception as e:
        conexion.cerrar()
        titulo = "Error al Editar"
        mensaje = f"No se pudo editar el registro: {e}"
        messagebox.showerror(titulo, mensaje)

# Eliminar un consultorio
def eliminar(id_consultorio):
    conexion = ConexionDB()
    sql = "DELETE FROM consultorio WHERE id_consultorio = %s"
    try:
        conexion.cursor.execute(sql, (id_consultorio,))
        conexion.cerrar()
        titulo = "Eliminación Exitosa"
        mensaje = "El registro se eliminó correctamente."
        messagebox.showinfo(titulo, mensaje)
    except Exception as e:
        conexion.cerrar()
        titulo = "Error al Eliminar"
        mensaje = f"No se pudo eliminar el registro: {e}"
        messagebox.showerror(titulo, mensaje)
