from pydantic import Field

from app.models.c_enums import CEstado
from app.schemas.c_comun_schemas import CEsquemaBase


class CCategoriaCrear(CEsquemaBase):
    nombre: str = Field(min_length=2, max_length=60, examples=["Comidas típicas"])
    descripcion: str | None = Field(None, max_length=200, examples=["Platos típicos del Huila"])
    estado: CEstado = CEstado.ACTIVO


class CCategoriaActualizar(CEsquemaBase):
    nombre: str | None = Field(None, min_length=2, max_length=60)
    descripcion: str | None = Field(None, max_length=200)
    estado: CEstado | None = None


class CCategoriaRespuesta(CCategoriaCrear):
    id_categoria: int
