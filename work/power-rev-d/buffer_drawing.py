from pathlib import Path
p=Path('work/power-rev-d/functional_drawings.py');s=p.read_text().replace("('U10',50,65,0)","('U14',80,140,0),('R64',30,140,0),('C37',55,160,0),('U10',50,65,0)");s=s.replace("s.text('Raw-cell voltage sensing'","s.join('DRIVE_REQ_RAW',[('U14',2),('R64',1)],axis='v',rail=60)\ns.text('Buffered drive request; R64 defaults low',20,120)\ns.text('Raw-cell voltage sensing'")
p.write_text(s)
p=Path('work/power-rev-d/header_clearance.py');s=p.read_text().replace("'U12','U13','Q9'","'U12','U13','U14','Q9'").replace("'Q10','Q11']","'Q10','Q11','U14']");p.write_text(s)
