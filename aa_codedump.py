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

