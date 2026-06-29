from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

# Importar funciones de Oracle
from crud_oracle import (
    obtener_usuarios, crear_usuario, actualizar_usuario, eliminar_usuario,
    obtener_cuentas, crear_cuenta, actualizar_cuenta, eliminar_cuenta,
    obtener_categorias, crear_categoria, actualizar_categoria, eliminar_categoria,
    obtener_transacciones, crear_transaccion, actualizar_transaccion, eliminar_transaccion,
    obtener_metas, crear_meta, actualizar_meta, eliminar_meta,
    obtener_estados, crear_estado, actualizar_estado, eliminar_estado
)

# Importar funciones de MongoDB
from crud_facturas import (
    obtener_facturas, guardar_factura, actualizar_factura, eliminar_factura,
    obtener_notificaciones, obtener_sincronizaciones
)

app = FastAPI(title="SmartBudget API", version="1.0")

# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Modelos Pydantic (Validación de entrada) ---
class UsuarioCreate(BaseModel):
    nombre: str
    apellido: str
    correo: str

class CuentaCreate(BaseModel):
    id_usuario: int
    banco: str
    numero_cuenta: str
    saldo_actual: float

class CategoriaCreate(BaseModel):
    nombre: str
    tipo: str

class TransaccionCreate(BaseModel):
    id_cuenta: int
    id_categoria: int
    monto: float
    tipo: str
    descripcion: str

class MetaCreate(BaseModel):
    id_usuario: int
    nombre_meta: str
    monto_objetivo: float
    monto_actual: float
    fecha_limite: str
    estado: str

class EstadoCreate(BaseModel):
    id_cuenta: int
    fecha_inicio: str
    fecha_fin: str
    saldo_inicial: float
    saldo_final: float

class FacturaCreate(BaseModel):
    usuario_id: int
    empresa: str
    monto: float
    categoria: str
    detalles: dict = {}

# Modelos Update (Suelen ser iguales pero pueden diferir. Los hacemos idénticos para simplicidad)
UsuarioUpdate = UsuarioCreate
CuentaUpdate = CuentaCreate
CategoriaUpdate = CategoriaCreate
TransaccionUpdate = TransaccionCreate
MetaUpdate = MetaCreate
EstadoUpdate = EstadoCreate
FacturaUpdate = FacturaCreate

# --- ENDPOINTS ORACLE ---

# USUARIOS
@app.get("/api/usuarios")
def get_usuarios():
    data = obtener_usuarios()
    return [{"id_usuario": row[0], "nombre": row[1], "apellido": row[2], "correo": row[3]} for row in (data or [])]

@app.post("/api/usuarios")
def post_usuario(u: UsuarioCreate):
    if not crear_usuario(u.nombre, u.apellido, u.correo):
        raise HTTPException(status_code=500, detail="Error al crear usuario")
    return {"message": "Éxito"}

@app.put("/api/usuarios/{id}")
def put_usuario(id: int, u: UsuarioUpdate):
    if not actualizar_usuario(id, u.nombre, u.apellido, u.correo):
        raise HTTPException(status_code=500, detail="Error al actualizar usuario")
    return {"message": "Éxito"}

@app.delete("/api/usuarios/{id}")
def delete_usuario(id: int):
    if not eliminar_usuario(id):
        raise HTTPException(status_code=500, detail="Error al eliminar usuario")
    return {"message": "Éxito"}

# CUENTAS
@app.get("/api/cuentas")
def get_cuentas():
    data = obtener_cuentas()
    return [{"id_cuenta": row[0], "propietario": row[1], "banco": row[2], "nro_cuenta": row[3], "saldo_actual": row[4]} for row in (data or [])]

@app.post("/api/cuentas")
def post_cuenta(c: CuentaCreate):
    if not crear_cuenta(c.id_usuario, c.banco, c.numero_cuenta, c.saldo_actual):
        raise HTTPException(status_code=500, detail="Error al crear cuenta")
    return {"message": "Éxito"}

@app.put("/api/cuentas/{id}")
def put_cuenta(id: int, c: CuentaUpdate):
    if not actualizar_cuenta(id, c.banco, c.numero_cuenta, c.saldo_actual):
        raise HTTPException(status_code=500, detail="Error al actualizar cuenta")
    return {"message": "Éxito"}

@app.delete("/api/cuentas/{id}")
def delete_cuenta(id: int):
    if not eliminar_cuenta(id):
        raise HTTPException(status_code=500, detail="Error al eliminar cuenta")
    return {"message": "Éxito"}

# CATEGORIAS
@app.get("/api/categorias")
def get_categorias():
    data = obtener_categorias()
    return [{"id_categoria": row[0], "nombre": row[1], "tipo": row[2]} for row in (data or [])]

@app.post("/api/categorias")
def post_categoria(c: CategoriaCreate):
    if not crear_categoria(c.nombre, c.tipo):
        raise HTTPException(status_code=500, detail="Error al crear categoria")
    return {"message": "Éxito"}

@app.put("/api/categorias/{id}")
def put_categoria(id: int, c: CategoriaUpdate):
    if not actualizar_categoria(id, c.nombre, c.tipo):
        raise HTTPException(status_code=500, detail="Error al actualizar categoria")
    return {"message": "Éxito"}

@app.delete("/api/categorias/{id}")
def delete_categoria(id: int):
    if not eliminar_categoria(id):
        raise HTTPException(status_code=500, detail="Error al eliminar categoria")
    return {"message": "Éxito"}

# TRANSACCIONES
@app.get("/api/transacciones")
def get_transacciones():
    data = obtener_transacciones()
    return [{"id_transaccion": row[0], "numero_cuenta": row[1], "categoria": row[2], "fecha": row[3], "monto": row[4], "tipo": row[5], "descripcion": row[6], "id_cuenta": row[7], "id_categoria": row[8]} for row in (data or [])]

@app.post("/api/transacciones")
def post_transaccion(t: TransaccionCreate):
    if not crear_transaccion(t.id_cuenta, t.id_categoria, t.monto, t.tipo, t.descripcion):
        raise HTTPException(status_code=500, detail="Error al ejecutar el SP de transacción")
    return {"message": "Éxito"}

@app.put("/api/transacciones/{id}")
def put_transaccion(id: int, t: TransaccionUpdate):
    # crud_oracle.actualizar_transaccion signature: (id_transaccion, monto, tipo, descripcion)
    if not actualizar_transaccion(id, t.monto, t.tipo, t.descripcion):
        raise HTTPException(status_code=500, detail="Error al actualizar transacción")
    return {"message": "Éxito"}

@app.delete("/api/transacciones/{id}")
def delete_transaccion(id: int):
    if not eliminar_transaccion(id):
        raise HTTPException(status_code=500, detail="Error al eliminar transacción")
    return {"message": "Éxito"}

# METAS
@app.get("/api/metas")
def get_metas():
    data = obtener_metas()
    return [{"id_meta": row[0], "usuario": row[1], "nombre_meta": row[2], "monto_objetivo": row[3], "monto_actual": row[4], "fecha_limite": row[5], "estado": row[6], "id_usuario": row[7]} for row in (data or [])]

@app.post("/api/metas")
def post_meta(m: MetaCreate):
    if not crear_meta(m.id_usuario, m.nombre_meta, m.monto_objetivo, m.monto_actual, m.fecha_limite, m.estado):
        raise HTTPException(status_code=500, detail="Error al crear meta")
    return {"message": "Éxito"}

@app.put("/api/metas/{id}")
def put_meta(id: int, m: MetaUpdate):
    if not actualizar_meta(id, m.nombre_meta, m.monto_objetivo, m.monto_actual, m.fecha_limite, m.estado):
        raise HTTPException(status_code=500, detail="Error al actualizar meta")
    return {"message": "Éxito"}

@app.delete("/api/metas/{id}")
def delete_meta(id: int):
    if not eliminar_meta(id):
        raise HTTPException(status_code=500, detail="Error al eliminar meta")
    return {"message": "Éxito"}

# ESTADOS DE CUENTA
@app.get("/api/estados")
def get_estados():
    data = obtener_estados()
    return [{"id_estado": row[0], "numero_cuenta": row[1], "fecha_inicio": row[2], "fecha_fin": row[3], "saldo_inicial": row[4], "saldo_final": row[5], "id_cuenta": row[6]} for row in (data or [])]

@app.post("/api/estados")
def post_estado(e: EstadoCreate):
    if not crear_estado(e.id_cuenta, e.fecha_inicio, e.fecha_fin, e.saldo_inicial, e.saldo_final):
        raise HTTPException(status_code=500, detail="Error al crear estado")
    return {"message": "Éxito"}

@app.put("/api/estados/{id}")
def put_estado(id: int, e: EstadoUpdate):
    if not actualizar_estado(id, e.fecha_inicio, e.fecha_fin, e.saldo_inicial, e.saldo_final):
        raise HTTPException(status_code=500, detail="Error al actualizar estado")
    return {"message": "Éxito"}

@app.delete("/api/estados/{id}")
def delete_estado(id: int):
    if not eliminar_estado(id):
        raise HTTPException(status_code=500, detail="Error al eliminar estado")
    return {"message": "Éxito"}

# --- ENDPOINTS MONGODB ---

@app.get("/api/facturas")
def get_facturas():
    return obtener_facturas()

@app.post("/api/facturas")
def post_factura(f: FacturaCreate):
    guardar_factura(f.usuario_id, f.empresa, f.monto, f.categoria, f.detalles)
    return {"message": "Éxito"}

@app.put("/api/facturas/{user_id}")
def put_factura(user_id: int, f: FacturaUpdate):
    actualizar_factura(user_id, f.empresa, f.monto, f.categoria, f.detalles)
    return {"message": "Éxito"}

@app.delete("/api/facturas/{user_id}")
def delete_fact(user_id: int):
    eliminar_factura(user_id)
    return {"message": "Éxito"}

@app.get("/api/notificaciones")
def get_notificaciones():
    return obtener_notificaciones()

@app.get("/api/sincronizaciones")
def get_sincronizaciones():
    return obtener_sincronizaciones()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api_main:app", host="127.0.0.1", port=8000, reload=True)
