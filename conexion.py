"""
conexion.py
Se encarga ÚNICAMENTE de conectarse a la base de datos MySQL.
Si cambian el usuario o la contraseña, solo se modifica este archivo.
"""
import mysql.connector

# Datos de conexión: cada alumno pone los de su propia instalación de MySQL
CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Qwerty123!",       # <-- poner aquí su contraseña de MySQL
    "database": "escuela",
}


def conectar():
    """Devuelve una conexión abierta a la base de datos."""
    return mysql.connector.connect(**CONFIG)
