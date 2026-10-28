// =====================================================================
// c_04_mongo_calificaciones.js
// Datos de prueba de la colección calificaciones (información no
// estructurada: opiniones de los clientes). La validación $jsonSchema
// de la colección está en c_01_ddl_colecciones.js.
// Cada calificación se construye a partir de un pedido ENTREGADO.
// =====================================================================

const c_bd = db.getSiblingDB(process.env.C_MONGO_DB || "bd_gastronomia");

c_bd.calificaciones.deleteMany({});

// [id_pedido, calificacion_servicio, comentario, calificaciones de los productos en orden]
const c_datos = [
  [1, 5, "Excelente atención y buen sabor", [5, 4]],
  [2, 4, "La bandeja estaba muy completa", [5, 4]],
  [3, 5, "Desayuno a tiempo y bien servido", [5, 5]],
  [4, 3, "Hubo demora en la entrega", [4, 3]],
  [5, 5, "El refrigerio del evento fue un éxito", [5, 4]],
  [6, 4, "Pollo jugoso, el jugo un poco dulce", [5, 3]],
  [7, 4, "Muy buena torta", [5, 4]],
  [8, 2, "La sopa llegó fría", [2, 4]],
  [9, 5, "Las galletas son deliciosas", [5, 5]],
  [10, 4, null, [4, 5]],
];

const c_documentos = c_datos.map(([c_id_pedido, c_servicio, c_comentario, c_notas], i) => {
  const c_pedido = c_bd.pedidos.findOne({ id_pedido: c_id_pedido, estado: "ENTREGADO" });
  if (!c_pedido) throw new Error(`El pedido ${c_id_pedido} no existe o no está ENTREGADO`);
  const c_fecha = new Date(c_pedido.fecha_pedido.getTime() + 2 * 60 * 60 * 1000);
  return {
    id_calificacion: i + 1,
    id_pedido: c_id_pedido,
    id_cliente: c_pedido.id_cliente,
    fecha: c_fecha,
    calificacion_servicio: c_servicio,
    comentario: c_comentario,
    productos: c_pedido.detalle.map((d, j) => ({
      id_producto: d.id_producto,
      nombre: d.nombre_producto,
      calificacion: c_notas[j] ?? 5,
    })),
  };
});

c_bd.calificaciones.insertMany(c_documentos);
c_bd.contadores.updateOne({ _id: "calificaciones" }, { $set: { seq: c_documentos.length } }, { upsert: true });

print("c_04_mongo_calificaciones.js ejecutado correctamente");
