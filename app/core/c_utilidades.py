"""Funciones de apoyo para fechas (zona America/Bogota) y redondeo."""
from datetime import date, datetime, time
from zoneinfo import ZoneInfo

from app.core.c_config import c_config

C_ZONA = ZoneInfo(c_config.c_zona_horaria)


def c_ahora() -> datetime:
    return datetime.now(C_ZONA)


def c_hoy() -> date:
    return c_ahora().date()


def c_inicio_dia(c_fecha: date) -> datetime:
    return datetime.combine(c_fecha, time.min, C_ZONA)


def c_fin_dia(c_fecha: date) -> datetime:
    return datetime.combine(c_fecha, time.max, C_ZONA)


def c_a_fecha(c_valor):
    """Convierte el datetime guardado en MongoDB a date (hora de Bogotá)."""
    if isinstance(c_valor, datetime):
        if c_valor.tzinfo is not None:
            c_valor = c_valor.astimezone(C_ZONA)
        return c_valor.date()
    return c_valor


def c_fecha_a_datetime(c_fecha: date | None) -> datetime | None:
    """MongoDB no tiene tipo DATE: se guarda la medianoche de Bogotá."""
    return c_inicio_dia(c_fecha) if c_fecha else None


def c_redondear(c_valor: float, c_decimales: int = 2) -> float:
    return round(float(c_valor), c_decimales)
