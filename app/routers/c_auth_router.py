from fastapi import APIRouter, Depends, status

from app.core.c_dependencias import c_requiere_roles, c_usuario_actual
from app.models.c_enums import CRol
from app.schemas.c_auth_schemas import CLoginSolicitud, CTokenRespuesta
from app.schemas.c_comun_schemas import C_RESP_409, C_RESP_AUTH, CError
from app.schemas.c_usuario_schemas import CUsuarioCrear, CUsuarioRespuesta
from app.services import c_auth_service, c_usuario_service

c_router = APIRouter(prefix="/auth", tags=["Autenticación"])


@c_router.post(
    "/login",
    response_model=CTokenRespuesta,
    summary="Iniciar sesión (único endpoint público)",
    description="Valida correo y contraseña (bcrypt) y devuelve un token JWT con el rol del usuario y su tiempo de expiración.",
    responses={401: {"model": CError, "description": "Credenciales incorrectas o usuario inactivo"}},
)
def c_login(c_datos: CLoginSolicitud):
    return c_auth_service.c_iniciar_sesion(c_datos.correo, c_datos.password)


@c_router.post(
    "/registro",
    response_model=CUsuarioRespuesta,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un usuario (solo ADMIN)",
    description="Crea un usuario con rol ADMIN, CAJERO o COCINERO. La contraseña se guarda cifrada con bcrypt y nunca se devuelve.",
    responses={**C_RESP_AUTH, **C_RESP_409},
)
def c_registrar(c_datos: CUsuarioCrear, _=Depends(c_requiere_roles(CRol.ADMIN))):
    return c_usuario_service.c_crear_usuario(c_datos)


@c_router.get(
    "/perfil",
    response_model=CUsuarioRespuesta,
    summary="Datos del usuario autenticado",
    responses={401: C_RESP_AUTH[401]},
)
def c_perfil(c_usuario: dict = Depends(c_usuario_actual)):
    return c_usuario
