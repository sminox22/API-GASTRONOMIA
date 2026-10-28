from fastapi import APIRouter, Depends, Path, Query, status

from app.core.c_dependencias import c_requiere_roles
from app.models.c_enums import CEstadoPedido, CRol
from app.schemas.c_comun_schemas import C_RESP_400, C_RESP_404, C_RESP_409, C_RESP_AUTH, CResultadoEliminacion
from app.schemas.c_pedido_schemas import (CCambioEstadoRespuesta, CPedidoActualizar, CPedidoCambioEstado,
                                          CPedidoCrear, CPedidoRespuesta)
from app.services import c_pedido_service as c_servicio

c_router = APIRouter(prefix="/pedidos", tags=["Pedidos"], responses=C_RESP_AUTH)
c_gestion = c_requiere_roles(CRol.ADMIN, CRol.CAJERO)
c_consulta = c_requiere_roles(CRol.ADMIN, CRol.CAJERO, CRol.COCINERO)


@c_router.get("", response_model=list[CPedidoRespuesta], summary="Listar pedidos (ADMIN, CAJERO, COCINERO)")
def c_listar_pedidos(
    estado: CEstadoPedido | None = Query(None),
    id_cliente: int | None = Query(None, gt=0),
    omitir: int = Query(0, ge=0),
    limite: int = Query(100, ge=1, le=500),
    _=Depends(c_consulta),
):
    return c_servicio.c_listar_pedidos(estado and estado.value, id_cliente, omitir, limite)


@c_router.get("/estado/{estado}", response_model=list[CPedidoRespuesta],
              summary="Pedidos filtrados por estado (ADMIN, CAJERO, COCINERO)",
              description="Ordenados del más antiguo al más reciente (cola de cocina).")
def c_pedidos_por_estado(estado: CEstadoPedido, _=Depends(c_consulta)):
    return c_servicio.c_pedidos_por_estado(estado.value)


@c_router.get("/{id_pedido}", response_model=CPedidoRespuesta, summary="Obtener pedido (ADMIN, CAJERO, COCINERO)",
              responses=C_RESP_404)
def c_obtener_pedido(id_pedido: int = Path(gt=0), _=Depends(c_consulta)):
    return c_servicio.c_obtener_pedido(id_pedido)


@c_router.post("", response_model=CPedidoRespuesta, status_code=status.HTTP_201_CREATED,
               summary="Registrar pedido (ADMIN, CAJERO)",
               description="RN01: la API toma el precio de cada producto, calcula subtotales y total. "
                           "El pedido inicia en PENDIENTE.",
               responses={**C_RESP_404, **C_RESP_409})
def c_crear_pedido(c_datos: CPedidoCrear, c_usuario: dict = Depends(c_gestion)):
    return c_servicio.c_crear_pedido(c_datos, c_usuario)


@c_router.put("/{id_pedido}", response_model=CPedidoRespuesta, summary="Actualizar pedido (ADMIN, CAJERO)",
              description="RN05: un pedido ENTREGADO o ANULADO no puede modificarse (409). Si cambia el detalle se recalcula el total.",
              responses={**C_RESP_400, **C_RESP_404, **C_RESP_409})
def c_actualizar_pedido(c_datos: CPedidoActualizar, id_pedido: int = Path(gt=0), _=Depends(c_gestion)):
    return c_servicio.c_actualizar_pedido(id_pedido, c_datos)


@c_router.patch("/{id_pedido}/estado", response_model=CCambioEstadoRespuesta,
                summary="Cambiar estado del pedido (ADMIN, CAJERO, COCINERO)",
                description="Transiciones: PENDIENTE → EN_PREPARACION | ENTREGADO | ANULADO; "
                            "EN_PREPARACION → ENTREGADO | ANULADO. "
                            "RN03: al pasar a ENTREGADO descuenta los insumos según la receta (409 si no alcanzan). "
                            "RN05: ENTREGADO y ANULADO son estados finales. COCINERO no puede anular.",
                responses={**C_RESP_400, **C_RESP_404, **C_RESP_409})
def c_cambiar_estado(c_datos: CPedidoCambioEstado, id_pedido: int = Path(gt=0), c_usuario: dict = Depends(c_consulta)):
    return c_servicio.c_cambiar_estado(id_pedido, c_datos.estado, c_usuario)


@c_router.delete("/{id_pedido}", response_model=CResultadoEliminacion, summary="Anular pedido (ADMIN, CAJERO)",
                 description="Los pedidos no se borran físicamente: se cambian a ANULADO. RN05 aplica (409).",
                 responses={**C_RESP_404, **C_RESP_409})
def c_eliminar_pedido(id_pedido: int = Path(gt=0), _=Depends(c_gestion)):
    return c_servicio.c_eliminar_pedido(id_pedido)
