from datetime import date

from fastapi import APIRouter, Depends, Query

from app.core.c_dependencias import c_requiere_roles
from app.models.c_enums import CRol
from app.schemas.c_comun_schemas import C_RESP_400, C_RESP_AUTH
from app.schemas.c_reporte_schemas import CProductoMasVendido, CReporteVentas
from app.services import c_reporte_service as c_servicio

c_router = APIRouter(prefix="/reportes", tags=["Reportes"], responses=C_RESP_AUTH)
c_solo_admin = c_requiere_roles(CRol.ADMIN)


@c_router.get("/ventas", response_model=CReporteVentas, summary="Ventas por rango de fechas (ADMIN)",
              description="Total vendido, número de pedidos ENTREGADOS, ticket promedio y ventas por día.",
              responses=C_RESP_400)
def c_reporte_ventas(
    desde: date = Query(description="Fecha inicial (YYYY-MM-DD)", examples=["2026-10-01"]),
    hasta: date = Query(description="Fecha final (YYYY-MM-DD)", examples=["2026-10-31"]),
    _=Depends(c_solo_admin),
):
    return c_servicio.c_reporte_ventas(desde, hasta)


@c_router.get("/productos-mas-vendidos", response_model=list[CProductoMasVendido],
              summary="Ranking de productos más vendidos (ADMIN)", responses=C_RESP_400)
def c_productos_mas_vendidos(
    limite: int = Query(10, ge=1, le=100),
    desde: date | None = Query(None, description="Opcional"),
    hasta: date | None = Query(None, description="Opcional"),
    _=Depends(c_solo_admin),
):
    return c_servicio.c_productos_mas_vendidos(limite, desde, hasta)
