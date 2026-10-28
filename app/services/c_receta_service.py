"""RF05: ítems de la receta (ficha técnica) de cada producto."""
from app.repositories.c_insumo_repository import c_insumo_repo
from app.repositories.c_producto_repository import c_producto_repo
from app.repositories.c_receta_repository import c_receta_repo
from app.schemas.c_receta_schemas import CRecetaActualizar, CRecetaCrear
from app.services.c_servicio_comun import c_cambios, c_requerir, c_resultado


def c_validar_referencias(c_id_producto: int | None, c_id_insumo: int | None) -> None:
    if c_id_producto is not None:
        c_requerir(c_producto_repo.c_obtener(c_id_producto), f"No existe el producto {c_id_producto}")
    if c_id_insumo is not None:
        c_requerir(c_insumo_repo.c_obtener(c_id_insumo), f"No existe el insumo {c_id_insumo}")


def c_listar_recetas(c_id_producto: int | None, c_omitir: int, c_limite: int) -> list[dict]:
    c_filtro = {"id_producto": c_id_producto} if c_id_producto else {}
    return c_receta_repo.c_listar(c_filtro, c_omitir=c_omitir, c_limite=c_limite)


def c_obtener_receta(c_id: int) -> dict:
    return c_requerir(c_receta_repo.c_obtener(c_id), f"No existe el ítem de receta {c_id}")


def c_crear_receta(c_datos: CRecetaCrear) -> dict:
    c_validar_referencias(c_datos.id_producto, c_datos.id_insumo)
    c_documento = c_datos.model_dump()
    c_documento["cantidad"] = round(c_documento["cantidad"], 3)
    return c_receta_repo.c_crear(c_documento)


def c_actualizar_receta(c_id: int, c_datos: CRecetaActualizar) -> dict:
    c_obtener_receta(c_id)
    c_nuevos = c_cambios(c_datos)
    c_validar_referencias(c_nuevos.get("id_producto"), c_nuevos.get("id_insumo"))
    if "cantidad" in c_nuevos:
        c_nuevos["cantidad"] = round(c_nuevos["cantidad"], 3)
    return c_receta_repo.c_actualizar(c_id, c_nuevos)


def c_eliminar_receta(c_id: int) -> dict:
    c_obtener_receta(c_id)
    c_receta_repo.c_eliminar(c_id)
    return c_resultado("Ítem de receta eliminado", False)
