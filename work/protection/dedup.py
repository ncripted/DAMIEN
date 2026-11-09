from pathlib import Path
import re
p=Path('outputs/rover/Omni_UGV_Rev_B_protection/omni_ugv.kicad_pcb');s=p.read_text()
def blocks(s):
 depth=0;quoted=False;esc=False;start=0
 for i,c in enumerate(s):
  if quoted:
   if esc:esc=False
   elif c=='\\':esc=True
   elif c=='"':quoted=False
  elif c=='"':quoted=True
  elif c=='(':
   if depth==1:start=i
   depth+=1
  elif c==')':
   if depth==2:yield start,i+1,s[start:i+1]
   depth-=1
seen=set();ed=[]
for a,z,t in blocks(s):
 if not t.startswith(('(segment','(via')):continue
 key=re.sub(r'\(uuid[^)]+\)','',t);key=re.sub(r'\s+','',key)
 if key in seen:ed.append((a,z))
 else:seen.add(key)
for a,z in reversed(ed):s=s[:a]+s[z:]
p.write_text(s);print('Removed identical copper duplicates:',len(ed))
