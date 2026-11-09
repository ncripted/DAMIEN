from pathlib import Path
import pcbnew as p,json
r=Path('outputs/rover/Omni_UGV_Rev_E_power_layout');fn=r/'omni_ugv.kicad_pcb';pro=(r/'omni_ugv.kicad_pro').read_bytes();b=p.LoadBoard(str(fn));changes={d['uuid']:d for d in json.loads(Path('work/rev-e/step2-width-changes.json').read_text())}
for t in b.GetTracks():
 if t.m_Uuid.AsString() in changes:t.SetWidth(p.FromMM(changes[t.m_Uuid.AsString()]['new']))
p.SaveBoard(str(fn),b);(r/'omni_ugv.kicad_pro').write_bytes(pro);print('Applied',len(changes),'clearance-limited power width increases')
