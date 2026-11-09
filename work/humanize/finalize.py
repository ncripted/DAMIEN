from pathlib import Path
import json,csv,re,shutil,hashlib,xml.etree.ElementTree as ET
root=Path('outputs/rover/Omni_UGV_Rev_B_protection');eng=root/'engineering';wf=root/'.pcba-workflow';wf.mkdir(exist_ok=True)
current=root/'validation/current';current.mkdir(exist_ok=True)
for n in ['erc.json','drc.json','schematic.net.xml']:shutil.copyfile(root/n,current/n)
hist=eng/'history';hist.mkdir(exist_ok=True)
for n in ['README.md','START_HERE.md','CHANGELOG.md']:
 if not (hist/('pre_step1_'+n)).exists():shutil.copyfile(root/n,hist/('pre_step1_'+n))
if not (hist/'Rev_A_AUDIT.md').exists():shutil.copyfile(eng/'AUDIT.md',hist/'Rev_A_AUDIT.md')
x=ET.parse(root/'schematic.net.xml');comps={c.attrib['ref']:c for c in x.findall('.//components/comp')}
rows=[]
for n in x.findall('.//nets/net'):
 for pin in n.findall('node'):
  ref=pin.attrib['ref'];rows.append(dict(Reference=ref,Physical_pin=pin.attrib['pin'],Pin_function=pin.attrib.get('pinfunction',''),Net=n.attrib['name'],Value=comps[ref].findtext('value')))
with (eng/'PIN_MAP.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(sorted(rows,key=lambda d:(d['Reference'],d['Physical_pin'].zfill(4))))
lines=['# Rev B actual ESP32 module pin map','', 'Exported from the current native KiCad XML netlist. Physical module pad numbers are not GPIO numbers.','', '| Physical pad | Pin function | Net |','|---|---|---|']
for d in sorted([d for d in rows if d['Reference']=='U1'],key=lambda d:int(d['Physical_pin'])):lines.append(f"| {d['Physical_pin']} | {d['Pin_function']} | {d['Net']} |")
lines+=['','GPIO1 / module pad38 is CELL_TEMP_ADC. GPIO43 / pad37 drives LED_STATUS and TP7. Native USB GPIO19/20 remains the programming interface. GPIO35/36/37 remain unused because this N8R8 module reserves them for PSRAM.','', 'J4: charger cell probe, pin1 BAT_NTC / pin2 GND. J5: independent drive cell probe, pin1 CELL_TEMP_DIV / pin2 GND. Both sensor heads attach to the cell, with insulated leads; neither connects to raw CELL_N.']
(eng/'PIN_MAP.md').write_text('\n'.join(lines)+'\n')
data=json.loads((root/'design_connections.json').read_text())
for d in data:
 if d['ref']=='R42':d['x']=125.3;d['y']=88
(root/'design_connections.json').write_text(json.dumps(data,indent=2)+'\n')
p=Path('work/protection/placements.json');d=json.loads(p.read_text());d['R42']=[125.3,88];p.write_text(json.dumps(d,indent=2))
for p in [Path('work/protection/new_parts.json')]:
 d=json.loads(p.read_text())
 for c in d:
  if c['ref']=='R42':c['x']=125.3;c['y']=88
 p.write_text(json.dumps(d,indent=2))
m=json.loads((root/'mechanical.json').read_text());m['rev_b_protection_notes']=['Backside protection parts need cover clearance and thermal qualification; missing package models make renders incomplete.','TH1 and TH2: separate insulated 103AT-2 probes bonded to actual cell pouch, with harness strain relief.','Battery dimensions and exact cell rating remain unselected; cradle and supports remain provisional.'];(root/'mechanical.json').write_text(json.dumps(m,indent=2)+'\n')
drc=json.loads((root/'drc.json').read_text());erc=json.loads((root/'erc.json').read_text())
summary=dict(review_date='2026-11-05',status='STEP_1_COMPLETE_PROTOTYPE_NOT_RELEASED',kicad_version='10.0.8',erc_violations=sum(len(s['violations']) for s in erc['sheets']),drc=dict(errors=sum(v['severity']=='error' for v in drc['violations']),warnings=sum(v['severity']=='warning' for v in drc['violations']),unconnected_items=len(drc['unconnected_items']),schematic_parity_issues=len(drc['schematic_parity'])),connectivity=dict(result='EXACT_MATCH',components=111,nets=96,pin_memberships=365),ignored_drc_checks=drc['ignored_checks'],local_manufacturing_exception='Inherited J1-only 0.19 mm hole clearance requires fabricator acceptance; global 0.25 mm unchanged.',release_blockers='engineering/UNRESOLVED.md',original_zip_sha256='b98c896f4cad7e2c9cc6c30c1111b8cb07aa9229da0994c1721cee39b67e5380')
assert summary['erc_violations']==0 and not any(summary['drc'].values())
(root/'validation_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
shutil.copyfile(Path('work/humanize/before/net.xml'),current/'before_readability.net.xml')
(current/'connectivity-comparison.txt').write_text('Baseline: 111 components, 96 nets. Final: 111 components, 96 nets.\nPASS: exact match of component identity, named nets and all 365 pin memberships.\nCompared using schematic-humanizer compare_connectivity.py against native KiCad XML exports.\n')
sources=eng/'presentation_baseline';sources.mkdir(exist_ok=True)
for p in Path('work/humanize/before').glob('*.kicad_sch'):shutil.copyfile(p,sources/p.name)
script=Path('work/humanize/build.py').read_text().replace("ROOT=Path('outputs/rover/Omni_UGV_Rev_B_protection')","ROOT=Path(__file__).resolve().parents[2]").replace("BASE=Path('work/humanize/before')","BASE=ROOT/'engineering/presentation_baseline'")
(eng/'scripts/readable_schematic.py').write_text(script)
(eng/'scripts/README.md').write_text('''# Editing workflow

The root native KiCad files are the current editable design. Open omni_ugv.kicad_pro in KiCad 10.
The PCB was edited using pcbnew and native text; schematics were regenerated with a presentation-only adapter and checked against XML netlists.

readable_schematic.py reconstructs the November 5 presentation from the explicitly archived presentation_baseline, not from arbitrary later electrical edits. It rewrites all seven schematic files and the CSD17308Q3 library symbol. Back up current files and update its input snapshot before using it after electrical changes. Do not run older protection construction scripts over the finished board: they reset routing.

validate.ps1 reruns the native configured checks. A CLI exit code alone is not the result; inspect violation counts. Saved reports apply to their hashed snapshot.

The KiCad GUI can display the same saved files, but there is no live IPC edit connection. Reload externally modified files; do not save an older open editor over a newer disk revision.
''')
audit=dict(schema='schematic-visual-audit-v1',status='PASS',source_type='native KiCad',adapter='Native S-expression presentation generator; KiCad 10.0.8 PDF/ERC/XML exports; exact schematic-connectivity-v1 comparison',authoritative_sources=[p.name for p in root.glob('*.kicad_sch')],baseline_connectivity='validation/current/before_readability.net.xml',final_connectivity='schematic.net.xml',connectivity_result='PASS',erc_or_lint={'before':0,'after':0},protected_artifacts_unchanged=False,protected_artifacts_note='Schematic cleanup preserved electrical identities and connectivity. Separately authorized board changes: R42 moved 0.2 mm left; U1 keepout expanded to explicit four-layer scope, with library coordinates corrected. See board-change-proof.json.',sheets=[dict(name=n,full_page_render=f'preview/schematics/sheet-{i+1}.png',status='PASS') for i,n in enumerate(['Overview','Controller','Regulator','Motors','Interlock','Charging','Protection'])],dense_crops=[dict(region=n,render=f'preview/schematics/detail-{n}.png',status='PASS') for n in ['controller','regulator','drivers','interlock','usb-charge','protection']],remaining_limitations=['Readability and configured rule-check success are not functional, thermal, footprint-manufacturer or mechanical approval.','Pin-explicit Q7/Q8 symbols stack electrically common package pads; the exported pin map includes every physical pad.'],final_snapshot='Schematic.pdf')
(wf/'schematic-visual-audit.json').write_text(json.dumps(audit,indent=2)+'\n')
(wf/'layout-review.json').write_text(json.dumps(dict(status='BLOCKED_FOR_FABRICATION',step1_status='PASS',date='2026-11-05',drc=summary['drc'],changes=['R42: (125.5,88) -> (125.3,88) mm; no trace edits','U1 keepout: all four copper layers; library polygon uses local coordinates'],exceptions=[summary['local_manufacturing_exception']],open_findings='engineering/UNRESOLVED.md',release_authorized=False),indent=2)+'\n')
(wf/'circuit-review.md').write_text('# Circuit review gate\n\nBLOCKED for fabrication release. Step 1 is complete: presentation equivalence, ERC, DRC and parity passed.\n\nThe Rev B protection circuit exists in the native schematic/PCB; electrical, thermal and fault-response qualification is still open. See engineering/AUDIT.md and engineering/UNRESOLVED.md. No firmware temperature cutoff or hardware testing is claimed.\n')
(root/'START_HERE.md').write_text('''# Omni rover — Rev B, step 1 complete

Open **omni_ugv.kicad_pro** in KiCad 10.0.8. This directory is the current working revision; the original ZIP and Rev A remain preserved.

The seven-page **Schematic.pdf** is the current review drawing. Native schematics now group functions and show local wiring. The XML comparison preserves 111 component identities, 96 named nets and 365 pin memberships.

On 2026-11-05: ERC 0, DRC errors 0, DRC warnings 0, unconnected items 0, schematic-parity issues 0. See validation_summary.json and validation/current. These results apply to configured checks and the recorded snapshot, not physical qualification.

Read engineering/STEP_1_REVIEW.md for changes, engineering/PIN_MAP.md for GPIOs, and engineering/UNRESOLVED.md before fabrication. The board remains an unbuilt engineering prototype. No fabrication release or order is authorized.

Rev B includes onboard cell protection and two separate off-board cell-temperature probes. J2 is raw cell input; J4 is the charger probe; J5 is the drive-monitor probe. Both probe heads must contact the actual cell through electrical insulation. Drive temperature shutdown still needs firmware.

Current previews: preview/protection-top.png, preview/protection-bottom.png and preview/schematics. Missing custom-package 3D bodies mean renders are not assembly-clearance proof. Mechanics remain provisional.
''')
(root/'README.md').write_text('''# Miniature three-wheel camera rover — Rev B

Current state: **step 1 complete, prototype not released for fabrication**. Start with START_HERE.md.

Three independent omni-wheel drives, ESP32-S3-WROOM-1-N8R8, two DRV8833PWP drivers, BQ24074 charger and TPS63802 regulator remain the core design. Rev B adds BQ298217RUGR protection, a CSD17308Q3 common-drain FET pair, a 10 mΩ shunt and a separate cell-temperature ADC input.

## Files

- Native project: omni_ugv.kicad_pro, root and six child .kicad_sch sheets, omni_ugv.kicad_pcb, local symbol/footprint libraries.
- Schematic.pdf and preview/schematics: current readable review drawing and detail images.
- BOM.csv / design_connections.json / engineering/PIN_MAP.csv: current parts, metadata and exported physical pin connections.
- validation/current and validation_summary.json: current checks; STEP1_SHA256.json identifies the checked native files.
- engineering/STEP_1_REVIEW.md: exact changes and verification limits.
- engineering/UNRESOLVED.md: next engineering gates.
- mechanics and mechanical.json: provisional fitting work; no physical-fit certification.
- engineering/history: prior notes retained for traceability; superseded where Rev B differs.

## Cell and temperature interface

J2 pin1 CELL_P, pin2 CELL_N feed onboard protection. Protected VBAT supplies the charger BAT connection and motor-power switching. Motor current does not pass through charger OUT/SYS_RAW. R36 is the intended raw-negative to system-ground connection.

J4 and J5 each use an independent electrically insulated two-wire 103AT-2 probe bonded to the cell. J4 serves charger TS. J5 feeds GPIO1/ADC1 through R42/R43/C25. GPIO43 now drives the status LED; native USB programming remains available.

No selected cell, connector/harness qualification, thermal test, braking test, built firmware or Vita video demonstration is implied by the current rule-check results.

## Repeatability

Run validate.ps1 for configured checks. engineering/scripts/README.md explains the presentation generator and reload limitations. Edits are saved files, not a live IPC session. Avoid saving a stale editor over externally modified files.
''')
(eng/'STEP_1_REVIEW.md').write_text('''# Step 1 review — 2026-11-05

Completed the authorized schematic organization and known rule-check cleanup in actual KiCad sources.

## Changes

1. Reorganized all seven pages: root overview, controller/camera/service points, regulator, motor channels, interlock/measurement, USB/charger, and protection/cell probes. Added native orthogonal wiring for reset/boot, decoupling, USB data, charger configuration, feedback, driver support, transistor controls and temperature divider. Global labels remain for cross-sheet and long connections. Moved the overlapping root sheet and previously off-page power flags into the drawing.
2. Made Q7/Q8 pin-explicit symbols show source and drain groups on opposite sides and the common-drain connection visibly. Hidden stacked pins remain in the XML pin map. Updated the bundled symbol to match. No physical pin assignment or component value changed during presentation cleanup.
3. Moved R42 on B.Cu from (125.5,88.0) to (125.3,88.0) mm. This removed two 0.0953 mm clearances to CELL_TEMP_ADC while preserving the 0.15 mm rule. Existing copper still terminates inside the pads. No trace/via routing was changed in step 1.
4. Investigated U1 using KiCad's native Compare Footprint with Library dialog. Its exact finding was that rule-area corners differed. The library polygon had board coordinates (87..135,40.25..61.25), rather than coordinates local to U1 at (111,68). Corrected the library polygon to (-24..24,-27.75..-6.75). The board's X/Y keepout extent did not move. Explicitly included F.Cu, In1.Cu, In2.Cu and B.Cu in the footprint keepout and recorded its four-layer stackup. Pads, pad numbers and module placement did not move. The mismatch warning now clears without an exclusion or severity change.

## Checks actually performed

KiCad 10.0.8 native ERC: 0 violations. Native DRC with zone refill and schematic parity: 0 errors, 0 warnings, 0 unconnected items, 0 parity issues. Native XML connectivity compared with the pre-cleanup snapshot: exact match of 111 component identities, 96 named nets and 365 pin memberships.

Rendered all seven pages and inspected full sheets plus detailed controller, regulator, driver, interlock, USB/charger and protection crops. Corrected label orientation/justification, title-block clipping, text crossing power leads and ambiguous collinear wire paths. The generator separately rejects different net labels sharing a continuous wire graph.

Schematic edits and board fixes were separate stages. See validation/current/board-change-proof.json for allowed board differences and STEP1_SHA256.json for native-file hashes. No geometry change to the original 100 mm outline or motor terminals was made.

The native KiCad editor was opened on this Rev B project to inspect the footprint warning. There is no live IPC connection: external file edits require reload.

## Limits

These are configured checks; the inherited ignored categories remain visible in the JSON report. No new checks were disabled. The inherited J1-only 0.19 mm hole-clearance rule still needs fabricator acceptance. A clean footprint-library comparison does not establish agreement with the module manufacturer's land pattern. Current thermal, power-transient, sourcing, mechanical and firmware qualification is still pending.

KiCad documents the native comparison workflow in its [PCB Editor manual](https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html). This review used the installed editor's comparison result and native files, not an assumption that exporting a footprint makes it equivalent.
''')
(eng/'UNRESOLVED.md').write_text('''# Open issues after step 1

The completed rule-check cleanup is not a fabrication release.

1. **Power/protection qualification:** finish exact package/land overlays, sense-return review, FET/shunt/connector temperature estimates and measurements, protection thresholds/delays/recovery, charger power-path behavior, regulator startup and motor braking overshoot. Existing AO3401A motor switching still needs thermal verification.
2. **Battery and probes:** select an exact 1S cell with verified current/charge ratings and dimensions; qualify connector/harness. Four amperes continuous / five amperes peak remains a conservative design target, not measured rover consumption. Confirm the cell's allowed charging temperature window against BQ24074 TS behavior. Two independently insulated probes must be bonded to the cell and strain-relieved.
3. **PCB layout beyond DRC:** inspect inherited In1.Cu M2_A motor route and return continuity, shunt pickup, shared power trunks/vias, switching loops, effective capacitance, USB/camera signal integrity and thermal spreading. Confirm fabrication support for J1's local hole-clearance exception.
4. **Mechanical fit:** measure motor terminals/height, shaft engagement, wheel/coupling envelope, battery and camera assembly. Validate clamps carry loads, backside cover clearance and camera field of view. Printed support sources remain provisional.
5. **Firmware and Vita:** implement and test default-off driving, fault/temperature/battery monitoring, link-loss stopping, acceleration limiting, motor signs and wheel order. Verify Vita networking/video decoding before selecting a final streaming protocol. No built firmware is delivered by step 1.
6. **Bench qualification:** staged power-up, faults, USB motor disable, thermal runs, braking transients, concurrent camera/motor loads and carpet trials. No physical tests have been performed.
''')
(eng/'AUDIT.md').write_text('''# Current engineering audit — Rev B

Read STEP_1_REVIEW.md for the completed November 5 cleanup and UNRESOLVED.md for remaining gates. The prior Rev A audit is preserved at history/Rev_A_AUDIT.md and is historical where Rev B conflicts.

Rev B replaces the assumption of external-only protection with onboard BQ298217RUGR, common-drain CSD17308Q3 Q7/Q8, WSL2512R0100FEA 10 mΩ R36 and support components. It adds J5 plus R42/R43/C25 for an independent cell-temperature ADC input. J4 remains the charger's independent cell probe. Both TH1 and TH2 are off-board cell-bonded 103AT-2 sensors. GPIO1 becomes CELL_TEMP_ADC and GPIO43 becomes LED_STATUS.

The protection's nominal overcurrent disconnect is approximately 60 mV / 10 mΩ = 6 A, not a regulated current limit. This threshold does not qualify the cell or connector for that current. Detailed electrical/thermal review and bench qualification remain open. Do not treat the emergency undervoltage cutoff as the normal firmware stopping threshold.

Charging and motor paths differ: protected VBAT feeds the motor switch directly and also the charger BAT pins. Charger OUT/SYS_RAW feeds logic regulation. Motor-current qualification cannot be inferred from the charger's approximately 249 mA charging setting.

Rule checks currently pass with zero violations; no thermal, transient, physical-fit, carpet or firmware claim follows from that result. Native schematic and PCB are authoritative over older notes.
''')
(root/'CHANGELOG.md').write_text('''# Change log

## 2026-11-05 — Rev B step 1

- Reorganized seven native schematic pages with functional grouping and visible local wiring; repaired label direction, clipped notes and root-sheet placement.
- Preserved 111 component identities, 96 net names and all 365 pin memberships against the pre-cleanup XML baseline; ERC remains 0.
- Moved R42 0.2 mm left to fix two clearance errors; no trace/via edits.
- Corrected U1 library keepout from absolute board coordinates to footprint-local coordinates and made footprint keepout explicitly cover all four copper layers. No pad or module placement changes.
- Native DRC: 0 errors, 0 warnings, 0 opens, 0 parity issues. No warning exclusions added.
- Refreshed schematic PDF, previews, pin map, validation records and open-issue list. Fabrication release remains blocked by engineering qualification.

## Earlier Rev B work

Added onboard BQ298217 protection, two CSD17308Q3 FETs, 10 mΩ shunt, supporting components and second cell-probe interface. GPIO1 now measures cell temperature; status LED moved to GPIO43. See current schematic/BOM and historical construction notes. Original ZIP and Rev A were preserved.
''')
print('Updated project notes, pin map, validation summary and presentation source.')
