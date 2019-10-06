# (c) 2019 Stefan Katerkamp
# LGPL: This file is part of the Bit Socket Holder Workbench for FreeCAD

__title__="Bit Socket Holder dialogs"
__author__="katerkamp"
__url__="github.com/katerkamp/FreeCAD/BitSocketHolder"
__license__="LGPL 3"

import FreeCAD,FreeCADGui,Part
pq=FreeCAD.Units.parseQuantity
import bsh_cmd
import bsh_utils
from prototype_forms import prototypeDialog
from os import listdir
from os.path import join, dirname, abspath
from PySide.QtCore import *
from PySide.QtGui import *
from math import degrees
from DraftVecUtils import rounded
from HolderProperties import HolderProperties

class insertSocketHolderForm(prototypeDialog):
  def __init__(self):
    super(insertSocketHolderForm,self).__init__('socketHolder.ui')
  def accept(self):
    HolderProperties().initDocument()

    propList=[\
      self.form.SocketTag.text(),\
      self.form.SocketDiameter.value(),\
      self.form.SocketInsertDepth.value(),\
      self.form.createCutoutObject.isChecked(),\
      self.form.createTagObject.isChecked()\
      ]

    pos = bsh_utils.getNewPosition()
    a=bsh_cmd.makeSocketHolder(propList, pos)

    a.ViewObject.ShapeColor=(0.8,0.8,0.8)
    print('created obj ' + a.Name + ' ' + a.Label)
    if a.Tag:
      a.Label = 'SocketHolder-' + a.Tag
    FreeCADGui.Control.closeDialog()
    FreeCAD.activeDocument().commitTransaction()
    FreeCAD.activeDocument().recompute()
    FreeCADGui.SendMsgToActiveView("ViewFit")

    
# fixme: sometimes isChecked object gets already deleted runtime error
class insertBitHolderForm(prototypeDialog):
  def __init__(self):
    super(insertBitHolderForm,self).__init__('bitHolder.ui')
  def accept(self):
    HolderProperties().initDocument()

    propList=[\
      self.form.BitTag.text(),\
      self.form.BitDiameter.value(),\
      self.form.BitInsertDepth.value(),\
      self.form.createCutoutObject.isChecked(),\
      self.form.createTagObject.isChecked()\
      ]

    pos = bsh_utils.getNewPosition()
    a=bsh_cmd.makeBitHolder(propList, pos)

    a.ViewObject.ShapeColor=(0.8,0.8,0.8)
    print('created obj ' + a.Name + ' ' + a.Label)
    if a.Tag:
      a.Label = 'BitHolder-' + a.Tag
    FreeCADGui.Control.closeDialog()
    FreeCAD.activeDocument().commitTransaction()
    FreeCAD.activeDocument().recompute()
    FreeCADGui.SendMsgToActiveView("ViewFit")

class insertPadForm(prototypeDialog):
  def __init__(self):
    super(insertPadForm,self).__init__('pad.ui')
  def accept(self):
    HolderProperties().initDocument()

    propList=[\
      self.form.trayWidth.value(),\
      self.form.trayHeight.value(),\
      self.form.trayDepth.value()\
      ]

    pos = bsh_utils.getNewPosition()
    a=bsh_cmd.makePad(propList, pos)

    a.ViewObject.ShapeColor=(0.5,0.8,0.5)
    FreeCADGui.Control.closeDialog()
    FreeCAD.activeDocument().commitTransaction()
    FreeCAD.activeDocument().recompute()
    FreeCADGui.SendMsgToActiveView("ViewFit")

    
class insertAnyHolderForm(prototypeDialog):
  def __init__(self):
    print("Any Holder Init")
    super(insertAnyHolderForm,self).__init__('anyHolder.ui')

    sketches = []
    for o in FreeCAD.ActiveDocument.Objects:
      if hasattr(o, "TypeId") and o.TypeId == 'Sketcher::SketchObject':
        sketches.append(o)

    self.form.shapesAvaliable = []
    for s in sketches:
      self.form.shapesAvailable.addItem(s.Label)

  def accept(self):
    print("Any Holder Accept")
    HolderProperties().initDocument()

    propList=[\
      self.form.AnyTag.text(),\
      self.form.shapesAvailable.currentText(),\
      self.form.AnyInsertDepth.value(),\
      self.form.createCutoutObject.isChecked(),\
      self.form.createTagObject.isChecked()\
      ]

    pos = bsh_utils.getNewPosition()
    a=bsh_cmd.makeAnyHolder(propList, pos)

    a.ViewObject.ShapeColor=(0.8,0.8,0.8)
    print('created obj ' + a.Name + ' ' + a.Label)
    if a.Tag:
      a.Label = 'AnyHolder-' + a.Tag
    FreeCADGui.Control.closeDialog()
    FreeCAD.activeDocument().commitTransaction()
    FreeCAD.activeDocument().recompute()
    FreeCADGui.SendMsgToActiveView("ViewFit")


    
