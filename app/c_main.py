"""Punto de entrada de la API REST de la Unidad Productiva de Gastronomía (CGDSS - SENA)."""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.core.c_excepciones import c_registrar_manejadores
from app.database.c_conexion_mongo import c_cerrar_conexion, c_verificar_conexion
from app.routers import (c_auth_router, c_calificaciones_router, c_categorias_router, c_clientes_router,
                         c_compras_router, c_insumos_router, c_pedidos_router, c_productos_router,
                         c_proveedores_router, c_recetas_router, c_reportes_router, c_usuarios_router)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
c_log = logging.getLogger("api_gastronomia")

C_PREFIJO = "/api/v1"

C_DESCRIPCION = """
API REST para gestionar la información de la **Unidad Productiva de Gastronomía** del
Centro de Gestión y Desarrollo Sostenible Surcolombiano (SENA).

* Base de datos: **MongoDB 7** (`bd_gastronomia`) ejecutada en **Docker Desktop**.
* Seguridad: todos los endpoints requieren **JWT** (`Authorization: Bearer <token>`) excepto `POST /api/v1/auth/login`.
  Responde **401** si no hay token o es inválido y **403** si el rol no tiene permiso.
* Roles: **ADMIN**, **CAJERO**, **COCINERO**.

Usuarios de prueba (contraseña `Gastro2026*`): `admin@gastronomia.edu.co`, `cajero@gastronomia.edu.co`,
`cocinero@gastronomia.edu.co`.
"""


@asynccontextmanager
async def c_ciclo_vida(_: FastAPI):
    if c_verificar_conexion():
        c_log.info("Conexión con MongoDB establecida")
    else:
        c_log.warning("MongoDB no responde todavía; se reintentará en cada solicitud")
    yield
    c_cerrar_conexion()


c_app = FastAPI(
    title="API Gastronomía CGDSS",
    description=C_DESCRIPCION,
    version="1.0.0",
    lifespan=c_ciclo_vida,
    contact={"name": "Aprendiz ADSO - Ficha 3312744"},
)

c_registrar_manejadores(c_app)

for c_modulo in (c_auth_router, c_usuarios_router, c_categorias_router, c_productos_router, c_insumos_router,
                 c_recetas_router, c_proveedores_router, c_compras_router, c_clientes_router, c_pedidos_router,
                 c_reportes_router, c_calificaciones_router):
    c_app.include_router(c_modulo.c_router, prefix=C_PREFIJO)


@c_app.get("/", include_in_schema=False)
def c_inicio():
    return RedirectResponse(url="/docs")
