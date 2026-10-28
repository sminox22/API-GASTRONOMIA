from app.models.c_colecciones import C_CLIENTES
from app.repositories.c_base_repository import CRepositorioBase


class CClienteRepositorio(CRepositorioBase):
    def __init__(self) -> None:
        super().__init__(C_CLIENTES)


c_cliente_repo = CClienteRepositorio()
