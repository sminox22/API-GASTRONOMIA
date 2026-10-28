from pydantic import EmailStr, Field

from app.models.c_enums import CEstado, CTipoCliente
from app.schemas.c_comun_schemas import CEsquemaBase


class CClienteCrear(CEsquemaBase):
    identificacion: str = Field(min_length=5, max_length=20, examples=["1080100099"])
    nombres: str = Field(min_length=2, max_length=80, examples=["Sofía"])
    apellidos: str = Field(min_length=2, max_length=80, examples=["Polanía Rivera"])
    telefono: str | None = Field(None, max_length=20, examples=["3205556677"])
    correo: EmailStr | None = Field(None, max_length=120, examples=["spolania@soy.sena.edu.co"])
    tipo_cliente: CTipoCliente = Field(examples=["APRENDIZ"])
    estado: CEstado = CEstado.ACTIVO


class CClienteActualizar(CEsquemaBase):
    identificacion: str | None = Field(None, min_length=5, max_length=20)
    nombres: str | None = Field(None, min_length=2, max_length=80)
    apellidos: str | None = Field(None, min_length=2, max_length=80)
    telefono: str | None = Field(None, max_length=20)
    correo: EmailStr | None = Field(None, max_length=120)
    tipo_cliente: CTipoCliente | None = None
    estado: CEstado | None = None


class CClienteRespuesta(CClienteCrear):
    id_cliente: int
    correo: str | None = None
