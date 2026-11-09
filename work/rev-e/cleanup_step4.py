from pathlib import Path
import sys,json,subprocess
sys.path.insert(0,'work/humanize');from build import blocks
p=Path('outputs/rover/Omni_UGV_Rev_E_power_layout/omni_ugv.kicad_pcb');rep=Path('work/rev-e/step4-after-en.json');removed=[]
for k in range(20):
 d=json.loads(rep.read_text());ids={v['items'][0]['uuid'] for v in d['violations'] if v['type']=='track_dangling'}
 if not ids:break
 s=p.read_text()
 for a,b,t in reversed(list(blocks(s))):
  if t.startswith('(segment') and any(i in t for i in ids):s=s[:a]+s[b:]
 p.write_text(s);removed.extend(ids)
 subprocess.run(['C:/Program Files/KiCad/10.0/bin/kicad-cli.exe','pcb','drc','--schematic-parity','--severity-all','--refill-zones','--format','json','-o',str(rep),str(p)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
print('Removed dangling tails',len(removed),'remaining',len(d['violations']),'opens',len(d['unconnected_items']))
Path('work/rev-e/step4-tail-cleanup.json').write_text(json.dumps(removed))

