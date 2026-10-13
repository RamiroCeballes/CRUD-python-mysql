"""
alumno_dao.py
DAO = Data Access Object (Objeto de Acceso a Datos).
Acá están las 4 operaciones del CRUD sobre la tabla 'alumnos':
    C - Create  -> insertar()
    R - Read    -> listar() / buscar()
    U - Update  -> actualizar()
    D - Delete  -> eliminar()

IMPORTANTE: siempre usamos %s y pasamos los valores aparte.
Nunca armar la consulta concatenando strings (evita la Inyección SQL).
"""
from conexion import conectar


def insertar(dni, nombre, apellido, email, telefono):
    conexion = conectar()
    cursor = conexion.cursor()
    sql = """INSERT INTO alumnos (dni, nombre, apellido, email, telefono)
             VALUES (%s, %s, %s, %s, %s)"""
    cursor.execute(sql, (dni, nombre, apellido, email, telefono))
    conexion.commit()          # confirma los cambios en la base
    cursor.close()
    conexion.close()


def listar():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, dni, nombre, apellido, email, telefono FROM alumnos ORDER BY apellido")
    filas = cursor.fetchall()  # lista de tuplas
    cursor.close()
    conexion.close()
    return filas


def buscar(texto):
    """Busca por DNI, nombre o apellido (coincidencia parcial)."""
    conexion = conectar()
    cursor = conexion.cursor()
    sql = """SELECT id, dni, nombre, apellido, email, telefono FROM alumnos
             WHERE dni LIKE %s OR nombre LIKE %s OR apellido LIKE %s
             ORDER BY apellido"""
    patron = f"%{texto}%"
    cursor.execute(sql, (patron, patron, patron))
    filas = cursor.fetchall()
    cursor.close()
    conexion.close()
    return filas


def actualizar(id_alumno, dni, nombre, apellido, email, telefono):
    conexion = conectar()
    cursor = conexion.cursor()
    sql = """UPDATE alumnos
             SET dni = %s, nombre = %s, apellido = %s, email = %s, telefono = %s
             WHERE id = %s"""
    cursor.execute(sql, (dni, nombre, apellido, email, telefono, id_alumno))
    conexion.commit()
    cursor.close()
    conexion.close()


def eliminar(id_alumno):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM alumnos WHERE id = %s", (id_alumno,))
    conexion.commit()
    cursor.close()
    conexion.close()
