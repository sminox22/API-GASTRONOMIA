"""Configuración de la API leída desde variables de entorno (.env)."""
import os
from urllib.parse import quote_plus

from dotenv import load_dotenv

load_dotenv()


def c_variable_obligatoria(c_nombre: str) -> str:
    c_valor = os.getenv(c_nombre)
    if not c_valor:
        raise RuntimeError(f"Falta la variable de entorno obligatoria {c_nombre} (revise el archivo .env)")
    return c_valor


class CConfiguracion:
    """Agrupa los parámetros de conexión y seguridad de la API."""

    def __init__(self) -> None:
        self.c_mongo_host = os.getenv("MONGO_HOST", "localhost")
        self.c_mongo_port = int(os.getenv("MONGO_PORT", "27017"))
        self.c_mongo_db = os.getenv("MONGO_DB", "bd_gastronomia")
        self.c_mongo_usuario = c_variable_obligatoria("MONGO_APP_USER")
        self.c_mongo_password = c_variable_obligatoria("MONGO_APP_PASSWORD")

        self.c_jwt_secreto = c_variable_obligatoria("JWT_SECRET")
        self.c_jwt_algoritmo = os.getenv("JWT_ALGORITHM", "HS256")
        self.c_jwt_minutos_expiracion = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))

        self.c_zona_horaria = os.getenv("ZONA_HORARIA", "America/Bogota")

    @property
    def c_mongo_uri(self) -> str:
        # El usuario de la API se crea en bd_gastronomia, por eso authSource apunta a ella
        return (
            f"mongodb://{quote_plus(self.c_mongo_usuario)}:{quote_plus(self.c_mongo_password)}"
            f"@{self.c_mongo_host}:{self.c_mongo_port}/{self.c_mongo_db}?authSource={self.c_mongo_db}"
        )


c_config = CConfiguracion()
