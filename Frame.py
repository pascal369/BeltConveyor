# -*- coding: utf-8 -*-
import os
import sys
import Import
import Spreadsheet
import DraftVecUtils
import Sketcher
import PartDesign
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui
from PySide import QtUiTools
from PySide import QtCore


BeltW=['400','450','500','600','700','750','800','900','1000',]
#       B0     b1     b2     t0    D0    d1   d2    Ls    h0
BDim={'400':( 145,   127.5,  10,  300,  260,  200,  500,  180,),	
      '450':( 165,   142.5,  10,  300,  260,  200,  500,  180,),
      '500':( 180,   160.0,  10,  360,  300,  200,  500,  180,),
      '600':( 210,   195.0,  10,  360,  300,  200,  500,  180,),
      '700':( 250,   225.0,  10,  360,  300,  200,  500,  180,),
      '750':( 265,   242.5,  10,  460,  390,  200,  500,  180,),
      '800':( 280,   260.0,  10,  460,  390,  200,  500,  180,),
      '900':( 315,   292.5,  10,  520,  440,  200,  500,  180,),
      '1000':(345,   327.5,  10,  520,  440,  200,  500,  180,),}
      
# 画面を並べて表示する
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(500, 250)
        Dialog.move(1000, 0)
        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(35, 70, 400, 200))
        self.label_6.setText("")
        self.label_6.setAlignment(QtCore.Qt.AlignTop)

        
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, 'Belt_data','png_data',"Frame.png")
        self.label_6.setPixmap(QtGui.QPixmap(joined_path))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        #ベルト幅
        self.label_B = QtGui.QLabel('BeltWidth',Dialog)
        self.label_B.setGeometry(QtCore.QRect(30, 13, 100, 22))
        self.comboBox_B = QtGui.QComboBox(Dialog)
        self.comboBox_B.setGeometry(QtCore.QRect(150, 13, 60, 22))
        self.comboBox_B.listIndex=11
        
        #機長
        self.label_C = QtGui.QLabel('C[mm]',Dialog)
        self.label_C.setGeometry(QtCore.QRect(30, 38, 100, 22))
        self.le_C = QtGui.QLineEdit(Dialog)
        self.le_C.setGeometry(QtCore.QRect(150, 38, 60, 20))
        self.le_C.setAlignment(QtCore.Qt.AlignCenter)
        #H
        self.label_H = QtGui.QLabel('H[mm]',Dialog)
        self.label_H.setGeometry(QtCore.QRect(220, 13, 100, 22))
        self.le_H = QtGui.QLineEdit(Dialog)
        self.le_H.setGeometry(QtCore.QRect(350, 13, 60, 20))
        self.le_H.setAlignment(QtCore.Qt.AlignCenter)
        #h1
        self.label_h1 = QtGui.QLabel('h1[mm]',Dialog)
        self.label_h1.setGeometry(QtCore.QRect(220, 38, 100, 22))
        self.le_h1 = QtGui.QLineEdit(Dialog)
        self.le_h1.setGeometry(QtCore.QRect(350, 38, 60, 20))
        self.le_h1.setAlignment(QtCore.Qt.AlignCenter)
        #h2
        self.label_h2 = QtGui.QLabel('h2[mm]',Dialog)
        self.label_h2.setGeometry(QtCore.QRect(220, 63, 100, 22))
        self.le_h2 = QtGui.QLineEdit(Dialog)
        self.le_h2.setGeometry(QtCore.QRect(350, 63, 60, 20))
        self.le_h2.setAlignment(QtCore.Qt.AlignCenter)
        #inclination angle
        self.label_k = QtGui.QLabel('inclination angle [deg]',Dialog)
        self.label_k.setGeometry(QtCore.QRect(220, 88, 120, 22))
        self.le_k = QtGui.QLineEdit(Dialog)
        self.le_k.setGeometry(QtCore.QRect(350, 88, 60, 20))
        self.le_k.setAlignment(QtCore.Qt.AlignCenter)

        #作成
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(30, 65, 60, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton(Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(121, 65, 60, 22))
        #インポート
        self.pushButton3 = QtGui.QPushButton('Import',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(30, 90, 180, 22))
        self.comboBox_B.addItems(BeltW)
        self.le_C.setText('5000')
        self.le_H.setText('1000')
        self.le_h1.setText('50')
        self.le_h2.setText('73')
        self.le_k.setText('0')

        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.importData)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "beltCvFrame", None))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Create", None))  
        self.pushButton2.setText(QtGui.QApplication.translate("Dialog", "Update", None))  

    def importData(self):
        global spreadsheet
        selection = Gui.Selection.getSelection()
        if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 parts_group = selected_object
                 for obj in parts_group.Group:
                     #print(obj.Label)
                     if obj.TypeId == "Spreadsheet::Sheet":
                         spreadsheet = obj

                         self.comboBox_B.setCurrentText(spreadsheet.getContents('B0'))
                         self.le_C.setText(spreadsheet.getContents('C0'))
                         self.le_H.setText(spreadsheet.getContents('Ht'))
                         self.le_h1.setText(spreadsheet.getContents('h1'))
                         self.le_h2.setText(spreadsheet.getContents('h2'))
                         self.le_k.setText(spreadsheet.getContents('k'))
       
   
    def update(self):
         key=self.comboBox_B.currentText()
         sa=BDim[key]
         L=self.le_C.text()
         H=self.le_H.text()
         h1=self.le_h1.text()
         h2=self.le_h2.text()
         k=self.le_k.text()
         W0=float(key)+310
         spreadsheet.set('C0',L)
         spreadsheet.set('B0',key)
         spreadsheet.set('Ht',H)
         spreadsheet.set('h1',h1)
         spreadsheet.set('h2',h2)
         spreadsheet.set('k',k)
         spreadsheet.set('W0',str(W0))
         C0=spreadsheet.getContents('C0') 
         post_c=int((float(C0)-1300)/2500)
         post_x=(float(C0)-1300)/(post_c+1)
         spreadsheet.set('post_c',str(post_c))
         spreadsheet.set('post_x',str(post_x))
         App.ActiveDocument.recompute()

    def create(self): 
        
         fname='Frame.FCStd'
         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base,'Belt_data',fname) 
         try:
            Gui.ActiveDocument.mergeProject(joined_path)
         except:
            doc=App.newDocument()
            Gui.ActiveDocument.mergeProject(joined_path)
         Gui.SendMsgToActiveView("ViewFit")   
         
class main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show() 
        script_window = Gui.getMainWindow().findChild(QtGui.QDialog, 'd')
        script_window.setWindowFlags(script_window.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)       
        
        