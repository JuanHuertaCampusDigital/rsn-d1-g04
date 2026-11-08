import argparse,hashlib,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('directorio');p.add_argument('--output',required=True);a=p.parse_args()
root=Path(a.directorio).resolve();out=Path(a.output).resolve()
if not root.is_dir():p.error('El origen debe ser un directorio existente')
rows=[]
for f in sorted(root.rglob('*')):
    if f.is_symlink():raise SystemExit('No se admiten enlaces simbólicos: '+str(f))
    if f.is_file() and f.resolve()!=out:
        h=hashlib.sha256()
        with f.open('rb') as stream:
            for b in iter(lambda:stream.read(1024*1024),b''):h.update(b)
        rows.append({'path':f.relative_to(root).as_posix(),'bytes':f.stat().st_size,'sha256':h.hexdigest()})
out.write_text(json.dumps(rows,indent=2),encoding='utf-8');print(len(rows),'ficheros registrados')
