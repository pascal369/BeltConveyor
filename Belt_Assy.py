# -*- coding: utf-8 -*-
import os
import sys
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui
from PySide import QtUiTools
from PySide import QtCore
import BeltCv
from Belt_data import mtrply_data

type_data=['MotorPulley',]
BeltW=['400','450','500','600','700','750','800','900',]
#       B0     b1     b2     t0    D0    d1   d2    Ls    h0   h1  h2  z   zb    zs    za     zr    vx   vh    vh2   hsk   hsk2  hwa
BDim={'400':( 145,   127.5,  10,  290,  260,  200,  500,  180, 25, 27, 20, 160,  263,  75 ,  182,  550,  -21,   98,  150,  350,   0),	
      '450':( 165,   142.5,  10,  300,  260,  200,  500,  180, 29, 42, 16, 160,  260,  75 ,  182,  600,  -15,   98,  150,  350,   0),
      '500':( 180,   160.0,  10,  300,  300,  200,  500,  180, 29, 43, 16, 160,  260,  75 ,  182,  600,  -15,   98,  150,  360,   0),
      '600':( 210,   195.0,  10,  360,  300,  200,  500,  180, 35, 65, -2, 150,  255,  75 ,  200,  700,   15,  120,  150,  390,  15),
      '700':( 250,   225.0,  10,  360,  300,  200,  500,  180, 35, 65, -2, 155,  255,  75 ,  205,  750,   15,  120,  150,  400,  30),
      '750':( 265,   242.5,  10,  360,  390,  200,  500,  180, 18, 47, 10, 170,  270,  95 ,  220,  800,   -2,  120,  150,  430,  40),
      '800':( 280,   260.0,  10,  460,  390,  200,  500,  180, 57,105,-30, 125,  230,  60 ,  233,  900,   70,  155,  150,  440,  75),
      '900':( 315,   292.5,  10,  520,  440,  200,  500,  180, 80,150,-53, 100,  210,  40 ,  270,  950,  102,  165,  150,  450, 125),
      '1000':(345,   327.5,  10,  520,  440,  200,  500,  180, 80,150,-53, 160,  260,  60 ,  200,  900,   70,  200,  150,  394, 125),
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
        self.label_type.setStyleSheet("color: gray;")
        self.comboBox_type = QtGui.QComboBox(Dialog)
        self.comboBox_type.setGeometry(QtCore.QRect(150, 10, 100, 22))
        self.comboBox_type.setEditable(True)
        #ベルト幅
        self.label_B = QtGui.QLabel('BeltWidth',Dialog)
        self.label_B.setGeometry(QtCore.QRect(30, 38, 100, 22))
        self.label_B.setStyleSheet("color: gray;")
        self.comboBox_B = QtGui.QComboBox(Dialog)
        self.comboBox_B.setGeometry(QtCore.QRect(150, 38, 100, 22))
        #self.comboBox_B.listIndex=11
        
        #機長
        self.label_C = QtGui.QLabel('CenterDistance[mm]',Dialog)
        self.label_C.setGeometry(QtCore.QRect(30, 63, 100, 22))
        self.label_C.setStyleSheet("color: gray;")
        self.le_C = QtGui.QLineEdit(Dialog)
        self.le_C.setGeometry(QtCore.QRect(150, 65, 60, 20))
        self.le_C.setAlignment(QtCore.Qt.AlignCenter)
        #テールプーリ高さ
        self.label_h = QtGui.QLabel('tailPulleyHight[mm]',Dialog)
        self.label_h.setGeometry(QtCore.QRect(30, 93, 100, 22))
        self.label_h.setStyleSheet("color: gray;")
        self.le_h = QtGui.QLineEdit('1000',Dialog)
        self.le_h.setGeometry(QtCore.QRect(150, 93, 60, 20))
        self.le_h.setAlignment(QtCore.Qt.AlignCenter)
        #コンベヤ傾斜角
        self.label_k = QtGui.QLabel('inclinationDegree[degree]',Dialog)
        self.label_k.setGeometry(QtCore.QRect(30, 118, 100, 22))
        self.label_k.setStyleSheet("color: gray;")
        self.le_k = QtGui.QLineEdit('0',Dialog)
        self.le_k.setGeometry(QtCore.QRect(150, 118, 60, 20))
        self.le_k.setAlignment(QtCore.Qt.AlignCenter)
        #作成
        self.pushButton = QtGui.QPushButton('Execute',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(30, 143, 50, 22))
        #更新
        self.pushButton2 = QtGui.QPushButton('Update',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(105, 143, 50, 22))
        #Import
        self.pushButton3 = QtGui.QPushButton('Import',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(175, 143, 50, 22))

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

        #count
        self.pushButton_ct = QtGui.QPushButton('Count',Dialog)
        self.pushButton_ct.setGeometry(QtCore.QRect(30, 405, 100, 23))
        self.le_ct = QtGui.QLineEdit(Dialog)
        self.le_ct.setGeometry(QtCore.QRect(130, 405, 50, 23))
        self.le_ct.setAlignment(QtCore.Qt.AlignCenter)  
        self.le_ct.setText('1')
        
        #質量入力
        self.pushButton_m3 = QtGui.QPushButton('massImput[kg]',Dialog)
        self.pushButton_m3.setGeometry(QtCore.QRect(30, 430, 100, 23))
        self.pushButton_m3.setObjectName("pushButton")  
        self.le_mass = QtGui.QLineEdit(Dialog)
        self.le_mass.setGeometry(QtCore.QRect(130, 430, 50, 23))
        self.le_mass.setAlignment(QtCore.Qt.AlignCenter)  
        self.le_mass.setText('10.0')
        #密度
        self.lbl_gr = QtGui.QLabel('SpecificGravity',Dialog)
        self.lbl_gr.setGeometry(QtCore.QRect(30, 460, 80, 12))
        self.lbl_gr.setStyleSheet("color: gray;")
        self.le_gr = QtGui.QLineEdit(Dialog)
        self.le_gr.setGeometry(QtCore.QRect(130, 455, 50, 23))
        self.le_gr.setAlignment(QtCore.Qt.AlignCenter)  
        self.le_gr.setText('7.85')

        self.comboBox_B.addItems(BeltW)
        self.comboBox_type.addItems(type_data)
        self.le_C.setText('5000')
        QtCore.QObject.connect(self.pushButton_ct, QtCore.SIGNAL("pressed()"), self.countCulc)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.setParts)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.select_objects_by_multiple_labels)
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
        
    def countCulc(self):
        c00 = Gui.Selection.getSelection()
        if c00:
            obj = c00[0]
        label='mass[kg]'
        count=int(self.le_ct.text())
        try:
            obj.addProperty("App::PropertyFloat", "count",label)
            obj.count=count
        except:
            obj.count=count 
    
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
                            try:
                                spreadsheet.set(f"C{row}", obj.Standard)   #standard
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
        global spreadsheet
        selection = Gui.Selection.getSelection()
        if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 parts_group = selected_object
                 for obj in parts_group.Group:
                     if obj.TypeId == "Spreadsheet::Sheet":
                         spreadsheet = obj

        self.comboBox_type.setCurrentText(spreadsheet.getContents('A1'))
        self.comboBox_B.setCurrentText(spreadsheet.getContents('B0'))     
        self.le_C.setText(spreadsheet.getContents('C0'))  
        self.le_h.setText(spreadsheet.getContents('Ht'))
        self.le_k.setText(spreadsheet.getContents('k'))  

    def collect_objects_recursive(self,group, target_labels):
        global Carrier
        global Return
        global takeUpAssy
        global Take_upPulley
        global bendPulley
        global BendPulley
        global Skirt
        global Cover
        global waterReceptacle
        global Belt
        global Scraper
        global Frame
        global Post
        global CPM
        global Self_Aligning_Carrier
        global Self_Aligning_Return
        global MotorPulley
        global carrierArray
        global returnArray
        """グループ以下を再帰的に探索し、ラベルが完全一致するオブジェクトを収集"""
        matched = []
        for obj in getattr(group, "Group", []):
            print(obj.Label)
            if obj.Label=='Carrier':
                Carrier=obj
            elif obj.Label=='Return':
                Return=obj  
            elif obj.Label=='takeUpAssy':
                takeUpAssy=obj 
            elif obj.Label=='Take_upPulley':
                Take_upPulley=obj  
            elif obj.Label=='MotorPulley':
                MotorPulley=obj  
            elif obj.Label=='bendPulley':
                bendPulley=obj 
            elif obj.Label=='BendPulley':
                BendPulley=obj          
            elif obj.Label=='Skirt':
                Skirt=obj
            elif obj.Label=='Cover':
                Cover=obj  
            elif obj.Label=='waterReceptacle':
                waterReceptacle=obj  
            elif obj.Label=='Belt':
                Belt=obj 
            elif obj.Label=='Scraper':
                Scraper=obj   
            elif obj.Label=='Frame':
                Frame=obj               
            elif obj.Label=='Post':
                Post=obj 
            elif obj.Label=='CPM':
                CPM=obj 
            elif obj.Label=='Self_Aligning_Carrier':
                Self_Aligning_Carrier=obj  
            elif obj.Label=='Self_Aligning_Return':
                Self_Aligning_Return=obj  
            elif obj.Label=='Self_Aligning_Return':
                Self_Aligning_Return=obj  
            elif obj.Label=='carrierArray':
                carrierArray=obj             
            elif obj.Label=='returnArray':
                returnArray=obj             
            # 下位フォルダなら再帰的に探索
            if hasattr(obj, "Group"):
                matched.extend(self.collect_objects_recursive(obj, target_labels))
            else:
                # ラベルが完全一致するオブジェクトを追加
                if obj.Label == target_labels:
                    matched.append(obj)
        return matched  
            

    def select_objects_by_multiple_labels(self):
        #print('nnnnnnnnnnnnn')
        """選択したフォルダ以下で、指定した複数ラベル名のオブジェクトを選択"""
        sel = Gui.Selection.getSelection()
        if not sel:
            App.Console.PrintError("まずフォルダを選択してください。\n")
            return     
             
        root = sel[0]
        if not hasattr(root, "Group"):
            App.Console.PrintError("選択されたオブジェクトはフォルダ（Groupなど）ではありません。\n")
            return
             # === 完全一致で探すラベル名を指定 ===
        target_labels =['Carrier', 'Return']   # ← ここを探したいラベル名に変更！
        # === 検索 ===
        matched_objects = self.collect_objects_recursive(root, target_labels)
        #print(matched_objects)
        # === 結果を選択 ===
        Gui.Selection.clearSelection()
        for obj in matched_objects:
            #print(obj)
            Gui.Selection.addSelection(obj)
        #App.Console.PrintMessage(f"ラベルが {target_labels} のいずれかに一致するオブジェクトを {len(matched_objects)} 個選択しました。\n") 
            
        
        #else:
        #   print('error')
        #   return
    def update(self):
        try:
            key=self.comboBox_B.currentText()
            sa=BDim[key]
            L=self.le_C.text()
            Ht=self.le_h.text()
            k=self.le_k.text()
            W0=float(key)+350
            
            spreadsheet.set('B2',L)
            spreadsheet.set('B0',key)
            spreadsheet.set('b1',str(sa[0]))#b1
            spreadsheet.set('b2',str(sa[1]))#b2
            spreadsheet.set('t0',str(sa[2]))#t0
            spreadsheet.set('D0',str(sa[3]))#D0  
            spreadsheet.set('d2',str(sa[5]))#d2
            spreadsheet.set('Ls',str(sa[6]))#Ls
            spreadsheet.set('h0',str(sa[7]))#h0
            spreadsheet.set('h1',str(sa[8]))#h1
            spreadsheet.set('h2',str(sa[9]))#h2
            spreadsheet.set('z',str(sa[10]))#z
            spreadsheet.set('zb',str(sa[11]))#zb
            spreadsheet.set('zs',str(sa[12]))#zs
            spreadsheet.set('za',str(sa[13]))#za
            spreadsheet.set('zr',str(sa[14]))#zr
            spreadsheet.set('vx',str(sa[15]))#vx
            spreadsheet.set('vh',str(sa[16]))#vh
            spreadsheet.set('vh2',str(sa[17]))#vh2
            spreadsheet.set('hsk',str(sa[18]))#hsk
            spreadsheet.set('hsk2',str(sa[19]))#hsk2
            spreadsheet.set('hwa',str(sa[20]))#hwa
            spreadsheet.set('Ht',Ht)#Ht
            spreadsheet.set('k',k)#k
            spreadsheet.set('W0',str(W0))#W0
            
            C0=spreadsheet.getContents('C0') 
            post_c=int((float(C0)-1300)/2500)
            post_x=round((float(C0)-1300)/(post_c+1),2)
            spreadsheet.set('post_c',str(post_c))
            spreadsheet.set('post_x',str(post_x))
            
            Take_upPulley.BeltWidth=spreadsheet.getContents('B0')
            MotorPulley.BeltWidth=spreadsheet.getContents('B0')
            Carrier.BeltWidth=spreadsheet.getContents('B0')
            Self_Aligning_Carrier.BeltWidth=spreadsheet.getContents('B0')
            Return.BeltWidth=spreadsheet.getContents('B0')
            Self_Aligning_Return.BeltWidth=spreadsheet.getContents('B0')
            BendPulley.BeltWidth=spreadsheet.getContents('B0')
            
            g0=7.85
            g=takeUpAssy.Shape.Volume*g0*1000/10**9
            takeUpAssy.mass=g
            
            g0=7.85
            g=round(bendPulley.Shape.Volume*g0*1000/10**9,2) 
            bendPulley.mass=g

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
            Belt.Standard='B='+ key + ',' + 'L='+C0
            

            sa=BeltCv.Carrier_lst[key]
            g=sa[8]
            Carrier.mass=g
            Carrier.count=carrierArray.Count

            
            sa=BeltCv.Return_lst[key]
            g=sa[7]
            Return.mass=g
            Return.count=returnArray.Count
            
            g0=7.85
            g=round(Scraper.Shape.Volume*g0*1000/10**9,2) 
            Scraper.mass=g
            

            g0=7.85
            g=round(Frame.Shape.Volume*g0*1000/10**9,2) 
            Frame.mass=g
            Frame.Standard='B='+key + ',' + 'L='+C0
            
            sa=mtrply_data.pulley_dim[key]
            standard=sa[16]
            
            g=sa[24]
            MotorPulley.mass=g
            
            MotorPulley.Standard=standard
            print('ggggggggggggggggggggggggggg')

            sa=BeltCv.J_Carrier_lst[key]
            g=sa[9]
            Self_Aligning_Carrier.mass=g
            
            sa=BeltCv.J_Return_lst[key]
            g=sa[9]
            Self_Aligning_Return.mass=g
            App.ActiveDocument.recompute()
        except:
            print('error push import')
            return    
    
    def create(self): 
         #W0=self.comboBox_B.currentText()
         if self.comboBox_type.currentText()=='MotorPulley':   
             fname='BeltCv_Assy_m.FCStd' 
         #else:
         #    return    
         base=os.path.dirname(os.path.abspath(__file__))
         joined_path = os.path.join(base,'Belt_data',fname) 
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