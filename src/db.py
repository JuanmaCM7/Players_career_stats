# src/db.py — Módulo para conexión con base de datos MySQL usando SQLAlchemy y dotenv

from sqlalchemy import create_engine  # Motor de conexión de SQLAlchemy
from dotenv import load_dotenv       # Cargar variables de entorno desde un archivo .env
import os                            # Acceso a variables de entorno del sistema

# Cargar las variables definidas en el archivo .env (como usuario, contraseña, etc.)
load_dotenv()

def get_engine():
    """
    Devuelve un engine SQLAlchemy configurado para conectarse a una base de datos MySQL.
    Usa variables de entorno para ocultar información sensible (usuario, contraseña...).
    """

    # Obtener valores desde las variables de entorno
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    database = os.getenv("DB_NAME")
    port = os.getenv("DB_PORT", 3306)  # Usa el puerto 3306 por defecto si no se especifica

    # Crear cadena de conexión con formato compatible con MySQL y PyMySQL
    connection_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

    # Crear engine de SQLAlchemy usando la cadena de conexión
    engine = create_engine(connection_string)

    # Devolver el engine para que pueda usarse en otras partes del proyecto
    return engine
