from pathlib import Path
import json,sys,re
sys.path.insert(0,'work/humanize');import build as h
r=Path('outputs/rover/Omni_UGV_Rev_E_power_layout');data=json.loads((r/'design_connections.json').read_text());dm={d['ref']:d for d in data}
for n in ['1','2','3']:dm['Q7']['nets'][n]='CELL_P';dm['Q8']['nets'][n]='PROTECTED_RAW';dm['Q13']['nets'][n]='PROTECTED_RAW'
dm['Q13']['nets']['5']='VBAT';dm['R40']['nets']['2']='CELL_P';dm['R41']['nets']['2']='PROTECTED_RAW';dm['R39']['nets']['1']='PROTECTED_RAW'
(r/'design_connections.json').write_text(json.dumps(data,indent=2))
h.ROOT=r;h.BASE=r;h.data=dm;h.data.update(TH1={'nets':{'1':'CELL_CHG_TEMP','2':'GND'}},TH2={'nets':{'1':'CELL_TEMP_DIV','2':'GND'}})
src=Path('work/rev-e/step3_schematic.py').read_text();a=src.index("sh=h.Sheet('battery_protection'");b=src.index('# Ground-side sense reference',a);exec(src[a:b])
sh=h.Sheet('discharge_cutoff','Discharge cutoff with charge recovery')
for ref,x,y,a in [('Q12',110,65,0),('Q13',190,65,0),('R65',65,65,90),('R66',90,35,0),('R67',150,105,0)]:sh.place(ref,x,y,a)
sh.covered.update([('Q13','2'),('Q13','3')])
sh.join('CUT_PNP_B',[('R65',2),('R66',2),('Q12',1)],axis='v',rail=90)
sh.join('CELL_P',[('Q12',2),('R66',1)],rail=25)
sh.join('CUT_GATE',[('Q12',3),('Q13',4),('R67',1)],rail=90)
sh.text('Discharge: CELL_P -> Q7/Q8 -> PROTECTED_RAW -> Q13 -> VBAT',20,145)
sh.text('U10 RESET_N low turns Q12 on; Q13 gate rises to raw CELL_P and blocks discharge.\nStatic trip window 3.0535..3.1465 V; recovery approximately 3.3 V. Verify dip response on a cell simulator.\nQ13 body diode points VBAT -> PROTECTED_RAW, permitting recovery charging while discharge is off.\nQ13 MUST be downstream of Q7/Q8: lifting Q7 source could exceed its gate-source rating at startup.\nU7 BAT/VDD still monitor raw cell; PACK and R41 connect to PROTECTED_RAW before Q13.\nBQ24074 and independent cell-mounted TH1 window still control charging; U7 protection stays in series.\nU7 cold-start/charger-wake compatibility remains a separate fabrication blocker. This is not a storage disconnect.',20,170)
sh.finish()
for p in r.glob('*.kicad_sch'):p.write_text(p.read_text().replace('B - prototype','E - prototype'))
print('Cutoff placed downstream of the primary protector; primary FET gate-source reference retained')
