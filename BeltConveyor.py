import os
import sys
import csv
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui
from PySide import QtUiTools
from PySide import QtCore
from FreeCAD import Base
import FreeCAD, Part, math
from math import pi


buhin=['ベルトコンベヤ',]

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 200)
        Dialog.move(1000, 0)
        #部品
        self.comboBox_buhin = QtGui.QComboBox(Dialog)
        self.comboBox_buhin.setGeometry(QtCore.QRect(80, 11, 130, 20))
        #self.comboBox_buhin.setObjectName("comboBox_2")
        self.label_buhin = QtGui.QLabel('部品',Dialog)
        self.label_buhin.setGeometry(QtCore.QRect(11, 11, 61, 16))
        #self.label_buhin.setObjectName("label_2")
        #部品2
        self.comboBox_buhin2 = QtGui.QComboBox(Dialog)
        self.comboBox_buhin2.setGeometry(QtCore.QRect(80, 36, 130, 20))
        #self.comboBox_buhin2.setObjectName("comboBox_2")
        self.label_buhin2 = QtGui.QLabel('部品2',Dialog)
        self.label_buhin2.setGeometry(QtCore.QRect(11, 36, 61, 16))
        #self.label_buhin2.setObjectName("label_2")
        #質量計算
        self.pushButton_m = QtGui.QPushButton('massCulculation',Dialog)
        self.pushButton_m.setGeometry(QtCore.QRect(80, 61, 100, 23))
        self.pushButton_m.setObjectName("pushButton")  
        
        #質量集計
        self.pushButton_m2 = QtGui.QPushButton('massTally',Dialog)
        self.pushButton_m2.setGeometry(QtCore.QRect(180, 61, 100, 23))
        self.pushButton_m2.setObjectName("pushButton")
        #質量入力
        self.pushButton_m3 = QtGui.QPushButton('massImput[kg]',Dialog)
        self.pushButton_m3.setGeometry(QtCore.QRect(80, 86, 100, 23))
        self.pushButton_m3.setObjectName("pushButton")  
        self.le_mass = QtGui.QLineEdit(Dialog)
        self.le_mass.setGeometry(QtCore.QRect(180, 86, 50, 20))
        self.le_mass.setAlignment(QtCore.Qt.AlignCenter)  
        self.le_mass.setText('10.0')
        #密度
        self.lbl_gr = QtGui.QLabel('SpecificGravity',Dialog)
        self.lbl_gr.setGeometry(QtCore.QRect(80, 111, 80, 12))
        self.le_gr = QtGui.QLineEdit(Dialog)
        self.le_gr.setGeometry(QtCore.QRect(180, 111, 50, 20))
        self.le_gr.setAlignment(QtCore.Qt.AlignCenter)  
        self.le_gr.setText('7.85')
        #実行
        self.pushButton = QtGui.QPushButton('Execution',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(80, 160, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.comboBox_buhin.addItems(buhin)
        self.comboBox_buhin.setCurrentIndex(1)
        self.comboBox_buhin.currentIndexChanged[int].connect(self.onSpec)
        self.comboBox_buhin.setCurrentIndex(0)
        
         #重心計算
        #self.pushButton_cm = QtGui.QPushButton('centerOfMass',Dialog)
        #self.pushButton_cm.setGeometry(QtCore.QRect(80, 135, 100, 23))
        #self.pushButton_cm.setObjectName("pushButton") 

        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton_m, QtCore.SIGNAL("pressed()"), self.massCulc)
        QtCore.QObject.connect(self.pushButton_m2, QtCore.SIGNAL("pressed()"), self.massTally2)
        QtCore.QObject.connect(self.pushButton_m3, QtCore.SIGNAL("pressed()"), self.massImput)
        #QtCore.QObject.connect(self.pushButton_cm, QtCore.SIGNAL("pressed()"), self.centerOfMas)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", 'BeltConveyorWB', None))
        
           
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
            pass

    def massTally2(self):
        #def get_object_mass():
        doc = App.ActiveDocument
        objects = doc.Objects
        mass_list = []
        for obj in objects:
            if Gui.ActiveDocument.getObject(obj.Name).Visibility:
                if obj.isDerivedFrom("Part::Feature"):
                    if hasattr(obj, "mass"):
                        # Add the object's name, count, and mass to the list
                        mass_list.append([obj.Label, 1, obj.mass])
                else:
                     pass
        doc_path = doc.FileName
        csv_filename = os.path.splitext(os.path.basename(doc_path))[0] + "_counts_and_masses.csv"
        csv_path = os.path.join(os.path.dirname(doc_path), csv_filename)
        #print(doc_path)
        with open(csv_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Object Name",'Count', "Mass[kg]"])
            writer.writerows(mass_list) 
    def onSpec(self):
        global buhin
        global pic
        buhin=self.comboBox_buhin.currentText()
        self.comboBox_buhin2.clear()
        self.comboBox_buhin2.show()
            
        if buhin=='ベルトコンベヤ':
            self.comboBox_buhin2.hide()    

    def create(self):
         buhin2=self.comboBox_buhin2.currentText()
         if buhin=='ベルトコンベヤ':
                 import BeltCv
class main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show()


        
