-- Seguridad basica Oracle.
-- Ejecutar con un usuario administrador si tu instalacion tiene permisos.
-- Si falla por permisos, usalo como evidencia teorica en el informe.

-- Solucion para el error ORA-65096 (CDB/PDB en Oracle 12c+)
ALTER SESSION SET "_ORACLE_SCRIPT" = true;

CREATE ROLE rol_fintech_consulta;
CREATE ROLE rol_fintech_operador;

GRANT CREATE SESSION TO rol_fintech_consulta;
GRANT CREATE SESSION TO rol_fintech_operador;

GRANT SELECT ON usuario TO rol_fintech_consulta;
GRANT SELECT ON cuenta_bancaria TO rol_fintech_consulta;
GRANT SELECT ON transaccion TO rol_fintech_consulta;
GRANT SELECT ON meta_ahorro TO rol_fintech_consulta;
GRANT SELECT ON estado_cuenta TO rol_fintech_consulta;

GRANT SELECT, INSERT, UPDATE, DELETE ON usuario TO rol_fintech_operador;
GRANT SELECT, INSERT, UPDATE, DELETE ON cuenta_bancaria TO rol_fintech_operador;
GRANT SELECT, INSERT, UPDATE, DELETE ON categoria TO rol_fintech_operador;
GRANT SELECT, INSERT, UPDATE, DELETE ON transaccion TO rol_fintech_operador;
GRANT SELECT, INSERT, UPDATE, DELETE ON meta_ahorro TO rol_fintech_operador;
GRANT SELECT, INSERT, UPDATE, DELETE ON estado_cuenta TO rol_fintech_operador;
GRANT EXECUTE ON sp_registrar_transaccion TO rol_fintech_operador;

-- Ejemplo de usuario de aplicacion:
-- Cambia la contrasena si tu politica de Oracle exige mayusculas, numeros o simbolos.
CREATE USER fintech_app IDENTIFIED BY Fintech123;
GRANT rol_fintech_operador TO fintech_app;
ALTER USER fintech_app DEFAULT ROLE ALL;

-- Conectar con el usuario fintech_app y crear sinónimos para que no tenga que usar system.tabla
-- CREATE OR REPLACE SYNONYM fintech_app.usuario FOR system.usuario;
-- CREATE OR REPLACE SYNONYM fintech_app.cuenta_bancaria FOR system.cuenta_bancaria;
-- CREATE OR REPLACE SYNONYM fintech_app.categoria FOR system.categoria;
-- CREATE OR REPLACE SYNONYM fintech_app.transaccion FOR system.transaccion;
-- CREATE OR REPLACE SYNONYM fintech_app.meta_ahorro FOR system.meta_ahorro;
-- CREATE OR REPLACE SYNONYM fintech_app.estado_cuenta FOR system.estado_cuenta;
-- CREATE OR REPLACE SYNONYM fintech_app.sp_registrar_transaccion FOR system.sp_registrar_transaccion;
