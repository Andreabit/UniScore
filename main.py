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


    def ver_materia(self, materia):
        def anadir_competencia():
            self.limpiar_frame()

            def definir_tareas():
                try:
                    cantidad_tareas = int(entry_tareas.get())
                    if cantidad_tareas <= 0:
                        raise ValueError
                except ValueError:
                    messagebox.showerror("Error", "Ingresa un número válido de tareas")
                    return
                self.registrar_notas_competencia(materia, cantidad_tareas)

            tk.Label(self.frame_principal, text="Cantidad de tareas:").pack()
            entry_tareas = tk.Entry(self.frame_principal)
            entry_tareas.pack()

            tk.Button(self.frame_principal, text="Siguiente", command=definir_tareas).pack(pady=10)
            tk.Button(self.frame_principal, text="Volver", command=lambda: self.ver_materia(materia)).pack(pady=10)

        def editar_competencia(idx):
            self.editar_notas_competencia(materia, idx)

        def eliminar_competencia(idx):
            del self.datos[materia]["competencias"][idx]
            guardar_datos(self.datos)
            self.ver_materia(materia)

        self.limpiar_frame()
        tk.Label(self.frame_principal, text=f"Materia: {materia}").pack()
        tk.Label(self.frame_principal, text=f"Semestre: {self.datos[materia]['semestre']}").pack()
        tk.Label(self.frame_principal, text=f"Peso Examen: {self.datos[materia]['peso_examen']}%").pack()
        tk.Label(self.frame_principal, text=f"Peso Prácticas: {self.datos[materia]['peso_practicas']}%").pack()

        tk.Button(self.frame_principal, text="+ Añadir Competencia", command=anadir_competencia).pack(pady=10)

        promedio_materia = 0
        if self.datos[materia]["competencias"]:
            promedio_materia = sum(
                c["promedio_final"] for c in self.datos[materia]["competencias"]
            ) / len(self.datos[materia]["competencias"])

        for idx, comp in enumerate(self.datos[materia]["competencias"], start=1):
            frame_competencia = tk.Frame(self.frame_principal)
            frame_competencia.pack(fill="x", pady=5)

            tk.Label(frame_competencia, text=f"Competencia {idx}: Promedio Final = {comp['promedio_final']:.2f}").pack(side="left")
            tk.Button(frame_competencia, text="Editar", command=lambda idx=idx-1: editar_competencia(idx)).pack(side="right")
            tk.Button(frame_competencia, text="Eliminar", command=lambda idx=idx-1: eliminar_competencia(idx)).pack(side="right")

        tk.Label(self.frame_principal, text=f"Promedio de la materia: {promedio_materia:.2f}").pack(pady=10)
        tk.Button(self.frame_principal, text="Volver", command=self.crear_pantalla_principal).pack(pady=10)

    def registrar_notas_competencia(self, materia, cantidad_tareas):
        def guardar_notas():
            try:
                nota_examen = float(entry_examen.get())
                if nota_examen < 0 or nota_examen > 100:
                    raise ValueError

                notas_tareas = []
                for i in range(cantidad_tareas):
                    nota_tarea = float(entries_tareas[i].get())
                    if nota_tarea < 0 or nota_tarea > 100:
                        raise ValueError
                    notas_tareas.append(nota_tarea)

                promedio_practicas = sum(notas_tareas) / len(notas_tareas)
                promedio_final = (
                    (nota_examen * self.datos[materia]["peso_examen"] / 100)
                    + (promedio_practicas * self.datos[materia]["peso_practicas"] / 100)
                )

                self.datos[materia]["competencias"].append({
                    "nota_examen": nota_examen,
                    "notas_tareas": notas_tareas,
                    "promedio_final": promedio_final,
                })
                guardar_datos(self.datos)
                self.ver_materia(materia)

            except ValueError:
                messagebox.showerror("Error", "Ingresa notas válidas entre 0 y 100")

        self.limpiar_frame()
        tk.Label(self.frame_principal, text="Ingresa la nota del examen:").pack()
        entry_examen = tk.Entry(self.frame_principal)
        entry_examen.pack()

        entries_tareas = []
        for i in range(cantidad_tareas):
            tk.Label(self.frame_principal, text=f"Nota de la tarea {i + 1}:").pack()
            entry = tk.Entry(self.frame_principal)
            entry.pack()
            entries_tareas.append(entry)

        tk.Button(self.frame_principal, text="Guardar", command=guardar_notas).pack(pady=10)
        tk.Button(self.frame_principal, text="Volver", command=lambda: self.ver_materia(materia)).pack(pady=10)

    def editar_notas_competencia(self, materia, idx):
        competencia = self.datos[materia]["competencias"][idx]
        cantidad_tareas = len(competencia["notas_tareas"])

        def guardar_cambios():
            try:
                nota_examen = float(entry_examen.get())
                if nota_examen < 0 or nota_examen > 100:
                    raise ValueError

                notas_tareas = []
                for i in range(cantidad_tareas):
                    nota_tarea = float(entries_tareas[i].get())
                    if nota_tarea < 0 or nota_tarea > 100:
                        raise ValueError
                    notas_tareas.append(nota_tarea)

                promedio_practicas = sum(notas_tareas) / len(notas_tareas)
                promedio_final = (
                    (nota_examen * self.datos[materia]["peso_examen"] / 100)
                    + (promedio_practicas * self.datos[materia]["peso_practicas"] / 100)
                )

                self.datos[materia]["competencias"][idx] = {
                    "nota_examen": nota_examen,
                    "notas_tareas": notas_tareas,
                    "promedio_final": promedio_final,
                }
                guardar_datos(self.datos)
                self.ver_materia(materia)

            except ValueError:
                messagebox.showerror("Error", "Ingresa notas válidas entre 0 y 100")

        self.limpiar_frame()
        tk.Label(self.frame_principal, text="Editar nota del examen:").pack()
        entry_examen = tk.Entry(self.frame_principal)
        entry_examen.insert(0, competencia["nota_examen"])
        entry_examen.pack()

        entries_tareas = []
        for i in range(cantidad_tareas):
            tk.Label(self.frame_principal, text=f"Editar nota de la tarea {i + 1}:").pack()
            entry = tk.Entry(self.frame_principal)
            entry.insert(0, competencia["notas_tareas"][i])
            entry.pack()
            entries_tareas.append(entry)

        tk.Button(self.frame_principal, text="Guardar cambios", command=guardar_cambios).pack(pady=10)
        tk.Button(self.frame_principal, text="Volver", command=lambda: self.ver_materia(materia)).pack(pady=10)


# Inicializar aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
