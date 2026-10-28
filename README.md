# API REST — Unidad Productiva de Gastronomía (CGDSS · SENA)

Prototipo de API REST con **Python + FastAPI** para gestionar recetas, inventario de insumos, compras,
pedidos, ventas y calificaciones de la Unidad Productiva de Gastronomía del Centro de Gestión y
Desarrollo Sostenible Surcolombiano.

> **Variante del instructivo EA4:** toda la persistencia se hace en **MongoDB 7** (sin MySQL) y la
> infraestructura corre en **Docker Desktop**. Las tablas relacionales del instructivo se modelaron
> como colecciones con validación `$jsonSchema`, índices únicos y referencias por id.

Programa: Análisis y Desarrollo de Software · Ficha 3312744
Prefijo del aprendiz en archivos, clases, funciones y variables: **`c_`**

---

## 1. Requisitos

| Herramienta | Versión | Uso |
|---|---|---|
| Docker Desktop | 4.x (Engine 24+) | Ejecuta MongoDB y la API |
| Imagen `mongo` | 7.0 | Base de datos |
| Imagen `python` | 3.12-slim | Contenedor de la API |
| MongoDB Compass o Studio 3T | última | Cliente gráfico (opcional) |
| Postman | última | Pruebas de la colección |
| Git | 2.x | Control de versiones |

No es necesario instalar Python ni MongoDB en el equipo: todo corre en contenedores.

## 2. Puesta en marcha

```powershell
# 1. Variables de entorno (el .env NO se sube a GitHub)
copy .env.example .env        # luego edite las claves

# 2. Levantar MongoDB + API
docker compose up -d --build

# 3. Verificar
docker compose ps
docker logs c_mongo_gastronomia 2>&1 | findstr "ejecutado"           # debe mostrar 4 líneas
docker logs c_api_gastronomia 2>&1 | findstr "MongoDB"               # debe decir "Conexión con MongoDB establecida"
```

- Swagger / OpenAPI: <http://localhost:8000/docs>
- ReDoc: <http://localhost:8000/redoc>

La primera vez que se crea el volumen, MongoDB ejecuta automáticamente los scripts de `database/`
en orden alfabético. Para **reiniciar la base de datos desde cero**:

```powershell
docker compose down -v
docker compose up -d
```

### Ejecutar la API fuera de Docker (opcional, para depurar)

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
docker compose up -d mongo
uvicorn app.c_main:c_app --reload
```

## 3. Usuarios de prueba

Contraseña de todos: `Gastro2026*`

| Correo | Rol |
|---|---|
| admin@gastronomia.edu.co | ADMIN |
| cajero@gastronomia.edu.co | CAJERO |
| cocinero@gastronomia.edu.co | COCINERO |

En Swagger: ejecute `POST /api/v1/auth/login`, copie el `access_token`, pulse **Authorize** y péguelo.

## 4. Estructura del proyecto

```
api_gastronomia/
├── app/
│   ├── c_main.py                 # punto de entrada (FastAPI)
│   ├── core/                     # c_config.py, c_security.py (JWT, bcrypt), c_dependencias.py (roles),
│   │                             # c_excepciones.py (códigos HTTP), c_utilidades.py (fechas Bogotá)
│   ├── database/                 # c_conexion_mongo.py
│   ├── models/                   # c_enums.py, c_colecciones.py
│   ├── schemas/                  # validaciones Pydantic (c_*_schemas.py)
│   ├── repositories/             # acceso a MongoDB (c_*_repository.py)
│   ├── services/                 # reglas de negocio RN01..RN06 (c_*_service.py)
│   └── routers/                  # endpoints por recurso (c_*_router.py)
├── database/
│   ├── c_01_ddl_colecciones.js   # colecciones, $jsonSchema, índices (equivale a DDL)
│   ├── c_02_dml_datos_prueba.js  # datos de prueba (equivale a DML)
│   ├── c_03_dcl_usuarios.js      # rol y usuarios de privilegios mínimos (equivale a DCL)
│   └── c_04_mongo_calificaciones.js
├── postman/c_api_gastronomia.postman_collection.json
├── docs/c_manual_configuracion_bd.md   # anexo: Manual de Configuración de Base de Datos
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

Flujo de una petición: **router** (valida token/rol y esquema) → **service** (reglas de negocio) →
**repository** (consultas MongoDB) → **MongoDB**.

## 5. Endpoints (prefijo `/api/v1`)

### Autenticación
| Método | Ruta | Roles |
|---|---|---|
| POST | `/auth/login` | Público |
| POST | `/auth/registro` | ADMIN |
| GET | `/auth/perfil` | Autenticado |

### CRUD (GET lista, GET /{id}, POST, PUT /{id}, DELETE /{id})
| Recurso | Ruta | Roles |
|---|---|---|
| Usuarios | `/usuarios` | ADMIN |
| Categorías | `/categorias` | ADMIN (consulta: todos) |
| Productos | `/productos` | ADMIN (consulta: todos) |
| Insumos | `/insumos` | ADMIN, COCINERO |
| Recetas | `/recetas` | ADMIN, COCINERO |
| Proveedores | `/proveedores` | ADMIN |
| Compras | `/compras` | ADMIN |
| Clientes | `/clientes` | ADMIN, CAJERO |
| Pedidos | `/pedidos` | ADMIN, CAJERO (consulta y cambio de estado: también COCINERO) |
| Calificaciones | `/calificaciones` | ADMIN, CAJERO |

Los listados aceptan `omitir` y `limite` (paginación) y filtros como `estado`, `rol`, `tipo_cliente`.

### Consultas y procesos de negocio
| Método | Ruta | Descripción |
|---|---|---|
| GET | `/productos/categoria/{id_categoria}` | Productos de una categoría |
| GET | `/productos/{id}/receta` | Insumos y cantidades de la receta |
| GET | `/productos/{id}/costo` | Costo de producción y margen (ADMIN, COCINERO) |
| GET | `/insumos/stock-bajo` | `stock_actual <= stock_minimo` |
| GET | `/insumos/por-vencer?dias=7` | Vencen en los próximos N días |
| GET | `/proveedores/{id}/compras` | Historial de compras |
| GET | `/clientes/{id}/pedidos` | Historial de pedidos |
| GET | `/pedidos/estado/{estado}` | Pedidos por estado |
| PATCH | `/pedidos/{id}/estado` | Cambio de estado (RN03, RN05) |
| GET | `/reportes/ventas?desde=&hasta=` | Ventas por rango (ADMIN) |
| GET | `/reportes/productos-mas-vendidos?limite=10` | Ranking (ADMIN) |
| GET | `/calificaciones/producto/{id_producto}` | Calificaciones y promedio |

## 6. Reglas de negocio implementadas

| Regla | Dónde | Cómo |
|---|---|---|
| RN01 | `c_pedido_service.c_construir_detalle` | El cliente solo envía producto y cantidad; la API toma `precio_venta`, calcula `subtotal` y `total`. |
| RN02 | `c_compra_service.c_crear_compra` | Tras guardar la compra, `$inc` de `stock_actual` y `$set` de `costo_unitario` (y vencimiento si se envía). |
| RN03 | `c_pedido_service.c_descontar_inventario` | Al pasar a ENTREGADO: Σ(cantidad receta × cantidad pedida) por insumo; verifica todo primero y descuenta con actualización condicional atómica (`stock_actual >= requerido`). Si falta → **409** con la lista de faltantes y se revierte lo descontado. |
| RN04 | `c_eliminar_*` en servicios | Producto, insumo, cliente, proveedor (y categoría/usuario) con movimientos → `estado = INACTIVO`; sin movimientos → borrado físico. |
| RN05 | `c_pedido_service.c_validar_modificable` | PUT, PATCH o DELETE sobre un pedido ENTREGADO/ANULADO → **409**. |
| RN06 | `c_security.py`, `c_usuario_repository.py` | bcrypt (12 rondas); la proyección de MongoDB excluye `password` y los esquemas de respuesta no lo tienen. |

## 7. Seguridad

- JWT HS256 con expiración (`JWT_EXPIRE_MINUTES`), enviado en `Authorization: Bearer <token>`.
- **401**: sin token, token inválido/expirado o usuario inactivo. **403**: rol sin permiso.
- Credenciales de MongoDB y clave del JWT en `.env` (ignorado por Git).
- La API se conecta con `c_api_gastronomia`, que solo tiene el rol personalizado
  `c_rol_api_gastronomia` (find/insert/update/remove sobre `bd_gastronomia`). No puede borrar
  colecciones, crear índices ni administrar usuarios. Nunca se usa el usuario root.
- Errores: 400 (regla/solicitud inválida), 404, 409 (duplicados y conflictos de estado),
  422 (validación Pydantic), 500 (errores internos, sin exponer detalles).

## 8. Pruebas con Postman

1. Importe `postman/c_api_gastronomia.postman_collection.json`.
2. Ejecute la colección completa con el **Runner** (en orden). La carpeta *01 Autenticación* guarda los tokens.
3. Resultado esperado: 113 peticiones, 149 aserciones, 0 fallos.

También puede ejecutarse sin instalar nada, con Newman en Docker:

```powershell
docker run --rm --network api_gastronomia_default -v "${PWD}/postman:/etc/newman" postman/newman:6-alpine `
  run c_api_gastronomia.postman_collection.json --env-var "baseUrl=http://api:8000/api/v1"
```

## 9. Respaldo y restauración

```powershell
# Respaldo (queda en la carpeta ./respaldos)
docker exec c_mongo_gastronomia sh -c 'mongodump -u "$MONGO_INITDB_ROOT_USERNAME" -p "$MONGO_INITDB_ROOT_PASSWORD" --authenticationDatabase admin --db bd_gastronomia --gzip --archive=/respaldos/bd_gastronomia.gz'

# Restauración
docker exec c_mongo_gastronomia sh -c 'mongorestore -u "$MONGO_INITDB_ROOT_USERNAME" -p "$MONGO_INITDB_ROOT_PASSWORD" --authenticationDatabase admin --gzip --archive=/respaldos/bd_gastronomia.gz --drop'
```
