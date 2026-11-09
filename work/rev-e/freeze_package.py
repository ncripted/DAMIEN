from pathlib import Path
import json,hashlib,zipfile,shutil
r=Path('outputs/rover/Omni_UGV_Rev_E_power_layout');val=r/'validation/current'
# Store the final inspection record separately from automatic checks.
record=dict(revision='E',native_3D_views=['preview/board-top.png','preview/board-bottom.png'],copper_views='preview/copper-layer-overview.png',schematic_pages=11,visually_inspected=['root overview','four-terminal protection','operating undervoltage','discharge cutoff','motor driver sheet','top and bottom board','all four copper layers'],limitations=['Custom 3D bodies and offboard mechanical assembly are incomplete.','No physical fit, thermal, transient or RF test.','Source-pad vias require filled/copper-capped processing or layout change.'],fabrication_gate='BLOCKED')
(val/'visual-review.json').write_text(json.dumps(record,indent=2))
# Remove unrelated stale current reports inherited from Rev D; history retains them.
keep={'drc.json','erc.json','schematic.net.xml','preservation-and-layout-proof.json','electrical-delta.json','step2-width-accepted.json','final-width-changes.json','visual-review.json','steps'}
for p in list(val.iterdir()):
 if p.name not in keep and p.is_file():p.unlink()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def included(p):return p.is_file() and '.validation-runtime' not in p.parts and p.suffix not in ['.lck','.kicad_prl'] and p.name!='REV_E_SHA256.json'
files=sorted([p for p in r.rglob('*') if included(p)])
manifest={p.relative_to(r).as_posix():sha(p) for p in files};(r/'REV_E_SHA256.json').write_text(json.dumps(manifest,indent=2))
z=r.parent/'Omni_UGV_Rev_E_power_layout_review.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as out:
 for p in files+[r/'REV_E_SHA256.json']:out.write(p,arcname=(Path(r.name)/p.relative_to(r)).as_posix())
with zipfile.ZipFile(z) as f:
 assert f.testzip() is None
 for rel,h in manifest.items():assert hashlib.sha256(f.read(r.name+'/'+rel)).hexdigest()==h
print(json.dumps(dict(package=str(z.resolve()),files=len(files)+1,bytes=z.stat().st_size,zip_sha256=sha(z),manifest_files_verified=len(manifest)),indent=2))
Path('work/rev-e/delivery.json').write_text(json.dumps(dict(zip=str(z.resolve()),sha256=sha(z),files=len(files)+1),indent=2))
