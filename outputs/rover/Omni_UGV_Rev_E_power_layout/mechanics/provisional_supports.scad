// PROVISIONAL FIT STUDY — dimensions in mm. Not validated for assembly.
// Select a part, render with F6, export STL after measured fit approval.
part = "motor_clamp"; // motor_clamp, battery_cradle, camera_bracket
$fn=64;
fit=0.3;
motor_width=12; motor_height=10; // motor roll orientation must be measured
clamp_axial_length=9;
clamp_hole_pitch=20; // actual PCB paired M2 holes, tangential spacing
motor_center_above_pcb=5; // provisional: terminal height is NOT established
pcb_thickness=1.6;
bolt_clearance=2.3;
battery=[62,34,6]; // ASSUMED PHB1S100020CJST envelope; measure actual 20C pack
battery_side_clearance=1; // each side; includes liner/fit allowance
battery_top_allowance=2; // retain free height; straps must not compress pouch
tray_inside=[battery[0]+2*battery_side_clearance,battery[1]+2*battery_side_clearance,battery[2]+battery_top_allowance];
wall=1.6; floor=1.6;
camera_board=[32,32,2]; // PLACEHOLDER: measure exact Waveshare PCB
camera_lens_diameter=14; // PLACEHOLDER: measure optical barrel

module motor_clamp(){
 // Saddle centered at radius 34 mm; ears align with existing PCB holes.
 // M2 through-bolts with washers and metal nuts below PCB; length selected
 // after motor vertical datum is measured. No reliance on solder for load.
 difference(){
  union(){
   translate([-clamp_axial_length/2,-14,0])cube([clamp_axial_length,28,2.4]);
   translate([-clamp_axial_length/2,-(motor_width/2+wall+fit),0])
    cube([clamp_axial_length,motor_width+2*(wall+fit),motor_center_above_pcb+motor_height/2+wall]);
  }
  translate([-clamp_axial_length,-(motor_width+fit)/2,-.01])
   cube([2*clamp_axial_length,motor_width+fit,motor_center_above_pcb+motor_height/2+fit]);
  for(y=[-clamp_hole_pitch/2,clamp_hole_pitch/2])
   translate([0,y,-.1])cylinder(h=20,d=bolt_clearance);
 }
}
module battery_cradle(){
 // Bottom tray with open ends, soft liner and two hook-and-loop straps.
 // Floating study: attachment to accessory holes is not yet collision checked.
 difference(){
  union(){
   cube([tray_inside[0]+2*wall,tray_inside[1]+2*wall,floor]);
   for(y=[0,tray_inside[1]+wall])translate([0,y,0])
    cube([tray_inside[0]+2*wall,wall,6]);
  }
  for(x=[10,tray_inside[0]-6])for(y=[3,tray_inside[1]-1])
   translate([x,y,-.1])cube([6,2.5,floor+.2]);
 }
}
module camera_bracket(){
 // Slotted universal backplate. M2 standoffs require actual hole pattern.
 // Lens window is a clearance study, not a verified field-of-view aperture.
 difference(){
  union(){cube([40,16,2.4]);translate([0,13.6,0])cube([40,2.4,40]);}
  for(x=[7,33])hull(){
   translate([x,5,-.1])cylinder(h=3,d=bolt_clearance);
   translate([x,10,-.1])cylinder(h=3,d=bolt_clearance);
  }
  translate([20,17,23])rotate([90,0,0])cylinder(h=5,d=camera_lens_diameter+2);
  for(x=[6,34])for(z=[10,34])hull(){
   translate([x,17,z-2])rotate([90,0,0])cylinder(h=5,d=bolt_clearance);
   translate([x,17,z+2])rotate([90,0,0])cylinder(h=5,d=bolt_clearance);
  }
 }
}
if(part=="motor_clamp")motor_clamp();
else if(part=="battery_cradle")battery_cradle();
else if(part=="camera_bracket")camera_bracket();
