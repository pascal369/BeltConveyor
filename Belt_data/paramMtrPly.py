from FreeCAD import Base
import FreeCAD, Part, math
from math import pi
import FreeCADGui as Gui
import Draft
import FreeCAD as App
import Part
from . import mtrply_data

class MotorPly:
    def __init__(self, obj):
        self.Type = 'BasePlate'
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)        
    def execute(self,obj):
        label=obj.Name
        key=App.ActiveDocument.getObject(label).key
        A=App.ActiveDocument.getObject(label).A
        a=App.ActiveDocument.getObject(label).a
        b=App.ActiveDocument.getObject(label).b
        D=App.ActiveDocument.getObject(label).D
        D1=App.ActiveDocument.getObject(label).D1
        D2=App.ActiveDocument.getObject(label).D2
        D3=App.ActiveDocument.getObject(label).D3
        L=App.ActiveDocument.getObject(label).L
        C=App.ActiveDocument.getObject(label).C
        E=App.ActiveDocument.getObject(label).E
        M=App.ActiveDocument.getObject(label).M
        R=App.ActiveDocument.getObject(label).R
        N1=App.ActiveDocument.getObject(label).N1
        N2=App.ActiveDocument.getObject(label).N2
        d=App.ActiveDocument.getObject(label).d
        B1=App.ActiveDocument.getObject(label).B1
        B2=App.ActiveDocument.getObject(label).B2
        F=App.ActiveDocument.getObject(label).F
        G1=App.ActiveDocument.getObject(label).G1
        G2=App.ActiveDocument.getObject(label).G2
        H=App.ActiveDocument.getObject(label).H
        P=App.ActiveDocument.getObject(label).P
        g=App.ActiveDocument.getObject(label).g
        x0=a+A/2

        x4=float(H+G1-N1)
        x5=P-(a+G1)
        x6=P-(G2+b)    
        
        def drum(self):#駆動プーリー
            global c00
            #ドラム
            p1=(-x0,0,0)
            p2=(-x0,0,D2/2)
            p3=(-x0+a,0,D2/2)
            p4=(-x0+a,0,D1/2)
            p5=(-x0+a+0.35*A,0,D/2)
            p6=(-x0+a+0.65*A,0,D/2)
            p7=(-x0+a+A,0,D1/2)
            p8=(-x0+a+A,0,D3/2)
            p9=(-x0+a+A+b,0,D3/2)
            p10=(a+A+b-x0,0,0)
            plst=[p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p1]
            pwire=Part.makePolygon(plst)
            #Part.show(pwire)
            pface = Part.Face(pwire)
            c00=pface.revolve(Base.Vector(0,0,0),Base.Vector(1,0,0),360)
            #Part.show(c00)

        def brg_left(self):
            global c00
            p1=(-x0,0,0)
            p2=(-x0,0,R)
            p3=(-x0,M/2-C,R)
            p4=(-x0,M/2-C,R+5)
            p5=(-x0,M/2-(C-5),R+5)
            p6=(-x0,M/2-(C-5),C)
            p7=(-x0,M/2,C+C-5)
            p8=(-x0,M/2+C-5,C)
            p9=(-x0,M/2+C-5,R+5)
            p10=(-x0,M/2+C,R+5)
            p11=(-x0,M/2+C,R)
            p12=(-x0,M,R)
            p13=(-x0,M,0)
            edge1=Part.makeLine(p1,p2)
            edge2=Part.makeLine(p2,p3)
            edge3=Part.makeCircle(5,Base.Vector(p4),Base.Vector(1,0,0),-90,0)
            edge4=Part.makeLine(p5,p6)
            edge5=Part.Arc(Base.Vector(p6),Base.Vector(p7),Base.Vector(p8)).toShape()
            #Part.show(edge5)
            edge6=Part.makeLine(p8,p9)
            edge7=Part.makeCircle(5,Base.Vector(p10),Base.Vector(1,0,0),180,270)
            edge8=Part.makeLine(p11,p12)
            edge9=Part.makeLine(p12,p13)
            edge10=Part.makeLine(p13,p1)

            aWire=Part.Wire([edge1,edge2,edge3,edge4,edge5,edge6,edge7,edge8,edge9,edge10])
            #Part.show(aWire)
            pface = Part.Face(aWire)
            c00=pface.extrude(Base.Vector(-(N1),0,0))
            c00.Placement=App.Placement(App.Vector(-x5,-M/2,-C),App.Rotation(App.Vector(1,1,1),0))
            c01= Part.makeCylinder((C-15),x5,Base.Vector(-x5-x0,0,0),Base.Vector(1,0,0),360)
            c00=c00.fuse(c01)
            if x4>0.0 :
                c00=c00.fuse(c01)
                c02= Part.makeCylinder(0.8*(C-15),x4/3,Base.Vector(-(x5+N1+x4/3)-x0,0,0),Base.Vector(1,0,0),360)
                c00=c00.fuse(c02)
                c03= Part.makeCylinder(0.6*(C-15),x4/3,Base.Vector(-(x5+N1+2*x4/3)-x0,0,0),Base.Vector(1,0,0),360)
                c00=c00.fuse(c03)
                c04= Part.makeCylinder(0.4*(C-15),x4/3,Base.Vector(-(x5+N1+3*x4/3)-x0,0,0),Base.Vector(1,0,0),360)
                c00=c00.fuse(c04)

            #ボルト穴
            for i in range(2):
                if i==0:
                    c05= Part.makeCylinder(d/2,C,Base.Vector(-(x5+N1)+G1-x0,E/2,-C),Base.Vector(0,0,1),360) 
                else:
                    c05= Part.makeCylinder(d/2,C,Base.Vector(-(x5+N1)+G1-x0,-E/2,-C),Base.Vector(0,0,1),360) 
                c00=c00.cut(c05)
            if key>10:
                x7=N1-2*G1
                for i in range(2):
                    if i==0:
                        c05= Part.makeCylinder(d/2,C,Base.Vector(-(x5+N1)+G1+x7-x0,E/2,-C),Base.Vector(0,0,1),360) 
                    else:
                        c05= Part.makeCylinder(d/2,C,Base.Vector(-(x5+N1)+G1+x7-x0,-E/2,-C),Base.Vector(0,0,1),360) 
                        #c05= Part.makeCylinder(d/2,C,Base.Vector(-(x5)+G1+x7,-E/2,-C),Base.Vector(0,0,1),360)
                    c00=c00.cut(c05)

        def brg_Right(self):
            global c00
            p1=(-x0,0,0)
            p2=(-x0,0,R)
            p3=(-x0,M/2-C,R)
            p4=(-x0,M/2-C,R+5)
            p5=(-x0,M/2-(C-5),R+5)
            p6=(-x0,M/2-(C-5),C)
            p7=(-x0,M/2,C+C-5)
            p8=(-x0,M/2+C-5,C)
            p9=(-x0,M/2+C-5,R+5)
            p10=(-x0,M/2+C,R+5)
            p11=(-x0,M/2+C,R)
            p12=(-x0,M,R)
            p13=(-x0,M,0)
            edge1=Part.makeLine(p1,p2)
            edge2=Part.makeLine(p2,p3)
            edge3=Part.makeCircle(5,Base.Vector(p4),Base.Vector(1,0,0),-90,0)
            edge4=Part.makeLine(p5,p6)
            edge5=Part.Arc(Base.Vector(p6),Base.Vector(p7),Base.Vector(p8)).toShape()
            edge6=Part.makeLine(p8,p9)
            edge7=Part.makeCircle(5,Base.Vector(p10),Base.Vector(1,0,0),180,270)
            edge8=Part.makeLine(p11,p12)
            edge9=Part.makeLine(p12,p13)
            edge10=Part.makeLine(p13,p1)

            aWire=Part.Wire([edge1,edge2,edge3,edge4,edge5,edge6,edge7,edge8,edge9,edge10])
            pface = Part.Face(aWire)
            c00=pface.extrude(Base.Vector(N2,0,0))
            c00.Placement=App.Placement(App.Vector(a+A+b+x6,-M/2,-C),App.Rotation(App.Vector(0,0,1),0))
            c01= Part.makeCylinder((C-15),x6,Base.Vector(a+A+b-x0,0,0),Base.Vector(1,0,0),360)
            c00=c00.fuse(c01)
            #ボルト穴
            for i in range(2):
                if i==0:
                    c05= Part.makeCylinder(d/2,C,Base.Vector((a+A+x6+a)+G2-x0,E/2,-C),Base.Vector(0,0,1),360) 
                else:
                    c05= Part.makeCylinder(d/2,C,Base.Vector((a+A+x6+b)+G2-x0,-E/2,-C),Base.Vector(0,0,1),360) 
                c00=c00.cut(c05)
            if key>10:
                x7=N2-2*G2
                for i in range(2):
                    if i==0:
                        c05= Part.makeCylinder(d/2,C,Base.Vector((a+A+x6)+G2+x7-x0,E/2,-C),Base.Vector(0,0,1),360) 
                    else:
                        c05= Part.makeCylinder(d/2,C,Base.Vector((a+A+x6)+G2+x7-x0,-E/2,-C),Base.Vector(0,0,1),360) 
                    c00=c00.cut(c05)  
            #ケーブル
            x8=a+A+b+N2+x6
            p1=(x8-x0,0,0)
            p2=(x8-x0,0,-15)  
            p3=(x8-x0,0,0)
            p4=(x8+15-x0,0,-15) 
            p5=(x8+15-x0,0,-65)  
            edge2 = Part.makeCircle(15, Base.Vector(p2), Base.Vector(0,1,0), -90, 0) 
            edge3=Part.makeLine(p4,p5) 
            aWire = Part.Wire([edge2,edge3])
            edge4=Part.makeCircle(10, Base.Vector(x8-x0,0,0), Base.Vector(1,0,0), 0, 360) 
            profile = Part.Wire([edge4])
            makeSolid=True
            isFrenet=True
            c06 = Part.Wire(aWire).makePipeShell([profile],makeSolid,isFrenet)
            c00=c00.fuse(c06)

        drum(self) 
        c1=c00 
       
        brg_left(self)
        c2=c00
        c1=c1.fuse(c2)
        brg_Right(self)
        c3=c00
        c1=c1.fuse(c3)
        c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),90))

        label='mass[kg]'
        try:
            obj.addProperty("App::PropertyFloat", "mass",label)
            obj.mass=g
            obj.ViewObject.Proxy=0
        except:
            obj.mass=g
            obj.ViewObject.Proxy=0
            pass   
        obj.Shape=c1

    



        

       