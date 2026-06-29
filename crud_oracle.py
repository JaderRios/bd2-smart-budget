from conexion import cursor_oracle, conexion_oracle

# --- USUARIOS ---
def obtener_usuarios():
    if not cursor_oracle:
        return []
    try:
        cursor_oracle.execute("SELECT id_usuario, nombre, apellido, correo FROM usuario")
        return cursor_oracle.fetchall()
    except Exception as e:
        print("Error obteniendo usuarios:", e)
        return []

def crear_usuario(nombre, apellido, correo):
    if not cursor_oracle:
        return False
    try:
        cursor_oracle.execute(
            "INSERT INTO usuario (id_usuario, nombre, apellido, correo, password_hash) VALUES ((SELECT NVL(MAX(id_usuario), 0) + 1 FROM usuario), :1, :2, :3, 'default_hash')",
            (nombre, apellido, correo)
        )
        conexion_oracle.commit()
        return True
    except Exception as e:
        print("Error creando usuario:", e)
        return False

def actualizar_usuario(id_usuario, nombre, apellido, correo):
    if not cursor_oracle:
        return False
    try:
        cursor_oracle.execute(
            "UPDATE usuario SET nombre = :1, apellido = :2, correo = :3 WHERE id_usuario = :4",
            (nombre, apellido, correo, id_usuario)
        )
        conexion_oracle.commit()
        return True
    except Exception as e:
        print("Error actualizando usuario:", e)
        return False

def eliminar_usuario(id_usuario):
    if not cursor_oracle:
        return False
    try:
        cursor_oracle.execute("DELETE FROM usuario WHERE id_usuario = :1", (id_usuario,))
        conexion_oracle.commit()
        return True
    except Exception as e:
        print("Error eliminando usuario:", e)
        return False

# --- CUENTAS ---
def obtener_cuentas():
    if not cursor_oracle:
        return []
    try:
        query = """
        SELECT c.id_cuenta, u.nombre, c.banco, c.numero_cuenta, c.saldo_actual, c.id_usuario 
        FROM cuenta_bancaria c
        JOIN usuario u ON c.id_usuario = u.id_usuario
        """
        cursor_oracle.execute(query)
        return cursor_oracle.fetchall()
    except Exception as e:
        print("Error obteniendo cuentas:", e)
        return []

def crear_cuenta(id_usuario, banco, numero_cuenta, saldo_actual):
    if not cursor_oracle:
        return False
    try:
        cursor_oracle.execute(
            "INSERT INTO cuenta_bancaria (id_cuenta, id_usuario, banco, numero_cuenta, tipo_cuenta, saldo_actual, moneda) VALUES ((SELECT NVL(MAX(id_cuenta), 0) + 1 FROM cuenta_bancaria), :1, :2, :3, 'AHORROS', :4, 'PEN')",
            (id_usuario, banco, numero_cuenta, saldo_actual)
        )
        conexion_oracle.commit()
        return True
    except Exception as e:
        print("Error creando cuenta:", e)
        return False

def actualizar_cuenta(id_cuenta, banco, numero_cuenta, saldo_actual):
    if not cursor_oracle:
        return False
    try:
        cursor_oracle.execute(
            "UPDATE cuenta_bancaria SET banco = :1, numero_cuenta = :2, saldo_actual = :3 WHERE id_cuenta = :4",
            (banco, numero_cuenta, saldo_actual, id_cuenta)
        )
        conexion_oracle.commit()
        return True
    except Exception as e:
        print("Error actualizando cuenta:", e)
        return False

def eliminar_cuenta(id_cuenta):
    if not cursor_oracle:
        return False
    try:
        cursor_oracle.execute("DELETE FROM cuenta_bancaria WHERE id_cuenta = :1", (id_cuenta,))
        conexion_oracle.commit()
        return True
    except Exception as e:
        print("Error eliminando cuenta:", e)
        return False


# --- CATEGORÍAS ---
def obtener_categorias():
    if not cursor_oracle:
        return []
    try:
        cursor_oracle.execute("SELECT id_categoria, nombre, tipo FROM categoria")
        return cursor_oracle.fetchall()
    except Exception as e:
        print("Error obteniendo categorías:", e)
        return []

def crear_categoria(nombre, tipo):
    if not cursor_oracle:
        return False
    try:
        cursor_oracle.execute(
            "INSERT INTO categoria (id_categoria, nombre, tipo) VALUES ((SELECT NVL(MAX(id_categoria), 0) + 1 FROM categoria), :1, :2)",
            (nombre, tipo)
        )
        conexion_oracle.commit()
        return True
    except Exception as e:
        print("Error creando categoría:", e)
        return False

def actualizar_categoria(id_categoria, nombre, tipo):
    if not cursor_oracle:
        return False
    try:
        cursor_oracle.execute(
            "UPDATE categoria SET nombre = :1, tipo = :2 WHERE id_categoria = :3",
            (nombre, tipo, id_categoria)
        )
        conexion_oracle.commit()
        return True
    except Exception as e:
        print("Error actualizando categoría:", e)
        return False

def eliminar_categoria(id_categoria):
    if not cursor_oracle:
        return False
    try:
        cursor_oracle.execute("DELETE FROM categoria WHERE id_categoria = :1", (id_categoria,))
        conexion_oracle.commit()
        return True
    except Exception as e:
        print("Error eliminando categoría:", e)
        return False


# --- TRANSACCIONES ---
def obtener_transacciones():
    if not cursor_oracle:
        return []
    try:
        query = """
        SELECT t.id_transaccion, c.numero_cuenta, cat.nombre, TO_CHAR(t.fecha_transaccion, 'YYYY-MM-DD HH24:MI'), t.monto, t.tipo, t.descripcion, t.id_cuenta, t.id_categoria
        FROM transaccion t
        JOIN cuenta_bancaria c ON t.id_cuenta = c.id_cuenta
        JOIN categoria cat ON t.id_categoria = cat.id_categoria
        ORDER BY t.fecha_transaccion DESC
        """
        cursor_oracle.execute(query)
        return cursor_oracle.fetchall()
    except Exception as e:
        print("Error obteniendo transacciones:", e)
        return []

def crear_transaccion(id_cuenta, id_categoria, monto, tipo, descripcion):
    if not cursor_oracle:
        return False
    try:
        # Obtener el próximo ID de transacción
        cursor_oracle.execute("SELECT NVL(MAX(id_transaccion), 0) + 1 FROM transaccion")
        next_id = cursor_oracle.fetchone()[0]
        
        # Llamar al stored procedure de Oracle
        cursor_oracle.callproc("sp_registrar_transaccion", [
            next_id,
            id_cuenta,
            id_categoria,
            monto,
            tipo,
            descripcion
        ])
        conexion_oracle.commit()
        return True
    except Exception as e:
        print("Error creando transacción:", e)
        return False

def actualizar_transaccion(id_transaccion, monto, tipo, descripcion):
    if not cursor_oracle:
        return False
    try:
        cursor_oracle.execute(
            "UPDATE transaccion SET monto = :1, tipo = :2, descripcion = :3 WHERE id_transaccion = :4",
            (monto, tipo, descripcion, id_transaccion)
        )
        conexion_oracle.commit()
        return True
    except Exception as e:
        print("Error actualizando transacción:", e)
        return False

def eliminar_transaccion(id_transaccion):
    if not cursor_oracle:
        return False
    try:
        cursor_oracle.execute("DELETE FROM transaccion WHERE id_transaccion = :1", (id_transaccion,))
        conexion_oracle.commit()
        return True
    except Exception as e:
        print("Error eliminando transacción:", e)
        return False


# --- METAS DE AHORRO ---
def obtener_metas():
    if not cursor_oracle:
        return []
    try:
        query = """
        SELECT m.id_meta, u.nombre || ' ' || u.apellido, m.nombre_meta, m.monto_objetivo, m.monto_actual, TO_CHAR(m.fecha_limite, 'YYYY-MM-DD'), m.estado, m.id_usuario
        FROM meta_ahorro m
        JOIN usuario u ON m.id_usuario = u.id_usuario
        """
        cursor_oracle.execute(query)
        return cursor_oracle.fetchall()
    except Exception as e:
        print("Error obteniendo metas:", e)
        return []

def crear_meta(id_usuario, nombre_meta, monto_objetivo, monto_actual, fecha_limite, estado):
    if not cursor_oracle:
        return False
    try:
        cursor_oracle.execute(
            "INSERT INTO meta_ahorro (id_meta, id_usuario, nombre_meta, monto_objetivo, monto_actual, fecha_limite, estado) VALUES ((SELECT NVL(MAX(id_meta), 0) + 1 FROM meta_ahorro), :1, :2, :3, :4, TO_DATE(:5, 'YYYY-MM-DD'), :6)",
            (id_usuario, nombre_meta, monto_objetivo, monto_actual, fecha_limite, estado)
        )
        conexion_oracle.commit()
        return True
    except Exception as e:
        print("Error creando meta:", e)
        return False

def actualizar_meta(id_meta, nombre_meta, monto_objetivo, monto_actual, fecha_limite, estado):
    if not cursor_oracle:
        return False
    try:
        cursor_oracle.execute(
            "UPDATE meta_ahorro SET nombre_meta = :1, monto_objetivo = :2, monto_actual = :3, fecha_limite = TO_DATE(:4, 'YYYY-MM-DD'), estado = :5 WHERE id_meta = :6",
            (nombre_meta, monto_objetivo, monto_actual, fecha_limite, estado, id_meta)
        )
        conexion_oracle.commit()
        return True
    except Exception as e:
        print("Error actualizando meta:", e)
        return False

def eliminar_meta(id_meta):
    if not cursor_oracle:
        return False
    try:
        cursor_oracle.execute("DELETE FROM meta_ahorro WHERE id_meta = :1", (id_meta,))
        conexion_oracle.commit()
        return True
    except Exception as e:
        print("Error eliminando meta:", e)
        return False


# --- ESTADOS DE CUENTA ---
def obtener_estados():
    if not cursor_oracle:
        return []
    try:
        query = """
        SELECT ec.id_estado, cb.numero_cuenta, TO_CHAR(ec.fecha_inicio, 'YYYY-MM-DD'), TO_CHAR(ec.fecha_fin, 'YYYY-MM-DD'), ec.saldo_inicial, ec.saldo_final, ec.id_cuenta
        FROM estado_cuenta ec
        JOIN cuenta_bancaria cb ON ec.id_cuenta = cb.id_cuenta
        """
        cursor_oracle.execute(query)
        return cursor_oracle.fetchall()
    except Exception as e:
        print("Error obteniendo estados de cuenta:", e)
        return []

def crear_estado(id_cuenta, fecha_inicio, fecha_fin, saldo_inicial, saldo_final):
    if not cursor_oracle:
        return False
    try:
        cursor_oracle.execute(
            "INSERT INTO estado_cuenta (id_estado, id_cuenta, fecha_inicio, fecha_fin, saldo_inicial, saldo_final) VALUES ((SELECT NVL(MAX(id_estado), 0) + 1 FROM estado_cuenta), :1, TO_DATE(:2, 'YYYY-MM-DD'), TO_DATE(:3, 'YYYY-MM-DD'), :4, :5)",
            (id_cuenta, fecha_inicio, fecha_fin, saldo_inicial, saldo_final)
        )
        conexion_oracle.commit()
        return True
    except Exception as e:
        print("Error creando estado de cuenta:", e)
        return False

def actualizar_estado(id_estado, fecha_inicio, fecha_fin, saldo_inicial, saldo_final):
    if not cursor_oracle:
        return False
    try:
        cursor_oracle.execute(
            "UPDATE estado_cuenta SET fecha_inicio = TO_DATE(:1, 'YYYY-MM-DD'), fecha_fin = TO_DATE(:2, 'YYYY-MM-DD'), saldo_inicial = :3, saldo_final = :4 WHERE id_estado = :5",
            (fecha_inicio, fecha_fin, saldo_inicial, saldo_final, id_estado)
        )
        conexion_oracle.commit()
        return True
    except Exception as e:
        print("Error actualizando estado de cuenta:", e)
        return False

def eliminar_estado(id_estado):
    if not cursor_oracle:
        return False
    try:
        cursor_oracle.execute("DELETE FROM estado_cuenta WHERE id_estado = :1", (id_estado,))
        conexion_oracle.commit()
        return True
    except Exception as e:
        print("Error eliminando estado de cuenta:", e)
        return False
