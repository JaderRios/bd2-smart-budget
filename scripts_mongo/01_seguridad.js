// 1. Conectarse como administrador al cluster de MongoDB e ingresar a la base de datos de Fintech
use fintech_db;

// 2. Crear un rol personalizado si fuera necesario, o utilizar roles integrados.
// Para este proyecto, utilizaremos el rol 'readWrite' que permite operaciones CRUD (insert, find, update, delete)

// 3. Crear el usuario de base de datos específico para la aplicación.
// IMPORTANTE: Asegúrate de habilitar la autenticación SCRAM-SHA-256 en tu mongod.conf 
// (security: authorization: "enabled") para que esto tenga efecto.

db.createUser({
  user: "api_smartbudget",
  pwd: "MongoSecurePassword2026",
  roles: [
    { role: "readWrite", db: "fintech_db" }
  ]
});

// Comentario para el informe:
// Se aplicó el principio de mínimos privilegios creando un usuario que únicamente tiene 
// acceso de lectura y escritura a la base de datos 'fintech_db', evitando el uso de
// credenciales maestras (root) en el código fuente de la aplicación Python.
