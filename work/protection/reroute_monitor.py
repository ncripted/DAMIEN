from pathlib import Path
exec(Path('work/protection/route.py').read_text().split('\ntry:\n')[0])
rr('CELL_TEMP_DIV','R42',2,'R43',1)
rr('CELL_TEMP_DIV','R43',1,'J5',1)
rr('+3V3','R42',1,'R4',1)
save()
