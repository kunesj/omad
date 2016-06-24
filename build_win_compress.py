#!/usr/bin/env python3
# encoding: utf-8

import os, zipfile, sys

VARSION = str(sys.argv[1])
ARCH = (sys.argv[2])

zf = zipfile.ZipFile("omad_"+VARSION+"_Win_"+ARCH+".zip", "w")
for dirname, subdirs, files in os.walk("dist"):
    zf.write(dirname)
    for filename in files:
        zf.write(os.path.join(dirname, filename))
zf.close()
