-- Sustituye CATALOGO_REAL y BUCKET_LAKE_REAL. Cada sentencia se lanza por separado en Athena.
CREATE EXTERNAL TABLE IF NOT EXISTS CATALOGO_REAL.eventos_raw (
 event_id string, ts string, planta string, lote string, temperatura double, kg double
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES ('separatorChar'=',')
LOCATION 's3://BUCKET_LAKE_REAL/raw/'
TBLPROPERTIES ('skip.header.line.count'='1');

CREATE EXTERNAL TABLE IF NOT EXISTS CATALOGO_REAL.eventos_curated (
 event_id string, ts string, planta string, lote string, temperatura double, kg double
)
PARTITIONED BY (fecha string)
STORED AS PARQUET
LOCATION 's3://BUCKET_LAKE_REAL/curated/';

MSCK REPAIR TABLE CATALOGO_REAL.eventos_curated;
SELECT fecha,planta,count(*) AS eventos,sum(kg) AS kg_total
FROM CATALOGO_REAL.eventos_curated
WHERE fecha='2026-10-01'
GROUP BY fecha,planta ORDER BY fecha,planta;
