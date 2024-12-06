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
