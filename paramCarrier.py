from FreeCAD import Base
import FreeCADGui as Gui
import FreeCAD, Part, math
from math import pi
import FreeCAD as App
import paramCarrierRoller
import paramSideRoller
import BeltCv
class Carrier:
    def __init__(self, obj):
        self.Type = ''
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)

    def execute(self, obj):
        buhin=obj.Name
        B=App.ActiveDocument.getObject(buhin).BeltWidth
        spec=App.ActiveDocument.getObject(buhin).spec
        spec2=App.ActiveDocument.getObject(buhin).spec2

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

        def base_p(self):
            global c00
            global B0
            M=sa[0]
            N=sa[2]
            B0=sa[3]
            pface=Part.makePlane(50,B0)
            c00=pface.extrude(Base.Vector(0,0,6))
            d=15.0
            t=6.0
            for i in range(2):
                if i==1:
                    M=0
                c01= Part.makeCylinder(d/2,t,Base.Vector(25+M,(B0-N)/2,0),Base.Vector(0,0,1),360)
                c02= Part.makeCylinder(d/2,t,Base.Vector(25+M,(B0+N)/2,0),Base.Vector(0,0,1),360)
                c00=c00.cut(c01)
                c00=c00.cut(c02)  
        def c_roller(self):
            global c00
            global L
            if spec2=='RubberLining':
                sa=BeltCv.groller_lst[B]
                D=sa[0]
                d=sa[1]
                L=sa[2]
                l=sa[3]

            elif spec2=='PVCLining':
                sa=BeltCv.eroller_lst[B]
                D=sa[0]
                d=sa[1]
                L=sa[2]
                l=sa[3]
            print(D)
            c01= Part.makeCylinder(d/2,(L-l)/2,Base.Vector(0,0,0),Base.Vector(1,0,0),360)
            c02= Part.makeCylinder(D/2,l,Base.Vector((L-l)/2,0,0),Base.Vector(1,0,0),360)
            c03= Part.makeCylinder(d/2,(L-l)/2,Base.Vector((L+l)/2,0,0),Base.Vector(1,0,0),360)
            c00=c01.fuse(c02)
            c00=c00.fuse(c03) 
        def s_1(self):
            global c00
            sa=BeltCv.Carrier_lst[B]
            h=sa[4]
            k=20/(180/math.pi)
            y2=h-(y0/2+6)+16
            r1=15
            y3=(r1)*math.sin(k)
            x3=(r1)*math.cos(k)
            x4=(y2+y3)*math.tan(k)
            p1=(0,0,0)
            p2=(0,0,y2)
            p3=(r1,0,y2)
            p4=(r1+x3,0,y2+y3)
            p5=(r1+x3+x4,0,0)
            p6=(0,-25,0)
            p7=(0,25,0)
            p8=(4.5,25,0)
            p9=(4.5,-25,0)
            edge1 = Part.makeLine(p1,p2)
            edge2 = Part.makeCircle(r1, Base.Vector(p3), Base.Vector(0,1,0),180,-20)
            edge3 = Part.makeLine(p4,p5)
            edge4=Part.makeLine(p6,p7)
            edge5=Part.makeLine(p7,p8)
            edge6=Part.makeLine(p8,p9)
            edge7=Part.makeLine(p9,p6)
            aWire = Part.Wire([edge1,edge2,edge3])
            profile=Part.Wire([edge4,edge5,edge6,edge7])
            makeSolid=True
            isFrenet=True
            c00 = Part.Wire(aWire).makePipeShell([profile],makeSolid,isFrenet)   
        def s_2(self):
            global c00
            global x0
            sa=BeltCv.groller_lst[B]
            D=sa[0]
            L=sa[2]
            sa=BeltCv.Carrier_lst[B]
            h=sa[4]
            L2=L+2*(r0+10)
            k=20/(180/math.pi)
            x0=L2*math.cos(k)
            x1=(10+D)*math.sin(k)
            y2=h-(y0/2+6)
            y3=L2*math.sin(k)
            y4=D*math.cos(k)
            y5=10*math.cos(k)
            p1=(0,0,0)
            p2=(0,0,y2+y3-y4)
            p3=(-x1,0,y2+y3+y5)
            L00=50
            W00=20
            p4=(0,-L00/2,0)
            p5=(0,L00/2,0)
            p6=(W00,L00/2,0)
            p7=(W00,L00/2-4.5,0)
            p8=(4.5,L00/2-4.5,0)
            p9=(4.5,-(L00/2-4.5),0)
            p10=(W00,-(L00/2-4.5),0)
            p11=(W00,-L00/2,0)
            edge1=Part.makeLine(p1,p2)
            edge2=Part.makeLine(p2,p3)
            edge3=Part.makeLine(p4,p5)
            edge4=Part.makeLine(p5,p6)
            edge5=Part.makeLine(p6,p7)
            edge6=Part.makeLine(p7,p8)
            edge7=Part.makeLine(p8,p9)
            edge8=Part.makeLine(p9,p10)
            edge9=Part.makeLine(p10,p11)
            edge10=Part.makeLine(p11,p4)
            aWire=Part.Wire([edge1,edge2])
            profile=Part.Wire([edge3,edge4,edge5,edge6,edge7,edge8,edge9,edge10])
            makeSolid=True
            isFrenet=True
            c00 = Part.Wire(aWire).makePipeShell([profile],makeSolid,isFrenet)  
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
        def s_200(self):#サポートカッター
            global c00
            p1=(0,0,0)
            p2=(0,-A,-A)
            p3=(0,A,-A)
            plst=[p1,p2,p3,p1]
            pwire=Part.makePolygon(plst)
            pface = Part.Face(pwire)
            c00=pface                 
        def s_10(self):#自動調心サポート内
            global c00
            sa=BeltCv.J_Carrier_lst[B]
            h=float(sa[4])
            k=float(20/(180/math.pi))
            y2=h-(y0/2+6)+16
            r1=10
            x3=(h-30)*math.sin(k)
            z3=(h-15)*math.cos(k)
            p1=(-r1,0,-(h-40))
            p2=(-r1,0,0)
            p3=(-r1,0,15)
            p4=(0,0,r1+15)
            p5=(r1*math.cos(k),0,15+r1*math.sin(k))
            p6=(r1*math.cos(k)+x3,0,-(z3-r1*math.sin(k)-20))
            p7=(-(r1+4.5),-25,0)
            p8=(-(r1+4.5),25,0)
            p9=(-r1,25,0)
            p10=(-r1,-25,0)
            edge1 = Part.makeLine(p1,p2)
            edge2 = Part.makeLine(p2,p3)
            edge3=Part.Arc(Base.Vector(p3),Base.Vector(p4),Base.Vector(p5)).toShape()
            edge4 = Part.makeLine(p5,p6)
            plst=[p7,p8,p9,p10,p7]
            profile=Part.makePolygon(plst)
            aWire = Part.Wire([edge1,edge2,edge3,edge4])
            makeSolid=True
            isFrenet=True
            c00 = Part.Wire(aWire).makePipeShell([profile],makeSolid,isFrenet)

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

        def s_roller(self):
            global c00
            global L
            B='1000'
            if spec2=='RubberLining':
                sa=BeltCv.sgroller_lst[B]
                D=sa[0]
                d=sa[1]
                L=sa[2]
                l=sa[3]
            elif spec2=='PVCLining':
                sa=BeltCv.seroller_lst[B]
                D=sa[0]
                d=sa[1]
                L=sa[2]
                l=sa[3]
            c01= Part.makeCylinder(D/2,l,Base.Vector(0,0,0),Base.Vector(1,0,0),360)
            c02= Part.makeCylinder((d+1)/2,(L-(l+30)),Base.Vector(l,0,0),Base.Vector(1,0,0),360)
            c03= Part.makeCylinder((d)/2,30,Base.Vector(L-30,0,0),Base.Vector(1,0,0),360)
            c00=c01.fuse(c02)
            c00=c00.fuse(c03)
            
            

        def sdr(self):#自動調心サイドローラ
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
            s_roller(self)
            c02=c00
            c02.Placement=App.Placement(App.Vector(0,-(La-25),L-30),App.Rotation(App.Vector(0,1,0),90))
            #Part.show(c02)
            c00=c01.fuse(c02)
            #c00=c00.fuse(c02)
            #c00=c01
            

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
            global y
            sa=BeltCv.Carrier_lst[B]
            A0=sa[1]
            B0=sa[3]
            h=sa[4]
            katakou=sa[7]
            
            sa1=BeltCv.angle_lst[katakou]
            angle(self)
            c01=c00

            c01.Placement=App.Placement(App.Vector(-A0/2,0,0),App.Rotation(App.Vector(1,0,0),-135))
            c011=c01.extrude(Base.Vector(A0,0,0))
            base_p(self)
            c02=c00
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
            c02.Placement=App.Placement(App.Vector(-A0/2,-B0/2,-y-t),App.Rotation(App.Vector(0,0,1),0))
            c1=c011.fuse(c02)
            base_p(self)
            c02=c00
            c02.Placement=App.Placement(App.Vector(-A0/2+A0-50,-B0/2,-y-t),App.Rotation(App.Vector(0,0,1),0))
            c1=c1.fuse(c02)
            c_roller(self)
            c01=c00
            c01.Placement=App.Placement(App.Vector(-A0/2+(A0-L)/2,0,-y-t+h),App.Rotation(App.Vector(0,0,1),0))
            c1=c1.fuse(c01)
            c_roller(self)
            c01=c00
            k=20/(180/math.pi)
            h0=(L+5)*math.sin(k)
            r0=7.5
            x1=r0*math.cos(k)
            y1=r0*math.sin(k)
            c01.Placement=App.Placement(App.Vector(-A0/2+(A0/2-0.5*L)-r0*(1+math.cos(k)),0,-y-t+h+y1),App.Rotation(App.Vector(0,1,0),-160))
            c1=c1.fuse(c01)
            c_roller(self)
            c01=c00
            c01.Placement=App.Placement(App.Vector(-A0/2+(A0/2+0.5*L)+r0*(1+math.cos(k)),0,-y-t+h+y1),App.Rotation(App.Vector(0,1,0),-20))
            c1=c1.fuse(c01)
            s_1(self)
            c01=c00
            c01.Placement=App.Placement(App.Vector(-A0/2+(A0/2+0.5*L-10),0,-(y0/2+6)),App.Rotation(App.Vector(0,0,1),0))
            s_1(self)
            c02=c00
            c02.Placement=App.Placement(App.Vector(-A0/2+(A0/2-0.5*L+10),0,-(y0/2+6)),App.Rotation(App.Vector(0,0,1),180))
            if float(B)<=700:
                ds=2*r0
            elif float(B)>700:
                ds=1.0*r0
            s_2(self)
            c03=c00
            sa=BeltCv.Carrier_lst[B]
            L2=L+2*(r0+10)
            k=20/(180/math.pi)
            x0=L2*math.cos(k)
            x2=L/2+r0+10+x0
            c03.Placement=App.Placement(App.Vector(-A0/2+(A0/2+x2-ds),0,-(y0/2+6)),App.Rotation(App.Vector(0,0,1),0))
            s_2(self)
            c04=c00
            x2=L/2+r0+10+x0
            c04.Placement=App.Placement(App.Vector(-A0/2+(A0/2-(x2-ds)),0,-(y0/2+6)),App.Rotation(App.Vector(0,0,1),180))
            c01=c01.fuse(c02)
            c01=c01.fuse(c03)
            c01=c01.fuse(c04)
            angle2(self)
            c021=c00
            c021.Placement=App.Placement(App.Vector(-A0/2,-A,-A),App.Rotation(App.Vector(0,0,1),0))
            c02=c021.extrude(Base.Vector(A0,0,0))
            c01=c01.cut(c02)
            c1=c1.fuse(c01)
            obj.Shape=c1  
        elif spec=='Self_Aligning':
            sa=BeltCv.J_Carrier_lst[B]
            A0=float(sa[1])
            B0=sa[3]
            M0=sa[0]
            N0=sa[2]
            h=sa[4]
            katakou=sa[7]
            katakou2=sa[8]
            g=sa[9]
            sa1=BeltCv.angle_lst[katakou]
            A=sa1[0]
            t=sa1[2]
            angle(self)
            c01=c00
            c01.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),90))
            c011=c01.extrude(Base.Vector(0,B0,0))
            c011.Placement=App.Placement(App.Vector(-(A0/2-A),-B0/2,0),App.Rotation(App.Vector(0,1,0),-90))
            angle(self)
            c02=c00
            c02.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),90))
            c012=c02.extrude(Base.Vector(0,B0,0))
            c012.Placement=App.Placement(App.Vector((A0/2-A),-B0/2,0),App.Rotation(App.Vector(0,1,0),-180))
            c011=c011.fuse(c012)
            c1=c011
            sa1=BeltCv.channel_lst[katakou2]
            channel(self)
            B00=float(sa1[1])
            H00=float(sa1[0])
            c02=c00
            y00=(A-B00)/2
            c02.Placement=App.Placement(App.Vector(-A0/2+A,-H00/2,-y00),App.Rotation(App.Vector(1,0,0),-90))
            c012=c02.extrude(Base.Vector(A0-2*A,0,0))
            c1=c1.fuse(c012)
            d=15
            for i in range(2):
                if i==1:
                    x=-M0/2
                else:
                    x=M0/2
                c01= Part.makeCylinder(d/2,t,Base.Vector(x,-N0/2,-t),Base.Vector(0,0,1),360)
                c02= Part.makeCylinder(d/2,t,Base.Vector(x,N0/2,-t),Base.Vector(0,0,1),360)
                c1=c1.cut(c01)
                c1=c1.cut(c02)
            sa1=BeltCv.angle_lst[katakou]
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
            angle(self)
            c01=c00
            L0=A0/3
            c01.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(1,0,0),-135))
            c011=c01.extrude(Base.Vector(L0+200,0,0))
            c011.Placement=App.Placement(App.Vector(-(L0/2+100),0,y+20),App.Rotation(App.Vector(1,0,0),0))
            k0=math.radians(20)
            p1=(L0/2,-65,y+20)
            p2=(L0/2+100,-65,y+20)
            p3=(L0/2+100,-65,20)
            p4=(L0/2+y*math.tan(k0/2),-65,20)
            p5=(L0/2+y*math.tan(k0)-100*math.cos(k0),-65,20-100*math.sin(k0))
            p6=(L0/2-100*math.cos(k0),-65,y+20-100*math.sin(k0))
            p7=(-L0/2,-65,y+20)
            p8=(-(L0/2+100),-65,y+20)
            p9=(-(L0/2+100),-65,20)
            p10=(-(L0/2+y*math.tan(k0/2)),-65,20)
            p11=(-(L0/2-100*math.cos(k0)),-65,y+20-100*math.sin(k0))
            p12=(-(L0/2+y*math.tan(k0)-100*math.cos(k0)),-65,20-100*math.sin(k0))
            angle(self)
            c02=c00
            c02.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(1,0,0),-135))
            c021=c01.extrude(Base.Vector(L0+100,0,0))
            c021.Placement=App.Placement(App.Vector(L0/2-100*math.cos(k0),0,y+20-100*math.sin(k0)),App.Rotation(App.Vector(0,1,0),-20))
            angle(self)
            c05=c00
            c05.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(1,0,0),-135))
            c022=c05.extrude(Base.Vector(-(L0+100),0,0))
            c022.Placement=App.Placement(App.Vector(-(L0/2-100*math.cos(k0)),0,y+20-100*math.sin(k0)),App.Rotation(App.Vector(0,1,0),20))
            plst=[p1,p2,p3,p4,p1]
            pwire=Part.makePolygon(plst)
            pface = Part.Face(pwire)
            c03=pface.extrude(Base.Vector(0,130,0))
            c011=c011.cut(c03)
            s_200(self)
            pface=c00
            c011a=pface.extrude(Base.Vector(L0,0,0))
            c011a.Placement=App.Placement(App.Vector(-L0/2,0,20+y0/math.cos(k0)),App.Rotation(App.Vector(0,0,1),0))
            c011b=pface.extrude(Base.Vector(L0,0,0))
            c011b.Placement=App.Placement(App.Vector(L0/2,0,20+y0/math.cos(k0)),App.Rotation(App.Vector(0,1,0),-20))
            c011c=pface.extrude(Base.Vector(L0,0,0))
            c011c.Placement=App.Placement(App.Vector(-1.4*L0,0,20+y0/math.cos(k0)+L0*math.sin(k0)),App.Rotation(App.Vector(0,1,0),20))
            c011a=c011a.fuse(c011b)
            c011a=c011a.fuse(c011c)
            c1=c1.fuse(c011)
            plst=[p1,p4,p5,p6,p1]
            pwire=Part.makePolygon(plst)
            pface = Part.Face(pwire)
            c04=pface.extrude(Base.Vector(0,130,0))
            c021=c021.cut(c04)
            c1=c1.fuse(c021)
            plst=[p7,p8,p9,p10,p7]
            pwire=Part.makePolygon(plst)
            pface = Part.Face(pwire)
            c06=pface.extrude(Base.Vector(0,130,0))
            c1=c1.cut(c06)
            plst=[p7,p11,p12,p10,p7]
            pwire=Part.makePolygon(plst)
            pface = Part.Face(pwire)
            c07=pface.extrude(Base.Vector(0,130,0))
            c022=c022.cut(c07)
            c1=c1.fuse(c022)
            c_roller(self)
            Lx=L
            c01=c00
            c01.Placement=App.Placement(App.Vector(-L/2,0,h),App.Rotation(App.Vector(0,0,1),0))
            c1=c1.fuse(c01)
            r0=7.5
            c_roller(self)
            c01=c00
            c01.Placement=App.Placement(App.Vector(L/2+(r0)*(1+math.cos(k0)),0,h+r0*math.sin(k0)),App.Rotation(App.Vector(0,1,0),-20))
            c1=c1.fuse(c01)
            c_roller(self)
            c01=c00
            c01.Placement=App.Placement(App.Vector(-(L/2+(r0)*(1+math.cos(k0))),0,h+r0*math.sin(k0)),App.Rotation(App.Vector(0,1,0),-160))
            c1=c1.fuse(c01)
            s_10(self)#サポート内
            c01=c00
            c01.Placement=App.Placement(App.Vector(L/2+5,0,h),App.Rotation(App.Vector(0,0,1),0))
            c01=c01.cut(c011a)
            c1=c1.fuse(c01)
            s_10(self)#サポート内
            c01=c00
            c01.Placement=App.Placement(App.Vector(-(L/2+5),0,h),App.Rotation(App.Vector(0,0,1),180))
            c01=c01.cut(c011a)
            c1=c1.fuse(c01)
            if float(B)<=700:
                m00=7.5
            else:
                m00=7.5
            s_20(self)#サポート外
            x0=L/2+r0+r0*math.cos(k0)+L*math.cos(k0)-m00*math.cos(k0)
            y0=h+r0*math.sin(k0)+L*math.sin(k0)-m00*math.sin(k0)
            c01=c00
            c01.Placement=App.Placement(App.Vector(x0,0,y0),App.Rotation(App.Vector(0,1,0),-20))
            c01=c01.cut(c011a)
            c1=c1.fuse(c01)
            s_21(self)#サポート外
            c01=c00
            c01.Placement=App.Placement(App.Vector(-x0,0,y0),App.Rotation(App.Vector(0,1,0),20))
            c01=c01.cut(c011a)
            c1=c1.fuse(c01)
            base_p2(self)
            c01=c00
            c01.Placement=App.Placement(App.Vector(0,0,20-6),App.Rotation(App.Vector(0,1,0),0))
            c1=c1.fuse(c01)
            brg(self)
            c01=c00
            c1=c1.fuse(c01)
            sdr(self)
            c01=c00
            x0=Lx/2+r0+r0*math.cos(k0)+Lx*math.cos(k0)+12.5
            y0=h+r0*math.sin(k0)+Lx*math.sin(k0)-20
            c01.Placement=App.Placement(App.Vector(x0,0,y0),App.Rotation(App.Vector(0,1,0),-20))
            c1=c1.fuse(c01)
            c01=c00
            c01.Placement=App.Placement(App.Vector(-x0,0,y0),App.Rotation(App.Vector(0,1,0),20))
            c1=c1.fuse(c01)
            c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),90))
            obj.Shape=c1  
    
            

    

