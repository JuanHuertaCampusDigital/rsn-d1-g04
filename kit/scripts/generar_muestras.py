from pathlib import Path
import csv,json,hashlib
from datetime import datetime,timedelta,timezone
root=Path('data');root.mkdir(exist_ok=True)
fields=['event_id','ts','planta','lote','temperatura','kg']
start=datetime(2026,10,1,tzinfo=timezone.utc)
rows=[]
for i in range(120):
    rows.append(dict(event_id=f'EV{i:04}',ts=(start+timedelta(minutes=i*30)).isoformat(),planta='P01' if i%2==0 else 'P02',lote=f'L{i%12:03}',temperatura=f'{20+(i%15)*0.5:.1f}',kg=str(100+i%20)))
def save(name,values):
    with (root/name).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(values)
save('telemetria.csv',rows)
bad=[dict(rows[0],event_id='BAD1',ts='fecha-invalida'),dict(rows[1],event_id='BAD2',kg='-1')]
save('telemetria_con_errores.csv',rows+bad)
(root/'calidad.txt').write_text('SAICA FICTICIA · lote L001 · NO VÁLIDO\n',encoding='utf-8')
(root/'estado.txt').write_text('SAICA FICTICIA · muestra pública sin datos personales\n',encoding='utf-8')
print(json.dumps({'validos':120,'con_errores':122,'sha256':hashlib.sha256((root/'telemetria.csv').read_bytes()).hexdigest()}))
