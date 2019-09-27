# (c) 2019 Stefan Katerkamp
# LGPL: This file is part of the Bit Socket Holder Workbench for FreeCAD

__title__="Bit Socket Holder toolbar"
__author__="katerkamp"
__url__="github.com/katerkamp/FreeCAD/BitSocketHolder"
__license__="LGPL 3"

# import FreeCAD modules
import FreeCAD, FreeCADGui,inspect, os

# helper -------------------------------------------------------------------
# FreeCAD TemplatePyMod module  
# (c) 2007 Juergen Riegel LGPL

def addCommand(name,cmdObject):
	(list,num) = inspect.getsourcelines(cmdObject.Activated)
	pos = 0
	# check for indentation
	while(list[1][pos] == ' ' or list[1][pos] == '\t'):
		pos += 1
	source = ""
	for i in range(len(list)-1):
		source += list[i+1][pos:]
	FreeCADGui.addCommand(name,cmdObject,source)

#---------------------------------------------------------------------------
# The command classes
#---------------------------------------------------------------------------


class insertSocketHolder:        
  def Activated (self):
    import bsh_forms
    FreeCADGui.Control.showDialog(bsh_forms.insertSocketHolderForm())
  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),"icons","SocketSlot.svg"),'MenuText':'Insert a socket storage position','ToolTip':'Insert a socket slot'}


class insertBitHolder:        
  def Activated (self):
    import bsh_forms
    FreeCADGui.Control.showDialog(bsh_forms.insertBitHolderForm())
  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),"icons","BitSlot.svg"),'MenuText':'Insert a hex bit storage position','ToolTip':'Insert a hex bit slot'}


class insertAnyHolder:        
  def Activated (self):
    import bsh_forms
    FreeCADGui.Control.showDialog(bsh_forms.insertAnyHolderForm())
  def GetResources(self):
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),"icons","AnySlot.svg"),'MenuText':'Insert a custom shaped storage position','ToolTip':'Insert a custom designed slot'}

class createAnyShape:        
  def Activated (self):
    print("Create Shape activated")
    import bsh_cmd
    #FreeCADGui.Control.showDialog(bsh_forms.makeAnyShapeForm())
    bsh_cmd.makeAnyShape()
  def GetResources(self):
    print("Create Shape getResources")
    return{'Pixmap':os.path.join(os.path.dirname(os.path.abspath(__file__)),"icons","AnyShape.svg"),'MenuText':'Create a custom tool shape','ToolTip':'Create a custom designed tool shape'}

#---------------------------------------------------------------------------
# Adds the commands to the FreeCAD command manager
#---------------------------------------------------------------------------
addCommand('insertSocketHolder',insertSocketHolder())
addCommand('insertBitHolder',insertBitHolder())
addCommand('insertAnyHolder',insertAnyHolder())
addCommand('createAnyShape',createAnyShape())
