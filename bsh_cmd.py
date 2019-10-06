# (c) 2019 Stefan Katerkamp
# LGPL: This file is part of the Bit Socket Holder Workbench for FreeCAD

__title__="bsh functions"
import FreeCAD, FreeCADGui, Part
from DraftVecUtils import rounded
from math import degrees
from bsh_features.SocketHolder import SocketHolder
from bsh_features.BitHolder import BitHolder
from bsh_features.Pad import Pad
from bsh_features.AnyHolder import AnyHolder
from HolderProperties import HolderProperties
import bsh_utils

__author__="skat"
__url__="github.com/katerkamp/ToolboxTrayOrganizer"
__license__="LGPL 3"
X=FreeCAD.Vector(1,0,0)
Y=FreeCAD.Vector(0,1,0)
Z=FreeCAD.Vector(0,0,1)


def makeSocketHolder(propList=[], pos=None, Z=None):
  '''Adds a SocketHolder object
  makeSocketHolder(propList,pos,Z);
    propList is one optional list with 8 elements:
    pos (vector): position of insertion; default = 0,0,0
    Z (vector): orientation: default = 0,0,1
  '''
  if pos==None:
    pos=FreeCAD.Vector(0,0,0)
  if Z==None:
    Z=FreeCAD.Vector(0,0,1)
  a=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","SocketHolder")
  SocketHolder(a,*propList)
  a.ViewObject.Proxy=0
  a.Placement.Base=pos
  rot=FreeCAD.Rotation(FreeCAD.Vector(0,0,1),Z)
  a.Placement.Rotation=rot.multiply(a.Placement.Rotation)
  return a

def makeBitHolder(propList=[], pos=None, Z=None):
  if pos==None:
    pos=FreeCAD.Vector(0,0,0)
  if Z==None:
    Z=FreeCAD.Vector(0,0,1)
  a=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","BitHolder")
  BitHolder(a,*propList)
  a.ViewObject.Proxy=0
  a.Placement.Base=pos
  rot=FreeCAD.Rotation(FreeCAD.Vector(0,0,1),Z)
  a.Placement.Rotation=rot.multiply(a.Placement.Rotation)
  return a

def makePad(propList=[], pos=None, Z=None):
  if pos==None:
    pos=FreeCAD.Vector(0,0,0)
  if Z==None:
    Z=FreeCAD.Vector(0,0,1)
  a=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Pad")
  Pad(a,*propList)
  a.ViewObject.Proxy=0
  a.Placement.Base=pos
  #rot=FreeCAD.Rotation(FreeCAD.Vector(0,0,1),Z)
  #a.Placement.Rotation=rot.multiply(a.Placement.Rotation)
  return a

def makeAnyHolder(propList=[], pos=None, Z=None):
  if pos==None:
    pos=FreeCAD.Vector(0,0,0)
  if Z==None:
    Z=FreeCAD.Vector(0,0,1)
  a=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","AnyHolder")
  AnyHolder(a,*propList)
  a.ViewObject.Proxy=0
  a.Placement.Base=pos
  rot=FreeCAD.Rotation(FreeCAD.Vector(0,0,1),Z)
  a.Placement.Rotation=rot.multiply(a.Placement.Rotation)
  return a

def nearestPort (pypeObject,point):
  try:
    pos=portsPos(pypeObject)[0]; Z=portsDir(pypeObject)[0]
    i=nearest=0
    for p in portsPos(pypeObject)[1:] :
      i+=1
      if (p-point).Length<(pos-point).Length:
        pos=p
        Z=portsDir(pypeObject)[i]
        nearest=i
    return nearest, pos, Z
  except:
    return None

    
def join(obj1,port1,obj2,port2):
  '''
  join(obj1,port1,obj2,port2)
  \t obj1, obj2 = two "Pype" parts
  \t port1, port2 = their respective ports to join
  '''  
  if hasattr(obj1,'PType') and hasattr(obj2,'PType'):
    if port1>len(obj1.Ports)-1 or port2>len(obj2.Ports)-1:
      FreeCAD.Console.PrintError('Wrong port(s) number\n')
    else:
      v1=portsDir(obj1)[port1]
      v2=portsDir(obj2)[port2]
      rot=FreeCAD.Rotation(v2,v1.negative())
      obj2.Placement.Rotation=rot.multiply(obj2.Placement.Rotation)
      p1=portsPos(obj1)[port1]
      p2=portsPos(obj2)[port2]
      obj2.Placement.move(p1-p2)
  else:
    FreeCAD.Console.PrintError('Object(s) are not pypes\n')



# create closed poylgon
# add points which become magnet holes
def makeAnyShape():
  #todo prepend form and ask for tray slot tag
  FreeCADGui.activateWorkbench("SketcherWorkbench")
  sketch=FreeCAD.activeDocument().addObject('Sketcher::SketchObject','AnyShape')
  sketch.Placement = FreeCAD.Placement(FreeCAD.Vector(0.000000,0.000000,0.000000),FreeCAD.Rotation(0.000000,0.000000,0.000000,1.000000))
  FreeCAD.activeDocument().AnyShape.MapMode = "Deactivated"
  FreeCADGui.activeDocument().activeView().setCamera('#Inventor V2.1 ascii \n OrthographicCamera {\n viewportMapping ADJUST_CAMERA \n position 0 0 87 \n orientation 0 0 1  0 \n nearDistance -112.88701 \n farDistance 287.28702 \n aspectRatio 1 \n focalDistance 87 \n height 143.52005 }')
  FreeCADGui.activeDocument().setEdit('AnyShape')
  # todo wait for end of edit and then swicth to
  #FreeCADGui.activateWorkbench("ToolboxTray")
