#!/bin/sh

pyinstaller topside.py
cp -r dist/topside built
rm -r dist
rm -r build
rm -r __pycache__
rm topside.spec
