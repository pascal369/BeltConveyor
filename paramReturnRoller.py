from FreeCAD import Base
import Part
import FreeCADGui as Gui
from math import pi
import FreeCAD as App
import BeltCv
class R_roller:
    def __init__(self, obj):
        self.Type = ''
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)
    def execute(self, obj):
        global c00
        label=obj.Name
        BeltWidth=App.ActiveDocument.getObject(label).BeltWidth
        spec=App.ActiveDocument.getObject(label).spec
        if spec=='RubberLining':
            sa=BeltCv.groller_lst[BeltWidth]
        elif spec=='PVCLining':
            sa=BeltCv.eroller_lst[BeltWidth]
        D=sa[0]
        d=sa[1]
        L=sa[4]
        l=sa[5]
        c01= Part.makeCylinder(d/2,(L-l)/2,Base.Vector(0,0,0),Base.Vector(1,0,0),360)
        c02= Part.makeCylinder(D/2,l,Base.Vector((L-l)/2,0,0),Base.Vector(1,0,0),360)
        c03= Part.makeCylinder(d/2,(L-l)/2,Base.Vector((L+l)/2,0,0),Base.Vector(1,0,0),360)
        c00=c01.fuse(c02)
        c00=c00.fuse(c03)

        c1=c00  
        obj.Shape=c1  