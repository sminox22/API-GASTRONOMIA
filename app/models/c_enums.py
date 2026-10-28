"""Valores permitidos (equivalentes a los ENUM de SQL y a los enum del $jsonSchema)."""
from enum import Enum


class CRol(str, Enum):
    ADMIN = "ADMIN"
    CAJERO = "CAJERO"
    COCINERO = "COCINERO"


class CEstado(str, Enum):
    ACTIVO = "ACTIVO"
    INACTIVO = "INACTIVO"


class CEstadoProducto(str, Enum):
    DISPONIBLE = "DISPONIBLE"
    AGOTADO = "AGOTADO"
    INACTIVO = "INACTIVO"


class CUnidadMedida(str, Enum):
    g = "g"
    kg = "kg"
    ml = "ml"
    l = "l"
    lb = "lb"
    unidad = "unidad"


class CTipoCliente(str, Enum):
    APRENDIZ = "APRENDIZ"
    INSTRUCTOR = "INSTRUCTOR"
    FUNCIONARIO = "FUNCIONARIO"
    EXTERNO = "EXTERNO"


class CTipoPedido(str, Enum):
    MESA = "MESA"
    PARA_LLEVAR = "PARA_LLEVAR"
    EVENTO = "EVENTO"


class CEstadoPedido(str, Enum):
    PENDIENTE = "PENDIENTE"
    EN_PREPARACION = "EN_PREPARACION"
    ENTREGADO = "ENTREGADO"
    ANULADO = "ANULADO"
