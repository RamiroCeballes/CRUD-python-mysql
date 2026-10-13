"""
app.py
Interfaz gráfica (Tkinter) del CRUD de alumnos.
Ejecutar con:  python app.py
"""
import tkinter as tk
from tkinter import ttk, messagebox

import mysql.connector
import alumno_dao

# Guarda el id del alumno seleccionado en la tabla (None = ninguno)
id_seleccionado = None


# ---------------------------------------------------------
# Funciones auxiliares
# ---------------------------------------------------------
def leer_formulario():
    """Devuelve un diccionario con los datos escritos en el formulario."""
    return {
        "dni": entry_dni.get().strip(),
        "nombre": entry_nombre.get().strip(),
        "apellido": entry_apellido.get().strip(),
        "email": entry_email.get().strip(),
        "telefono": entry_telefono.get().strip(),
    }


def validar(datos):
    """Controla los datos antes de mandarlos a la base. Devuelve True si están bien."""
    if not datos["dni"] or not datos["nombre"] or not datos["apellido"]:
        messagebox.showwarning("Faltan datos", "DNI, Nombre y Apellido son obligatorios.")
        return False
    if not datos["dni"].isdigit():
        messagebox.showwarning("DNI inválido", "El DNI solo puede contener números.")
        return False
    if datos["email"] and "@" not in datos["email"]:
        messagebox.showwarning("Email inválido", "Revise el email ingresado.")
        return False
    return True


def limpiar_formulario():
    global id_seleccionado
    id_seleccionado = None
    for entry in (entry_dni, entry_nombre, entry_apellido, entry_email, entry_telefono):
        entry.delete(0, tk.END)
    tabla.selection_remove(tabla.selection())
    entry_dni.focus()


def cargar_tabla(filas=None):
    """Borra la tabla y la vuelve a llenar con los datos de la base."""
    for item in tabla.get_children():
        tabla.delete(item)
    try:
        if filas is None:
            filas = alumno_dao.listar()
    except mysql.connector.Error as error:
        messagebox.showerror("Error de base de datos", str(error))
        return
    for fila in filas:
        tabla.insert("", tk.END, values=fila)


# ---------------------------------------------------------
# Operaciones del CRUD (se ejecutan al tocar los botones)
# ---------------------------------------------------------
def guardar():
    datos = leer_formulario()
    if not validar(datos):
        return
    try:
        alumno_dao.insertar(**datos)
        messagebox.showinfo("Listo", "Alumno guardado correctamente.")
        limpiar_formulario()
        cargar_tabla()
    except mysql.connector.IntegrityError:
        messagebox.showerror("Error", "Ya existe un alumno con ese DNI.")
    except mysql.connector.Error as error:
        messagebox.showerror("Error de base de datos", str(error))


def modificar():
    if id_seleccionado is None:
        messagebox.showwarning("Atención", "Seleccione un alumno de la tabla.")
        return
    datos = leer_formulario()
    if not validar(datos):
        return
    try:
        alumno_dao.actualizar(id_seleccionado, **datos)
        messagebox.showinfo("Listo", "Alumno modificado correctamente.")
        limpiar_formulario()
        cargar_tabla()
    except mysql.connector.IntegrityError:
        messagebox.showerror("Error", "Ya existe otro alumno con ese DNI.")
    except mysql.connector.Error as error:
        messagebox.showerror("Error de base de datos", str(error))


def eliminar():
    if id_seleccionado is None:
        messagebox.showwarning("Atención", "Seleccione un alumno de la tabla.")
        return
    if not messagebox.askyesno("Confirmar", "¿Seguro que desea eliminar este alumno?"):
        return
    try:
        alumno_dao.eliminar(id_seleccionado)
        limpiar_formulario()
        cargar_tabla()
    except mysql.connector.Error as error:
        messagebox.showerror("Error de base de datos", str(error))


def buscar():
    texto = entry_buscar.get().strip()
    try:
        cargar_tabla(alumno_dao.buscar(texto))
    except mysql.connector.Error as error:
        messagebox.showerror("Error de base de datos", str(error))


def mostrar_todos():
    entry_buscar.delete(0, tk.END)
    cargar_tabla()


def al_seleccionar(evento):
    """Cuando se hace clic en una fila, pasa sus datos al formulario."""
    global id_seleccionado
    seleccion = tabla.selection()
    if not seleccion:
        return
    valores = tabla.item(seleccion[0], "values")
    id_seleccionado = valores[0]
    entries = (entry_dni, entry_nombre, entry_apellido, entry_email, entry_telefono)
    for entry, valor in zip(entries, valores[1:]):
        entry.delete(0, tk.END)
        entry.insert(0, valor)


# ---------------------------------------------------------
# Ventana principal
# ---------------------------------------------------------
ventana = tk.Tk()
ventana.title("CRUD de Alumnos")
ventana.geometry("820x520")

# --- Formulario ---
marco_form = ttk.LabelFrame(ventana, text="Datos del alumno", padding=10)
marco_form.pack(fill="x", padx=10, pady=10)

ttk.Label(marco_form, text="DNI:").grid(row=0, column=0, sticky="w", pady=3)
entry_dni = ttk.Entry(marco_form, width=30)
entry_dni.grid(row=0, column=1, padx=5)

ttk.Label(marco_form, text="Nombre:").grid(row=1, column=0, sticky="w", pady=3)
entry_nombre = ttk.Entry(marco_form, width=30)
entry_nombre.grid(row=1, column=1, padx=5)

ttk.Label(marco_form, text="Apellido:").grid(row=2, column=0, sticky="w", pady=3)
entry_apellido = ttk.Entry(marco_form, width=30)
entry_apellido.grid(row=2, column=1, padx=5)

ttk.Label(marco_form, text="Email:").grid(row=0, column=2, sticky="w", padx=(20, 0))
entry_email = ttk.Entry(marco_form, width=30)
entry_email.grid(row=0, column=3, padx=5)

ttk.Label(marco_form, text="Teléfono:").grid(row=1, column=2, sticky="w", padx=(20, 0))
entry_telefono = ttk.Entry(marco_form, width=30)
entry_telefono.grid(row=1, column=3, padx=5)

# --- Botones ---
marco_botones = ttk.Frame(ventana)
marco_botones.pack(fill="x", padx=10)

ttk.Button(marco_botones, text="Guardar", command=guardar).pack(side="left", padx=5)
ttk.Button(marco_botones, text="Modificar", command=modificar).pack(side="left", padx=5)
ttk.Button(marco_botones, text="Eliminar", command=eliminar).pack(side="left", padx=5)
ttk.Button(marco_botones, text="Limpiar", command=limpiar_formulario).pack(side="left", padx=5)

# --- Búsqueda ---
ttk.Button(marco_botones, text="Ver todos", command=mostrar_todos).pack(side="right", padx=5)
ttk.Button(marco_botones, text="Buscar", command=buscar).pack(side="right", padx=5)
entry_buscar = ttk.Entry(marco_botones, width=25)
entry_buscar.pack(side="right", padx=5)
entry_buscar.bind("<Return>", lambda evento: buscar())

# --- Tabla (Treeview) ---
marco_tabla = ttk.Frame(ventana)
marco_tabla.pack(fill="both", expand=True, padx=10, pady=10)

columnas = ("id", "dni", "nombre", "apellido", "email", "telefono")
tabla = ttk.Treeview(marco_tabla, columns=columnas, show="headings")

encabezados = {"id": 40, "dni": 90, "nombre": 120, "apellido": 120, "email": 200, "telefono": 110}
for col, ancho in encabezados.items():
    tabla.heading(col, text=col.capitalize())
    tabla.column(col, width=ancho)

scroll = ttk.Scrollbar(marco_tabla, orient="vertical", command=tabla.yview)
tabla.configure(yscrollcommand=scroll.set)
tabla.pack(side="left", fill="both", expand=True)
scroll.pack(side="right", fill="y")

tabla.bind("<<TreeviewSelect>>", al_seleccionar)

# Cargar los datos al abrir la ventana
cargar_tabla()

ventana.mainloop()
