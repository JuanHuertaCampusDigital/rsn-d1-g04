"""Modelo docente: dos directorios locales/montados, un coordinador, sin borrados.
Primera ejecución aplica solo ficheros exclusivos; los distintos en ambos lados son conflicto.
El estado se guarda FUERA de las raíces. No sustituye un servicio de sincronización industrial.
"""
import argparse,hashlib,json,shutil
from pathlib import Path
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
def sync(left,right,statefile,apply=False):
    left=Path(left).resolve();right=Path(right).resolve();sf=Path(statefile).resolve()
    if left==right or left in right.parents or right in left.parents:raise ValueError('Raíces deben ser distintas y no anidadas')
    if left in sf.parents or right in sf.parents:raise ValueError('Estado fuera de las raíces')
    if not left.is_dir() or not right.is_dir():raise ValueError('Ambas raíces deben existir')
    old=json.loads(sf.read_text()) if sf.exists() else {};new=dict(old);events=[]
    paths=set(old)
    for root in (left,right):
        for f in root.rglob('*'):
            if f.is_symlink():raise ValueError('No se admiten symlinks')
            if f.is_file():paths.add(f.relative_to(root).as_posix())
    for rel in sorted(paths):
        if Path(rel).is_absolute() or '..' in Path(rel).parts:raise ValueError('Ruta de estado no válida')
        a,b=left/rel,right/rel;ha,hb=digest(a),digest(b);prev=old.get(rel)
        if ha==hb:
            if apply:new[rel]=ha
            events.append({'path':rel,'action':'equal'});continue
        direction=None
        if prev is None:
            if ha is None:direction='R→L'
            elif hb is None:direction='L→R'
        elif ha is None or hb is None:
            events.append({'path':rel,'action':'conflict-delete'});continue
        elif ha!=prev and hb==prev:direction='L→R'
        elif hb!=prev and ha==prev:direction='R→L'
        if direction is None:events.append({'path':rel,'action':'conflict'});continue
        src,dst=(a,b) if direction=='L→R' else (b,a)
        if apply:
            dst.parent.mkdir(parents=True,exist_ok=True);tmp=dst.with_name(dst.name+'.saica-tmp')
            if tmp.exists():raise ValueError('Temporal previo: revisar antes de continuar')
            shutil.copy2(src,tmp);tmp.replace(dst)
            if digest(src)!=digest(dst):raise ValueError('Fallo de integridad')
            new[rel]=digest(dst)
        events.append({'path':rel,'action':direction,'applied':apply})
    if apply:
        sf.parent.mkdir(parents=True,exist_ok=True);sf.write_text(json.dumps(new,indent=2))
    return events
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('left');p.add_argument('right');p.add_argument('--state',required=True);p.add_argument('--apply',action='store_true');a=p.parse_args()
    result=sync(a.left,a.right,a.state,a.apply);print(json.dumps(result,ensure_ascii=False,indent=2));raise SystemExit(2 if any(x['action'].startswith('conflict') for x in result) else 0)
