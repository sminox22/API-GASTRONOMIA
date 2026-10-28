from fastapi import APIRouter, Depends, Path, Query, status

from app.core.c_dependencias import c_requiere_roles
from app.models.c_enums import CEstado, CRol
from app.schemas.c_comun_schemas import C_RESP_400, C_RESP_404, C_RESP_409, C_RESP_AUTH, CResultadoEliminacion
from app.schemas.c_usuario_schemas import CUsuarioActualizar, CUsuarioCrear, CUsuarioRespuesta
from app.services import c_usuario_service as c_servicio

c_router = APIRouter(prefix="/usuarios", tags=["Usuarios"], responses=C_RESP_AUTH)
c_solo_admin = c_requiere_roles(CRol.ADMIN)


@c_router.get("", response_model=list[CUsuarioRespuesta], summary="Listar usuarios (ADMIN)")
def c_listar_usuarios(
    rol: CRol | None = Query(None, description="Filtrar por rol"),
    estado: CEstado | None = Query(None, description="Filtrar por estado"),
    omitir: int = Query(0, ge=0, description="Registros a omitir (paginación)"),
    limite: int = Query(100, ge=1, le=500, description="Máximo de registros"),
    _=Depends(c_solo_admin),
):
    return c_servicio.c_listar_usuarios(rol and rol.value, estado and estado.value, omitir, limite)


@c_router.get("/{id_usuario}", response_model=CUsuarioRespuesta, summary="Obtener un usuario (ADMIN)",
              responses=C_RESP_404)
def c_obtener_usuario(id_usuario: int = Path(gt=0), _=Depends(c_solo_admin)):
    return c_servicio.c_obtener_usuario(id_usuario)


@c_router.post("", response_model=CUsuarioRespuesta, status_code=status.HTTP_201_CREATED,
               summary="Crear usuario (ADMIN)", responses=C_RESP_409)
def c_crear_usuario(c_datos: CUsuarioCrear, _=Depends(c_solo_admin)):
    return c_servicio.c_crear_usuario(c_datos)


@c_router.put("/{id_usuario}", response_model=CUsuarioRespuesta, summary="Actualizar usuario (ADMIN)",
              description="Solo se modifican los campos enviados. Si se envía password se cifra de nuevo.",
              responses={**C_RESP_400, **C_RESP_404, **C_RESP_409})
def c_actualizar_usuario(c_datos: CUsuarioActualizar, id_usuario: int = Path(gt=0), _=Depends(c_solo_admin)):
    return c_servicio.c_actualizar_usuario(id_usuario, c_datos)


@c_router.delete("/{id_usuario}", response_model=CResultadoEliminacion, summary="Eliminar usuario (ADMIN)",
                 description="Si el usuario registró pedidos o compras se inactiva (borrado lógico).",
                 responses={**C_RESP_400, **C_RESP_404})
def c_eliminar_usuario(id_usuario: int = Path(gt=0), c_usuario: dict = Depends(c_solo_admin)):
    return c_servicio.c_eliminar_usuario(id_usuario, c_usuario)
