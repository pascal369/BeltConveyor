from FreeCAD import Base
import FreeCADGui as Gui
import FreeCAD, Part, math
from math import pi
import FreeCAD as App
import paramCarrierRoller
import paramSideRoller
import BeltCv
class Return:
    def __init__(self, obj):
        self.Type = ''
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)

    def execute(self, obj):
        buhin=obj.Name
        B=App.ActiveDocument.getObject(buhin).BeltWidth
        spec=App.ActiveDocument.getObject(buhin).spec
        spec2=App.ActiveDocument.getObject(buhin).spec2

        def r_roller(self):
            global c00
            global L
            global D
            if spec2=='RubberLining':
                sa=BeltCv.groller_lst[B]
                D=sa[0]
                d=sa[1]
                L=sa[4]
                l=sa[5]

            elif spec2=='PVCLining':
                sa=BeltCv.eroller_lst[B]
                D=sa[0]
                d=sa[1]
                L=sa[4]
                l=sa[5]

            c01= Part.makeCylinder(d/2,(L-l)/2,Base.Vector(0,0,0),Base.Vector(1,0,0),360)
            c02= Part.makeCylinder(D/2,l,Base.Vector((L-l)/2,0,0),Base.Vector(1,0,0),360)
            c03= Part.makeCylinder(d/2,(L-l)/2,Base.Vector((L+l)/2,0,0),Base.Vector(1,0,0),360)
            c00=c01.fuse(c02)
            c00=c00.fuse(c03)

        #リターンサポート
        def s_3(self):
            global c00
            global A0
            global B0
            global S
            global W0
            sa=BeltCv.Return_lst[B]
            S=sa[1]
            A0=sa[3]
            B0=sa[5]
            h=sa[6]
            W0=(A0-S)/2
            h0=h+15
            x0=W0-50
            y0=h0-30
            k=math.atan(x0/y0)/2
            c=4.5*math.tan(k)
            p1=(0,0,0)
            p2=(0,0,30)
            p3=(W0-50,0,h0)
            p4=(W0,0,h0)
            p5=(W0,0,h0-4.5)
            p6=(W0-50+c,0,h0-4.5)
            p7=(4.5,0,30-c)
            p8=(4.5,0,0)
            plst=[p1,p2,p3,p4,p5,p6,p7,p8,p1]
            pwire=Part.makePolygon(plst)
            pface = Part.Face(pwire)
            c00=pface.extrude(Base.Vector(0,B0,0))
            d=15
            p=25
            for i in range(2):
                if i==1:
                    p=25
                else:
                    p=85
                c01= Part.makeCylinder(d/2,4.5,Base.Vector(W0-25,p,h0-4.5),Base.Vector(0,0,1),360)
                c00=c00.cut(c01)
            p1=(0,0,-10)
            p2=(0,0,h0-4.5)
            p3=(0,25,0)
            p4=(0,B0-25,0)
            p5=(0,B0,h0-4.5)
            p6=(0,B0,-10)
            plst=[p1,p2,p3,p4,p5,p6,p1]
            pwire=Part.makePolygon(plst)
            pface = Part.Face(pwire)
            c01=pface.extrude(Base.Vector(B0,0,0))
            c00=c00.cut(c01)    

        def angle(self):
            global c00
            global A
            global r2
            A=float(sa1[0])
            B=float(sa1[1])
            t=float(sa1[2])
            r1=float(sa1[3])
            r2=float(sa1[4])
            x1=r2*(1-1/math.sqrt(2))
            x2=r2-x1
            y1=r1*(1-1/math.sqrt(2))
            y2=r1-y1
            y3=A-(r2+r1+t)
            x=t-r2
            p1=(0,0,0)
            p2=(0,0,A)
            p3=(0,x,A)
            p4=(0,t-x1,A-x1)
            p5=(0,t,A-r2)
            p6=(0,t,A-(r2+y3))
            p7=(0,t+y1,t+y1)
            p8=(0,t+r1,t)
            p9=(0,B-r2,t)
            p10=(0,B-x1,t-x1)
            p11=(0,B,t-r2)
            p12=(0,B,0)
            edge1=Part.makeLine(p1,p2)
            edge2=Part.makeLine(p2,p3)
            edge3=Part.Arc(Base.Vector(p3),Base.Vector(p4),Base.Vector(p5)).toShape()
            edge4=Part.makeLine(p5,p6)
            edge5=Part.Arc(Base.Vector(p6),Base.Vector(p7),Base.Vector(p8)).toShape()
            edge6=Part.makeLine(p8,p9)
            edge7=Part.Arc(Base.Vector(p9),Base.Vector(p10),Base.Vector(p11)).toShape()
            edge8=Part.makeLine(p11,p12)
            edge9=Part.makeLine(p12,p1)
            aWire=Part.Wire([edge1,edge2,edge3,edge4,edge5,edge6,edge7,edge8,edge9])
            pface=Part.Face(aWire)
            c00=pface

        def s_20(self):#自動調心サポート外
            global c00
            sa=BeltCv.groller_lst[B]
            D=sa[0]
            L=sa[2]
            sa=BeltCv.J_Carrier_lst[B]
            h=sa[4]
            p1=(0,-25,-(h-20))
            p2=(0,25,-(h-20))
            p3=(25,25,-(h-20))
            p4=(25,20.5,-(h-20))
            p5=(4.5,20.5,-(h-20))
            p6=(4.5,-20.5,-(h-20))
            p7=(25,-20.5,-(h-20))
            p8=(25,-25,-(h-20))
            plst=[p1,p2,p3,p4,p5,p6,p7,p8,p1]
            pwire=Part.makePolygon(plst)
            pface = Part.Face(pwire)
            c00=pface.extrude(Base.Vector(0,0,h))

        def angle2(self):
            global c00
            global A
            A=float(sa1[0])
            p1=(0,0,0)
            p2=(0,A,A)
            p3=(0,2*A,0)
            edge1=Part.makeLine(p1,p2)
            edge2=Part.makeLine(p2,p3)
            edge3=Part.makeLine(p3,p1)
            aWire=Part.Wire([edge1,edge2,edge3])
            pface=Part.Face(aWire)
            c00=pface

        def s_21(self):#自動調心サポート外
            global c00
            sa=BeltCv.groller_lst[B]
            D=sa[0]
            L=sa[2]
            sa=BeltCv.J_Carrier_lst[B]
            h=sa[4]
            p1=(0,-25,-(h-20))
            p2=(0,25,-(h-20))
            p3=(-25,25,-(h-20))
            p4=(-25,20.5,-(h-20))
            p5=(-4.5,20.5,-(h-20))
            p6=(-4.5,-20.5,-(h-20))
            p7=(-25,-20.5,-(h-20))
            p8=(-25,-25,-(h-20))
            plst=[p1,p2,p3,p4,p5,p6,p7,p8,p1]
            pwire=Part.makePolygon(plst)
            pface = Part.Face(pwire)
            c00=pface.extrude(Base.Vector(0,0,h))

        def channel(self):
            global c00
            H=float(sa1[0])
            B=float(sa1[1])
            t1=float(sa1[2])
            t2=float(sa1[3])
            r1=float(sa1[4])
            r2=float(sa1[5])
            Cy=float(sa1[8])*10
            s0=5
            s5=math.radians(s0)
            s45=math.radians(45)
            y1=r2*math.cos(s45)
            y2=r2*math.cos(s5)
            y3=r1*math.cos(s5)
            x1=r2*(1-math.cos(s45))
            x2=r2*math.sin(s5)
            x30=r2-x2
            x3=r1*math.sin(s5)
            x4=r1*math.cos(s45)
            x5=r1-x4
            x40=r1+x3
            x6=B-(x30+x40+t1)
            y6=x6*math.tan(s5)
            x7=Cy-(t1+x40)
            x8=x6-x7
            y7=x8*math.tan(s5)
            y8=t2-y7
            y4=y8-y2
            y10=y4+y2+y6
            y11=y4+y2+y6+x5
            y12=y4+y2+y6+x5+x4
            p1=(0,0,0)
            p2=(0,0,H)
            p3=(0,B,H)
            p4=(0,B,H-y4)
            p5=(0,B-x1,H-(y4+y1))
            p6=(0,B-x30,H-(y4+y2))
            p7=(0,t1+x40,H-y10)
            p8=(0,t1+x5,H-y11)
            p9=(0,t1,H-y12)
            p10=(0,t1,y12)
            p11=(0,t1+x5,y11)
            p12=(0,t1+x40,y10)
            p13=(0,B-x30,y4+y2)
            p14=(0,B-x1,y4+y1)
            p15=(0,B,y4)
            p16=(0,B,0)
            edge1=Part.makeLine(p1,p2)
            edge2=Part.makeLine(p2,p3)
            edge3=Part.makeLine(p3,p4)
            edge4=Part.Arc(Base.Vector(p4),Base.Vector(p5),Base.Vector(p6)).toShape()
            edge5=Part.makeLine(p6,p7)
            edge6=Part.Arc(Base.Vector(p7),Base.Vector(p8),Base.Vector(p9)).toShape()
            edge7=Part.makeLine(p9,p10)
            edge8=Part.Arc(Base.Vector(p10),Base.Vector(p11),Base.Vector(p12)).toShape()
            edge9=Part.makeLine(p12,p13)
            edge10=Part.Arc(Base.Vector(p13),Base.Vector(p14),Base.Vector(p15)).toShape()
            edge11=Part.makeLine(p15,p16)
            edge12=Part.makeLine(p16,p1)
            aWire=Part.Wire([edge1,edge2,edge3,edge4,edge5,edge6,edge7,edge8,edge9,edge10,edge11,edge12])
            pface=Part.Face(aWire)
            c00=pface 

        def rib(self):
            global c00
            sa=BeltCv.J_Return_lst[B]
            M0=sa[1]
            A0=sa[2]
            x1=30+(A0-M0)/2-6
            p1=(0,0,0)
            p2=(0,0,-x1)
            p3=(-x1,0,0)
            plst=[p1,p2,p3,p1]
            pwire=Part.makePolygon(plst)
            pface = Part.Face(pwire)
            c00=pface

        def sdr2(self):#自動調心サイドローラ
            global c00
            if float(B)<=500:
                La=185
            elif float(B)<=700:
                La=190
            else:
                La=195
            p1=(-5,-25,0)
            p2=(-5,-(La-40),0)
            p3=(-5,-(La-40),-30)
            p4=(-5,-25,-60)
            p5=(0,-(La-25),-30)
            plst=[p1,p2,p3,p4,p1]
            pwire=Part.makePolygon(plst)
            pface = Part.Face(pwire)
            c01=pface.extrude(Base.Vector(10,0,0))
            c02= Part.makeCylinder(15,30,Base.Vector(p5),Base.Vector(0,0,1),360)
            c01=c01.fuse(c02)
            s_roller2(self)
            c02=c00
            c02.Placement=App.Placement(App.Vector(0,-(La-25),L-30),App.Rotation(App.Vector(0,1,0),90))
            c00=c00.fuse(c01)
            c00=c00.fuse(c02)

        def s_roller2(self):
            global c00
            global L
            B='1000'
            #self.label_4.setText(QtGui.QApplication.translate("Dialog", str(spec), None))
            if spec2=='RubberLining':
                sa=BeltCv.sgroller2_lst[B]
                D=sa[0]
                d=sa[1]
                L=sa[2]
                l=sa[3]
            elif spec2=='PVCLining':
                sa=BeltCv.seroller2_lst[B]

                D=sa[0]
                d=sa[1]
                L=sa[2]
                l=sa[3]
            c01= Part.makeCylinder(D/2,l,Base.Vector(0,0,0),Base.Vector(1,0,0),360)
            c02= Part.makeCylinder((d+1)/2,(L-(l+30)),Base.Vector(l,0,0),Base.Vector(1,0,0),360)
            c03= Part.makeCylinder((d)/2,30,Base.Vector(L-30,0,0),Base.Vector(1,0,0),360)
            c00=c01.fuse(c02)
            c00=c00.fuse(c03)

        def brg(self):#軸受
            global c00
            p1=(-30,0,-40)
            p2=(-30,0,10)
            p3=(-10,0,10)
            p4=(-10,0,25)
            p5=(0,0,25)
            p6=(0,0,-40)
            plst=[p1,p2,p3,p4,p5,p6,p1]
            pwire=Part.makePolygon(plst)
            pface = Part.Face(pwire)
            c00=pface.revolve(Base.Vector(0,0.0,0),Base.Vector(0,0,1),360)

        def base_p2(self):
            global c00
            A=float(sa1[0])
            p1=(-32.5,-(2*A-10)/2,0)
            p2=(-32.5,(2*A-10)/2,0)
            p3=(32.5,(2*A-10)/2,0)
            p4=(32.5,-(2*A-10)/2,0)
            plst=[p1,p2,p3,p4,p1]
            pwire=Part.makePolygon(plst)
            pface = Part.Face(pwire)
            c00=pface.extrude(Base.Vector(0,0,6)) 


        if spec=='Fixed':
            r_roller(self)
            c1=c00
            c1.Placement=App.Placement(App.Vector(-L/2,0,0),App.Rotation(App.Vector(0,0,1),0))
            s_3(self)
            c01=c00
            sa=BeltCv.Return_lst[B]
            #A0=sa[3]
            B0=sa[5]
            c01.Placement=App.Placement(App.Vector(S/2,-B0/2,-15),App.Rotation(App.Vector(0,0,1),0))
            s_3(self)
            c02=c00
            c02.Placement=App.Placement(App.Vector(-S/2,B0/2,-15),App.Rotation(App.Vector(0,0,1),180))
            c01=c01.fuse(c02)
            c1=c1.fuse(c01)
            c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),90))
            obj.Shape=c1 
        elif spec=='Self_Aligning' :
            buhinmei='Self_Aligning_Return_'+B
            r_roller(self)
            c1=c00
            c1.Placement=App.Placement(App.Vector(-L/2,0,0),App.Rotation(App.Vector(0,0,1),0))
            sa=BeltCv.J_Return_lst[B]
            M0=sa[1]
            A0=sa[2]
            N0=sa[3]
            B0=sa[4]
            h=sa[5]
            H=sa[6]
            katakou=sa[7]
            katakou2=sa[8]
            sa1=BeltCv.angle_lst[katakou]
            A=float(sa1[0])
            angle(self)
            c01=c00
            x0=L/2+10
            y0=(D/2+20)
            c01.Placement=App.Placement(App.Vector(-x0,0,-y0),App.Rotation(App.Vector(1,0,0),-135))
            c011=c01.extrude(Base.Vector(L+20,0,0))
            c1=c1.fuse(c011)
            s_20(self)#サイドチャンネル
            c01=c00
            c01.Placement=App.Placement(App.Vector((x0-25),0,0),App.Rotation(App.Vector(1,0,0),0))
            
            angle2(self)#アングルカット
            c02=c00
            #Part.show(c02)
            c011=c02.extrude(Base.Vector((L+100),0,0))
            c011.Placement=App.Placement(App.Vector(-(x0+50),-A,-(y0+A)),App.Rotation(App.Vector(1,0,0),0))
            c01=c01.cut(c011)
            c1=c1.fuse(c01)
            
            s_21(self)
            c01=c00
            c01.Placement=App.Placement(App.Vector(-(x0-25),0,0),App.Rotation(App.Vector(1,0,0),0))
            c01=c01.cut(c011)
            c1=c1.fuse(c01)
            sa1=BeltCv.channel_lst[katakou2]
            H00=float(sa1[0])
            B00=float(sa1[1])
            channel(self)
            c01=c00
            c01.Placement=App.Placement(App.Vector(-(A0-12)/2,-H00/2,-(H-h)+B00),App.Rotation(App.Vector(1,0,0),-90))
            c02=c00.extrude(Base.Vector(A0-12,0,0))
            c1=c1.fuse(c02)
            #Part.show(c01)
            
            pface=Part.makePlane(6,H)
            c01=pface.extrude(Base.Vector(0,0,B0))
            c01.Placement=App.Placement(App.Vector(A0/2-6,-B0/2,h),App.Rotation(App.Vector(1,0,0),-90))
            c1=c1.fuse(c01)
            c01=pface.extrude(Base.Vector(0,0,B0))
            c01.Placement=App.Placement(App.Vector(-(A0/2),-B0/2,h),App.Rotation(App.Vector(1,0,0),-90))
            c1=c1.fuse(c01)
            x1=30+(A0-M0)/2-6
            pface=Part.makePlane(x1,B0)
            c01=pface.extrude(Base.Vector(0,0,6))
            c01.Placement=App.Placement(App.Vector((A0/2-x1-6),-B0/2,h-6),App.Rotation(App.Vector(1,0,0),0))
            c1=c1.fuse(c01)
            c01=pface.extrude(Base.Vector(0,0,6))
            c01.Placement=App.Placement(App.Vector(-(A0/2-6),-B0/2,h-6),App.Rotation(App.Vector(1,0,0),0))
            c1=c1.fuse(c01)
            rib(self)
            pface=c00
            c01=pface.extrude(Base.Vector(0,6,0))
            c01.Placement=App.Placement(App.Vector(A0/2-6,-(B0/2-3-x1),h-6),App.Rotation(App.Vector(1,0,0),0))
            c1=c1.fuse(c01)
            c01=pface.extrude(Base.Vector(0,6,0))
            c01.Placement=App.Placement(App.Vector(-(A0/2-6),-(B0/2-3-x1),h-6),App.Rotation(App.Vector(0,1,0),-90))
            c1=c1.fuse(c01)
            sdr2(self)
            c01=c00
            c01.Placement=App.Placement(App.Vector(x0-12.5,0,-10),App.Rotation(App.Vector(1,0,0),0))
            c1=c1.fuse(c01)
            c01=c00
            c01.Placement=App.Placement(App.Vector(-(x0-12.5),0,-10),App.Rotation(App.Vector(1,0,0),0))
            c1=c1.fuse(c01)
            brg(self)
            c01=c00
            c01.Placement=App.Placement(App.Vector(0,0,-(H-h)+B00),App.Rotation(App.Vector(0,0,1),0))
            c1=c1.fuse(c01)
            sa1=BeltCv.angle_lst[katakou]
            base_p2(self)
            c01=c00
            t=float(sa1[2])
            r2=float(sa1[4])
            A=float(sa1[0])
            L1=A-r2
            b=t-r2
            a=math.sqrt(L1**2+b**2)
            k=math.atan(b/L1)
            k1=45/(180/math.pi)-k
            y0=a*math.cos(k1)
            y=y0+r2
            c01.Placement=App.Placement(App.Vector(0,0,-(D/2+20+y+6)),App.Rotation(App.Vector(0,0,1),0))
            c1=c1.fuse(c01)
            d=15
            for i in range(2):
                if i==1:
                    x=-M0/2
                else:
                    x=M0/2
                c01= Part.makeCylinder(d/2,6,Base.Vector(x,-N0/2,h-6),Base.Vector(0,0,1),360)
                c02= Part.makeCylinder(d/2,6,Base.Vector(x,N0/2,h-6),Base.Vector(0,0,1),360)
                c1=c1.cut(c01)
                c1=c1.cut(c02)
            c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),90)) 
            obj.Shape=c1 
            

    

