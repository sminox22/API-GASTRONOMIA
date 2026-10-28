"""RF08: registro de compras de insumos con su detalle (RN02)."""
from app.core.c_excepciones import CConflicto
from app.core.c_utilidades import c_ahora, c_fecha_a_datetime, c_redondear
from app.repositories.c_compra_repository import c_compra_repo
from app.repositories.c_insumo_repository import c_insumo_repo
from app.repositories.c_proveedor_repository import c_proveedor_repo
from app.schemas.c_compra_schemas import CCompraActualizar, CCompraCrear
from app.services.c_servicio_comun import c_cambios, c_requerir, c_resultado


def c_validar_proveedor(c_id_proveedor: int) -> None:
    c_proveedor = c_requerir(c_proveedor_repo.c_obtener(c_id_proveedor), f"No existe el proveedor {c_id_proveedor}")
    if c_proveedor["estado"] != "ACTIVO":
        raise CConflicto(f"El proveedor {c_id_proveedor} está INACTIVO")


def c_listar_compras(c_id_proveedor: int | None, c_omitir: int, c_limite: int) -> list[dict]:
    c_filtro = {"id_proveedor": c_id_proveedor} if c_id_proveedor else {}
    return c_compra_repo.c_listar(c_filtro, c_orden=[("fecha_compra", -1)], c_omitir=c_omitir, c_limite=c_limite)


def c_obtener_compra(c_id: int) -> dict:
    return c_requerir(c_compra_repo.c_obtener(c_id), f"No existe la compra {c_id}")


def c_crear_compra(c_datos: CCompraCrear, c_usuario: dict) -> dict:
    c_validar_proveedor(c_datos.id_proveedor)

    c_detalle = []
    for c_item in c_datos.detalle:
        c_insumo = c_requerir(c_insumo_repo.c_obtener(c_item.id_insumo), f"No existe el insumo {c_item.id_insumo}")
        if c_insumo["estado"] != "ACTIVO":
            raise CConflicto(f"El insumo {c_item.id_insumo} está INACTIVO")
        c_detalle.append({
            "id_insumo": c_item.id_insumo,
            "nombre_insumo": c_insumo["nombre"],
            "cantidad": c_item.cantidad,
            "costo_unitario": c_item.costo_unitario,
            "subtotal": c_redondear(c_item.cantidad * c_item.costo_unitario),
            "fecha_vencimiento": c_fecha_a_datetime(c_item.fecha_vencimiento),
        })

    c_compra = c_compra_repo.c_crear({
        "numero_factura": c_datos.numero_factura,
        "fecha_compra": c_datos.fecha_compra or c_ahora(),
        "id_proveedor": c_datos.id_proveedor,
        "id_usuario": c_usuario["id_usuario"],
        "total": c_redondear(sum(c_d["subtotal"] for c_d in c_detalle)),
        "detalle": c_detalle,
    })

    # RN02: se aplica después de guardar la compra (si la factura está duplicada no se toca el inventario)
    for c_d in c_detalle:
        c_insumo_repo.c_incrementar_stock(c_d["id_insumo"], c_d["cantidad"], c_d["costo_unitario"],
                                          c_d["fecha_vencimiento"])
    return c_compra


def c_actualizar_compra(c_id: int, c_datos: CCompraActualizar) -> dict:
    c_obtener_compra(c_id)
    c_nuevos = c_cambios(c_datos)
    if "id_proveedor" in c_nuevos:
        c_validar_proveedor(c_nuevos["id_proveedor"])
    return c_compra_repo.c_actualizar(c_id, c_nuevos)


def c_eliminar_compra(c_id: int) -> dict:
    """Revierte el stock que sumó la compra; si esas existencias ya se consumieron responde 409."""
    c_compra = c_obtener_compra(c_id)
    c_revertidos = []
    for c_d in c_compra["detalle"]:
        if not c_insumo_repo.c_descontar_stock(c_d["id_insumo"], c_d["cantidad"]):
            for c_r in c_revertidos:
                c_insumo_repo.c_incrementar_stock(c_r["id_insumo"], c_r["cantidad"])
            raise CConflicto(
                f"No se puede eliminar la compra: el insumo {c_d['id_insumo']} ya no tiene existencias suficientes para revertirla"
            )
        c_revertidos.append(c_d)
    c_compra_repo.c_eliminar(c_id)
    return c_resultado("Compra eliminada y existencias revertidas", False)
