import tkinter as tk
from tkinter import messagebox
import json
import subprocess

def agregar_busqueda():
    query = entry_query.get()
    scroll_post = entry_scroll_post.get()
    scroll_comment = entry_scroll_comment.get()
    
    if query and scroll_post and scroll_comment:
        busquedas.append({
            "query": query,
            "scroll_post": scroll_post,
            "scroll_comment": scroll_comment
        })
        
        entry_query.delete(0, tk.END)
        entry_scroll_post.delete(0, tk.END)
        entry_scroll_comment.delete(0, tk.END)
        actualizar_lista_busquedas()
    else:
        messagebox.showwarning("Campos incompletos", "Por favor completa todos los campos.")

def borrar_busqueda():
    try:
        selected_index = lista_busquedas.curselection()[0]
        busquedas.pop(selected_index)
        actualizar_lista_busquedas()
    except IndexError:
        messagebox.showwarning("Selección inválida", "Por favor selecciona una búsqueda para borrar.")

def actualizar_lista_busquedas():
    lista_busquedas.delete(0, tk.END)
    for busqueda in busquedas:
        lista_busquedas.insert(tk.END, f"Query: {busqueda['query']}, Scroll Post: {busqueda['scroll_post']}, Scroll Comment: {busqueda['scroll_comment']}")

def guardar_config():
    config = {
        "usuario": entry_usuario.get(),
        "correo": entry_correo.get(),
        "contraseña": entry_contraseña.get(),
        "busquedas": busquedas
    }
    
    with open("config.json", "w") as file:
        json.dump(config, file, indent=4)
    
    messagebox.showinfo("Guardado", "La configuración ha sido guardada exitosamente.")

def ejecutar_script(script_name):
    try:
        subprocess.run(["python", script_name], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error al ejecutar {script_name}: {e}")
    except FileNotFoundError:
        messagebox.showerror("Archivo no encontrado", f"El archivo {script_name} no existe.")

# Ventana principal
root = tk.Tk()
root.title("Configuración de Búsquedas")

# Entradas de usuario
tk.Label(root, text="Usuario").grid(row=0, column=0)
entry_usuario = tk.Entry(root)
entry_usuario.grid(row=0, column=1)

tk.Label(root, text="Correo").grid(row=1, column=0)
entry_correo = tk.Entry(root)
entry_correo.grid(row=1, column=1)

tk.Label(root, text="Contraseña").grid(row=2, column=0)
entry_contraseña = tk.Entry(root, show="*")
entry_contraseña.grid(row=2, column=1)

# Entradas para busquedas
tk.Label(root, text="Busqueda").grid(row=3, column=0)
entry_query = tk.Entry(root)
entry_query.grid(row=3, column=1)

tk.Label(root, text="Scroll Post").grid(row=4, column=0)
entry_scroll_post = tk.Entry(root)
entry_scroll_post.grid(row=4, column=1)

tk.Label(root, text="Scroll Comment").grid(row=5, column=0)
entry_scroll_comment = tk.Entry(root)
entry_scroll_comment.grid(row=5, column=1)

# Botón para agregar búsqueda
btn_agregar = tk.Button(root, text="Agregar Búsqueda", command=agregar_busqueda)
btn_agregar.grid(row=6, column=0, columnspan=2)

# Botón para borrar búsqueda
btn_borrar = tk.Button(root, text="Borrar Búsqueda", command=borrar_busqueda)
btn_borrar.grid(row=7, column=0, columnspan=2)

# Lista de busquedas
tk.Label(root, text="Lista de Búsquedas").grid(row=8, column=0, columnspan=2)
lista_busquedas = tk.Listbox(root, width=50, height=10)
lista_busquedas.grid(row=9, column=0, columnspan=2)

# Botón para guardar configuración
btn_guardar = tk.Button(root, text="Guardar Configuración", command=guardar_config)
btn_guardar.grid(row=10, column=0, columnspan=2)

# Botones para ejecutar los scripts
btn_main = tk.Button(root, text="Ejecutar main.py", command=lambda: ejecutar_script("main.py"))
btn_main.grid(row=11, column=0)

btn_users = tk.Button(root, text="Ejecutar users.py", command=lambda: ejecutar_script("users.py"))
btn_users.grid(row=11, column=1)

# Inicializar lista de busquedas
busquedas = []

# Ejecutar la interfaz
root.mainloop()
