from conexion import cursor_oracle

def obtener_usuarios():
    if not cursor_oracle:
        return []
    try:
        cursor_oracle.execute("SELECT id_usuario, nombre, apellido, correo FROM usuario")
        return cursor_oracle.fetchall()
    except Exception as e:
        print("Error obteniendo usuarios:", e)
        return []

def obtener_cuentas():
    if not cursor_oracle:
        return []
    try:
        query = """
        SELECT c.id_cuenta, u.nombre, c.banco, c.numero_cuenta, c.saldo_actual 
        FROM cuenta_bancaria c
        JOIN usuario u ON c.id_usuario = u.id_usuario
        """
        cursor_oracle.execute(query)
        return cursor_oracle.fetchall()
    except Exception as e:
        print("Error obteniendo cuentas:", e)
        return []
