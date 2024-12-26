#***************************************************************************
#*    Copyright (C) 2023 
#*    This library is free software
#***************************************************************************
import inspect
import os
import sys
import FreeCAD
import FreeCADGui

class beltCvShowCommand:
    def GetResources(self):
        file_path = inspect.getfile(inspect.currentframe())
        module_path=os.path.dirname(file_path)
        return { 
          'Pixmap': os.path.join(module_path, "icons", "beltcv.svg"),
          'MenuText': "beltCv",
          'ToolTip': "Show/Hide beltCv"}

    def IsActive(self):
        import BeltCv
        BeltCv
        return True

    def Activated(self):
        try:
          import BeltCv
          BeltCv.main.d.show()
        except Exception as e:
          FreeCAD.Console.PrintError(str(e) + "\n")

    def IsActive(self):
        import BeltCv
        return not FreeCAD.ActiveDocument is None

class beltCvWB(FreeCADGui.Workbench):
    def __init__(self):
        file_path = inspect.getfile(inspect.currentframe())
        module_path=os.path.dirname(file_path)
        self.__class__.Icon = os.path.join(module_path, "icons", "beltcv.svg")
        self.__class__.MenuText = "beltCv"
        self.__class__.ToolTip = "beltCv by Pascal"

    def Initialize(self):
        self.commandList = ["beltCv_Show"]
        self.appendToolbar("&beltCv", self.commandList)
        self.appendMenu("&beltCv", self.commandList)

    def Activated(self):
        import BeltCv
        BeltCv
        return

    def Deactivated(self):
        return

    def ContextMenu(self, recipient):
        return

    def GetClassName(self): 
        return "Gui::PythonWorkbench"
    
FreeCADGui.addWorkbench(beltCvWB())
FreeCADGui.addCommand("beltCv_Show", beltCvShowCommand())    
