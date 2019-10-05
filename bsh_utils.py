#!/usr/bin/env python
# -*- coding: utf8 -*-

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


# make a 3D version of a String
def makeTag(props, tagString, slotWidth):
  import Part
  fontdir, font = getFont(props)

  # test: tagS=Part.makeWireString("34öäüZB", "/usr/share/fonts/truetype/dejavu/", "DejaVuSans-Bold.ttf", 6.0, 0)
  tagS = Part.makeWireString(unicode(tagString),fontdir, font, props.tagTextSize, 0)

  # Draft causes problems with GUI
  #tagShapeString = Draft.makeShapeString(String=unicode(tagString),\
  #  FontFile=join(fontdir,font),Size=props.tagTextSize,Tracking=0) 
  #tag=tagShapeString.Shape.extrude(FreeCAD.Vector(0,0,props.tagTextHeight))
  #tagF = [Part.Face(c) for c in tagS] # does not work for multi wire chars like "4", so I do this:

  tagF = []
  tagFcuts = []
  for c in tagS:
    for ci in c:
      if not isInside(ci, c):
        tagF.append(Part.Face(ci))
      else:
        tagFcuts.append(Part.Face(ci))
    
  tagC = Part.Compound(tagF)
  tagCcuts = Part.Compound(tagFcuts)
  tagC = tagC.cut(tagCcuts)

  tag = tagC.extrude(FreeCAD.Vector(0,0,props.tagTextHeight))

  tag.translate(FreeCAD.Vector((slotWidth - tag.BoundBox.XLength)/2,props.marginBottom,0))
  return tag

def isInside(wire, charWireList):
  import Part
  otherWires = []
  for w in charWireList:
    if wire != w:
      otherWires.append(w)
  for w in otherWires:
    f = Part.Face(w)
    for v in wire.Vertexes:
        p = v.Point
        if f.isInside(p,0.0,True):
          return True
  return False
  

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
  if maxZ > 0:
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

  

def addCutoutObject(fp, part, name):
  if not fp.CutoutObject:
    return
  pos = FreeCAD.Vector(0,0,0)
  Z = FreeCAD.Vector(0,0,1)
  a = FreeCAD.activeDocument().addObject('Part::Feature', name)
  a.Shape = part
  a.ViewObject.Visibility=False
  if fp.Tag:
    a.Label = name + "-" + fp.Tag.replace(' ','_')
  else:
    a.Label = name

