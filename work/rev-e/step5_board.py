import pcbnew as p,json,re
from pathlib import Path
r=Path('outputs/rover/Omni_UGV_Rev_E_power_layout');pr=(r/'omni_ugv.kicad_pro').read_bytes();b=p.LoadBoard(str(r/'omni_ugv.kicad_pcb'));dm={d['ref']:d for d in json.loads((r/'design_connections.json').read_text())};new=json.loads(Path('work/rev-e/cutoff-new-parts.json').read_text());nets={n.GetNetname():n for n in b.GetNetInfo().NetsByNetcode().values()}
for name in {v for d in dm.values() for v in d['nets'].values() if v}:
 if name not in nets:n=p.NETINFO_ITEM(b,name);b.Add(n);nets[name]=n
fps={f.GetReference():f for f in b.GetFootprints()}
for ref in ['Q7','R40','R46']:
 for pad in fps[ref].Pads():
  if pad.GetNumber() in dm[ref]['nets']:pad.SetNet(nets[dm[ref]['nets'][pad.GetNumber()]])
tid=re.search(r'\(uuid "?([0-9a-f-]+)',(r/'omni_ugv.kicad_sch').read_text())[1]
for d in new:
 f=p.FootprintLoad(str((r/'UGV.pretty').resolve()),d['localfp'].split(':')[1]);assert f
 f.SetReference(d['ref']);f.SetValue(d['value']);f.SetFPID(p.LIB_ID('UGV',d['localfp'].split(':')[1]));f.SetPosition(p.VECTOR2I(p.FromMM(d['x']),p.FromMM(d['y'])));f.SetPath(p.KIID_PATH('/'+tid+'/'+d['sheet_uuid']+'/'+d['uuid']));b.Add(f);f.Flip(f.GetPosition(),False)
 for pad in f.Pads():
  name=d['nets'].get(pad.GetNumber())
  if name:pad.SetNet(nets[name])
 f.Reference().SetTextSize(p.VECTOR2I(p.FromMM(.8),p.FromMM(.8)));f.Value().SetVisible(False)
p.SaveBoard(str(r/'omni_ugv.kicad_pcb'),b);(r/'omni_ugv.kicad_pro').write_bytes(pr)

