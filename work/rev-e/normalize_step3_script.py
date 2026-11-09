from pathlib import Path
p=Path('work/rev-e/step3_schematic.py');s=p.read_text().replace("p.write_text(s)\n# Rebuild", "p.write_text(s.replace('(symbol\\n','(symbol '))\n# Rebuild");p.write_text(s)
