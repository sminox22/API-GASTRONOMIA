from datetime import date

from pydantic import Field

from app.models.c_enums import CEstado, CUnidadMedida
from app.schemas.c_comun_schemas import CEsquemaBase, CFecha


class CInsumoCrear(CEsquemaBase):
    nombre: str = Field(min_length=2, max_length=100, examples=["Cebolla cabezona"])
    unidad_medida: CUnidadMedida = Field(examples=["kg"])
    stock_actual: float = Field(0, ge=0, examples=[10])
    stock_minimo: float = Field(0, ge=0, examples=[3])
    costo_unitario: float = Field(0, ge=0, examples=[3500])
    fecha_vencimiento: date | None = Field(None, examples=["2026-11-30"])
    estado: CEstado = CEstado.ACTIVO


class CInsumoActualizar(CEsquemaBase):
    nombre: str | None = Field(None, min_length=2, max_length=100)
    unidad_medida: CUnidadMedida | None = None
    stock_actual: float | None = Field(None, ge=0)
    stock_minimo: float | None = Field(None, ge=0)
    costo_unitario: float | None = Field(None, ge=0)
    fecha_vencimiento: date | None = None
    estado: CEstado | None = None


class CInsumoRespuesta(CEsquemaBase):
    id_insumo: int
    nombre: str
    unidad_medida: CUnidadMedida
    stock_actual: float
    stock_minimo: float
    costo_unitario: float
    fecha_vencimiento: CFecha | None = None
    estado: CEstado


class CInsumoPorVencer(CInsumoRespuesta):
    dias_para_vencer: int
