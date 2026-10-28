from pydantic import BaseModel, EmailStr, Field

from app.schemas.c_usuario_schemas import CUsuarioRespuesta


class CLoginSolicitud(BaseModel):
    correo: EmailStr = Field(examples=["admin@gastronomia.edu.co"])
    password: str = Field(min_length=1, max_length=72, examples=["Gastro2026*"])


class CTokenRespuesta(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expira_en_minutos: int
    usuario: CUsuarioRespuesta
