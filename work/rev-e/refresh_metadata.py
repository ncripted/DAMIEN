import pcbnew as p,json
from pathlib import Path
r=Path('outputs/rover/Omni_UGV_Rev_E_power_layout');b=p.LoadBoard(str(r/'omni_ugv.kicad_pcb'));data=json.loads((r/'design_connections.json').read_text());dm={d['ref']:d for d in data}
for f in b.GetFootprints():
 if f.GetReference() in dm:dm[f.GetReference()].update(x=p.ToMM(f.GetPosition().x),y=p.ToMM(f.GetPosition().y),a=f.GetOrientationDegrees(),side='B' if f.GetLayer()==p.B_Cu else 'F')
(r/'design_connections.json').write_text(json.dumps(data,indent=2));print('Refreshed placement metadata from native board')
print('Copper layers',b.GetCopperLayerCount(),'zones',[(z.GetNetname(),z.GetIsRuleArea(),[b.GetLayerName(l) for l in z.GetLayerSet().CuStack()]) for z in b.Zones()])
