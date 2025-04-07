# src/db.py

from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()  # Cargar variables de entorno

def get_engine():
    """Devuelve un engine SQLAlchemy configurado con pymysql y dotenv"""
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    database = os.getenv("DB_NAME")
    port = os.getenv("DB_PORT", 3306)

    connection_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    engine = create_engine(connection_string)
    return engine
