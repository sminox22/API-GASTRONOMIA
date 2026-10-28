from fastapi import APIRouter, Depends, Path, Query, status

from app.core.c_dependencias import C_TODOS, c_requiere_roles
from app.models.c_enums import CEstado, CRol
from app.schemas.c_categoria_schemas import CCategoriaActualizar, CCategoriaCrear, CCategoriaRespuesta
from app.schemas.c_comun_schemas import C_RESP_400, C_RESP_404, C_RESP_409, C_RESP_AUTH, CResultadoEliminacion
from app.services import c_categoria_service as c_servicio

c_router = APIRouter(prefix="/categorias", tags=["Categorías"], responses=C_RESP_AUTH)
c_solo_admin = c_requiere_roles(CRol.ADMIN)
c_todos = c_requiere_roles(*C_TODOS)


@c_router.get("", response_model=list[CCategoriaRespuesta], summary="Listar categorías (todos los roles)")
def c_listar_categorias(
    estado: CEstado | None = Query(None),
    omitir: int = Query(0, ge=0),
    limite: int = Query(100, ge=1, le=500),
    _=Depends(c_todos),
):
    return c_servicio.c_listar_categorias(estado and estado.value, omitir, limite)


@c_router.get("/{id_categoria}", response_model=CCategoriaRespuesta, summary="Obtener categoría (todos los roles)",
              responses=C_RESP_404)
def c_obtener_categoria(id_categoria: int = Path(gt=0), _=Depends(c_todos)):
    return c_servicio.c_obtener_categoria(id_categoria)


@c_router.post("", response_model=CCategoriaRespuesta, status_code=status.HTTP_201_CREATED,
               summary="Crear categoría (ADMIN)", responses=C_RESP_409)
def c_crear_categoria(c_datos: CCategoriaCrear, _=Depends(c_solo_admin)):
    return c_servicio.c_crear_categoria(c_datos)


@c_router.put("/{id_categoria}", response_model=CCategoriaRespuesta, summary="Actualizar categoría (ADMIN)",
              responses={**C_RESP_400, **C_RESP_404, **C_RESP_409})
def c_actualizar_categoria(c_datos: CCategoriaActualizar, id_categoria: int = Path(gt=0), _=Depends(c_solo_admin)):
    return c_servicio.c_actualizar_categoria(id_categoria, c_datos)


@c_router.delete("/{id_categoria}", response_model=CResultadoEliminacion, summary="Eliminar categoría (ADMIN)",
                 description="Si tiene productos asociados se inactiva (borrado lógico).", responses=C_RESP_404)
def c_eliminar_categoria(id_categoria: int = Path(gt=0), _=Depends(c_solo_admin)):
    return c_servicio.c_eliminar_categoria(id_categoria)
