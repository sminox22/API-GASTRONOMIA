"""Repositorio genérico: operaciones CRUD sobre una colección de MongoDB."""
from pymongo import ReturnDocument
from pymongo.collection import Collection

from app.database.c_conexion_mongo import c_obtener_bd
from app.models.c_colecciones import C_CONTADORES


class CRepositorioBase:
    """Cada documento tiene un id entero propio (id_xxx); el _id interno nunca se expone."""

    c_proyeccion: dict = {"_id": 0}

    def __init__(self, c_definicion: tuple[str, str]) -> None:
        self.c_coleccion, self.c_campo_id = c_definicion

    @property
    def c_col(self) -> Collection:
        return c_obtener_bd()[self.c_coleccion]

    def c_siguiente_id(self) -> int:
        """Secuencia atómica en la colección contadores (equivale a AUTO_INCREMENT)."""
        c_contador = c_obtener_bd()[C_CONTADORES].find_one_and_update(
            {"_id": self.c_coleccion},
            {"$inc": {"seq": 1}},
            upsert=True,
            return_document=ReturnDocument.AFTER,
        )
        return int(c_contador["seq"])

    def c_listar(self, c_filtro: dict | None = None, c_orden: list | None = None,
                 c_omitir: int = 0, c_limite: int = 0) -> list[dict]:
        c_cursor = (
            self.c_col.find(c_filtro or {}, self.c_proyeccion)
            .sort(c_orden or [(self.c_campo_id, 1)])
            .skip(c_omitir)
            .limit(c_limite)
        )
        return list(c_cursor)

    def c_obtener(self, c_id: int) -> dict | None:
        return self.c_col.find_one({self.c_campo_id: c_id}, self.c_proyeccion)

    def c_buscar_uno(self, c_filtro: dict) -> dict | None:
        return self.c_col.find_one(c_filtro, self.c_proyeccion)

    def c_existe(self, c_filtro: dict) -> bool:
        return self.c_col.find_one(c_filtro, {"_id": 1}) is not None

    def c_crear(self, c_datos: dict) -> dict:
        c_documento = {self.c_campo_id: self.c_siguiente_id(), **c_datos}
        self.c_col.insert_one(c_documento)
        return self.c_obtener(c_documento[self.c_campo_id])

    def c_actualizar(self, c_id: int, c_cambios: dict, c_filtro_extra: dict | None = None) -> dict | None:
        return self.c_col.find_one_and_update(
            {self.c_campo_id: c_id, **(c_filtro_extra or {})},
            {"$set": c_cambios},
            projection=self.c_proyeccion,
            return_document=ReturnDocument.AFTER,
        )

    def c_eliminar(self, c_id: int) -> bool:
        return self.c_col.delete_one({self.c_campo_id: c_id}).deleted_count == 1
