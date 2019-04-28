# -*- coding: utf-8 -*-
import os
import sys
import urllib3
import requests


from operator import itemgetter, attrgetter
from bs4 import BeautifulSoup

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

# - file imports - #
from aa_scan import scan
from aa_data import data

# - config - #
online = False

# - dataset - #
scriptpath = os.path.dirname(os.path.realpath(__file__))
dataset = os.path.join(scriptpath,"dataset")
icons = os.path.join(scriptpath,"icons")

# - styles - #

mainstyle = "font-size:10px; background-color:#292929; border: 2px solid #1C1C1C"
darkstyle = "font-size:10px; color: #858585; font-weight: bold;background-color:#1C1C1C; border: 2px solid #111111; text-align: left; padding-left: 10px; padding-right: 10px; height: 20px;"
lightstyle = "font-size:10px; color: #CCCCCC; background-color:#3B3B3B; border: 1px solid #1C1C1C; height: 20px;"
blackstyle = "font-size:15px; color: #1C1C1C; font-weight: bold; height: 20px; border: 2px solid #292929"
darktextstyle = "font-size:10px; background-color:#292929; border: 2px solid #292929;"

# - dataset - #

# - styles - #
app = QApplication(sys.argv)

class albionAuctioneer(QWidget):
    def __init__(self):
        super(albionAuctioneer, self).__init__()

        # - layouts - #     
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(5,5,5,5)
        self.mainLayout.setSpacing(0) 

        self.controllayout = QVBoxLayout()
        self.datalayout = QVBoxLayout()

        # - ui loop - #
        self.catagories = ["control","data"]
        self.layouts = [self.controllayout,self.datalayout]
        for w,c,l in zip(self.catagories,range(len(self.catagories)),self.layouts):
            self.catagorylayout = QGridLayout()

            self.catagorybutton = QPushButton(w.upper())
            self.catagorybutton.setObjectName(w)
            self.catagorybutton.setFocusPolicy(Qt.NoFocus)
            self.catagorybutton.setLayoutDirection(Qt.RightToLeft)
            self.catagorybutton.setStyleSheet(darkstyle)

            self.catagoryframe = QFrame()
            self.catagoryframe.setFrameShape(QFrame.StyledPanel)
            self.catagoryframe.setObjectName(w+"_frame")

            self.mainLayout.addWidget(self.catagorybutton)
            self.mainLayout.addWidget(self.catagoryframe)

            self.catagoryframe.setLayout(l)

        self.scanui = QPushButton("scan")
        self.scanui.setFixedSize(100,20)
        self.scanui.clicked.connect(scan)
        self.ccity = QCheckBox("Caerleon")
        self.lcity = QCheckBox("Lymhurst")
        self.mcity = QCheckBox("Martlock")
        self.bcity = QCheckBox("Bridgewatch")
        self.tcity = QCheckBox("Thetford")
        self.fcity = QCheckBox("Fort Sterling")
        self.margincap = QLineEdit("75")
        self.margincap.setAlignment(Qt.AlignCenter)
        self.margincap.setFixedSize(30,20)
        self.hourcap = QLineEdit("15")
        self.hourcap.setAlignment(Qt.AlignCenter)
        self.hourcap.setFixedSize(30,20)
        
        self.generateui = QPushButton("generate")
        self.generateui.clicked.connect(self.generate)
        self.generateui.setFixedSize(378,20)


        self.toplayout = QHBoxLayout()
        self.botlayout = QHBoxLayout()

        self.controllayout.addLayout(self.toplayout)
        self.controllayout.addLayout(self.botlayout)

        [self.botlayout.addWidget(w) for w in [self.ccity,self.lcity,self.mcity,self.bcity,self.tcity,self.fcity,self.margincap,self.hourcap,self.generateui,self.scanui]]

        # - set main layout - #
        self.setLayout(self.mainLayout)
        self.mainLayout.setSizeConstraint(self.mainLayout.SetFixedSize)

        # - set main layout - #
        self.setWindowTitle('albionAuctioneer v1.0')
        self.styles()

    # - Function to set UI styles - #
    def styles(self):
        self.setStyleSheet(mainstyle)
        [w.setStyleSheet(lightstyle) for w in [self.margincap,self.hourcap,self.generateui,self.scanui]]
        [w.setStyleSheet(darktextstyle) for w in [self.ccity,self.lcity,self.mcity,self.bcity,self.tcity,self.fcity]]

    # - Function for clearing the browser layout                           - #
    def clearLayout(self):
        layout = self.datalayout
        for i in reversed(range(layout.count())):
            layout.takeAt(i).widget().deleteLater()

    def generate(self):
        catagories = ["accessories","armor","artefacts","cityresources","consumables","farmables","furniture","gatherergear","luxurygoods","magic","materials","melee","mounts","offhand","products","ranged","resources","token","tools","trophies"]
        tiers = ["1","2","3","4","5","6","7","8"]
        cities = ["Caerleon","Lymhurst","Martlock","Bridgewatch","Thetford","Fort Sterling","Black Market"]
        hourcap = self.hourcap.text()
        margincap = self.margincap.text()
        
        data(catagories, tiers, cities, hourcap, margincap)

panel = albionAuctioneer()
panel.show()
sys.exit(app.exec_())

