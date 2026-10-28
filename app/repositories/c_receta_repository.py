from app.models.c_colecciones import C_RECETAS
from app.repositories.c_base_repository import CRepositorioBase


class CRecetaRepositorio(CRepositorioBase):
    def __init__(self) -> None:
        super().__init__(C_RECETAS)

    def c_receta_con_insumos(self, c_id_producto: int) -> list[dict]:
        """Une recetas con insumos ($lookup) para mostrar nombre, unidad y costo."""
        c_pipeline = [
            {"$match": {"id_producto": c_id_producto}},
            {"$lookup": {"from": "insumos", "localField": "id_insumo",
                         "foreignField": "id_insumo", "as": "insumo"}},
            {"$unwind": "$insumo"},
            {"$project": {
                "_id": 0,
                "id_receta": 1,
                "id_insumo": 1,
                "cantidad": 1,
                "nombre_insumo": "$insumo.nombre",
                "unidad_medida": "$insumo.unidad_medida",
                "costo_unitario": "$insumo.costo_unitario",
                "costo_total": {"$round": [{"$multiply": ["$cantidad", "$insumo.costo_unitario"]}, 2]},
            }},
            {"$sort": {"id_receta": 1}},
        ]
        return list(self.c_col.aggregate(c_pipeline))


c_receta_repo = CRecetaRepositorio()
