from app.models.c_colecciones import C_COMPRAS
from app.repositories.c_base_repository import CRepositorioBase


class CCompraRepositorio(CRepositorioBase):
    def __init__(self) -> None:
        super().__init__(C_COMPRAS)


c_compra_repo = CCompraRepositorio()
