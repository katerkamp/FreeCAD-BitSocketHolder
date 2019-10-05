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
    
class AnyHolder(Holder):

  def __init__(self, obj, Tag="",ShapeLabel="Sketch",Depth=10,CutoutObject=False,TagObject=False):
    # initialize the parent class
    super(AnyHolder,self).__init__(obj)
    obj.addProperty("App::PropertyString","ShapeLabel","Base","Label of Cutout sketch").ShapeLabel
    # define common properties TODO take from TrayProps
    obj.BSHType="Holder" 
    obj.Tag=Tag.strip()
    obj.ShapeLabel=ShapeLabel
    obj.Depth=Depth
    obj.CutoutObject = CutoutObject
    obj.TagObject = TagObject
    self.Label = obj.Name + Tag.strip().replace(' ','_')
    # define specific properties
    obj.addProperty("App::PropertyString","ShapeLabel","Base","Sketch label of shape").ShapeLabel=ShapeLabel

  def onChanged(self, fp, prop):
    return None

  #todo if no sketch given, return with message
  def execute(self, fp): # fp is FeaturePython
    import math
    props = HolderProperties().getProperties()

    # extrude sketch "Sketch" and get dimensions
    sketchName = fp.ShapeLabel
    sketchObject = FreeCAD.activeDocument().getObject(sketchName)
    sketchObject.ViewObject.Visibility = False
    import Part
    wire = sketchObject.Shape.Wires[0]
    face = Part.Face(wire)
    toolCutout = face.extrude(FreeCAD.Vector(0,0,-fp.Depth))

    # magnets
    magnetPositions = []
    i = 0
    while i < sketchObject.GeometryCount:
      g = sketchObject.Geometry[i]
      if type(g) is Part.Point:
        magnetPositions.append(FreeCAD.Vector(g.X, g.Y, 0))
      i = i + 1

    for pos in magnetPositions:
      magHole = Part.makeCylinder(props.magHoleDiameter/2,props.magHoleDepth,FreeCAD.Vector(pos.x,pos.y,-fp.Depth),vZ*-1)
      toolCutout = toolCutout.fuse(magHole)

    # Scale slighly bigger for tolerance
    #Draft.scale([toolShape],delta=FreeCAD.Vector(1.0,1.0,1.0),center=FreeCAD.Vector(-106.0,-86.0,0.0),copy=False,legacy=False)

    bsh_utils.addCutoutObject(fp, toolCutout, 'AnyCutout')

    isRecomputeNeeded, slotWidth, trayHeight, trayDepth = bsh_utils.getSlotSize(props, toolCutout.BoundBox.XLength, toolCutout.BoundBox.YLength, fp.Depth)
    bsh_utils.markHolderRecompute(isRecomputeNeeded)

    # center cutout in box horizontally, position vertically with top margin
    xoff = toolCutout.BoundBox.XLength/2 - toolCutout.BoundBox.XMax + slotWidth/2
    yoffCenter = toolCutout.BoundBox.YLength/2 - toolCutout.BoundBox.YMax
    yoff = yoffCenter + trayHeight - props.marginTop - toolCutout.BoundBox.YLength/2
    toolCutout.translate(FreeCAD.Vector(xoff, yoff, 0))

    box = Part.makeBox(slotWidth, trayHeight, trayDepth, vO, FreeCAD.Vector(0,0,-1))
    box.translate(FreeCAD.Vector(slotWidth, 0, 0))  # todo center
    #holder = box.fuse(toolCutout)  # devel
    holder = box.cut(toolCutout)

    tag = bsh_utils.makeTag(props, fp.Tag, slotWidth)
    holder = holder.fuse(tag)

    fp.Shape = holder
    super(AnyHolder,self).execute(fp) # perform common operations
    
