# -*- coding: utf-8 -*-
import os
import sys
import urllib3
import requests

from operator import itemgetter, attrgetter

try:
    from PySide2.QtWidgets import *
    from PySide2.QtGui import *
    from PySide2.QtCore import *
except:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *

# - file imports - #
from aa_scan import scan
from aa_data import data

# - config - #
online = False

# - dataset - #
scriptpath = os.path.dirname(os.path.realpath(__file__))
dataset = os.path.join(scriptpath,"dataset")
scandatapath = os.path.join(scriptpath, "scan")
icons = os.path.join(scriptpath,"icons")

app = QApplication(sys.argv)

class albionAuctioneer(QWidget):
    def __init__(self):
        super(albionAuctioneer, self).__init__()
        # - main ui - #

        # - default lists - #
        defaultcity = ["Caerleon","Lymhurst","Martlock","Bridgewatch","Thetford","Fort Sterling","Black Market"]
        defaultcatagory = ["accessories","armor","artefacts","cityresources","consumables","farmables","furniture","gatherergear","luxurygoods","magic","materials","melee","mounts","offhand","products","ranged","resources","token","tools","trophies"]
        self.catagorylist = []

        # - layouts - #     
        self.mainLayout = QVBoxLayout()
        self.categorieslayout = QGridLayout()
        self.controllayout = QVBoxLayout()
        self.datalayout = QFormLayout()
        self.toplayout = QGridLayout()
        self.botlayout = QHBoxLayout()

        # - widgets - #
        self.catauibutton = QPushButton("CATEGORIES")
        self.catauiframe = QFrame()
        self.ctrluibutton = QPushButton("CONTROL")
        self.ctrluiframe = QFrame()
        self.datauibutton = QPushButton("DATA")
        self.datascrollarea = QScrollArea()
        self.datascrollwidget = QWidget()
        self.tiercaplabel = QLabel("lowest tier limit ")
        self.tiercap = QLineEdit("T4")
        self.margincaplabel = QLabel("low/high margin limit ")
        self.margincaplow = QLineEdit("0")      
        self.margincap = QLineEdit("100")
        self.hourcaplabel = QLabel("auction age limit (mins) ")
        self.hourcap = QLineEdit("15")
        self.generateui = QPushButton("load")
        self.cityfromui = QComboBox()
        self.citylabel = QPushButton(">")
        self.citytoui = QComboBox()
        self.selectcat = QPushButton("")
        self.selectcat.setObjectName("all")
        self.scanui = QPushButton("scan")

        # - styles - #
        self.catauibutton.setLayoutDirection(Qt.RightToLeft)
        self.ctrluibutton.setLayoutDirection(Qt.RightToLeft)
        self.datauibutton.setLayoutDirection(Qt.RightToLeft)
        self.catauiframe.setFrameShape(QFrame.StyledPanel)
        self.ctrluiframe.setFrameShape(QFrame.StyledPanel)
        self.mainLayout.setContentsMargins(5,5,5,5)
        self.mainLayout.setSpacing(0)
        self.datascrollarea.setWidgetResizable(True) 
        self.datascrollarea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.datascrollarea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tiercap.setFixedSize(30,20)
        self.tiercap.setAlignment(Qt.AlignCenter) 
        self.margincaplow.setAlignment(Qt.AlignCenter)
        self.margincaplow.setFixedSize(30,20)
        self.margincap.setAlignment(Qt.AlignCenter)
        self.margincap.setFixedSize(30,20)
        self.hourcap.setAlignment(Qt.AlignCenter)
        self.hourcap.setFixedSize(30,20)
        self.generateui.setFixedSize(50,20)
        self.cityfromui.setFixedSize(180,20)
        self.citylabel.setFixedSize(20,20)
        self.citytoui.setFixedSize(180,20)
        self.selectcat.setFixedSize(50,20)
        self.scanui.setFixedSize(50,20)

        # - assignments - #
        self.mainLayout.addWidget(self.catauibutton)
        self.mainLayout.addWidget(self.catauiframe)  
        self.mainLayout.addWidget(self.ctrluibutton)
        self.mainLayout.addWidget(self.ctrluiframe)  
        self.mainLayout.addWidget(self.datauibutton)
        self.mainLayout.addWidget(self.datascrollarea)  
        self.catauiframe.setLayout(self.categorieslayout)
        self.ctrluiframe.setLayout(self.controllayout)
        self.datascrollarea.setWidget(self.datascrollwidget)
        self.datascrollwidget.setLayout(self.datalayout)
        self.setLayout(self.mainLayout)
        self.controllayout.addLayout(self.toplayout)
        self.controllayout.addLayout(self.botlayout)
        self.categorieslayout.addWidget(self.selectcat,0,10)
        self.categorieslayout.addWidget(self.scanui,1,10)
        self.cityfromui.addItem("any")
        self.cityfromui.addItems(defaultcity)
        self.citytoui.addItem("any")
        self.citytoui.addItems(defaultcity)
        [self.botlayout.addWidget(w) for w in [self.cityfromui,self.citylabel,self.citytoui,self.tiercaplabel, self.tiercap, self.margincaplabel, self.margincaplow,self.margincap, self.hourcaplabel, self.hourcap,self.generateui]]

        for cat,c in zip(defaultcatagory,range(len(defaultcatagory))):
            self.checkbox = QCheckBox(cat)
            self.checkbox.stateChanged.connect(self.category)
            if c < 10:
                self.categorieslayout.addWidget(self.checkbox,0,c)
            else:
                self.categorieslayout.addWidget(self.checkbox,1,(c % 10))
            self.styles()

        # - signals - #
        self.generateui.clicked.connect(self.generate)
        self.cityfromui.currentIndexChanged.connect(self.generate)
        self.citylabel.clicked.connect(self.cityswap)
        self.citytoui.currentIndexChanged.connect(self.generate)
        self.selectcat.clicked.connect(self.catagoryswap)
        self.scanui.clicked.connect(self.runscan)

        # - setup functions - #
        self.timestamp()
        self.styles()

    # - Function to set UI styles - #
    def styles(self):
        bgcolor = "#292929"
        bgcolorlight = "#3B3B3B"
        bgcolordark = "#1C1C1C"

        fontcolorlight = "#CCCCCC"
        fontcolordark = "#858585"
        fontsize = "10px"

        bordercolor = "#111111"

        self.main = "background-color:%s;" % (bgcolor)
        self.text = "font-size:%s; color: %s; background-color:%s; border: 1px solid %s;" % (fontsize, fontcolorlight, bgcolor, bgcolor)
        self.darktext = "font-size:%s; color: %s; background-color:%s; border: 1px solid %s;" % (fontsize, fontcolordark, bgcolor, bgcolor)
        self.frames = "font-size:%s; color: %s; background-color:%s; border: 1px solid %s;" % (fontsize, fontcolorlight, bgcolor, bordercolor)
        self.widgets = "font-size:%s; color: %s; background-color: %s; border: 1px solid %s;" % (fontsize,fontcolorlight,bgcolorlight,bordercolor)
        self.catagorywidget = "font-size:%s; font-weight: bold; color: %s; background-color: %s; border: 1px solid %s; text-align: left; padding-left: 10px; padding-right: 10px; height: 20px;" % (fontsize,fontcolordark,bgcolordark,bordercolor) 

        self.setStyleSheet(self.main)
        self.checkbox.setStyleSheet(self.darktext)
        [w.setStyleSheet(self.frames) for w in [self.catauiframe,self.ctrluiframe,self.datascrollarea]]
        [w.setStyleSheet(self.catagorywidget) for w in [self.catauibutton,self.ctrluibutton,self.datauibutton]]
        [w.setStyleSheet(self.text) for w in [self.tiercaplabel,self.margincaplabel,self.hourcaplabel]]
        [w.setStyleSheet(self.widgets) for w in [self.cityfromui,self.citylabel,self.citytoui,self.tiercap, self.margincaplow,self.margincap,self.hourcap,self.generateui,self.scanui,self.selectcat]]


    # - Function for clearing the browser layout                           - #
    def clearLayout(self):
        layout = self.datalayout
        for i in reversed(range(layout.count())):
            layout.takeAt(i).widget().deleteLater()

    # - set main layout - #
    def timestamp(self):
        timestampfile = os.path.join(scandatapath,"timestamp.txt")
        if os.path.isfile(timestampfile):
            timestamp = open(timestampfile,"r")  
            self.setWindowTitle('albionAuctioneer v1.4 - '+timestamp.read())
            timestamp.close()
        else:
            self.setWindowTitle('albionAuctioneer v1.4')

    def category(self):
        print("WORKING")
        self.catagorylist = []
        layout = self.categorieslayout
        widgets = (layout.itemAt(i).widget() for i in range(layout.count())) 
        for widget in widgets:
            if isinstance(widget, QCheckBox):
                if widget.isChecked():
                    self.catagorylist.append(widget.text())
                    widget.setStyleSheet(self.text)
                else:
                    print("style")
                    widget.setStyleSheet(self.darktext)

        if "scan" in self.catagorylist:
            self.catagorylist.remove("scan")
        if "select" in self.catagorylist:
            self.catagorylist.remove("select")

        print(self.catagorylist)

        return self.catagorylist

    def catagoryswap(self):
        state = self.sender().objectName()
        layout = self.categorieslayout
        widgets = (layout.itemAt(i).widget() for i in range(layout.count())) 
        for widget in widgets:
            if isinstance(widget, QCheckBox):
                if state == "all":
                    widget.setChecked(True)
                    self.sender().setObjectName("none")
                else:
                    widget.setChecked(False)
                    self.sender().setObjectName("all")

    def cityswap(self):
        f = self.cityfromui.currentText()
        t = self.citytoui.currentText()
        self.cityfromui.setCurrentIndex(self.cityfromui.findText(t))
        self.citytoui.setCurrentIndex(self.cityfromui.findText(f))

    def runscan(self):
        catagorylist = self.catagorylist
        currenttime = scan(catagorylist)
        print(currenttime)
        self.setWindowTitle('albionAuctioneer v1.4 - '+currenttime)

    def copyname(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.sender().text())

    def generate(self):
        catagories = self.catagorylist
        cities = ["Caerleon","Lymhurst","Martlock","Bridgewatch","Thetford","Fort Sterling","Black Market"]

        # - tier list - #
        tier = self.tiercap.text()
        tiers = []

        for tier in range(int(tier[1]), 9):
            tiers.append(tier)

        # - #

        hourcap = self.hourcap.text()
        margincaplow = self.margincaplow.text()
        margincaphigh = self.margincap.text()
        cityfromcap = self.cityfromui.currentText()
        citytocap = self.citytoui.currentText()

        completeauctionlist = data(cityfromcap, citytocap, catagories, tiers, cities, hourcap, margincaplow, margincaphigh)

        print("generate")
        self.clearLayout()

        for self.auction,c in zip(sorted(completeauctionlist, key=itemgetter(5), reverse=True),range(len(completeauctionlist))):
            h = 40
            self.auctionlayout = QHBoxLayout()
            self.auctionwidget = QWidget()
            self.auctionwidget.setLayout(self.auctionlayout)

            self.iconlabel = QToolButton()
            self.iconlabel.setFixedSize(h,h)
            icon  = QPixmap(icons+"\\"+self.auction[7]+".png")
            self.iconlabel.setIcon(QIcon(icon))
            self.iconlabel.setIconSize(QSize(h-2, h-2))

            self.namelabel = QToolButton()
            self.namelabel.setText(str(self.auction[6]))
            self.namelabel.clicked.connect(self.copyname)
            self.namelabel.setFixedSize(200,h)
            
            # - button icon - #

            self.fromlabel = QLabel(str(self.auction[0])+"\n"+str(self.auction[8]))
            self.fromlabel.setFixedSize(150,h)
            self.fromlabel.setAlignment(Qt.AlignCenter)

            self.fromvalue = QLabel(str(self.auction[1]))
            self.fromvalue.setFixedSize(50,h)
            self.fromvalue.setAlignment(Qt.AlignCenter)

            self.travelicon = QLabel(">")
            self.travelicon.setAlignment(Qt.AlignCenter)
            self.travelicon.setFixedSize(25,h)

            self.tovalue = QLabel(str(self.auction[3]))
            self.tovalue.setFixedSize(50,h)
            self.tovalue.setAlignment(Qt.AlignCenter)

            self.tolabel = QLabel(str(self.auction[2])+"\n"+str(self.auction[8]))
            self.tolabel.setFixedSize(150,h)
            self.tolabel.setAlignment(Qt.AlignCenter)

            self.marginlabel = QLabel(str(self.auction[4]))
            self.marginlabel.setFixedSize(50,h)
            self.marginlabel.setAlignment(Qt.AlignCenter)

            self.marginplabel = QLabel(str(self.auction[5])+" %")
            self.marginplabel.setFixedSize(50,h)
            self.marginplabel.setAlignment(Qt.AlignCenter)

            widgets = [self.iconlabel,self.namelabel,self.fromlabel,self.fromvalue,self.travelicon,self.tovalue,self.tolabel,self.marginlabel,self.marginplabel]

            [self.auctionlayout.addWidget(w) for w in widgets]
            [w.setStyleSheet(self.widgets) for w in widgets]

            self.travelicon.setStyleSheet(self.darktext)

            self.datalayout.addRow(self.auctionwidget)

panel = albionAuctioneer()
panel.show()
sys.exit(app.exec_())