from pathlib import Path
import sys,re,json,os
os.environ['KICAD_DOCUMENTS_HOME']=str(Path('work/kicad-documents').resolve());os.environ['KICAD_CONFIG_HOME']=str(Path('work/kicad-config').resolve())
sys.path.insert(0,'work/humanize');from build import blocks
import pcbnew as p
r=Path('outputs/rover/Omni_UGV_Rev_C_flex_camera');base=r.parent/'Omni_UGV_Rev_B_protection';s=(base/'omni_ugv.kicad_pcb').read_text()
for a,b,t in reversed(list(blocks(s))):
 if (t.startswith('(footprint') and '(property "Reference" "J3"' in t) or (t.startswith(('(segment','(via')) and re.search(r'\(net "CAM_',t)):s=s[:a]+s[b:]
tmp=Path('work/camera-rev-c/stripped.kicad_pcb');tmp.write_text(s);b=p.LoadBoard(str(tmp));new=json.loads(Path('work/camera-rev-c/new_parts.json').read_text());nets={n.GetNetname():n for n in b.GetNetInfo().NetsByNetcode().values()}
for name in set(v for d in new for v in d['nets'].values() if v):
 if name not in nets:n=p.NETINFO_ITEM(b,name);b.Add(n);nets[name]=n
def xy(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
sid=re.search(r'\(uuid "?([0-9a-f-]+)',(r/'camera.kicad_sch').read_text())[1];tid=re.search(r'\(uuid "?([0-9a-f-]+)',(r/'omni_ugv.kicad_sch').read_text())[1]
fps={f.GetReference():f for f in b.GetFootprints()}
fps['J5'].SetPosition(xy(141.25,81.5))
for d in new:
 f=p.FootprintLoad(str((r/'UGV.pretty').resolve()),d['localfp'].split(':')[1]);assert f
 f.SetReference(d['ref']);f.SetValue(d['value']);f.SetFPID(p.LIB_ID('UGV',d['localfp'].split(':')[1]));f.SetPosition(xy(d['x'],d['y']));f.SetPath(p.KIID_PATH('/'+tid+'/'+sid+'/'+d['uuid']))
 for pad in f.Pads():
  name=d['nets'].get(pad.GetNumber())
  if pad.GetNumber()=='MP':name=None
  if name:pad.SetNet(nets[name])
  elif pad.GetNumber() in d['nets']:
   name='unconnected-('+d['ref']+'-'+({'J3':{'1':'STROBE','23':'Y1','24':'Y0'}}.get(d['ref'],{}).get(pad.GetNumber(),'NC'))+'-Pad'+pad.GetNumber()+')'
   n=p.NETINFO_ITEM(b,name);b.Add(n);pad.SetNet(n)
 b.Add(f)
 f.Reference().SetTextSize(xy(.8,.8));f.Value().SetVisible(False)
pro=(r/'omni_ugv.kicad_pro').read_bytes();p.SaveBoard(str(r/'omni_ugv.kicad_pcb'),b);(r/'omni_ugv.kicad_pro').write_bytes(pro)
print('New FPC connector and local camera supplies placed in upper-right sector.')
