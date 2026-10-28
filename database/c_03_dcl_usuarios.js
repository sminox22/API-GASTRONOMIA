// =====================================================================
// c_03_dcl_usuarios.js
// "DCL" de MongoDB: rol y usuarios de privilegios mínimos.
// La API NUNCA se conecta con el usuario root del contenedor.
//  - c_rol_api_gastronomia: solo find, insert, update y remove sobre
//    bd_gastronomia (no puede borrar colecciones, ni crear índices,
//    ni administrar usuarios).
//  - Usuario de reportes: solo lectura (rol "read").
// Las credenciales se leen de variables de entorno (archivo .env).
// =====================================================================

const c_nombre_bd = process.env.C_MONGO_DB || "bd_gastronomia";
const c_bd = db.getSiblingDB(c_nombre_bd);

const c_app_user = process.env.C_MONGO_APP_USER;
const c_app_pass = process.env.C_MONGO_APP_PASSWORD;
const c_rep_user = process.env.C_MONGO_REPORT_USER;
const c_rep_pass = process.env.C_MONGO_REPORT_PASSWORD;

if (!c_app_user || !c_app_pass) {
  throw new Error("Faltan C_MONGO_APP_USER / C_MONGO_APP_PASSWORD en el entorno");
}

// Rol personalizado con privilegios mínimos (equivalente a GRANT SELECT, INSERT, UPDATE, DELETE)
if (!c_bd.getRole("c_rol_api_gastronomia")) {
  c_bd.createRole({
    role: "c_rol_api_gastronomia",
    privileges: [
      { resource: { db: c_nombre_bd, collection: "" }, actions: ["find", "insert", "update", "remove"] },
    ],
    roles: [],
  });
}

// Usuario de la API
if (c_bd.getUser(c_app_user)) {
  c_bd.updateUser(c_app_user, { pwd: c_app_pass, roles: [{ role: "c_rol_api_gastronomia", db: c_nombre_bd }] });
} else {
  c_bd.createUser({ user: c_app_user, pwd: c_app_pass, roles: [{ role: "c_rol_api_gastronomia", db: c_nombre_bd }] });
}

// Usuario de solo lectura para consultas y reportes (Compass / Studio 3T)
if (c_rep_user && c_rep_pass) {
  if (c_bd.getUser(c_rep_user)) {
    c_bd.updateUser(c_rep_user, { pwd: c_rep_pass, roles: [{ role: "read", db: c_nombre_bd }] });
  } else {
    c_bd.createUser({ user: c_rep_user, pwd: c_rep_pass, roles: [{ role: "read", db: c_nombre_bd }] });
  }
}

printjson(c_bd.getUsers({ showPrivileges: false }).users.map((u) => ({ user: u.user, roles: u.roles })));
print("c_03_dcl_usuarios.js ejecutado correctamente");
