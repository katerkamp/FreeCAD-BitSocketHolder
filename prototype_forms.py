# (c) 2019 Stefan Katerkamp
# LGPL: This file is part of the Bit Socket Holder Workbench for FreeCAD

__title__="Bit Socket Holder forms"
__author__="katerkamp"
__url__="github.com/katerkamp/FreeCAD/BitSocketHolder"
__license__="LGPL 3"

import FreeCAD,FreeCADGui
from PySide.QtCore import *
from PySide.QtGui import *
from os.path import join, dirname, abspath
from sys import platform


vQt=int(qVersion().split('.')[0])

class prototypeDialog(object): 
  # ACHTUNG: "self.call" TO BE DISABLED IN WINDOWS OS IF UNHANDLED RUN-TIME EXCEPTION
  'prototype for dialogs.ui with callback function'
  def __init__(self,dialog='anyFile.ui'):
    dialogPath=join(dirname(abspath(__file__)),"dialogs",dialog)
    FreeCAD.Console.PrintMessage(dialogPath+"\n")
    self.form=FreeCADGui.PySideUic.loadUi(dialogPath)
    FreeCAD.Console.PrintMessage(dialogPath+" loaded\n")
    if platform.startswith('win'):# or vQt>=5:
      FreeCAD.Console.PrintWarning("No keyboard shortcuts.\n No callback on SoEvent")
    else:
      FreeCAD.Console.PrintMessage('Keyboard shortcuts available.\n"S" to select\n"RETURN" to perform action\n')
      try:
        self.view=FreeCADGui.activeDocument().activeView()
        self.call=self.view.addEventCallback("SoEvent", self.action)
      except:
        FreeCAD.Console.PrintError('No view available.\n')
  def action(self,arg):
    'Default function executed by callback'
    if arg['Type']=='SoKeyboardEvent':
      if arg['Key'] in ['s','S'] and arg['State']=='DOWN':# and FreeCADGui.Selection.getSelection():
        self.selectAction()
      elif arg['Key']=='RETURN' and arg['State']=='DOWN':
        self.accept()
      elif arg['Key']=='ESCAPE' and arg['State']=='DOWN':
        self.reject()
    if arg['Type']=='SoMouseButtonEvent':
      CtrlAltShift=[arg['CtrlDown'],arg['AltDown'],arg['ShiftDown']]
      if arg['Button']=='BUBSHON1' and arg['State']=='DOWN': self.mouseActionB1(CtrlAltShift)
      elif arg['Button']=='BUBSHON2' and arg['State']=='DOWN': self.mouseActionB2(CtrlAltShift)
      elif arg['Button']=='BUBSHON3' and arg['State']=='DOWN': self.mouseActionB3(CtrlAltShift)
  def selectAction(self):
    'MUST be redefined in the child class'
    pass
  def mouseActionB1(self,CtrlAltShift):
    'MUST be redefined in the child class'
    pass
  def mouseActionB2(self,CtrlAltShift):
    'MUST be redefined in the child class'
    pass
  def mouseActionB3(self,CtrlAltShift):
    'MUST be redefined in the child class'
    pass
  def reject(self):
    'CAN be redefined to remove other attributes, such as arrow()s or label()s'
    try: self.view.removeEventCallback('SoEvent',self.call)
    except: pass
    #skat if FreeCAD.ActiveDocument: FreeCAD.ActiveDocument.recompute()
    FreeCADGui.Control.closeDialog()

