"""Excepciones de negocio y manejadores globales de errores HTTP."""
import logging

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from pymongo.errors import DuplicateKeyError, PyMongoError, ServerSelectionTimeoutError, WriteError

c_log = logging.getLogger("api_gastronomia")


class CErrorNegocio(Exception):
    c_codigo = status.HTTP_400_BAD_REQUEST

    def __init__(self, c_mensaje: str, c_datos: dict | None = None) -> None:
        super().__init__(c_mensaje)
        self.c_mensaje = c_mensaje
        self.c_datos = c_datos or {}


class CSolicitudInvalida(CErrorNegocio):
    c_codigo = status.HTTP_400_BAD_REQUEST


class CNoEncontrado(CErrorNegocio):
    c_codigo = status.HTTP_404_NOT_FOUND


class CConflicto(CErrorNegocio):
    c_codigo = status.HTTP_409_CONFLICT


class CNoAutorizado(CErrorNegocio):
    c_codigo = status.HTTP_401_UNAUTHORIZED


class CProhibido(CErrorNegocio):
    c_codigo = status.HTTP_403_FORBIDDEN


def c_registrar_manejadores(c_app: FastAPI) -> None:
    @c_app.exception_handler(CErrorNegocio)
    async def c_manejar_negocio(_: Request, c_error: CErrorNegocio):
        return JSONResponse(status_code=c_error.c_codigo, content={"detail": c_error.c_mensaje, **c_error.c_datos})

    @c_app.exception_handler(DuplicateKeyError)
    async def c_manejar_duplicado(_: Request, c_error: DuplicateKeyError):
        c_valores = (c_error.details or {}).get("keyValue", {})
        c_texto = ", ".join(f"{k}={v}" for k, v in c_valores.items()) or "clave única"
        return JSONResponse(status_code=409, content={"detail": f"Ya existe un registro con {c_texto}"})

    @c_app.exception_handler(WriteError)
    async def c_manejar_escritura(_: Request, c_error: WriteError):
        if c_error.code == 121:  # DocumentValidationFailure ($jsonSchema)
            return JSONResponse(status_code=400, content={"detail": "El documento no cumple la validación de la colección"})
        c_log.exception("Error de escritura en MongoDB")
        return JSONResponse(status_code=500, content={"detail": "Error al escribir en la base de datos"})

    @c_app.exception_handler(ServerSelectionTimeoutError)
    async def c_manejar_sin_conexion(_: Request, c_error: ServerSelectionTimeoutError):
        c_log.error("No hay conexión con MongoDB: %s", c_error)
        return JSONResponse(status_code=500, content={"detail": "No fue posible conectarse a la base de datos"})

    @c_app.exception_handler(PyMongoError)
    async def c_manejar_mongo(_: Request, c_error: PyMongoError):
        c_log.exception("Error de MongoDB")
        return JSONResponse(status_code=500, content={"detail": "Error interno de la base de datos"})

    @c_app.exception_handler(Exception)
    async def c_manejar_general(_: Request, c_error: Exception):
        c_log.exception("Error no controlado")
        return JSONResponse(status_code=500, content={"detail": "Error interno del servidor"})
