# (c) 2019 Stefan Katerkamp
# LGPL: This file is part of the Bit Socket Holder Workbench for FreeCAD

__title__="bsh properties"
__author__="skat"
__url__="github.com/katerkamp/FreeCAD-BitSocketHolder"
__license__="LGPL 3"

import FreeCAD

class HolderProperties:

  DocumentLabel = "TrayProps"

  def __init__(self):
    pass
 
  def getProperties(self):
    return FreeCAD.activeDocument().getObject(HolderProperties.DocumentLabel)

  def initDocument(self):
    if not FreeCAD.activeDocument().getObject(HolderProperties.DocumentLabel) is None:
      return

    doc = FreeCAD.activeDocument().addObject('Spreadsheet::Sheet', HolderProperties.DocumentLabel)
  
    doc.set('A1', 'Cutout Increase')
    doc.set('B1', '0,2')
    doc.setDisplayUnit('B1:B1', 'mm')
    doc.setAlias('B1', 'cutoutIncrease')
    doc.set('C1', 'Move wall to the outside, needed to compensate for filament extrusion width')

    doc.set('A2', 'Magnet Hole Diameter')
    doc.set('B2', '2.4')
    doc.setDisplayUnit('B2:B2', 'mm')
    doc.setAlias('B2', 'magHoleDiameter')
    doc.set('C2', 'Diameter of the magnetic cylinder, including adjustment for filament extrusion width')

    doc.set('A3', 'Magnet Hole Depth')
    doc.set('B3', '4.4')
    doc.setDisplayUnit('B3:B3', 'mm')
    doc.setAlias('B3', 'magHoleDepth')
    doc.set('C3', 'Length of the magnetic cylinder, including adjustment for layer height')

    doc.set('A4', 'Text Size for Tags')
    doc.set('B4', '5')
    doc.setDisplayUnit('B4:B4', 'mm')
    doc.setAlias('B4', 'tagTextSize')

    doc.set('A5', 'Text Extrude Height for Tags')
    doc.set('B5', '0.7')
    doc.setDisplayUnit('B5:B5', 'mm')
    doc.setAlias('B5', 'tagTextHeight')

    doc.set('A6', 'Min Base Plate Thickness')
    doc.set('B6', '0.7')
    doc.setDisplayUnit('B6:B6', 'mm')
    doc.setAlias('B6', 'basePlateThickness')

    doc.set('A7', 'Margin between hole and corner')
    doc.set('B7', '1.5')
    doc.setDisplayUnit('B7:B7', 'mm')
    doc.setAlias('B7', 'marginTop')

    doc.set('A8', 'Margin between text and corner')
    doc.set('B8', '2.0')
    doc.setDisplayUnit('B8:B8', 'mm')
    doc.setAlias('B8', 'marginBottom')

    doc.set('A9', 'Margin between hole and text')
    doc.set('B9', '0.1')
    doc.setDisplayUnit('B9:B9', 'mm')
    doc.setAlias('B9', 'marginMiddle')
  
    doc.set('A10', 'Magnet offset to outer side')
    doc.set('B10', '0')
    doc.setDisplayUnit('B10:B10', 'mm')
    doc.setAlias('B10', 'magHoleOffset')

    # will be calculated automatically based on base plate thickness, otherwise if specified base plate thickness is the min value
    # and error will be reported if value too small
    doc.set('A11', 'Depth of Tray Block without text padding height')
    doc.set('B11', '')
    doc.setDisplayUnit('B11:B11', 'mm')
    doc.setAlias('B11', 'trayBaseDepth')

    doc.set('A12', 'Path to ttf font file')
    doc.set('B12', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')
    doc.setAlias('B12', 'ttfFontPath')

    FreeCAD.activeDocument().recompute()
    print('created TrayProps spreadsheet')


