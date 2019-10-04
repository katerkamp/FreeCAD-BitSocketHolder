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

from Holder import Holder
from HolderProperties import HolderProperties
    
class BitHolder(Holder):
  def __init__(self, obj, Tag="",Diameter=12,Depth=10):
    # initialize the parent class
    super(BitHolder,self).__init__(obj)
    # define common properties TODO take from TrayProps
    obj.BSHType="Holder" 
    obj.Tag=Tag
    obj.Diameter=Diameter
    obj.Depth=Depth
    self.Label = obj.Name + Tag
    # define specific properties
    #obj.addProperty("App::PropertyString","FooType","Foo","Type of flange").FooType="foobar"
  def onChanged(self, fp, prop):
    return None
  def execute(self, fp): # fp is FeaturePython
    import math
    props = HolderProperties().getProperties()
    bitHoleDiameter = fp.Diameter + props.cutoutIncrease  # fp.Diameter is measured diameter of nut

    # Create nut hole with 4 magholes
    r=bitHoleDiameter/2
    s=0.8660254
    c=0.5
    p1 = FreeCAD.Vector(-r,0,0)
    p2 = FreeCAD.Vector(-r*c,r*s,0)
    p3 = FreeCAD.Vector(r*c,r*s,0)
    p4 = FreeCAD.Vector(r,0,0)
    p5 = FreeCAD.Vector(r*c,-r*s,0)
    p6 = FreeCAD.Vector(-r*c,-r*s,0)
    pointslist = [p1,p2,p3,p4,p5,p6,p1]
    base=Part.Face(Part.Wire(Part.makePolygon(pointslist)))
    bitHole = base.extrude(FreeCAD.Vector(0,0,-1 * fp.Depth))
    xy=(bitHoleDiameter/2 * 0.7071068) - props.magHoleDiameter/2 + props.magHoleOffset
    magHole1 = Part.makeCylinder(props.magHoleDiameter/2,props.magHoleDepth,FreeCAD.Vector(xy,xy,-fp.Depth),vZ*-1)
    magHole2 = Part.makeCylinder(props.magHoleDiameter/2,props.magHoleDepth,FreeCAD.Vector(-xy,xy,-fp.Depth),vZ*-1)
    magHole3 = Part.makeCylinder(props.magHoleDiameter/2,props.magHoleDepth,FreeCAD.Vector(xy,-xy,-fp.Depth),vZ*-1)
    magHole4 = Part.makeCylinder(props.magHoleDiameter/2,props.magHoleDepth,FreeCAD.Vector(-xy,-xy,-fp.Depth),vZ*-1)
    bitHole = bitHole.fuse(magHole1)
    bitHole = bitHole.fuse(magHole2)
    bitHole = bitHole.fuse(magHole3)
    bitHole = bitHole.fuse(magHole4)


    isRecomputeNeeded, slotWidth, trayHeight, trayDepth = bsh_utils.getSlotSize(props, bitHole.BoundBox.XLength, bitHole.BoundBox.YLength, fp.Depth)

    bitHole.translate(FreeCAD.Vector(slotWidth/2, trayHeight - props.marginTop - bitHoleDiameter/2, 0))

    box = Part.makeBox(slotWidth, trayHeight, trayDepth, vO, FreeCAD.Vector(0,0,-1))
    box.translate(FreeCAD.Vector(slotWidth, 0, 0))
    #holder = box.fuse(bitHole)  # devel
    holder = box.cut(bitHole)

    tag = bsh_utils.makeTag(props, fp.Tag, slotWidth)
    holder = holder.fuse(tag)

    bsh_utils.markHolderRecompute(isRecomputeNeeded)

    fp.Shape = holder
    super(BitHolder,self).execute(fp) # perform common operations
    
