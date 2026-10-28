from fastapi import APIRouter, Depends, Path, Query, status

from app.core.c_dependencias import c_requiere_roles
from app.models.c_enums import CRol
from app.schemas.c_calificacion_schemas import (CCalificacionActualizar, CCalificacionCrear,
                                                CCalificacionesProductoRespuesta, CCalificacionRespuesta)
from app.schemas.c_comun_schemas import C_RESP_400, C_RESP_404, C_RESP_409, C_RESP_AUTH, CResultadoEliminacion
from app.services import c_calificacion_service as c_servicio

c_router = APIRouter(prefix="/calificaciones", tags=["Calificaciones"], responses=C_RESP_AUTH)
c_permitidos = c_requiere_roles(CRol.ADMIN, CRol.CAJERO)


@c_router.get("", response_model=list[CCalificacionRespuesta], summary="Listar calificaciones (ADMIN, CAJERO)")
def c_listar_calificaciones(
    id_cliente: int | None = Query(None, gt=0),
    omitir: int = Query(0, ge=0),
    limite: int = Query(100, ge=1, le=500),
    _=Depends(c_permitidos),
):
    return c_servicio.c_listar_calificaciones(id_cliente, omitir, limite)


@c_router.get("/producto/{id_producto}", response_model=CCalificacionesProductoRespuesta,
              summary="Calificaciones y promedio de un producto (ADMIN, CAJERO)", responses=C_RESP_404)
def c_calificaciones_producto(id_producto: int = Path(gt=0), _=Depends(c_permitidos)):
    return c_servicio.c_calificaciones_de_producto(id_producto)


@c_router.get("/{id_calificacion}", response_model=CCalificacionRespuesta,
              summary="Obtener calificación (ADMIN, CAJERO)", responses=C_RESP_404)
def c_obtener_calificacion(id_calificacion: int = Path(gt=0), _=Depends(c_permitidos)):
    return c_servicio.c_obtener_calificacion(id_calificacion)


@c_router.post("", response_model=CCalificacionRespuesta, status_code=status.HTTP_201_CREATED,
               summary="Registrar calificación de un pedido (ADMIN, CAJERO)",
               description="Solo pedidos ENTREGADOS y una calificación por pedido. El cliente se toma del pedido.",
               responses={**C_RESP_400, **C_RESP_404, **C_RESP_409})
def c_crear_calificacion(c_datos: CCalificacionCrear, _=Depends(c_permitidos)):
    return c_servicio.c_crear_calificacion(c_datos)


@c_router.put("/{id_calificacion}", response_model=CCalificacionRespuesta,
              summary="Actualizar calificación (ADMIN, CAJERO)", responses={**C_RESP_400, **C_RESP_404})
def c_actualizar_calificacion(c_datos: CCalificacionActualizar, id_calificacion: int = Path(gt=0),
                              _=Depends(c_permitidos)):
    return c_servicio.c_actualizar_calificacion(id_calificacion, c_datos)


@c_router.delete("/{id_calificacion}", response_model=CResultadoEliminacion,
                 summary="Eliminar calificación (ADMIN, CAJERO)", responses=C_RESP_404)
def c_eliminar_calificacion(id_calificacion: int = Path(gt=0), _=Depends(c_permitidos)):
    return c_servicio.c_eliminar_calificacion(id_calificacion)
