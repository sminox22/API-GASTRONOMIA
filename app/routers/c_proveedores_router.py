from fastapi import APIRouter, Depends, Path, Query, status

from app.core.c_dependencias import c_requiere_roles
from app.models.c_enums import CEstado, CRol
from app.schemas.c_comun_schemas import C_RESP_400, C_RESP_404, C_RESP_409, C_RESP_AUTH, CResultadoEliminacion
from app.schemas.c_compra_schemas import CCompraRespuesta
from app.schemas.c_proveedor_schemas import CProveedorActualizar, CProveedorCrear, CProveedorRespuesta
from app.services import c_proveedor_service as c_servicio

c_router = APIRouter(prefix="/proveedores", tags=["Proveedores"], responses=C_RESP_AUTH)
c_solo_admin = c_requiere_roles(CRol.ADMIN)


@c_router.get("", response_model=list[CProveedorRespuesta], summary="Listar proveedores (ADMIN)")
def c_listar_proveedores(
    estado: CEstado | None = Query(None),
    omitir: int = Query(0, ge=0),
    limite: int = Query(100, ge=1, le=500),
    _=Depends(c_solo_admin),
):
    return c_servicio.c_listar_proveedores(estado and estado.value, omitir, limite)


@c_router.get("/{id_proveedor}", response_model=CProveedorRespuesta, summary="Obtener proveedor (ADMIN)",
              responses=C_RESP_404)
def c_obtener_proveedor(id_proveedor: int = Path(gt=0), _=Depends(c_solo_admin)):
    return c_servicio.c_obtener_proveedor(id_proveedor)


@c_router.get("/{id_proveedor}/compras", response_model=list[CCompraRespuesta],
              summary="Historial de compras a un proveedor (ADMIN)", responses=C_RESP_404)
def c_compras_proveedor(id_proveedor: int = Path(gt=0), _=Depends(c_solo_admin)):
    return c_servicio.c_compras_de_proveedor(id_proveedor)


@c_router.post("", response_model=CProveedorRespuesta, status_code=status.HTTP_201_CREATED,
               summary="Crear proveedor (ADMIN)", responses=C_RESP_409)
def c_crear_proveedor(c_datos: CProveedorCrear, _=Depends(c_solo_admin)):
    return c_servicio.c_crear_proveedor(c_datos)


@c_router.put("/{id_proveedor}", response_model=CProveedorRespuesta, summary="Actualizar proveedor (ADMIN)",
              responses={**C_RESP_400, **C_RESP_404, **C_RESP_409})
def c_actualizar_proveedor(c_datos: CProveedorActualizar, id_proveedor: int = Path(gt=0), _=Depends(c_solo_admin)):
    return c_servicio.c_actualizar_proveedor(id_proveedor, c_datos)


@c_router.delete("/{id_proveedor}", response_model=CResultadoEliminacion, summary="Eliminar proveedor (ADMIN)",
                 description="RN04: si tiene compras se cambia a INACTIVO (borrado lógico).", responses=C_RESP_404)
def c_eliminar_proveedor(id_proveedor: int = Path(gt=0), _=Depends(c_solo_admin)):
    return c_servicio.c_eliminar_proveedor(id_proveedor)
