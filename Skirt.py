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
        Dialog.resize(250, 370)
        Dialog.move(1000, 0)
        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(35, 165, 200, 200))
        self.label_6.setText("")
        
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, 'Belt_data','png_data',"Skirt.png")
        self.label_6.setPixmap(QtGui.QPixmap(joined_path))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        
        #ベルト幅
        self.label_B = QtGui.QLabel('BeltWidth',Dialog)
        self.label_B.setGeometry(QtCore.QRect(30, 13, 100, 22))
        self.label_B.setStyleSheet("color: gray;")
        self.comboBox_B = QtGui.QComboBox(Dialog)
        self.comboBox_B.setGeometry(QtCore.QRect(150, 13, 60, 22))
        self.comboBox_B.listIndex=11
        
        #機長
        self.label_C = QtGui.QLabel('CenterDistance',Dialog)
        self.label_C.setGeometry(QtCore.QRect(30, 38, 100, 22))
        self.label_C.setStyleSheet("color: gray;")
        self.le_C = QtGui.QLineEdit(Dialog)
        self.le_C.setGeometry(QtCore.QRect(150, 38, 60, 20))
        self.le_C.setAlignment(QtCore.Qt.AlignCenter)

        #作成
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(30, 110, 50, 22))

        #更新
        self.pushButton2 = QtGui.QPushButton(Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(120, 110, 50, 22))
        #import
        self.pushButton3 = QtGui.QPushButton('Import',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(30, 135, 180, 22))

        #self.comboBox_parts.addItems(parts)
        self.comboBox_B.addItems(BeltW)

        self.comboBox_B.setCurrentIndex(1)
        self.comboBox_B.currentIndexChanged[int].connect(self.onWidth) 
        self.comboBox_B.setCurrentIndex(0)
        self.le_C.setText('5000')

        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.importData)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.update)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Skirt", None))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Create", None))  
        self.pushButton2.setText(QtGui.QApplication.translate("Dialog", "Update", None))  

    def onWidth(self):
        return
        global L
        L=self.le_C.text()
   
    def importData(self):
        global spreadsheet
        selection = Gui.Selection.getSelection()
        if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 parts_group = selected_object
                 for obj in parts_group.Group:
                     if obj.TypeId == "Spreadsheet::Sheet":
                         spreadsheet = obj

                         self.comboBox_B.setCurrentText(spreadsheet.getContents('B0'))
                         self.le_C.setText(spreadsheet.getContents('C0'))
                         
    def update(self):
        # selection = Gui.Selection.getSelection()
        # for obj in selection:
        #     try:
         key=self.comboBox_B.currentText()
         sa=BDim[key]
         L=self.le_C.text()
         W=float(key)+310
         spreadsheet.set('B2',L)
         spreadsheet.set('B3',key)
         spreadsheet.set('W0',str(W))
         App.ActiveDocument.recompute()

    def create(self): 
         doc = App.ActiveDocument
         fname='Skirt.FCStd'
         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base,'Belt_data',fname) 
         try:
            Gui.ActiveDocument.mergeProject(joined_path)
         except:
            doc=App.newDocument()
            Gui.ActiveDocument.mergeProject(joined_path)
         
class main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show()  
        script_window = Gui.getMainWindow().findChild(QtGui.QDialog, 'd') 
        script_window.setWindowFlags(script_window.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)            
        
        