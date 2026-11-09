import pcbnew as p,json
from pathlib import Path
r=Path('outputs/rover/Omni_UGV_Rev_E_power_layout');pr=(r/'omni_ugv.kicad_pro').read_bytes();b=p.LoadBoard(str(r/'omni_ugv.kicad_pcb'));dm={d['ref']:d for d in json.loads((r/'design_connections.json').read_text())};nets={n.GetNetname():n for n in b.GetNetInfo().NetsByNetcode().values()}
n=p.NETINFO_ITEM(b,'PROTECTED_RAW');b.Add(n);nets['PROTECTED_RAW']=n
for f in b.GetFootprints():
 if f.GetReference() in ['Q7','Q8','Q13','R40','R41','R39']:
  for pad in f.Pads():
   name=dm[f.GetReference()]['nets'].get(pad.GetNumber())
   if name:pad.SetNet(nets[name])
p.SaveBoard(str(r/'omni_ugv.kicad_pcb'),b);(r/'omni_ugv.kicad_pro').write_bytes(pr)
