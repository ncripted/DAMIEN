from pathlib import Path
import json,csv,shutil,re,sys,math,hashlib,xml.etree.ElementTree as E
sys.path.insert(0,'work/humanize');from build import blocks
sys.path.insert(0,'work/power-rev-d');from calculate import calc
r=Path('outputs/rover/Omni_UGV_Rev_D_power_audit');base=r.parent/'Omni_UGV_Rev_C_flex_camera';eng=r/'engineering';val=r/'validation/current';eng.mkdir(exist_ok=True)
history=eng/'history/Rev_C';history.mkdir(parents=True,exist_ok=True)
for fn in ['START_HERE.md','README.md','validation_summary.json','REV_C_SHA256.json']:
 if (r/fn).exists():shutil.copy2(r/fn,history/fn)
for fn in ['PIN_MAP.md','PIN_MAP.csv','UNRESOLVED.md','BATTERY_ASSUMPTIONS.md','STEP_1_REVIEW.md','COPPER_CHANGE_MANIFEST.json','board_inventory.json']:
 if (eng/fn).exists():shutil.copy2(eng/fn,history/fn)
def nominal(temp):
 a,b=(200e3,100e3) if temp=='hot' else (442e3,100e3);v=(.3945 if temp=='hot' else .4)*(1+a/b)
 rn=v/((3.3-v)/1e4-v/300e3-v/542e3)
 return 1/(1/298.15+math.log(rn/1e4)/3435)-273.15
g=json.loads(Path('work/power-rev-d/geometry.json').read_text())
inventory={}
for n in ['CELL_P','CELL_N','VBAT','VMOTOR','SYS_RAW','M1_A','M1_B','M2_A','M2_B','M3_A','M3_B','REG_L1','REG_L2']:
 ts=[t for t in g['tracks'] if t['net']==n]
 inventory[n]={'width_mm_to_total_segment_length_mm':{str(w):sum(math.dist(t['a'],t['z']) for t in ts if not t['via'] and t['width']==w) for w in sorted({t['width'] for t in ts if not t['via']})},'In1_total_track_length_mm':sum(math.dist(t['a'],t['z']) for t in ts if not t['via'] and t['layer']=='In1.Cu'),'via_count':sum(t['via'] for t in ts),'limitation':'Segment inventory, not a serial power path, current-density solution, Kelvin proof or ampacity qualification.'}
(eng/'power-layout-inventory.json').write_text(json.dumps(inventory,indent=2))
calcdata={'model':'Static nodal / beta-equation engineering estimates; no physical measurements','temperature_assertion_corners_C':calc(),'nominal_temperature_assertion_C':{k:nominal(k) for k in ['hot','cold']},'corner_evaluations':4096,'resistor_envelope':'+/-1.5% including provisional TCR budget','NTC':'103AT-2 R25 +/-1%, B3435 +/-1%; full R-T curve and mounting not guaranteed by beta model','reference_envelope':'+/-1.5%','comparator_bias_A':{'hot':25e-9,'cold':15e-9},'charger_current_A':{'nominal':890/3570,'minimum':797/(3570*1.01),'maximum':975/(3570*.99)},'uv_supervisor_falling_V':[3.1*.985,3.1*1.015],'uv_supervisor_recovery_V':[3.1*.985+.175,3.1*1.015+.225],'uv_delay_nominal_s':618937*1e-7+50e-6,'U7_OCD_A':[.055/.0101,.065/.0099],'U7_OCC_A':[.033/.0101,.039/.0099],'U7_SCD_A':[.188/.0101,.212/.0099],'motor_chopping_A':[.160/(.25*1.01),.240/(.25*.99)],'Q1_Q2_pair_W_at_2p4A':{'old_85mohm_each':2*2.4**2*.085,'new_45mohm_each_at_VGS_2p5':2*2.4**2*.045,'new_62mohm_each_at_VGS_1p8':2*2.4**2*.062},'harness_budget_A':{'three_motor_static_upper':3*.240/(.25*.99),'logic_0p5A_at3p3V_from3p1V_assumed85pct':.5*3.3/(3.1*.85)},'C90_energy_J_4p2_to6V':.5*220e-6*(6**2-4.2**2),'drive_buffer':{'supply_test_envelope_V':[3.2,3.6],'max_static_output_load_A_using_VBE_0p4_R25_min_1pct':(3.6-.4)/(47000*.99)+3.6/(1e6*.99)+26e-6,'VOH_bound_V_at_3p2V_and_100uA':3.0,'DRIVE_ENABLE_bound_V_after1k_at100uA':2.9,'required_nSLEEP_high_V':2.5},'limitations':['Threshold endpoint calculations do not include measured contamination/leakage, mechanical thermal lag or the complete NTC R-T curve.','Current thresholds are static; include blanking, protection timing tolerance, overshoot, copper/TCR and fault recovery.','0.5A logic allocation and 85% efficiency are assumptions; 4A/5A harness targets are not a PCB rating.','U7 factory UV 2.6V remains an emergency-backstop compatibility blocker against an absolute assumed 3.0V cell minimum. U10 removes operating loads earlier, but does not make storage leakage zero.']}
assert calcdata['temperature_assertion_corners_C']['hot'][1]<45 and calcdata['temperature_assertion_corners_C']['cold'][0]>0
assert calcdata['drive_buffer']['max_static_output_load_A_using_VBE_0p4_R25_min_1pct']<100e-6
(eng/'POWER_CALCULATIONS.json').write_text(json.dumps(calcdata,indent=2))
report=Path('work/power-rev-d/POWER_AUDIT.md').read_text(encoding='utf-8').replace('6.4 °C cold / 40.0 °C hot',f"{nominal('cold'):.2f} °C cold / {nominal('hot'):.2f} °C hot").replace('approximately 11.1 mm long',f"approximately {inventory['M2_A']['In1_total_track_length_mm']:.2f} mm long")
report=report.replace('U7 retains its factory', 'U7 retains its factory')
report+='\n**Emergency undervoltage limit:** U10 is an operating-load shutdown, not a new high-side pack disconnect. U7 still has its 2.6 V factory backstop. Against a strict 3.0 V absolute cell minimum, the emergency/storage protection gate remains open: confirm the actual cell specification or implement a reviewed higher-threshold disconnect. Do not describe that compatibility issue as closed by U10.\n'
(eng/'POWER_AUDIT.md').write_text(report,encoding='utf-8');(r/'.pcba-workflow/circuit-review.md').write_text(report,encoding='utf-8')
# Canonical pin map and explicit electrical delta.
def connections(p):
 x=E.parse(p).getroot();out={}
 for net in x.findall('./nets/net'):
  for n in net.findall('node'):out[(n.get('ref'),n.get('pin'))]=dict(Net=net.get('name'),Pin_function=n.get('pinfunction',''))
 return x,out
x,con=connections(val/'schematic.net.xml');xb,before=connections(base/'validation/current/schematic.net.xml');values={c.get('ref'):c.findtext('value') for c in x.findall('./components/comp')}
rows=[dict(Reference=k[0],Physical_pin=k[1],Pin_function=v['Pin_function'],Net=v['Net'],Value=values.get(k[0],'')) for k,v in con.items()]
with (eng/'PIN_MAP.csv').open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(sorted(rows,key=lambda d:(d['Reference'],d['Physical_pin'].zfill(4))))
md=['# Rev D pin map from the saved native netlist','','Physical pad numbers are not GPIO numbers.','']
for ref in ['U1','J3','J4','J5','U7','U10','U11','U12','U13','U14']:
 md += [f'## {ref} — {values.get(ref,"")}', '', '| Physical pin | Pin function | Net |','|---|---|---|']
 for d in sorted([d for d in rows if d['Reference']==ref],key=lambda d:int(d['Physical_pin'])):md.append(f"| {d['Physical_pin']} | {d['Pin_function']} | {d['Net']} |")
 md+=['']
md+=['GPIO2 / module pad38 is CELL_TEMP_ADC. GPIO1 / pad39 is VBAT_ADC. An earlier explanatory sentence reversed these; the native pad assignments did not. GPIO42 / pad35 is now DRIVE_REQ_RAW, buffered by U14. GPIO44 / pad36 selects USB input mode. GPIO43 / pad37 drives status LED. GPIO35/36/37 remain reserved for N8R8 PSRAM and unused.','','J4 is the independent charging-temperature probe input to U12. J5 is the separate drive-temperature ADC probe. Both sensor heads attach to the insulated cell surface; neither lead connects to CELL_N.','']
(eng/'PIN_MAP.md').write_text('\n'.join(md),encoding='utf-8')
delta={'changed_existing_pins':[dict(ref=k[0],pin=k[1],before=before[k],after=con.get(k)) for k in before if con.get(k)!=before[k]],'added_pins':[dict(ref=k[0],pin=k[1],**v) for k,v in con.items() if k not in before],'removed_pins':[list(k) for k in before if k not in con],'new_parts':sorted(set(values)-{c.get('ref') for c in xb.findall('./components/comp')}),'intent':'U5 CE/TS and J4 charging probe; SW3 request separated from EN; GPIO42 buffered; remaining existing pin memberships must match Rev C.'}
expected={('U1','35'),('SW3','2'),('J4','1'),('U5','1'),('U5','4'),('TH1','1')}
assert {(d['ref'],d['pin']) for d in delta['changed_existing_pins']}==expected,delta['changed_existing_pins'];assert not delta['removed_pins']
(val/'power-connectivity-delta.json').write_text(json.dumps(delta,indent=2))
# Native board comparison, including exact preservation of ground-plane route and geometry.
def cu(s):return {re.search(r'\(uuid "?([0-9a-f-]+)',t)[1]:t for a,b,t in blocks(s) if t.startswith(('(segment','(via'))}
aa=(base/'omni_ugv.kicad_pcb').read_text();zz=(r/'omni_ugv.kicad_pcb').read_text();ca,cz=cu(aa),cu(zz)
changed=[k for k in ca.keys()&cz.keys() if re.sub(r'\s+','',ca[k])!=re.sub(r'\s+','',cz[k])]
assert not changed,changed
edges=lambda s:sorted(re.sub(r'\s+','',t) for a,b,t in blocks(s) if t.startswith('(gr_') and '(layer "Edge.Cuts")' in t)
assert edges(aa)==edges(zz)
new_copper={k:cz[k] for k in cz.keys()-ca.keys()};new_in1=[k for k,t in new_copper.items() if '(layer "In1.Cu")' in t and t.startswith('(segment')];assert not new_in1
oldpro=json.loads((base/'omni_ugv.kicad_pro').read_text());newpro=json.loads((r/'omni_ugv.kicad_pro').read_text());oldpro['text_variables']['REVISION']=newpro['text_variables']['REVISION'];assert oldpro==newpro,'Rules/project changes beyond revision variable'
assert (base/'omni_ugv.kicad_dru').read_bytes()==(r/'omni_ugv.kicad_dru').read_bytes()
proof={'outline_exactly_unchanged_from_Rev_C':True,'modified_existing_copper_uuids':changed,'removed_copper_uuids':sorted(ca.keys()-cz.keys()),'added_copper_uuids':sorted(new_copper),'new_In1_tracks':new_in1,'project_rule_settings_unchanged_except_revision_text_variable':True,'custom_DRC_rules_byte_identical':True,'inherited_M2_A_In1_route':'Preserved exactly; release review remains open.','intentional_pad_net_changes':['U1.35','SW3.2','J4.1','U5.1','U5.4'],'new_footprints':delta['new_parts']}
(val/'power-board-proof.json').write_text(json.dumps(proof,indent=2));(eng/'COPPER_CHANGE_MANIFEST.json').write_text(json.dumps(proof,indent=2))
data=json.loads((r/'design_connections.json').read_text());dm={d['ref']:d for d in data}
for fn in r.glob('*.kicad_sch'):
 for a,b,t in blocks(fn.read_text()):
  if not t.startswith('(symbol'):continue
  m=re.search(r'\(property "Reference" "([^"]+)',t)
  if m and m[1] in dm:
   v=list(map(float,re.search(r'\(at ([^)]+)',t)[1].split()));dm[m[1]].update(sx=v[0],sy=v[1])
(r/'design_connections.json').write_text(json.dumps(data,indent=2))
roles={'U10':'Raw-cell UV supervisor','Q9':'Protected-rail inversion of UV reset','Q10':'UV clamp on regulator enable','Q11':'UV clamp on driver/motor enable','R54':'Isolates switch request from clamped EN','U11':'USB-powered temperature reference LDO','U12':'Cell hot/cold window comparator','U13':'Fail-disabled charger CE inversion','U14':'Drive request logic buffer','R64':'Default-low buffer input','R60':'Fixed BQ TS bias; TH1 monitoring moved to U12','R55':'Cell thermistor excitation','R56':'Hot divider top','R57':'Hot divider bottom','R58':'Cold divider top','R59':'Cold divider bottom','R61':'Delayed permission pullup','R62':'Limits comparator capacitor-discharge current','C35':'Charge-enable startup delay','R63':'CE startup pullup','U5':'USB charger and logic power path','U4':'Main buck-boost regulator','U7':'Emergency cell fault protection controller','Q7':'Charge protection FET','Q8':'Discharge protection FET','R36':'Main cell-current shunt','Q1':'Motor rail reverse-blocking P-FET pair','Q2':'Motor rail reverse-blocking P-FET pair','Q3':'Motor switch gate pull-down','Q4':'USB-driven hardware motor inhibit','U2':'Two active motor bridges','U3':'One active motor bridge; unused bridge grounded/NC as documented','J2':'Raw cell connector','J4':'Off-board TH1 cell charge-temperature probe','J5':'Off-board TH2 drive-temperature probe'}
with (eng/'COMPONENT_FUNCTIONS.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=['Reference','Value','Functional_block','Role','Nets']);w.writeheader()
 for d in data:w.writerow(dict(Reference=d['ref'],Value=d['value'],Functional_block=d.get('group',''),Role=roles.get(d['ref'],('Local bypass/filter capacitor' if d['ref'].startswith('C') else 'Bias/limit/sense resistor; exact pin nets provided' if d['ref'].startswith('R') else 'See native functional schematic')),Nets='; '.join(f'{k}:{v}' for k,v in d['nets'].items())))
summary={'revision':'D','status':'DESIGN_AUDIT_IMPLEMENTED__FABRICATION_BLOCKED','kicad_version':'10.0.8','erc_violations':0,'drc':{'errors':0,'warnings':0,'unconnected_items':0,'schematic_parity_issues':0},'physical_tests_performed':[],'new_components':len(delta['new_parts']),'review':'engineering/POWER_AUDIT.md','open_items':'engineering/UNRESOLVED.md','scope':'Configured checks and engineering estimates; not an electrical/thermal/mechanical qualification or release.'}
dr=json.loads((val/'drc.json').read_text());er=json.loads((val/'erc.json').read_text());assert not dr['violations'] and not dr['unconnected_items'] and not dr['schematic_parity'];assert not any(s['violations'] for s in er['sheets'])
(r/'validation_summary.json').write_text(json.dumps(summary,indent=2));(val/'validation_summary.json').write_text(json.dumps(summary,indent=2))
for fn in ['erc.json','drc.json','schematic.net.xml']:shutil.copy2(val/fn,r/fn)
shutil.copy2('work/power-rev-d/rev-c-baseline-sha256.json',val/'rev-c-baseline-sha256.json')
scripts=eng/'scripts/Rev_D_power';scripts.mkdir(parents=True,exist_ok=True)
for fn in ['calculate.py','functional_drawings.py','build_revision.py','add_drive_buffer.py','finalize_engineering.py']:shutil.copy2(Path('work/power-rev-d')/fn,scripts/fn)
sources=eng/'power-sources';sources.mkdir(exist_ok=True);urls={}
for root in [Path('work/power-audit/sources'),Path('work/power-rev-d/sources')]:
 if (root/'urls.json').exists():urls.update(json.loads((root/'urls.json').read_text()))
 for p in root.glob('*.pdf'):
  if p.read_bytes()[:4]==b'%PDF':shutil.copy2(p,sources/p.name)
urls.update(sn74lvc1g17='https://www.ti.com/lit/ds/symlink/sn74lvc1g17.pdf',mmbt3904='https://www.diodes.com/datasheet/download/MMBT3904.pdf',mmbt3906='https://www.diodes.com/datasheet/download/MMBT3906.pdf',pololu3065='https://www.pololu.com/product/3065/specs',esp32_s3_wroom='https://www.espressif.com/sites/default/files/documentation/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf')
for name in ['bss138bk','bat54']:urls.pop(name,None)
(sources/'sources.json').write_text(json.dumps({'reviewed_utc_date':'2026-11-06','urls':urls,'download_limitations':'Diodes direct downloads returned HTTP403; exact current official PDFs were inspected through browser research. URLs retained. No distributor substitute used as electrical authority.','sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sources.glob('*.pdf')}},indent=2))
print('Final native metadata:',len(values),'components,',len(con),'pin memberships;',len(delta['new_parts']),'new components; rule and geometry proofs passed')
