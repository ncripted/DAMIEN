from pathlib import Path
import json,csv,shutil
r=Path('outputs/rover/Omni_UGV_Rev_E_power_layout');dm0=json.loads((r/'design_connections.json').read_text());dm={d['ref']:d for d in dm0}
notes={'U7':'Primary BQ298217: factory UV 2.6V; cold-start/wake compatibility open. CS/VSS use R36 voltage contacts. PACK senses PROTECTED_RAW before Q13.','Q7':'Primary charge FET: source CELL_P, common drain PROT_DRAIN.','Q8':'Primary discharge FET: source PROTECTED_RAW. Source pad1 intersects a through-via: filled/copper-capped processing or reroute required.','Q13':'Secondary discharge-only PFET: sources1-3 PROTECTED_RAW, merged drain5 represents physical5-8 and connects VBAT. Body diode permits charge recovery. Source pad1 via requires filled/capped processing or reroute.','Q12':'Raw-cell PNP inverter: U10 reset low raises Q13 gate to inhibit discharge.','R39':'U7 PACK sense from PROTECTED_RAW, upstream of secondary Q13.','R40':'Q7 gate-source bias to raw CELL_P.','R41':'Q8 gate-source bias to PROTECTED_RAW.','C24':'U7 VDD decoupling returns to PROT_VSS_SENSE, not the main GND plane.'}
for ref,note in notes.items():dm[ref]['note']=note
(r/'design_connections.json').write_text(json.dumps(dm0,indent=2))
with (r/'BOM.csv').open(newline='',encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))
for row in rows:
 if row['Reference'] in dm:
  d=dm[row['Reference']];row.update(Value=d['value'],MPN=d.get('mpn',row['MPN']),Notes=d.get('note',row['Notes']))
with (r/'BOM.csv').open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
roles=[]
for row in rows:
 ref=row['Reference'];d=dm.get(ref,{});roles.append(dict(Reference=ref,Value=row['Value'],Functional_block=d.get('group','Cell-mounted probe' if ref.startswith('TH') else 'Existing circuit'),Role=row['Notes'],Nets='; '.join(sorted({n for n in d.get('nets',{}).values() if n}))))
with (r/'engineering/COMPONENT_FUNCTIONS.csv').open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=roles[0]);w.writeheader();w.writerows(roles)
src=(r/'mechanics/Rev_D_board_only.step').resolve();dst=(r/'mechanics/history/Rev_D/Rev_D_board_only.step').resolve();assert src.is_relative_to(r.resolve()) and dst.is_relative_to(r.resolve())
if src.exists():dst.parent.mkdir(parents=True,exist_ok=True);shutil.move(str(src),str(dst))
p=r/'mechanics/README.md';p.write_text('# Rev E mechanical status\n\nRev_E_Bare_PCB.step is freshly exported from the saved Rev E board. The 100 mm outline and motor/mounting geometry are unchanged. This is a bare-board reference, not a complete robot assembly.\n\nprovisional_supports.scad remains editable preliminary fit geometry. It has not been qualified against measured motors, couplings, wheel rollers, battery or camera flex. Check clearance around new backside Q12/Q13 and the four-terminal R36 before using it. No final printable support set is released in this electrical-layout revision. Earlier board STEP exports are under history/.\n',encoding='utf-8')
print('Updated BOM function notes and mechanical artifact status')
