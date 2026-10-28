from pydantic import BaseModel, Field

from app.models.c_enums import CEstadoProducto
from app.schemas.c_comun_schemas import CEsquemaBase


class CProductoCrear(CEsquemaBase):
    codigo: str = Field(min_length=1, max_length=20, examples=["PF-010"])
    nombre: str = Field(min_length=2, max_length=100, examples=["Asado huilense"])
    descripcion: str | None = Field(None, examples=["Cerdo adobado con insulso y arepa"])
    precio_venta: float = Field(gt=0, examples=[25000])
    unidad_venta: str = Field(min_length=1, max_length=20, examples=["porción"])
    id_categoria: int = Field(gt=0, examples=[1])
    estado: CEstadoProducto = CEstadoProducto.DISPONIBLE


class CProductoActualizar(CEsquemaBase):
    codigo: str | None = Field(None, min_length=1, max_length=20)
    nombre: str | None = Field(None, min_length=2, max_length=100)
    descripcion: str | None = None
    precio_venta: float | None = Field(None, gt=0)
    unidad_venta: str | None = Field(None, min_length=1, max_length=20)
    id_categoria: int | None = Field(None, gt=0)
    estado: CEstadoProducto | None = None


class CProductoRespuesta(CProductoCrear):
    id_producto: int


class CItemRecetaProducto(BaseModel):
    id_receta: int
    id_insumo: int
    nombre_insumo: str
    unidad_medida: str
    cantidad: float
    costo_unitario: float
    costo_total: float


class CRecetaProductoRespuesta(BaseModel):
    id_producto: int
    nombre: str
    insumos: list[CItemRecetaProducto]


class CCostoProductoRespuesta(BaseModel):
    id_producto: int
    nombre: str
    precio_venta: float
    costo_produccion: float = Field(description="Σ cantidad × costo_unitario de la receta")
    margen: float = Field(description="precio_venta − costo_produccion")
    margen_porcentaje: float = Field(description="margen / precio_venta × 100")
    detalle: list[CItemRecetaProducto]
