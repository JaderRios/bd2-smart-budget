from conexion import db

# CREATE
def guardar_factura(usuario_id, empresa, monto, categoria, detalles_json=None):
    if detalles_json is None:
        detalles_json = {}

    factura = {
        "usuario_id": usuario_id,
        "empresa": empresa,
        "monto": monto,
        "categoria": categoria,
        "detalles": detalles_json
    }

    db.facturas.insert_one(factura)


# READ
def obtener_facturas():

    return list(
        db.facturas.find(
            {},
            {"_id": 0}
        )
    )


# UPDATE
def actualizar_factura(usuario_id, empresa, monto, categoria, detalles_json=None):
    if detalles_json is None:
        detalles_json = {}
        
    db.facturas.update_one(
        {"usuario_id": usuario_id},
        {
            "$set":
            {
                "empresa": empresa,
                "monto": monto,
                "categoria": categoria,
                "detalles": detalles_json
            }
        }
    )


# DELETE
def eliminar_factura(usuario_id):

    db.facturas.delete_one(
        {"usuario_id": usuario_id}
    )

def total_facturas():
    return db.facturas.count_documents({})

def monto_total():

    facturas = db.facturas.find()

    total = 0

    for f in facturas:

        total += float(
            f.get("monto",0)
        )

    return total

def obtener_notificaciones():
    return list(db.notificaciones.find({}, {"_id": 0}))

def obtener_sincronizaciones():
    return list(db.sincronizaciones.find({}, {"_id": 0}))
