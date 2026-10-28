"""Dependencias de FastAPI: usuario autenticado (401) y control de roles (403)."""
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.c_security import c_decodificar_token
from app.models.c_enums import CRol
from app.repositories.c_usuario_repository import c_usuario_repo

c_esquema_bearer = HTTPBearer(
    auto_error=False,
    scheme_name="JWT",
    description="Token obtenido en POST /api/v1/auth/login. Encabezado: Authorization: Bearer <token>",
)


def c_no_autenticado(c_mensaje: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=c_mensaje,
        headers={"WWW-Authenticate": "Bearer"},
    )


def c_usuario_actual(
    c_credenciales: HTTPAuthorizationCredentials | None = Depends(c_esquema_bearer),
) -> dict:
    if c_credenciales is None or c_credenciales.scheme.lower() != "bearer":
        raise c_no_autenticado("No se envió el token de acceso")
    try:
        c_payload = c_decodificar_token(c_credenciales.credentials)
    except jwt.ExpiredSignatureError:
        raise c_no_autenticado("El token ha expirado")
    except jwt.InvalidTokenError:
        raise c_no_autenticado("Token inválido")

    c_usuario = c_usuario_repo.c_obtener(int(c_payload["sub"]))
    if c_usuario is None or c_usuario["estado"] != "ACTIVO":
        raise c_no_autenticado("El usuario del token no existe o está inactivo")
    return c_usuario


def c_requiere_roles(*c_roles: CRol):
    """Uso: Depends(c_requiere_roles(CRol.ADMIN, CRol.CAJERO))"""
    c_permitidos = {c_rol.value for c_rol in c_roles}

    def c_verificar_rol(c_usuario: dict = Depends(c_usuario_actual)) -> dict:
        if c_usuario["rol"] not in c_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"El rol {c_usuario['rol']} no tiene permiso para esta operación",
            )
        return c_usuario

    return c_verificar_rol


C_TODOS = (CRol.ADMIN, CRol.CAJERO, CRol.COCINERO)
