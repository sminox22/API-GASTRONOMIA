"""RF02: gestión de usuarios con roles ADMIN, CAJERO y COCINERO."""
from app.core.c_excepciones import CSolicitudInvalida
from app.core.c_security import c_cifrar_password
from app.repositories.c_compra_repository import c_compra_repo
from app.repositories.c_pedido_repository import c_pedido_repo
from app.repositories.c_usuario_repository import c_usuario_repo
from app.schemas.c_usuario_schemas import CUsuarioActualizar, CUsuarioCrear
from app.services.c_servicio_comun import c_cambios, c_requerir, c_resultado


def c_listar_usuarios(c_rol: str | None, c_estado: str | None, c_omitir: int, c_limite: int) -> list[dict]:
    c_filtro = {k: v for k, v in {"rol": c_rol, "estado": c_estado}.items() if v}
    return c_usuario_repo.c_listar(c_filtro, c_omitir=c_omitir, c_limite=c_limite)


def c_obtener_usuario(c_id: int) -> dict:
    return c_requerir(c_usuario_repo.c_obtener(c_id), f"No existe el usuario {c_id}")


def c_crear_usuario(c_datos: CUsuarioCrear) -> dict:
    c_documento = c_datos.model_dump()
    c_documento["password"] = c_cifrar_password(c_documento["password"])  # RN06
    return c_usuario_repo.c_crear(c_documento)


def c_actualizar_usuario(c_id: int, c_datos: CUsuarioActualizar) -> dict:
    c_obtener_usuario(c_id)
    c_nuevos = c_cambios(c_datos)
    if "password" in c_nuevos:
        c_nuevos["password"] = c_cifrar_password(c_nuevos["password"])
    return c_usuario_repo.c_actualizar(c_id, c_nuevos)


def c_eliminar_usuario(c_id: int, c_usuario_actual: dict) -> dict:
    c_obtener_usuario(c_id)
    if c_id == c_usuario_actual["id_usuario"]:
        raise CSolicitudInvalida("No puede eliminar su propio usuario")
    c_tiene_movimientos = (c_pedido_repo.c_existe({"id_usuario": c_id})
                           or c_compra_repo.c_existe({"id_usuario": c_id}))
    if c_tiene_movimientos:
        c_usuario_repo.c_actualizar(c_id, {"estado": "INACTIVO"})
        return c_resultado("El usuario tiene pedidos o compras registradas: se marcó como INACTIVO", True)
    c_usuario_repo.c_eliminar(c_id)
    return c_resultado("Usuario eliminado", False)
