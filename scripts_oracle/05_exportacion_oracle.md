# Exportacion de Oracle

## Opcion rapida desde SQL Developer

1. Abre Oracle SQL Developer.
2. Conectate al esquema donde creaste las tablas.
3. Clic derecho sobre el usuario o sobre cada tabla.
4. Elige `Export`.
5. Marca `DDL` y `Data`.
6. Formato recomendado: `SQL Insert`.
7. Guarda el archivo como `smartbudget_oracle_export.sql`.

## Opcion con Data Pump

Si tienes permisos de administrador:

```sql
CREATE OR REPLACE DIRECTORY export_dir AS 'C:\oracle_exports';
GRANT READ, WRITE ON DIRECTORY export_dir TO tu_usuario;
```

Desde consola:

```bash
expdp tu_usuario/tu_password schemas=tu_usuario directory=export_dir dumpfile=smartbudget_oracle.dmp logfile=smartbudget_oracle.log
```

## Que colocar en el informe

- Oracle almacena los datos transaccionales porque requieren integridad referencial, restricciones, relaciones entre tablas y consistencia ACID.
- El trigger `trg_actualiza_saldo` actualiza automaticamente el saldo de la cuenta cuando se inserta una transaccion.
- El procedimiento `sp_registrar_transaccion` simula una operacion real de la aplicacion.
- Los roles separan permisos de consulta y permisos operativos.

