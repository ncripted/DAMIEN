from pathlib import Path
import pcbnew as p
root=Path('outputs/rover/Omni_UGV_Rev_B_protection')
b=p.LoadBoard(str(root/'omni_ugv.kicad_pcb'));f=next(f for f in b.GetFootprints() if f.GetReference()=='U1');g=p.FootprintLoad(str((root/'UGV.pretty').resolve()),'RF_Module__ESP32-S3-WROOM-1')
print('similarity',f.Similarity(g)); f.NormalizeForCompare();g.NormalizeForCompare();print('normalized',f.Similarity(g))
for label,h in [('board',f),('lib',g)]:
 out=Path('work/humanize')/(label+'.pretty');out.mkdir(exist_ok=True)
 p.PCB_IO_MGR.FindPlugin(p.PCB_IO_MGR.KICAD_SEXP).FootprintSave(str(out.resolve()),h)
 print(label,'pads',len(list(h.Pads())),'zones',len(list(h.Zones())))
 for z in h.Zones(): print('zone layers',z.GetLayerSet().FmtHex(),'prio',z.GetAssignedPriority(),'keepout',z.GetIsRuleArea())
