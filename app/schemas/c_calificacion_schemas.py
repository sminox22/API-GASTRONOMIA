from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.c_comun_schemas import CEsquemaBase


class CCalificacionProductoCrear(CEsquemaBase):
    id_producto: int = Field(gt=0, examples=[1])
    calificacion: int = Field(ge=1, le=5, examples=[5])


class CCalificacionCrear(CEsquemaBase):
    """El cliente y el nombre de cada producto se toman del pedido."""
    id_pedido: int = Field(gt=0, examples=[12])
    calificacion_servicio: int = Field(ge=1, le=5, examples=[5])
    comentario: str | None = Field(None, max_length=500, examples=["Excelente atención y buen sabor"])
    productos: list[CCalificacionProductoCrear] = []


class CCalificacionActualizar(CEsquemaBase):
    calificacion_servicio: int | None = Field(None, ge=1, le=5)
    comentario: str | None = Field(None, max_length=500)
    productos: list[CCalificacionProductoCrear] | None = None


class CCalificacionProductoRespuesta(BaseModel):
    id_producto: int
    nombre: str | None = None
    calificacion: int


class CCalificacionRespuesta(BaseModel):
    id_calificacion: int
    id_pedido: int
    id_cliente: int
    fecha: datetime
    calificacion_servicio: int
    comentario: str | None = None
    productos: list[CCalificacionProductoRespuesta]


class CCalificacionDeProducto(BaseModel):
    id_calificacion: int
    id_pedido: int
    id_cliente: int
    fecha: datetime
    calificacion: int
    comentario: str | None = None


class CCalificacionesProductoRespuesta(BaseModel):
    id_producto: int
    nombre: str | None = None
    total_calificaciones: int
    promedio: float | None
    calificaciones: list[CCalificacionDeProducto]
