from pathlib import Path
p=Path('work/power-rev-d/package_revision.py');s=p.read_text();at="proof=json.loads((val/'power-board-proof.json').read_text());"
new="""def copper(s):return {re.search(r'\\(uuid \"?([0-9a-f-]+)',t)[1]:t for a,b,t in blocks(s) if t.startswith(('(segment','(via'))}
+c0,c1=[copper((p/'omni_ugv.kicad_pcb').read_text()) for p in [base,r]]
+assert not [k for k in c0.keys()&c1.keys() if re.sub(r'\\s+','',c0[k])!=re.sub(r'\\s+','',c1[k])]
+proof=json.loads((val/'power-board-proof.json').read_text());proof['removed_copper_uuids']=sorted(c0.keys()-c1.keys());proof['added_copper_uuids']=sorted(c1.keys()-c0.keys());proof['new_In1_tracks']=[k for k in c1.keys()-c0.keys() if c1[k].startswith('(segment') and '(layer \"In1.Cu\")' in c1[k]];assert not proof['new_In1_tracks'];""".replace('\n+','\n')
s=s.replace(at,new);p.write_text(s)
