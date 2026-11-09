from pathlib import Path
p=Path('work/protection/route.py');s=p.read_text();a=s.index(' # Power source pins');z=s.index(' # Reserve radial escapes')
s=s[:a]+" if '--signals' not in sys.argv:\n"+''.join(' '+l+'\n' for l in s[a:z].splitlines())+" if '--initial' in sys.argv:\n  save();sys.exit(0)\n"+s[z:]
p.write_text(s)
