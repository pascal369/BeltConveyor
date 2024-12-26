from FreeCAD import Base
import FreeCADGui as Gui
import pyautogui
import FreeCAD, Part, math
import DraftVecUtils
import Sketcher
import PartDesign
from math import pi
import Draft
import FreeCAD as App
from . import ShpstData

class Carrier:
    def __init__(self, obj):
        self.Type = ''
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)
   
    def execute(self, obj):
        label=obj.Name
        L=App.ActiveDocument.getObject(label).L