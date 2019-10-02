# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lab1.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib import pyplot
import cv2
import numpy as np
from PIL import Image
import os

HPF = ((1, 1, 1),
       (1, 1, 1),
       (1, 1, 1))


class Ui_MainWindow(QtWidgets.QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1366, 768)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setMinimumSize(QtCore.QSize(300, 380))
        self.scrollArea.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 663, 113))
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_3)
        self.gridLayout.setObjectName("gridLayout")
        self.origin_image_3 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.origin_image_3.setObjectName("origin_image_3")
        self.gridLayout.addWidget(self.origin_image_3, 1, 0)
        self.Change = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
        self.Change.setObjectName("Change")
        self.gridLayout.addWidget(self.Change, 2, 1)
        self.changed_image_3 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.changed_image_3.setObjectName("changed_image_3")
        self.gridLayout.addWidget(self.changed_image_3, 1, 1)
        self.filtering_image_3 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.filtering_image_3.setObjectName("filtering_image_3")
        self.gridLayout.addWidget(self.filtering_image_3, 1, 2)
        self.Save = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
        self.Save.setObjectName("Save")
        self.gridLayout.addWidget(self.Save, 3, 0)
        self.Open = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
        self.Open.setObjectName("Open")
        self.gridLayout.addWidget(self.Open, 2, 0)
        self.show_hist = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
        self.show_hist.setObjectName("pushButton")
        self.gridLayout.addWidget(self.show_hist, 3, 1)
        self.label = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 4, 0)
        self.lineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_3)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 4, 0)
        self.label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 5, 0)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_3)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 5, 0)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_3)
        self.verticalLayout.addWidget(self.scrollArea)
        MainWindow.setCentralWidget(self.centralwidget)
        self.Open.clicked.connect(self.show_dialog)
        self.Save.clicked.connect(self.filt_image)
        self.Change.clicked.connect(self.change_image)
        self.show_hist.clicked.connect(self.make_and_show_hist)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def filt_image(self):
        a = Image.open(self.image_file[0])        
        final_image = Image.new("RGB", (a.width-2, a.height-2))
        for i in range(1, a.width-2):
            for j in range(1, a.height-2):
                r = b = g = 0
                for k in range(-1, 2):
                    for l in range(-1, 2):
                        r += round(a.getpixel((i+k,j+l))[0] * HPF[k+1][l+1]/9)
                        g += round(a.getpixel((i+k,j+l))[1] * HPF[k+1][l+1]/9)
                        b += round(a.getpixel((i+k,j+l))[2] * HPF[k+1][l+1]/9)
                final_image.putpixel((i,j), (abs(r), abs(g), abs(b)))
        final_image.save("filtered_image.jpg")
        final_image.show()
        
    
    def change_image(self): 
        a = Image.open(self.image_file[0])
        c = float(self.lineEdit.text())
        y = float(self.lineEdit_2.text())
        for i in range(a.width):
            for j in range(a.height):
                a.putpixel((i,j), tuple([round(c * (a.getpixel((i,j))[k]/255) ** (1/y)*255)  for k in range(3)]))  
       
        a.save('changed.jpg')
        pixmap = QtGui.QPixmap('changed.jpg')
        self.changed_image_3.setPixmap(pixmap)
        self.changed_image_3.resize(pixmap.width(), pixmap.height())
        self.resize(pixmap.width(), pixmap.height())
        
        
    def show_dialog(self):
        self.image_file = QtWidgets.QFileDialog.getOpenFileName(self, str("Open Image"), "/home/Pictures/",
                                                                      str("Image Files (*.png *.jpg *.bmp)"))
        file = ''.join(self.image_file[0])
        pixmap = QtGui.QPixmap(file)
        self.origin_image_3.setPixmap(pixmap)
        self.origin_image_3.resize(pixmap.width(), pixmap.height())
        self.resize(pixmap.width(), pixmap.height())

    def make_and_show_hist(self):
        pyplot.subplot(1,3,1)
        pyplot.bar(range(256), self.take_counts(Image.open(self.image_file[0])), width=1, edgecolor='red')
        pyplot.subplot(1,3,2)
        pyplot.bar(range(256), self.take_counts(Image.open('changed.jpg')), width=1, edgecolor='blue')
        pyplot.subplot(1,3,3)
        pyplot.bar(range(256), self.take_counts(Image.open('filtered_image.jpg')), width=1, edgecolor='green')
        
        pyplot.show()
        
    def take_counts(self, img):
        b = img.load()
        tmp = []
        for j in range(img.height):
            for i in range(img.width):
                tmp.append(int(b[i,j][0]*0.2126+b[i,j][1]*0.7152+b[i, j][2]*0.0722))              
        counts=[tmp.count(i) for i in range(0, 256)]
        return counts
    
    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.origin_image_3.setText(_translate("MainWindow", "TextLabel"))
        self.Change.setText(_translate("MainWindow", "Преобразовать"))
        self.changed_image_3.setText(_translate("MainWindow", "TextLabel"))
        self.Save.setText(_translate("MainWindow", "Фильтрация"))
        self.Open.setText(_translate("MainWindow", "Открыть изображение"))
        self.show_hist.setText(_translate("MainWindow", "Показать гистограммы"))
        self.label.setText(_translate("MainWindow", "с"))
        self.label_2.setText(_translate("MainWindow", "у"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
