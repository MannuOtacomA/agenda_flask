from model.conexion_db import ConexionDB
from tkinter import messagebox

# Modelo Medico
class Medico:
    def __init__(self, nombre, especialidad, telefono, id_hospital=None):
        self.id_medico = None
        self.nombre = nombre
        self.especialidad = especialidad
        self.telefono = telefono
        self.id_hospital = id_hospital  # Relación con el hospital

    def __str__(self):
        return f'Medico[{self.nombre},{self.especialidad},{self.telefono}, Hospital ID: {self.id_hospital}]'

# Guardar
def guardar(medico):
    # Validación de que los campos no estén vacíos
    if not medico.nombre or not medico.especialidad or not medico.telefono or not medico.id_hospital:
        titulo = "Campos Vacíos"
        mensaje = "Por favor, completa todos los campos antes de guardar."
        messagebox.showerror(titulo, mensaje)
        return  # No continuar con la ejecución si los campos están vacíos

    conexion = ConexionDB()
    sql = '''
    INSERT INTO medico (nombre, especialidad, telefono, id_hospital) 
    VALUES (%s, %s, %s, %s)
    '''
    try:
        conexion.cursor.execute(sql, (medico.nombre, medico.especialidad, medico.telefono, medico.id_hospital))
        conexion.cerrar()
        titulo = "Registro Exitoso"
        mensaje = "Los datos del medico se guardaron correctamente."
        messagebox.showinfo(titulo, mensaje)
    except Exception as e:
        conexion.cerrar()
        titulo = "Error de Registro"
        mensaje = f"No se pudo guardar el registro: {e}"
        messagebox.showerror(titulo, mensaje)

# Listar todos los médicos
def listar():
    conexion = ConexionDB()
    sql = "SELECT * FROM medico"
    try:
        conexion.cursor.execute(sql)
        registros = conexion.cursor.fetchall()
        conexion.cerrar()
        return registros
    except Exception as e:
        conexion.cerrar()
        titulo = "Error al Listar"
        mensaje = f"No se pudo recuperar la lista de medicos: {e}"
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

# Listar un médico por ID
def listar_por_id(id_medico):
    conexion = ConexionDB()
    sql = "SELECT * FROM medico WHERE id_medico = %s"
    try:
        conexion.cursor.execute(sql, (id_medico,))
        registro = conexion.cursor.fetchone()  # Esperamos un único resultado
        conexion.cerrar()

        if registro:
            return registro
        else:
            return None
    except Exception as e:
        conexion.cerrar()
        titulo = "Error al Listar por ID"
        mensaje = f"No se pudo recuperar el medico con ID {id_medico}: {e}"
        messagebox.showerror(titulo, mensaje)
        return None

# Editar un médico
def editar(medico, id_medico):
    conexion = ConexionDB()
    sql = '''
    UPDATE medico 
    SET nombre = %s, especialidad = %s, telefono = %s, id_hospital = %s
    WHERE id_medico = %s
    '''
    try:
        conexion.cursor.execute(sql, (medico.nombre, medico.especialidad, medico.telefono, medico.id_hospital, id_medico))
        conexion.cerrar()
        titulo = "Edición Exitosa"
        mensaje = "El registro se actualizó correctamente."
        messagebox.showinfo(titulo, mensaje)
    except Exception as e:
        conexion.cerrar()
        titulo = "Error al Editar"
        mensaje = f"No se pudo editar el registro: {e}"
        messagebox.showerror(titulo, mensaje)

# Eliminar un médico
def eliminar(id_medico):
    conexion = ConexionDB()
    sql = "DELETE FROM medico WHERE id_medico = %s"
    try:
        conexion.cursor.execute(sql, (id_medico,))
        conexion.cerrar()
        titulo = "Eliminación Exitosa"
        mensaje = "El registro se eliminó correctamente."
        messagebox.showinfo(titulo, mensaje)
    except Exception as e:
        conexion.cerrar()
        titulo = "Error al Eliminar"
        mensaje = f"No se pudo eliminar el registro: {e}"
        messagebox.showerror(titulo, mensaje)
