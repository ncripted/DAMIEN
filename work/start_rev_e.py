from pathlib import Path
import shutil,json,hashlib,re,sys
sys.path.insert(0,'work/humanize');from build import blocks
w=Path('work/rev-e');w.mkdir(exist_ok=True);src=Path('outputs/rover/Omni_UGV_Rev_D_power_audit');dst=src.parent/'Omni_UGV_Rev_E_power_layout';assert not dst.exists();shutil.copytree(src,dst,ignore=shutil.ignore_patterns('.validation-runtime','*.lck','*.kicad_prl'))
(w/'baseline-sha256.json').write_text(json.dumps({str(p.relative_to(src)):hashlib.sha256(p.read_bytes()).hexdigest() for p in src.rglob('*') if p.is_file() and '.validation-runtime' not in p.parts},indent=2));(w/'steps').mkdir(exist_ok=True)
fn=dst/'omni_ugv.kicad_pcb';s=fn.read_text();removed=[]
for a,b,t in reversed(list(blocks(s))):
 if t.startswith('(segment') and '(net "M2_A")' in t and '(layer "In1.Cu")' in t:removed.append(t);s=s[:a]+s[b:]
fn.write_text(s);(w/'step1-removed.json').write_text(json.dumps(removed,indent=2));print('Preserved Rev D; removed',len(removed),'In1 motor segments in Rev E')
for name in ['export_geometry.py','apply_routes.py']:
 s=Path('work/power-rev-d/'+name).read_text().replace('Omni_UGV_Rev_D_power_audit','Omni_UGV_Rev_E_power_layout').replace('work/power-rev-d','work/rev-e');(w/name).write_text(s)
s=Path('work/power-rev-d/route.py').read_text().split('errors=[]')[0].replace('work/power-rev-d','work/rev-e');(w/'router.py').write_text(s)
