from app.models.c_colecciones import C_PROVEEDORES
from app.repositories.c_base_repository import CRepositorioBase


class CProveedorRepositorio(CRepositorioBase):
    def __init__(self) -> None:
        super().__init__(C_PROVEEDORES)


c_proveedor_repo = CProveedorRepositorio()
