# -*- coding: utf-8 -*-
import os
import sys
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui
from PySide import QtUiTools
from PySide import QtCore
from FreeCAD import Base
import FreeCAD, Part, math
import DraftVecUtils
import Sketcher
import PartDesign
from math import pi
import Draft
import paramPulley
belt_haba=['400','450','500','600','700','750','800','900','1000',]
pulley_buhin=['DrivePulley','HeadPulley','Take_upPulley','TailPulley','BendPulley','SnapPulley'
]
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 325)
        Dialog.move(900, 0)
        #ベルト幅
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(11, 37, 61, 16))
        self.label.setObjectName("label")
        self.comboBox = QtGui.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(80, 37, 130, 20))
        self.comboBox.setObjectName("comboBox")
        #部品
        self.comboBox_2 = QtGui.QComboBox(Dialog)
        self.comboBox_2.setGeometry(QtCore.QRect(80, 11, 130, 20))
        self.comboBox_2.setObjectName("comboBox_2")
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(11, 11, 61, 16))
        self.label_2.setObjectName("label_2")
        #L
        self.label_30 = QtGui.QLabel(Dialog)
        self.label_30.setGeometry(QtCore.QRect(50, 63, 61, 16))
        self.label_30.setObjectName("label_3")
        self.lineEdit_30 = QtGui.QLineEdit(Dialog)
        self.lineEdit_30.setGeometry(QtCore.QRect(80, 63, 50, 20))
        self.lineEdit_30.setObjectName("lineEdit")
        #A
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(50, 93, 61, 16))
        self.label_3.setObjectName("label_3")
        self.lineEdit_3 = QtGui.QLineEdit(Dialog)
        self.lineEdit_3.setGeometry(QtCore.QRect(80, 93, 50, 20))
        self.lineEdit_3.setObjectName("lineEdit")
        #B
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(50, 120, 61, 16))
        self.label_6.setObjectName("label_6")
        self.lineEdit_6 = QtGui.QLineEdit(Dialog)
        self.lineEdit_6.setGeometry(QtCore.QRect(80, 120, 50, 20))
        self.lineEdit_6.setObjectName("lineEdit_6") 
        #C
        self.label_50 = QtGui.QLabel(Dialog)
        self.label_50.setGeometry(QtCore.QRect(50, 150, 61, 16))
        self.label_50.setObjectName("label_6")
        self.lineEdit_50 = QtGui.QLineEdit(Dialog)
        self.lineEdit_50.setGeometry(QtCore.QRect(80, 150, 50, 20))
        self.lineEdit_50.setObjectName("lineEdit_50")   
        #D
        self.label_7 = QtGui.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(50, 180, 61, 16))
        self.label_7.setObjectName("label_7")
        self.lineEdit_7 = QtGui.QLineEdit(Dialog)
        self.lineEdit_7.setGeometry(QtCore.QRect(80, 180, 50, 20))
        self.lineEdit_7.setObjectName("lineEdit_7")
        #E
        self.label_8 = QtGui.QLabel(Dialog)
        self.label_8.setGeometry(QtCore.QRect(50, 210, 61, 16))
        self.label_8.setObjectName("label_8")
        self.lineEdit_8 = QtGui.QLineEdit(Dialog)
        self.lineEdit_8.setGeometry(QtCore.QRect(80, 210, 50, 20))
        self.lineEdit_8.setObjectName("lineEdit_8")
        #d1
        self.label_9 = QtGui.QLabel(Dialog)
        self.label_9.setGeometry(QtCore.QRect(50, 240, 61, 16))
        self.label_9.setObjectName("label_9")
        self.lineEdit_9 = QtGui.QLineEdit(Dialog)
        self.lineEdit_9.setGeometry(QtCore.QRect(80, 240, 50, 20))
        self.lineEdit_9.setObjectName("lineEdit_9") 
        #d2
        self.label_10 = QtGui.QLabel(Dialog)
        self.label_10.setGeometry(QtCore.QRect(140, 63, 61, 16))
        self.label_10.setObjectName("label_10")
        self.lineEdit_10 = QtGui.QLineEdit(Dialog)
        self.lineEdit_10.setGeometry(QtCore.QRect(160, 63, 50, 20))
        self.lineEdit_10.setObjectName("lineEdit_10") 
        #d3
        self.label_11 = QtGui.QLabel(Dialog)
        self.label_11.setGeometry(QtCore.QRect(140, 90, 61, 16))
        self.label_11.setObjectName("label_11")
        self.lineEdit_11 = QtGui.QLineEdit(Dialog)
        self.lineEdit_11.setGeometry(QtCore.QRect(160, 90, 50, 20))
        self.lineEdit_11.setObjectName("lineEdit_11")
        #t1
        self.label_12 = QtGui.QLabel(Dialog)
        self.label_12.setGeometry(QtCore.QRect(140, 120, 61, 16))
        self.label_12.setObjectName("label_12")
        self.lineEdit_12 = QtGui.QLineEdit(Dialog)
        self.lineEdit_12.setGeometry(QtCore.QRect(160, 120, 50, 20))
        self.lineEdit_12.setObjectName("lineEdit_12")
        #t2
        self.label_13 = QtGui.QLabel(Dialog)
        self.label_13.setGeometry(QtCore.QRect(140, 150, 61, 16))
        self.label_13.setObjectName("label_13")
        self.lineEdit_13 = QtGui.QLineEdit(Dialog)
        self.lineEdit_13.setGeometry(QtCore.QRect(160, 150, 50, 20))
        self.lineEdit_13.setObjectName("lineEdit_13")  
        #t3
        self.label_14 = QtGui.QLabel(Dialog)
        self.label_14.setGeometry(QtCore.QRect(140, 180, 61, 16))
        self.label_14.setObjectName("label_14")
        self.lineEdit_14 = QtGui.QLineEdit(Dialog)
        self.lineEdit_14.setGeometry(QtCore.QRect(160, 180, 50, 20))
        self.lineEdit_14.setObjectName("lineEdit_14")
        #t4
        self.label_15 = QtGui.QLabel(Dialog)
        self.label_15.setGeometry(QtCore.QRect(140, 210, 61, 16))
        self.label_15.setObjectName("label_15")
        self.lineEdit_15 = QtGui.QLineEdit(Dialog)
        self.lineEdit_15.setGeometry(QtCore.QRect(160, 210, 50, 20))
        self.lineEdit_15.setObjectName("lineEdit_15")
        #image
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(225, 0, 160, 270))
        #self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")

        #実行
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(160, 295, 75, 23))
        self.pushButton.setObjectName("pushButton")

        self.comboBox.addItems(belt_haba)
        self.comboBox_2.addItems(pulley_buhin)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.comboBox.setCurrentIndex(1)
        self.comboBox.currentIndexChanged[int].connect(self.onSpec)
        self.comboBox.setCurrentIndex(0)

        self.comboBox_2.setCurrentIndex(1)
        self.comboBox_2.currentIndexChanged[int].connect(self.onSpec)
        self.comboBox_2.setCurrentIndex(0)

        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "pully", None))
        self.label_30.setText(QtGui.QApplication.translate("Dialog", "L", None))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "A", None))
        self.label_6.setText(QtGui.QApplication.translate("Dialog", "B", None))
        self.label_50.setText(QtGui.QApplication.translate("Dialog", "C", None))
        self.label_7.setText(QtGui.QApplication.translate("Dialog", "D", None))
        self.label_8.setText(QtGui.QApplication.translate("Dialog", "E", None))
        self.label_9.setText(QtGui.QApplication.translate("Dialog", "d1", None))
        self.label_10.setText(QtGui.QApplication.translate("Dialog", "d2", None))
        self.label_11.setText(QtGui.QApplication.translate("Dialog", "d3", None))
        self.label_12.setText(QtGui.QApplication.translate("Dialog", "t1", None))
        self.label_13.setText(QtGui.QApplication.translate("Dialog", "t2", None))
        self.label_14.setText(QtGui.QApplication.translate("Dialog", "t3", None))
        self.label_15.setText(QtGui.QApplication.translate("Dialog", "t4", None))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "create", None))
    def onSpec(self):
        global buhin
        global B0
        global L
        global A
        global B
        global C
        global D
        global E
        global d1
        global d2
        global d3
        global t1
        global t2
        global t3
        buhin=self.comboBox_2.currentText()
        pic=buhin+'.png'
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, 'png_data',pic)
        self.label_5.setPixmap(QtGui.QPixmap(joined_path))
    
        B0=self.comboBox.currentText()
        sa=pulley_dim[B0]
        L=float(sa[0])
        A=float(sa[1])
        C=float(sa[3])
        if buhin=='DrivePulley' or buhin=='HeadPulley':
            D=400.0
        elif buhin=='TailPulley':
            D=350.0
        elif buhin=='Take_upPulley':    
            D=380.0
        elif buhin=='Bendpulley':  
            D=250.0 
        elif buhin=='SnapPulley': 
            D=250.0 

        if buhin=='DrivePulley':    
            E=float(sa[5])
        else:
            E=0.0

        d1=float(sa[6])
        d2=float(sa[7])
        if buhin=='DrivePulley':   
            d3=float(sa[8])
        else:
            d3=0.0
        t1=float(sa[9])
        t2=float(sa[10])
        t3=float(sa[11])
        t4=float(sa[12])
        B=round(d2*2.3,1)
        E=round(1.7*d3,1)

        self.lineEdit_30.setText(str(L))
        self.lineEdit_3.setText(str(A))
        self.lineEdit_6.setText(str(B))
        self.lineEdit_50.setText(str(C))
        self.lineEdit_7.setText(str(D))
        self.lineEdit_8.setText(str(E))
        self.lineEdit_9.setText(str(d1))
        self.lineEdit_10.setText(str(d2))
        self.lineEdit_11.setText(str(d3))
        self.lineEdit_12.setText(str(t1))
        self.lineEdit_13.setText(str(t2))
        self.lineEdit_14.setText(str(t3))
        self.lineEdit_15.setText(str(t4))
    
    def create(self):
        label=buhin
        try:
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
        except:
            doc=App.newDocument()
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
          
            obj.addProperty("App::PropertyEnumeration", "BeltWidth",label)
            i=self.comboBox.currentIndex()  
            sa=belt_haba
            obj.BeltWidth=sa[i] 

            obj.addProperty("App::PropertyString", "L",label).L=str(L) 

            paramPulley.Pulleys(obj)
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
     
