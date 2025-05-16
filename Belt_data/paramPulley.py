from FreeCAD import Base
import FreeCADGui as Gui
#import pyautogui
import FreeCAD, Part, math
import DraftVecUtils
import Sketcher
import PartDesign
from math import pi
import Draft
import FreeCAD as App
from . import ShpstData

class Pulleys:
    def __init__(self, obj):
        self.Type = ''
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)
   
    def execute(self, obj):
        label=obj.Name
        L=App.ActiveDocument.getObject(label).L
        A=App.ActiveDocument.getObject(label).A
        B=App.ActiveDocument.getObject(label).B
        C=App.ActiveDocument.getObject(label).C
        D=App.ActiveDocument.getObject(label).D
        E=App.ActiveDocument.getObject(label).E
        d1=App.ActiveDocument.getObject(label).d1
        d2=App.ActiveDocument.getObject(label).d2
        d3=App.ActiveDocument.getObject(label).d3
        t1=App.ActiveDocument.getObject(label).t1
        t2=App.ActiveDocument.getObject(label).t2
        t3=App.ActiveDocument.getObject(label).t3
        t4=App.ActiveDocument.getObject(label).t4
        
        #d4=App.ActiveDocument.getObject(label).d4
        def DriveP(self):
        #ドラム
            global c00
            p1=(-L/2,0,D/2-t3)
            p2=(-L/2,0,D/2)
            p3=(L/2,0,D/2)
            p4=(L/2,0,D/2-t3)
            p5=(L/2-A,0,D/2-t3)
            p6=(L/2-A,0,D/2-t1)
            p7=(-(L/2-A),0,D/2-t1)
            p8=(-(L/2-A),0,D/2-t3)
            plst=[p1,p2,p3,p4,p5,p6,p7,p8,p1]
            pwire=Part.makePolygon(plst)
            pface = Part.Face(pwire)
            c00=pface.revolve(Base.Vector(0,0.0,0),Base.Vector(1,0,0),360)
            #側板
            p1=(-L/2+A-t2,0,d1/2)
            p2=(-L/2+A-t2,0,D/2-t3)
            p3=(-L/2+A,0,D/2-t3)
            p4=(-L/2+A,0,d1/2)
            plst=[p1,p2,p3,p4,p1]
            pwire=Part.makePolygon(plst)
            pface = Part.Face(pwire)
            c01=pface.revolve(Base.Vector(0,0.0,0),Base.Vector(1,0,0),360)
            c00=c00.fuse(c01)
            c01=pface.revolve(Base.Vector(0,0.0,0),Base.Vector(1,0,0),360)
            c01.Placement=App.Placement(App.Vector(L-2*A+t2,0,0),App.Rotation(App.Vector(1,0,0),0))
            c00=c00.fuse(c01)
            #軸
            p1=(-(C/2+B+E),0,0)
            p2=(-(C/2+B+E),0,d3/2)
            p3=(-(C/2+B),0,d3/2)
            p4=(-(C/2+B),0,d2/2)
            p5=(-C/2,0,d2/2)
            p6=(-C/2,0,d1/2)
            p7=(C/2,0,d1/2)
            p8=(C/2,0,d2/2)
            p9=(C/2+B,0,d2/2)
            p10=(C/2+B,0,0)
            plst=[p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p1]
            pwire=Part.makePolygon(plst)
            pface = Part.Face(pwire)
            c01=pface.revolve(Base.Vector(0,0.0,0),Base.Vector(1,0,0),360)
            c00=c00.fuse(c01)

           
        def HeadP(self):
            global c00
        #ドラム
            p1=(-L/2,0,D/2-t3)
            p2=(-L/2,0,D/2)
            p3=(L/2,0,D/2)
            p4=(L/2,0,D/2-t3)
            p5=(L/2-A,0,D/2-t3)
            p6=(L/2-A,0,D/2-t1)
            p7=(-(L/2-A),0,D/2-t1)
            p8=(-(L/2-A),0,D/2-t3)
            plst=[p1,p2,p3,p4,p5,p6,p7,p8,p1]
            pwire=Part.makePolygon(plst)
            pface = Part.Face(pwire)
            c00=pface.revolve(Base.Vector(0,0.0,0),Base.Vector(1,0,0),360)

            
            #側板
            p1=(-L/2+A-t2,0,d1/2)
            p2=(-L/2+A-t2,0,D/2-t3)
            p3=(-L/2+A,0,D/2-t3)
            p4=(-L/2+A,0,d1/2)
            plst=[p1,p2,p3,p4,p1]
            pwire=Part.makePolygon(plst)
            pface = Part.Face(pwire)
            c01=pface.revolve(Base.Vector(0,0.0,0),Base.Vector(1,0,0),360)
            c00=c00.fuse(c01)
            c01=pface.revolve(Base.Vector(0,0.0,0),Base.Vector(1,0,0),360)
            c01.Placement=App.Placement(App.Vector(L-2*A+t2,0,0),App.Rotation(App.Vector(1,0,0),0))
            c00=c00.fuse(c01)
            #軸
            p1=(-(C/2+B+E),0,0)
            p2=(-(C/2+B+E),0,d3/2)
            p3=(-(C/2+B),0,d3/2)
            p4=(-(C/2+B),0,d2/2)
            p5=(-C/2,0,d2/2)
            p6=(-C/2,0,d1/2)
            p7=(C/2,0,d1/2)
            p8=(C/2,0,d2/2)
            p9=(C/2+B,0,d2/2)
            p10=(C/2+B,0,0)
            p11=(-(C/2+B),0,0)
            plst=[p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11]
            pwire=Part.makePolygon(plst)
            pface = Part.Face(pwire)
            c01=pface.revolve(Base.Vector(0,0.0,0),Base.Vector(1,0,0),360)
            c00=c00.fuse(c01) 
            
            
        try:     
            doc=App.activeDocument()  
        except:
            doc=App.newDocument()  
       
        if label=='DrivePulley':
            DriveP(self) 
        else:
            HeadP(self) 
        g0=7.85
        g=c00.Volume*g0*1000/10**9 
        label='mass[kg]'
        try:
            obj.addProperty("App::PropertyFloat", "mass",label)
            obj.mass=g
            obj.ViewObject.Proxy=0
        except:
            obj.mass=g
            obj.ViewObject.Proxy=0
            pass          

        obj.Shape=c00
       

      
       
        



        