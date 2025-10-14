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
takeupDia=['20','25','30','35','40','45','50']
#       B0     b1     b2     t0    D0    d1   d2    Ls    h0
BDim={'400':( 145,   127.5,  10,  300,  260,  200,  500,  180,),	
      '450':( 165,   142.5,  10,  300,  260,  200,  500,  180,),
      '500':( 180,   160.0,  10,  300,  300,  200,  500,  180,),
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
        self.label_6.setAlignment(QtCore.Qt.AlignTop)
        
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, 'Belt_data','png_data',"takeupAssy.png")
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
        #テークアップ軸径
        self.label_d = QtGui.QLabel('takeUpDia',Dialog)
        self.label_d.setGeometry(QtCore.QRect(30, 38, 100, 22))
        self.label_d.setStyleSheet("color: gray;")
        self.comboBox_d = QtGui.QComboBox(Dialog)
        self.comboBox_d.setGeometry(QtCore.QRect(150, 38, 60, 22))
        #self.comboBox_d.listIndex=11
        #プーリ径
        self.label_C = QtGui.QLabel('pulleyDia',Dialog)
        self.label_C.setGeometry(QtCore.QRect(30, 63, 100, 22))
        self.label_C.setStyleSheet("color: gray;")
        self.le_C = QtGui.QLineEdit(Dialog)
        self.le_C.setGeometry(QtCore.QRect(150, 63, 60, 20))
        self.le_C.setAlignment(QtCore.Qt.AlignCenter)
        #作成
        self.pushButton = QtGui.QPushButton('Create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(100, 90, 100, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton('Update',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(100, 115, 100, 22))
        #import
        self.pushButton3 = QtGui.QPushButton('Import',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(100, 140, 100, 22))
        self.comboBox_B.addItems(BeltW)
        self.comboBox_d.addItems(takeupDia)

        
        self.le_C.setText('300')
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.import_data)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.update)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "takeUpAssy", None))
        

    def import_data(self):
         global Take_upPulley
         global spreadsheet
         global B
         selection = Gui.Selection.getSelection()
         # Partsグループが選択されているかチェック
         if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 parts_group = selected_object
                 for obj in parts_group.Group:
                     print(obj.Label)
                     if obj.Label=='Take_upPulley':
                         Take_upPulley=obj
                     elif obj.Label == "Spreadsheet_takeup":
                         spreadsheet = obj
                 B=spreadsheet.getContents('W0')
                 d0=spreadsheet.getContents('d0')
                 D0=spreadsheet.getContents('D0')
                 self.comboBox_B.setCurrentText(B)  
                 self.comboBox_d.setCurrentText(d0)     
                 self.le_C.setText(D0) 
   
    def update(self):
         
         try:
             for i in range(3,12):
                 W0=self.comboBox_B.currentText()
                 if W0==spreadsheet.getContents('A'+str(i+2)):
                     break

             W0=spreadsheet.getContents('A'+str(i+2))
             d0=spreadsheet.getContents('B'+str(i+2))
             D0=spreadsheet.getContents('D'+str(i+2))
             L0=spreadsheet.getContents('E'+str(i+2))
             B0=spreadsheet.getContents('G'+str(i+2))
             Y=spreadsheet.getContents('H'+str(i+2))

             spreadsheet.set('W0',W0)  
             spreadsheet.set('d0',d0) 
             spreadsheet.set('D0',D0)    
             spreadsheet.set('L0',L0)  
             spreadsheet.set('B0',B0)   
             spreadsheet.set('Y',Y) 


             Take_upPulley.BeltWidth=W0
             App.ActiveDocument.recompute()    
         except:
             'error'
             return                 

    def create(self): 
         fname='Take-Up_Assy.FCStd'
         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base,'Belt_data','takeup_data',fname) 
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
        ## 閉じるボタンを無効にする
        script_window = Gui.getMainWindow().findChild(QtGui.QDialog, 'd') 
        script_window.setWindowFlags(script_window.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)            
        