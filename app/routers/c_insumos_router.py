from fastapi import APIRouter, Depends, Path, Query, status

from app.core.c_dependencias import c_requiere_roles
from app.models.c_enums import CEstado, CRol
from app.schemas.c_comun_schemas import C_RESP_400, C_RESP_404, C_RESP_409, C_RESP_AUTH, CResultadoEliminacion
from app.schemas.c_insumo_schemas import CInsumoActualizar, CInsumoCrear, CInsumoPorVencer, CInsumoRespuesta
from app.services import c_insumo_service as c_servicio

c_router = APIRouter(prefix="/insumos", tags=["Insumos"], responses=C_RESP_AUTH)
c_permitidos = c_requiere_roles(CRol.ADMIN, CRol.COCINERO)


@c_router.get("", response_model=list[CInsumoRespuesta], summary="Listar insumos (ADMIN, COCINERO)")
def c_listar_insumos(
    estado: CEstado | None = Query(None),
    omitir: int = Query(0, ge=0),
    limite: int = Query(100, ge=1, le=500),
    _=Depends(c_permitidos),
):
    return c_servicio.c_listar_insumos(estado and estado.value, omitir, limite)


@c_router.get("/stock-bajo", response_model=list[CInsumoRespuesta],
              summary="Insumos con stock_actual <= stock_minimo (ADMIN, COCINERO)")
def c_stock_bajo(_=Depends(c_permitidos)):
    return c_servicio.c_insumos_stock_bajo()


@c_router.get("/por-vencer", response_model=list[CInsumoPorVencer],
              summary="Insumos que vencen en los próximos N días (ADMIN, COCINERO)")
def c_por_vencer(dias: int = Query(7, ge=0, le=365, description="Días a partir de hoy"),
                 _=Depends(c_permitidos)):
    return c_servicio.c_insumos_por_vencer(dias)


@c_router.get("/{id_insumo}", response_model=CInsumoRespuesta, summary="Obtener insumo (ADMIN, COCINERO)",
              responses=C_RESP_404)
def c_obtener_insumo(id_insumo: int = Path(gt=0), _=Depends(c_permitidos)):
    return c_servicio.c_obtener_insumo(id_insumo)


@c_router.post("", response_model=CInsumoRespuesta, status_code=status.HTTP_201_CREATED,
               summary="Crear insumo (ADMIN, COCINERO)", responses=C_RESP_409)
def c_crear_insumo(c_datos: CInsumoCrear, _=Depends(c_permitidos)):
    return c_servicio.c_crear_insumo(c_datos)


@c_router.put("/{id_insumo}", response_model=CInsumoRespuesta, summary="Actualizar insumo (ADMIN, COCINERO)",
              responses={**C_RESP_400, **C_RESP_404, **C_RESP_409})
def c_actualizar_insumo(c_datos: CInsumoActualizar, id_insumo: int = Path(gt=0), _=Depends(c_permitidos)):
    return c_servicio.c_actualizar_insumo(id_insumo, c_datos)


@c_router.delete("/{id_insumo}", response_model=CResultadoEliminacion, summary="Eliminar insumo (ADMIN, COCINERO)",
                 description="RN04: si está en compras o recetas se cambia a INACTIVO (borrado lógico).",
                 responses=C_RESP_404)
def c_eliminar_insumo(id_insumo: int = Path(gt=0), _=Depends(c_permitidos)):
    return c_servicio.c_eliminar_insumo(id_insumo)
