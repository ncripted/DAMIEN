import os,json,subprocess,re
from pathlib import Path
root=Path('outputs/rover/Omni_UGV_Rev_B_protection');board=root/'omni_ugv.kicad_pcb'
os.environ['KICAD_DOCUMENTS_HOME']=str(Path('work/kicad-documents').resolve());os.environ['KICAD_CONFIG_HOME']=str(Path('work/kicad-config').resolve())
cli=r'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe'
src=Path('work/protection/dedup.py').read_text();exec(src[src.index('def blocks'):src.index('seen=set()')])
removed=[]
for i in range(100):
 report=Path('work/protection/drc-cleanup.json')
 subprocess.run([cli,'pcb','drc','--schematic-parity','--refill-zones','--format','json','-o',str(report),str(board)],capture_output=True,check=True)
 d=json.loads(report.read_text());assert not d['unconnected_items'] and not d['schematic_parity'],d
 ids=[it['uuid'] for v in d['violations'] if v['type'] in ['track_dangling','via_dangling'] for it in v['items']]
 if not ids:break
 s=board.read_text();ed=[]
 for a,z,t in blocks(s):
  if t.startswith(('(segment','(via')) and any(u in t for u in ids):ed.append((a,z))
 assert len(ed)==len(ids)
 for a,z in reversed(ed):s=s[:a]+s[z:]
 board.write_text(s);removed+=ids
else:raise RuntimeError('Cleanup iteration limit')
Path('work/protection/cleanup_removed.json').write_text(json.dumps(removed,indent=2))
print('Removed',len(removed),'dangling copper objects in',i,'passes; final opens',len(d['unconnected_items']))
