import pcbnew as p,json
from pathlib import Path
r=Path('outputs/rover/Omni_UGV_Rev_E_power_layout');fn=r/'omni_ugv.kicad_pcb';pr=(r/'omni_ugv.kicad_pro').read_bytes();b=p.LoadBoard(str(fn));bad=set(json.loads(Path('work/rev-e/step2-width-rejected.json').read_text()));ds={d['uuid']:d for d in json.loads(Path('work/rev-e/step2-width-changes.json').read_text())}
for t in b.GetTracks():
 if t.m_Uuid.AsString() in bad:t.SetWidth(p.FromMM(ds[t.m_Uuid.AsString()]['old']))
p.SaveBoard(str(fn),b);(r/'omni_ugv.kicad_pro').write_bytes(pr)
