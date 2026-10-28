from datetime import date, datetime

from pydantic import BaseModel, Field

from app.schemas.c_comun_schemas import CEsquemaBase, CFecha


class CDetalleCompraCrear(CEsquemaBase):
    id_insumo: int = Field(gt=0, examples=[1])
    cantidad: float = Field(gt=0, examples=[10])
    costo_unitario: float = Field(ge=0, examples=[4300])
    fecha_vencimiento: date | None = Field(None, description="Vencimiento del nuevo lote (opcional)")


class CCompraCrear(CEsquemaBase):
    numero_factura: str = Field(min_length=1, max_length=30, examples=["FV-1050"])
    id_proveedor: int = Field(gt=0, examples=[6])
    fecha_compra: datetime | None = Field(None, description="Si se omite se usa la fecha y hora actual")
    detalle: list[CDetalleCompraCrear] = Field(min_length=1)


class CCompraActualizar(CEsquemaBase):
    """Solo se modifican los datos de encabezado; el detalle afecta el inventario y no se edita."""
    numero_factura: str | None = Field(None, min_length=1, max_length=30)
    id_proveedor: int | None = Field(None, gt=0)
    fecha_compra: datetime | None = None


class CDetalleCompraRespuesta(BaseModel):
    id_insumo: int
    nombre_insumo: str | None = None
    cantidad: float
    costo_unitario: float
    subtotal: float
    fecha_vencimiento: CFecha | None = None


class CCompraRespuesta(BaseModel):
    id_compra: int
    numero_factura: str
    fecha_compra: datetime
    id_proveedor: int
    id_usuario: int
    total: float
    detalle: list[CDetalleCompraRespuesta]
