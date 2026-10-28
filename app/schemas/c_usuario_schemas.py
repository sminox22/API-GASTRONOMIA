from pydantic import EmailStr, Field, field_validator

from app.models.c_enums import CEstado, CRol
from app.schemas.c_comun_schemas import CEsquemaBase


class CUsuarioBase(CEsquemaBase):
    identificacion: str = Field(min_length=5, max_length=20, examples=["1075000099"])
    nombres: str = Field(min_length=2, max_length=80, examples=["Laura"])
    apellidos: str = Field(min_length=2, max_length=80, examples=["Gutiérrez Polanía"])
    correo: EmailStr = Field(max_length=120, examples=["lgutierrez@gastronomia.edu.co"])
    rol: CRol

    @field_validator("correo")
    @classmethod
    def c_correo_minusculas(cls, c_valor: str) -> str:
        return c_valor.lower()


class CUsuarioCrear(CUsuarioBase):
    password: str = Field(min_length=8, max_length=72, examples=["Gastro2026*"])
    estado: CEstado = CEstado.ACTIVO


class CUsuarioActualizar(CEsquemaBase):
    identificacion: str | None = Field(None, min_length=5, max_length=20)
    nombres: str | None = Field(None, min_length=2, max_length=80)
    apellidos: str | None = Field(None, min_length=2, max_length=80)
    correo: EmailStr | None = Field(None, max_length=120)
    password: str | None = Field(None, min_length=8, max_length=72)
    rol: CRol | None = None
    estado: CEstado | None = None

    @field_validator("correo")
    @classmethod
    def c_correo_minusculas(cls, c_valor: str | None) -> str | None:
        return c_valor.lower() if c_valor else c_valor


class CUsuarioRespuesta(CUsuarioBase):
    """RN06: el esquema de respuesta no incluye el campo password."""
    id_usuario: int
    estado: CEstado
