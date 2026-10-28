// =====================================================================
// c_02_dml_datos_prueba.js
// "DML" de MongoDB: datos de prueba (mínimo 10 documentos por colección
// principal). Contraseña de todos los usuarios de prueba: Gastro2026*
// =====================================================================

const c_bd = db.getSiblingDB(process.env.C_MONGO_DB || "bd_gastronomia");
const c_hash = "$2b$12$hHiTi2Kkvxgu3KWOAJMsQe5QRIwZfHvY1LpJVcPzFdkBSe.YttASy"; // Gastro2026*
const c_fecha = (c_texto) => new Date(c_texto + "-05:00"); // hora de Bogotá
const c_redondear = (c_valor) => Math.round(c_valor * 100) / 100;

// Limpia los datos previos para que el script sea re-ejecutable
["usuarios", "categorias", "productos", "insumos", "recetas", "proveedores",
 "compras", "clientes", "pedidos", "contadores"].forEach((c) => c_bd[c].deleteMany({}));

// ---------------------------------------------------------------- usuarios
const c_usuarios = [
  [1, "1075000001", "Carolina", "Pérez Rojas", "admin@gastronomia.edu.co", "ADMIN", "ACTIVO"],
  [2, "1075000002", "Jorge", "Trujillo Silva", "jtrujillo@gastronomia.edu.co", "ADMIN", "ACTIVO"],
  [3, "1075000003", "Camila", "Andrade Ruiz", "cajero@gastronomia.edu.co", "CAJERO", "ACTIVO"],
  [4, "1075000004", "Andrés", "Medina Polanco", "amedina@gastronomia.edu.co", "CAJERO", "ACTIVO"],
  [5, "1075000005", "Luisa", "Cabrera Vargas", "lcabrera@gastronomia.edu.co", "CAJERO", "ACTIVO"],
  [6, "1075000006", "Diego", "Charry Ortiz", "dcharry@gastronomia.edu.co", "CAJERO", "INACTIVO"],
  [7, "1075000007", "Marta", "Quintero Losada", "cocinero@gastronomia.edu.co", "COCINERO", "ACTIVO"],
  [8, "1075000008", "Fabián", "Rojas Perdomo", "frojas@gastronomia.edu.co", "COCINERO", "ACTIVO"],
  [9, "1075000009", "Paola", "Ramírez Cuéllar", "pramirez@gastronomia.edu.co", "COCINERO", "ACTIVO"],
  [10, "1075000010", "Héctor", "Motta Díaz", "hmotta@gastronomia.edu.co", "COCINERO", "ACTIVO"],
];
c_bd.usuarios.insertMany(c_usuarios.map(([id, ide, nom, ape, cor, rol, est]) => ({
  id_usuario: id, identificacion: ide, nombres: nom, apellidos: ape,
  correo: cor, password: c_hash, rol: rol, estado: est,
})));

// -------------------------------------------------------------- categorias
const c_categorias = [
  [1, "Platos fuertes", "Almuerzos y platos principales"],
  [2, "Bebidas", "Jugos naturales, café y bebidas calientes"],
  [3, "Panadería", "Pan y productos horneados de sal"],
  [4, "Repostería", "Tortas, galletas y productos de dulce"],
  [5, "Desayunos", "Desayunos típicos y continentales"],
  [6, "Comidas rápidas", "Sándwiches, empanadas y similares"],
  [7, "Sopas", "Sopas y cremas del día"],
  [8, "Ensaladas", "Ensaladas frescas"],
  [9, "Postres", "Postres fríos y tradicionales"],
  [10, "Eventos", "Refrigerios y menús para eventos institucionales"],
];
c_bd.categorias.insertMany(c_categorias.map(([id, nom, des]) => ({
  id_categoria: id, nombre: nom, descripcion: des, estado: "ACTIVO",
})));

// --------------------------------------------------------------- productos
const c_productos = [
  [1, "PF-001", "Almuerzo ejecutivo", "Sopa, arroz, proteína, principio y ensalada", 15000, "porción", 1, "DISPONIBLE"],
  [2, "PF-002", "Bandeja paisa", "Arroz, fríjol, carne molida, huevo y tajada", 22000, "porción", 1, "DISPONIBLE"],
  [3, "PF-003", "Pollo a la plancha", "Pechuga a la plancha con papa", 18000, "porción", 1, "DISPONIBLE"],
  [4, "BE-001", "Jugo de lulo", "Jugo natural en agua", 5000, "vaso", 2, "DISPONIBLE"],
  [5, "BE-002", "Jugo de mora", "Jugo natural en agua", 5000, "vaso", 2, "DISPONIBLE"],
  [6, "BE-003", "Café tinto", "Café colombiano", 2000, "pocillo", 2, "DISPONIBLE"],
  [7, "PA-001", "Pan de queso", "Pan horneado con queso campesino", 1500, "unidad", 3, "DISPONIBLE"],
  [8, "PA-002", "Pan francés", "Pan blanco tradicional", 1000, "unidad", 3, "DISPONIBLE"],
  [9, "RE-001", "Torta de vainilla", "Porción de torta casera", 6000, "porción", 4, "DISPONIBLE"],
  [10, "RE-002", "Galletas de mantequilla", "Paquete de 6 galletas", 3000, "paquete", 4, "DISPONIBLE"],
  [11, "DE-001", "Desayuno típico", "Huevos, pan, queso, café con leche", 12000, "porción", 5, "DISPONIBLE"],
  [12, "SO-001", "Sopa de fríjol", "Sopa del día", 9000, "porción", 7, "DISPONIBLE"],
  [13, "EV-001", "Refrigerio institucional", "Pan de queso y jugo natural", 7000, "unidad", 10, "AGOTADO"],
];
c_bd.productos.insertMany(c_productos.map(([id, cod, nom, des, pre, uni, cat, est]) => ({
  id_producto: id, codigo: cod, nombre: nom, descripcion: des, precio_venta: pre,
  unidad_venta: uni, id_categoria: cat, estado: est,
})));

// ----------------------------------------------------------------- insumos
const c_insumos = [
  [1, "Arroz", "kg", 50, 10, 4200, "2027-03-01"],
  [2, "Pechuga de pollo", "kg", 20, 5, 16000, "2026-10-25"],
  [3, "Carne de res", "kg", 15, 5, 28000, "2026-10-24"],
  [4, "Papa", "kg", 40, 10, 2500, "2026-11-15"],
  [5, "Harina de trigo", "kg", 30, 10, 3800, "2027-01-10"],
  [6, "Azúcar", "kg", 25, 5, 4000, "2027-06-01"],
  [7, "Huevo", "unidad", 120, 60, 600, "2026-10-28"],
  [8, "Leche", "l", 20, 10, 4500, "2026-10-23"],
  [9, "Mantequilla", "kg", 4, 5, 22000, "2026-12-01"],
  [10, "Lulo", "kg", 8, 3, 7000, "2026-10-26"],
  [11, "Mora", "kg", 2, 3, 8000, "2026-10-27"],
  [12, "Café molido", "kg", 5, 2, 30000, "2027-02-01"],
  [13, "Queso campesino", "kg", 6, 3, 18000, "2026-10-30"],
  [14, "Aceite vegetal", "l", 10, 3, 9000, "2027-05-01"],
  [15, "Fríjol", "kg", 12, 4, 7500, "2027-04-01"],
];
c_bd.insumos.insertMany(c_insumos.map(([id, nom, um, sa, sm, cu, fv]) => ({
  id_insumo: id, nombre: nom, unidad_medida: um, stock_actual: sa, stock_minimo: sm,
  costo_unitario: cu, fecha_vencimiento: c_fecha(fv + "T00:00:00"), estado: "ACTIVO",
})));

// ----------------------------------------------------------------- recetas
// [id_producto, id_insumo, cantidad por unidad de producto (en la unidad del insumo)]
const c_recetas = [
  [1, 1, 0.15], [1, 2, 0.15], [1, 4, 0.2], [1, 14, 0.02], [1, 15, 0.08],
  [2, 1, 0.2], [2, 3, 0.25], [2, 15, 0.15], [2, 7, 1], [2, 14, 0.03],
  [3, 2, 0.3], [3, 4, 0.25], [3, 14, 0.02],
  [4, 10, 0.12], [4, 6, 0.03],
  [5, 11, 0.12], [5, 6, 0.03],
  [6, 12, 0.01], [6, 6, 0.01],
  [7, 5, 0.04], [7, 13, 0.03], [7, 7, 0.2], [7, 9, 0.005],
  [8, 5, 0.06], [8, 9, 0.005],
  [9, 5, 0.05], [9, 6, 0.04], [9, 7, 0.5], [9, 9, 0.02], [9, 8, 0.05],
  [10, 5, 0.08], [10, 6, 0.04], [10, 9, 0.03], [10, 7, 0.3],
  [11, 7, 2], [11, 5, 0.06], [11, 13, 0.05], [11, 12, 0.01], [11, 8, 0.1], [11, 14, 0.01],
  [12, 15, 0.12], [12, 4, 0.1], [12, 3, 0.05],
  [13, 5, 0.05], [13, 13, 0.03], [13, 10, 0.08], [13, 6, 0.03],
];
c_bd.recetas.insertMany(c_recetas.map(([prod, ins, cant], i) => ({
  id_receta: i + 1, id_producto: prod, id_insumo: ins, cantidad: cant,
})));

// ------------------------------------------------------------- proveedores
const c_proveedores = [
  [1, "900100001-1", "Distribuidora Surcolombiana S.A.S.", "3101000001", "ventas@surcolombiana.com", "Cra 5 # 10-20 Neiva"],
  [2, "900100002-2", "Avícola El Huila Ltda.", "3101000002", "pedidos@avicolahuila.com", "Km 3 vía Rivera"],
  [3, "900100003-3", "Carnes Selectas del Sur", "3101000003", "contacto@carnesselectas.com", "Cl 21 # 7-45 Neiva"],
  [4, "900100004-4", "Lácteos La Pradera", "3101000004", "ventas@lapradera.com", "Vereda El Caguán"],
  [5, "900100005-5", "Frutas y Verduras Garzón", "3101000005", "frutasgarzon@gmail.com", "Plaza de mercado Garzón"],
  [6, "900100006-6", "Molinos del Magdalena", "3101000006", "comercial@molinosmagdalena.com", "Zona industrial Neiva"],
  [7, "900100007-7", "Café Origen Huila", "3101000007", "ventas@cafeorigen.com", "Pitalito, Huila"],
  [8, "900100008-8", "Granos y Abarrotes Rivera", "3101000008", "abarrotesrivera@gmail.com", "Cra 2 # 4-10 Rivera"],
  [9, "900100009-9", "Aceites del Llano S.A.", "3101000009", "info@aceitesllano.com", "Villavicencio"],
  [10, "1075123456", "Huevos Doña Rosa", "3101000010", null, "Vereda Fortalecillas"],
];
c_bd.proveedores.insertMany(c_proveedores.map(([id, nit, rs, tel, cor, dir]) => ({
  id_proveedor: id, nit: nit, razon_social: rs, telefono: tel, correo: cor,
  direccion: dir, estado: "ACTIVO",
})));

// ----------------------------------------------------------------- compras
const c_nombre_insumo = Object.fromEntries(c_insumos.map((i) => [i[0], i[1]]));
const c_compras = [
  [1, "FV-1001", "2026-10-01T08:00:00", 6, 1, [[1, 30, 4100], [5, 20, 3700]]],
  [2, "FV-2001", "2026-10-02T09:15:00", 2, 1, [[2, 15, 16000]]],
  [3, "FV-3001", "2026-10-03T07:40:00", 3, 2, [[3, 12, 28000]]],
  [4, "FV-4001", "2026-10-05T10:00:00", 4, 1, [[8, 20, 4500], [13, 6, 18000], [9, 3, 22000]]],
  [5, "FV-5001", "2026-10-06T06:30:00", 5, 2, [[10, 10, 7000], [11, 5, 8000], [4, 25, 2500]]],
  [6, "FV-6001", "2026-10-07T11:20:00", 7, 1, [[12, 4, 30000]]],
  [7, "FV-7001", "2026-10-08T08:45:00", 8, 1, [[15, 10, 7500], [6, 20, 4000]]],
  [8, "FV-8001", "2026-10-09T09:00:00", 9, 2, [[14, 10, 9000]]],
  [9, "FV-9001", "2026-10-10T07:00:00", 10, 1, [[7, 150, 600]]],
  [10, "FV-1002", "2026-10-15T08:10:00", 6, 1, [[1, 20, 4200], [5, 10, 3800]]],
];
c_bd.compras.insertMany(c_compras.map(([id, fac, fec, prov, usu, items]) => {
  const c_detalle = items.map(([ins, cant, costo]) => ({
    id_insumo: ins, nombre_insumo: c_nombre_insumo[ins], cantidad: cant,
    costo_unitario: costo, subtotal: c_redondear(cant * costo), fecha_vencimiento: null,
  }));
  return {
    id_compra: id, numero_factura: fac, fecha_compra: c_fecha(fec), id_proveedor: prov,
    id_usuario: usu, total: c_redondear(c_detalle.reduce((s, d) => s + d.subtotal, 0)),
    detalle: c_detalle,
  };
}));

// ---------------------------------------------------------------- clientes
const c_clientes = [
  [1, "1080100001", "Valentina", "Gómez Salas", "3201000001", "vgomez@soy.sena.edu.co", "APRENDIZ"],
  [2, "1080100002", "Santiago", "Cuéllar Ríos", "3201000002", "scuellar@soy.sena.edu.co", "APRENDIZ"],
  [3, "1080100003", "Daniela", "Perdomo Vega", "3201000003", "dperdomo@soy.sena.edu.co", "APRENDIZ"],
  [4, "1080100004", "Juan", "Losada Trujillo", "3201000004", "jlosada@soy.sena.edu.co", "APRENDIZ"],
  [5, "1080100005", "Wilson", "Ramos Penagos", "3201000005", "wramos@sena.edu.co", "INSTRUCTOR"],
  [6, "1080100006", "Adriana", "Bermeo Castro", "3201000006", "abermeo@sena.edu.co", "INSTRUCTOR"],
  [7, "1080100007", "Ricardo", "Salazar Muñoz", "3201000007", "rsalazar@sena.edu.co", "INSTRUCTOR"],
  [8, "1080100008", "Gloria", "Vargas Ome", "3201000008", "gvargas@sena.edu.co", "FUNCIONARIO"],
  [9, "1080100009", "Óscar", "Tovar Calderón", "3201000009", "otovar@sena.edu.co", "FUNCIONARIO"],
  [10, "1080100010", "Natalia", "Herrera Paz", "3201000010", "natalia.herrera@gmail.com", "EXTERNO"],
  [11, "1080100011", "Felipe", "Ortiz Chávarro", "3201000011", null, "EXTERNO"],
  [12, "900200300-1", "Alcaldía de Neiva", "Eventos institucionales", "6088000000", "eventos@neiva.gov.co", "EXTERNO"],
];
c_bd.clientes.insertMany(c_clientes.map(([id, ide, nom, ape, tel, cor, tipo]) => ({
  id_cliente: id, identificacion: ide, nombres: nom, apellidos: ape, telefono: tel,
  correo: cor, tipo_cliente: tipo, estado: "ACTIVO",
})));

// ----------------------------------------------------------------- pedidos
// RN01: subtotal = cantidad * precio_unitario; total = suma de subtotales
const c_producto_por_id = Object.fromEntries(c_productos.map((p) => [p[0], p]));
const c_pedidos = [
  [1, "2026-10-01T12:10:00", 1, 3, "MESA", "ENTREGADO", [[1, 1], [4, 1]]],
  [2, "2026-10-01T12:25:00", 5, 3, "MESA", "ENTREGADO", [[2, 1], [5, 1]]],
  [3, "2026-10-02T07:30:00", 8, 4, "PARA_LLEVAR", "ENTREGADO", [[11, 1], [6, 2]]],
  [4, "2026-10-03T12:40:00", 2, 4, "MESA", "ENTREGADO", [[1, 2], [4, 2]]],
  [5, "2026-10-06T15:00:00", 12, 3, "EVENTO", "ENTREGADO", [[7, 40], [4, 40]]],
  [6, "2026-10-08T12:15:00", 6, 5, "MESA", "ENTREGADO", [[3, 1], [5, 1]]],
  [7, "2026-10-09T10:00:00", 9, 5, "PARA_LLEVAR", "ENTREGADO", [[9, 2], [6, 2]]],
  [8, "2026-10-13T12:20:00", 3, 3, "MESA", "ENTREGADO", [[12, 1], [1, 1]]],
  [9, "2026-10-14T16:30:00", 10, 4, "PARA_LLEVAR", "ENTREGADO", [[10, 3], [7, 6]]],
  [10, "2026-10-16T12:05:00", 7, 3, "MESA", "ENTREGADO", [[2, 1], [4, 1]]],
  [11, "2026-10-20T07:20:00", 4, 4, "MESA", "ANULADO", [[11, 1]]],
  [12, "2026-10-21T11:50:00", 11, 3, "PARA_LLEVAR", "EN_PREPARACION", [[3, 1], [6, 1]]],
  [13, "2026-10-21T12:00:00", 1, 3, "MESA", "PENDIENTE", [[1, 1], [5, 1]]],
  [14, "2026-10-21T12:05:00", 5, 5, "MESA", "PENDIENTE", [[2, 1], [8, 2]]],
];
c_bd.pedidos.insertMany(c_pedidos.map(([id, fec, cli, usu, tipo, est, items]) => {
  const c_detalle = items.map(([prod, cant]) => {
    const c_precio = c_producto_por_id[prod][4];
    return {
      id_producto: prod, nombre_producto: c_producto_por_id[prod][2], cantidad: cant,
      precio_unitario: c_precio, subtotal: c_redondear(cant * c_precio),
    };
  });
  return {
    id_pedido: id, fecha_pedido: c_fecha(fec), id_cliente: cli, id_usuario: usu,
    tipo_pedido: tipo, estado: est, observaciones: null,
    total: c_redondear(c_detalle.reduce((s, d) => s + d.subtotal, 0)),
    fecha_entrega: est === "ENTREGADO" ? c_fecha(fec) : null,
    detalle: c_detalle,
  };
}));

// --------------------------------------------------------------- contadores
// Se inicializan con el id más alto de cada colección (como AUTO_INCREMENT)
[["usuarios", "id_usuario"], ["categorias", "id_categoria"], ["productos", "id_producto"],
 ["insumos", "id_insumo"], ["recetas", "id_receta"], ["proveedores", "id_proveedor"],
 ["compras", "id_compra"], ["clientes", "id_cliente"], ["pedidos", "id_pedido"]]
  .forEach(([c_col, c_campo]) => {
    const c_ultimo = c_bd[c_col].find().sort({ [c_campo]: -1 }).limit(1).toArray()[0];
    c_bd.contadores.updateOne({ _id: c_col }, { $set: { seq: c_ultimo ? c_ultimo[c_campo] : 0 } }, { upsert: true });
  });

print("c_02_dml_datos_prueba.js ejecutado correctamente");
