"""RF01: autenticación con correo y contraseña."""
from app.core.c_config import c_config
from app.core.c_excepciones import CNoAutorizado
from app.core.c_security import c_crear_token, c_verificar_password
from app.repositories.c_usuario_repository import c_usuario_repo


def c_iniciar_sesion(c_correo: str, c_password: str) -> dict:
    c_usuario = c_usuario_repo.c_buscar_con_password(c_correo)
    # Mismo mensaje para correo o contraseña incorrectos (no se revela cuál falló)
    if c_usuario is None or not c_verificar_password(c_password, c_usuario["password"]):
        raise CNoAutorizado("Correo o contraseña incorrectos")
    if c_usuario["estado"] != "ACTIVO":
        raise CNoAutorizado("El usuario está inactivo")

    c_usuario.pop("password")  # RN06
    return {
        "access_token": c_crear_token(c_usuario),
        "token_type": "bearer",
        "expira_en_minutos": c_config.c_jwt_minutos_expiracion,
        "usuario": c_usuario,
    }
