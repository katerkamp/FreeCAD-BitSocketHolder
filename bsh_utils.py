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


def markHolderRecompute(mark):
  if (not mark):
    return
  print("Marking all SocketHolders to recompute")
  for obj in FreeCAD.activeDocument().Objects:
    objGui = FreeCAD.activeDocument().getObject(obj.Name)
    if hasattr (objGui, "BSHType") and objGui.BSHType == "Holder":
      objGui.touch()


# todo: special chars like umlauts
def makeTag(props, tagString, slotWidth):
  import Part
  fontdir, font = getFont(props)
  string = Part.makeWireString(tagString,fontdir, font, props.tagTextSize, 0)
  tag = Part.Compound([Part.Face(c) for c in string])
  tag = tag.extrude(FreeCAD.Vector(0,0,props.tagTextHeight))
  tag.translate(FreeCAD.Vector((slotWidth - tag.BoundBox.XLength)/2,props.marginBottom,0))
  return tag


def getSlotSize(props, toolWidth, toolHeight, toolDepth):
  # see what sizes already exist
  # calculate tray insert height (y direction)
  # calculate tray insert depth
  maxY = 0 # depends on hole diameter
  maxZ = 0 # depends on hole depth
  for obj in FreeCAD.activeDocument().Objects:
    objGui = FreeCAD.activeDocument().getObject(obj.Name)
    if hasattr (objGui, "BSHType") and objGui.BSHType == "Holder":
      print(objGui.Name + " " + objGui.Label + " dia:" + str(objGui.Diameter) + " height:" + str(objGui.Shape.BoundBox.YLength))
      if objGui.Shape.BoundBox.YLength == float("-inf"):
          continue # thats our self
      if maxY < objGui.Shape.BoundBox.YLength:
        maxY = objGui.Shape.BoundBox.YLength
      if objGui.Tag:
          ZLengthNoText = objGui.Shape.BoundBox.ZLength - props.tagTextHeight
      else:
          ZLengthNoText = objGui.Shape.BoundBox.ZLength
      if maxZ < ZLengthNoText:
        maxZ = ZLengthNoText

  trayHeight = math.ceil(toolHeight + props.marginTop + props.marginBottom + props.marginMiddle + props.tagTextSize)
  slotWidth = math.ceil(toolWidth + 2 * props.marginTop) # todo use marginLeftRight
  trayDepth = toolDepth + props.magHoleDepth + props.basePlateThickness

  isRecomputeNeeded = False
  if trayDepth > maxZ:
    isRecomputeNeeded = True
  else:
    trayDepth = maxZ
  if trayHeight > maxY:
    isRecomputeNeeded = True
  else:
    trayHeight = maxY

  print("Tray Insert Block Size: w" + str(slotWidth) + " h" + str(trayHeight) + " d" + str(trayDepth))

  return isRecomputeNeeded, slotWidth, trayHeight, trayDepth

  
