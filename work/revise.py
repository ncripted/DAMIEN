from pathlib import Path
import re,json,csv,hashlib
root=Path('outputs/rover/Omni_UGV_Rev_A')
def blocks(s):
 depth=0; quoted=False; escape=False; start=0
 for i,c in enumerate(s):
  if quoted:
   if escape: escape=False
   elif c=='\\': escape=True
   elif c=='"': quoted=False
  elif c=='"': quoted=True
  elif c=='(':
   if depth==1: start=i
   depth+=1
  elif c==')':
   if depth==2: yield start,i+1,s[start:i+1]
   depth-=1
changes={'R25':'100k','R27':'1k','R29':'10k'}
for fn in ['interlock.kicad_sch','omni_ugv.kicad_pcb']:
 path=root/fn; s=path.read_text(); edits=[]
 for a,z,t in blocks(s):
  m=re.search(r'\(property "Reference" "([^"]+)"',t)
  if m and m[1] in changes:
   t,n=re.subn(r'(\(property "Value" ")[^"]+',lambda m:m[1]+changes[re.search(r'\(property "Reference" "([^"]+)"',t)[1]],t,count=1)
   assert n==1
   edits.append((a,z,t))
  if fn.endswith('pcb') and any(u in t for u in ['e4c141f2-d872-499b-918f-44825d5a8ea1','9a132c83-01c3-4239-9f43-113742daade0','1de23af2-62cf-46a7-a3cd-94b7a6e42161']):
   assert t.startswith('(segment'); edits.append((a,z,''))
 for a,z,t in reversed(edits): s=s[:a]+t+s[z:]
 path.write_text(s)
 print(fn,len(edits),'edits')
path=root/'design_connections.json'; data=json.loads(path.read_text())
for d in data:
 if d['ref'] in changes: d['value']=changes[d['ref']]
path.write_text(json.dumps(data,indent=2)+'\n')
path=root/'BOM.csv'
with path.open(newline='') as f: rows=list(csv.DictReader(f))
notes={'R25':'100k reduces Q3 base loading of DRIVE_ENABLE; see engineering/AUDIT.md', 'R27':'1k preserves DRV8833 nSLEEP high-level margin; 1% tolerance', 'R29':'10k supplies USB override Q4 base current with R27=1k; 1% tolerance'}
for r in rows:
 if r['Reference'] in changes: r['Value']=changes[r['Reference']]; r['Notes']=notes[r['Reference']]
with path.open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
# Board U1 has ALL silk graphics moved to fab, not just one antenna line.
# Make local library intentional modification agree; do not alter pads or copper.
path=root/'UGV.pretty/RF_Module__ESP32-S3-WROOM-1.kicad_mod'
s=path.read_text(); edits=[]
for a,z,t in blocks(s):
 if t.startswith(('(fp_line','(fp_arc','(fp_rect','(fp_poly','(fp_circle')) and '"F.SilkS"' in t:
  edits.append((a,z,t.replace('"F.SilkS"','"F.Fab"')))
for a,z,t in reversed(edits): s=s[:a]+t+s[z:]
path.write_text(s)
print('library silk graphics moved',len(edits))
