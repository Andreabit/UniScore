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

    def iniciar_sesion(self):
        usuario = self.entry_usuario.get().strip()
        contrasena = self.entry_contrasena.get().strip()

        if usuario not in self.usuarios or self.usuarios[usuario] != contrasena:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
            return

        self.app.usuario_actual = usuario
        self.app.cargar_datos_usuario()
        self.frame_login.destroy()
        self.app.iniciar_aplicacion()

# Clase principal de la aplicación
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Control de Notas Universitarias")
        self.usuario_actual = None
        self.datos = {}

        self.login_screen = LoginScreen(root, self)

    def cargar_datos_usuario(self):
        archivo_usuario = os.path.join(USER_DATA_DIR, f"{self.usuario_actual}.json")
        if os.path.exists(archivo_usuario):
            with open(archivo_usuario, "r") as file:
                self.datos = json.load(file)
        else:
            self.datos = {}

    def guardar_datos_usuario(self):
        archivo_usuario = os.path.join(USER_DATA_DIR, f"{self.usuario_actual}.json")
        with open(archivo_usuario, "w") as file:
            json.dump(self.datos, file, indent=4)

    def iniciar_aplicacion(self):
        self.frame_principal = tk.Frame(self.root, bg="white")
        self.frame_principal.pack(fill="both", expand=True)
        self.crear_pantalla_principal()

    def limpiar_frame(self):
        for widget in self.frame_principal.winfo_children():
            widget.destroy()

    def crear_pantalla_principal(self):
        self.limpiar_frame()  # Limpia el marco principal.

        # Crear la franja superior con mayor ancho y el mensaje de bienvenida dentro de la franja
        color_franja = "#004d40"  # Color de la franja superior.
        franja = tk.Frame(self.frame_principal, bg=color_franja, height=60)  # Crear la franja como un Frame.
        franja.pack(fill="x")  # Hacer que la franja ocupe todo el ancho de la ventana.

        # Agregar el texto de bienvenida dentro de la franja.
        tk.Label(
            franja, text=f"Bienvenido {self.usuario_actual} al Sistema de UniScore",
            bg=color_franja, fg="white", font=("Arial", 18, "bold")
        ).pack(pady=10)

        # Crear un Frame para la cuadrícula con fondo blanco
        grid_frame = tk.Frame(self.frame_principal, bg="white")
        grid_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Paleta de colores claros
        colores_claros = [
            "#FFCDD2", "#F8BBD0", "#E1BEE7", "#D1C4E9", "#C5CAE9",
            "#BBDEFB", "#B3E5FC", "#B2EBF2", "#B2DFDB", "#C8E6C9",
            "#DCEDC8", "#F0F4C3", "#FFECB3", "#FFE0B2", "#FFCCBC"
        ]

        # Crear botones en la cuadrícula (3 filas x 4 columnas)
        for fila in range(3):
            for columna in range(4):
                if fila == 0 and columna == 0:
                    # Botón "Añadir Materia" en la primera celda
                    tk.Button(
                        grid_frame, text="Añadir Materia", bg="#1b5e20", fg="white",
                        font=("Arial", 14, "bold"), width=20, height=8,
                        command=self.anadir_materia
                    ).grid(row=fila, column=columna, padx=10, pady=10, sticky="nsew")
                else:
                    # Obtener la materia correspondiente
                    indice = (fila * 4 + columna) - 1  # Restar 1 por "Añadir Materia"
                    if indice < len(self.datos):
                        materia = list(self.datos.keys())[indice]
                        datos = self.datos[materia]
                        color_aleatorio = random.choice(colores_claros)
                        tk.Button(
                            grid_frame, text=f"{materia} (Semestre {datos['semestre']})",
                            bg=color_aleatorio, fg="black", font=("Arial", 14, "bold"),
                            width=20, height=8,
                            command=lambda m=materia: self.ver_materia(m)
                        ).grid(row=fila, column=columna, padx=10, pady=10, sticky="nsew")

        # Configurar columnas y filas para que sean proporcionales
        for i in range(4):  # 4 columnas
            grid_frame.columnconfigure(i, weight=1)
        for i in range(3):  # 3 filas
            grid_frame.rowconfigure(i, weight=1)

        # Botón Salir al final
        tk.Button(
            self.frame_principal, text="Salir", bg="#b71c1c", fg="white",
            font=("Arial", 14, "bold"), command=self.salir_aplicacion
        ).pack(pady=20)


    def anadir_materia(self):
        self.limpiar_frame()  # Limpia el marco principal.
        def guardar_materia():
            nombre = entry_nombre.get().strip()
            semestre = entry_semestre.get().strip()
            examen = entry_examen.get().strip()
            practicas = entry_practicas.get().strip()

            if not nombre or not semestre or not examen or not practicas:
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
            
            if nombre in self.datos:
                messagebox.showerror("Error", "La materia ya existe")
                return

            self.datos[nombre] = {
                "semestre": semestre,
                "peso_examen": int(examen),
                "peso_practicas": int(practicas),
                "competencias": [],                      
            }

            self.guardar_datos_usuario()
            self.crear_pantalla_principal()

        tk.Label(self.frame_principal, text="Nombre de la materia:").pack()
        entry_nombre = tk.Entry(self.frame_principal)
        entry_nombre.pack()

        tk.Label(self.frame_principal, text="Semestre:").pack()
        entry_semestre = tk.Entry(self.frame_principal)
        entry_semestre.pack()

        tk.Label(self.frame_principal, text="Peso (%) Examen:").pack()
        entry_examen = tk.Entry(self.frame_principal)
        entry_examen.pack()

        tk.Label(self.frame_principal, text="Peso (%) Prácticas:").pack()
        entry_practicas = tk.Entry(self.frame_principal)
        entry_practicas.pack()

        tk.Button(self.frame_principal, text="Guardar", command=guardar_materia).pack(pady=10)
        tk.Button(self.frame_principal, text="Volver", command=self.crear_pantalla_principal).pack(pady=10)
