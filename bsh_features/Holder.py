# (c) 2019 Stefan Katerkamp
# LGPL: This file is part of the Bit Socket Holder Workbench for FreeCAD

__title__="Bit/Socket Holder objects"
__author__="katerkamp"
__url__="github.com/katerkamp/FreeCAD/BitSocketHolder"
__license__="LGPL 3"
objs=['SocketHolder', 'BitHolder', 'AnyHolder']

import FreeCAD, FreeCADGui, Part, bsh_cmd, bsh_utils

vO=FreeCAD.Vector(0,0,0)
vX=FreeCAD.Vector(1,0,0)
vY=FreeCAD.Vector(0,1,0)
vZ=FreeCAD.Vector(0,0,1)


class Holder(object):
  def __init__(self,obj):
    print("Init holder Type")
    obj.Proxy = self
    obj.addProperty("App::PropertyString","BSHType","BSH","BSH Type").BSHType
    obj.addProperty("App::PropertyString","Tag","Base","Tag name").Tag
    obj.addProperty("App::PropertyFloat","Diameter","Base","Real mesured diameter").Diameter
    obj.addProperty("App::PropertyFloat","Depth","Base","Depth of cutout").Depth
    obj.addProperty("App::PropertyInteger","PosLR","Base","Position Index left to right").PosLR
    obj.addProperty("App::PropertyInteger","PosFB","Base","Position Index fron to back").PosFB
    obj.addProperty("App::PropertyBool","CutoutObject","Base","Create Cutout Object").CutoutObject
    obj.addProperty("App::PropertyBool","TagObject","Base","Create Tagstring Object").TagObject
    obj.addExtension("Part::AttachExtensionPython",obj)
    self.Name=obj.Name
  def execute(self, fp):
    fp.positionBySupport() # todo recompute placement according the Support
