from fastapi import APIRouter, Depends, Path, Query, status

from app.core.c_dependencias import C_TODOS, c_requiere_roles
from app.models.c_enums import CEstadoProducto, CRol
from app.schemas.c_comun_schemas import C_RESP_400, C_RESP_404, C_RESP_409, C_RESP_AUTH, CResultadoEliminacion
from app.schemas.c_producto_schemas import (CCostoProductoRespuesta, CProductoActualizar, CProductoCrear,
                                            CProductoRespuesta, CRecetaProductoRespuesta)
from app.services import c_producto_service as c_servicio

c_router = APIRouter(prefix="/productos", tags=["Productos"], responses=C_RESP_AUTH)
c_solo_admin = c_requiere_roles(CRol.ADMIN)
c_todos = c_requiere_roles(*C_TODOS)


@c_router.get("", response_model=list[CProductoRespuesta], summary="Listar productos (todos los roles)")
def c_listar_productos(
    estado: CEstadoProducto | None = Query(None),
    omitir: int = Query(0, ge=0),
    limite: int = Query(100, ge=1, le=500),
    _=Depends(c_todos),
):
    return c_servicio.c_listar_productos(estado and estado.value, omitir, limite)


@c_router.get("/categoria/{id_categoria}", response_model=list[CProductoRespuesta],
              summary="Productos de una categoría (todos los roles)", responses=C_RESP_404)
def c_productos_por_categoria(id_categoria: int = Path(gt=0), _=Depends(c_todos)):
    return c_servicio.c_listar_por_categoria(id_categoria)


@c_router.get("/{id_producto}", response_model=CProductoRespuesta, summary="Obtener producto (todos los roles)",
              responses=C_RESP_404)
def c_obtener_producto(id_producto: int = Path(gt=0), _=Depends(c_todos)):
    return c_servicio.c_obtener_producto(id_producto)


@c_router.get("/{id_producto}/receta", response_model=CRecetaProductoRespuesta,
              summary="Receta (ficha técnica) del producto (todos los roles)",
              description="Insumos y cantidades por unidad de producto, con el costo de cada insumo.",
              responses=C_RESP_404)
def c_receta_producto(id_producto: int = Path(gt=0), _=Depends(c_todos)):
    return c_servicio.c_obtener_receta_producto(id_producto)


@c_router.get("/{id_producto}/costo", response_model=CCostoProductoRespuesta,
              summary="Costo de producción y margen (ADMIN, COCINERO)",
              description="Costo = Σ (cantidad × costo_unitario) de la receta. Margen = precio_venta − costo.",
              responses=C_RESP_404)
def c_costo_producto(id_producto: int = Path(gt=0), _=Depends(c_requiere_roles(CRol.ADMIN, CRol.COCINERO))):
    return c_servicio.c_calcular_costo_producto(id_producto)


@c_router.post("", response_model=CProductoRespuesta, status_code=status.HTTP_201_CREATED,
               summary="Crear producto (ADMIN)", responses={**C_RESP_404, **C_RESP_409})
def c_crear_producto(c_datos: CProductoCrear, _=Depends(c_solo_admin)):
    return c_servicio.c_crear_producto(c_datos)


@c_router.put("/{id_producto}", response_model=CProductoRespuesta, summary="Actualizar producto (ADMIN)",
              responses={**C_RESP_400, **C_RESP_404, **C_RESP_409})
def c_actualizar_producto(c_datos: CProductoActualizar, id_producto: int = Path(gt=0), _=Depends(c_solo_admin)):
    return c_servicio.c_actualizar_producto(id_producto, c_datos)


@c_router.delete("/{id_producto}", response_model=CResultadoEliminacion, summary="Eliminar producto (ADMIN)",
                 description="RN04: si el producto tiene pedidos se cambia a INACTIVO (borrado lógico).",
                 responses=C_RESP_404)
def c_eliminar_producto(id_producto: int = Path(gt=0), _=Depends(c_solo_admin)):
    return c_servicio.c_eliminar_producto(id_producto)
