from model.conexion_db import ConexionDB
from tkinter import messagebox

def crear_tabla():
    conexion = ConexionDB()
    sql = '''
    CREATE TABLE IF NOT EXISTS hospital (
        id_hospital SERIAL PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        direccion VARCHAR(100) NOT NULL,
        telefono VARCHAR(50) NOT NULL
    )
    '''
    try:
        conexion.cursor.execute(sql)
        conexion.cerrar()
        titulo = "Crear Registro"
        mensaje = "Se creó la tabla en la base de datos PostgreSQL."
        messagebox.showinfo(titulo, mensaje)
    except Exception as e:
        conexion.cerrar()
        titulo = "Error al Crear"
        mensaje = f"No se pudo crear la tabla: {e}"
        messagebox.showerror(titulo, mensaje)

def boorar_tabla():
    conexion = ConexionDB()
    sql = "DROP TABLE hospital"
    try:
        conexion.cursor.execute(sql)
        conexion.cerrar()
        titulo = "Borrar Registro"
        mensaje = "Se borro la tabla en la base de datos"
        messagebox.showinfo(titulo, mensaje)
    except:
        titulo = "Borrar Registro"
        mensaje = "No existe tabla para borrar"
        messagebox.showwarning(titulo, mensaje)

#modelo hospital
class Hospital():
    def __init__(self, nombre,direccion,telefono):
        self.id_hospital = None
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono

    def __str__(self):
        return f'Hospital[{self.nombre},{self.direccion},{self.telefono}]'

#guardar
def guardar(hospital):
    conexion = ConexionDB()
    sql = '''
    INSERT INTO hospital (nombre, direccion, telefono) 
    VALUES (%s, %s, %s)
    '''
    try:
        conexion.cursor.execute(sql, (hospital.nombre, hospital.direccion, hospital.telefono))
        conexion.cerrar()
        titulo = "Registro Exitoso"
        mensaje = "Los datos del hospital se guardaron correctamente."
        messagebox.showinfo(titulo, mensaje)
    except Exception as e:
        conexion.cerrar()
        titulo = "Error de Registro"
        mensaje = f"No se pudo guardar el registro: {e}"
        messagebox.showerror(titulo, mensaje)


#listar
def listar():
    conexion = ConexionDB()
    sql = "SELECT * FROM hospital"
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


#listar por id
def listar_por_id(id_hospital):
    conexion = ConexionDB()
    sql = "SELECT * FROM hospital WHERE id_hospital = %s"  # Ajustamos la consulta para buscar por id
    try:
        conexion.cursor.execute(sql, (id_hospital,))  # Pasamos el parámetro id_hospital
        registro = conexion.cursor.fetchone()  # Usamos fetchone() porque esperamos un único resultado
        conexion.cerrar()

        # Si no se encuentra el hospital, retornamos None o un mensaje indicándolo
        if registro:
            return registro
        else:
            return None
    except Exception as e:
        conexion.cerrar()
        titulo = "Error al Listar por ID"
        mensaje = f"No se pudo recuperar el hospital con ID {id_hospital}: {e}"
        messagebox.showerror(titulo, mensaje)
        return None


#actualizar
def editar(hospital, id_hospital):
    conexion = ConexionDB()
    sql = '''
    UPDATE hospital 
    SET nombre = %s, direccion = %s, telefono = %s
    WHERE id_hospital = %s
    '''
    try:
        conexion.cursor.execute(sql, (hospital.nombre, hospital.direccion, hospital.telefono, id_hospital))
        conexion.cerrar()
        titulo = "Edición Exitosa"
        mensaje = "El registro se actualizó correctamente."
        messagebox.showinfo(titulo, mensaje)
    except Exception as e:
        conexion.cerrar()
        titulo = "Error al Editar"
        mensaje = f"No se pudo editar el registro: {e}"
        messagebox.showerror(titulo, mensaje)


#eliminar
def eliminar(id_hospital):
    conexion = ConexionDB()
    sql = "DELETE FROM hospital WHERE id_hospital = %s"
    try:
        conexion.cursor.execute(sql, (id_hospital,))
        conexion.cerrar()
        titulo = "Eliminación Exitosa"
        mensaje = "El registro se eliminó correctamente."
        messagebox.showinfo(titulo, mensaje)
    except Exception as e:
        conexion.cerrar()
        titulo = "Error al Eliminar"
        mensaje = f"No se pudo eliminar el registro: {e}"
        messagebox.showerror(titulo, mensaje)





