# -*- coding: utf-8 -*-
import os
import sys
import json
import urllib3
import requests
import time
from datetime import datetime, timezone
import pytz

from operator import itemgetter, attrgetter
from bs4 import BeautifulSoup

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

# - config - #
online = False

# - dataset - #
scriptpath = "C:\\Users\\tobia\\Google Drive\\scripts\\albionAuctioneer\\"
dataset = os.path.join(scriptpath,"dataset")
icons = os.path.join(scriptpath,"icons")

# - styles - #

mainstyle = "font-size:10px; background-color:#292929; border: 2px solid #1C1C1C"
darkstyle = "font-size:10px; color: #858585; font-weight: bold;background-color:#1C1C1C; border: 2px solid #111111; text-align: left; padding-left: 10px; padding-right: 10px; height: 20px;"
lightstyle = "font-size:10px; color: #CCCCCC; background-color:#3B3B3B; border: 1px solid #1C1C1C; height: 20px;"
blackstyle = "font-size:15px; color: #1C1C1C; font-weight: bold; height: 20px; border: 2px solid #292929"
darktextstyle = "font-size:10px; background-color:#292929; border: 2px solid #292929;"

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
        self.scanui.clicked.connect(self.scanAuctionHouse)
        self.generateui = QPushButton("generate")
        self.generateui.clicked.connect(self.generate)
        self.generateui.setFixedSize(378,20)

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

    def generate(self):#
        print("generate")
        self.clearLayout()
        self.datagather()

        for self.auction in sorted(self.completeauctionlist, key=itemgetter(5), reverse=True):
            h = 40
            self.auctionlayout = QHBoxLayout()
            self.auctionwidget = QWidget()
            self.auctionwidget.setLayout(self.auctionlayout)

            self.iconlabel = QToolButton()
            self.iconlabel.setFixedSize(h,h)
            print(icons+self.auction[6]+".png")
            icon  = QPixmap(icons+"\\"+self.auction[6]+".png")
            self.iconlabel.setIcon(icon)
            self.iconlabel.setIconSize(QSize(h-2, h-2))

            self.namelabel = QPushButton(str(self.auction[6]))
            self.namelabel.setFixedSize(200,h)
            
            # - button icon - #

            self.fromlabel = QLabel(str(self.auction[0])+"\n"+str(self.auction[7]))
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

            self.datalayout.addWidget(self.auctionwidget)

    def scanAuctionHouse(self):
        # - dataset - #
        self.scanui.setText("SCANNING!")
        scriptpath = "C:\\Users\\tobia\\Google Drive\\scripts\\albionAuctioneer\\"
        dataset = os.path.join(scriptpath,"dataset")

        catagories = ["accessories","armor","artefacts","cityresources","consumables","farmables","furniture","gatherergear","luxurygoods","magic","materials","melee","mounts","offhand","products","ranged","resources","token","tools","trophies"]
        tiers = ["1","2","3","4","5","6","7","8"]

        # - dataset - #
        for catagory in catagories:
            for tier in tiers:
                catagorypath = os.path.join(dataset,catagory+".txt")
                file = open(catagorypath, "r+")
                lines = file.readlines()
                itemlist = [line.rstrip('\n') for line in lines]
                tierlist = []
                for item in itemlist:
                    if item.split(":")[2] == tier:
                        tierlist.append(item.split(":")[3])

                urllist = "%2C".join(tierlist)

                page = "https://www.albion-online-data.com/api/v1/stats/prices/%s" % (urllist)
                page = requests.get(page)

                f = open("C:\\Users\\tobia\\Google Drive\\scripts\\albionAuctioneer\\scan\\"+catagory+"_"+tier+".txt","wb+")
                print(catagory+"_"+tier)
                f.write(page.content)
                f.close()
        self.scanui.setText("last scan "+str(datetime.now(tz=pytz.utc).replace(microsecond=0)))

    def datagather(self):
        # - dataset - #
        catagories = ["accessories","armor","artefacts","cityresources","consumables","farmables","furniture","gatherergear","luxurygoods","magic","materials","melee","mounts","offhand","products","ranged","resources","token","tools","trophies"]
        tiers = ["1","2","3","4","5","6","7","8"]
        cities = ["Caerleon","Lymhurst","Martlock","Bridgewatch","Thetford","Fort Sterling","Black Market"]

        allids = []
        allauctions = []

        for category in catagories:
            for tier in tiers:
                path = "C:\\Users\\tobia\\Google Drive\\scripts\\albionAuctioneer\\scan\\%s_%s.txt" % (category,tier)
                if os.path.isfile(path):
                    if os.stat(path).st_size != 0:
                        file = open(path, "r")
                        datastore = json.load(file)
                        with open(path) as json_file:  
                            data = json.load(json_file)
                            for i in data:
                                if i['sell_price_min_date'] != "0001-01-01T00:00:00":
                                    currenttime = datetime.now(tz=pytz.utc).replace(microsecond=0)
                                    datatime = datetime.strptime(i['sell_price_min_date'], '%Y-%m-%dT%H:%M:%S')
                                    currenttime = currenttime.replace(tzinfo=None)
                                    difference = (currenttime-datatime).seconds/60

                                    if difference < int(self.hourcap.text()):
                                        print(difference)
                                        if i["city"] in cities:
                                            print(i["item_id"])
                                            print(i["city"])
                                            print(i["sell_price_min"])
                                            print(i["sell_price_min_date"])
                                            print("")
                                            allids.append(i["item_id"])
                                            allauctions.append((i["item_id"],category,i["city"],i["sell_price_min"],i["sell_price_min_date"]))
                                    else:
                                        pass
                                else:
                                    pass
                else:
                    pass

        self.completeauctionlist = []
        for itemid in set(allids):
            idauctions = []
            for auction in allauctions:
                if auction[0] == itemid:
                    idauctions.append(auction)

            if len(idauctions) > 1: 

                fromdata = sorted(idauctions, key=itemgetter(3))[0]
                todata = sorted(idauctions, key=itemgetter(3))[-1]

                fromcity = fromdata[2]
                fromvalue = fromdata[3]
                fromvaluedata = fromdata[4].replace("T"," ")

                tocity = todata[2]
                tovalue = todata[3]
                tovaluedata = todata[4].replace("T"," ")

                margin = todata[3]-fromdata[3]
                marginp = round((margin/todata[3])*100,2)


                if marginp > float(self.margincap.text()):
                    pass
                else:
                    self.completeauctionlist.append((fromcity,fromvalue,tocity,tovalue,margin,marginp,itemid,tovaluedata,fromvaluedata))
            else:
                pass

        print(self.completeauctionlist)

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

panel = albionAuctioneer()
panel.show()
sys.exit(app.exec_())

