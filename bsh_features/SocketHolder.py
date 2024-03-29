# (c) 2019 Stefan Katerkamp
# LGPL: This file is part of the Bit Socket Holder Workbench for FreeCAD

__title__="Bit/Socket Holder objects"
__author__="katerkamp"
__url__="github.com/katerkamp/FreeCAD-BitSocketHolder"
__license__="LGPL 3"

import FreeCAD, FreeCADGui, Part, bsh_cmd, bsh_utils

vO=FreeCAD.Vector(0,0,0)
vX=FreeCAD.Vector(1,0,0)
vY=FreeCAD.Vector(0,1,0)
vZ=FreeCAD.Vector(0,0,1)

from Holder import Holder
from HolderProperties import HolderProperties

class SocketHolder(Holder):
  '''Class for object 
  SocketHolder(obj,[Tag="",Diameter="12", Depth=10])
    obj: the "App::FeaturePython" object
    Tag(string): Tag
    Diameter (float): Diam
    Depth (float): Depth'''

  def __init__(self, obj, Tag="",Diameter=12,Depth=10,CutoutObject=False,TagObject=True):
    # initialize the parent class
    super(SocketHolder,self).__init__(obj)
    # define common properties TODO take from TrayProps
    obj.BSHType="Holder" 
    obj.Tag=Tag.strip()
    obj.Diameter=Diameter
    obj.Depth=Depth
    obj.CutoutObject = CutoutObject
    obj.TagObject = TagObject
    self.Label = obj.Name + Tag.strip().replace(' ','_')
    # define specific properties
    #obj.addProperty("App::PropertyString","FooType","Foo","Type of flange").FooType="foobar"

  def onChanged(self, fp, prop):
    return None

  def execute(self, fp): # fp is FeaturePython
    import math
    props = HolderProperties().getProperties()

    socketHoleDiameter = fp.Diameter + (2 * props.cutoutIncrease)  # fp.Diameter is measured diameter of nut

    print("Create Cutout Object: " + str(fp.CutoutObject)) # todo

    # Create nut hole with 4 magholes
    base=Part.Face(Part.Wire(Part.makeCircle((socketHoleDiameter)/2)))
    socketHole = base.extrude(FreeCAD.Vector(0,0,-1 * fp.Depth))

    xy=(socketHoleDiameter/2 - props.magHoleDiameter/2 + props.magHoleOffset) * math.sin(math.radians(45))

    magHole1 = Part.makeCylinder(props.magHoleDiameter/2,props.magHoleDepth,FreeCAD.Vector(xy,xy,-fp.Depth),vZ*-1)
    magHole2 = Part.makeCylinder(props.magHoleDiameter/2,props.magHoleDepth,FreeCAD.Vector(-xy,xy,-fp.Depth),vZ*-1)
    magHole3 = Part.makeCylinder(props.magHoleDiameter/2,props.magHoleDepth,FreeCAD.Vector(xy,-xy,-fp.Depth),vZ*-1)
    magHole4 = Part.makeCylinder(props.magHoleDiameter/2,props.magHoleDepth,FreeCAD.Vector(-xy,-xy,-fp.Depth),vZ*-1)
    socketHole = socketHole.fuse(magHole1)
    socketHole = socketHole.fuse(magHole2)
    socketHole = socketHole.fuse(magHole3)
    socketHole = socketHole.fuse(magHole4)

    bsh_utils.addCutoutObject(fp, socketHole, 'SocketCutout')
    fp.CutoutWidth = socketHole.BoundBox.XLength
    fp.CutoutHeight = socketHole.BoundBox.YLength
    fp.CutoutDepth = socketHole.BoundBox.ZLength

    isRecomputeNeeded, slotWidth, trayHeight, trayDepth = bsh_utils.getSlotSize(props, fp)
    bsh_utils.markHolderRecompute(isRecomputeNeeded)

    socketHole.translate(FreeCAD.Vector(slotWidth/2, trayHeight - props.marginTop - socketHoleDiameter/2, 0))

    box = Part.makeBox(slotWidth, trayHeight, trayDepth, vO, FreeCAD.Vector(0,0,-1))
    box.translate(FreeCAD.Vector(slotWidth, 0, 0))
    #holder = box.fuse(socketHole)  # devel
    holder = box.cut(socketHole)

    tag = bsh_utils.makeTag(props, fp.Tag, slotWidth)
    holder = holder.fuse(tag)

    fp.Shape = holder
    super(SocketHolder,self).execute(fp) # perform common operations
    
