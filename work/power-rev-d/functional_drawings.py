from pathlib import Path
import sys,json,re
sys.path.insert(0,'work/humanize');import build as h
r=Path('outputs/rover/Omni_UGV_Rev_D_power_audit');h.ROOT=r;h.BASE=r
h.data={d['ref']:d for d in json.loads((r/'design_connections.json').read_text())}
s=h.Sheet('cell_undervoltage','Independent cell undervoltage shutdown')
for ref,x,y,a in [('U14',80,140,0),('R64',30,140,0),('C37',55,160,0),('U10',50,65,0),('C30',20,65,0),('C31',80,90,0),('R46',95,45,0),('R47',115,63,90),('Q9',145,63,0),('R48',130,40,0),('R49',175,95,0),('R50',200,63,90),('Q10',235,63,0),('R51',225,95,0),('R52',200,130,90),('Q11',235,130,0),('R53',225,160,0),('R54',280,63,90)]:s.place(ref,x,y,a)
s.join('CELL_P',[('U10',2),('U10',4),('C30',1)],axis='v',rail=30)
s.join('CELL_UV_RESET_N',[('U10',1),('R46',2),('R47',1)],rail=55)
s.link('CELL_UV_CT',('U10',5),('C31',1),[(80,67)])
s.join('CELL_UV_PNP_B',[('R47',2),('R48',2),('Q9',1)],rail=63)
s.join('CELL_UV_FAULT',[('Q9',3),('R49',1),('R50',1),('R52',1)],axis='v',rail=180)
s.join('CELL_UV_EN_B',[('R50',2),('Q10',1),('R51',1)],rail=63)
s.join('CELL_UV_MOTOR_B',[('R52',2),('Q11',1),('R53',1)],rail=130)
s.join('SYS_ON',[('Q10',3),('R54',2)],rail=80)
s.join('DRIVE_REQ_RAW',[('U14',2),('R64',1)],axis='v',rail=60)
s.text('Buffered drive request; R64 defaults low',20,120)
s.text('Raw-cell voltage sensing',15,30)
s.text('Protected-rail inverter',105,25)
s.text('Regulator enable inhibit',215,30)
s.text('Motor / nSLEEP inhibit',210,110)
s.text('3.1 V nominal falling cutoff; approximately 3.3 V recovery. CT delays release, not fault assertion.\nQ9 and pullups use protected VBAT: only the nanopower supervisor remains on raw CELL_P after U7 cutoff.\nCharging is independent of SYS_ON, so USB can recover a discharged cell while ESP32/camera stay off.\nU7 retains its factory 2.6 V emergency cutoff. Firmware should stop normally before this hardware trip.',20,190)
s.finish()
s=h.Sheet('charge_temperature','Independent cell temperature charging window')
for ref,x,y,a in [('U11',45,50,0),('C32',20,72,0),('C33',65,70,0),('R55',115,55,0),('R56',105,90,0),('R57',105,115,0),('R58',75,90,0),('R59',75,115,0),('U12',205,102,0),('C34',205,145,0),('R62',235,100,90),('R61',250,75,0),('C35',250,125,0),('U13',265,102,0),('C36',290,145,0),('R63',295,80,0),('R60',45,130,0)]:s.place(ref,x,y,a)
s.join('USB_5V',[('U11',1),('U11',3)],axis='v',rail=25)
s.link('CHG_3V3',('U11',5),('C33',1),[(65,48)])
s.join('CELL_CHG_TEMP',[('R55',2),('R56',1),('R58',1)],rail=75)
s.join('CHG_HOT_SENSE',[('R56',2),('R57',1),('U12',3)],rail=100)
s.link('CHG_COLD_SENSE',('R58',2),('R59',1))
s.link('CHG_COLD_SENSE',('R58',2),('U12',4),[(85,93),(85,130),(185,130),(185,104)])
s.join('CHG_TEMP_OK_OD',[('U12',1),('U12',6),('R62',1)],axis='v',rail=220)
s.join('CHG_TEMP_ALLOW_RC',[('R62',2),('R61',2),('C35',1),('U13',2)],axis='v',rail=250)
s.link('CHG_DISABLE',('U13',4),('R63',2),[(295,102)])
s.text('USB-powered reference supply',15,30)
s.text('TH1 at J4: actual cell temperature',90,30)
s.text('Hot / cold comparison and fail-disabled enable',180,45)
s.text('Fixed BQ TS bias',20,110)
s.text('TH1 is an electrically insulated OFF-BOARD 103AT-2, bonded to the cell. Open/short probe disables charging.\nU12 open-drain outputs both release only within the temperature window. U13 then drives CE low.\nR61/C35 delay charge enable at USB startup; R62 limits capacitor discharge into U12. No ESP32 dependency.\nR60 intentionally replaces the direct TS thermistor. This independent circuit now decides cell charge temperature.\nTolerance calculation uses the NTC beta model: verify actual resistance-temperature curve and trip limits on a fixture.',20,180)
s.finish()
# Keep vertical terminal labels horizontal and clear of values; preserve every pin membership.
for fn in ['cell_undervoltage.kicad_sch','charge_temperature.kicad_sch']:
 p=r/fn;t=p.read_text().replace('B - prototype','D - prototype')
 for a,b,u in reversed(list(h.blocks(t))):
  if u.startswith('(global_label'):
   m=re.search(r'\(at ([^ ]+) ([^ ]+) ([^)]+)\)',u)
   if int(m[3]) in [90,270]:u=u[:m.start()]+f'(at {m[1]} {m[2]} 0)'+u[m.end():];u=u.replace('(justify right bottom)','(justify left bottom)')
   t=t[:a]+u+t[b:]
 p.write_text(t)
print('Built connected functional diagrams without changing pin assignments')

