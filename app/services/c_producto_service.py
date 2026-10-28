"""RF04, RF05 y RF06: productos, su receta y su costo de producción."""
from app.core.c_excepciones import CConflicto
from app.core.c_utilidades import c_redondear
from app.repositories.c_categoria_repository import c_categoria_repo
from app.repositories.c_pedido_repository import c_pedido_repo
from app.repositories.c_producto_repository import c_producto_repo
from app.repositories.c_receta_repository import c_receta_repo
from app.schemas.c_producto_schemas import CProductoActualizar, CProductoCrear
from app.services.c_servicio_comun import c_cambios, c_requerir, c_resultado


def c_validar_categoria(c_id_categoria: int) -> None:
    c_categoria = c_requerir(c_categoria_repo.c_obtener(c_id_categoria), f"No existe la categoría {c_id_categoria}")
    if c_categoria["estado"] != "ACTIVO":
        raise CConflicto(f"La categoría {c_id_categoria} está INACTIVA")


def c_listar_productos(c_estado: str | None, c_omitir: int, c_limite: int) -> list[dict]:
    return c_producto_repo.c_listar({"estado": c_estado} if c_estado else {}, c_omitir=c_omitir, c_limite=c_limite)


def c_listar_por_categoria(c_id_categoria: int) -> list[dict]:
    c_requerir(c_categoria_repo.c_obtener(c_id_categoria), f"No existe la categoría {c_id_categoria}")
    return c_producto_repo.c_listar({"id_categoria": c_id_categoria}, c_orden=[("nombre", 1)])


def c_obtener_producto(c_id: int) -> dict:
    return c_requerir(c_producto_repo.c_obtener(c_id), f"No existe el producto {c_id}")


def c_crear_producto(c_datos: CProductoCrear) -> dict:
    c_validar_categoria(c_datos.id_categoria)
    return c_producto_repo.c_crear(c_datos.model_dump())


def c_actualizar_producto(c_id: int, c_datos: CProductoActualizar) -> dict:
    c_obtener_producto(c_id)
    c_nuevos = c_cambios(c_datos)
    if "id_categoria" in c_nuevos:
        c_validar_categoria(c_nuevos["id_categoria"])
    return c_producto_repo.c_actualizar(c_id, c_nuevos)


def c_eliminar_producto(c_id: int) -> dict:
    """RN04: con pedidos asociados solo se inactiva."""
    c_obtener_producto(c_id)
    if c_pedido_repo.c_existe({"detalle.id_producto": c_id}):
        c_producto_repo.c_actualizar(c_id, {"estado": "INACTIVO"})
        return c_resultado("El producto tiene pedidos asociados: se marcó como INACTIVO", True)
    c_receta_repo.c_col.delete_many({"id_producto": c_id})
    c_producto_repo.c_eliminar(c_id)
    return c_resultado("Producto y su receta eliminados", False)


def c_obtener_receta_producto(c_id: int) -> dict:
    c_producto = c_obtener_producto(c_id)
    return {
        "id_producto": c_id,
        "nombre": c_producto["nombre"],
        "insumos": c_receta_repo.c_receta_con_insumos(c_id),
    }


def c_calcular_costo_producto(c_id: int) -> dict:
    """RF06: costo = Σ cantidad × costo_unitario; margen frente al precio de venta."""
    c_producto = c_obtener_producto(c_id)
    c_detalle = c_receta_repo.c_receta_con_insumos(c_id)
    c_costo = c_redondear(sum(c_item["costo_total"] for c_item in c_detalle))
    c_precio = float(c_producto["precio_venta"])
    c_margen = c_redondear(c_precio - c_costo)
    return {
        "id_producto": c_id,
        "nombre": c_producto["nombre"],
        "precio_venta": c_precio,
        "costo_produccion": c_costo,
        "margen": c_margen,
        "margen_porcentaje": c_redondear(c_margen / c_precio * 100) if c_precio else 0,
        "detalle": c_detalle,
    }
