import os,json,subprocess,re
from pathlib import Path
root=Path('outputs/rover/Omni_UGV_Rev_A'); board=root/'omni_ugv.kicad_pcb'
os.environ['KICAD_DOCUMENTS_HOME']=str(Path('work/kicad-documents').resolve())
os.environ['KICAD_CONFIG_HOME']=str(Path('work/kicad-config').resolve())
cli=r'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe'
removed=[]
for i in range(60):
 report=root/'validation/current/drc.json'
 subprocess.run([cli,'pcb','drc','--schematic-parity','--severity-all','--format','json','-o',str(report),str(board)],capture_output=True,check=True)
 d=json.loads(report.read_text())
 assert not d['unconnected_items'] and not d['schematic_parity']
 ids=[it['uuid'] for v in d['violations'] if v['type']=='track_dangling' for it in v['items']]
 if not ids: break
 s=board.read_text()
 edits=[]; depth=0; quoted=False; escape=False; start=0
 for j,c in enumerate(s):
  if quoted:
   if escape:escape=False
   elif c=='\\':escape=True
   elif c=='"':quoted=False
  elif c=='"':quoted=True
  elif c=='(':
   if depth==1:start=j
   depth+=1
  elif c==')':
   if depth==2:
    t=s[start:j+1]
    if t.startswith('(segment') and any(uid in t for uid in ids):edits.append((start,j+1))
   depth-=1
 assert len(edits)==len(ids)
 for a,z in reversed(edits):s=s[:a]+s[z:]
 removed+=ids; board.write_text(s)
else: raise RuntimeError('cleanup iteration guard')
(root/'engineering/removed_dangling_tracks.json').write_text(json.dumps(removed,indent=2))
print('Removed',len(removed),'additional dangling segments; current',[(v['severity'],v['type']) for v in d['violations']])
