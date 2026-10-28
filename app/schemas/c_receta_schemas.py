from pydantic import Field

from app.schemas.c_comun_schemas import CEsquemaBase


class CRecetaCrear(CEsquemaBase):
    id_producto: int = Field(gt=0, examples=[1])
    id_insumo: int = Field(gt=0, examples=[6])
    cantidad: float = Field(gt=0, examples=[0.015],
                            description="Cantidad por unidad de producto, en la unidad de medida del insumo")


class CRecetaActualizar(CEsquemaBase):
    id_producto: int | None = Field(None, gt=0)
    id_insumo: int | None = Field(None, gt=0)
    cantidad: float | None = Field(None, gt=0)


class CRecetaRespuesta(CRecetaCrear):
    id_receta: int
