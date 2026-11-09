from pathlib import Path
import pcbnew as p,json,shutil,re,sys,os
os.environ['KICAD_DOCUMENTS_HOME']=str(Path('work/kicad-documents').resolve())
os.environ['KICAD_CONFIG_HOME']=str(Path('work/kicad-config').resolve())
root=Path('outputs/rover/Omni_UGV_Rev_B_protection');base=Path('outputs/rover/Omni_UGV_Rev_A');std=Path('C:/Program Files/KiCad/10.0/share/kicad/footprints')
sys.path.insert(0,str(Path('work/protection').resolve()))
# Read definitions without re-running schematic construction.
data=json.loads((root/'design_connections.json').read_text());new=json.loads(Path('work/protection/new_parts.json').read_text())
def mm(v):return p.FromMM(v)
def xy(x,y):return p.VECTOR2I(mm(x),mm(y))
def footprint(name,pads,body,court,desc):
 s=f'(footprint "{name}" (version 20260206) (generator "pcbnew") (layer "F.Cu") (descr "{desc}") (attr smd) (property "Reference" "REF**" (at 0 {-court-0.8} 0) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12)))) (property "Value" "{name}" (at 0 {court+0.8} 0) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))'
 s+=f'(fp_rect (start {-body/2} {-body/2}) (end {body/2} {body/2}) (stroke (width 0.1) (type default)) (layer "F.Fab")) (fp_rect (start {-court} {-court}) (end {court} {court}) (stroke (width 0.05) (type default)) (layer "F.CrtYd"))'
 for num,x,y,w,h,paste in pads:
  s+=f'(pad "{num}" smd roundrect (at {x} {y}) (size {w} {h}) (layers "F.Cu" "F.Mask"'+(' "F.Paste"' if paste else '')+') (roundrect_rratio 0.1))'
 s+='(fp_circle (center -1.95 -1.5) (end -1.85 -1.5) (stroke (width 0.1) (type default)) (fill none) (layer "F.Fab")))'
 (root/'UGV.pretty'/f'{name}.kicad_mod').write_text(s)
pad=[]
for n,y in [(1,-.5),(2,0),(3,.5)]:pad.append((n,-.675,y,.55,.2 if n==2 else .25,True))
for n,y in [(7,-.5),(6,0),(5,.5)]:pad.append((n,.675,y,.55,.2 if n==6 else .25,True))
pad += [(8,0,-.65,.3,.6,True),(4,0,.65,.3,.6,True)]
footprint('BQ298217_RUG0008A',pad,1.5,1.2,'TI RUG0008A 4222060/A land pattern; verified against ADS7041 package appendix; BQ298217 pinout')
pad=[]
for n,y in [(1,-.975),(2,-.325),(3,.325),(4,.975)]:pad.append((n,-1.435,y,.63,.5,True))
for n,y in [(8,-.975),(7,-.325),(6,.325),(5,.975)]:pad.append((n,1.435,y,.63,.5,True))
pad.append((9,.39,0,1.9,2.45,False))
# EP paste split into two apertures, each kept inside the drain land.
footprint('CSD17308Q3_TI',pad,3.3,2.05,'TI CSD17308Q3 SLPS262C page10; recommended 3.50x2.45mm land; S1-3 G4 D5-9')
fpfile=root/'UGV.pretty/CSD17308Q3_TI.kicad_mod';s=fpfile.read_text().rstrip()[:-1]
for y in [-.6125,.6125]:s+=f'(pad "" smd rect (at .39 {y}) (size 1.55 .975) (layers "F.Paste")))'[:-1]
fpfile.write_text(s+')')
shutil.copyfile(std/'Resistor_SMD.pretty/R_2512_6332Metric.kicad_mod',root/'UGV.pretty/Resistor_SMD__R_2512_6332Metric.kicad_mod')
f=root/'UGV.pretty/Resistor_SMD__R_2512_6332Metric.kicad_mod';f.write_text(f.read_text().replace('(footprint "R_2512_6332Metric"','(footprint "Resistor_SMD__R_2512_6332Metric"',1))
removed=[]
removed.append('5ad18859-faf6-4769-b5e5-25f0c1c2abf7') # old VBAT branch overlaps raw J2 pad after net split
def blocks(s):
 depth=0;quote=False;escape=False;start=0
 for i,c in enumerate(s):
  if quote:
   if escape:escape=False
   elif c=='\\':escape=True
   elif c=='"':quote=False
  elif c=='"':quote=True
  elif c=='(':
   if depth==1:start=i
   depth+=1
  elif c==')':
   if depth==2:yield start,i+1,s[start:i+1]
   depth-=1
s=(base/'omni_ugv.kicad_pcb').read_text()
oldpts=[tuple(v['at']) for v in json.loads((base/'engineering/board_inventory.json').read_text())['footprints']['J2']['pads'] if v['number']]
netnames={m[0]:m[1] for m in re.findall(r'\(net\s+(\d+)\s+"([^"]*)"\)',s)}
for a,z,t in blocks(s):
 if not t.startswith(('(segment','(via')):continue
 nm=re.search(r'\(net\s+(\d+)\)',t);name=netnames.get(nm[1],'') if nm else ''
 named=re.search(r'\(net\s+"([^"]+)"\)',t)
 if named:name=named[1]
 points=[tuple(map(float,m)) for m in re.findall(r'\((?:start|end|at)\s+([-\d.]+)\s+([-\d.]+)\)',t)]
 if name in ['LED_STATUS','UART_TX'] or (name in ['VBAT','GND'] and any(pt in oldpts for pt in points)):
  removed.append(re.search(r'\(uuid\s+"?([\w-]+)',t)[1])
for a,z,t in reversed(list(blocks(s))):
 if t.startswith(('(segment','(via')) and any(u in t for u in removed):s=s[:a]+s[z:]
tmp=Path('work/protection/disconnected.kicad_pcb');tmp.write_text(s)
print('Loading board',flush=True)
b=p.LoadBoard(str(tmp));fps={f.GetReference():f for f in b.GetFootprints()}
nets={n.GetNetname():n for n in b.GetNetInfo().NetsByNetcode().values()}
for name in set(v for d in data for v in d['nets'].values() if v):
 if name not in nets:
  ni=p.NETINFO_ITEM(b,name);b.Add(ni);nets[name]=ni
for d in data:
 if d['ref'] in fps:
  f=fps[d['ref']];f.SetValue(d['value'])
  for pad in f.Pads():
   n=d['nets'].get(pad.GetNumber())
   if n:pad.SetNet(nets[n])
sid=re.search(r'\(uuid ([^)]+)',(root/'battery_protection.kicad_sch').read_text())[1]
topid=re.search(r'\(uuid ([^)]+)',(root/'omni_ugv.kicad_sch').read_text())[1]
for d in new:
 print('Adding',d['ref'],flush=True)
 f=p.FootprintLoad(str((root/'UGV.pretty').resolve()),d['localfp'].split(':')[1]);assert f,d['ref']
 print('loaded',flush=True)
 f.SetReference(d['ref']);f.SetValue(d['value']);f.SetFPID(p.LIB_ID('UGV',d['localfp'].split(':')[1]));f.SetPosition(xy(d['x'],d['y']));f.SetOrientationDegrees(d['a'])
 print('positioned',flush=True)
 f.SetPath(p.KIID_PATH('/'+topid+'/'+sid+'/'+d['uuid']))
 print('path',flush=True)
 b.Add(f);fps[d['ref']]=f
 if d['side']=='B':f.Flip(f.GetPosition(),False)
 f.Reference().SetTextSize(xy(.8,.8));f.Reference().SetTextThickness(mm(.12));f.Value().SetVisible(False)
 for pad in f.Pads():
  n=d['nets'].get(pad.GetNumber())
  if n:pad.SetNet(nets[n])
p.SaveBoard(str(root/'omni_ugv.kicad_pcb'),b)
shutil.copyfile(base/'omni_ugv.kicad_pro',root/'omni_ugv.kicad_pro')
Path('work/protection/board_changes.json').write_text(json.dumps({'removed_initial_tracks':removed},indent=2))
print('Added',len(new),'footprints; removed',len(removed),'old connector/GPIO track segments')
print({r:[(pad.GetNumber(),tuple(round(p.ToMM(v),4) for v in [pad.GetPosition().x,pad.GetPosition().y]),pad.GetNetname()) for pad in fps[r].Pads() if pad.GetNumber()] for r in ['J2','U7','Q7','Q8','R36','J5']})
