# (c) 2019 Stefan Katerkamp
# LGPL: This file is part of the Bit Socket Holder Workbench for FreeCAD

__title__="bsh utils"
__author__="katerkamp"
__url__="github.com/katerkamp/FreeCAD/BitSocketHolder"
__license__="LGPL 3"

import math, FreeCAD, FreeCADGui
from os.path import join, dirname, abspath, basename, exists

def polar2xy(ro,teta):
  'arg1=ro1(length), arg2=teta(deg): returns [x,y,0]'
  return ro*math.cos(teta),ro*math.sin(teta),0


def getFont(props):
  fontdir = FreeCAD.getResourceDir() + "Mod/TechDraw/Resources/fonts/" #"/usr/share/fonts/truetype/dejavu/"
  font = "osifont-lgpl3fe.ttf" # "DejaVuSans-Bold.ttf"

  if not props.ttfFontPath is None:
    if exists(props.ttfFontPath):
      font = basename(props.ttfFontPath)
      fontdir = join(dirname(props.ttfFontPath), '') # Part.makeWireString wants trailing slash
    else:
      print("No Font found at path in TrayProps: " + props.ttfFontPath)

  return fontdir, font

