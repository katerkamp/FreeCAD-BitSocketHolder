#****************************************************************************
#*                                                                          *
#*   Bit Socket Holder Workbench:                                           *
#*       create holders to store tools like bits and nuts                   *
#*   Copyright (c) 2019 Stefan Katerkamp <info@katerkamp.de>                *
#*                                                                          *
#*   This program is free software; you can redistribute it and/or modify   *
#*   it under the terms of the GNU Lesser General Public License (LGPL)     *
#*   as published by the Free Software Foundation; either version 2 of      *
#*   the License, or (at your option) any later version.                    *
#*   for detail see the LICENCE text file.                                  *
#*                                                                          *
#*   This program is distributed in the hope that it will be useful,        *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of         *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          *
#*   GNU Library General Public License for more details.                   *
#*                                                                          *
#*   You should have received a copy of the GNU Library General Public      *
#*   License along with this program; if not, write to the Free Software    *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307   *
#*   USA                                                                    *
#*                                                                          *
#****************************************************************************

class ToolboxTray ( Workbench ):

  def __init__(self):
    self.__class__.Icon = FreeCAD.getUserAppDataDir()+"Mod" + "/BitSocketHolder/icons/katerkamp-logo.svg"
    self.__class__.MenuText = "Bit/Socket Holder"
    self.__class__.ToolTip = "Bits/Socket Holders for Craftman Toolbox"

  # todo these tools are always active even if Gui.ActiveDocument is None, grey them out
  def Initialize(self):
    import CommandsBSH
    cmdList=["insertSocketHolder", "insertBitHolder", "insertAnyHolder", "createAnyShape"]
    self.appendToolbar("BSH Tools",cmdList)
    Log ('Loading BSH tools: done\n')
    menu = ["Tool Shapes"]
    self.appendMenu(menu,cmdList)    

  def Activated(self):
    #if hasattr(FreeCADGui,"draftToolBar"):
    #  FreeCADGui.draftToolBar.Activated()
    #if hasattr(FreeCADGui,"Snapper"):
    #  FreeCADGui.Snapper.show()
    FreeCAD.__activeBSH__=None
    Msg("Created variables in FreeCAD module:\n")
    Msg("__activeBSH__\n")

  def Deactivated(self):
    del FreeCAD.__activeBSH__
    Msg("Deleted variables in FreeCAD module:\n")
    Msg("__activeBSH__\n")

#  def ContextMenu(self, recipient):
#    """This is executed whenever the user right-clicks on screen"""
#    # "recipient" will be either "view" or "tree"
#    self.appendContextMenu("My commands",self.list) # add commands to the context menu

  def GetClassName(self):
    # this function is mandatory if this is a full python workbench
    return "Gui::PythonWorkbench"

Gui.addWorkbench(ToolboxTray)
