// NOTE: since color does not render, you may wish to export to PNG from preview
// file units are nonexistent

// set viewport characteristics
$vpr = [66, 0, 141];
$vpt = [0, 0, 0.75];
$vpd = 32;

// shape of frame base polygon
vertices = [[0, 0], [1, 0], [3, 2], [6, 2], [8, 0], [9, 0], [9, 1], [7, 4], [7, 7], [9, 10], [9, 11], [8, 11], [6, 9], [3, 9], [1, 11], [0, 11], [0, 10], [2, 7], [2, 4], [0, 1]];

// segment length resolution for arcs
$fs = 0.1;

// colors
plate_color = [1, 1, 1];  // white
tube_color = [0.97, 0.82, 0.60];  // orange
thruster_color = [0.60, 0.83, 0.97];  // blue

// some design parameters (but not all)
plate_thickness = 0.5;
tube_rad = 1.5;
tube_len = 8;
thruster_rad = 1.1;
thruster_len = 2;
shift_x = -4.5;  // half of plate width
shift_y = -5.5;  // half of plate length

// frame plate bottom
color(plate_color)
  translate([shift_x, shift_y, 0])
    linear_extrude(height=plate_thickness)
      polygon(vertices);

// tube
color(tube_color) {
  translate([0, 0, plate_thickness + tube_rad])
    rotate([90, 90, 0])
      cylinder(h=tube_len, r1=tube_rad, r2=tube_rad, center=true);
  translate([0, 0.5 * tube_len, plate_thickness + tube_rad])
    sphere(r=tube_rad);
}

// frame plate top
color(plate_color)
  translate([shift_x, shift_y, plate_thickness + 2 * tube_rad])
    linear_extrude(height=plate_thickness)
      polygon(vertices);

// horiztonal thrusters
for (coords = [[1, 1, -45], [8, 1, 45], [8, 10, -45], [1, 10, 45]]) {
  color(thruster_color)
    translate([coords[0] + shift_x, coords[1] + shift_y, thruster_rad + plate_thickness])
      rotate([0, 90, coords[2]])
        cylinder(h=thruster_len, r1=thruster_rad, r2=thruster_rad, center=true);
}

// vertical thrusters
target = 0.2;  // offset from top
for (x = [2.5 + thruster_rad, -(2.5 + thruster_rad)]) {
  color(thruster_color)
    translate([x, 0, 2 * plate_thickness + 2 * tube_rad + target - 0.5 * thruster_len])
      cylinder(h=thruster_len, r1=thruster_rad, r2=thruster_rad, center=true);
}
