ANALYZE planta.eventos;
EXPLAIN (ANALYZE,BUFFERS) SELECT * FROM planta.eventos
WHERE lote_id='L001' AND fecha>=timestamptz '2026-10-01 01:00:00+00'
ORDER BY fecha;
-- Medir primero sin este índice, después con él; no modificar consulta y datos a la vez.
CREATE INDEX IF NOT EXISTS eventos_lote_fecha_idx ON planta.eventos(lote_id,fecha);
ANALYZE planta.eventos;
EXPLAIN (ANALYZE,BUFFERS) SELECT * FROM planta.eventos
WHERE lote_id='L001' AND fecha>=timestamptz '2026-10-01 01:00:00+00'
ORDER BY fecha;
SELECT pg_size_pretty(pg_total_relation_size('planta.eventos')) AS espacio_total;
