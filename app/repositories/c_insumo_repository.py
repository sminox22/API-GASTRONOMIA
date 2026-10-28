from datetime import datetime

from app.models.c_colecciones import C_INSUMOS
from app.repositories.c_base_repository import CRepositorioBase


class CInsumoRepositorio(CRepositorioBase):
    def __init__(self) -> None:
        super().__init__(C_INSUMOS)

    def c_stock_bajo(self) -> list[dict]:
        # $expr permite comparar dos campos del mismo documento
        return self.c_listar(
            {"estado": "ACTIVO", "$expr": {"$lte": ["$stock_actual", "$stock_minimo"]}},
            c_orden=[("nombre", 1)],
        )

    def c_por_vencer(self, c_desde: datetime, c_hasta: datetime) -> list[dict]:
        return self.c_listar(
            {"estado": "ACTIVO", "fecha_vencimiento": {"$gte": c_desde, "$lte": c_hasta}},
            c_orden=[("fecha_vencimiento", 1)],
        )

    def c_incrementar_stock(self, c_id: int, c_cantidad: float, c_costo: float | None = None,
                            c_vencimiento: datetime | None = None) -> None:
        """RN02: suma existencias y actualiza el costo unitario con el de la compra."""
        c_cambios: dict = {"stock_actual": {"$round": [{"$add": ["$stock_actual", c_cantidad]}, 3]}}
        if c_costo is not None:
            c_cambios["costo_unitario"] = c_costo
        if c_vencimiento is not None:
            c_cambios["fecha_vencimiento"] = c_vencimiento
        # Actualización con pipeline: atómica y con redondeo para evitar errores de coma flotante
        self.c_col.update_one({self.c_campo_id: c_id}, [{"$set": c_cambios}])

    def c_descontar_stock(self, c_id: int, c_cantidad: float) -> bool:
        """Descuento condicional y atómico: solo se aplica si hay existencias suficientes."""
        c_resultado = self.c_col.update_one(
            {self.c_campo_id: c_id, "stock_actual": {"$gte": c_cantidad}},
            [{"$set": {"stock_actual": {"$round": [{"$subtract": ["$stock_actual", c_cantidad]}, 3]}}}],
        )
        return c_resultado.matched_count == 1


c_insumo_repo = CInsumoRepositorio()
