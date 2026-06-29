# SmartBudget - Plataforma FinTech Híbrida (Oracle + MongoDB)

SmartBudget es una aplicación de gestión financiera que utiliza una arquitectura de bases de datos híbrida para asegurar consistencia transaccional y flexibilidad en esquemas variables.

## 📁 Estructura del Proyecto

- `/scripts_oracle`: Scripts SQL para la base de datos relacional (Tablas, Procedimientos, Triggers, Seguridad).
- `/scripts_mongo`: Scripts JS para la base de datos NoSQL (Seguridad, Índices).
- `/electron-app`: Frontend web desarrollado en React (Vite).
- `api_main.py`: Backend API desarrollado en FastAPI (Python).
- `crud_oracle.py` / `crud_facturas.py`: Capas de acceso a datos para ambas bases de datos.

---

## 🛠️ 1. Configuración de Bases de Datos

### A. Oracle Database (Datos Transaccionales)
Abre tu cliente SQL (SQL Developer, DBeaver) y conéctate como usuario administrador (`SYSTEM` o `ADMIN`). Ejecuta los scripts en el siguiente orden:
1. `scripts_oracle/01_ddl.sql`: Crea las tablas principales.
2. `scripts_oracle/02_sp.sql`: Crea el Procedimiento Almacenado de transacciones.
3. `scripts_oracle/03_triggers.sql`: Crea Triggers y Secuencias.
4. `scripts_oracle/04_seguridad.sql`: Crea los roles, el usuario de aplicación (`fintech_app`) y los sinónimos.

*(Si usas credenciales distintas, actualiza el archivo `conexion.py` del backend).*

### B. MongoDB (Datos Dinámicos)
Abre tu consola de MongoDB (`mongosh`) o MongoDB Compass y ejecuta el contenido de los scripts:
1. `scripts_mongo/01_seguridad.js`: Para habilitar el usuario `api_smartbudget`.
2. `scripts_mongo/02_indices.js`: Para crear los índices optimizados en las colecciones.

*(Si prefieres usar MongoDB sin seguridad por ahora, el backend en `conexion.py` caerá en el modo "fallback" y funcionará igual).*

---

## 🚀 2. Ejecutar el Backend (FastAPI / Python)

Abre una terminal en la raíz del proyecto (donde está `api_main.py`):

1. (Opcional) Crea y activa un entorno virtual de python.
2. Instala las dependencias:
   ```bash
   pip install fastapi uvicorn pymongo oracledb
   ```
3. Inicia el servidor:
   ```bash
   uvicorn api_main:app --reload
   ```
   El backend estará escuchando en `http://127.0.0.1:8000`.

---

## 💻 3. Ejecutar el Frontend (React)

Abre **otra terminal** distinta, navega a la carpeta del frontend y ejecuta:

1. Entra a la carpeta:
   ```bash
   cd electron-app
   ```
2. Instala las dependencias de Node:
   ```bash
   npm install
   ```
3. Levanta el servidor de desarrollo:
   ```bash
   npm run dev
   ```
   Abre el link local que te arroje la consola (generalmente `http://localhost:5173`) en tu navegador web.

¡Listo! Ya puedes utilizar SmartBudget completamente integrado.