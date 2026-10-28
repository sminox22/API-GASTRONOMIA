"""RF10: pedidos con su detalle y cambio de estado (RN01, RN03 y RN05)."""
from collections import defaultdict

from app.core.c_excepciones import CConflicto, CProhibido, CSolicitudInvalida
from app.core.c_utilidades import c_ahora, c_redondear
from app.repositories.c_cliente_repository import c_cliente_repo
from app.repositories.c_insumo_repository import c_insumo_repo
from app.repositories.c_pedido_repository import c_pedido_repo
from app.repositories.c_producto_repository import c_producto_repo
from app.repositories.c_receta_repository import c_receta_repo
from app.schemas.c_pedido_schemas import CDetallePedidoCrear, CPedidoActualizar, CPedidoCrear
from app.services.c_servicio_comun import c_cambios, c_requerir, c_resultado

C_ESTADOS_FINALES = {"ENTREGADO", "ANULADO"}
C_TRANSICIONES = {
    "PENDIENTE": {"EN_PREPARACION", "ENTREGADO", "ANULADO"},
    "EN_PREPARACION": {"ENTREGADO", "ANULADO"},
    "ENTREGADO": set(),
    "ANULADO": set(),
}


def c_validar_modificable(c_pedido: dict) -> None:
    """RN05: un pedido ENTREGADO o ANULADO no puede modificarse."""
    if c_pedido["estado"] in C_ESTADOS_FINALES:
        raise CConflicto(f"El pedido {c_pedido['id_pedido']} está {c_pedido['estado']} y no puede modificarse")


def c_validar_cliente(c_id_cliente: int) -> None:
    c_cliente = c_requerir(c_cliente_repo.c_obtener(c_id_cliente), f"No existe el cliente {c_id_cliente}")
    if c_cliente["estado"] != "ACTIVO":
        raise CConflicto(f"El cliente {c_id_cliente} está INACTIVO")


def c_construir_detalle(c_items: list[CDetallePedidoCrear]) -> tuple[list[dict], float]:
    """RN01: precio tomado del producto, subtotal = cantidad × precio_unitario, total = Σ subtotales."""
    c_cantidades: dict[int, int] = {}
    for c_item in c_items:  # un mismo producto repetido se agrupa en un solo ítem
        c_cantidades[c_item.id_producto] = c_cantidades.get(c_item.id_producto, 0) + c_item.cantidad

    c_detalle = []
    for c_id_producto, c_cantidad in c_cantidades.items():
        c_producto = c_requerir(c_producto_repo.c_obtener(c_id_producto), f"No existe el producto {c_id_producto}")
        if c_producto["estado"] != "DISPONIBLE":
            raise CConflicto(f"El producto {c_producto['nombre']} está {c_producto['estado']}")
        c_precio = float(c_producto["precio_venta"])
        c_detalle.append({
            "id_producto": c_id_producto,
            "nombre_producto": c_producto["nombre"],
            "cantidad": c_cantidad,
            "precio_unitario": c_precio,
            "subtotal": c_redondear(c_cantidad * c_precio),
        })
    return c_detalle, c_redondear(sum(c_d["subtotal"] for c_d in c_detalle))


def c_listar_pedidos(c_estado: str | None, c_id_cliente: int | None, c_omitir: int, c_limite: int) -> list[dict]:
    c_filtro = {k: v for k, v in {"estado": c_estado, "id_cliente": c_id_cliente}.items() if v}
    return c_pedido_repo.c_listar(c_filtro, c_orden=[("fecha_pedido", -1)], c_omitir=c_omitir, c_limite=c_limite)


def c_pedidos_por_estado(c_estado: str) -> list[dict]:
    return c_pedido_repo.c_listar({"estado": c_estado}, c_orden=[("fecha_pedido", 1)])


def c_obtener_pedido(c_id: int) -> dict:
    return c_requerir(c_pedido_repo.c_obtener(c_id), f"No existe el pedido {c_id}")


def c_crear_pedido(c_datos: CPedidoCrear, c_usuario: dict) -> dict:
    c_validar_cliente(c_datos.id_cliente)
    c_detalle, c_total = c_construir_detalle(c_datos.detalle)
    return c_pedido_repo.c_crear({
        "fecha_pedido": c_ahora(),
        "id_cliente": c_datos.id_cliente,
        "id_usuario": c_usuario["id_usuario"],
        "tipo_pedido": c_datos.tipo_pedido,
        "estado": "PENDIENTE",
        "observaciones": c_datos.observaciones,
        "total": c_total,
        "fecha_entrega": None,
        "detalle": c_detalle,
    })


def c_actualizar_pedido(c_id: int, c_datos: CPedidoActualizar) -> dict:
    c_pedido = c_obtener_pedido(c_id)
    c_validar_modificable(c_pedido)
    c_nuevos = c_cambios(c_datos)
    if "id_cliente" in c_nuevos:
        c_validar_cliente(c_nuevos["id_cliente"])
    if "detalle" in c_nuevos:
        c_nuevos["detalle"], c_nuevos["total"] = c_construir_detalle(c_datos.detalle)
    # El filtro por estado evita modificar un pedido que cambió de estado en paralelo
    c_actualizado = c_pedido_repo.c_actualizar(c_id, c_nuevos, {"estado": {"$nin": list(C_ESTADOS_FINALES)}})
    if c_actualizado is None:
        raise CConflicto("El pedido cambió de estado y ya no puede modificarse")
    return c_actualizado


def c_eliminar_pedido(c_id: int) -> dict:
    """Los pedidos no se borran físicamente: se anulan (si aún son modificables)."""
    c_pedido = c_obtener_pedido(c_id)
    c_validar_modificable(c_pedido)
    c_pedido_repo.c_actualizar(c_id, {"estado": "ANULADO"})
    return c_resultado("Pedido ANULADO (los pedidos se conservan como historial)", True)


def c_reintegrar(c_descontados: list[dict]) -> None:
    for c_d in c_descontados:
        c_insumo_repo.c_incrementar_stock(c_d["id_insumo"], c_d["cantidad_descontada"])


def c_descontar_inventario(c_pedido: dict) -> list[dict]:
    """RN03: descuenta los insumos de la receta × cantidad de cada producto. Si falta algo → 409."""
    c_requeridos: dict[int, float] = defaultdict(float)
    for c_item in c_pedido["detalle"]:
        for c_receta in c_receta_repo.c_listar({"id_producto": c_item["id_producto"]}):
            c_requeridos[c_receta["id_insumo"]] += c_receta["cantidad"] * c_item["cantidad"]
    if not c_requeridos:
        return []

    c_insumos = {c_i["id_insumo"]: c_i for c_i in c_insumo_repo.c_listar({"id_insumo": {"$in": list(c_requeridos)}})}

    # 1) Verificación previa de todas las existencias
    c_faltantes = []
    for c_id_insumo, c_cantidad in c_requeridos.items():
        c_cantidad = round(c_cantidad, 3)
        c_insumo = c_insumos.get(c_id_insumo)
        c_disponible = float(c_insumo["stock_actual"]) if c_insumo else 0.0
        if c_disponible < c_cantidad:
            c_faltantes.append({
                "id_insumo": c_id_insumo,
                "nombre": c_insumo["nombre"] if c_insumo else "(no existe)",
                "requerido": c_cantidad,
                "disponible": c_disponible,
            })
    if c_faltantes:
        raise CConflicto("Inventario insuficiente para entregar el pedido", {"faltantes": c_faltantes})

    # 2) Descuento atómico por insumo; si otro proceso consumió el stock se revierte lo descontado
    c_descontados = []
    for c_id_insumo, c_cantidad in c_requeridos.items():
        c_cantidad = round(c_cantidad, 3)
        if not c_insumo_repo.c_descontar_stock(c_id_insumo, c_cantidad):
            c_reintegrar(c_descontados)
            raise CConflicto(f"Inventario insuficiente del insumo {c_insumos[c_id_insumo]['nombre']}")
        c_descontados.append({
            "id_insumo": c_id_insumo,
            "nombre": c_insumos[c_id_insumo]["nombre"],
            "cantidad_descontada": c_cantidad,
            "stock_resultante": round(float(c_insumos[c_id_insumo]["stock_actual"]) - c_cantidad, 3),
        })
    return c_descontados


def c_cambiar_estado(c_id: int, c_nuevo: str, c_usuario: dict) -> dict:
    c_pedido = c_obtener_pedido(c_id)
    c_actual = c_pedido["estado"]
    c_validar_modificable(c_pedido)  # RN05
    if c_nuevo == c_actual:
        raise CSolicitudInvalida(f"El pedido ya está en estado {c_actual}")
    if c_nuevo not in C_TRANSICIONES[c_actual]:
        raise CConflicto(f"Transición no permitida: {c_actual} → {c_nuevo}")
    if c_usuario["rol"] == "COCINERO" and c_nuevo == "ANULADO":
        raise CProhibido("El rol COCINERO no puede anular pedidos")

    c_nuevos: dict = {"estado": c_nuevo}
    c_descontados: list[dict] = []
    if c_nuevo == "ENTREGADO":
        c_descontados = c_descontar_inventario(c_pedido)  # RN03
        c_nuevos["fecha_entrega"] = c_ahora()

    c_actualizado = c_pedido_repo.c_actualizar(c_id, c_nuevos, {"estado": c_actual})
    if c_actualizado is None:
        c_reintegrar(c_descontados)
        raise CConflicto("El pedido cambió de estado simultáneamente; intente de nuevo")

    return {
        "mensaje": f"Pedido {c_id}: {c_actual} → {c_nuevo}",
        "pedido": c_actualizado,
        "insumos_descontados": c_descontados,
    }
