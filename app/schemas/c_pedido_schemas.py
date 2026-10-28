from datetime import datetime

from pydantic import BaseModel, Field

from app.models.c_enums import CEstadoPedido, CTipoPedido
from app.schemas.c_comun_schemas import CEsquemaBase


class CDetallePedidoCrear(CEsquemaBase):
    """El cliente solo envía producto y cantidad: precio y subtotal los calcula la API (RN01)."""
    id_producto: int = Field(gt=0, examples=[1])
    cantidad: int = Field(gt=0, le=1000, examples=[2])


class CPedidoCrear(CEsquemaBase):
    id_cliente: int = Field(gt=0, examples=[1])
    tipo_pedido: CTipoPedido = Field(examples=["MESA"])
    observaciones: str | None = Field(None, max_length=300, examples=["Sin cebolla"])
    detalle: list[CDetallePedidoCrear] = Field(min_length=1)


class CPedidoActualizar(CEsquemaBase):
    id_cliente: int | None = Field(None, gt=0)
    tipo_pedido: CTipoPedido | None = None
    observaciones: str | None = Field(None, max_length=300)
    detalle: list[CDetallePedidoCrear] | None = Field(None, min_length=1)


class CPedidoCambioEstado(CEsquemaBase):
    estado: CEstadoPedido = Field(examples=["EN_PREPARACION"])


class CDetallePedidoRespuesta(BaseModel):
    id_producto: int
    nombre_producto: str | None = None
    cantidad: int
    precio_unitario: float
    subtotal: float


class CPedidoRespuesta(BaseModel):
    id_pedido: int
    fecha_pedido: datetime
    id_cliente: int
    id_usuario: int
    tipo_pedido: CTipoPedido
    estado: CEstadoPedido
    observaciones: str | None = None
    total: float
    fecha_entrega: datetime | None = None
    detalle: list[CDetallePedidoRespuesta]


class CInsumoDescontado(BaseModel):
    id_insumo: int
    nombre: str
    cantidad_descontada: float
    stock_resultante: float


class CCambioEstadoRespuesta(BaseModel):
    mensaje: str
    pedido: CPedidoRespuesta
    insumos_descontados: list[CInsumoDescontado] = []
