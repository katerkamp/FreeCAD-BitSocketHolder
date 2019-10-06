# (c) 2019 Stefan Katerkamp
# LGPL: This file is part of the Bit Socket Holder Workbench for FreeCAD

__title__="Bit/Socket Holder objects"
__author__="katerkamp"
__url__="github.com/katerkamp/FreeCAD/BitSocketHolder"
__license__="LGPL 3"

import FreeCAD, FreeCADGui, Part, bsh_cmd, bsh_utils

vO=FreeCAD.Vector(0,0,0)
vX=FreeCAD.Vector(1,0,0)
vY=FreeCAD.Vector(0,1,0)
vZ=FreeCAD.Vector(0,0,1)

from Holder import Holder
from HolderProperties import HolderProperties
    
class BitHolder(Holder):
  def __init__(self, obj, Tag="",Diameter=12,Depth=10,CutoutObject=False,TagObject=False):
    # initialize the parent class
    super(BitHolder,self).__init__(obj)
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
    bitHoleDiameter = fp.Diameter + 2*props.cutoutIncrease 

    # Cutout
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
    x=bitHoleDiameter/2 - props.magHoleDiameter/2 - props.magHoleDiameter*0.13 + props.magHoleOffset
    y=0
    magHole1 = Part.makeCylinder(props.magHoleDiameter/2,props.magHoleDepth,FreeCAD.Vector(x,y,-fp.Depth),vZ*-1)
    magHole2 = Part.makeCylinder(props.magHoleDiameter/2,props.magHoleDepth,FreeCAD.Vector(-x,y,-fp.Depth),vZ*-1)
    bitHole = bitHole.fuse(magHole1)
    bitHole = bitHole.fuse(magHole2)

    bsh_utils.addCutoutObject(fp, bitHole, 'BitCutout')

    fp.CutoutWidth = bitHole.BoundBox.XLength
    fp.CutoutHeight = bitHole.BoundBox.YLength
    fp.CutoutDepth = bitHole.BoundBox.ZLength

    isRecomputeNeeded, slotWidth, trayHeight, trayDepth = bsh_utils.getSlotSize(props, fp)

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
    
