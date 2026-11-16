CREATE TABLE IF NOT EXISTS pagos (
    id        SERIAL PRIMARY KEY,
    cliente   VARCHAR(64) NOT NULL DEFAULT 'anonimo',
    monto     NUMERIC(10, 2) NOT NULL,
    creado_en TIMESTAMPTZ NOT NULL DEFAULT now()
);