from datetime import date

from pydantic import BaseModel


class CVentaDia(BaseModel):
    fecha: date
    numero_pedidos: int
    total_vendido: float


class CReporteVentas(BaseModel):
    desde: date
    hasta: date
    numero_pedidos: int
    total_vendido: float
    ticket_promedio: float
    ventas_por_dia: list[CVentaDia]


class CProductoMasVendido(BaseModel):
    posicion: int
    id_producto: int
    nombre_producto: str | None = None
    cantidad_vendida: int
    total_vendido: float
    numero_pedidos: int
