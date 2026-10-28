from datetime import datetime

from app.core.c_config import c_config
from app.models.c_colecciones import C_PEDIDOS
from app.repositories.c_base_repository import CRepositorioBase


class CPedidoRepositorio(CRepositorioBase):
    def __init__(self) -> None:
        super().__init__(C_PEDIDOS)

    def c_reporte_ventas(self, c_desde: datetime, c_hasta: datetime) -> dict:
        """RF11: total vendido y número de pedidos ENTREGADOS en el rango, con detalle por día."""
        c_pipeline = [
            {"$match": {"estado": "ENTREGADO", "fecha_pedido": {"$gte": c_desde, "$lte": c_hasta}}},
            {"$facet": {
                "resumen": [
                    {"$group": {"_id": None, "numero_pedidos": {"$sum": 1}, "total_vendido": {"$sum": "$total"}}},
                ],
                "por_dia": [
                    {"$group": {
                        "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$fecha_pedido",
                                                  "timezone": c_config.c_zona_horaria}},
                        "numero_pedidos": {"$sum": 1},
                        "total_vendido": {"$sum": "$total"},
                    }},
                    {"$sort": {"_id": 1}},
                    {"$project": {"_id": 0, "fecha": "$_id", "numero_pedidos": 1, "total_vendido": 1}},
                ],
            }},
        ]
        c_resultado = next(self.c_col.aggregate(c_pipeline))
        c_resumen = c_resultado["resumen"][0] if c_resultado["resumen"] else {"numero_pedidos": 0, "total_vendido": 0}
        return {
            "numero_pedidos": c_resumen["numero_pedidos"],
            "total_vendido": c_resumen["total_vendido"],
            "ventas_por_dia": c_resultado["por_dia"],
        }

    def c_productos_mas_vendidos(self, c_limite: int, c_desde: datetime | None = None,
                                 c_hasta: datetime | None = None) -> list[dict]:
        """RF11: ranking de productos por cantidad vendida en pedidos ENTREGADOS."""
        c_filtro: dict = {"estado": "ENTREGADO"}
        if c_desde or c_hasta:
            c_filtro["fecha_pedido"] = {}
            if c_desde:
                c_filtro["fecha_pedido"]["$gte"] = c_desde
            if c_hasta:
                c_filtro["fecha_pedido"]["$lte"] = c_hasta
        c_pipeline = [
            {"$match": c_filtro},
            {"$unwind": "$detalle"},
            {"$group": {
                "_id": "$detalle.id_producto",
                "nombre_producto": {"$first": "$detalle.nombre_producto"},
                "cantidad_vendida": {"$sum": "$detalle.cantidad"},
                "total_vendido": {"$sum": "$detalle.subtotal"},
                "numero_pedidos": {"$sum": 1},
            }},
            {"$sort": {"cantidad_vendida": -1, "total_vendido": -1}},
            {"$limit": c_limite},
            {"$project": {"_id": 0, "id_producto": "$_id", "nombre_producto": 1, "cantidad_vendida": 1,
                          "total_vendido": 1, "numero_pedidos": 1}},
        ]
        return list(self.c_col.aggregate(c_pipeline))


c_pedido_repo = CPedidoRepositorio()
