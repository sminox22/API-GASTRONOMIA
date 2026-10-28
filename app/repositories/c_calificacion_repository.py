from app.models.c_colecciones import C_CALIFICACIONES
from app.repositories.c_base_repository import CRepositorioBase


class CCalificacionRepositorio(CRepositorioBase):
    def __init__(self) -> None:
        super().__init__(C_CALIFICACIONES)

    def c_por_producto(self, c_id_producto: int) -> dict:
        """RF12: calificaciones de un producto y su promedio."""
        c_pipeline = [
            {"$match": {"productos.id_producto": c_id_producto}},
            {"$unwind": "$productos"},
            {"$match": {"productos.id_producto": c_id_producto}},
            {"$sort": {"fecha": -1}},
            {"$group": {
                "_id": "$productos.id_producto",
                "nombre": {"$first": "$productos.nombre"},
                "total_calificaciones": {"$sum": 1},
                "promedio": {"$avg": "$productos.calificacion"},
                "calificaciones": {"$push": {
                    "id_calificacion": "$id_calificacion",
                    "id_pedido": "$id_pedido",
                    "id_cliente": "$id_cliente",
                    "fecha": "$fecha",
                    "calificacion": "$productos.calificacion",
                    "comentario": "$comentario",
                }},
            }},
            {"$project": {"_id": 0, "id_producto": "$_id", "nombre": 1, "total_calificaciones": 1,
                          "promedio": {"$round": ["$promedio", 2]}, "calificaciones": 1}},
        ]
        return next(self.c_col.aggregate(c_pipeline), None)


c_calificacion_repo = CCalificacionRepositorio()
