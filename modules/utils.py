import os
import json

USUARIOS_PATH = "data/usuarios.json"
MATERIAS_PATH = "data/materias.json"

# Crear carpeta y archivo de usuarios si no existen
def setup_data():
    os.makedirs(os.path.dirname(USUARIOS_PATH), exist_ok=True)
    if not os.path.exists(USUARIOS_PATH):
        with open(USUARIOS_PATH, 'w') as f:
            json.dump({}, f)

# Crear carpeta y archivo de materias si no existen
def setup_materias():
    os.makedirs(os.path.dirname(MATERIAS_PATH), exist_ok=True)
    if not os.path.exists(MATERIAS_PATH):
        with open(MATERIAS_PATH, 'w') as f:
            json.dump({}, f)

# Función para obtener los datos de usuarios
def cargar_datos(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Función para guardar datos en un archivo JSON
def guardar_datos(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

# Función para obtener materias de un usuario
def obtener_materias(usuario):
    materias = cargar_datos(MATERIAS_PATH)
    return materias.get(usuario, [])

# Función para agregar una materia a un usuario
def agregar_materia(usuario, datos_materia):
    materias = cargar_datos(MATERIAS_PATH)
    if usuario not in materias:
        materias[usuario] = []
    materias[usuario].append(datos_materia)
    guardar_datos(MATERIAS_PATH, materias)

# Función para eliminar una materia de un usuario
def eliminar_materia(usuario, materia):
    materias = cargar_datos(MATERIAS_PATH)
    if usuario in materias:
        materias[usuario] = [m for m in materias[usuario] if m['nombre'] != materia]
        guardar_datos(MATERIAS_PATH, materias)
