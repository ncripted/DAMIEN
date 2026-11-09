from pathlib import Path
import sys,re,json
sys.path.insert(0,'work/humanize');from build import blocks
r=Path('outputs/rover/Omni_UGV_Rev_D_power_audit');fn=r/'omni_ugv.kicad_pcb';s=fn.read_text();removed=[]
for a,b,t in reversed(list(blocks(s))):
 if t.startswith(('(segment','(via')) and '(net "DRIVE_REQ")' in t:removed.append(re.search(r'\(uuid "?([0-9a-f-]+)',t)[1]);s=s[:a]+s[b:]
fn.write_text(s);Path('work/power-rev-d/drive-request-removed.json').write_text(json.dumps(removed));print('Removed',len(removed),'pre-buffer request copper objects')
