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
import paramCarrier
Vscraper_haba=['500','600','750']
belt_haba=['400','450','500','600','700','750','800','900','1000',]
belt_buhin=['Carrier','Return']
spec_roller=['RubberLining','PVCLining',]
groller_dia=['99','124']
eroller_dia=['95','121']
carrier_spec=['Fixed','Self_Aligning']
roller_spec=['SteelPipe',]



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
#ベルト幅B　　　M　  A0    N   B0   h    H    L0     g[kg]
Carrier_lst={
'400':(   640, 690, 140,190, 125, 229, 469, 'L6x50',14),
'450':(   690, 740, 140,190, 125, 236, 526, 'L6x50',15),
'500':(   740, 790, 140,190, 125, 241, 569, 'L6x50',16),
'600':(   840, 890, 150,200, 140, 266, 656, 'L6x65',19),
'700':(   940, 990, 150,200, 140, 280, 771, 'L6x65',21),
'750':(  1040,1090, 160,210, 150, 305, 806, 'L6x75',26),
'800':(  1090,1140, 160,210, 150, 310, 849, 'L6x75',27),
'900':(  1190,1240, 160,210, 150, 322, 949, 'L6x75',30),
'1000':( 1290,1340, 160,210, 150, 332,1036, 'L6x75',32),
}

#自動調心キャリヤ
#ベルト幅B　　　M　  A0    N   B0   h    H    L0      channel    g[kg]       
J_Carrier_lst={
'400':(   640, 690, 140,190, 130, 232, 471, 'L6x50','C100x50x5',24),
'450':(   690, 740, 140,190, 130, 239, 528, 'L6x50','C100x50x5',26),
'500':(   740, 790, 140,190, 130, 244, 571, 'L6x50','C100x50x5',28),
'600':(   840, 890, 150,200, 145, 269, 658, 'L6x65','C100x50x5',32),
'700':(   940, 990, 150,200, 145, 283, 773, 'L6x65','C100x50x5',36),
'750':(  1040,1090, 160,210, 155, 310, 807, 'L6x75','C125x65x6',46),
'800':(  1090,1140, 160,210, 155, 315, 851, 'L6x75','C125x65x6',48),
'900':(  1190,1240, 160,210, 155, 327, 951, 'L6x75','C125x65x6',52),
'1000':( 1290,1340, 160,210, 155, 337,1038, 'L6x75','C125x65x6',55),
}

#リターン
#ベルト幅B　l　   S     M     A0    N    B0    h     g[kg]
Return_lst={
'400':(   460,  480,  640,  690,  60,  110,  110,   7),
'450':(   510,  530,  690,  740,  60,  110,  110,   8),
'500':(   560,  580,  740,  790,  60,  110,  110,   8),
'600':(   660,  680,  840,  890,  60,  110,  110,   10),
'700':(   760,  780,  940,  990,  60,  110,  110,   11),
'750':(   850,  880, 1040, 1090,  60,  110,  110,   15),
'800':(   900,  930, 1090, 1140,  60,  110,  110,   15),
'900':(  1000, 1030, 1190, 1240,  60,  110,  110,   18),
'1000':( 1100, 1130, 1290, 1340,  60,  110,  110,   19),
}

#自動調心リターン
#ベルト幅B　l　    M     A0    N    B0    h　 　H    angle     channel    g[kg]
J_Return_lst={
'400':(   460,   640,  690,  60,  110,  110, 295,  'L6x50',  'C100x50x5',  21 ),
'450':(   510,   690,  740,  60,  110,  110, 295,  'L6x50',  'C100x50x5',  22 ),
'500':(   560,   740,  790,  60,  110,  110, 295,  'L6x50',  'C100x50x5',  25 ),
'600':(   660,   840,  890,  60,  110,  110, 310,  'L6x65',  'C100x50x5',  30 ),
'700':(   760,   940,  990,  60,  110,  110, 310,  'L6x65',  'C100x50x5',  32 ),
'750':(   850,  1040, 1090,  60,  130,  125, 320,  'L6x50',  'C125x65x6',  43 ),
'800':(   900,  1090, 1140,  60,  130,  110, 345,  'L6x75',  'C125x65x6',  44 ),
'900':(  1000,  1190, 1240,  60,  130,  110, 345,  'L6x75',  'C125x65x6',  49 ),
'1000':( 1100,  1290, 1340,  60,  130,  110, 345,  'L6x75',  'C125x65x6',  52 ),
}


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(355, 150)
        Dialog.move(1000, 0)
         #ベルト幅BeltWidh
        self.label = QtGui.QLabel('BeltWidth',Dialog)
        self.label.setGeometry(QtCore.QRect(11, 37, 61, 16))
        self.label.setObjectName("label")
        self.comboBox = QtGui.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(80, 37, 130, 20))
        self.comboBox.setObjectName("comboBox")
        #部品parts
        self.comboBox_2 = QtGui.QComboBox(Dialog)
        self.comboBox_2.setGeometry(QtCore.QRect(80, 11, 130, 20))
        self.comboBox_2.setObjectName("comboBox_2")
        self.label_2 = QtGui.QLabel('Parts',Dialog)
        self.label_2.setGeometry(QtCore.QRect(11, 11, 61, 16))
        self.label_2.setObjectName("label_2")
        #仕様Spec
        self.label_3 = QtGui.QLabel('Spec',Dialog)
        self.label_3.setGeometry(QtCore.QRect(11, 63, 61, 16))
        self.label_3.setObjectName("label_3")
        self.comboBox_3 = QtGui.QComboBox(Dialog)
        self.comboBox_3.setGeometry(QtCore.QRect(80, 63, 130, 20))
        self.comboBox_3.setObjectName("comboBox_3")
        #仕様2Spec2
        self.comboBox_4 = QtGui.QComboBox(Dialog)
        self.comboBox_4.setGeometry(QtCore.QRect(80, 90, 130, 20))
        self.comboBox_4.setObjectName("comboBox_4")
        self.label_6 = QtGui.QLabel('Spec2',Dialog)
        self.label_6.setGeometry(QtCore.QRect(12, 90, 51, 16))
        self.label_6.setObjectName("label_6")
        #png
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(225, 10, 121, 101))
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        
        #実行
        self.pushButton = QtGui.QPushButton('Create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(30, 120, 75, 23))
        self.pushButton.setObjectName("pushButton")
        #Import
        self.pushButton2 = QtGui.QPushButton('Import',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(110, 120, 75, 23))
        self.pushButton2.setObjectName("pushButton")
        #upDate
        self.pushButton3 = QtGui.QPushButton('upDate',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(190, 120, 75, 23))
        self.pushButton3.setObjectName("pushButton")


        self.comboBox.addItems(belt_haba)
        self.comboBox_2.addItems(belt_buhin)

        self.comboBox_2.setCurrentIndex(1)
        self.comboBox_2.currentIndexChanged[int].connect(self.onSpec)
        self.comboBox_2.setCurrentIndex(0)

        self.comboBox_3.currentIndexChanged[int].connect(self.onSpec2)

        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.importData)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.uPdate)
        #QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.create)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", 'Carrier', None))
        
    def importData(self):
        global Carrier
        global Return
        global BendPulleyAssy
        global V_shapedScraper
        selection = Gui.Selection.getSelection()
        if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 parts_group = selected_object
                 for obj in parts_group.Group:
                     print(obj.Label)
                     if obj.Label=='Carrier':
                         Carrier=obj
                     elif obj.Label=='Return':
                         Return=obj
                 self.comboBox.setCurrentText(obj.BeltWidth)         
                     
    
    def uPdate(self):
         doc = App.ActiveDocument
         selection = Gui.Selection.getSelection()
         if not selection:
            App.Console.PrintMessage("オブジェクトを選択してください。\n")

         for obj in selection: 
             if obj.Label=='Carrier' or obj.Label=='Return' :  
                 obj.BeltWidth=self.comboBox.currentText()
        
    def onSpec(self):
        global buhin
        global pic
        buhin=self.comboBox_2.currentText()
        spec=self.comboBox_3.currentText()
        
        
        if buhin=='Carrier':
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
        

        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "Belt_data",'png_data',pic)
        self.label_5.setPixmap(QtGui.QPixmap(joined_path))

    def onSpec2(self):#部品
        spec2=self.comboBox_3.currentText()
        if buhin=='Carrier':
            pic=buhin +'_'  + spec2 + '.png'
        elif buhin=='Return':
            pic=buhin+'_'  + spec2 + '.png'
        
            
        else:
            pic=buhin + '.png'
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
        label='Carrier'
        try:
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
        except:
            doc=App.newDocument()
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
        BeltWidth=self.comboBox.currentText()
        spec=self.comboBox_3.currentText()
        spec2=self.comboBox_4.currentText()
        if label=='Carrier':
            obj.addProperty("App::PropertyString", "spec",label).spec=spec
            obj.addProperty("App::PropertyString", "spec2",label).spec2=spec2
            obj.addProperty("App::PropertyEnumeration", "BeltWidth",label)
            i=self.comboBox.currentIndex()  
            sa=belt_haba
            print(obj.Label)
            obj.BeltWidth=sa[i]
    
            paramCarrier.Carrier(obj)
            obj.ViewObject.Proxy=0
            FreeCAD.ActiveDocument.recompute() 


     
class main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show()
        script_window = Gui.getMainWindow().findChild(QtGui.QDialog, 'd')
        script_window.setWindowFlags(script_window.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)
     

