\copy (SELECT lote_id,planta_id,kg,estado FROM planta.lotes ORDER BY lote_id) TO 'data/lotes_export.csv' WITH (FORMAT csv,HEADER true)
