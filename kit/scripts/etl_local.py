import csv,json,argparse
from pathlib import Path
from datetime import datetime
from decimal import Decimal,InvalidOperation
def transform(source,dest):
    dest=Path(dest);dest.mkdir(parents=True,exist_ok=True)
    valid=[];reject=[];seen=set()
    with open(source,newline='',encoding='utf-8') as f:
        for n,row in enumerate(csv.DictReader(f),2):
            try:
                stamp=datetime.fromisoformat(row['ts'])
                if stamp.tzinfo is None:raise ValueError('timestamp sin zona')
                kg=Decimal(row['kg']);temp=Decimal(row['temperatura'])
                if not kg.is_finite() or not temp.is_finite() or kg<0:raise ValueError('valor no válido')
                if row['event_id'] in seen:raise ValueError('event_id duplicado')
                if not row['planta'] or not row['lote']:raise ValueError('clave vacía')
                seen.add(row['event_id'])
                valid.append(dict(event_id=row['event_id'],ts=stamp.isoformat(),planta=row['planta'],lote=row['lote'],temperatura=float(temp),kg=float(kg),fecha=stamp.date().isoformat()))
            except (ValueError,KeyError,InvalidOperation) as ex:reject.append(dict(line=n,error=str(ex),record=row))
    # Archivos deterministas y separados: repetir no añade filas al resultado.
    with (dest/'curated.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['event_id','ts','planta','lote','temperatura','kg','fecha']);w.writeheader();w.writerows(valid)
    (dest/'rechazados.json').write_text(json.dumps(reject,ensure_ascii=False,indent=2),encoding='utf-8')
    totals={}
    for row in valid:
        key=(row['fecha'],row['planta']);totals[key]=totals.get(key,Decimal('0'))+Decimal(str(row['kg']))
    report={'entrada':len(valid)+len(reject),'validos':len(valid),'rechazados':len(reject),'kg_total':float(sum(totals.values(),Decimal('0'))),'grupos':[{'fecha':k[0],'planta':k[1],'kg':float(v)} for k,v in sorted(totals.items())]}
    (dest/'control.json').write_text(json.dumps(report,indent=2),encoding='utf-8');return report
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('dest');a=p.parse_args();print(json.dumps(transform(a.source,a.dest)))
