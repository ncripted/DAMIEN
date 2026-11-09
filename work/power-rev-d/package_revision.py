from pathlib import Path
import shutil,json,re,sys,csv,hashlib,zipfile,math,xml.etree.ElementTree as E
import pymupdf
sys.path.insert(0,'work/humanize');from build import blocks
r=Path('outputs/rover/Omni_UGV_Rev_D_power_audit');base=r.parent/'Omni_UGV_Rev_C_flex_camera';eng=r/'engineering';val=r/'validation/current'
# Refresh derivative metadata after the final resistor loading correction; do not rewrite native CAD.
x=E.parse(val/'schematic.net.xml').getroot();values={c.get('ref'):c.findtext('value') for c in x.findall('./components/comp')};rows=[]
for net in x.findall('./nets/net'):
 for n in net.findall('node'):rows.append(dict(Reference=n.get('ref'),Physical_pin=n.get('pin'),Pin_function=n.get('pinfunction',''),Net=net.get('name'),Value=values.get(n.get('ref'),'')))
with (eng/'PIN_MAP.csv').open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(sorted(rows,key=lambda d:(d['Reference'],d['Physical_pin'].zfill(4))))
with (eng/'COMPONENT_FUNCTIONS.csv').open(newline='',encoding='utf-8-sig') as f:roles=list(csv.DictReader(f))
for d in roles:d['Value']=values.get(d['Reference'],d['Value'])
for ref in ['TH1','TH2']:
 if ref not in {d['Reference'] for d in roles}:roles.append(dict(Reference=ref,Value=values.get(ref,'103AT-2'),Functional_block='Off-board cell probes',Role='Insulated probe bonded to actual cell; independent two-wire connection',Nets='; '.join(z['Net'] for z in rows if z['Reference']==ref)))
with (eng/'COMPONENT_FUNCTIONS.csv').open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=roles[0]);w.writeheader();w.writerows(roles)
g=json.loads(Path('work/power-rev-d/geometry.json').read_text());(eng/'board_inventory.json').write_text(json.dumps(g))
# Verify antenna rule area and existing mechanical/component pad geometry, separately from DRC.
def fps(s):return {re.search(r'\(property "Reference" "([^"]+)',t)[1]:t for a,b,t in blocks(s) if t.startswith('(footprint')}
fa,fb=[fps((p/'omni_ugv.kicad_pcb').read_text()) for p in [base,r]]
def sel(s,start):return sorted(re.sub(r'\s+','',t) for a,b,t in blocks(s) if t.startswith(start))
assert sel(fa['U1'],'(zone')==sel(fb['U1'],'(zone')
changes=[]
for ref in fa:
 pa,pb=sel(fa[ref],'(pad'),sel(fb[ref],'(pad')
 if pa!=pb:changes.append(ref)
assert set(changes)=={'U1','U5','J4','SW3'},changes
def copper(s):return {re.search(r'\(uuid "?([0-9a-f-]+)',t)[1]:t for a,b,t in blocks(s) if t.startswith(('(segment','(via'))}
c0,c1=[copper((p/'omni_ugv.kicad_pcb').read_text()) for p in [base,r]]
assert not [k for k in c0.keys()&c1.keys() if re.sub(r'\s+','',c0[k])!=re.sub(r'\s+','',c1[k])]
proof=json.loads((val/'power-board-proof.json').read_text());proof['removed_copper_uuids']=sorted(c0.keys()-c1.keys());proof['added_copper_uuids']=sorted(c1.keys()-c0.keys());proof['new_In1_tracks']=[k for k in c1.keys()-c0.keys() if c1[k].startswith('(segment') and '(layer "In1.Cu")' in c1[k]];assert not proof['new_In1_tracks'];proof.update(antenna_rule_area_exactly_preserved=True,existing_footprints_with_intentional_pad_net_changes=changes,all_other_existing_pad_blocks_exactly_preserved=True)
(val/'power-board-proof.json').write_text(json.dumps(proof,indent=2));(eng/'COPPER_CHANGE_MANIFEST.json').write_text(json.dumps(proof,indent=2))
baseline=json.loads(Path('work/power-rev-d/rev-c-baseline-sha256.json').read_text());native=[p for p in base.iterdir() if p.suffix in ['.kicad_pcb','.kicad_sch','.kicad_pro','.kicad_sym','.kicad_dru']]
assert all(hashlib.sha256(p.read_bytes()).hexdigest()==baseline[p.name] for p in native),'Preserved Rev C native files changed'
(val/'preservation-proof.json').write_text(json.dumps({'Rev_C_native_files_unchanged':True,'checked_files':[p.name for p in native],'original_zip_sha256':hashlib.sha256(Path('work/original/Omni_UGV_KiCad_Review.zip').read_bytes()).hexdigest()},indent=2))
# Archive inherited views; current previews are generated from the final ten-page PDF.
hist=r/'preview/history/Rev_C';hist.mkdir(parents=True,exist_ok=True)
for p in list((r/'preview').glob('rev-c-*'))+list((r/'preview/layers').glob('rev-c-*')):
 dst=hist/p.name
 if not dst.exists():p.rename(dst)
sh=r/'preview/schematics';old=hist/'schematics';old.mkdir(exist_ok=True)
for p in sh.glob('*'):
 if p.is_file() and not (old/p.name).exists():p.rename(old/p.name)
doc=pymupdf.open(r/'Schematic.pdf');assert len(doc)==10
for i,page in enumerate(doc):page.get_pixmap(matrix=pymupdf.Matrix(1.4,1.4)).save(sh/f'sheet-{i+1}.png')
for name,i,bb in [('controller',1,(20,35,200,140)),('regulator',2,(20,40,325,175)),('drivers',3,(25,35,310,245)),('interlock',4,(20,35,380,250)),('usb-charge',5,(20,30,390,250)),('protection',6,(20,30,375,250)),('camera-power',7,(20,30,330,170)),('undervoltage',8,(15,25,385,225)),('charge-temperature',9,(15,30,395,225))]:
 doc[i].get_pixmap(matrix=pymupdf.Matrix(1.7,1.7),clip=pymupdf.Rect(*(v*72/25.4 for v in bb))).save(sh/f'detail-{name}.png')
contact=pymupdf.open()
for row in range(5):
 page=contact.new_page(width=1000,height=355)
 for col in range(2):page.show_pdf_page(pymupdf.Rect(col*500,0,(col+1)*500,355),doc,row*2+col)
contact.save(r/'preview/schematic-contact-sheets.pdf')
# Pure documentation pointer: distinguish the earlier presentation step from this power audit.
(eng/'STEP_1_REVIEW.md').write_text('# Current power audit\n\nSee POWER_AUDIT.md, POWER_CALCULATIONS.json and validation/current. The earlier schematic-organization step report is preserved at history/Rev_C/STEP_1_REVIEW.md. Current design-side changes are implemented; fabrication remains blocked by UNRESOLVED.md.\n',encoding='utf-8')
for p in (r/'mechanics').glob('Rev_C_board_only.step'):
 dst=r/'mechanics/history/Rev_C_board_only.step';dst.parent.mkdir(exist_ok=True)
 if not dst.exists():p.rename(dst)
p=r/'REV_C_SHA256.json'
if p.exists():
 dst=eng/'history/Rev_C/REV_C_SHA256.json'
 assert dst.read_bytes()==p.read_bytes();p.unlink()
# Store the complete actual editing trail as historical, non-idempotent helpers.
out=eng/'scripts/Rev_D_power';out.mkdir(parents=True,exist_ok=True)
for p in Path('work/power-rev-d').glob('*.py'):shutil.copy2(p,out/p.name)
(out/'README.md').write_text('Native CAD is authoritative. These scripts record incremental editing/audit operations in the original workspace; many are non-idempotent and expect its work/outputs directories. Do not run them over the delivered design. Use root validate.ps1 to repeat native rule checks. calculate.py is the temperature nodal-model source; copy it to a scratch workspace before running. No transient simulation or physical bench results are included.\n')
src=eng/'power-sources';p=Path('work/power-rev-d/sources/sn74lvc1g17.pdf');shutil.copy2(p,src/p.name)
p=src/'sources.json';s=json.loads(p.read_text());s['sha256'][p.name if False else 'sn74lvc1g17.pdf']=hashlib.sha256((src/'sn74lvc1g17.pdf').read_bytes()).hexdigest();p.write_text(json.dumps(s,indent=2))
visual={'revision':'D','status':'INSPECTED','pages':10,'source':'Schematic.pdf','native_3D_top':'preview/rev-d-top.png','native_3D_bottom':'preview/rev-d-bottom.png','limitations':['Missing custom 3D protection packages and offboard assembly; renders are not fit checks.','All pages regenerated; full-sheet overview and changed functional/power details inspected; no automatic readability guarantee.'],'notes':['Connected functional diagrams replace the temporary component-grid presentation.','Corrected property/power-label overlap and checked source parsing with native export and parity.']}
(r/'.pcba-workflow/schematic-visual-audit.json').write_text(json.dumps(visual,indent=2))
# Ensure final reports and native identity match before packaging.
d=json.loads((val/'drc.json').read_text());e=json.loads((val/'erc.json').read_text());assert not d['violations'] and not d['unconnected_items'] and not d['schematic_parity'];assert not any(v['violations'] for v in e['sheets'])
for fn in ['erc.json','drc.json','schematic.net.xml']:shutil.copy2(val/fn,r/fn)
manifest={str(p.relative_to(r)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in r.rglob('*') if p.is_file() and '.validation-runtime' not in p.parts and p.suffix not in ['.lck','.kicad_prl'] and p.name!='REV_D_SHA256.json'}
(r/'REV_D_SHA256.json').write_text(json.dumps(manifest,indent=2))
zp=r.parent/'Omni_UGV_Rev_D_power_audit_review.zip'
with zipfile.ZipFile(zp,'w',zipfile.ZIP_DEFLATED) as z:
 for p in r.rglob('*'):
  if p.is_file() and '.validation-runtime' not in p.parts and p.suffix not in ['.lck','.kicad_prl']:z.write(p,str(Path(r.name)/p.relative_to(r)))
with zipfile.ZipFile(zp) as z:assert z.testzip() is None;count=len(z.namelist())
print('Packaged',count,'files,',round(zp.stat().st_size/1e6,2),'MB; Rev C native preservation, antenna geometry, pad geometry and clean final checks verified')
