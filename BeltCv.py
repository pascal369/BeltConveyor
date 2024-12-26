# -*- coding: utf-8 -*-
import os
import sys
import csv
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui
from PySide import QtUiTools
from PySide import QtCore
from FreeCAD import Base
import FreeCAD, Part, math
from math import pi

belt_haba=['400','450','500','600','700','750','800','900','1000',]
belt_buhin=['Assy','Belt','Pulleys','MotorPulley','Carrier','Return','CarrierRoller','ReturnRoller',
            'SideRoller','Take-UP','Take-UpAssy','PillowBlock',]
spec_roller=['RubberLining','PVCLining',]
groller_dia=['99','124']
eroller_dia=['95','121']
carrier_spec=['Fixed','Self_Aligning']
roller_spec=['SteelPipe',]
takeup_dia=['20','25','30','35','40','45','50']
pillow_spec=['UCP204FC','UCP205FC','UCP206FC','UCP207FC','UCP208FC',
             'UCP204FCD','UCP205FCD','UCP206FCD','UCP207FCD','UCP208FCD',]


#ゴムライニング             キャリヤ　　　　　　　リターン
#ベルト幅B　　ローラ径D　軸径d　軸長L　ローラ長l　軸長L　ローラ長l
groller_lst={
'400':(   99,    19,   175, 145,    505, 460),
'450':(   99,    19,   195, 165,    555, 510),
'500':(   99,    19,   210, 180,    605, 560),
'600':(   99,    19,   240, 210,    705, 660),
'700':(   99,    19,   280, 250,    805, 760),
'750':(  124,    19,   295, 265,    905, 850),
'800':(  124,    19,   310, 280,    955, 900),
'900':(  124,    19,   345, 315,   1055,1000),
'1000':( 124,    19,   375, 345,   1155,1100),
}
#塩ビライニング　　　　　　　　　　　キャリヤ　　　　　　　リターン
#ベルト幅B　　ローラ径D　軸径d　軸長L　ローラ長l　軸長L　ローラ長l
eroller_lst={
'400':(     95,    19,   175, 145,    505, 460),
'450':(     95,    19,   195, 165,    555, 510),
'500':(     95,    19,   210, 180,    605, 560),
'600':(     95,    19,   240, 210,    705, 660),
'700':(     95,    19,   280, 250,    805, 760),
'750':(  120.5,    19,   295, 265,    905, 850),
'800':(  120.5,    19,   310, 280,    955, 900),
'900':(  120.5,    19,   345, 315,   1055,1000),
'1000':( 120.5,    19,   375, 345,   1155,1100),
}

#サイドローラ              ゴムライニング
#ベルト幅B　　ローラ径D　軸径d　軸長L　ローラ長l
sgroller_lst={
'1000':(   86,    16,   165, 120),
}

#サイドローラ              ゴムライニング
#ベルト幅B　　ローラ径D　軸径d　軸長L　ローラ長l
sgroller2_lst={
'1000':(   86,    16,   140, 100),
}

#サイドローラ              塩ビライニング
#ベルト幅B　　ローラ径D　軸径d　軸長L　ローラ長l
seroller_lst={
'1000':(   81,    16,   165, 120),
}

#サイドローラ              塩ビライニング
#ベルト幅B　　ローラ径D　軸径d　軸長L　ローラ長l
seroller2_lst={
'1000':(   81,    16,   140, 100),
}

#ｼﾘｰｽﾞ,寸法(mm),,,,,断面積,質量,重心(cm),,断面2次ﾓｰﾒﾝﾄ(cm4),,,断面2次半径,,,断面係数(cm3),
#          A, B, t,r1, r2, (cm2),(kg/m),Cx,  Cy,  Ix,  Iy,  最小Iv,ix,  iy,  最小iv,Zx,  Zy
angle_lst={
'L6x50':(50,50,6,6.5,4.5,5.644,4.43,1.44,1.44,12.60,12.60,5.24,1.50,1.50,0.96,3.55,3.55),
'L6x65':(65,65,6,8.5,4.0,7.527,5.91,1.81,1.81,29.40,29.40,12.10,1.98,1.98,1.27,6.27,6.27),
'L6x75':(75,75,6,8.5,4.0,8.727,6.85,2.06,2.06,46.10,46.10,19.00,2.30,2.30,1.47,8.47,8.47),
}

#ｼﾘｰｽﾞ,寸法(mm),,,,,,断面積,質量,重心,断面2次ﾓｰﾒﾝﾄ(cm4),,断面2次半径(cm),,断面係数(cm3),
#          H, B, t1,t2,r1,r2,(cm2),(kg/m),Cy(cm),Ix,  Iy,  ix,  iy,  Zx,  Zy
channel_lst={
'C100x50x5':(100,50,5,7.5,8,4,11.92,9.36,1.54,188,26,3.97,1.48,37.6,7.52),
'C125x65x6':(125,65,6,8,8,4,17.11,13.4,1.9,424,61.8,4.98,1.9,67.8,13.4),
}

#キャリヤ
#ベルト幅B　　　M　  A0    N   B0   h    H    L0
Carrier_lst={
'400':(   640, 690, 140,190, 125, 229, 469, 'L6x50'),
'450':(   690, 740, 140,190, 125, 236, 526, 'L6x50'),
'500':(   740, 790, 140,190, 125, 241, 569, 'L6x50'),
'600':(   840, 890, 150,200, 140, 266, 656, 'L6x65'),
'700':(   940, 990, 150,200, 140, 280, 771, 'L6x65'),
'750':(  1040,1090, 160,210, 150, 305, 806, 'L6x75'),
'800':(  1090,1140, 160,210, 150, 310, 849, 'L6x75'),
'900':(  1190,1240, 160,210, 150, 322, 949, 'L6x75'),
'1000':( 1290,1340, 160,210, 150, 332,1036, 'L6x75'),
}

#自動調心キャリヤ
#ベルト幅B　　　M　  A0    N   B0   h    H    L0
J_Carrier_lst={
'400':(   640, 690, 140,190, 130, 232, 471, 'L6x50','C100x50x5'),
'450':(   690, 740, 140,190, 130, 239, 528, 'L6x50','C100x50x5'),
'500':(   740, 790, 140,190, 130, 244, 571, 'L6x50','C100x50x5'),
'600':(   840, 890, 150,200, 145, 269, 658, 'L6x65','C100x50x5'),
'700':(   940, 990, 150,200, 145, 283, 773, 'L6x65','C100x50x5'),
'750':(  1040,1090, 160,210, 155, 310, 807, 'L6x75','C125x65x6'),
'800':(  1090,1140, 160,210, 155, 315, 851, 'L6x75','C125x65x6'),
'900':(  1190,1240, 160,210, 155, 327, 951, 'L6x75','C125x65x6'),
'1000':( 1290,1340, 160,210, 155, 337,1038, 'L6x75','C125x65x6'),
}

#リターン
#ベルト幅B　l　   S     M     A0    N    B0    h
Return_lst={
'400':(   460,  480,  640,  690,  60,  110,  110),
'450':(   510,  530,  690,  740,  60,  110,  110),
'500':(   560,  580,  740,  790,  60,  110,  110),
'600':(   660,  680,  840,  890,  60,  110,  110),
'700':(   760,  780,  940,  990,  60,  110,  110),
'750':(   850,  880, 1040, 1090,  60,  110,  110),
'800':(   900,  930, 1090, 1140,  60,  110,  110),
'900':(  1000, 1030, 1190, 1240,  60,  110,  110),
'1000':( 1100, 1130, 1290, 1340,  60,  110,  110),
}

#自動調心リターン
#ベルト幅B　l　    M     A0    N    B0    h　 　H
J_Return_lst={
'400':(   460,   640,  690,  60,  110,  110, 295,  'L6x50',  'C100x50x5'),
'450':(   510,   690,  740,  60,  110,  110, 295,  'L6x50',  'C100x50x5'),
'500':(   560,   740,  790,  60,  110,  110, 295,  'L6x50',  'C100x50x5'),
'600':(   660,   840,  890,  60,  110,  110, 310,  'L6x65',  'C100x50x5'),
'700':(   760,   940,  990,  60,  110,  110, 310,  'L6x65',  'C100x50x5'),
'750':(   850,  1040, 1090,  60,  130,  125, 320,  'L6x50',  'C125x65x6'),
'800':(   900,  1090, 1140,  60,  130,  110, 345,  'L6x75',  'C125x65x6'),
'900':(  1000,  1190, 1240,  60,  130,  110, 345,  'L6x75',  'C125x65x6'),
'1000':( 1100,  1290, 1340,  60,  130,  110, 345,  'L6x75',  'C125x65x6'),
}


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(355, 150)
        Dialog.move(1000, 0)
         #ベルト幅BeltWidh
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(11, 37, 61, 16))
        self.label.setObjectName("label")
        self.comboBox = QtGui.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(80, 37, 130, 20))
        self.comboBox.setObjectName("comboBox")
        #部品parts
        self.comboBox_2 = QtGui.QComboBox(Dialog)
        self.comboBox_2.setGeometry(QtCore.QRect(80, 11, 130, 20))
        self.comboBox_2.setObjectName("comboBox_2")
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(11, 11, 61, 16))
        self.label_2.setObjectName("label_2")
        #仕様Spec
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(11, 63, 61, 16))
        self.label_3.setObjectName("label_3")
        self.comboBox_3 = QtGui.QComboBox(Dialog)
        self.comboBox_3.setGeometry(QtCore.QRect(80, 63, 130, 20))
        self.comboBox_3.setObjectName("comboBox_3")
        #仕様2Spec2
        self.comboBox_4 = QtGui.QComboBox(Dialog)
        self.comboBox_4.setGeometry(QtCore.QRect(80, 90, 130, 20))
        self.comboBox_4.setObjectName("comboBox_4")
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(12, 90, 51, 16))
        self.label_6.setObjectName("label_6")
        #png
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(225, 10, 121, 101))
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        
        #実行
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(240, 120, 75, 23))
        self.pushButton.setObjectName("pushButton")

        self.comboBox.addItems(belt_haba)
        self.comboBox_2.addItems(belt_buhin)

        self.comboBox_2.setCurrentIndex(1)
        self.comboBox_2.currentIndexChanged[int].connect(self.onSpec)
        self.comboBox_2.setCurrentIndex(0)

        self.comboBox_3.currentIndexChanged[int].connect(self.onSpec2)

        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", 'Belt Conveyor', None))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Belt Width", None))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Parts", None))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Spec", None))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Execution", None))
        self.label_6.setText(QtGui.QApplication.translate("Dialog", "Spec2", None))

    def onSpec(self):
        global buhin
        global pic
        buhin=self.comboBox_2.currentText()
        spec=self.comboBox_3.currentText()
        
        if buhin=='CarrierRoller':
            self.comboBox.show()
            self.comboBox_3.show()
            self.comboBox_4.show()
            pic=buhin+'.png' 
            ta=spec_roller
            tb=roller_spec
        elif buhin=='ReturnRoller':
            self.comboBox.show()
            self.comboBox_3.show()
            self.comboBox_4.show()
            pic=buhin+'.png' 
            ta=spec_roller
            tb=roller_spec
        elif buhin=='SideRoller':
            self.comboBox.show()
            self.comboBox_3.show()
            self.comboBox_4.show()
            pic=buhin+'.png' 
            ta=spec_roller
            tb=roller_spec
        elif buhin=='Carrier':
            self.comboBox.show()
            self.comboBox_3.show()
            self.comboBox_4.show()
            ta=spec_roller
            tb=carrier_spec
        elif buhin=='Return':
            self.comboBox.show()
            self.comboBox_3.show()
            self.comboBox_4.show()
            ta=spec_roller
            tb=carrier_spec
        elif buhin=='Pulleys':
            self.comboBox_2.show()
            self.comboBox_3.hide()
            self.comboBox_4.hide()
            pic='Pulleys.png'
        elif buhin=='MotorPulley':  
            self.comboBox.show()
            self.comboBox_3.hide()
            self.comboBox_4.hide()
            pic=buhin+'.png'
        elif buhin=='Take-UP':   
            self.comboBox.show()
            self.comboBox_2.show()
            self.comboBox_3.show()
            #self.comboBox_4.show()
            pic=buhin+'.png'   
            tb=takeup_dia
        elif buhin=='PillowBlock': 
            self.comboBox.show() 
            self.comboBox_3.show()
            self.comboBox_4.hide() 
            pic=buhin+'.png'   
            tb=pillow_spec 
        elif buhin=='Assy':  
            
            self.comboBox.hide() 
            self.comboBox_3.hide()  
            self.comboBox_4.hide()  
            pic='Belt_Assy.png'
            print(buhin)
            #self.comboBox_3.clear()
        elif buhin=='Belt':  
            self.comboBox.hide() 
            self.comboBox_3.hide()  
            self.comboBox_4.hide()   
            pic='Belt.png'
        elif buhin=='Take-UpAssy':
            self.comboBox.hide() 
            self.comboBox_3.hide()  
            self.comboBox_4.hide()  
            pic='takeupAssy.png'
        self.comboBox_3.clear()    
        try:
            self.comboBox_3.addItems(tb)
        except:
            pass    
        
        self.comboBox_4.clear()
        try:
            self.comboBox_4.addItems(ta)
        except:
            pass

        spec=self.comboBox_3.currentText()
        if buhin=='Carrier':
            pic=buhin +'_' + spec + '.png'
        elif buhin=='Return':
            pic=buhin +'_' + spec + '.png'
        #else:
        #    pic=buhin  + '.png'
        #print(buhin)
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "Belt_data",'png_data',pic)
        self.label_5.setPixmap(QtGui.QPixmap(joined_path))

    def onSpec2(self):#部品
        spec2=self.comboBox_3.currentText()
        #print(buhin)
        #print(spec2)

        if buhin=='Carrier':
            pic=buhin +'_'  + spec2 + '.png'
        elif buhin=='Return':
            pic=buhin+'_'  + spec2 + '.png'
        else:
            pic=buhin + '.png'
        #print(pic)    
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "Belt_data",'png_data',pic)
        self.label_5.setPixmap(QtGui.QPixmap(joined_path))

    def onSpec3(self):
        spec2=self.comboBox_3.currentText()
        #spec3=self.comboBox_4.currentText()
        if buhin=='Carrier_':
            pic=buhin  + spec2 + '.png'
        elif buhin=='Return_':
            pic=buhin  + spec2 + '.png'
        else:
            pic=buhin  + '.png'
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "Belt_data",'png_data',pic)
        self.label_5.setPixmap(QtGui.QPixmap(joined_path))

    def create(self):

        global D
        global d
        global L
        global l
        global spec
        global buhin

        buhin=self.comboBox_2.currentText()
        B=self.comboBox.currentText()
        spec=self.comboBox_4.currentText()
       
        def c_roller(self):
            global c00
            global L
            #self.label_4.setText(QtGui.QApplication.translate("Dialog", str(spec), None))
            if spec=='RubberLining':
                sa=groller_lst[B]
                D=sa[0]
                d=sa[1]
                L=sa[2]
                l=sa[3]

            elif spec=='PVCLining':
                sa=eroller_lst[B]
                D=sa[0]
                d=sa[1]
                L=sa[2]
                l=sa[3]

            c01= Part.makeCylinder(d/2,(L-l)/2,Base.Vector(0,0,0),Base.Vector(1,0,0),360)
            c02= Part.makeCylinder(D/2,l,Base.Vector((L-l)/2,0,0),Base.Vector(1,0,0),360)
            c03= Part.makeCylinder(d/2,(L-l)/2,Base.Vector((L+l)/2,0,0),Base.Vector(1,0,0),360)
            c00=c01.fuse(c02)
            c00=c00.fuse(c03)
            
        def r_roller(self):
            global c00
            global L
            global D
            if spec=='RubberLining':
                sa=groller_lst[B]
                D=sa[0]
                d=sa[1]
                L=sa[4]
                l=sa[5]

            elif spec=='PVCLining':
                sa=eroller_lst[B]
                D=sa[0]
                d=sa[1]
                L=sa[4]
                l=sa[5]

            c01= Part.makeCylinder(d/2,(L-l)/2,Base.Vector(0,0,0),Base.Vector(1,0,0),360)
            c02= Part.makeCylinder(D/2,l,Base.Vector((L-l)/2,0,0),Base.Vector(1,0,0),360)
            c03= Part.makeCylinder(d/2,(L-l)/2,Base.Vector((L+l)/2,0,0),Base.Vector(1,0,0),360)
            c00=c01.fuse(c02)
            c00=c00.fuse(c03)

        def s_roller(self):
            global c00
            global L
            B='1000'
            if spec=='RubberLining':
                sa=sgroller_lst[B]
                D=sa[0]
                d=sa[1]
                L=sa[2]
                l=sa[3]
            elif spec=='PVCLining':
                sa=seroller_lst[B]
                D=sa[0]
                d=sa[1]
                L=sa[2]
                l=sa[3]
            c01= Part.makeCylinder(D/2,l,Base.Vector(0,0,0),Base.Vector(1,0,0),360)
            c02= Part.makeCylinder((d+1)/2,(L-(l+30)),Base.Vector(l,0,0),Base.Vector(1,0,0),360)
            c03= Part.makeCylinder((d)/2,30,Base.Vector(L-30,0,0),Base.Vector(1,0,0),360)
            c00=c01.fuse(c02)
            c00=c00.fuse(c03)
           

        def s_roller2(self):
            global c00
            global L
            B='1000'
            #self.label_4.setText(QtGui.QApplication.translate("Dialog", str(spec), None))
            if spec=='RubberLining':
                sa=sgroller2_lst[B]
                D=sa[0]
                d=sa[1]
                L=sa[2]
                l=sa[3]
            elif spec=='PVCLining':
                sa=seroller2_lst[B]

                D=sa[0]
                d=sa[1]
                L=sa[2]
                l=sa[3]
            c01= Part.makeCylinder(D/2,l,Base.Vector(0,0,0),Base.Vector(1,0,0),360)
            c02= Part.makeCylinder((d+1)/2,(L-(l+30)),Base.Vector(l,0,0),Base.Vector(1,0,0),360)
            c03= Part.makeCylinder((d)/2,30,Base.Vector(L-30,0,0),Base.Vector(1,0,0),360)
            c00=c01.fuse(c02)
            c00=c00.fuse(c03)

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
        #サポート内
        def s_1(self):
            global c00
            sa=Carrier_lst[B]
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

        def s_10(self):#自動調心サポート内
            global c00
            sa=J_Carrier_lst[B]
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

        #サポート外
        def s_2(self):
            global c00
            global x0
            sa=groller_lst[B]
            D=sa[0]
            L=sa[2]
            sa=Carrier_lst[B]
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

        def s_20(self):#自動調心サポート外
            global c00
            sa=groller_lst[B]
            D=sa[0]
            L=sa[2]
            sa=J_Carrier_lst[B]
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
            sa=groller_lst[B]
            D=sa[0]
            L=sa[2]
            sa=J_Carrier_lst[B]
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

        def rib(self):
            global c00
            sa=J_Return_lst[B]
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

        def s_200(self):#サポートカッター
            global c00
            p1=(0,0,0)
            p2=(0,-A,-A)
            p3=(0,A,-A)
            plst=[p1,p2,p3,p1]
            pwire=Part.makePolygon(plst)
            pface = Part.Face(pwire)
            c00=pface

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
            c00=c00.fuse(c01)
            c00=c00.fuse(c02)

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

        #リターンサポート
        def s_3(self):
            global c00
            global A0
            global B0
            global S
            global W0
            sa=Return_lst[B]
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

        if buhin=='Pulleys':
            import Belt_data.BltCvPulley
            pass

        elif buhin=='MotorPulley':
            import Belt_data.MotorPulley
            pass

        elif buhin=='CarrierRoller':
            buhinmei='Carrier roller_'+B
            c_roller(self)
            c1=c00

        elif buhin=='ReturnRoller':
            buhinmei='Return roller_'+B
            if spec=='RubberLining':
                sa=groller_lst[B]
                D=sa[0]
                d=sa[1]
                L=sa[4]
                l=sa[5]
                r_roller(self)
                c1=c00
            elif spec=='PVCLining':
                sa=groller_lst[B]
                D=sa[0]
                d=sa[1]
                L=sa[4]
                l=sa[5]
                r_roller(self)
                c1=c00

        elif buhin=='SideRoller':
            buhinmei='Side roller_'
            s_roller(self)
            c1=c00

        elif buhin=='Carrier':
            global katakou
            global sa1
            global r0
            
            buhinmei='Carrier_'+B
            spec2=self.comboBox_3.currentText()
            if spec2=='Fixed':
                global y
                #buhinmei='Carrier_'+B
                sa=Carrier_lst[B]
                A0=sa[1]
                B0=sa[3]
                h=sa[4]
                katakou=sa[7]
                sa1=angle_lst[katakou]
                angle(self)
                c01=c00
                c01.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(1,0,0),-135))
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
                c02.Placement=App.Placement(App.Vector(0,-B0/2,-y-t),App.Rotation(App.Vector(0,0,1),0))
                c1=c011.fuse(c02)
                base_p(self)
                c02=c00
                c02.Placement=App.Placement(App.Vector(A0-50,-B0/2,-y-t),App.Rotation(App.Vector(0,0,1),0))
                c1=c1.fuse(c02)
                c_roller(self)
                c01=c00
                c01.Placement=App.Placement(App.Vector((A0-L)/2,0,-y-t+h),App.Rotation(App.Vector(0,0,1),0))
                c1=c1.fuse(c01)
                c_roller(self)
                c01=c00
                k=20/(180/math.pi)
                h0=(L+5)*math.sin(k)
                r0=7.5
                x1=r0*math.cos(k)
                y1=r0*math.sin(k)
                c01.Placement=App.Placement(App.Vector((A0/2-0.5*L)-r0*(1+math.cos(k)),0,-y-t+h+y1),App.Rotation(App.Vector(0,1,0),-160))
                c1=c1.fuse(c01)
                c_roller(self)
                c01=c00
                c01.Placement=App.Placement(App.Vector((A0/2+0.5*L)+r0*(1+math.cos(k)),0,-y-t+h+y1),App.Rotation(App.Vector(0,1,0),-20))
                c1=c1.fuse(c01)
                s_1(self)
                c01=c00
                c01.Placement=App.Placement(App.Vector((A0/2+0.5*L-10),0,-(y0/2+6)),App.Rotation(App.Vector(0,0,1),0))
                s_1(self)
                c02=c00
                c02.Placement=App.Placement(App.Vector((A0/2-0.5*L+10),0,-(y0/2+6)),App.Rotation(App.Vector(0,0,1),180))
                if float(B)<=700:
                    ds=2*r0
                elif float(B)>700:
                    ds=1.0*r0
                s_2(self)
                c03=c00
                sa=Carrier_lst[B]
                L2=L+2*(r0+10)
                k=20/(180/math.pi)
                x0=L2*math.cos(k)
                x2=L/2+r0+10+x0
                c03.Placement=App.Placement(App.Vector((A0/2+x2-ds),0,-(y0/2+6)),App.Rotation(App.Vector(0,0,1),0))
                s_2(self)
                c04=c00
                x2=L/2+r0+10+x0
                c04.Placement=App.Placement(App.Vector((A0/2-(x2-ds)),0,-(y0/2+6)),App.Rotation(App.Vector(0,0,1),180))
                c01=c01.fuse(c02)
                c01=c01.fuse(c03)
                c01=c01.fuse(c04)
                angle2(self)
                c021=c00
                c021.Placement=App.Placement(App.Vector(0,-A,-A),App.Rotation(App.Vector(0,0,1),0))
                c02=c021.extrude(Base.Vector(A0,0,0))
                c01=c01.cut(c02)
                c1=c1.fuse(c01)
                c1.Placement=App.Placement(App.Vector(0,-A0/2,0),App.Rotation(App.Vector(0,0,1),90))
                #Part.show(c1)

            elif spec2=='Self_Aligning':
                buhinmei='Self_Aligning_Carrier_'+B
                sa=J_Carrier_lst[B]
                A0=float(sa[1])
                B0=sa[3]
                M0=sa[0]
                N0=sa[2]
                h=sa[4]
                katakou=sa[7]
                katakou2=sa[8]
                sa1=angle_lst[katakou]
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
                sa1=channel_lst[katakou2]
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
                sa1=angle_lst[katakou]
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
                #c1.Placement=App.Placement(App.Vector(0,-A0/2,0),App.Rotation(App.Vector(0,0,1),90))
                c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),90))
            
        
        elif buhin=='Return':
            spec2=self.comboBox_3.currentText()
            if spec2=='Fixed':
                buhinmei='Return_'+B
                r_roller(self)
                c1=c00
                c1.Placement=App.Placement(App.Vector(-L/2,0,0),App.Rotation(App.Vector(0,0,1),0))
                s_3(self)
                c01=c00
                sa=Return_lst[B]
                #A0=sa[3]
                B0=sa[5]
                c01.Placement=App.Placement(App.Vector(S/2,-B0/2,-15),App.Rotation(App.Vector(0,0,1),0))
                s_3(self)
                c02=c00
                c02.Placement=App.Placement(App.Vector(-S/2,B0/2,-15),App.Rotation(App.Vector(0,0,1),180))
                c01=c01.fuse(c02)
                c1=c1.fuse(c01)
                c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),90))
                #self.label_4.setText(QtGui.QApplication.translate("Dialog", str(spec2), None))

            elif spec2=='Self_Aligning' :
                buhinmei='Self_Aligning_Return_'+B
                r_roller(self)
                c1=c00
                c1.Placement=App.Placement(App.Vector(-L/2,0,0),App.Rotation(App.Vector(0,0,1),0))
                sa=J_Return_lst[B]
                M0=sa[1]
                A0=sa[2]
                N0=sa[3]
                B0=sa[4]
                h=sa[5]
                H=sa[6]
                katakou=sa[7]
                katakou2=sa[8]
                sa1=angle_lst[katakou]
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
                sa1=channel_lst[katakou2]
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
                #Part.show(c01)
                #Part.show(c1)
                sa1=angle_lst[katakou]
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
        elif buhin=='Take-UP'or buhin=='PillowBlock':
                buhinmei=buhin
                base=os.path.dirname(os.path.abspath(__file__))
                if buhin=='Take-UP':
                    fname=buhin+'_'+self.comboBox_3.currentText()+'.FCStd'
                    joined_path = os.path.join(base, 'Belt_data','takeup_data',fname) 
                elif buhin=='PillowBlock':
                    fname=self.comboBox_3.currentText()+'.FCStd'
                    joined_path = os.path.join(base, 'Belt_data','brg_data',fname) 
                try:
                    Gui.ActiveDocument.mergeProject(joined_path)
                except:
                    doc=App.newDocument()
                    Gui.ActiveDocument.mergeProject(joined_path)    
                App.ActiveDocument.recompute()  
                Gui.ActiveDocument.ActiveView.fitAll()
                return  
        elif buhin=='Assy':
            import Belt_Assy
            #return
        elif buhin=='Belt':
            import Belt  
        elif buhin=='Take-UpAssy':
            import TakeUp     

        label= buhinmei
        doc=App.activeDocument()
        try:
            F_Obj = doc.addObject("Part::Feature",label)

        except:
            doc=App.newDocument()
            F_Obj = doc.addObject("Part::Feature",label)
            pass    
        F_Obj.Shape=c1
        Gui.SendMsgToActiveView("ViewFit")
     
class main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show()

