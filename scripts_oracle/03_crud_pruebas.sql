-- Pruebas CRUD para mostrar en la sustentacion.
-- Ejecuta por bloques para tomar capturas.

-- CREATE / INSERT
INSERT INTO usuario (
    id_usuario, nombre, apellido, correo, password_hash, fecha_registro, estado
) VALUES (
    101, 'Carlos', 'Prueba', 'carlos.prueba@smartbudget.com', 'HASH_101', SYSDATE, 'ACTIVO'
);

INSERT INTO cuenta_bancaria (
    id_cuenta, id_usuario, banco, numero_cuenta, tipo_cuenta, saldo_actual, moneda
) VALUES (
    101, 101, 'BCP', 'CTA2026101', 'AHORROS', 500, 'PEN'
);

COMMIT;

-- READ / SELECT
SELECT u.id_usuario, u.nombre, u.correo, c.banco, c.saldo_actual
FROM usuario u
JOIN cuenta_bancaria c ON c.id_usuario = u.id_usuario
WHERE u.id_usuario = 101;

-- UPDATE
UPDATE usuario
SET nombre = 'Carlos Actualizado'
WHERE id_usuario = 101;

COMMIT;

SELECT id_usuario, nombre, correo
FROM usuario
WHERE id_usuario = 101;

-- PROCEDURE + TRIGGER
-- La cuenta 101 inicia con saldo 500. Este ingreso debe subir el saldo a 650.
BEGIN
    sp_registrar_transaccion(
        p_id_transaccion => 101,
        p_id_cuenta      => 101,
        p_id_categoria   => 1,
        p_monto          => 150,
        p_tipo           => 'INGRESO',
        p_descripcion    => 'Ingreso de prueba desde procedimiento'
    );
END;
/

COMMIT;

SELECT id_cuenta, saldo_actual
FROM cuenta_bancaria
WHERE id_cuenta = 101;

-- DELETE
DELETE FROM transaccion WHERE id_transaccion = 101;
DELETE FROM cuenta_bancaria WHERE id_cuenta = 101;
DELETE FROM usuario WHERE id_usuario = 101;

COMMIT;

SELECT *
FROM usuario
WHERE id_usuario = 101;

