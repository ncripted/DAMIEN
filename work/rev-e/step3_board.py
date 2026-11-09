import pcbnew as p,json,re
from pathlib import Path
r=Path('outputs/rover/Omni_UGV_Rev_E_power_layout');fn=r/'omni_ugv.kicad_pcb';pro=(r/'omni_ugv.kicad_pro').read_bytes();b=p.LoadBoard(str(fn));nets={n.GetNetname():n for n in b.GetNetInfo().NetsByNetcode().values()};dm={d['ref']:d for d in json.loads((r/'design_connections.json').read_text())};fps={f.GetReference():f for f in b.GetFootprints()}
for name in ['PROT_CS_SENSE','PROT_VSS_SENSE']:
 if name not in nets:n=p.NETINFO_ITEM(b,name);b.Add(n);nets[name]=n
for ref in ['U7','C24']:
 f=fps[ref]
 if ref=='C24':f.SetPosition(p.VECTOR2I(p.FromMM(dm[ref]['x']),p.FromMM(dm[ref]['y'])))
 for pad in f.Pads():
  name=dm[ref]['nets'].get(pad.GetNumber())
  if name:pad.SetNet(nets[name])
d=dm['R36'];f=p.FootprintLoad(str((r/'UGV.pretty').resolve()),'WSK2512_T1p19_Kelvin');f.SetReference('R36');f.SetValue(d['value']);f.SetFPID(p.LIB_ID('UGV','WSK2512_T1p19_Kelvin'));f.SetPosition(p.VECTOR2I(p.FromMM(d['x']),p.FromMM(d['y'])));b.Add(f);f.Flip(f.GetPosition(),False);f.SetOrientationDegrees(0)
tid=re.search(r'\(uuid "?([0-9a-f-]+)',(r/'omni_ugv.kicad_sch').read_text())[1];sid=re.search(r'\(uuid "?([0-9a-f-]+)',(r/'battery_protection.kicad_sch').read_text())[1];f.SetPath(p.KIID_PATH('/'+tid+'/'+sid+'/'+d['uuid']))
for pad in f.Pads():pad.SetNet(nets[d['nets'][pad.GetNumber()]])
f.Reference().SetTextSize(p.VECTOR2I(p.FromMM(.8),p.FromMM(.8)));f.Value().SetVisible(False)
p.SaveBoard(str(fn),b);(r/'omni_ugv.kicad_pro').write_bytes(pro);print('Placed 4-terminal shunt on B.Cu; CS/VSS pickups isolated from load nets')
