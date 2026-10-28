from app.models.c_colecciones import C_USUARIOS
from app.repositories.c_base_repository import CRepositorioBase


class CUsuarioRepositorio(CRepositorioBase):
    # RN06: la contraseña nunca sale del repositorio en las consultas normales
    c_proyeccion = {"_id": 0, "password": 0}

    def __init__(self) -> None:
        super().__init__(C_USUARIOS)

    def c_buscar_con_password(self, c_correo: str) -> dict | None:
        """Único método que devuelve el hash, usado solo para el login."""
        return self.c_col.find_one({"correo": c_correo.lower()}, {"_id": 0})


c_usuario_repo = CUsuarioRepositorio()
