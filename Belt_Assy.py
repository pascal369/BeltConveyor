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
import math

from PySide import QtGui
from PySide import QtUiTools
from PySide import QtCore
type_data=['MotorPulley',]
#type_data=['MotorPulley','ChainDrive','DirectDrive']
BeltW=['500','600','750',]
#       B0     b1     b2     t0    D0    d1   d2    Ls    h0
BDim={
      '500':( 180,   160.0,  10,  360,  300,  200,  500,  180,),
      '600':( 210,   195.0,  10,  360,  300,  200,  500,  180,),
      '750':( 265,   242.5,  10,  460,  380,  200,  500,  180,),
      '900':( 315,   292.5,  10,  520,  380,  200,  500,  180,),
      }
      
# 画面を並べて表示する
class Ui_Dialog(object):
    #print('aaaaaaa')
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(280, 400)
        Dialog.move(1000, 0)
        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(35, 170, 200, 200))
        self.label_6.setText("")
        
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, 'Belt_data','png_data',"Belt_Assy.png")
        self.label_6.setPixmap(QtGui.QPixmap(joined_path))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        #タイプ
        self.label_type = QtGui.QLabel('Type',Dialog)
        self.label_type.setGeometry(QtCore.QRect(30, 13, 100, 22))
        self.comboBox_type = QtGui.QComboBox(Dialog)
        self.comboBox_type.setGeometry(QtCore.QRect(150, 13, 100, 22))
        self.comboBox_type.listIndex=11

        #ベルト幅
        self.label_B = QtGui.QLabel('BeltWidth',Dialog)
        self.label_B.setGeometry(QtCore.QRect(30, 38, 100, 22))
        self.comboBox_B = QtGui.QComboBox(Dialog)
        self.comboBox_B.setGeometry(QtCore.QRect(150, 38, 100, 22))
        self.comboBox_B.listIndex=11
        
        #機長
        self.label_C = QtGui.QLabel('CenterDistance[mm]',Dialog)
        self.label_C.setGeometry(QtCore.QRect(30, 63, 100, 22))
        self.le_C = QtGui.QLineEdit(Dialog)
        self.le_C.setGeometry(QtCore.QRect(150, 63, 60, 20))
        self.le_C.setAlignment(QtCore.Qt.AlignCenter)
        #テールプーリ高さ
        self.label_h = QtGui.QLabel('tailPulleyHight[mm]',Dialog)
        self.label_h.setGeometry(QtCore.QRect(30, 93, 100, 22))
        self.le_h = QtGui.QLineEdit('1000',Dialog)
        self.le_h.setGeometry(QtCore.QRect(150, 93, 60, 20))
        self.le_h.setAlignment(QtCore.Qt.AlignCenter)
        #コンベヤ傾斜角
        self.label_k = QtGui.QLabel('inclinationDegree[degree]',Dialog)
        self.label_k.setGeometry(QtCore.QRect(30, 118, 100, 22))
        self.le_k = QtGui.QLineEdit('0',Dialog)
        self.le_k.setGeometry(QtCore.QRect(150, 118, 60, 20))
        self.le_k.setAlignment(QtCore.Qt.AlignCenter)
        #作成
        self.pushButton = QtGui.QPushButton('create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(30, 143, 60, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton('update',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(100, 143, 60, 22))
        #Import
        self.pushButton3 = QtGui.QPushButton('Import',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(170, 143, 60, 22))
        self.comboBox_B.addItems(BeltW)
        self.comboBox_type.addItems(type_data)
        self.le_C.setText('5000')
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.setParts)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "BeltConveyor", None))
        
    def setParts(self):
        global Spreadsheet
        global parts_group
        selection=''
        selection = Gui.Selection.getSelection()
        if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 parts_group = selected_object
                 print(parts_group.Label)
                 for obj in parts_group.Group:
                     #print(obj.Label)
                     if obj.TypeId == "Spreadsheet::Sheet":
                         Spreadsheet=obj
                         #print(obj.Label)

                         self.comboBox_B.setCurrentText(obj.getContents('F2'))     
                         self.le_C.setText(Spreadsheet.getContents('C0'))  
                         self.le_h.setText(Spreadsheet.getContents('Ht'))  
                         self.le_k.setText(Spreadsheet.getContents('k'))  
                         #print('aaaaaaaaaaaaaaaaaaa')
                         #parts_group.placement




    def update(self):

        try:
            h00=0
            key=self.comboBox_B.currentText()
            sa=BDim[key]
            L=self.le_C.text()
            Ht=float(self.le_h.text())
            h00=Ht-1000
            k=self.le_k.text()
            #print('aaaaaaaaaaaaaaaaaaa')
            Spreadsheet.set('C0',L)
            Spreadsheet.set('B0',key)
            Spreadsheet.set('b1',str(sa[0]))#b1
            
            Spreadsheet.set('b2',str(sa[1]))#b2
            Spreadsheet.set('t0',str(sa[2]))#t0
            Spreadsheet.set('D0',str(sa[3]))#D0  
            
            Spreadsheet.set('d1',str(sa[4]))#d1 
            
            Spreadsheet.set('d2',str(sa[5]))#d2
            
            
            Spreadsheet.set('Ls',str(sa[6]))#Ls
            Spreadsheet.set('h0',str(sa[7]))#h0
            
            Spreadsheet.set('Ht',str(Ht))#Ht
            Spreadsheet.set('k',k)#k
            
            placement = parts_group.Placement
            parts_group.Placement=App.Placement(App.Vector(placement.Base.x,placement.Base.y,Ht),App.Rotation(App.Vector(0,0,1),0))
            #print('aaaaaaaaaaaaaaaaa')
            N=int((float(L)-1400)/2500)+1
            
            postX=(float(L)-1400)*math.cos(float(k)/57.3)/N
            print(postX)
            Spreadsheet.set('postN',str(N))
            Spreadsheet.set('postX',str(postX))


            App.ActiveDocument.recompute()
        except:
            print('select an object')    
        
    
    def create(self): 
         W0=self.comboBox_B.currentText()
         if self.comboBox_type.currentText()=='MotorPulley':
             dPath='MotorPulley'
             fname='BeltCv'+W0+'BAssy_M.FCStd'
         elif self.comboBox_type.currentText()=='ChainDrive' :
             dPath='ChainDrive'
             fname='BeltCv'+W0+'BAssy_C.FCStd'
         elif self.comboBox_type.currentText()=='DirectDrive' :
             dPath='DirectDrive'
             fname='BeltCv'+W0+'BAssy_D.FCStd'    
         dPath2=self.comboBox_B.currentText()+'B'       

         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base, 'Belt_data','assy_data',dPath,dPath2,fname) 

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