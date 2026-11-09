from pathlib import Path
p=Path('work/humanize/build.py');s=p.read_text().replace("kind='label' if local else 'global_label';shape='' if local else '(shape bidirectional)'","kind='global_label';shape='(shape bidirectional)'")
s=s.replace("('SW1',47,70,90)","('SW1',47,70,270)").replace("('SW2',30,130,90)","('SW2',30,130,270)")
s=s.replace("(vcp,2),[(50,64+base)]","(vcp,1),[(55,64+base),(55,35+base),(50,35+base)]")
s=s.replace("('R17',80,145,0)","('R17',45,145,0)").replace("('C16',1)],rail=137)","('C16',1)],rail=145)")
s=s.replace("s.link('MOTOR_MID',('Q1',2),('Q2',2),[(132,70),(173,70)])","s.link('MOTOR_MID',('Q1',2),('Q2',2),[(132,65),(165,65),(165,45),(173,45)])")
s=s.replace("s.join('GND',[('J5',2),('TH2',2),('C25',2)],rail=200)","s.join('GND',[('TH2',2),('C25',2)],rail=200)")
p.write_text(s)
