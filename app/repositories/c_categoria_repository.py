from app.models.c_colecciones import C_CATEGORIAS
from app.repositories.c_base_repository import CRepositorioBase


class CCategoriaRepositorio(CRepositorioBase):
    def __init__(self) -> None:
        super().__init__(C_CATEGORIAS)


c_categoria_repo = CCategoriaRepositorio()
