from pathlib import Path
p=Path('work/rev-e/step5_sources.py');s=p.read_text();s=s.replace("p=r/'UGV.kicad_sym';p.write_text(p.read_text().rstrip()[:-1]+sym+')')","p=r/'UGV.kicad_sym'\nif '(symbol \"PFET_3333\"' not in p.read_text():p.write_text(p.read_text().rstrip()[:-1]+sym+')')")
s=s.replace(";sid=uid()",";sid=next(re.search(r'\\(uuid \"?([0-9a-f-]+)',t)[1] for a,b,t in h.blocks(top) if t.startswith('(sheet') and 'discharge_cutoff.kicad_sch' in t)")
s=s.replace("(r/'omni_ugv.kicad_sch').write_text(top)","# Root sheet was already created by the first run.")
s=s.replace("('R66',110,35,90)","('R66',90,35,0)")
p.write_text(s)
