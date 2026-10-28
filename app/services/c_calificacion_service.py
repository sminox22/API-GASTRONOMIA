"""RF12: calificaciones de los clientes sobre pedidos y productos."""
from app.core.c_excepciones import CConflicto, CSolicitudInvalida
from app.core.c_utilidades import c_ahora
from app.repositories.c_calificacion_repository import c_calificacion_repo
from app.repositories.c_pedido_repository import c_pedido_repo
from app.repositories.c_producto_repository import c_producto_repo
from app.schemas.c_calificacion_schemas import (CCalificacionActualizar, CCalificacionCrear,
                                                CCalificacionProductoCrear)
from app.services.c_servicio_comun import c_cambios, c_requerir, c_resultado


def c_armar_productos(c_pedido: dict, c_items: list[CCalificacionProductoCrear]) -> list[dict]:
    """Solo se califican productos que estén en el pedido; el nombre se toma del detalle."""
    c_nombres = {c_d["id_producto"]: c_d.get("nombre_producto") for c_d in c_pedido["detalle"]}
    c_productos, c_vistos = [], set()
    for c_item in c_items:
        if c_item.id_producto not in c_nombres:
            raise CSolicitudInvalida(f"El producto {c_item.id_producto} no hace parte del pedido {c_pedido['id_pedido']}")
        if c_item.id_producto in c_vistos:
            raise CSolicitudInvalida(f"El producto {c_item.id_producto} está repetido")
        c_vistos.add(c_item.id_producto)
        c_productos.append({"id_producto": c_item.id_producto, "nombre": c_nombres[c_item.id_producto],
                            "calificacion": c_item.calificacion})
    return c_productos


def c_listar_calificaciones(c_id_cliente: int | None, c_omitir: int, c_limite: int) -> list[dict]:
    c_filtro = {"id_cliente": c_id_cliente} if c_id_cliente else {}
    return c_calificacion_repo.c_listar(c_filtro, c_orden=[("fecha", -1)], c_omitir=c_omitir, c_limite=c_limite)


def c_obtener_calificacion(c_id: int) -> dict:
    return c_requerir(c_calificacion_repo.c_obtener(c_id), f"No existe la calificación {c_id}")


def c_crear_calificacion(c_datos: CCalificacionCrear) -> dict:
    c_pedido = c_requerir(c_pedido_repo.c_obtener(c_datos.id_pedido), f"No existe el pedido {c_datos.id_pedido}")
    if c_pedido["estado"] != "ENTREGADO":
        raise CConflicto("Solo se pueden calificar pedidos ENTREGADOS")
    return c_calificacion_repo.c_crear({
        "id_pedido": c_pedido["id_pedido"],
        "id_cliente": c_pedido["id_cliente"],
        "fecha": c_ahora(),
        "calificacion_servicio": c_datos.calificacion_servicio,
        "comentario": c_datos.comentario,
        "productos": c_armar_productos(c_pedido, c_datos.productos),
    })


def c_actualizar_calificacion(c_id: int, c_datos: CCalificacionActualizar) -> dict:
    c_calificacion = c_obtener_calificacion(c_id)
    c_nuevos = c_cambios(c_datos)
    if "productos" in c_nuevos:
        c_pedido = c_pedido_repo.c_obtener(c_calificacion["id_pedido"])
        c_nuevos["productos"] = c_armar_productos(c_pedido, c_datos.productos or [])
    return c_calificacion_repo.c_actualizar(c_id, c_nuevos)


def c_eliminar_calificacion(c_id: int) -> dict:
    c_obtener_calificacion(c_id)
    c_calificacion_repo.c_eliminar(c_id)
    return c_resultado("Calificación eliminada", False)


def c_calificaciones_de_producto(c_id_producto: int) -> dict:
    c_producto = c_requerir(c_producto_repo.c_obtener(c_id_producto), f"No existe el producto {c_id_producto}")
    c_resumen = c_calificacion_repo.c_por_producto(c_id_producto)
    return c_resumen or {
        "id_producto": c_id_producto,
        "nombre": c_producto["nombre"],
        "total_calificaciones": 0,
        "promedio": None,
        "calificaciones": [],
    }
