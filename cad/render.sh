#!/bin/bash

# creates "nice" pngs for all openscad files
# you may want to customize for each file
# you will obviously need openscad installed

for source_file in *.scad; do
  echo "rendering $source_file"
  out_file=${source_file%.scad}.png
  openscad $source_file --render -o $out_file
done

