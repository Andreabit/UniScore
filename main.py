import tkinter as tk
from tkinter import messagebox
import json
import os
import random

# Archivos para usuarios y datos
USERS_FILE = "usuarios.json"
USER_DATA_DIR = "data/usuarios"
DATA_FILE = "notas_estudiante.json"

# Crear directorio para usuarios si no existe
if not os.path.exists(USER_DATA_DIR):
    os.makedirs(USER_DATA_DIR)

# Función para cargar usuarios
def cargar_usuarios():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as file:
            return json.load(file)
    return {}

# Función para guardar usuarios
def guardar_usuarios(usuarios):
    with open(USERS_FILE, "w") as file:
        json.dump(usuarios, file, indent=4)

def guardar_datos(datos):
    with open(DATA_FILE, "w") as file:
        json.dump(datos, file, indent=4)

# Clase para la pantalla de inicio de sesión
class LoginScreen:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.usuarios = cargar_usuarios()

        self.frame_login = tk.Frame(root, bg="#e0f7fa")
        self.frame_login.pack(fill="both", expand=True)
        self.mostrar_pantalla_login()

    def limpiar_frame(self):
        for widget in self.frame_login.winfo_children():
            widget.destroy()

    def mostrar_pantalla_login(self):
        self.limpiar_frame()
        tk.Label(self.frame_login, text="Inicio de Sesión", bg="#e0f7fa", font=("Arial", 18, "bold")).pack(pady=20)
        tk.Label(self.frame_login, text="Usuario", bg="#e0f7fa").pack(pady=5)
        self.entry_usuario = tk.Entry(self.frame_login)
        self.entry_usuario.pack(pady=5)

        tk.Label(self.frame_login, text="Contraseña", bg="#38EB5C").pack(pady=5)
        self.entry_contrasena = tk.Entry(self.frame_login, show="*")
        self.entry_contrasena.pack(pady=5)

        tk.Button(self.frame_login, text="Iniciar Sesión", bg="#00796b", fg="white",
                  command=self.iniciar_sesion).pack(pady=10)
        tk.Button(self.frame_login, text="Registrarse", bg="#004d40", fg="white",
                  command=self.mostrar_pantalla_registro).pack(pady=10)

    def mostrar_pantalla_registro(self):
        self.limpiar_frame()
        tk.Label(self.frame_login, text="Registrar Usuario", bg="#e0f7fa", font=("Arial", 18, "bold")).pack(pady=20)

        tk.Label(self.frame_login, text="Usuario", bg="#e0f7fa").pack(pady=5)
        self.entry_usuario = tk.Entry(self.frame_login)
        self.entry_usuario.pack(pady=5)

        tk.Label(self.frame_login, text="Contraseña", bg="#e0f7fa").pack(pady=5)
        self.entry_contrasena = tk.Entry(self.frame_login, show="*")
        self.entry_contrasena.pack(pady=5)

        tk.Button(self.frame_login, text="Registrar", bg="#00796b", fg="white",
                  command=self.registrar_usuario).pack(pady=10)
        tk.Button(self.frame_login, text="Volver", bg="#004d40", fg="white",
                  command=self.mostrar_pantalla_login).pack(pady=10)

    def registrar_usuario(self):
        usuario = self.entry_usuario.get().strip()
        contrasena = self.entry_contrasena.get().strip()

        if not usuario or not contrasena:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        if usuario in self.usuarios:
            messagebox.showerror("Error", "El usuario ya existe")
            return

        self.usuarios[usuario] = contrasena
        guardar_usuarios(self.usuarios)

        archivo_usuario = os.path.join(USER_DATA_DIR, f"{usuario}.json")
        with open(archivo_usuario, "w") as file:
            json.dump({}, file)

        messagebox.showinfo("Éxito", "Usuario registrado exitosamente")
        self.mostrar_pantalla_login()
