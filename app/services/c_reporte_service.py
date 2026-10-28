"""RF11: reportes de ventas y de productos más vendidos (solo pedidos ENTREGADOS)."""
from datetime import date

from app.core.c_excepciones import CSolicitudInvalida
from app.core.c_utilidades import c_fin_dia, c_inicio_dia, c_redondear
from app.repositories.c_pedido_repository import c_pedido_repo


def c_validar_rango(c_desde: date | None, c_hasta: date | None) -> None:
    if c_desde and c_hasta and c_desde > c_hasta:
        raise CSolicitudInvalida("La fecha 'desde' no puede ser mayor que 'hasta'")


def c_reporte_ventas(c_desde: date, c_hasta: date) -> dict:
    c_validar_rango(c_desde, c_hasta)
    c_datos = c_pedido_repo.c_reporte_ventas(c_inicio_dia(c_desde), c_fin_dia(c_hasta))
    c_numero = c_datos["numero_pedidos"]
    c_total = c_redondear(c_datos["total_vendido"])
    return {
        "desde": c_desde,
        "hasta": c_hasta,
        "numero_pedidos": c_numero,
        "total_vendido": c_total,
        "ticket_promedio": c_redondear(c_total / c_numero) if c_numero else 0,
        "ventas_por_dia": c_datos["ventas_por_dia"],
    }


def c_productos_mas_vendidos(c_limite: int, c_desde: date | None, c_hasta: date | None) -> list[dict]:
    c_validar_rango(c_desde, c_hasta)
    c_ranking = c_pedido_repo.c_productos_mas_vendidos(
        c_limite,
        c_inicio_dia(c_desde) if c_desde else None,
        c_fin_dia(c_hasta) if c_hasta else None,
    )
    return [{"posicion": c_i, **c_fila} for c_i, c_fila in enumerate(c_ranking, start=1)]
