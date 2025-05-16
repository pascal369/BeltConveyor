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
import DraftVecUtils
import Sketcher
import PartDesign
from math import pi
import Draft
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
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(11, 37, 61, 16))
        self.label.setObjectName("label")
        self.lineEdit_B = QtGui.QLineEdit(Dialog)
        self.lineEdit_B.setGeometry(QtCore.QRect(80, 37, 130, 20))
        self.lineEdit_B.setObjectName("lineEdit_B")
        #形式
        self.comboBox_2 = QtGui.QComboBox(Dialog)
        self.comboBox_2.setGeometry(QtCore.QRect(80, 11, 130, 20))
        self.comboBox_2.setObjectName("comboBox_2")
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(11, 11, 61, 16))
        self.label_2.setObjectName("label_2")
        #A
        self.label_30 = QtGui.QLabel(Dialog)
        self.label_30.setGeometry(QtCore.QRect(50, 63, 61, 16))
        self.label_30.setObjectName("label_3")
        self.lineEdit_30 = QtGui.QLineEdit(Dialog)
        self.lineEdit_30.setGeometry(QtCore.QRect(80, 63, 50, 20))
        self.lineEdit_30.setObjectName("lineEdit")
        #a
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(50, 93, 61, 16))
        self.label_3.setObjectName("label_3")
        self.lineEdit_3 = QtGui.QLineEdit(Dialog)
        self.lineEdit_3.setGeometry(QtCore.QRect(80, 93, 50, 20))
        self.lineEdit_3.setObjectName("lineEdit")
        #b
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(50, 120, 61, 16))
        self.label_6.setObjectName("label_6")
        self.lineEdit_6 = QtGui.QLineEdit(Dialog)
        self.lineEdit_6.setGeometry(QtCore.QRect(80, 120, 50, 20))
        self.lineEdit_6.setObjectName("lineEdit_6") 
        #D
        self.label_50 = QtGui.QLabel(Dialog)
        self.label_50.setGeometry(QtCore.QRect(50, 150, 61, 16))
        self.label_50.setObjectName("label_6")
        self.lineEdit_50 = QtGui.QLineEdit(Dialog)
        self.lineEdit_50.setGeometry(QtCore.QRect(80, 150, 50, 20))
        self.lineEdit_50.setObjectName("lineEdit_50")   
        #D1
        self.label_7 = QtGui.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(50, 180, 61, 16))
        self.label_7.setObjectName("label_7")
        self.lineEdit_7 = QtGui.QLineEdit(Dialog)
        self.lineEdit_7.setGeometry(QtCore.QRect(80, 180, 50, 20))
        self.lineEdit_7.setObjectName("lineEdit_7")
        #D2
        self.label_8 = QtGui.QLabel(Dialog)
        self.label_8.setGeometry(QtCore.QRect(50, 210, 61, 16))
        self.label_8.setObjectName("label_8")
        self.lineEdit_8 = QtGui.QLineEdit(Dialog)
        self.lineEdit_8.setGeometry(QtCore.QRect(80, 210, 50, 20))
        self.lineEdit_8.setObjectName("lineEdit_8")
        #D3
        self.label_9 = QtGui.QLabel(Dialog)
        self.label_9.setGeometry(QtCore.QRect(50, 240, 61, 16))
        self.label_9.setObjectName("label_9")
        self.lineEdit_9 = QtGui.QLineEdit(Dialog)
        self.lineEdit_9.setGeometry(QtCore.QRect(80, 240, 50, 20))
        self.lineEdit_9.setObjectName("lineEdit_9") 
        #F
        self.label_F = QtGui.QLabel(Dialog)
        self.label_F.setGeometry(QtCore.QRect(50, 270, 61, 16))
        self.label_F.setObjectName("label_F")
        self.lineEdit_F = QtGui.QLineEdit(Dialog)
        self.lineEdit_F.setGeometry(QtCore.QRect(80, 270, 50, 20))
        self.lineEdit_F.setObjectName("lineEdit_F") 
        #L
        self.label_10 = QtGui.QLabel(Dialog)
        self.label_10.setGeometry(QtCore.QRect(140, 63, 61, 16))
        self.label_10.setObjectName("label_10")
        self.lineEdit_10 = QtGui.QLineEdit(Dialog)
        self.lineEdit_10.setGeometry(QtCore.QRect(160, 63, 50, 20))
        self.lineEdit_10.setObjectName("lineEdit_10") 
        #C
        self.label_11 = QtGui.QLabel(Dialog)
        self.label_11.setGeometry(QtCore.QRect(140, 90, 61, 16))
        self.label_11.setObjectName("label_11")
        self.lineEdit_11 = QtGui.QLineEdit(Dialog)
        self.lineEdit_11.setGeometry(QtCore.QRect(160, 90, 50, 20))
        self.lineEdit_11.setObjectName("lineEdit_11")
        #E
        self.label_12 = QtGui.QLabel(Dialog)
        self.label_12.setGeometry(QtCore.QRect(140, 120, 61, 16))
        self.label_12.setObjectName("label_12")
        self.lineEdit_12 = QtGui.QLineEdit(Dialog)
        self.lineEdit_12.setGeometry(QtCore.QRect(160, 120, 50, 20))
        self.lineEdit_12.setObjectName("lineEdit_12")
        #M
        self.label_13 = QtGui.QLabel(Dialog)
        self.label_13.setGeometry(QtCore.QRect(140, 150, 61, 16))
        self.label_13.setObjectName("label_13")
        self.lineEdit_13 = QtGui.QLineEdit(Dialog)
        self.lineEdit_13.setGeometry(QtCore.QRect(160, 150, 50, 20))
        self.lineEdit_13.setObjectName("lineEdit_13")  
        #R
        self.label_14 = QtGui.QLabel(Dialog)
        self.label_14.setGeometry(QtCore.QRect(140, 180, 61, 16))
        self.label_14.setObjectName("label_14")
        self.lineEdit_14 = QtGui.QLineEdit(Dialog)
        self.lineEdit_14.setGeometry(QtCore.QRect(160, 180, 50, 20))
        self.lineEdit_14.setObjectName("lineEdit_14")
        #N1
        self.label_15 = QtGui.QLabel(Dialog)
        self.label_15.setGeometry(QtCore.QRect(140, 210, 61, 16))
        self.label_15.setObjectName("label_15")
        self.lineEdit_15 = QtGui.QLineEdit(Dialog)
        self.lineEdit_15.setGeometry(QtCore.QRect(160, 210, 50, 20))
        self.lineEdit_15.setObjectName("lineEdit_15")
        #G1
        self.label_G1 = QtGui.QLabel(Dialog)
        self.label_G1.setGeometry(QtCore.QRect(230, 210, 61, 16))
        self.label_G1.setObjectName("label_15")
        self.lineEdit_G1 = QtGui.QLineEdit(Dialog)
        self.lineEdit_G1.setGeometry(QtCore.QRect(250, 210, 50, 20))
        self.lineEdit_G1.setObjectName("lineEdit_15")

        #P
        self.label_P = QtGui.QLabel(Dialog)
        self.label_P.setGeometry(QtCore.QRect(320, 210, 61, 16))
        self.label_P.setObjectName("label_P")
        self.lineEdit_P = QtGui.QLineEdit(Dialog)
        self.lineEdit_P.setGeometry(QtCore.QRect(350, 210, 50, 20))
        self.lineEdit_P.setObjectName("lineEdit_P")

        #G2
        self.label_G2 = QtGui.QLabel(Dialog)
        self.label_G2.setGeometry(QtCore.QRect(230, 240, 61, 16))
        self.label_G2.setObjectName("label_G2")
        self.lineEdit_G2 = QtGui.QLineEdit(Dialog)
        self.lineEdit_G2.setGeometry(QtCore.QRect(250, 240, 50, 20))
        self.lineEdit_G2.setObjectName("lineEdit_G2")

        #H
        self.label_H = QtGui.QLabel(Dialog)
        self.label_H.setGeometry(QtCore.QRect(230, 270, 61, 16))
        self.label_H.setObjectName("label_H")
        self.lineEdit_H = QtGui.QLineEdit(Dialog)
        self.lineEdit_H.setGeometry(QtCore.QRect(250, 270, 50, 20))
        self.lineEdit_H.setObjectName("lineEdit_H")

        #N2
        self.label_16 = QtGui.QLabel(Dialog)
        self.label_16.setGeometry(QtCore.QRect(140, 240, 61, 16))
        self.label_16.setObjectName("label_16")
        self.lineEdit_16 = QtGui.QLineEdit(Dialog)
        self.lineEdit_16.setGeometry(QtCore.QRect(160, 240, 50, 20))
        self.lineEdit_16.setObjectName("lineEdit_16")
        #d
        self.label_17 = QtGui.QLabel(Dialog)
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
        '''
        #ライセンスキー
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(10, 300, 130, 16))
        self.label_4.setObjectName("label_4")
        self.lineEdit = QtGui.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(80, 300, 60, 20))
        self.lineEdit.setObjectName("lineEdit")
        '''
        #実行
        self.pushButton = QtGui.QPushButton('Create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(160, 300, 75, 23))
        self.pushButton.setObjectName("pushButton")

        
        self.comboBox_2.addItems(mtrply_data.pulley_buhin)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.comboBox_2.setCurrentIndex(1)
        self.comboBox_2.currentIndexChanged[int].connect(self.onSpec)
        self.comboBox_2.setCurrentIndex(0)

        

        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "motorPully", None))
        self.label.setText(QtGui.QApplication.translate("Dialog", "beltWidth", None))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "type", None))
        self.label_30.setText(QtGui.QApplication.translate("Dialog", "A", None))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "a", None))
        self.label_6.setText(QtGui.QApplication.translate("Dialog", "b", None))
        self.label_50.setText(QtGui.QApplication.translate("Dialog", "D", None))
        self.label_7.setText(QtGui.QApplication.translate("Dialog", "D1", None))
        self.label_8.setText(QtGui.QApplication.translate("Dialog", "D2", None))
        self.label_9.setText(QtGui.QApplication.translate("Dialog", "D3", None))
        self.label_10.setText(QtGui.QApplication.translate("Dialog", "L", None))
        self.label_11.setText(QtGui.QApplication.translate("Dialog", "C", None))
        self.label_12.setText(QtGui.QApplication.translate("Dialog", "E", None))
        self.label_13.setText(QtGui.QApplication.translate("Dialog", "M", None))
        self.label_14.setText(QtGui.QApplication.translate("Dialog", "R", None))
        self.label_15.setText(QtGui.QApplication.translate("Dialog", "N1", None))
        self.label_16.setText(QtGui.QApplication.translate("Dialog", "N2", None))
        self.label_17.setText(QtGui.QApplication.translate("Dialog", "d", None))
        self.label_F.setText(QtGui.QApplication.translate("Dialog", "F", None))
        self.label_G1.setText(QtGui.QApplication.translate("Dialog", "G1", None))
        self.label_G2.setText(QtGui.QApplication.translate("Dialog", "G2", None))
        self.label_H.setText(QtGui.QApplication.translate("Dialog", "H", None))
        self.label_P.setText(QtGui.QApplication.translate("Dialog", "P", None))
        
        #self.pushButton.setText(QtGui.QApplication.translate("Dialog", "実行", None))
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
        global g
        global x4
        global x5
        global x6
        buhin='CycloMotorPulley.jpg'
        pic=buhin
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, 'png_data',pic)
        self.label_5.setPixmap(QtGui.QPixmap(joined_path))
        B0=self.comboBox_2.currentText()
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
        B2=float(sa[16]) 
        F=float(sa[17]) 
        G1=float(sa[18]) 
        G2=float(sa[19]) 
        H=float(sa[20]) 
        P=float(sa[21]) 
        g=sa[22]


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
        B00=str(int(B1))+' '+str(int(B2))
        self.lineEdit_B.setText(str(B00))
        self.lineEdit_G1.setText(str(G1))
        self.lineEdit_G2.setText(str(G2))
        self.lineEdit_H.setText(str(H))
        self.lineEdit_P.setText(str(P))
    
    def create(self):
        #label='Motor Pulley'
        label=self.comboBox_2.currentText()
        key=self.comboBox_2.currentIndex()

        try:
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
        except:
            doc=App.newDocument()
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)

        obj.addProperty("App::PropertyInteger", "key",label).key=key
        
        obj.addProperty("App::PropertyFloat", "A",label).A=A
        obj.addProperty("App::PropertyFloat", "a",label).a=a
        obj.addProperty("App::PropertyFloat", "b",label).b=b
        obj.addProperty("App::PropertyFloat", "D",label).D=D
        obj.addProperty("App::PropertyFloat", "D1",label).D1=D1
        obj.addProperty("App::PropertyFloat", "D2",label).D2=D2
        obj.addProperty("App::PropertyFloat", "D3",label).D3=D3
        obj.addProperty("App::PropertyFloat", "L",label).L=L
        obj.addProperty("App::PropertyFloat", "C",label).C=C
        obj.addProperty("App::PropertyFloat", "E",label).E=E
        obj.addProperty("App::PropertyFloat", "M",label).M=M
        obj.addProperty("App::PropertyFloat", "R",label).R=R
        obj.addProperty("App::PropertyFloat", "N1",label).N1=N1
        obj.addProperty("App::PropertyFloat", "N2",label).N2=N2
        obj.addProperty("App::PropertyFloat", "d",label).d=d
        obj.addProperty("App::PropertyFloat", "B1",label).B1=B1
        obj.addProperty("App::PropertyFloat", "B2",label).B2=B2
        obj.addProperty("App::PropertyFloat", "F",label).F=F
        obj.addProperty("App::PropertyFloat", "G1",label).G1=G1
        obj.addProperty("App::PropertyFloat", "G2",label).G2=G2
        obj.addProperty("App::PropertyFloat", "H",label).H=H
        obj.addProperty("App::PropertyFloat", "P",label).P=P
        obj.addProperty("App::PropertyFloat", "g",label).g=g

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
