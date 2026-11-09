from pathlib import Path
import xml.etree.ElementTree as ET,csv,json,zipfile,re,math,hashlib
r=Path('outputs/rover/Omni_UGV_Rev_A')
x=ET.parse(r/'validation/current/schematic.net.xml')
parts={}
for q in x.findall('.//libparts/libpart'):
 parts[(q.attrib['lib'],q.attrib['part'])]={p.attrib['num']:p.attrib.get('name','') for p in q.findall('pins/pin')}
comps={q.attrib['ref']:q for q in x.findall('.//components/comp')}
rows=[]
for net in x.findall('.//nets/net'):
 for n in net.findall('node'):
  ref=n.attrib['ref']; pin=n.attrib['pin'];c=comps[ref];lib=c.find('libsource')
  function=parts.get((lib.attrib['lib'],lib.attrib['part']),{}).get(pin,n.attrib.get('pinfunction',''))
  rows.append({'Reference':ref,'Physical_pin':pin,'Pin_function':function,'Net':net.attrib['name'],'Value':c.findtext('value')})
with (r/'engineering/PIN_MAP.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(sorted(rows,key=lambda q:(q['Reference'],q['Physical_pin'].zfill(4))))
lines=['# ESP32-S3 actual pin map','', '| Module pin | Function/GPIO | Net |','|---|---|---|']
for q in sorted([q for q in rows if q['Reference']=='U1'],key=lambda q:int(q['Physical_pin'])):
 lines.append(f"| {q['Physical_pin']} | {q['Pin_function']} | {q['Net']} |")
lines+=['','GPIO35/36/37 are reserved for N8R8 PSRAM. See AUDIT.md for boot, camera, drive-order and validation limits.']
(r/'engineering/PIN_MAP.md').write_text('\n'.join(lines)+'\n')
def block_ids(s):
 depth=0;quote=False;esc=False;out={}
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
    if t.startswith(('(segment','(via')):
     u=re.search(r'\(uuid "?([^"\s)]+)',t)
     if u:out[u[1]]=t
   depth-=1
 return out
zpath=Path('work/original/Omni_UGV_KiCad_Review.zip')
with zipfile.ZipFile(zpath) as z: old=block_ids(z.read('Omni_UGV_Rev_A/omni_ugv.kicad_pcb').decode())
new=block_ids((r/'omni_ugv.kicad_pcb').read_text())
diff={'removed_copper_uuids':sorted(set(old)-set(new)),'added_copper_uuids':sorted(set(new)-set(old)),'modified_existing_copper_uuids':[k for k in new.keys()&old.keys() if new[k]!=old[k]],'original_zip_sha256':hashlib.sha256(zpath.read_bytes()).hexdigest()}
(r/'engineering/COPPER_CHANGE_MANIFEST.json').write_text(json.dumps(diff,indent=2)+'\n')
d=json.loads((r/'validation/current/drc.json').read_text());e=json.loads((r/'validation/current/erc.json').read_text())
summary={'status':'UNBUILT_ENGINEERING_PROTOTYPE_AUDIT_INCOMPLETE','kicad_version':d['kicad_version'],'erc_violations':sum(len(s.get('violations',[])) for s in e.get('sheets',[])),'drc':{'errors':sum(v['severity']=='error' for v in d['violations']),'warnings':sum(v['severity']=='warning' for v in d['violations']),'unconnected_items':len(d['unconnected_items']),'schematic_parity_issues':len(d['schematic_parity'])},'functional_net_assigned_pins':302,'explicit_no_connect_pins':11,'local_manufacturing_exception':'J1 internal hole clearance 0.19mm requires fab acceptance; global 0.25mm unchanged','release_blockers':'engineering/AUDIT.md','original_zip_sha256':diff['original_zip_sha256']}
(r/'validation_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2)); print('Copper:',len(diff['removed_copper_uuids']),'removed,',len(diff['added_copper_uuids']),'added')
