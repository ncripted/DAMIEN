from pathlib import Path
import re,uuid,shutil
r=Path('outputs/rover/Omni_UGV_Rev_A');path=r/'omni_ugv.kicad_pcb'
shutil.copy2(path,'work/before-switch-node-repair.kicad_pcb')
s=path.read_text(); depth=0; quote=False;esc=False;edits=[]
for j,c in enumerate(s):
 if quote:
  if esc:esc=False
  elif c=='\\':esc=True
  elif c=='"':quote=False
 elif c=='"':quote=True
 elif c=='(':
  if depth==1:start=j
  depth+=1
 elif c==')':
  if depth==2:
   t=s[start:j+1]
   if t.startswith(('(segment','(via')) and re.search(r'\(net (54|55)\)',t):edits.append((start,j+1))
  depth-=1
for a,z in reversed(edits):s=s[:a]+s[z:]
paths={54:[(96.75,113.5),(98,113.5),(99.1,112.4),(101,112.4)],55:[(96.75,114.5),(98,114.5),(99.1,115.6),(101,115.6)]}
new=''
for n,pts in paths.items():
 for a,b in zip(pts,pts[1:]):
  new+=f'\n(segment (start {a[0]} {a[1]}) (end {b[0]} {b[1]}) (width 0.4) (layer "F.Cu") (net {n}) (uuid "{uuid.uuid4()}"))'
s=s.rstrip(); assert s[-1]==')';path.write_text(s[:-1]+new+'\n)\n')
print('Replaced',len(edits),'switch-node tracks/vias with 6 front-copper segments')
