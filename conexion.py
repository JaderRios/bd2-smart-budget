from pymongo import MongoClient
import oracledb

# --- CONEXIÓN MONGODB ---
# Híbrido: Conexión usando el usuario seguro restringido 'api_smartbudget' creado en 01_seguridad.js
# Si no has activado la seguridad en tu MongoDB, puedes usar la URI básica: "mongodb://localhost:27017/"
try:
    # URL de conexión con credenciales seguras
    cliente = MongoClient("mongodb://api_smartbudget:MongoSecurePassword2026@localhost:27017/FINTECH_DB?authSource=FINTECH_DB", serverSelectionTimeoutMS=2000)
    # Trigger a connection test
    cliente.admin.command('ping')
    db = cliente["FINTECH_DB"]
    print("Conexión segura a MongoDB exitosa")
except Exception:
    # Fallback a conexión sin autenticación por si el alumno no ha corrido el script de seguridad todavía
    cliente = MongoClient("mongodb://localhost:27017/")
    db = cliente["FINTECH_DB"]
    print("Conexión a MongoDB exitosa (Modo desarrollo sin contraseña)")

# --- CONEXIÓN ORACLE ---
# Conexión usando el usuario restringido 'fintech_app' con el rol de operador 'rol_fintech_operador' (04_seguridad.sql)
# Si te da error de conexión, asegúrate de haber ejecutado el archivo de seguridad en Oracle.
try:
    conexion_oracle = oracledb.connect(
        user="fintech_app",
        password="Fintech123",
        dsn="localhost/xe"
    )
    cursor_oracle = conexion_oracle.cursor()
    print("Conexión segura a Oracle exitosa (Usuario: fintech_app)")
except Exception as e_secure:
    # Fallback temporal al usuario administrador SYSTEM por si aún no corres el script de seguridad
    try:
        conexion_oracle = oracledb.connect(
            user="system",
            password="12345678",
            dsn="localhost/xe"
        )
        cursor_oracle = conexion_oracle.cursor()
        print("Conexión a Oracle exitosa (Fallback: SYSTEM)")
    except Exception as e:
        print("Error conectando a Oracle:", e)
        cursor_oracle = None

