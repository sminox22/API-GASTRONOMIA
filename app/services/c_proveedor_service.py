"""RF08: gestión de proveedores."""
from app.repositories.c_compra_repository import c_compra_repo
from app.repositories.c_proveedor_repository import c_proveedor_repo
from app.schemas.c_proveedor_schemas import CProveedorActualizar, CProveedorCrear
from app.services.c_servicio_comun import c_cambios, c_requerir, c_resultado


def c_listar_proveedores(c_estado: str | None, c_omitir: int, c_limite: int) -> list[dict]:
    return c_proveedor_repo.c_listar({"estado": c_estado} if c_estado else {}, c_omitir=c_omitir, c_limite=c_limite)


def c_obtener_proveedor(c_id: int) -> dict:
    return c_requerir(c_proveedor_repo.c_obtener(c_id), f"No existe el proveedor {c_id}")


def c_crear_proveedor(c_datos: CProveedorCrear) -> dict:
    return c_proveedor_repo.c_crear(c_datos.model_dump())


def c_actualizar_proveedor(c_id: int, c_datos: CProveedorActualizar) -> dict:
    c_obtener_proveedor(c_id)
    return c_proveedor_repo.c_actualizar(c_id, c_cambios(c_datos))


def c_eliminar_proveedor(c_id: int) -> dict:
    """RN04: con compras registradas solo se inactiva."""
    c_obtener_proveedor(c_id)
    if c_compra_repo.c_existe({"id_proveedor": c_id}):
        c_proveedor_repo.c_actualizar(c_id, {"estado": "INACTIVO"})
        return c_resultado("El proveedor tiene compras registradas: se marcó como INACTIVO", True)
    c_proveedor_repo.c_eliminar(c_id)
    return c_resultado("Proveedor eliminado", False)


def c_compras_de_proveedor(c_id: int) -> list[dict]:
    c_obtener_proveedor(c_id)
    return c_compra_repo.c_listar({"id_proveedor": c_id}, c_orden=[("fecha_compra", -1)])
