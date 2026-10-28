"""Conexión única (pool) a MongoDB con el usuario de privilegios mínimos."""
from pymongo import MongoClient
from pymongo.database import Database

from app.core.c_config import c_config
from app.core.c_utilidades import C_ZONA

_c_cliente: MongoClient | None = None


def c_obtener_cliente() -> MongoClient:
    global _c_cliente
    if _c_cliente is None:
        # tz_aware + tzinfo: las fechas se guardan en UTC y se devuelven en hora de Bogotá
        _c_cliente = MongoClient(
            c_config.c_mongo_uri,
            tz_aware=True,
            tzinfo=C_ZONA,
            serverSelectionTimeoutMS=5000,
            appname="c_api_gastronomia",
        )
    return _c_cliente


def c_obtener_bd() -> Database:
    return c_obtener_cliente()[c_config.c_mongo_db]


def c_verificar_conexion() -> bool:
    try:
        c_obtener_bd().command("ping")
        return True
    except Exception:
        return False


def c_cerrar_conexion() -> None:
    global _c_cliente
    if _c_cliente is not None:
        _c_cliente.close()
        _c_cliente = None
