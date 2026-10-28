"""RF09: gestión de clientes por tipo."""
from app.repositories.c_cliente_repository import c_cliente_repo
from app.repositories.c_pedido_repository import c_pedido_repo
from app.schemas.c_cliente_schemas import CClienteActualizar, CClienteCrear
from app.services.c_servicio_comun import c_cambios, c_requerir, c_resultado


def c_listar_clientes(c_tipo: str | None, c_estado: str | None, c_omitir: int, c_limite: int) -> list[dict]:
    c_filtro = {k: v for k, v in {"tipo_cliente": c_tipo, "estado": c_estado}.items() if v}
    return c_cliente_repo.c_listar(c_filtro, c_omitir=c_omitir, c_limite=c_limite)


def c_obtener_cliente(c_id: int) -> dict:
    return c_requerir(c_cliente_repo.c_obtener(c_id), f"No existe el cliente {c_id}")


def c_crear_cliente(c_datos: CClienteCrear) -> dict:
    return c_cliente_repo.c_crear(c_datos.model_dump())


def c_actualizar_cliente(c_id: int, c_datos: CClienteActualizar) -> dict:
    c_obtener_cliente(c_id)
    return c_cliente_repo.c_actualizar(c_id, c_cambios(c_datos))


def c_eliminar_cliente(c_id: int) -> dict:
    """RN04: con pedidos solo se inactiva."""
    c_obtener_cliente(c_id)
    if c_pedido_repo.c_existe({"id_cliente": c_id}):
        c_cliente_repo.c_actualizar(c_id, {"estado": "INACTIVO"})
        return c_resultado("El cliente tiene pedidos registrados: se marcó como INACTIVO", True)
    c_cliente_repo.c_eliminar(c_id)
    return c_resultado("Cliente eliminado", False)


def c_pedidos_de_cliente(c_id: int) -> list[dict]:
    c_obtener_cliente(c_id)
    return c_pedido_repo.c_listar({"id_cliente": c_id}, c_orden=[("fecha_pedido", -1)])
