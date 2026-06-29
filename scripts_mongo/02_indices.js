// 1. Conectarse a la base de datos
use fintech_db;

// 2. Creación de Índices
// Para una aplicación de finanzas, las consultas más recurrentes sobre las facturas
// son: "Buscar todas las facturas de un usuario específico" o "Buscar facturas de un mes específico".

// Índice por usuario (Para acelerar la búsqueda cuando el usuario abre su perfil)
db.facturas.createIndex({ "usuario_id": 1 });

// Índice por categoría de empresa (Para hacer dashboards y reportes rápidos)
db.facturas.createIndex({ "categoria": 1 });

// Índice Compuesto (Si la app buscara por usuario Y categoría al mismo tiempo)
db.facturas.createIndex({ "usuario_id": 1, "categoria": 1 });

// Comentario para el informe:
// Se crearon índices B-Tree en la colección 'facturas' sobre los campos 'usuario_id' y 'categoria'
// para optimizar los tiempos de respuesta de las consultas frecuentes (lecturas), 
// lo cual es un requisito fundamental para escalabilidad en bases de datos NoSQL.
