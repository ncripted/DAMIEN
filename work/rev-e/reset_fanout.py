from pathlib import Path
import json,sys
sys.path.insert(0,'work/humanize');from build import blocks
r=Path('outputs/rover/Omni_UGV_Rev_E_power_layout');g=json.loads(Path('work/rev-e/geometry.json').read_text());bad={t['uuid'] for t in g['tracks'] if t['net'] in ['PROT_VSS_SENSE','PROT_CS_SENSE','PROT_VDD','PROT_DSG','PROT_CHG','PROT_PACK','PROT_BAT']};bad.update(['c8341aad-788f-4dfa-bd29-53775218818c','056de480-902d-4c1e-89eb-c20e2481c7e6','c2e3eb70-cfe3-495b-be06-c69505ed3fb7'])
s=(r/'omni_ugv.kicad_pcb').read_text()
for a,b,t in reversed(list(blocks(s))):
 if t.startswith(('(segment','(via')) and any(i in t for i in bad):s=s[:a]+s[b:]
(r/'omni_ugv.kicad_pcb').write_text(s)
