// =====================================================================
// c_01_ddl_colecciones.js
// "DDL" de MongoDB: crea las colecciones de bd_gastronomia con validación
// $jsonSchema, índices únicos y la colección de contadores (ids enteros).
// Se ejecuta automáticamente la primera vez que se crea el volumen de Docker
// (carpeta /docker-entrypoint-initdb.d). También puede ejecutarse a mano:
//   mongosh -u <root> -p <clave> --authenticationDatabase admin bd_gastronomia c_01_ddl_colecciones.js
// =====================================================================

const c_bd = db.getSiblingDB(process.env.C_MONGO_DB || "bd_gastronomia");

const c_entero = { bsonType: ["int", "long"] };
const c_numero = { bsonType: ["int", "long", "double", "decimal"] };
const c_estado_activo = { enum: ["ACTIVO", "INACTIVO"] };

function c_crear_coleccion(c_nombre, c_requeridos, c_propiedades) {
  if (c_bd.getCollectionNames().includes(c_nombre)) {
    c_bd.runCommand({
      collMod: c_nombre,
      validator: { $jsonSchema: { bsonType: "object", required: c_requeridos, properties: c_propiedades } },
      validationLevel: "strict",
      validationAction: "error",
    });
  } else {
    c_bd.createCollection(c_nombre, {
      validator: { $jsonSchema: { bsonType: "object", required: c_requeridos, properties: c_propiedades } },
      validationLevel: "strict",
      validationAction: "error",
    });
  }
  print(`Colección ${c_nombre} lista`);
}

// ---------------------------------------------------------------- usuarios
c_crear_coleccion("usuarios",
  ["id_usuario", "identificacion", "nombres", "apellidos", "correo", "password", "rol", "estado"],
  {
    id_usuario: c_entero,
    identificacion: { bsonType: "string", minLength: 5, maxLength: 20 },
    nombres: { bsonType: "string", minLength: 2, maxLength: 80 },
    apellidos: { bsonType: "string", minLength: 2, maxLength: 80 },
    correo: { bsonType: "string", maxLength: 120, pattern: "^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$" },
    password: { bsonType: "string", minLength: 59, maxLength: 255, description: "hash bcrypt" },
    rol: { enum: ["ADMIN", "CAJERO", "COCINERO"] },
    estado: c_estado_activo,
  });
c_bd.usuarios.createIndex({ id_usuario: 1 }, { unique: true, name: "uq_usuarios_id" });
c_bd.usuarios.createIndex({ identificacion: 1 }, { unique: true, name: "uq_usuarios_identificacion" });
c_bd.usuarios.createIndex({ correo: 1 }, { unique: true, name: "uq_usuarios_correo" });

// -------------------------------------------------------------- categorias
c_crear_coleccion("categorias",
  ["id_categoria", "nombre", "estado"],
  {
    id_categoria: c_entero,
    nombre: { bsonType: "string", minLength: 2, maxLength: 60 },
    descripcion: { bsonType: ["string", "null"], maxLength: 200 },
    estado: c_estado_activo,
  });
c_bd.categorias.createIndex({ id_categoria: 1 }, { unique: true, name: "uq_categorias_id" });
c_bd.categorias.createIndex({ nombre: 1 }, { unique: true, name: "uq_categorias_nombre" });

// --------------------------------------------------------------- productos
c_crear_coleccion("productos",
  ["id_producto", "codigo", "nombre", "precio_venta", "unidad_venta", "id_categoria", "estado"],
  {
    id_producto: c_entero,
    codigo: { bsonType: "string", minLength: 1, maxLength: 20 },
    nombre: { bsonType: "string", minLength: 2, maxLength: 100 },
    descripcion: { bsonType: ["string", "null"] },
    precio_venta: { ...c_numero, minimum: 0, exclusiveMinimum: true },
    unidad_venta: { bsonType: "string", maxLength: 20 },
    id_categoria: c_entero,
    estado: { enum: ["DISPONIBLE", "AGOTADO", "INACTIVO"] },
  });
c_bd.productos.createIndex({ id_producto: 1 }, { unique: true, name: "uq_productos_id" });
c_bd.productos.createIndex({ codigo: 1 }, { unique: true, name: "uq_productos_codigo" });
c_bd.productos.createIndex({ id_categoria: 1 }, { name: "ix_productos_categoria" });

// ----------------------------------------------------------------- insumos
c_crear_coleccion("insumos",
  ["id_insumo", "nombre", "unidad_medida", "stock_actual", "stock_minimo", "costo_unitario", "estado"],
  {
    id_insumo: c_entero,
    nombre: { bsonType: "string", minLength: 2, maxLength: 100 },
    unidad_medida: { enum: ["g", "kg", "ml", "l", "lb", "unidad"] },
    stock_actual: { ...c_numero, minimum: 0 },
    stock_minimo: { ...c_numero, minimum: 0 },
    costo_unitario: { ...c_numero, minimum: 0 },
    fecha_vencimiento: { bsonType: ["date", "null"] },
    estado: c_estado_activo,
  });
c_bd.insumos.createIndex({ id_insumo: 1 }, { unique: true, name: "uq_insumos_id" });
c_bd.insumos.createIndex({ nombre: 1 }, { unique: true, name: "uq_insumos_nombre" });
c_bd.insumos.createIndex({ fecha_vencimiento: 1 }, { name: "ix_insumos_vencimiento" });

// ----------------------------------------------------------------- recetas
c_crear_coleccion("recetas",
  ["id_receta", "id_producto", "id_insumo", "cantidad"],
  {
    id_receta: c_entero,
    id_producto: c_entero,
    id_insumo: c_entero,
    cantidad: { ...c_numero, minimum: 0, exclusiveMinimum: true },
  });
c_bd.recetas.createIndex({ id_receta: 1 }, { unique: true, name: "uq_recetas_id" });
c_bd.recetas.createIndex({ id_producto: 1, id_insumo: 1 }, { unique: true, name: "uq_recetas_producto_insumo" });
c_bd.recetas.createIndex({ id_insumo: 1 }, { name: "ix_recetas_insumo" });

// ------------------------------------------------------------- proveedores
c_crear_coleccion("proveedores",
  ["id_proveedor", "nit", "razon_social", "estado"],
  {
    id_proveedor: c_entero,
    nit: { bsonType: "string", minLength: 5, maxLength: 20 },
    razon_social: { bsonType: "string", minLength: 2, maxLength: 120 },
    telefono: { bsonType: ["string", "null"], maxLength: 20 },
    correo: { bsonType: ["string", "null"], maxLength: 120 },
    direccion: { bsonType: ["string", "null"], maxLength: 150 },
    estado: c_estado_activo,
  });
c_bd.proveedores.createIndex({ id_proveedor: 1 }, { unique: true, name: "uq_proveedores_id" });
c_bd.proveedores.createIndex({ nit: 1 }, { unique: true, name: "uq_proveedores_nit" });

// ----------------------------------------------------------------- compras
// El detalle de la compra se guarda embebido (en SQL sería detalle_compra).
c_crear_coleccion("compras",
  ["id_compra", "numero_factura", "fecha_compra", "id_proveedor", "id_usuario", "total", "detalle"],
  {
    id_compra: c_entero,
    numero_factura: { bsonType: "string", minLength: 1, maxLength: 30 },
    fecha_compra: { bsonType: "date" },
    id_proveedor: c_entero,
    id_usuario: c_entero,
    total: { ...c_numero, minimum: 0 },
    detalle: {
      bsonType: "array",
      minItems: 1,
      items: {
        bsonType: "object",
        required: ["id_insumo", "cantidad", "costo_unitario", "subtotal"],
        properties: {
          id_insumo: c_entero,
          nombre_insumo: { bsonType: "string" },
          cantidad: { ...c_numero, minimum: 0, exclusiveMinimum: true },
          costo_unitario: { ...c_numero, minimum: 0 },
          subtotal: { ...c_numero, minimum: 0 },
          fecha_vencimiento: { bsonType: ["date", "null"] },
        },
      },
    },
  });
c_bd.compras.createIndex({ id_compra: 1 }, { unique: true, name: "uq_compras_id" });
c_bd.compras.createIndex({ id_proveedor: 1, numero_factura: 1 }, { unique: true, name: "uq_compras_proveedor_factura" });
c_bd.compras.createIndex({ "detalle.id_insumo": 1 }, { name: "ix_compras_insumo" });

// ---------------------------------------------------------------- clientes
c_crear_coleccion("clientes",
  ["id_cliente", "identificacion", "nombres", "apellidos", "tipo_cliente", "estado"],
  {
    id_cliente: c_entero,
    identificacion: { bsonType: "string", minLength: 5, maxLength: 20 },
    nombres: { bsonType: "string", minLength: 2, maxLength: 80 },
    apellidos: { bsonType: "string", minLength: 2, maxLength: 80 },
    telefono: { bsonType: ["string", "null"], maxLength: 20 },
    correo: { bsonType: ["string", "null"], maxLength: 120 },
    tipo_cliente: { enum: ["APRENDIZ", "INSTRUCTOR", "FUNCIONARIO", "EXTERNO"] },
    estado: c_estado_activo,
  });
c_bd.clientes.createIndex({ id_cliente: 1 }, { unique: true, name: "uq_clientes_id" });
c_bd.clientes.createIndex({ identificacion: 1 }, { unique: true, name: "uq_clientes_identificacion" });

// ----------------------------------------------------------------- pedidos
// El detalle del pedido se guarda embebido (en SQL sería detalle_pedido).
c_crear_coleccion("pedidos",
  ["id_pedido", "fecha_pedido", "id_cliente", "id_usuario", "tipo_pedido", "estado", "total", "detalle"],
  {
    id_pedido: c_entero,
    fecha_pedido: { bsonType: "date" },
    id_cliente: c_entero,
    id_usuario: c_entero,
    tipo_pedido: { enum: ["MESA", "PARA_LLEVAR", "EVENTO"] },
    estado: { enum: ["PENDIENTE", "EN_PREPARACION", "ENTREGADO", "ANULADO"] },
    observaciones: { bsonType: ["string", "null"], maxLength: 300 },
    total: { ...c_numero, minimum: 0 },
    fecha_entrega: { bsonType: ["date", "null"] },
    detalle: {
      bsonType: "array",
      minItems: 1,
      items: {
        bsonType: "object",
        required: ["id_producto", "cantidad", "precio_unitario", "subtotal"],
        properties: {
          id_producto: c_entero,
          nombre_producto: { bsonType: "string" },
          cantidad: { ...c_entero, minimum: 1 },
          precio_unitario: { ...c_numero, minimum: 0, exclusiveMinimum: true },
          subtotal: { ...c_numero, minimum: 0, exclusiveMinimum: true },
        },
      },
    },
  });
c_bd.pedidos.createIndex({ id_pedido: 1 }, { unique: true, name: "uq_pedidos_id" });
c_bd.pedidos.createIndex({ id_cliente: 1, fecha_pedido: -1 }, { name: "ix_pedidos_cliente" });
c_bd.pedidos.createIndex({ estado: 1, fecha_pedido: -1 }, { name: "ix_pedidos_estado_fecha" });
c_bd.pedidos.createIndex({ "detalle.id_producto": 1 }, { name: "ix_pedidos_producto" });

// ---------------------------------------------------------- calificaciones
c_crear_coleccion("calificaciones",
  ["id_calificacion", "id_pedido", "id_cliente", "fecha", "calificacion_servicio", "productos"],
  {
    id_calificacion: c_entero,
    id_pedido: c_entero,
    id_cliente: c_entero,
    fecha: { bsonType: "date" },
    calificacion_servicio: { ...c_entero, minimum: 1, maximum: 5 },
    comentario: { bsonType: ["string", "null"], maxLength: 500 },
    productos: {
      bsonType: "array",
      items: {
        bsonType: "object",
        required: ["id_producto", "calificacion"],
        properties: {
          id_producto: c_entero,
          nombre: { bsonType: "string" },
          calificacion: { ...c_entero, minimum: 1, maximum: 5 },
        },
      },
    },
  });
c_bd.calificaciones.createIndex({ id_calificacion: 1 }, { unique: true, name: "uq_calificaciones_id" });
c_bd.calificaciones.createIndex({ id_pedido: 1 }, { unique: true, name: "uq_calificaciones_pedido" });
c_bd.calificaciones.createIndex({ "productos.id_producto": 1 }, { name: "ix_calificaciones_producto" });

// --------------------------------------------------------------- contadores
// Secuencias para los ids enteros (equivalente a AUTO_INCREMENT).
if (!c_bd.getCollectionNames().includes("contadores")) {
  c_bd.createCollection("contadores");
}

print("c_01_ddl_colecciones.js ejecutado correctamente");
