from pathlib import Path
import json,sys
sys.path.insert(0,'work/humanize');from build import blocks
r=Path('outputs/rover/Omni_UGV_Rev_E_power_layout');g=json.loads(Path('work/rev-e/geometry.json').read_text());bad={t['uuid'] for t in g['tracks'] if t['net'] in ['PROT_VSS_SENSE','PROT_VDD']}
s=(r/'omni_ugv.kicad_pcb').read_text()
for a,b,t in reversed(list(blocks(s))):
 if t.startswith(('(segment','(via')) and any(i in t for i in bad):s=s[:a]+s[b:]
(r/'omni_ugv.kicad_pcb').write_text(s)
Path('work/rev-e/c24-placement.json').write_text('[121,127.5]')
