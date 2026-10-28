"""RF03: gestión de categorías de productos."""
from app.repositories.c_categoria_repository import c_categoria_repo
from app.repositories.c_producto_repository import c_producto_repo
from app.schemas.c_categoria_schemas import CCategoriaActualizar, CCategoriaCrear
from app.services.c_servicio_comun import c_cambios, c_requerir, c_resultado


def c_listar_categorias(c_estado: str | None, c_omitir: int, c_limite: int) -> list[dict]:
    return c_categoria_repo.c_listar({"estado": c_estado} if c_estado else {}, c_omitir=c_omitir, c_limite=c_limite)


def c_obtener_categoria(c_id: int) -> dict:
    return c_requerir(c_categoria_repo.c_obtener(c_id), f"No existe la categoría {c_id}")


def c_crear_categoria(c_datos: CCategoriaCrear) -> dict:
    return c_categoria_repo.c_crear(c_datos.model_dump())


def c_actualizar_categoria(c_id: int, c_datos: CCategoriaActualizar) -> dict:
    c_obtener_categoria(c_id)
    return c_categoria_repo.c_actualizar(c_id, c_cambios(c_datos))


def c_eliminar_categoria(c_id: int) -> dict:
    c_obtener_categoria(c_id)
    if c_producto_repo.c_existe({"id_categoria": c_id}):
        c_categoria_repo.c_actualizar(c_id, {"estado": "INACTIVO"})
        return c_resultado("La categoría tiene productos asociados: se marcó como INACTIVO", True)
    c_categoria_repo.c_eliminar(c_id)
    return c_resultado("Categoría eliminada", False)
