from pathlib import Path
from math import cos,sin,radians
root=Path("outputs/rover/Omni_UGV_Rev_F_integration")
work=Path("work/rev-f-startup")
land="TI_RPW0010A"
def polygon(points,width):
    coords=" ".join(f"(xy {x:.6f} {y:.6f})" for x,y in points)
    return f"(gr_poly (pts {coords}) (width {width}) (fill yes))"
def rounded(w,h):
    return [(x+.05*cos(radians(a)),y+.05*sin(radians(a)))
            for x,y,start in [(w/2-.05,h/2-.05,0),(-w/2+.05,h/2-.05,90),
                              (-w/2+.05,-h/2+.05,180),(w/2-.05,-h/2+.05,270)]
            for a in range(start,start+91,15)]
p=[f'(footprint "{land}" (version 20241229) (generator "pcbnew") (layer "F.Cu") (attr smd) (descr "TI RPW0010A per 4225183/A; see LAYOUT_NOTES.md")',
   '(fp_text reference "REF**" (at 0 -2.15) (layer "F.SilkS") (effects (font (size .8 .8) (thickness .13))))',
   '(fp_text value "TI_RPW0010A" (at 0 2.15) (layer "F.Fab") (effects (font (size .8 .8) (thickness .13))))',
   '(fp_rect (start -1.45 -1.45) (end 1.45 1.45) (stroke (width .05) (type default)) (fill none) (layer "F.CrtYd"))',
   '(fp_rect (start -1 -1) (end 1 1) (stroke (width .1) (type default)) (fill none) (layer "F.Fab"))',
   '(fp_circle (center -1.38 -1.32) (end -1.48 -1.32) (stroke (width .1) (type default)) (fill solid) (layer "F.SilkS"))']
for n,x,y,sx,sy in [(1,-.725,-.875,1,1),(4,-.725,.875,1,-1),(7,.725,.875,-1,-1),(10,.725,-.875,-1,1)]:
    for layer,edge,width in [('F.Cu" "F.Mask',-.425,.1),('F.Paste',-.406,.075)]:
        body=polygon(rounded(.25,.65),0)
        arm=polygon([(sx*a,sy*b) for a,b in [(edge,.275),(.075,.275),(.075,-.275),(-.075,-.275),(-.075,.075),(edge,.075)]],width)
        number=n if layer.startswith("F.Cu") else ""
        p.append(f'(pad "{number}" smd custom (at {x} {y}) (size .25 .25) (layers "{layer}") (options (clearance outline) (anchor circle)) (primitives {body} {arm}))')
for n,x,y in [(2,-.9,-.225),(3,-.9,.225),(8,.9,.225),(9,.9,-.225)]:
    p.append(f'(pad "{n}" smd roundrect (at {x} {y}) (size .6 .3) (layers "F.Cu" "F.Mask" "F.Paste") (roundrect_rratio .166667))')
for n,x in [(5,-.25),(6,.25)]:
    p.append(f'(pad "{n}" smd roundrect (at {x} 0) (size .3 2.4) (layers "F.Cu" "F.Mask") (roundrect_rratio .166667))')
    for y in [-.53,.53]:
        p.append(f'(pad "" smd roundrect (at {x} {y}) (size .28 1.06) (layers "F.Paste") (roundrect_rratio .178571))')
(root/"UGV.pretty"/f"{land}.kicad_mod").write_text("\n".join(p)+")\n")
