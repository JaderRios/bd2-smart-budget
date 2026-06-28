# SmartBudget FinTech - Parte Oracle

Tu parte cubre la base de datos relacional del proyecto. Oracle guarda la informacion estructurada y transaccional:

- Usuarios
- Cuentas bancarias
- Categorias
- Transacciones
- Metas de ahorro
- Estados de cuenta

## Orden de ejecucion en Oracle SQL Developer

1. Ejecuta `01_schema_oracle.sql`
2. Ejecuta `02_datos_muestra.sql`
3. Ejecuta `03_crud_pruebas.sql` por partes para tomar capturas
4. Ejecuta `04_seguridad.sql` si tienes permisos de administrador
5. Usa `05_exportacion_oracle.md` como guia para exportar

## Que capturas debes tomar

- Tablas creadas en SQL Developer.
- Diagrama entidad relacion.
- Resultado de `SELECT COUNT(*)` por tabla.
- Pruebas CRUD: INSERT, SELECT, UPDATE y DELETE.
- Trigger actualizando saldo de cuenta.
- Procedimiento almacenado ejecutado.
- Usuario/rol creado para seguridad, si tu Oracle lo permite.

## DER sugerido

```mermaid
erDiagram
    USUARIO ||--o{ CUENTA_BANCARIA : posee
    USUARIO ||--o{ META_AHORRO : define
    CUENTA_BANCARIA ||--o{ TRANSACCION : registra
    CUENTA_BANCARIA ||--o{ ESTADO_CUENTA : genera
    CATEGORIA ||--o{ TRANSACCION : clasifica

    USUARIO {
        NUMBER id_usuario PK
        VARCHAR2 nombre
        VARCHAR2 apellido
        VARCHAR2 correo UK
        VARCHAR2 password_hash
        DATE fecha_registro
        VARCHAR2 estado
    }

    CUENTA_BANCARIA {
        NUMBER id_cuenta PK
        NUMBER id_usuario FK
        VARCHAR2 banco
        VARCHAR2 numero_cuenta UK
        VARCHAR2 tipo_cuenta
        NUMBER saldo_actual
        VARCHAR2 moneda
    }

    CATEGORIA {
        NUMBER id_categoria PK
        VARCHAR2 nombre
        VARCHAR2 tipo
    }

    TRANSACCION {
        NUMBER id_transaccion PK
        NUMBER id_cuenta FK
        NUMBER id_categoria FK
        DATE fecha_transaccion
        NUMBER monto
        VARCHAR2 tipo
        VARCHAR2 descripcion
    }

    META_AHORRO {
        NUMBER id_meta PK
        NUMBER id_usuario FK
        VARCHAR2 nombre_meta
        NUMBER monto_objetivo
        NUMBER monto_actual
        DATE fecha_limite
        VARCHAR2 estado
    }

    ESTADO_CUENTA {
        NUMBER id_estado PK
        NUMBER id_cuenta FK
        DATE fecha_inicio
        DATE fecha_fin
        NUMBER saldo_inicial
        NUMBER saldo_final
    }
```

