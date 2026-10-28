from app.models.c_colecciones import C_PRODUCTOS
from app.repositories.c_base_repository import CRepositorioBase


class CProductoRepositorio(CRepositorioBase):
    def __init__(self) -> None:
        super().__init__(C_PRODUCTOS)


c_producto_repo = CProductoRepositorio()
