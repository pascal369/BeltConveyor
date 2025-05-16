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
import csv

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
        Dialog.resize(280, 470)
        Dialog.move(1000, 0)
        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(35, 270, 200, 200))
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

        #質量計算
        self.pushButton_m = QtGui.QPushButton('massCulculation',Dialog)
        self.pushButton_m.setGeometry(QtCore.QRect(30, 170, 100, 23))
        self.pushButton_m.setObjectName("pushButton") 
        #質量集計
        self.pushButton_m20 = QtGui.QPushButton('massTally_csv',Dialog)
        self.pushButton_m20.setGeometry(QtCore.QRect(130, 170, 130, 23))
        self.pushButton_m2 = QtGui.QPushButton('massTally_SpreadSheet',Dialog)
        self.pushButton_m2.setGeometry(QtCore.QRect(130, 195, 130, 23))
        #質量入力
        self.pushButton_m3 = QtGui.QPushButton('massImput[kg]',Dialog)
        self.pushButton_m3.setGeometry(QtCore.QRect(30, 220, 100, 23))
        self.pushButton_m3.setObjectName("pushButton")  
        self.le_mass = QtGui.QLineEdit(Dialog)
        self.le_mass.setGeometry(QtCore.QRect(130, 220, 50, 20))
        self.le_mass.setAlignment(QtCore.Qt.AlignCenter)  
        self.le_mass.setText('10.0')
        #密度
        self.lbl_gr = QtGui.QLabel('SpecificGravity',Dialog)
        self.lbl_gr.setGeometry(QtCore.QRect(30, 250, 80, 12))
        self.le_gr = QtGui.QLineEdit(Dialog)
        self.le_gr.setGeometry(QtCore.QRect(130, 245, 50, 20))
        self.le_gr.setAlignment(QtCore.Qt.AlignCenter)  
        self.le_gr.setText('7.85')

        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.setParts)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.update)
        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton_m, QtCore.SIGNAL("pressed()"), self.massCulc)
        QtCore.QObject.connect(self.pushButton_m2, QtCore.SIGNAL("pressed()"), self.massTally)
        QtCore.QObject.connect(self.pushButton_m20, QtCore.SIGNAL("pressed()"), self.massTally2)
        QtCore.QObject.connect(self.pushButton_m3, QtCore.SIGNAL("pressed()"), self.massImput)

        QtCore.QMetaObject.connectSlotsByName(Dialog)
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "BeltConveyorAssy", None))
        
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
        c00 = Gui.Selection.getSelection()
        if c00:
            obj = c00[0]
        label='mass[kg]'
        g0=float(self.le_gr.text())
        g=round(obj.Shape.Volume*g0*1000/10**9,2) 
        try:
            obj.addProperty("App::PropertyFloat", "mass",label)
            obj.mass=g
            
        except:
            obj.mass=g
            pass

    def massTally2(self):#csv
        doc = App.ActiveDocument
        objects = doc.Objects
        mass_list = []
        for obj in objects:
                    
            if obj.Label=='本体' or obj.Label=='本体 (mirrored)' or obj.Label[:7]=='Channel' or obj.Label[:7]=='Extrude' or obj.Label[:6]=='Fusion':
                pass        
            #if Gui.ActiveDocument.getObject(obj.Name).Visibility:
                #if obj.isDerivedFrom("Part::Feature"):
            else:    
                if hasattr(obj, "Shape") :
                    try:
                        if obj.Label[:7]=='Carrier':
                            n1=carrierArray.Count
                        elif obj.Label[:6]=='Return':
                            n1=returnArray.Count  
                        elif obj.Label[:3]=='UCP':
                            n1=2 
                        elif obj.Label[:6]=='TakeUp':
                            n1=2          
                        else:
                            n1=1 
                        obj.mass=round(obj.mass,2)    
                        g=round(obj.mass*n1,2)      
                        mass_list.append([obj.Label,str(n1),obj.mass, str(g)])
                    except:
                        #print('aaaaaaaaaaaaaa')
                        pass    
                #else:
                #     pass
                    doc_path = doc.FileName
                    csv_filename = os.path.splitext(os.path.basename(doc_path))[0] + "_parts_list.csv"
                    csv_path = os.path.join(os.path.dirname(doc_path), csv_filename)
                    with open(csv_path, 'w', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(['Name','Count','Unit', "Mass[kg]"])
                        writer.writerows(mass_list) 

    def massTally(self):#spreadsheet
        doc = App.ActiveDocument
        # 新しいスプレッドシートを作成
        try:
            spreadsheet=doc.Spreadsheet('PartsList')
        except:
            spreadsheet = doc.addObject("Spreadsheet::Sheet", "PartList")
            spreadsheet.Label = "Parts List"
        
        # ヘッダー行を記入
        headers = ['No',"Name", 'Count','Unit[kg]','Mass[kg]']
        for header in enumerate(headers):
            spreadsheet.set(f"A{1}", headers[0])
            spreadsheet.set(f"B{1}", headers[1])
            spreadsheet.set(f"C{1}", headers[2])
            spreadsheet.set(f"D{1}", headers[3])
            spreadsheet.set(f"E{1}", headers[4])
            
        # パーツを列挙して情報を書き込む
        row = 2
        i=1
        s=0
        n1=1
        for i,obj in enumerate(doc.Objects):
            try:
                spreadsheet.set(f"E{row}", f"{obj.mass:.2f}")  # mass
                s=round(obj.mass,2)+s
                if obj.Label=='本体' or obj.Label=='本体 (mirrored)' or obj.Label[:7]=='Channel' or obj.Label[:7]=='Extrude' or obj.Label[:6]=='Fusion':
                    pass

                else:
                    if hasattr(obj, "Shape") and obj.Shape.Volume > 0:
                       
                        try:
                            spreadsheet.set(f"A{row}", str(row-1))  # No
                            spreadsheet.set(f"B{row}", obj.Label)
                            if obj.Label[:7]=='Carrier':
                                n1=carrierArray.Count
                            elif obj.Label[:6]=='Return':
                                n1=returnArray.Count  
                            elif obj.Label[:3]=='UCP':
                                n1=2 
                            elif obj.Label[:6]=='TakeUp':
                                n1=2          
                            else:
                                n1=1    
                            spreadsheet.set(f"C{row}", str(n1))   # count
                            spreadsheet.set(f"D{row}", f"{obj.mass:.2f}")  #unit
                            g=round(float(obj.mass)*n1,2)
                            spreadsheet.set(f"E{row}", str(g))  #unit*count
                            row += 1
                        except:
                            pass    
            except:
                pass

            #spreadsheet.set(f'E{row}',str(s))
        App.ActiveDocument.recompute()
        Gui.activeDocument().activeView().viewAxometric()
    
    
    def setParts(self):
        global Spreadsheet
        global Cover
        global carrierArray
        global returnArray
        global waterReceptacle
        global Post
        global Frame
        global Belt
        global Skirt

        doc = App.ActiveDocument
        objects = doc.Objects
        mass_list = []
        for obj in objects:
             #print(obj.Label)
             if obj.Label == "shtBeltAssy":
                 Spreadsheet=obj
             elif obj.Label=='Cover':
                 Cover=obj
             elif obj.Label=='carrierArray':
                 carrierArray=obj 
             elif obj.Label=='returnArray':
                 returnArray=obj 
             elif obj.Label=='waterReceptacle':
                 waterReceptacle=obj  
             elif obj.Label=='Post':
                 Post=obj  
             elif obj.Label=='Frame':
                 Frame=obj 
             elif obj.Label=='Belt':
                 Belt=obj 
             elif obj.Label=='Skirt':
                 Skirt=obj        

        self.comboBox_B.setCurrentText(Spreadsheet.getContents('B0'))   
        self.le_C.setText(Spreadsheet.getContents('C0'))  
        self.le_h.setText(Spreadsheet.getContents('Ht'))  
        self.le_k.setText(Spreadsheet.getContents('k'))  

    def update(self):
        try:
            h00=0
            key=self.comboBox_B.currentText()
            sa=BDim[key]
            L=self.le_C.text()
            Ht=float(self.le_h.text())
            h00=Ht-1000
            k=self.le_k.text()
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

            N=int((float(L)-1400)/2500)+1
            postX=(float(L)-1400)*math.cos(float(k)/57.3)/N
            Spreadsheet.set('postN',str(N))
            Spreadsheet.set('postX',str(postX))
            App.ActiveDocument.recompute()

            #cover
            g0=7.85
            g=round(Cover.Shape.Volume*g0*1000/10**9,2) 
            Cover.mass=g
            #waterReceptacle
            g0=7.85
            g=round(waterReceptacle.Shape.Volume*g0*1000/10**9,2)
            waterReceptacle.mass=g
            #Frame
            g0=7.85
            g=round(Frame.Shape.Volume*g0*1000/10**9*2,2)
            Frame.mass=g
            #Post
            g0=7.85
            g=round(Post.Shape.Volume*g0*1000/10**9*2,2)
            Post.mass=g
            #Skirt
            g0=7.85
            g=round(Skirt.Shape.Volume*g0*1000/10**9*2,2)
            Skirt.mass=g
            #Belt
            g0=1.0
            g=round(Belt.Shape.Volume*g0*1000/10**9*2,2)
            Belt.mass=g
            
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