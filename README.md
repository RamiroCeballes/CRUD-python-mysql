# CRUD de Alumnos — Tkinter + MySQL

Aplicación de escritorio para **C**rear, **L**eer (Read), **A**ctualizar (Update) y **E**liminar (Delete) alumnos.

## Estructura

| Archivo          | Responsabilidad                                   |
|------------------|---------------------------------------------------|
| `script.sql`     | Crea la base `escuela` y la tabla `alumnos`       |
| `conexion.py`    | Datos de conexión a MySQL                         |
| `alumno_dao.py`  | Las consultas SQL (INSERT, SELECT, UPDATE, DELETE)|
| `app.py`         | La ventana Tkinter y los botones                  |

## Pasos para ejecutarlo

Todos los comandos se ejecutan **dentro de la carpeta `crud_alumnos`** (`cd crud_alumnos`).

1. Crear un entorno virtual e instalar el conector:
   - Mac / Linux:
     ```
     python3 -m venv .venv
     source .venv/bin/activate
     pip install mysql-connector-python
     ```
   - Windows:
     ```
     python -m venv .venv
     .venv\Scripts\activate
     pip install mysql-connector-python
     ```
2. Crear la base de datos (o abrir `script.sql` en MySQL Workbench y ejecutarlo):
   ```
   mysql -u root -p < script.sql
   ```
3. Poner su contraseña de MySQL en `conexion.py`.
4. Ejecutar (con el entorno virtual activado):
   ```
   python app.py
   ```

## Cómo se usa

- **Guardar**: completar el formulario y presionar *Guardar*.
- **Modificar**: hacer clic en una fila, cambiar los datos y presionar *Modificar*.
- **Eliminar**: hacer clic en una fila y presionar *Eliminar*.
- **Buscar**: escribir DNI, nombre o apellido y presionar *Buscar* (o Enter).

## Para pensar 🤔

1. ¿Por qué usamos `%s` en las consultas en lugar de armar el texto con `+` o f-strings?
2. ¿Qué pasa si intentan guardar dos alumnos con el mismo DNI? ¿Dónde se controla eso?
3. ¿Por qué hace falta `conexion.commit()` en INSERT/UPDATE/DELETE pero no en SELECT?
4. Desafío: agregar un campo `fecha_nacimiento` a la tabla y al formulario.
