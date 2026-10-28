from fastapi import APIRouter, Depends, Path, Query, status

from app.core.c_dependencias import c_requiere_roles
from app.models.c_enums import CRol
from app.schemas.c_comun_schemas import C_RESP_400, C_RESP_404, C_RESP_409, C_RESP_AUTH, CResultadoEliminacion
from app.schemas.c_receta_schemas import CRecetaActualizar, CRecetaCrear, CRecetaRespuesta
from app.services import c_receta_service as c_servicio

c_router = APIRouter(prefix="/recetas", tags=["Recetas"], responses=C_RESP_AUTH)
c_permitidos = c_requiere_roles(CRol.ADMIN, CRol.COCINERO)


@c_router.get("", response_model=list[CRecetaRespuesta], summary="Listar ítems de receta (ADMIN, COCINERO)")
def c_listar_recetas(
    id_producto: int | None = Query(None, gt=0, description="Filtrar por producto"),
    omitir: int = Query(0, ge=0),
    limite: int = Query(200, ge=1, le=1000),
    _=Depends(c_permitidos),
):
    return c_servicio.c_listar_recetas(id_producto, omitir, limite)


@c_router.get("/{id_receta}", response_model=CRecetaRespuesta, summary="Obtener ítem de receta (ADMIN, COCINERO)",
              responses=C_RESP_404)
def c_obtener_receta(id_receta: int = Path(gt=0), _=Depends(c_permitidos)):
    return c_servicio.c_obtener_receta(id_receta)


@c_router.post("", response_model=CRecetaRespuesta, status_code=status.HTTP_201_CREATED,
               summary="Agregar insumo a la receta de un producto (ADMIN, COCINERO)",
               description="Un insumo no puede repetirse en la receta de un mismo producto (409).",
               responses={**C_RESP_404, **C_RESP_409})
def c_crear_receta(c_datos: CRecetaCrear, _=Depends(c_permitidos)):
    return c_servicio.c_crear_receta(c_datos)


@c_router.put("/{id_receta}", response_model=CRecetaRespuesta, summary="Actualizar ítem de receta (ADMIN, COCINERO)",
              responses={**C_RESP_400, **C_RESP_404, **C_RESP_409})
def c_actualizar_receta(c_datos: CRecetaActualizar, id_receta: int = Path(gt=0), _=Depends(c_permitidos)):
    return c_servicio.c_actualizar_receta(id_receta, c_datos)


@c_router.delete("/{id_receta}", response_model=CResultadoEliminacion,
                 summary="Eliminar ítem de receta (ADMIN, COCINERO)", responses=C_RESP_404)
def c_eliminar_receta(id_receta: int = Path(gt=0), _=Depends(c_permitidos)):
    return c_servicio.c_eliminar_receta(id_receta)
