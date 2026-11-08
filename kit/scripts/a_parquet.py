import argparse,csv
from pathlib import Path
import pyarrow as pa,pyarrow.dataset as ds
p=argparse.ArgumentParser();p.add_argument('csv');p.add_argument('dest');a=p.parse_args()
dest=Path(a.dest)
if dest.exists() and any(dest.iterdir()):p.error('Usa un directorio vacío para evitar mezclar ejecuciones')
with open(a.csv,newline='',encoding='utf-8') as f:rows=list(csv.DictReader(f))
for row in rows:
    row['kg']=float(row['kg']);row['temperatura']=float(row['temperatura'])
schema=pa.schema([(x,pa.float64() if x in ('kg','temperatura') else pa.string()) for x in ['event_id','ts','planta','lote','temperatura','kg','fecha']])
ds.write_dataset(pa.Table.from_pylist(rows,schema=schema),str(dest),format='parquet',partitioning=['fecha'],partitioning_flavor='hive',existing_data_behavior='error')
print('Parquet particionado por fecha; comparar conteo, suma y bytes antes de publicar')
