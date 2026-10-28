"""Seguridad: cifrado de contraseñas con bcrypt (RN06) y tokens JWT (RF01)."""
from datetime import timedelta

import bcrypt
import jwt

from app.core.c_config import c_config
from app.core.c_utilidades import c_ahora


def c_cifrar_password(c_password: str) -> str:
    return bcrypt.hashpw(c_password.encode("utf-8"), bcrypt.gensalt(rounds=12)).decode("utf-8")


def c_verificar_password(c_password: str, c_hash: str) -> bool:
    try:
        return bcrypt.checkpw(c_password.encode("utf-8"), c_hash.encode("utf-8"))
    except ValueError:
        return False


def c_crear_token(c_usuario: dict) -> str:
    c_emitido = c_ahora()
    c_payload = {
        "sub": str(c_usuario["id_usuario"]),
        "correo": c_usuario["correo"],
        "rol": c_usuario["rol"],
        "iat": c_emitido,
        "exp": c_emitido + timedelta(minutes=c_config.c_jwt_minutos_expiracion),
    }
    return jwt.encode(c_payload, c_config.c_jwt_secreto, algorithm=c_config.c_jwt_algoritmo)


def c_decodificar_token(c_token: str) -> dict:
    """Lanza jwt.ExpiredSignatureError o jwt.InvalidTokenError si el token no es válido."""
    return jwt.decode(
        c_token,
        c_config.c_jwt_secreto,
        algorithms=[c_config.c_jwt_algoritmo],
        options={"require": ["sub", "exp", "rol"]},
    )
