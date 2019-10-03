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

################ CLASSES ###########################

class holderType(object):
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

class SocketHolder(holderType):
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
    obj.Tag=Tag
    obj.Diameter=Diameter
    obj.Depth=Depth
    obj.CutoutObject = CutoutObject
    obj.TagObject = TagObject
    self.Label = obj.Name + Tag
    # define specific properties
    #obj.addProperty("App::PropertyString","FooType","Foo","Type of flange").FooType="foobar"

  def onChanged(self, fp, prop):
    return None

  def execute(self, fp): # fp is FeaturePython
    import math
    props = FreeCAD.activeDocument().TrayProps

    socketHoleDiameter = fp.Diameter + props.holeTolerance  # fp.Diameter is measured diameter of nut

    print("Create Cutout" + str(fp.CutoutObject))

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

    trayHeight = math.ceil(socketHoleDiameter + props.marginTop + props.marginBottom + props.marginMiddle + props.tagTextSize)
    slotWidth = math.ceil(socketHoleDiameter + 2 * props.marginTop) # todo use marginLeftRight
    trayDepth = fp.Depth + props.magHoleDepth + props.basePlateThickness
    print("Depth is " + str(trayDepth) + " = " + str(fp.Depth) + "+" + str(props.magHoleDepth) + "+" + str(props.basePlateThickness))

    markRecompute = False
    if trayDepth > maxZ:
      markRecompute = True
    else:
      trayDepth = maxZ
    if trayHeight > maxY:
      markRecompute = True
    else:
      trayHeight = maxY

    print("Tray Insert Block Size: w" + str(slotWidth) + " h" + str(trayHeight) + " d" + str(trayDepth))

    bsh_utils.markHolderRecompute(mark)

    # Create nut hole with 4 magholes
    base=Part.Face(Part.Wire(Part.makeCircle((socketHoleDiameter)/2)))
    socketHole = base.extrude(FreeCAD.Vector(0,0,-1 * fp.Depth))
    xy=(socketHoleDiameter/2 * 0.7071068) - props.magHoleDiameter/5 # todo make property for /5 offset
    magHole1 = Part.makeCylinder(props.magHoleDiameter/2,props.magHoleDepth,FreeCAD.Vector(xy,xy,-fp.Depth),vZ*-1)
    magHole2 = Part.makeCylinder(props.magHoleDiameter/2,props.magHoleDepth,FreeCAD.Vector(-xy,xy,-fp.Depth),vZ*-1)
    magHole3 = Part.makeCylinder(props.magHoleDiameter/2,props.magHoleDepth,FreeCAD.Vector(xy,-xy,-fp.Depth),vZ*-1)
    magHole4 = Part.makeCylinder(props.magHoleDiameter/2,props.magHoleDepth,FreeCAD.Vector(-xy,-xy,-fp.Depth),vZ*-1)
    socketHole = socketHole.fuse(magHole1)
    socketHole = socketHole.fuse(magHole2)
    socketHole = socketHole.fuse(magHole3)
    socketHole = socketHole.fuse(magHole4)
    socketHole.translate(FreeCAD.Vector(slotWidth/2, trayHeight - props.marginTop - socketHoleDiameter/2, 0))

    box = Part.makeBox(slotWidth, trayHeight, trayDepth, vO, FreeCAD.Vector(0,0,-1))
    box.translate(FreeCAD.Vector(slotWidth, 0, 0))
    #holder = box.fuse(socketHole)  # devel
    holder = box.cut(socketHole)

    tag = bsh_util.makeTag(props)
    holder = holder.fuse(tag)

    fp.Shape = holder
    super(SocketHolder,self).execute(fp) # perform common operations
    
class BitHolder(holderType):
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
    props = FreeCAD.activeDocument().TrayProps
    bitHoleDiameter = fp.Diameter + props.holeTolerance  # fp.Diameter is measured diameter of nut

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

    trayHeight = math.ceil(bitHoleDiameter + props.marginTop + props.marginBottom + props.marginMiddle + props.tagTextSize)
    slotWidth = math.ceil(bitHoleDiameter + 2 * props.marginTop) # todo use marginLeftRight
    trayDepth = fp.Depth + props.magHoleDepth + props.basePlateThickness
    print("Depth is " + str(trayDepth) + " = " + str(fp.Depth) + "+" + str(props.magHoleDepth) + "+" + str(props.basePlateThickness))

    markRecompute = False
    if trayDepth > maxZ:
      markRecompute = True
    else:
      trayDepth = maxZ
    if trayHeight > maxY:
      markRecompute = True
    else:
      trayHeight = maxY

    print("Tray Insert Block Size: w" + str(slotWidth) + " h" + str(trayHeight) + " d" + str(trayDepth))

    bsh_utils.markHolderRecompute(markRecompute)

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
    xy=(bitHoleDiameter/2 * 0.7071068) - props.magHoleDiameter/5 # todo make property for /5 offset
    magHole1 = Part.makeCylinder(props.magHoleDiameter/2,props.magHoleDepth,FreeCAD.Vector(xy,xy,-fp.Depth),vZ*-1)
    magHole2 = Part.makeCylinder(props.magHoleDiameter/2,props.magHoleDepth,FreeCAD.Vector(-xy,xy,-fp.Depth),vZ*-1)
    magHole3 = Part.makeCylinder(props.magHoleDiameter/2,props.magHoleDepth,FreeCAD.Vector(xy,-xy,-fp.Depth),vZ*-1)
    magHole4 = Part.makeCylinder(props.magHoleDiameter/2,props.magHoleDepth,FreeCAD.Vector(-xy,-xy,-fp.Depth),vZ*-1)
    bitHole = bitHole.fuse(magHole1)
    bitHole = bitHole.fuse(magHole2)
    bitHole = bitHole.fuse(magHole3)
    bitHole = bitHole.fuse(magHole4)
    bitHole.translate(FreeCAD.Vector(slotWidth/2, trayHeight - props.marginTop - bitHoleDiameter/2, 0))

    box = Part.makeBox(slotWidth, trayHeight, trayDepth, vO, FreeCAD.Vector(0,0,-1))
    box.translate(FreeCAD.Vector(slotWidth, 0, 0))
    #holder = box.fuse(bitHole)  # devel
    holder = box.cut(bitHole)

    tag = bsh_util.makeTag(props)
    holder = holder.fuse(tag)

    fp.Shape = holder
    super(BitHolder,self).execute(fp) # perform common operations
    
class AnyHolder(holderType):

  def __init__(self, obj, Tag="",ShapeLabel="Sketch",Depth=10):
    # initialize the parent class
    super(AnyHolder,self).__init__(obj)
    obj.addProperty("App::PropertyString","ShapeLabel","Base","Label of Cutout sketch").ShapeLabel
    # define common properties TODO take from TrayProps
    obj.BSHType="Holder" 
    obj.Tag=Tag
    obj.ShapeLabel=ShapeLabel
    obj.Depth=Depth
    self.Label = obj.Name + Tag
    # define specific properties
    obj.addProperty("App::PropertyString","ShapeLabel","Base","Sketch label of shape").ShapeLabel=ShapeLabel

  def onChanged(self, fp, prop):
    return None

  def execute(self, fp): # fp is FeaturePython
    import math
    props = FreeCAD.activeDocument().TrayProps

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

    markRecompute = bsh_utils.checkIfHolderIsBiggerThanOthers(props, toolCutout.BoundBox.XLength, toolCutout.BoundBox.YLength, fp.Depth)
    bsh_utils.markHolderRecompute(markRecompute)

    # center cutout in box horizontally, position vertically with top margin
    slotWidth = math.ceil(toolCutout.BoundBox.XLength + 2 * props.marginTop) # todo use marginLeftRight
    trayHeight = math.ceil(toolCutout.BoundBox.YLength + props.marginTop + props.marginBottom + props.marginMiddle + props.tagTextSize)
    trayDepth = fp.Depth + props.magHoleDepth + props.basePlateThickness

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
    
