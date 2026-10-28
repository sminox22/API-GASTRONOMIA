"""Funciones de apoyo reutilizadas por los servicios."""
from pydantic import BaseModel

from app.core.c_excepciones import CNoEncontrado, CSolicitudInvalida


def c_requerir(c_documento: dict | None, c_mensaje: str) -> dict:
    if c_documento is None:
        raise CNoEncontrado(c_mensaje)
    return c_documento


def c_cambios(c_modelo: BaseModel) -> dict:
    """Solo los campos enviados en el PUT (los omitidos conservan su valor)."""
    c_datos = c_modelo.model_dump(exclude_unset=True)
    if not c_datos:
        raise CSolicitudInvalida("No se enviaron campos para actualizar")
    return c_datos


def c_resultado(c_mensaje: str, c_logico: bool) -> dict:
    return {"mensaje": c_mensaje, "borrado_logico": c_logico}
