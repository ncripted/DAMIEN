from pathlib import Path
s=Path('work/power-rev-d/calculate.py').read_text().replace('s[1]*.015','s[1]*.02').replace('v*(1+e*.015)','v*(1+e*.02)');s=s[:s.index('print(calc())')];exec(s);print(calc())
