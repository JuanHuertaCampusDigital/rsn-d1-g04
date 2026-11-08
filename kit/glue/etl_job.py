# AWS Glue Python shell: muestra pequeña. No es un ETL de producción ni procesa volúmenes ilimitados.
import argparse,csv,io,json,boto3
from datetime import datetime
p=argparse.ArgumentParser();p.add_argument('--bucket',required=True);p.add_argument('--input-key',required=True);p.add_argument('--run-id',required=True);a,_=p.parse_known_args()
s3=boto3.client('s3');obj=s3.get_object(Bucket=a.bucket,Key=a.input_key)
if obj['ContentLength']>1024*1024:raise ValueError('Limite docente 1 MiB')
reader=csv.DictReader(io.StringIO(obj['Body'].read().decode('utf-8')))
valid=[];bad=[];seen=set()
for n,row in enumerate(reader,2):
    try:
        ts=datetime.fromisoformat(row['ts']);kg=float(row['kg']);temp=float(row['temperatura'])
        import math
        if ts.tzinfo is None or not math.isfinite(kg) or not math.isfinite(temp) or kg<0 or row['event_id'] in seen or not row['event_id'] or not row['planta'] or not row['lote']:raise ValueError('dato no valido/duplicado')
        seen.add(row['event_id']);row.update(kg=kg,temperatura=temp,fecha=ts.date().isoformat());valid.append(row)
    except (ValueError,KeyError) as ex:bad.append({'line':n,'error':str(ex),'record':row})
payload=io.StringIO();w=csv.DictWriter(payload,fieldnames=['event_id','ts','planta','lote','temperatura','kg','fecha']);w.writeheader();w.writerows(valid)
prefix='stage/'+a.run_id+'/'
s3.put_object(Bucket=a.bucket,Key=prefix+'curated.csv',Body=payload.getvalue().encode(),ServerSideEncryption='AES256')
s3.put_object(Bucket=a.bucket,Key=prefix+'rechazados.json',Body=json.dumps(bad).encode(),ServerSideEncryption='AES256')
control={'entrada':len(valid)+len(bad),'validos':len(valid),'rechazados':len(bad),'kg_total':sum(r['kg'] for r in valid)}
s3.put_object(Bucket=a.bucket,Key=prefix+'control.json',Body=json.dumps(control).encode(),ServerSideEncryption='AES256')
print(json.dumps(control))
# Falla como señal de calidad tras guardar cuarentena; el alumno debe interpretar el motivo.
if bad:raise ValueError('Registros rechazados: revisar cuarentena antes de publicar curated')
