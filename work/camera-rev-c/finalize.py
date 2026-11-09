from pathlib import Path
import json,csv,shutil,hashlib,re,sys,xml.etree.ElementTree as E
sys.path.insert(0,'work/humanize');from build import blocks
r=Path('outputs/rover/Omni_UGV_Rev_C_flex_camera');base=r.parent/'Omni_UGV_Rev_B_protection'
history=r/'engineering/history/Rev_B';history.mkdir(parents=True,exist_ok=True)
for n in ['README.md','START_HERE.md','validation_summary.json']:
 if not (history/n).exists():shutil.copy2(base/n,history/n)
# Fresh metadata for the new native parts and moved probe connector.
new=json.loads(Path('work/camera-rev-c/new_parts.json').read_text());data=json.loads((r/'design_connections.json').read_text());by={d['ref']:d for d in data}
for d in new:by[d['ref']].update(x=d['x'],y=d['y'])
by['J5'].update(x=141.25,y=81.5)
(r/'design_connections.json').write_text(json.dumps(data,indent=2)+'\n')
m=json.loads((r/'mechanical.json').read_text());m['camera_revision']={'selected_module':'Arducam M0031','interface':'24-pin DVP FPC; Hirose FH12-24S-0.5SH(55)','connector_at_pcb_mm':[130.75,73.5],'head_mount':'printed bracket deferred pending measured head, lens, flex and optical geometry','fit_status':'UNVERIFIED','probe_connector_J5_at_mm':[141.25,81.5]};(r/'mechanical.json').write_text(json.dumps(m,indent=2)+'\n')
root=E.parse(r/'schematic.net.xml').getroot();vals={c.get('ref'):c.findtext('value') for c in root.findall('./components/comp')};rows=[]
for net in root.findall('./nets/net'):
 for p in net.findall('node'):rows.append(dict(Reference=p.get('ref'),Physical_pin=p.get('pin'),Pin_function=p.get('pinfunction',''),Net=net.get('name'),Value=vals.get(p.get('ref'),'')))
with (r/'engineering/PIN_MAP.csv').open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(sorted(rows,key=lambda d:(d['Reference'],d['Physical_pin'])))
p=r/'engineering/PIN_MAP.md';s=(base/'engineering/PIN_MAP.md').read_text(encoding='utf-8').replace('Rev B','Rev C');s+='\n\n## Rev C camera J3 physical pin map\n\n| Pin | Function | Net |\n|---|---|---|\n'
for d in sorted([d for d in rows if d['Reference']=='J3'],key=lambda d:int(d['Physical_pin'])):s+=f"| {d['Physical_pin']} | {d['Pin_function']} | {d['Net']} |\n"
p.write_text(s,encoding='utf-8')
# Prove outline, motor/clamp geometry, module and existing component pads unchanged.
a=(base/'omni_ugv.kicad_pcb').read_text();b=(r/'omni_ugv.kicad_pcb').read_text()
def sel(s,pred):return sorted(re.sub(r'\s+','',t) for _,_,t in blocks(s) if pred(t))
def fps(s):return {re.search(r'\(property "Reference" "([^"]+)',t)[1]:t for _,_,t in blocks(s) if t.startswith('(footprint')}
fa,fb=fps(a),fps(b);pads=lambda s:sel(s,lambda t:t.startswith('(pad'))
pad_changed=[n for n in fa if n not in ['J3','J5'] and pads(fa[n])!=pads(fb[n])]
edge=lambda t:'(layer "Edge.Cuts")' in t and t.startswith('(gr_')
def edge_geometry(s):
 return sorted(tuple(tuple(float(v) for v in pair.split()) for pair in re.findall(r'\((?:start|end|mid) ([^)]+)\)',t)) for _,_,t in blocks(s) if edge(t))
assert not pad_changed and edge_geometry(a)==edge_geometry(b)
routes=json.loads(Path('work/camera-rev-c/routes.json').read_text());assert not any(t['layer']=='In1.Cu' and not t['via'] for t in routes)
proof={'existing_component_pad_changes_except_J3_J5':pad_changed,'outline_unchanged_from_solid_perimeter_Rev_B':True,'new_In1_tracks':0,'intentional_changes':['J3 replaced by 24-pin FPC connector','J5 relocated','U8/U9 and camera support added','Camera signals and support routed on F/B/In2; through-vias present','Old header stubs removed','Silkscreen revision/camera label corrected'],'not_proven':['camera timing/eye margin','exact flex fit/orientation','assembled mechanical clearance','power and thermal qualification']}
(r/'validation/current/camera-board-proof.json').write_text(json.dumps(proof,indent=2)+'\n')
for n in ['erc.json','drc.json']:shutil.copy2(r/'validation/current'/n,r/n)
drc=json.loads((r/'drc.json').read_text());erc=json.loads((r/'erc.json').read_text());assert not drc['violations'] and not drc['unconnected_items'] and not drc['schematic_parity'];assert not any(s['violations'] for s in erc['sheets'])
summary={'review_date':'2026-11-06','revision':'C flex camera','status':'RULE_CHECKS_PASS_HARDWARE_QUALIFICATION_PENDING','kicad_version':'10.0.8','erc_violations':0,'drc':{'errors':0,'warnings':0,'unconnected_items':0,'schematic_parity_issues':0},'connectivity':'All existing non-J3 pin/net assignments match Rev B; J3 intentionally remapped; eight support parts added. See camera-connectivity-delta.json.','ignored_drc_checks':drc.get('ignored_checks',[]),'physical_testing':'none','release_blockers':'engineering/UNRESOLVED.md','native_source':'omni_ugv.kicad_pro'}
(r/'validation_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
(r/'START_HERE.md').write_text('''# Omni rover — Rev C flex camera

Open **omni_ugv.kicad_pro** in KiCad 10.0.8. This is the new camera revision. Rev B remains preserved separately.

J3 now accepts the selected **Arducam M0031 24-pin DVP flex module**, via a Hirose FH12-24S-0.5SH(55). It is incompatible with the old 18-pin Waveshare carrier. See engineering/CAMERA_REV_C.md and engineering/PIN_MAP.md before connecting anything.

Eight-page Schematic.pdf, BOM.csv, design_connections.json and validation/current reflect Rev C. Final configured checks: ERC 0; DRC errors/warnings 0; unconnected items 0; schematic parity 0. Every existing non-J3 pin retains its Rev B net assignment. These checks do not establish camera operation or fabrication readiness.

Current board previews: preview/rev-c-top.png and preview/rev-c-bottom.png. Old renders and mechanical STEP are historical and must not be used as current assembly geometry. Custom 3D bodies and the attached camera head are not fully represented.

Camera bracket, exact flex fit/contact orientation, signal integrity and camera power/thermal behavior require validation. Battery assumptions, protection cutoff/temperature-window work, regulator/motor thermal/transient work, mechanical fit, RF testing, firmware and Vita integration remain open. No board order or fabrication release is authorized.
''',encoding='utf-8')
(r/'README.md').write_text('''# Miniature omni camera rover — Rev C

Rev C replaces the large camera header with a 24-pin locking FPC interface for Arducam M0031. The camera connector and local supplies use the upper-right sector; power-converter and motor-driver groups retain locality. The solid 100 mm nominal perimeter and three motor openings are retained.

Read START_HERE.md, engineering/CAMERA_REV_C.md, engineering/BATTERY_ASSUMPTIONS.md, engineering/PIN_MAP.md and engineering/UNRESOLVED.md. Native KiCad sources are authoritative. Reversible edits used native text/API operations and KiCad CLI validation; there is no live editor IPC connection. Reload external edits in the editor rather than overwriting them from an older in-memory board.

Reports refer to configured checks and are not proof of electrical, thermal, RF or mechanical operation. Rev B construction/presentation scripts are historical and must not be run over Rev C. A prototype qualification pass and measured camera bracket are still required.
''',encoding='utf-8')
p=r/'CHANGELOG.md';p.write_text(p.read_text(encoding='utf-8')+'\n## Rev C — 2026-11-06\n\nSelected Arducam M0031; remapped J3 to locking FPC24; added U8/U9 core/analog supplies, C26–C29 and R44/R45; routed camera interface; relocated J5 for access; removed obsolete header stubs; corrected camera/revision silkscreen. Retained outline, motor geometry and all other existing pin/net assignments. Final configured ERC/DRC/parity/connectivity checks are clean. No hardware or bracket fit tests.\n',encoding='utf-8')
p=r/'engineering/UNRESOLVED.md';s=p.read_text(encoding='utf-8');s+='\n## Rev C camera qualification\n\nVerify supplied M0031 revision, flex contact side/thickness/pin-1 and connector drawing overlay. Measure lens/head/flex dimensions for the printed bracket. Check 1.3/2.8/3.3 V rails, sequencing, effective capacitors, SCCB logic levels, regulator thermal margin and added 3.3 V load. Scope XCLK/PCLK/data and prove camera capture/streaming. Camera cabling and bracket must avoid the antenna and motor leads. Motor/power audit remains unresolved as above.\n';s=s.replace('update the inherited board silkscreen revision mark (currently REV A) to the released revision. The current working project is Rev B.','ensure the released revision matches the board silkscreen (now REV C).');p.write_text(s,encoding='utf-8')
(r/'.pcba-workflow/circuit-review.md').write_text('# Circuit review — Rev C\n\nStatus: BLOCKED for fabrication. Native camera changes and configured checks are documented in engineering/CAMERA_REV_C.md. Exact supplied module/flex and mechanical geometry, camera sequencing/rail/thermal/timing qualification, prior power/protection issues and physical testing remain open.\n',encoding='utf-8')
(r/'.pcba-workflow/layout-review.json').write_text(json.dumps({'schema':'pcb-layout-review-v1','status':'BLOCKED','board_revision':'C','drc':summary['drc'],'configured_rule_check_status':'PASS','mechanical_status':'UNVERIFIED','critical_nets':['CAM_XCLK','CAM_PCLK','CAM_D0..7','CAM_1V3','CAM_2V8','+3V3'],'new_In1_signal_tracks':0,'unresolved':'engineering/UNRESOLVED.md','renders':['preview/rev-c-top.png','preview/rev-c-bottom.png']},indent=2)+'\n')
print('Updated Rev C engineering records; native and report assertions passed.')
