"""RF07: insumos, stock bajo y próximos a vencer."""
from datetime import timedelta

from app.core.c_utilidades import c_a_fecha, c_fecha_a_datetime, c_fin_dia, c_hoy, c_inicio_dia
from app.repositories.c_compra_repository import c_compra_repo
from app.repositories.c_insumo_repository import c_insumo_repo
from app.repositories.c_receta_repository import c_receta_repo
from app.schemas.c_insumo_schemas import CInsumoActualizar, CInsumoCrear
from app.services.c_servicio_comun import c_cambios, c_requerir, c_resultado


def c_listar_insumos(c_estado: str | None, c_omitir: int, c_limite: int) -> list[dict]:
    return c_insumo_repo.c_listar({"estado": c_estado} if c_estado else {}, c_omitir=c_omitir, c_limite=c_limite)


def c_obtener_insumo(c_id: int) -> dict:
    return c_requerir(c_insumo_repo.c_obtener(c_id), f"No existe el insumo {c_id}")


def c_crear_insumo(c_datos: CInsumoCrear) -> dict:
    c_documento = c_datos.model_dump()
    c_documento["fecha_vencimiento"] = c_fecha_a_datetime(c_documento["fecha_vencimiento"])
    return c_insumo_repo.c_crear(c_documento)


def c_actualizar_insumo(c_id: int, c_datos: CInsumoActualizar) -> dict:
    c_obtener_insumo(c_id)
    c_nuevos = c_cambios(c_datos)
    if "fecha_vencimiento" in c_nuevos:
        c_nuevos["fecha_vencimiento"] = c_fecha_a_datetime(c_nuevos["fecha_vencimiento"])
    return c_insumo_repo.c_actualizar(c_id, c_nuevos)


def c_eliminar_insumo(c_id: int) -> dict:
    """RN04: si está en recetas o compras solo se inactiva."""
    c_obtener_insumo(c_id)
    if c_compra_repo.c_existe({"detalle.id_insumo": c_id}) or c_receta_repo.c_existe({"id_insumo": c_id}):
        c_insumo_repo.c_actualizar(c_id, {"estado": "INACTIVO"})
        return c_resultado("El insumo tiene compras o recetas asociadas: se marcó como INACTIVO", True)
    c_insumo_repo.c_eliminar(c_id)
    return c_resultado("Insumo eliminado", False)


def c_insumos_stock_bajo() -> list[dict]:
    return c_insumo_repo.c_stock_bajo()


def c_insumos_por_vencer(c_dias: int) -> list[dict]:
    c_hoy_bogota = c_hoy()
    c_insumos = c_insumo_repo.c_por_vencer(c_inicio_dia(c_hoy_bogota),
                                           c_fin_dia(c_hoy_bogota + timedelta(days=c_dias)))
    for c_insumo in c_insumos:
        c_insumo["dias_para_vencer"] = (c_a_fecha(c_insumo["fecha_vencimiento"]) - c_hoy_bogota).days
    return c_insumos
