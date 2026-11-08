-- Ejecutar solo en saica del equipo; no contiene DROP.
BEGIN;
CREATE SCHEMA IF NOT EXISTS planta;
CREATE TABLE IF NOT EXISTS planta.lotes (
 lote_id text PRIMARY KEY, planta_id text NOT NULL,
 kg numeric(12,2) NOT NULL CHECK (kg>=0),
 estado text NOT NULL CHECK (estado IN ('abierto','cerrado')),
 creado timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS planta.eventos (
 event_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 lote_id text NOT NULL REFERENCES planta.lotes(lote_id),
 fecha timestamptz NOT NULL,
 temperatura numeric(6,2) NOT NULL,
 origen text NOT NULL
);
INSERT INTO planta.lotes(lote_id,planta_id,kg,estado)
SELECT 'L'||lpad(n::text,3,'0'),'P'||lpad((n%2+1)::text,2,'0'),100+n,'abierto'
FROM generate_series(0,11) AS n ON CONFLICT(lote_id) DO NOTHING;
-- La carga se ejecuta una sola vez. No añadir otra copia al repetir el script.
INSERT INTO planta.eventos(lote_id,fecha,temperatura,origen)
SELECT 'L'||lpad((n%12)::text,3,'0'),timestamptz '2026-10-01 00:00:00+00'+n*interval '1 second',20+(n%30)/10.0,'sintetico'
FROM generate_series(1,12000) AS n
WHERE NOT EXISTS (SELECT 1 FROM planta.eventos);
COMMIT;
SELECT count(*) AS lotes FROM planta.lotes;
SELECT count(*) AS eventos FROM planta.eventos;
