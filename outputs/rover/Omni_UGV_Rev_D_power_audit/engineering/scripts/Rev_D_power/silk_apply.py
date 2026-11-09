import pcbnew as p,json
from pathlib import Path
r=Path('outputs/rover/Omni_UGV_Rev_D_power_audit');fn=r/'omni_ugv.kicad_pcb';pro=(r/'omni_ugv.kicad_pro').read_bytes();b=p.LoadBoard(str(fn));fps={f.GetReference():f for f in b.GetFootprints()}
for d in json.loads(Path('work/power-rev-d/silk-positions.json').read_text()):
 v=next(o for o in b.GetDrawings() if hasattr(o,'GetText') and o.GetText()=='N. SANFORD') if d['id']=='signature' else fps[d['id']].Reference()
 if d['id']!='signature':v.SetTextSize(p.VECTOR2I(p.FromMM(.8),p.FromMM(.8)))
 v.SetPosition(p.VECTOR2I(p.FromMM(d['at'][0]),p.FromMM(d['at'][1])))
p.SaveBoard(str(fn),b);(r/'omni_ugv.kicad_pro').write_bytes(pro)
