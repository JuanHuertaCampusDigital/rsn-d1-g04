-- EXPLAIN ANALYZE EJECUTA las escrituras. Solo muestra sintética del equipo.
-- ROLLBACK deshace filas, no el avance de una secuencia: no exigir IDs consecutivos.
\timing on
BEGIN;
EXPLAIN (ANALYZE,BUFFERS) INSERT INTO planta.eventos(lote_id,fecha,temperatura,origen)
VALUES ('L001',timestamptz '2026-10-02 00:00:00+00',21.5,'ensayo-crud');
EXPLAIN (ANALYZE,BUFFERS) UPDATE planta.lotes SET kg=kg+1 WHERE lote_id='L001';
EXPLAIN (ANALYZE,BUFFERS) SELECT * FROM planta.lotes WHERE lote_id='L001';
ROLLBACK;
SELECT count(*) AS eventos_tras_rollback FROM planta.eventos;
