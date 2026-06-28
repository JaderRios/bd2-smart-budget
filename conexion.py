from pymongo import MongoClient
import oracledb

# --- CONEXIÓN MONGODB ---
cliente = MongoClient("mongodb://localhost:27017/")
db = cliente["FINTECH_DB"]

# --- CONEXIÓN ORACLE ---
# IMPORTANTE: Rellena tus datos aquí antes de ejecutar
try:
    conexion_oracle = oracledb.connect(
        user="system",
        password="12345678",
        dsn="localhost/xe"
    )
    cursor_oracle = conexion_oracle.cursor()
    print("Conexión a Oracle exitosa")
except Exception as e:
    print("Error conectando a Oracle:", e)
    cursor_oracle = None
