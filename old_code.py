# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from pathlib import Path
import os
import re


'''GUI CLASS'''


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(813, 605)
        MainWindow.setMouseTracking(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(120, 120, 256, 271))
        self.listWidget.setObjectName("listWidget")
        self.treeWidget = QtWidgets.QTreeWidget(self.centralwidget)
        self.treeWidget.setGeometry(QtCore.QRect(460, 170, 256, 192))
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "1")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(350, 40, 47, 13))
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 813, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", f"{movies}"))
        self.label.adjustSize()
    


def is_tv_show(parent_dir):  ###Cheks if video file is in a fodler containing a whole season of a show
    tvShowRegex = re.compile(r'\.S\d\d\.')
    mo = tvShowRegex.search(str(parent_dir))
    if mo != None:
        return True

def is_single_episode(parent_dir):
    tvEpisodeRegex = re.compile(r'\.S\d\dE\d\d\.')
    mo = tvEpisodeRegex.search(str(parent_dir))
    if mo != None:
        return True



video_files = {}

'''Adds all .mkv and .mp4 files from pobrane folder and child folders into a directory with Path and size values'''

pobrane = Path('D:\Pobrane')

for directory_string in os.listdir(pobrane):      ###pobrane folder
    directory_path = pobrane/directory_string
    if directory_path.is_file():
        if directory_path.suffix == '.mkv' or directory_path.suffix == '.mp4':
            video_files[directory_string]= (directory_path,os.path.getsize(directory_path))
    elif directory_path.is_dir():
        for directory2_string in os.listdir(directory_path):          #child folders
            directory2_path = directory_path/directory2_string
            if directory2_path.is_file():
                if directory2_path.suffix == '.mkv' or directory2_path.suffix == '.mp4' or directory2_path.suffix == '.avi':
                    video_files[directory2_string]= (directory2_path,os.path.getsize(directory2_path))
            elif directory2_path.is_dir(): 
                for directory3_string in os.listdir(directory2_path):
                    directory3_path = directory2_path/directory3_string      #child child folders
                    if directory3_path.is_file():
                        if directory3_path.suffix == '.mkv' or directory3_path.suffix == '.mp4':
                            video_files[directory3_string]= (directory3_path,os.path.getsize(directory3_path))
            
exclusion_list =['WEBRip','x265-RARBG','AMZN','DDP5','Atmos','x264-NOGRP','x264-CM','WEB-DL','BluRay','H264','AAC-RARBG','264-NTb','1','x264-usury','blueray','DSNP','HMAX','x264-NTb','Repack','264-CM','x264-NTb[rartv]','0','DD2','h264-plzproper']   
                
'''Separates tv shows and movies into two different dictionaries and groups the tv show episondes togheter(pretty messy; interacting with it not reccomended)'''
tv_shows = {}
'''
Structure:
tv_shows = {tvshowseasonfolder:{filename:(windowsPath(absolutepath),sizeinbytes),...},...}
                /\                 /\              /\                   /\
                key             keyofvalue      value1ofvalue        value2ofvalue
                               |_____________________________________________________|  
                                                        value
'''                                 

movies = {}
'''
Structure:
movies = {filename:(windowsPath(absolutepath),sizeinbytes),...}
            /\          /\                      /\
            key         value1                  value2
'''
for key in video_files.keys():
   
    if is_tv_show(video_files[key][0].parent.absolute()) == True:
        try:
            tv_shows[str(video_files[key][0].parent.absolute())].update({key:video_files[key]})
        except:
            tv_shows[str(video_files[key][0].parent.absolute())] = {}
            tv_shows[str(video_files[key][0].parent.absolute())].update({key:video_files[key]})
    elif is_single_episode(video_files[key][0].parent.absolute()) == True:
        tv_shows.update({key:video_files[key]})
    else:
        movies.update({key:video_files[key]})



import sys
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec_())
