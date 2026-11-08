BEGIN;
UPDATE planta.lotes SET kg=kg+1 WHERE lote_id='L001';
SELECT lote_id,kg FROM planta.lotes WHERE lote_id='L001';
ROLLBACK;
SELECT lote_id,kg FROM planta.lotes WHERE lote_id='L001';
-- Ensayo negativo separado: CHECK debe rechazar kg=-1. Ejecutar interactivamente.
-- BEGIN; UPDATE planta.lotes SET kg=-1 WHERE lote_id='L001'; ROLLBACK;
