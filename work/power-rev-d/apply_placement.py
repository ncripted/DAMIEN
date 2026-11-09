import pcbnew as p,json
from pathlib import Path
r=Path('outputs/rover/Omni_UGV_Rev_D_power_audit');fn=r/'omni_ugv.kicad_pcb';pro=(r/'omni_ugv.kicad_pro').read_bytes();b=p.LoadBoard(str(fn));fps={f.GetReference():f for f in b.GetFootprints()};nets={n.GetNetname():n for n in b.GetNetInfo().NetsByNetcode().values()};new=json.loads(Path('work/power-rev-d/new_parts.json').read_text());dm={d['ref']:d for d in json.loads((r/'design_connections.json').read_text())}
for d in new:
 f=fps[d['ref']];f.SetPosition(p.VECTOR2I(p.FromMM(d['x']),p.FromMM(d['y'])));dm[d['ref']].update(x=d['x'],y=d['y'])
 for pad in f.Pads():
  name=d['nets'].get(pad.GetNumber())
  if name:pad.SetNet(nets[name])
for ref,d in dm.items():
 if ref in fps:fps[ref].SetValue(d['value'])
p.SaveBoard(str(fn),b);(r/'omni_ugv.kicad_pro').write_bytes(pro);(r/'design_connections.json').write_text(json.dumps(list(dm.values()),indent=2));print('Applied final component placement and power-control values')
