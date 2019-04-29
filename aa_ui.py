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

# - styles - #

mainstyle = "font-size:10px; background-color:#292929; border: 2px solid #1C1C1C"
mainstylegrey = "font-size:10px; background-color:#292929; border: 2px solid #292929"
darkstyle = "font-size:10px; color: #858585; font-weight: bold;background-color:#1C1C1C; border: 2px solid #111111; text-align: left; padding-left: 10px; padding-right: 10px; height: 20px;"
lightstyle = "font-size:10px; color: #CCCCCC; background-color:#3B3B3B; border: 1px solid #1C1C1C; height: 20px;"
blackstyle = "font-size:15px; color: #1C1C1C; font-weight: bold; height: 20px; border: 2px solid #292929"
darktextstyle = "font-size:10px; background-color:#292929; border: 2px solid #292929;"
lighttextstyle = "font-size:10px; color: #CCCCCC; background-color:#292929; border: 2px solid #292929;"

# - dataset - #

# - styles - #
app = QApplication(sys.argv)

class albionAuctioneer(QWidget):
    def __init__(self):
        super(albionAuctioneer, self).__init__()
        # - selected catagories - #
        self.catagorylist = []

        # - layouts - #     
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(5,5,5,5)
        self.mainLayout.setSpacing(0) 

        self.categorieslayout = QGridLayout()
        self.controllayout = QVBoxLayout()
        self.datalayout = QFormLayout()

        # - ui loop - #
        self.catagories = ["categories","control","data"]
        self.layouts = [self.categorieslayout,self.controllayout,self.datalayout]
        for w,c,l in zip(self.catagories,range(len(self.catagories)),self.layouts):
            self.catagorylayout = QGridLayout()

            self.catagorybutton = QPushButton(w.upper())
            self.catagorybutton.setObjectName(w)
            self.catagorybutton.setFocusPolicy(Qt.NoFocus)
            self.catagorybutton.setLayoutDirection(Qt.RightToLeft)
            self.catagorybutton.setStyleSheet(darkstyle)

            if w == "data":
                self.catagoryframe = QScrollArea()
                self.catagoryframe.setObjectName(w+"_frame")
                self.catagoryframe.setWidgetResizable(True)
                self.scrollwidget = QWidget()
                self.catagoryframe.setWidgetResizable(True)
                self.catagoryframe.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
                self.catagoryframe.setWidget(self.scrollwidget)
                self.scrollwidget.setLayout(l)
            else:
                self.catagoryframe = QFrame()
                self.catagoryframe.setFrameShape(QFrame.StyledPanel)
                self.catagoryframe.setObjectName(w+"_frame")
                self.catagoryframe.setLayout(l)

            self.mainLayout.addWidget(self.catagorybutton)
            self.mainLayout.addWidget(self.catagoryframe)               

        self.scanui = QPushButton("scan")
        self.scanui.setFixedSize(100,20)
        self.scanui.clicked.connect(self.runscan)

        self.tiercaplabel = QLabel("lowest tier limit ")
        self.tiercap = QLineEdit("T4")
        self.tiercap.setFixedSize(30,20)
        self.tiercap.setAlignment(Qt.AlignCenter)        
        self.margincaplabel = QLabel("low/high margin limit ")
        self.margincaplow = QLineEdit("0")
        self.margincaplow.setAlignment(Qt.AlignCenter)
        self.margincaplow.setFixedSize(30,20)
        self.margincap = QLineEdit("100")
        self.margincap.setAlignment(Qt.AlignCenter)
        self.margincap.setFixedSize(30,20)
        self.hourcaplabel = QLabel("auction age limit (mins) ")
        self.hourcap = QLineEdit("15")
        self.hourcap.setAlignment(Qt.AlignCenter)
        self.hourcap.setFixedSize(30,20)
        
        self.generateui = QPushButton("read scan data")
        self.generateui.clicked.connect(self.generate)
        self.generateui.setFixedSize(100,20)

        citylist = ["any","Caerleon","Lymhurst","Martlock","Bridgewatch","Thetford","Fort Sterling","Black Market"]

        self.cityfromui = QComboBox()
        self.cityfromui.setFixedSize(100,20)
        self.cityfromui.currentIndexChanged.connect(self.generate)
        self.citylabel = QLabel(">") 
        self.citytoui = QComboBox()
        self.citytoui.currentIndexChanged.connect(self.generate)
        self.citytoui.setFixedSize(100,20)
        self.cityfromui.addItems(citylist)
        self.citytoui.addItems(citylist)


        self.toplayout = QGridLayout()
        self.botlayout = QHBoxLayout()

        self.controllayout.addLayout(self.toplayout)
        self.controllayout.addLayout(self.botlayout)

        catagoriesone = ["accessories","armor","artefacts","cityresources","consumables","farmables","furniture","gatherergear","luxurygoods","magic"]
        catagoriestwo = ["materials","melee","mounts","offhand","products","ranged","resources","token","tools","trophies"]

        for cat,c in zip(catagoriesone,range(len(catagoriesone))):
            self.checkbox = QCheckBox(cat)
            self.checkbox.setStyleSheet(darktextstyle)
            self.checkbox.setObjectName(cat)
            self.checkbox.stateChanged.connect(self.category)
            self.categorieslayout.addWidget(self.checkbox,0,c)
        for cat,c in zip(catagoriestwo,range(len(catagoriestwo))):
            self.checkbox = QCheckBox(cat)
            self.checkbox.setStyleSheet(darktextstyle)
            self.checkbox.setObjectName(cat)
            self.checkbox.stateChanged.connect(self.category)
            self.categorieslayout.addWidget(self.checkbox,1,c)

        [self.botlayout.addWidget(w) for w in [self.cityfromui,self.citylabel,self.citytoui,self.tiercaplabel, self.tiercap, self.margincaplabel, self.margincaplow,self.margincap, self.hourcaplabel, self.hourcap,self.generateui,self.scanui]]

        # - set main layout - #
        self.setLayout(self.mainLayout)

        # - set main layout - #
        timestampfile = os.path.join(scandatapath,"timestamp.txt")
        if os.path.isfile(timestampfile):
            timestamp = open(timestampfile,"r")  
            self.setWindowTitle('albionAuctioneer v1.0 - scanned - '+timestamp.read())
            timestamp.close()
        else:
            self.setWindowTitle('albionAuctioneer v1.2')

        self.styles()

    # - Function to set UI styles - #
    def styles(self):
        self.setStyleSheet(mainstyle)
        self.scrollwidget.setStyleSheet(mainstylegrey)
        self.citylabel.setStyleSheet(darktextstyle)
        [w.setStyleSheet(lightstyle) for w in [self.cityfromui,self.citytoui,self.tiercap, self.margincaplow,self.margincap,self.hourcap,self.generateui,self.scanui]]
        [w.setStyleSheet(lighttextstyle) for w in [self.tiercaplabel,self.margincaplabel,self.hourcaplabel]]

    # - Function for clearing the browser layout                           - #
    def clearLayout(self):
        layout = self.datalayout
        for i in reversed(range(layout.count())):
            layout.takeAt(i).widget().deleteLater()

    def category(self):
        print("WORKING")
        self.catagorylist = []
        layout = self.categorieslayout
        widgets = (layout.itemAt(i).widget() for i in range(layout.count())) 
        for widget in widgets:
            if isinstance(widget, QCheckBox):
                if widget.isChecked():
                    self.catagorylist.append(widget.text())
                    widget.setStyleSheet(lighttextstyle)
                else:
                    widget.setStyleSheet(darktextstyle)

        return self.catagorylist

    def runscan(self):
        catagorylist = self.catagorylist
        currenttime = scan(catagorylist)
        print(currenttime)
        self.setWindowTitle('albionAuctioneer v1.0 - scanned - '+currenttime)

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
            self.auctionwidget.setStyleSheet(mainstyle)
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
            [w.setStyleSheet(lightstyle) for w in widgets]

            self.travelicon.setStyleSheet(blackstyle)

            self.datalayout.addRow(self.auctionwidget)

            #value = (h+15)*(c+1)
            #print(value)

            #if c <= 10:
            #    self.catagoryframe.setFixedHeight(value)
            #else:
            #    pass
panel = albionAuctioneer()
panel.show()
sys.exit(app.exec_())
