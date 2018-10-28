#!/bin/bash

# set the file name
FNAME='rogue2019'

# this compiles the documentation
echo 'BUILD.SH: welcome! i will dutifully compile your documentation'
echo '          if you like, you can run TeX in --verbose mode'

# check for --verbose flag (yes, this is sloppy)
function compile()
{
  if [ "$1" == '--verbose' ]
  then
    xelatex "$FNAME.tex"
  else
    xelatex -interaction=batchmode "$FNAME.tex"
  fi
}

echo 'BUILD.SH: compiling for first time'
compile $1
echo 'BUILD.SH: recompiling for references'
compile $1
echo 'BUILD.SH: merging cover page with documentation body'
#gs -q -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -sOutputFile=RogueRobotics_RogueUnderwaterSolutions_TechnicalDocumentation_2019.pdf "$FNAME-cover.pdf" "$FNAME.pdf"
echo 'BUILD.SH: done'
