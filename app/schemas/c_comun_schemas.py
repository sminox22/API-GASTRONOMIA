"""Esquemas compartidos y respuestas de error para la documentación OpenAPI."""
from datetime import date
from typing import Annotated

from pydantic import BaseModel, BeforeValidator, ConfigDict

from app.core.c_utilidades import c_a_fecha


class CEsquemaBase(BaseModel):
    # Los Enum se guardan en MongoDB como texto
    model_config = ConfigDict(use_enum_values=True, str_strip_whitespace=True)


# Fecha guardada como datetime en MongoDB y expuesta como YYYY-MM-DD
CFecha = Annotated[date, BeforeValidator(c_a_fecha)]


class CMensaje(BaseModel):
    mensaje: str


class CResultadoEliminacion(BaseModel):
    mensaje: str
    borrado_logico: bool


class CError(BaseModel):
    detail: str


C_RESP_AUTH = {
    401: {"model": CError, "description": "Token ausente, inválido o expirado"},
    403: {"model": CError, "description": "El rol del usuario no tiene permiso"},
}
C_RESP_404 = {404: {"model": CError, "description": "Recurso no encontrado"}}
C_RESP_409 = {409: {"model": CError, "description": "Conflicto con el estado actual o un dato único"}}
C_RESP_400 = {400: {"model": CError, "description": "Solicitud inválida"}}
