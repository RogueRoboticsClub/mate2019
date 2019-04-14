// file units are mm
WALL_THICKNESS = 3;
DIAMETER_OFFSET = 1;
HOOK_DIAMETER = 16.5;
AXLE_DIAMETER = 6;
SCREW_DIAMETER = 3;
INFTY = 100;

union() {
  difference() {  // to hook piece
    inner = (HOOK_DIAMETER + DIAMETER_OFFSET) / 2;
    outer = inner + WALL_THICKNESS;
    screw = SCREW_DIAMETER / 2;

    cylinder(r1=outer, r2=outer, h=30, center=true);
    cylinder(r1=inner, r2=inner, h=30, center=true);
    rotate([0, 90, 0])
      cylinder(r1=screw, r2=screw, h=INFTY, center=true);
    translate([0, -INFTY / 2, 0])
      cube([INFTY, INFTY, INFTY], true);
  }
  rotate([0, 90, 0])  // to axle piece
    translate([0, (HOOK_DIAMETER + AXLE_DIAMETER) / 2 + WALL_THICKNESS + 1, 0])
    difference() {
      inner = (AXLE_DIAMETER + DIAMETER_OFFSET) / 2;
      outer = inner + WALL_THICKNESS;
      screw = SCREW_DIAMETER / 2;

      cylinder(r1=outer, r2=outer, h=30, center=true);
      cylinder(r1=inner, r2=inner, h=30, center=true);
      rotate([0, 90, 0])
        cylinder(r1=screw, r2=screw, h=INFTY, center=true);
    }
}