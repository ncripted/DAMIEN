import pcbnew as p
b=p.LoadBoard('outputs/rover/Omni_UGV_Rev_D_power_audit/omni_ugv.kicad_pcb')
f=next(x for x in b.GetFootprints() if x.GetReference()=='H6')
print([a for a in dir(f) if 'Courtyard' in a or 'Bounding' in a]);print(f.GetBoundingBox(False,False))
try:print(f.GetCourtyard(p.F_Cu).OutlineCount())
except Exception as e:print(e)
