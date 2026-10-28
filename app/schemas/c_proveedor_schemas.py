from pydantic import EmailStr, Field

from app.models.c_enums import CEstado
from app.schemas.c_comun_schemas import CEsquemaBase


class CProveedorCrear(CEsquemaBase):
    nit: str = Field(min_length=5, max_length=20, examples=["900100099-1"])
    razon_social: str = Field(min_length=2, max_length=120, examples=["Verduras del Valle S.A.S."])
    telefono: str | None = Field(None, max_length=20, examples=["3109998877"])
    correo: EmailStr | None = Field(None, max_length=120, examples=["ventas@verdurasvalle.com"])
    direccion: str | None = Field(None, max_length=150, examples=["Cra 7 # 8-90 Neiva"])
    estado: CEstado = CEstado.ACTIVO


class CProveedorActualizar(CEsquemaBase):
    nit: str | None = Field(None, min_length=5, max_length=20)
    razon_social: str | None = Field(None, min_length=2, max_length=120)
    telefono: str | None = Field(None, max_length=20)
    correo: EmailStr | None = Field(None, max_length=120)
    direccion: str | None = Field(None, max_length=150)
    estado: CEstado | None = None


class CProveedorRespuesta(CProveedorCrear):
    id_proveedor: int
    correo: str | None = None
