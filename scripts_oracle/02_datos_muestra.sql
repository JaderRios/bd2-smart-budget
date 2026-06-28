-- Datos de muestra: al menos 30 registros por tabla principal.

INSERT INTO categoria VALUES (1, 'Sueldo', 'INGRESO');
INSERT INTO categoria VALUES (2, 'Freelance', 'INGRESO');
INSERT INTO categoria VALUES (3, 'Bonos', 'INGRESO');
INSERT INTO categoria VALUES (4, 'Alimentacion', 'GASTO');
INSERT INTO categoria VALUES (5, 'Transporte', 'GASTO');
INSERT INTO categoria VALUES (6, 'Educacion', 'GASTO');
INSERT INTO categoria VALUES (7, 'Servicios', 'GASTO');
INSERT INTO categoria VALUES (8, 'Salud', 'GASTO');
INSERT INTO categoria VALUES (9, 'Entretenimiento', 'GASTO');
INSERT INTO categoria VALUES (10, 'Ahorro programado', 'GASTO');

BEGIN
    FOR i IN 11..30 LOOP
        INSERT INTO categoria (
            id_categoria, nombre, tipo
        ) VALUES (
            i,
            'Categoria adicional ' || i,
            CASE WHEN MOD(i, 5) = 0 THEN 'INGRESO' ELSE 'GASTO' END
        );
    END LOOP;
END;
/

BEGIN
    FOR i IN 1..30 LOOP
        INSERT INTO usuario (
            id_usuario, nombre, apellido, correo, password_hash, fecha_registro, estado
        ) VALUES (
            i,
            'Usuario' || i,
            'Fintech' || i,
            'usuario' || i || '@smartbudget.com',
            'HASH_' || i,
            SYSDATE - i,
            'ACTIVO'
        );

        INSERT INTO cuenta_bancaria (
            id_cuenta, id_usuario, banco, numero_cuenta, tipo_cuenta, saldo_actual, moneda
        ) VALUES (
            i,
            i,
            CASE MOD(i, 4)
                WHEN 0 THEN 'BCP'
                WHEN 1 THEN 'Interbank'
                WHEN 2 THEN 'BBVA'
                ELSE 'Scotiabank'
            END,
            'CTA2026' || LPAD(i, 4, '0'),
            CASE WHEN MOD(i, 2) = 0 THEN 'AHORROS' ELSE 'CORRIENTE' END,
            1000 + (i * 25),
            'PEN'
        );

        INSERT INTO meta_ahorro (
            id_meta, id_usuario, nombre_meta, monto_objetivo, monto_actual, fecha_limite, estado
        ) VALUES (
            i,
            i,
            'Meta de ahorro ' || i,
            1500 + (i * 100),
            200 + (i * 30),
            ADD_MONTHS(SYSDATE, 3),
            'EN_PROCESO'
        );

        INSERT INTO estado_cuenta (
            id_estado, id_cuenta, fecha_inicio, fecha_fin, saldo_inicial, saldo_final
        ) VALUES (
            i,
            i,
            TRUNC(ADD_MONTHS(SYSDATE, -1)),
            TRUNC(SYSDATE),
            900 + (i * 20),
            1000 + (i * 25)
        );
    END LOOP;
END;
/

BEGIN
    FOR i IN 1..30 LOOP
        INSERT INTO transaccion (
            id_transaccion, id_cuenta, id_categoria, fecha_transaccion, monto, tipo, descripcion
        ) VALUES (
            i,
            i,
            CASE WHEN MOD(i, 3) = 0 THEN 1 ELSE 4 + MOD(i, 6) END,
            SYSDATE - MOD(i, 20),
            20 + (i * 3),
            CASE WHEN MOD(i, 3) = 0 THEN 'INGRESO' ELSE 'GASTO' END,
            'Movimiento financiero de prueba ' || i
        );
    END LOOP;
END;
/

COMMIT;

SELECT 'USUARIO' tabla, COUNT(*) total FROM usuario
UNION ALL SELECT 'CUENTA_BANCARIA', COUNT(*) FROM cuenta_bancaria
UNION ALL SELECT 'CATEGORIA', COUNT(*) FROM categoria
UNION ALL SELECT 'TRANSACCION', COUNT(*) FROM transaccion
UNION ALL SELECT 'META_AHORRO', COUNT(*) FROM meta_ahorro
UNION ALL SELECT 'ESTADO_CUENTA', COUNT(*) FROM estado_cuenta;
