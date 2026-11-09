import pcbnew as p,json,re
from pathlib import Path
r=Path('outputs/rover/Omni_UGV_Rev_D_power_audit');fn=r/'omni_ugv.kicad_pcb';pro=(r/'omni_ugv.kicad_pro').read_bytes();b=p.LoadBoard(str(fn));fps={f.GetReference():f for f in b.GetFootprints()};nets={n.GetNetname():n for n in b.GetNetInfo().NetsByNetcode().values()};ds=json.loads(Path('work/power-rev-d/new_parts.json').read_text())[-3:];tid=re.search(r'\(uuid "?([0-9a-f-]+)',(r/'omni_ugv.kicad_sch').read_text())[1]
for name in ['DRIVE_REQ_RAW']:
 n=p.NETINFO_ITEM(b,name);b.Add(n);nets[name]=n
for d in ds:
 f=p.FootprintLoad(str((r/'UGV.pretty').resolve()),d['localfp'].split(':')[1]);f.SetReference(d['ref']);f.SetValue(d['value']);f.SetFPID(p.LIB_ID('UGV',d['localfp'].split(':')[1]));f.SetPosition(p.VECTOR2I(p.FromMM(d['x']),p.FromMM(d['y'])));f.SetPath(p.KIID_PATH('/'+tid+'/'+d['sheet_uuid']+'/'+d['uuid']))
 for pad in f.Pads():
  n=d['nets'].get(pad.GetNumber())
  if not n:
   n='unconnected-('+d['ref']+'-NC-Pad'+pad.GetNumber()+')';o=p.NETINFO_ITEM(b,n);b.Add(o);nets[n]=o
  pad.SetNet(nets[n])
 b.Add(f);f.Reference().SetTextSize(p.VECTOR2I(p.FromMM(.8),p.FromMM(.8)));f.Value().SetVisible(False)
next(v for v in fps['U1'].Pads() if v.GetNumber()=='35').SetNet(nets['DRIVE_REQ_RAW']);fps['R28'].SetValue('1M')
p.SaveBoard(str(fn),b);(r/'omni_ugv.kicad_pro').write_bytes(pro)
