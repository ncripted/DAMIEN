from pathlib import Path
import json,re,sys,csv,math,shutil,hashlib,xml.etree.ElementTree as ET
import pymupdf
sys.path.insert(0,'work/humanize');from build import blocks
r=Path('outputs/rover/Omni_UGV_Rev_E_power_layout');base=r.parent/'Omni_UGV_Rev_D_power_audit';eng=r/'engineering';val=r/'validation/current'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
drc=json.loads((val/'drc.json').read_text());erc=json.loads((val/'erc.json').read_text())
assert not drc['violations'] and not drc['unconnected_items'] and not drc['schematic_parity']
assert not any(s['violations'] for s in erc['sheets'])
g=json.loads(Path('work/rev-e/geometry.json').read_text());gb=json.loads(Path('work/rev-e/baseline_geometry.json').read_text())
assert g['outline']==gb['outline'],'Outline changed'
critical={p['ref'] for p in gb['pads'] if p['ref'].startswith(('M','H'))}
def padkey(p):return {k:p[k] for k in ['ref','num','at','size','angle','drill','layers','shape']}
assert sorted([padkey(p) for p in g['pads'] if p['ref'] in critical],key=str)==sorted([padkey(p) for p in gb['pads'] if p['ref'] in critical],key=str)
assert not [t for t in g['tracks'] if not t['via'] and t['layer']=='In1.Cu' and t['net']!='GND']
def footprint(s,ref):return next(t for a,b,t in blocks(s) if t.startswith('(footprint') and f'(property "Reference" "{ref}"' in t)
def rf(s):return [re.sub(r'\s+','',t) for a,b,t in blocks(footprint(s,'U1')) if t.startswith('(zone')]
assert rf((r/'omni_ugv.kicad_pcb').read_text())==rf((base/'omni_ugv.kicad_pcb').read_text())
assert sha(r/'omni_ugv.kicad_dru')==sha(base/'omni_ugv.kicad_dru')
j,jb=[json.loads((p/'omni_ugv.kicad_pro').read_text()) for p in [r,base]]
assert j['board']['design_settings']==jb['board']['design_settings']
baseline=json.loads(Path('work/rev-e/baseline-sha256.json').read_text());preserved=[fn for fn,h in baseline.items() if (base/fn).is_file() and sha(base/fn)==h]
assert len(preserved)==len(baseline)
original=Path('work/original/Omni_UGV_KiCad_Review.zip')
proof=dict(revision='E',preserved_Rev_D_files=len(preserved),original_zip_sha256=sha(original),outline_exactly_preserved=True,motor_and_mount_pad_geometry_preserved=True,antenna_footprint_rule_area_preserved=True,custom_rules_unchanged=True,board_design_settings_unchanged=True,In1_non_ground_track_count=0,limitations=['Configured rules include inherited ignored checks and the J1-specific hole-clearance rule.','This evidence is not thermal, RF, structural, assembly-process or cell qualification.'])
(val/'preservation-and-layout-proof.json').write_text(json.dumps(proof,indent=2))
# Netlist-derived pin map and intended source membership, independent of drawing labels.
x=ET.parse(val/'schematic.net.xml').getroot();values={c.get('ref'):c.findtext('value') for c in x.findall('./components/comp')};rows=[];nets={}
for net in x.findall('./nets/net'):
 nodes=[(n.get('ref'),n.get('pin')) for n in net.findall('node')];nets[net.get('name')]=nodes
 for n in net.findall('node'):rows.append(dict(Reference=n.get('ref'),Physical_pin=n.get('pin'),Pin_function=n.get('pinfunction',''),Net=net.get('name'),Value=values.get(n.get('ref'),'')))
assert {('R36','4'),('U7','4')}==set(nets['PROT_CS_SENSE'])
assert {('R36','3'),('U7','3'),('C24','2')}=={n for n in nets['PROT_VSS_SENSE'] if not n[0].startswith('#')}
assert ('Q13','5') in nets['VBAT'] and ('Q13','1') in nets['PROTECTED_RAW'] and ('Q8','1') in nets['PROTECTED_RAW']
assert ('Q7','1') in nets['CELL_P'] and ('R46','1') in nets['CELL_P']
with (eng/'PIN_MAP.csv').open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(sorted(rows,key=lambda z:(z['Reference'],z['Physical_pin'].zfill(4))))
md=['# Rev E pin map','', 'Derived from validation/current/schematic.net.xml. Physical module pads differ from GPIO numbers.','']
for ref in ['U1','J3','J4','J5','U7','R36','U10','Q12','Q13','U14']:
 md += [f'## {ref} — {values.get(ref, "")}', '', '| Physical pin | Function | Net |','|---|---|---|']
 md += [f"| {z['Physical_pin']} | {z['Pin_function']} | {z['Net']} |" for z in rows if z['Reference']==ref];md+=['']
(eng/'PIN_MAP.md').write_text('\n'.join(md),encoding='utf-8')
before=ET.parse(base/'schematic.net.xml').getroot();bn={}
for n in before.findall('./nets/net'):
 for node in n.findall('node'):bn[(node.get('ref'),node.get('pin'))]=n.get('name')
delta=[dict(Reference=z['Reference'],Physical_pin=z['Physical_pin'],Before=bn.get((z['Reference'],z['Physical_pin'])),After=z['Net']) for z in rows if bn.get((z['Reference'],z['Physical_pin']))!=z['Net']]
(val/'electrical-delta.json').write_text(json.dumps(delta,indent=2))
(eng/'board_inventory.json').write_text(json.dumps(g))
inv={}
for net in ['CELL_P','CELL_N','PROTECTED_RAW','VBAT','VMOTOR','SYS_RAW','M1_A','M1_B','M2_A','M2_B','M3_A','M3_B','M1_SENSE','M2_SENSE','M3_SENSE','REG_L1','REG_L2']:
 ts=[t for t in g['tracks'] if t['net']==net];inv[net]=dict(width_to_segment_length_mm={str(w):sum(math.dist(t['a'],t['z']) for t in ts if not t['via'] and t['width']==w) for w in sorted({t['width'] for t in ts if not t['via']})},via_count=sum(t['via'] for t in ts),In1_track_length_mm=sum(math.dist(t['a'],t['z']) for t in ts if not t['via'] and t['layer']=='In1.Cu'))
(eng/'power-layout-inventory.json').write_text(json.dumps(inv,indent=2))
calc=dict(model='Engineering estimates; no bench measurements',UV_falling_V=[3.1*.985,3.1*1.015],UV_recovery_V=[3.1*.985+.175,3.1*1.015+.225],UV_release_delay_nominal_s=618937*100e-9+50e-6,shunt_ohm=.01,shunt_dissipation_W={str(i):i*i*.01 for i in [4,5,6]},Q13_loss_W_at_25C_max_Rds_2p5V={str(i):i*i*.0098 for i in [4,5]},Q13_loss_W_assuming_2x_hot_Rds={str(i):i*i*.0196 for i in [4,5]},shunt_current_thresholds_1pct_only_A={'OCD':[.055/.0101,.065/.0099],'OCC':[.033/.0101,.039/.0099],'SCD':[.188/.0101,.212/.0099]},shunt_TCR_budget_ohm=[.01*(1-.0135),.01*(1+.0135)],OCD_with_1p35pct_resistance_budget_A=[.055/(.01*1.0135),.065/(.01*.9865)],copper_assumptions={'rho_ohm_m':1.724e-8,'thickness_m':35e-6,'resistance_mohm_per_10mm':{str(w):1.724e-8*.01/(w*1e-3*35e-6)*1e3 for w in [.2,.4,.6,.8,1.5]},'via_barrel_mohm_assuming_1p6mm_length_0p3mm_finished_hole_20um_plating':1.724e-8*.0016/(math.pi*.0003*.00002)*1e3},cutoff_standby_estimate_uA={'R46_at_3p1V_reset_low':3.1/100e3*1e6,'Q12_base_R65_assuming_0p7V_BE_0p2V_reset':(3.1-.7-.2)/47e3*1e6,'Q12_collector_R67_assuming_gate_2p9V':2.9/56e3*1e6,'additional':'U7/U10, leakage, R66, gate pulls and residual protected loads must be measured; budget about 0.15mA, not a guaranteed maximum'},limitations=['Copper segment sums include branches/parallel copper; they are not a serial path resistance or IPC-2152 ampacity rating.','Gate and UV thresholds are static; startup, dip response, MOSFET off leakage and recovery remain bench tests.','22uF is nominal. No guaranteed effective capacitance at DC bias/temperature/aging has been established.','Protection fault timing and short-circuit pulse energy require measured verification.'])
(eng/'POWER_CALCULATIONS.json').write_text(json.dumps(calc,indent=2))
# Record actual assembly-sensitive via locations instead of hiding them behind zero DRC.
via_notes=[]
for ref in ['Q7','Q8','Q13']:
 for p in [p for p in g['pads'] if p['ref']==ref and p['num'] in ['1','2','3']]:
  for t in g['tracks']:
   if t['via'] and t['net']==p['net'] and abs(t['a'][0]-p['at'][0])<p['size'][0]/2+t['drill']/2 and abs(t['a'][1]-p['at'][1])<p['size'][1]/2+t['drill']/2:via_notes.append(dict(Reference=ref,Pad=p['num'],Via_UUID=t['uuid'],X_mm=t['a'][0],Y_mm=t['a'][1],Diameter_mm=t['width'],Drill_mm=t['drill'],Requirement='Filled and copper-capped via-in-pad process, or reroute before standard assembly'))
with (eng/'SOURCE_PAD_VIAS.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=list(via_notes[0]) if via_notes else ['Reference']);w.writeheader();w.writerows(via_notes)
sources=[('WSK2512 manufacturer land pattern and ratings','https://www.vishay.com/docs/30108/wsk2512.pdf'),('BQ2980/BQ2982 primary protector','https://www.ti.com/lit/ds/symlink/bq2980.pdf'),('TPS3840 supervisor','https://www.ti.com/lit/ds/symlink/tps3840.pdf'),('TPS63802 regulator','https://www.ti.com/lit/ds/symlink/tps63802.pdf'),('DMP2008UFG PFET','https://www.diodes.com/datasheet/download/DMP2008UFG.pdf'),('TDK capacitor production listing','https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C2012X5R1A226M125AB')]
(eng/'SOURCES.md').write_text('# Rev E primary sources\n\nReviewed 2026-11-07.\n\n'+'\n'.join(f'- [{name}]({url})' for name,url in sources)+'\n\nThe TDK K-tolerance variant is NRND; the selected M-tolerance variant is listed Production. The K-variant characterization graph is not a guaranteed bias specification for the selected M part. No such guarantee is claimed.\n',encoding='utf-8')
sourcesdir=eng/'sources';sourcesdir.mkdir(exist_ok=True)
for src in ['work/rev-e/sources/wsk2512.pdf','work/protection/bq2980.pdf','work/power-rev-d/sources/tps3840.pdf','work/power-audit/sources/tps63802.pdf']:
 p=Path(src)
 if p.exists():shutil.copy2(p,sourcesdir/p.name)
for fn in ['CAMERA_REV_C.md','BATTERY_ASSUMPTIONS.md','OUTLINE_CHANGE.md']:
 shutil.copy2(r/'.history/rev-d-import/engineering'/fn,eng/fn)
summary=dict(revision='E',date='2026-11-07',KiCad='10.0.8',DrcErrors=0,DrcWarnings=0,Unconnected=0,ParityIssues=0,ErcViolations=0,zones_refilled_and_saved=True,physical_tests_performed=False,fabrication_gate='BLOCKED',source_pad_vias_requiring_process_review=len(via_notes),ignored_checks=drc.get('ignored_checks',[]),primary_artifacts=['omni_ugv.kicad_pro','omni_ugv.kicad_pcb','Schematic.pdf','engineering/SIX_STEP_REVIEW.md'])
(r/'validation_summary.json').write_text(json.dumps(summary,indent=2))
(r/'.pcba-workflow/layout-review.json').write_text(json.dumps(dict(status='BLOCKED',reason=['U7 startup/wake compatibility','Source-pad via filling/capping or layout change','Unqualified thermal/current/transient/effective-capacitance behavior'],configured_checks=summary),indent=2))
sh=r/'preview/schematics';sh.mkdir(exist_ok=True);doc=pymupdf.open(r/'Schematic.pdf');assert len(doc)==11
for i,page in enumerate(doc):page.get_pixmap(matrix=pymupdf.Matrix(1.25,1.25)).save(sh/f'sheet-{i+1}.png')
# Clear current-facing stale manifest; its preserved copy remains in the history import.
p=r/'REV_D_SHA256.json'
if p.exists():p.unlink()
# Only current accepted checkpoints are exported as evidence. Rejected routing experiments stay in work/.
steps=val/'steps';steps.mkdir(exist_ok=True)
for n in [1,2,3,4,5]:
 p=Path(f'work/rev-e/steps/step{n}-drc.json')
 if p.exists():shutil.copy2(p,steps/p.name)
for fn in ['step2-width-accepted.json','final-width-changes.json']:
 shutil.copy2(Path('work/rev-e')/fn,val/fn)
print('Prepared current pin map, evidence, calculations and',len(via_notes),'source-pad via process entries')
