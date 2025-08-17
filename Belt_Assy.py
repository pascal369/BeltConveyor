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
import csv
from PySide import QtGui
from PySide import QtUiTools
from PySide import QtCore
import FreeCAD

type_data=['MotorPulley',]
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
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(280, 510)
        Dialog.move(1000, 0)
        
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

        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(35, 170, 200, 200))
        self.label_6.setText("")
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, 'Belt_data','png_data',"Belt_Assy.png")
        self.label_6.setPixmap(QtGui.QPixmap(joined_path))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")

        #質量計算
        self.pushButton_m = QtGui.QPushButton('massCulculation',Dialog)
        self.pushButton_m.setGeometry(QtCore.QRect(30, 380, 100, 23))
        self.pushButton_m.setObjectName("pushButton")  
        
        #質量集計_spreadsheet
        self.pushButton_m2 = QtGui.QPushButton('massTally_spreadsheet',Dialog)
        self.pushButton_m2.setGeometry(QtCore.QRect(130, 380, 120, 23))
        self.pushButton_m2.setObjectName("pushButton")
        
        #質量入力
        self.pushButton_m3 = QtGui.QPushButton('massImput[kg]',Dialog)
        self.pushButton_m3.setGeometry(QtCore.QRect(30, 430, 100, 23))
        self.pushButton_m3.setObjectName("pushButton")  
        self.le_mass = QtGui.QLineEdit(Dialog)
        self.le_mass.setGeometry(QtCore.QRect(130, 430, 50, 20))
        self.le_mass.setAlignment(QtCore.Qt.AlignCenter)  
        self.le_mass.setText('10.0')
        #密度
        self.lbl_gr = QtGui.QLabel('SpecificGravity',Dialog)
        self.lbl_gr.setGeometry(QtCore.QRect(30, 455, 80, 12))
        self.le_gr = QtGui.QLineEdit(Dialog)
        self.le_gr.setGeometry(QtCore.QRect(130, 455, 50, 20))
        self.le_gr.setAlignment(QtCore.Qt.AlignCenter)  
        self.le_gr.setText('7.85')

        self.comboBox_B.addItems(BeltW)
        self.comboBox_type.addItems(type_data)
        self.le_C.setText('5000')
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.setParts)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.update)
        for i in range(2):
            QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)

        self.retranslateUi(Dialog)
        
        QtCore.QObject.connect(self.pushButton_m, QtCore.SIGNAL("pressed()"), self.massCulc)
        QtCore.QObject.connect(self.pushButton_m2, QtCore.SIGNAL("pressed()"), self.massTally)
        QtCore.QObject.connect(self.pushButton_m3, QtCore.SIGNAL("pressed()"), self.massImput)
        
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "BeltCvAssy", None))
        
    def massImput(self):
         # 選択したオブジェクトを取得する
        c00 = Gui.Selection.getSelection()
        if c00:
            obj = c00[0]
        label='mass[kg]'
        g=float(self.le_mass.text())
        try:
            obj.addProperty("App::PropertyFloat", "mass",label)
            obj.mass=g
        except:
            obj.mass=g

    def massCulc(self):
        # 選択したオブジェクトを取得する
        c00 = Gui.Selection.getSelection()
        if c00:
            obj = c00[0]
        label='mass[kg]'
        g0=float(self.le_gr.text())
        g=obj.Shape.Volume*g0*1000/10**9  
        try:
            obj.addProperty("App::PropertyFloat", "mass",label)
            obj.mass=g
        except:
            obj.mass=g
            pass

    def massTally(self):#spreadsheet
        doc = App.ActiveDocument
        # 新しいスプレッドシートを作成
        spreadsheet = doc.addObject("Spreadsheet::Sheet", "Parts_List")
        spreadsheet.Label = "Parts_List"
        # ヘッダー行を記入
        headers = ['No',"Name",'Standard', 'Count','Unit[kg]','Mass[kg]']
        for header in enumerate(headers):
            spreadsheet.set(f"A{1}", headers[0])
            spreadsheet.set(f"B{1}", headers[1])
            spreadsheet.set(f"C{1}", headers[2])
            spreadsheet.set(f"D{1}", headers[3])
            spreadsheet.set(f"E{1}", headers[4])
            spreadsheet.set(f"F{1}", headers[5])
        # パーツを列挙して情報を書き込む
        row = 2
        i=1
        s=0
        for i,obj in enumerate(doc.Objects):
            if obj.Label=='本体' or obj.Label=='本体 (mirrored)' or obj.Label[:7]=='Channel' or obj.Label[:5]=='Angle' \
                or obj.Label[:6]=='Square' or obj.Label[:7]=='Extrude' or obj.Label[:6]=='Fusion' or obj.Label[:6]=='Corner' \
                    or obj.Label[:5]=='basic' or obj.Label[:4]=='Edge' or obj.Label[:3]=='hub' or obj.Label[:7]=='_8_tube'\
                        or obj.Label[:5]=='plate' or obj.Label[:6]=='keyway' or obj.Label[:4]=='tube' or obj.Label[:5]=='color'\
                            or obj.Label[:6]=='HShape':
                pass        
            else:  
                try:
                    spreadsheet.set(f"E{row}", f"{obj.mass:.2f}")  # Unit
                    
                    if hasattr(obj, "Shape") and obj.Shape.Volume > 0:
                        try:
                            spreadsheet.set(f"A{row}", str(row-1))  # No
                            spreadsheet.set(f"B{row}", obj.Label)   #Name
                            try:
                                spreadsheet.set(f"C{row}", obj.dia)
                            except:
                                pass
                            if obj.Label[:6]=='Return':
                                n=returnArray.Count
                            elif obj.Label[:7]=='Carrier':
                                n=carrierArray.Count    
                            else:
                                n=1    
                            spreadsheet.set(f"D{row}", str(n))   # count
                            g=round(obj.mass*n,2)
                            spreadsheet.set(f"F{row}", str(g))   # g
                            s=g+s
                            row += 1
                        except:
                            print('error')
                            pass    
                except:
                    pass
                spreadsheet.set(f'F{row}',str(s))
        App.ActiveDocument.recompute()
        Gui.activeDocument().activeView().viewAxometric()      

    def setParts(self):
        global shtBeltCvAssy
        global takeUpAssy
        global bendPully
        global Skirt
        global Cover
        global waterReceptacle
        global Belt
        global Carrier
        global Return
        global Scraper
        global Frame
        global Post
        global returnArray
        global carrierArray
        global CPM
        global Self_Aligning_Carrier
        global Self_Aligning_Return
        global Parts_List
        
        doc = FreeCAD.activeDocument()
        if doc:
             group_names = []
             for obj in doc.Objects:
                 if obj.Label[:13] == "shtBeltCvAssy":
                     shtBeltCvAssy = obj
                 elif obj.Label[:10]=='takeUpAssy':
                     takeUpAssy=obj 
                 elif obj.Label=='bendPully':
                     bendPully=obj  
                 elif obj.Label[:5]=='Skirt':
                     Skirt=obj   
                 elif obj.Label[:5]=='Cover':
                     Cover=obj 
                 elif obj.Label[:15]=='waterReceptacle':
                     waterReceptacle=obj     
                 elif obj.Label[:4]=='Belt':
                     Belt=obj 
                 elif obj.Label[:7]=='Carrier':
                     Carrier=obj     
                 elif obj.Label[:6]=='Return':
                     Return=obj  
                 elif obj.Label[:7]=='Scraper':
                     Scraper=obj      
                 elif obj.Label[:5]=='Frame':
                     Frame=obj  
                 elif obj.Label[:4]=='Post':
                     Post=obj  
                 elif obj.Label=='returnArray':
                     returnArray=obj   
                 elif obj.Label=='carrierArray':
                     carrierArray=obj    
                 elif obj.Label[:3] =='CPM':
                     CPM=obj
                 elif obj.Label[:21] =='Self_Aligning_Carrier':
                     Self_Aligning_Carrier=obj   
                 elif obj.Label[:20] =='Self_Aligning_Return':
                     Self_Aligning_Return=obj   
                 elif obj.Label=='Parts_List':
                     #print('aaaaaaaaaaaaaaaaaaaaaaa')
                     Parts_List=obj    

                 print(obj.Label)
                 self.comboBox_B.setCurrentText(shtBeltCvAssy.getContents('F2'))     
                 self.le_C.setText(shtBeltCvAssy.getContents('B2'))  
                 self.le_h.setText(shtBeltCvAssy.getContents('Ht'))
                 self.le_k.setText(shtBeltCvAssy.getContents('k'))        

    def update(self):
        
        try:
            key=self.comboBox_B.currentText()
            sa=BDim[key]
            L=self.le_C.text()
            Ht=self.le_h.text()
            k=self.le_k.text()
            
            shtBeltCvAssy.set('B2',L)
            shtBeltCvAssy.set('B0',key)
            shtBeltCvAssy.set('b1',str(sa[0]))#b1
            shtBeltCvAssy.set('b2',str(sa[1]))#b2
            shtBeltCvAssy.set('t0',str(sa[2]))#t0
            shtBeltCvAssy.set('D0',str(sa[3]))#D0  
            shtBeltCvAssy.set('d1',str(sa[4]))#d1 
            shtBeltCvAssy.set('d2',str(sa[5]))#d2
            shtBeltCvAssy.set('Ls',str(sa[6]))#Ls
            shtBeltCvAssy.set('h0',str(sa[7]))#h0
            shtBeltCvAssy.set('Ht',Ht)#Ht
            shtBeltCvAssy.set('k',k)#k
            
            C0=shtBeltCvAssy.getContents('C0') 
            
            post_c=int((float(C0)-1300)/2500)
            
            post_x=round((float(C0)-1300)/(post_c+1),2)
            
            shtBeltCvAssy.set('post_c',str(post_c))
            
            shtBeltCvAssy.set('post_x',str(post_x))
            
            g0=7.85
            g=round(takeUpAssy.Shape.Volume*g0*1000/10**9,2) 
            takeUpAssy.mass=g
            
            
            g0=7.85
            g=round(bendPully.Shape.Volume*g0*1000/10**9,2) 
            bendPully.mass=g
           

            g0=7.85
            g=round(Skirt.Shape.Volume*g0*1000/10**9,2) 
            Skirt.mass=g
            
            g0=7.85
            g=round(Cover.Shape.Volume*g0*1000/10**9,2) 
            Cover.mass=g
            

            g0=7.85
            g=round(waterReceptacle.Shape.Volume*g0*1000/10**9,2) 
            waterReceptacle.mass=g
            
            g0=1.0
            g=round(Belt.Shape.Volume*g0*1000/10**9,2) 
            Belt.mass=g
            
            g0=7.85
            g=round(Carrier.Shape.Volume*g0*1000/10**9,2) 
            Carrier.mass=g
            
            g0=7.85
            g=round(Return.Shape.Volume*g0*1000/10**9,2) 
            Return.mass=g
            
            g0=7.85
            g=round(Scraper.Shape.Volume*g0*1000/10**9,2) 
            Scraper.mass=g
            
            g0=7.85
            g=round(Frame.Shape.Volume*g0*1000/10**9,2) 
            Frame.mass=g
            
            g0=7.85
            g=round(Post.Shape.Volume*g0*1000/10**9,2) 
            Post.mass=g
            
            g0=7.85
            g=round(CPM.Shape.Volume*g0*1000/10**9,2) 
            CPM.mass=g
            
            g0=7.85
            g=round(Self_Aligning_Carrier.Shape.Volume*g0*1000/10**9,2) 
            Self_Aligning_Carrier.mass=g
            
            g0=7.85
            g=round(Self_Aligning_Return.Shape.Volume*g0*1000/10**9,2) 
            Self_Aligning_Return.mass=g

        
            App.ActiveDocument.recompute()
        except:
            print('error')
            return    
    
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
         joined_path = os.path.join(base, 'assy_data',dPath,dPath2,fname) 
         print(joined_path)
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