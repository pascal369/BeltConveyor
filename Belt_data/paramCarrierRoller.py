from FreeCAD import Base
import Part
import FreeCADGui as Gui
from math import pi
import FreeCAD as App
#from . import BeltCv
class C_roller:
    def __init__(self, obj):
        self.Type = ''
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)
    def execute(self, obj):
        label=obj.Name
        BeltWidth=App.ActiveDocument.getObject(label).BeltWidth
        spec=App.ActiveDocument.getObjject(label).spec
        spec2=App.ActiveDocument.getObjject(label).spec2

        if spec=='RubberLining':
            sa=BeltCv.groller_lst[BeltWidth]
        elif spec=='PVCLining':
            sa=BeltCv.eroller_lst[BeltWidth]
        D=sa[0]
        d=sa[1]
        L=sa[2]
        l=sa[3]
        c01= Part.makeCylinder(d/2,(L-l)/2,Base.Vector(0,0,0),Base.Vector(1,0,0),360)
        c02= Part.makeCylinder(D/2,l,Base.Vector((L-l)/2,0,0),Base.Vector(1,0,0),360)
        c03= Part.makeCylinder(d/2,(L-l)/2,Base.Vector((L+l)/2,0,0),Base.Vector(1,0,0),360)
        c00=c01.fuse(c02)
        c00=c00.fuse(c03)