# -*- coding: utf-8 -*-
#copyright katsuichi yamashita
import os
import sys
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui
from PySide import QtUiTools
from PySide import QtCore
from FreeCAD import Base
import FreeCAD, Part, math
from math import pi
from . import mtrply_data
from . import paramMtrPly

class ViewProvider:
    def __init__(self, obj):
        '''Set this object to the proxy object of the actual view provider'''
        obj.Proxy = self
        return
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(800, 330)
        Dialog.move(1000, 0)
        #ベルト幅
        self.label_B = QtGui.QLabel('BeltWidth',Dialog)
        self.label_B.setGeometry(QtCore.QRect(11, 11, 61, 16))
        self.label_B.setObjectName("label")
        self.comboBox_B = QtGui.QComboBox(Dialog)
        self.comboBox_B.setGeometry(QtCore.QRect(80, 11, 130, 20))

        #A
        self.label_30 = QtGui.QLabel('A',Dialog)
        self.label_30.setGeometry(QtCore.QRect(50, 63, 61, 16))
        self.label_30.setObjectName("label_3")
        self.lineEdit_30 = QtGui.QLineEdit(Dialog)
        self.lineEdit_30.setGeometry(QtCore.QRect(80, 63, 50, 20))
        self.lineEdit_30.setObjectName("lineEdit")
        #a
        self.label_3 = QtGui.QLabel('a',Dialog)
        self.label_3.setGeometry(QtCore.QRect(50, 93, 61, 16))
        self.label_3.setObjectName("label_3")
        self.lineEdit_3 = QtGui.QLineEdit(Dialog)
        self.lineEdit_3.setGeometry(QtCore.QRect(80, 93, 50, 20))
        self.lineEdit_3.setObjectName("lineEdit")
        #b
        self.label_6 = QtGui.QLabel('b',Dialog)
        self.label_6.setGeometry(QtCore.QRect(50, 120, 61, 16))
        self.label_6.setObjectName("label_6")
        self.lineEdit_6 = QtGui.QLineEdit(Dialog)
        self.lineEdit_6.setGeometry(QtCore.QRect(80, 120, 50, 20))
        self.lineEdit_6.setObjectName("lineEdit_6") 
        #D
        self.label_50 = QtGui.QLabel('D',Dialog)
        self.label_50.setGeometry(QtCore.QRect(50, 150, 61, 16))
        self.label_50.setObjectName("label_6")
        self.lineEdit_50 = QtGui.QLineEdit(Dialog)
        self.lineEdit_50.setGeometry(QtCore.QRect(80, 150, 50, 20))
        self.lineEdit_50.setObjectName("lineEdit_50")   
        #D1
        self.label_7 = QtGui.QLabel('D1',Dialog)
        self.label_7.setGeometry(QtCore.QRect(50, 180, 61, 16))
        self.label_7.setObjectName("label_7")
        self.lineEdit_7 = QtGui.QLineEdit(Dialog)
        self.lineEdit_7.setGeometry(QtCore.QRect(80, 180, 50, 20))
        self.lineEdit_7.setObjectName("lineEdit_7")
        #D2
        self.label_8 = QtGui.QLabel('D2',Dialog)
        self.label_8.setGeometry(QtCore.QRect(50, 210, 61, 16))
        self.label_8.setObjectName("label_8")
        self.lineEdit_8 = QtGui.QLineEdit(Dialog)
        self.lineEdit_8.setGeometry(QtCore.QRect(80, 210, 50, 20))
        self.lineEdit_8.setObjectName("lineEdit_8")
        #D3
        self.label_9 = QtGui.QLabel('D3',Dialog)
        self.label_9.setGeometry(QtCore.QRect(50, 240, 61, 16))
        self.label_9.setObjectName("label_9")
        self.lineEdit_9 = QtGui.QLineEdit(Dialog)
        self.lineEdit_9.setGeometry(QtCore.QRect(80, 240, 50, 20))
        self.lineEdit_9.setObjectName("lineEdit_9") 
        #F
        self.label_F = QtGui.QLabel('F',Dialog)
        self.label_F.setGeometry(QtCore.QRect(50, 270, 61, 16))
        self.label_F.setObjectName("label_F")
        self.lineEdit_F = QtGui.QLineEdit(Dialog)
        self.lineEdit_F.setGeometry(QtCore.QRect(80, 270, 50, 20))
        self.lineEdit_F.setObjectName("lineEdit_F") 
        #L
        self.label_10 = QtGui.QLabel('L',Dialog)
        self.label_10.setGeometry(QtCore.QRect(140, 63, 61, 16))
        self.label_10.setObjectName("label_10")
        self.lineEdit_10 = QtGui.QLineEdit(Dialog)
        self.lineEdit_10.setGeometry(QtCore.QRect(160, 63, 50, 20))
        self.lineEdit_10.setObjectName("lineEdit_10") 
        #C
        self.label_11 = QtGui.QLabel('C',Dialog)
        self.label_11.setGeometry(QtCore.QRect(140, 90, 61, 16))
        self.label_11.setObjectName("label_11")
        self.lineEdit_11 = QtGui.QLineEdit(Dialog)
        self.lineEdit_11.setGeometry(QtCore.QRect(160, 90, 50, 20))
        self.lineEdit_11.setObjectName("lineEdit_11")
        #E
        self.label_12 = QtGui.QLabel('E',Dialog)
        self.label_12.setGeometry(QtCore.QRect(140, 120, 61, 16))
        self.label_12.setObjectName("label_12")
        self.lineEdit_12 = QtGui.QLineEdit(Dialog)
        self.lineEdit_12.setGeometry(QtCore.QRect(160, 120, 50, 20))
        self.lineEdit_12.setObjectName("lineEdit_12")
        #M
        self.label_13 = QtGui.QLabel('M',Dialog)
        self.label_13.setGeometry(QtCore.QRect(140, 150, 61, 16))
        self.label_13.setObjectName("label_13")
        self.lineEdit_13 = QtGui.QLineEdit(Dialog)
        self.lineEdit_13.setGeometry(QtCore.QRect(160, 150, 50, 20))
        self.lineEdit_13.setObjectName("lineEdit_13")  
        #R
        self.label_14 = QtGui.QLabel('R',Dialog)
        self.label_14.setGeometry(QtCore.QRect(140, 180, 61, 16))
        self.label_14.setObjectName("label_14")
        self.lineEdit_14 = QtGui.QLineEdit(Dialog)
        self.lineEdit_14.setGeometry(QtCore.QRect(160, 180, 50, 20))
        self.lineEdit_14.setObjectName("lineEdit_14")
        #N1
        self.label_15 = QtGui.QLabel('N1',Dialog)
        self.label_15.setGeometry(QtCore.QRect(140, 210, 61, 16))
        self.label_15.setObjectName("label_15")
        self.lineEdit_15 = QtGui.QLineEdit(Dialog)
        self.lineEdit_15.setGeometry(QtCore.QRect(160, 210, 50, 20))
        self.lineEdit_15.setObjectName("lineEdit_15")
        #G1
        self.label_G1 = QtGui.QLabel('G1',Dialog)
        self.label_G1.setGeometry(QtCore.QRect(230, 210, 61, 16))
        self.label_G1.setObjectName("label_15")
        self.lineEdit_G1 = QtGui.QLineEdit(Dialog)
        self.lineEdit_G1.setGeometry(QtCore.QRect(250, 210, 50, 20))
        self.lineEdit_G1.setObjectName("lineEdit_15")

        #P
        self.label_P = QtGui.QLabel('P',Dialog)
        self.label_P.setGeometry(QtCore.QRect(320, 210, 61, 16))
        self.label_P.setObjectName("label_P")
        self.lineEdit_P = QtGui.QLineEdit(Dialog)
        self.lineEdit_P.setGeometry(QtCore.QRect(350, 210, 50, 20))
        self.lineEdit_P.setObjectName("lineEdit_P")

        #G2
        self.label_G2 = QtGui.QLabel('G2',Dialog)
        self.label_G2.setGeometry(QtCore.QRect(230, 240, 61, 16))
        self.label_G2.setObjectName("label_G2")
        self.lineEdit_G2 = QtGui.QLineEdit(Dialog)
        self.lineEdit_G2.setGeometry(QtCore.QRect(250, 240, 50, 20))
        self.lineEdit_G2.setObjectName("lineEdit_G2")

        #H
        self.label_H = QtGui.QLabel('H',Dialog)
        self.label_H.setGeometry(QtCore.QRect(230, 270, 61, 16))
        self.label_H.setObjectName("label_H")
        self.lineEdit_H = QtGui.QLineEdit(Dialog)
        self.lineEdit_H.setGeometry(QtCore.QRect(250, 270, 50, 20))
        self.lineEdit_H.setObjectName("lineEdit_H")

        #N2
        self.label_16 = QtGui.QLabel('N2',Dialog)
        self.label_16.setGeometry(QtCore.QRect(140, 240, 61, 16))
        self.label_16.setObjectName("label_16")
        self.lineEdit_16 = QtGui.QLineEdit(Dialog)
        self.lineEdit_16.setGeometry(QtCore.QRect(160, 240, 50, 20))
        self.lineEdit_16.setObjectName("lineEdit_16")
        #d
        self.label_17 = QtGui.QLabel('d',Dialog)
        self.label_17.setGeometry(QtCore.QRect(140, 270, 61, 16))
        self.label_17.setObjectName("label_17")
        self.lineEdit_17 = QtGui.QLineEdit(Dialog)
        self.lineEdit_17.setGeometry(QtCore.QRect(160, 270, 50, 20))
        self.lineEdit_17.setObjectName("lineEdit_17")
        #image
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(225, 0, 600, 220))
        #self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")

        #実行
        self.pushButton = QtGui.QPushButton('Create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(160, 300, 75, 23))
        self.pushButton.setObjectName("pushButton")

        #インポート
        self.pushButton2 = QtGui.QPushButton('Import',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(250, 300, 75, 23))
        self.pushButton2.setObjectName("pushButton")

        #更新
        self.pushButton3 = QtGui.QPushButton('Update',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(340, 300, 75, 23))
        self.pushButton3.setObjectName("pushButton")
        
        self.comboBox_B.addItems(mtrply_data.belthaba)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.comboBox_B.setCurrentIndex(1)
        self.comboBox_B.currentIndexChanged[int].connect(self.onSpec)
        self.comboBox_B.setCurrentIndex(0)

        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.read_data)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.upDate)
       
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "motorPully", None))
        
    
    def read_data(self):
        selection = Gui.Selection.getSelection()
        for obj in selection:
            try:
                self.comboBox_2.setCurrentText(obj.Standard)
            except:
                pass
        App.ActiveDocument.recompute()   

    def upDate(self):
        sb=mtrply_data.pulley_buhin
        selection = Gui.Selection.getSelection()
        for obj in selection:
            try:
                i=self.comboBox_B.currentIndex()
                obj.Standard=sb[i]+'  beltWidth='+str(int(B1))+'-'+str(int(B2))
            except:
                print('error')
        label=sb[i]
        App.ActiveDocument.recompute()         

    def onSpec(self):
        global buhin
        global B0
        global A
        global a
        global b
        global D
        global D1
        global D2
        global D3
        global L
        global C
        global E
        global M
        global R
        global N1
        global N2
        global d
        global B1
        global B2
        global B0
        global B00
        global F
        global G1
        global G2
        global H
        global P
        global x4
        global x5
        global x6
        global g
        
        buhin='CycloMotorPulley.jpg'
        pic=buhin
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, 'png_data',pic)
        self.label_5.setPixmap(QtGui.QPixmap(joined_path))
        B0=self.comboBox_B.currentText()
        sa=mtrply_data.pulley_dim[B0]
        A=float(sa[0])
        a=float(sa[1])
        b=float(sa[2])
        D=float(sa[3])
        D1=float(sa[4])  
        D2=float(sa[5])  
        D3=float(sa[6]) 
        L=float(sa[7])   
        C=float(sa[8])
        E=float(sa[9]) 
        M=float(sa[10])  
        R=float(sa[11])  
        N1=float(sa[12]) 
        N2=float(sa[13]) 
        d=float(sa[14])  
        B1=float(sa[15])     
        B2=sa[16]
        F=float(sa[17]) 
        G1=float(sa[18]) 
        G2=float(sa[19]) 
        H=float(sa[20]) 
        P=float(sa[21]) 
        g=float(sa[24]) 


        self.lineEdit_10.setText(str(L))
        self.lineEdit_30.setText(str(A))
        self.lineEdit_3.setText(str(a))
        self.lineEdit_6.setText(str(b))
        self.lineEdit_50.setText(str(D))
        self.lineEdit_7.setText(str(D1))
        self.lineEdit_8.setText(str(D2))
        self.lineEdit_9.setText(str(D3))
        self.lineEdit_10.setText(str(L))
        self.lineEdit_11.setText(str(C))
        self.lineEdit_12.setText(str(E))
        self.lineEdit_13.setText(str(M))
        self.lineEdit_14.setText(str(R))
        self.lineEdit_15.setText(str(N1))
        self.lineEdit_16.setText(str(N2))
        self.lineEdit_17.setText(str(d))
        self.lineEdit_F.setText(str(F))
        self.lineEdit_G1.setText(str(G1))
        self.lineEdit_G2.setText(str(G2))
        self.lineEdit_H.setText(str(H))
        self.lineEdit_P.setText(str(P))
    
    def create(self):
        label='MotorPulley'
        key=self.comboBox_B.currentIndex()
        try:
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
        except:
            doc=App.newDocument()
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)

        obj.addProperty("App::PropertyEnumeration", "BeltWidth",label)
        i=self.comboBox_B.currentIndex()  
        obj.BeltWidth=mtrply_data.belthaba
        obj.BeltWidth=mtrply_data.belthaba[i]  

        obj.addProperty("App::PropertyFloat", "D",label).D=D
        obj.addProperty("App::PropertyFloat", "mass",'mass[kg]').mass=g

        paramMtrPly.MotorPly(obj)
        obj.ViewObject.Proxy=0
        FreeCAD.ActiveDocument.recompute() 
        Gui.SendMsgToActiveView("ViewFit")

class main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show()
        # スクリプトのウィンドウを取得
        script_window = Gui.getMainWindow().findChild(QtGui.QDialog, 'd')
        # 閉じるボタンを無効にする
        script_window.setWindowFlags(script_window.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)
