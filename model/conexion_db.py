import psycopg2
from psycopg2 import sql

class ConexionDB:
    def __init__(self):
        self.config = {
            'dbname': 'agenda2',
            'user': 'postgres',
            'password': 'postgres',
            'host': 'localhost',
            'port': '5432'
        }
        self.conexion = psycopg2.connect(**self.config)
        self.cursor = self.conexion.cursor()

    def cerrar(self):
        self.conexion.commit()
        self.cursor.close()
        self.conexion.close()
