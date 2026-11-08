import argparse,json,boto3
p=argparse.ArgumentParser();p.add_argument('--table',required=True);p.add_argument('--count',type=int,default=120);a=p.parse_args()
if not 1<=a.count<=120:p.error('Limite docente: 120 items')
t=boto3.resource('dynamodb').Table(a.table)
with t.batch_writer(overwrite_by_pkeys=['PK','SK']) as batch:
    for i in range(a.count):
        batch.put_item(Item={'PK':f'LOTE#L{i%12:03}','SK':f'2026-10-01T10:{i//60:02}:{i%60:02}Z#EV{i:04}','planta':'P01' if i%2==0 else 'P02','kg':100+i%20})
print(json.dumps({'tabla':a.table,'items':a.count,'aviso':'claves deterministas; repetir sobrescribe las mismas muestras'}))
