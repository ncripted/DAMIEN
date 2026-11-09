import pcbnew as p,json,sys,re,math
from pathlib import Path
sys.path.insert(0,'work/humanize');from build import blocks
r=Path('outputs/rover/Omni_UGV_Rev_D_power_audit');fn=r/'omni_ugv.kicad_pcb';pro=(r/'omni_ugv.kicad_pro').read_bytes()
data=json.loads((r/'design_connections.json').read_text());dm={d['ref']:d for d in data};new=json.loads(Path('work/power-rev-d/new_parts.json').read_text())
g=json.loads(Path('work/power-rev-d/geometry.json').read_text());ce=next(d for d in g['pads'] if d['ref']=='U5' and d['num']=='4');x,y=ce['at'];w,h=ce['size'];removed=[]
for t in g['tracks']:
 hit=t['net'] in ['SYS_ON','BAT_NTC']
 if t['net']=='GND' and any(abs(pt[0]-x)<w/2+.03 and abs(pt[1]-y)<h/2+.03 for pt in [t['a'],t['z']]):hit=True
 if hit:removed.append(dict(uuid=t['uuid'],net=t['net']))
ids={d['uuid'] for d in removed};s=fn.read_text()
for a,z,t in reversed(list(blocks(s))):
 if t.startswith(('(segment','(via')) and any(i in t for i in ids):s=s[:a]+s[z:]
tmp=Path('work/power-rev-d/stripped.kicad_pcb');tmp.write_text(s);b=p.LoadBoard(str(tmp));nets={n.GetNetname():n for n in b.GetNetInfo().NetsByNetcode().values()}
for name in {v for d in data for v in d['nets'].values() if v}:
 if name not in nets:n=p.NETINFO_ITEM(b,name);b.Add(n);nets[name]=n
fps={f.GetReference():f for f in b.GetFootprints()}
for ref in ['SW3','J4','U5','Q1','Q2','R24']:
 d=dm[ref];f=fps[ref];f.SetValue(d['value'])
 for pad in f.Pads():
  name=d['nets'].get(pad.GetNumber())
  if name:pad.SetNet(nets[name])
tid=re.search(r'\(uuid "?([0-9a-f-]+)',(r/'omni_ugv.kicad_sch').read_text())[1]
def xy(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
for d in new:
 f=p.FootprintLoad(str((r/'UGV.pretty').resolve()),d['localfp'].split(':')[1]);assert f
 f.SetReference(d['ref']);f.SetValue(d['value']);f.SetFPID(p.LIB_ID('UGV',d['localfp'].split(':')[1]));f.SetPosition(xy(d['x'],d['y']));f.SetPath(p.KIID_PATH('/'+tid+'/'+d['sheet_uuid']+'/'+d['uuid']))
 for pad in f.Pads():
  name=d['nets'].get(pad.GetNumber())
  if name:pad.SetNet(nets[name])
  elif pad.GetNumber() in d['nets']:
   name='unconnected-('+d['ref']+'-NC-Pad'+pad.GetNumber()+')'
   if name not in nets:n=p.NETINFO_ITEM(b,name);b.Add(n);nets[name]=n
   pad.SetNet(nets[name])
 b.Add(f);f.Reference().SetTextSize(xy(.7,.7));f.Value().SetVisible(False)
for t in b.GetDrawings():
 if hasattr(t,'GetText') and 'REV C' in t.GetText():t.SetText(t.GetText().replace('REV C','REV D'))
p.SaveBoard(str(fn),b);(r/'omni_ugv.kicad_pro').write_bytes(pro)
Path('work/power-rev-d/removed-before-routing.json').write_text(json.dumps(removed,indent=2));print('Added',len(new),'footprints; removed',len(removed),'old-route objects')
