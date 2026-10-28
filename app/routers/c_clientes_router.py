from fastapi import APIRouter, Depends, Path, Query, status

from app.core.c_dependencias import c_requiere_roles
from app.models.c_enums import CEstado, CRol, CTipoCliente
from app.schemas.c_cliente_schemas import CClienteActualizar, CClienteCrear, CClienteRespuesta
from app.schemas.c_comun_schemas import C_RESP_400, C_RESP_404, C_RESP_409, C_RESP_AUTH, CResultadoEliminacion
from app.schemas.c_pedido_schemas import CPedidoRespuesta
from app.services import c_cliente_service as c_servicio

c_router = APIRouter(prefix="/clientes", tags=["Clientes"], responses=C_RESP_AUTH)
c_permitidos = c_requiere_roles(CRol.ADMIN, CRol.CAJERO)


@c_router.get("", response_model=list[CClienteRespuesta], summary="Listar clientes (ADMIN, CAJERO)")
def c_listar_clientes(
    tipo_cliente: CTipoCliente | None = Query(None),
    estado: CEstado | None = Query(None),
    omitir: int = Query(0, ge=0),
    limite: int = Query(100, ge=1, le=500),
    _=Depends(c_permitidos),
):
    return c_servicio.c_listar_clientes(tipo_cliente and tipo_cliente.value, estado and estado.value, omitir, limite)


@c_router.get("/{id_cliente}", response_model=CClienteRespuesta, summary="Obtener cliente (ADMIN, CAJERO)",
              responses=C_RESP_404)
def c_obtener_cliente(id_cliente: int = Path(gt=0), _=Depends(c_permitidos)):
    return c_servicio.c_obtener_cliente(id_cliente)


@c_router.get("/{id_cliente}/pedidos", response_model=list[CPedidoRespuesta],
              summary="Historial de pedidos de un cliente (ADMIN, CAJERO)", responses=C_RESP_404)
def c_pedidos_cliente(id_cliente: int = Path(gt=0), _=Depends(c_permitidos)):
    return c_servicio.c_pedidos_de_cliente(id_cliente)


@c_router.post("", response_model=CClienteRespuesta, status_code=status.HTTP_201_CREATED,
               summary="Crear cliente (ADMIN, CAJERO)", responses=C_RESP_409)
def c_crear_cliente(c_datos: CClienteCrear, _=Depends(c_permitidos)):
    return c_servicio.c_crear_cliente(c_datos)


@c_router.put("/{id_cliente}", response_model=CClienteRespuesta, summary="Actualizar cliente (ADMIN, CAJERO)",
              responses={**C_RESP_400, **C_RESP_404, **C_RESP_409})
def c_actualizar_cliente(c_datos: CClienteActualizar, id_cliente: int = Path(gt=0), _=Depends(c_permitidos)):
    return c_servicio.c_actualizar_cliente(id_cliente, c_datos)


@c_router.delete("/{id_cliente}", response_model=CResultadoEliminacion, summary="Eliminar cliente (ADMIN, CAJERO)",
                 description="RN04: si tiene pedidos se cambia a INACTIVO (borrado lógico).", responses=C_RESP_404)
def c_eliminar_cliente(id_cliente: int = Path(gt=0), _=Depends(c_permitidos)):
    return c_servicio.c_eliminar_cliente(id_cliente)
