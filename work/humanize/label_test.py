from pathlib import Path
import uuid
s='(kicad_sch (version 20230121) (generator eeschema) (uuid '+str(uuid.uuid4())+') (paper "A4") (lib_symbols)'
for i,a in enumerate([0,90,180,270]):
 x=50+i*40;y=50
 s+=f'(global_label "ANGLE_{a}" (shape bidirectional) (at {x} {y} {a}) (effects (font (size 2 2)) (justify left bottom)) (uuid {uuid.uuid4()})) (junction (at {x} {y}) (diameter 1) (color 0 0 0 0) (uuid {uuid.uuid4()}))'
Path('work/humanize/label_test.kicad_sch').write_text(s+')')
