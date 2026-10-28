from fastapi import APIRouter, Depends, Path, Query, status

from app.core.c_dependencias import c_requiere_roles
from app.models.c_enums import CRol
from app.schemas.c_comun_schemas import C_RESP_400, C_RESP_404, C_RESP_409, C_RESP_AUTH, CResultadoEliminacion
from app.schemas.c_compra_schemas import CCompraActualizar, CCompraCrear, CCompraRespuesta
from app.services import c_compra_service as c_servicio

c_router = APIRouter(prefix="/compras", tags=["Compras"], responses=C_RESP_AUTH)
c_solo_admin = c_requiere_roles(CRol.ADMIN)


@c_router.get("", response_model=list[CCompraRespuesta], summary="Listar compras (ADMIN)")
def c_listar_compras(
    id_proveedor: int | None = Query(None, gt=0),
    omitir: int = Query(0, ge=0),
    limite: int = Query(100, ge=1, le=500),
    _=Depends(c_solo_admin),
):
    return c_servicio.c_listar_compras(id_proveedor, omitir, limite)


@c_router.get("/{id_compra}", response_model=CCompraRespuesta, summary="Obtener compra con su detalle (ADMIN)",
              responses=C_RESP_404)
def c_obtener_compra(id_compra: int = Path(gt=0), _=Depends(c_solo_admin)):
    return c_servicio.c_obtener_compra(id_compra)


@c_router.post("", response_model=CCompraRespuesta, status_code=status.HTTP_201_CREATED,
               summary="Registrar compra de insumos (ADMIN)",
               description="RN02: incrementa el stock_actual de cada insumo y actualiza su costo_unitario. "
                           "Subtotales y total los calcula la API.",
               responses={**C_RESP_404, **C_RESP_409})
def c_crear_compra(c_datos: CCompraCrear, c_usuario: dict = Depends(c_solo_admin)):
    return c_servicio.c_crear_compra(c_datos, c_usuario)


@c_router.put("/{id_compra}", response_model=CCompraRespuesta, summary="Actualizar encabezado de la compra (ADMIN)",
              description="Solo número de factura, proveedor y fecha. El detalle no se edita porque ya afectó el inventario.",
              responses={**C_RESP_400, **C_RESP_404, **C_RESP_409})
def c_actualizar_compra(c_datos: CCompraActualizar, id_compra: int = Path(gt=0), _=Depends(c_solo_admin)):
    return c_servicio.c_actualizar_compra(id_compra, c_datos)


@c_router.delete("/{id_compra}", response_model=CResultadoEliminacion, summary="Eliminar compra (ADMIN)",
                 description="Revierte las existencias sumadas. Si ya se consumieron responde 409.",
                 responses={**C_RESP_404, **C_RESP_409})
def c_eliminar_compra(id_compra: int = Path(gt=0), _=Depends(c_solo_admin)):
    return c_servicio.c_eliminar_compra(id_compra)
