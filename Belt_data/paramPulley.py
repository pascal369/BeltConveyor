from FreeCAD import Base
import FreeCADGui as Gui
#import pyautogui
import FreeCAD, Part, math
from math import pi
import Draft
import FreeCAD as App

#プーリー寸法
#ベルト幅   L     A    B    C    D    E     d1    d2   d3   t1  t2  t3  t4
pulley_dim={
'400':(   450,   50,  100, 500, 400,  100, 50,   45,  40,  9,  9,  8,  8),
'450':(   500,   50,  100, 550, 400,  100, 50,   45,  40,  9,  9,  8,  8),
'500':(   550,   50,  100, 600, 400,  100, 50,   45,  40,  9,  9,  8,  8),
'600':(   650,   50,  100, 700, 400,  100, 50,   45,  40,  9,  9,  8,  8),
'700':(   770,   50,  100, 820, 400,  100, 50,   45,  40,  9,  9,  8,  8),
'750':(   820,   50,  100, 870, 400,  100, 50,   45,  40,  9,  9,  8,  8),
'800':(   870,   50,  100, 920, 400,  100, 50,   45,  40,  9,  9,  8,  8),
'900':(  1000,   50,  100,1050, 400,  100, 50,   45,  40,  9,  9,  8,  8),
'1000':( 1100,   50,  100,1150, 400,  100, 50,   45,  40,  9,  9,  8,  8),
}
class Pulleys:
    def __init__(self, obj):
        self.Type = ''
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)
   
    def execute(self, obj):
        label=obj.Name
        BeltWidth=App.ActiveDocument.getObject(label).BeltWidth
        sa=pulley_dim[BeltWidth]
        #print(sa)
        D=App.ActiveDocument.getObject(label).D
        E=App.ActiveDocument.getObject(label).E
        L=float(App.ActiveDocument.getObject(label).L)
        #print(L)
        #L=sa[0]
        A=sa[1]
        B=sa[2]
        C=sa[3]
        #D=sa[4]
        #E=sa[5]
        d1=sa[6]
        d2=sa[7]
        d3=sa[8]
        t1=sa[9]
        t2=sa[10]
        t3=sa[11]
        t4=sa[11]
        #L=obj.L
        #print(L)
        L=sa[0]
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

        def BendP(self):
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
            #p1=(-(C/2+B+E),0,0)
            #p2=(-(C/2+B+E),0,d3/2)
            p3=(-(C/2+B),0,0)
            p4=(-(C/2+B),0,d2/2)
            p5=(-C/2,0,d2/2)
            p6=(-C/2,0,d1/2)
            p7=(C/2,0,d1/2)
            p8=(C/2,0,d2/2)
            p9=(C/2+B,0,d2/2)
            p10=(C/2+B,0,0)
            p11=(-(C/2+B),0,0)
            plst=[p3,p4,p5,p6,p7,p8,p9,p10,p11]
            pwire=Part.makePolygon(plst)
            pface = Part.Face(pwire)
            c01=pface.revolve(Base.Vector(0,0.0,0),Base.Vector(1,0,0),360)
            c00=c00.fuse(c01) 
        obj.BeltWidth=BeltWidth
        obj.D=D
        obj.E=E
        obj.L=sa[0]  
        #print(sa[0])
        try:     
            doc=App.activeDocument()  
        except:
            doc=App.newDocument()  
        
        if label=='DrivePulley' or label=='HeadPulley':
            #print(label)
            DriveP(self) 
            obj.Shape=c00
        else:
            BendP(self) 
            obj.Shape=c00
        FreeCAD.ActiveDocument.recompute()       
            

        
       

      
       
        



        