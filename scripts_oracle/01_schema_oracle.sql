-- SmartBudget FinTech - Modelo relacional Oracle
-- Ejecutar como usuario propietario del esquema.

BEGIN
   EXECUTE IMMEDIATE 'DROP TRIGGER trg_actualiza_saldo';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

BEGIN
   EXECUTE IMMEDIATE 'DROP PROCEDURE sp_registrar_transaccion';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE estado_cuenta CASCADE CONSTRAINTS';
   EXECUTE IMMEDIATE 'DROP TABLE meta_ahorro CASCADE CONSTRAINTS';
   EXECUTE IMMEDIATE 'DROP TABLE transaccion CASCADE CONSTRAINTS';
   EXECUTE IMMEDIATE 'DROP TABLE categoria CASCADE CONSTRAINTS';
   EXECUTE IMMEDIATE 'DROP TABLE cuenta_bancaria CASCADE CONSTRAINTS';
   EXECUTE IMMEDIATE 'DROP TABLE usuario CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

CREATE TABLE usuario (
    id_usuario      NUMBER PRIMARY KEY,
    nombre          VARCHAR2(50) NOT NULL,
    apellido        VARCHAR2(50) NOT NULL,
    correo          VARCHAR2(100) NOT NULL UNIQUE,
    password_hash   VARCHAR2(100) NOT NULL,
    fecha_registro  DATE DEFAULT SYSDATE NOT NULL,
    estado          VARCHAR2(15) DEFAULT 'ACTIVO' NOT NULL,
    CONSTRAINT chk_usuario_estado CHECK (estado IN ('ACTIVO', 'INACTIVO'))
);

CREATE TABLE cuenta_bancaria (
    id_cuenta      NUMBER PRIMARY KEY,
    id_usuario     NUMBER NOT NULL,
    banco          VARCHAR2(50) NOT NULL,
    numero_cuenta  VARCHAR2(30) NOT NULL UNIQUE,
    tipo_cuenta    VARCHAR2(20) NOT NULL,
    saldo_actual   NUMBER(12,2) DEFAULT 0 NOT NULL,
    moneda         VARCHAR2(3) DEFAULT 'PEN' NOT NULL,
    CONSTRAINT fk_cuenta_usuario FOREIGN KEY (id_usuario)
        REFERENCES usuario(id_usuario),
    CONSTRAINT chk_tipo_cuenta CHECK (tipo_cuenta IN ('AHORROS', 'CORRIENTE')),
    CONSTRAINT chk_saldo_actual CHECK (saldo_actual >= 0)
);

CREATE TABLE categoria (
    id_categoria  NUMBER PRIMARY KEY,
    nombre        VARCHAR2(50) NOT NULL,
    tipo          VARCHAR2(10) NOT NULL,
    CONSTRAINT chk_categoria_tipo CHECK (tipo IN ('INGRESO', 'GASTO'))
);

CREATE TABLE transaccion (
    id_transaccion     NUMBER PRIMARY KEY,
    id_cuenta          NUMBER NOT NULL,
    id_categoria       NUMBER NOT NULL,
    fecha_transaccion  DATE DEFAULT SYSDATE NOT NULL,
    monto              NUMBER(12,2) NOT NULL,
    tipo               VARCHAR2(10) NOT NULL,
    descripcion        VARCHAR2(200),
    CONSTRAINT fk_trans_cuenta FOREIGN KEY (id_cuenta)
        REFERENCES cuenta_bancaria(id_cuenta),
    CONSTRAINT fk_trans_categoria FOREIGN KEY (id_categoria)
        REFERENCES categoria(id_categoria),
    CONSTRAINT chk_trans_tipo CHECK (tipo IN ('INGRESO', 'GASTO')),
    CONSTRAINT chk_trans_monto CHECK (monto > 0)
);

CREATE TABLE meta_ahorro (
    id_meta         NUMBER PRIMARY KEY,
    id_usuario      NUMBER NOT NULL,
    nombre_meta     VARCHAR2(100) NOT NULL,
    monto_objetivo  NUMBER(12,2) NOT NULL,
    monto_actual    NUMBER(12,2) DEFAULT 0 NOT NULL,
    fecha_limite    DATE,
    estado          VARCHAR2(15) DEFAULT 'EN_PROCESO' NOT NULL,
    CONSTRAINT fk_meta_usuario FOREIGN KEY (id_usuario)
        REFERENCES usuario(id_usuario),
    CONSTRAINT chk_meta_montos CHECK (monto_objetivo > 0 AND monto_actual >= 0),
    CONSTRAINT chk_meta_estado CHECK (estado IN ('EN_PROCESO', 'CUMPLIDA', 'CANCELADA'))
);

CREATE TABLE estado_cuenta (
    id_estado      NUMBER PRIMARY KEY,
    id_cuenta      NUMBER NOT NULL,
    fecha_inicio   DATE NOT NULL,
    fecha_fin      DATE NOT NULL,
    saldo_inicial  NUMBER(12,2) NOT NULL,
    saldo_final    NUMBER(12,2) NOT NULL,
    CONSTRAINT fk_estado_cuenta FOREIGN KEY (id_cuenta)
        REFERENCES cuenta_bancaria(id_cuenta),
    CONSTRAINT chk_estado_fechas CHECK (fecha_fin >= fecha_inicio)
);

CREATE INDEX idx_cuenta_usuario ON cuenta_bancaria(id_usuario);
CREATE INDEX idx_trans_cuenta_fecha ON transaccion(id_cuenta, fecha_transaccion);
CREATE INDEX idx_meta_usuario ON meta_ahorro(id_usuario);
CREATE INDEX idx_estado_cuenta ON estado_cuenta(id_cuenta);

CREATE OR REPLACE TRIGGER trg_actualiza_saldo
AFTER INSERT ON transaccion
FOR EACH ROW
BEGIN
    IF :NEW.tipo = 'INGRESO' THEN
        UPDATE cuenta_bancaria
        SET saldo_actual = saldo_actual + :NEW.monto
        WHERE id_cuenta = :NEW.id_cuenta;
    ELSE
        UPDATE cuenta_bancaria
        SET saldo_actual = saldo_actual - :NEW.monto
        WHERE id_cuenta = :NEW.id_cuenta;
    END IF;
END;
/

CREATE OR REPLACE PROCEDURE sp_registrar_transaccion (
    p_id_transaccion IN NUMBER,
    p_id_cuenta      IN NUMBER,
    p_id_categoria   IN NUMBER,
    p_monto          IN NUMBER,
    p_tipo           IN VARCHAR2,
    p_descripcion    IN VARCHAR2
) AS
BEGIN
    INSERT INTO transaccion (
        id_transaccion,
        id_cuenta,
        id_categoria,
        fecha_transaccion,
        monto,
        tipo,
        descripcion
    ) VALUES (
        p_id_transaccion,
        p_id_cuenta,
        p_id_categoria,
        SYSDATE,
        p_monto,
        UPPER(p_tipo),
        p_descripcion
    );
END;
/

