def scan(catagorylist):
    import os
    import requests
    from pathlib import Path
    from datetime import datetime, timezone

    print(catagorylist)
    tiers = ["1","2","3","4","5","6","7","8"]

    scriptpath = os.path.dirname(os.path.realpath(__file__))
    datapath = os.path.join(scriptpath, "dataset")
    scandatapath = os.path.join(scriptpath, "scan")

    print(datapath)

    # - dataset - #

    for catagory in catagorylist:
        for tier in tiers:
            categoryfile = os.path.join(scriptpath, "dataset", catagory+".txt")
            file = open(categoryfile, "r+")
            lines = file.readlines()
            itemlist = [line.rstrip('\n') for line in lines]
            tierlist = []
            for item in itemlist:
                if item.split(":")[2] == tier:
                    tierlist.append(item.split(":")[3])

            urllist = "%2C".join(tierlist)

            page = "https://www.albion-online-data.com/api/v1/stats/prices/%s" % (urllist)
            page = requests.get(page)

            scanfile = os.path.join(scriptpath, "scan", catagory+"_"+tier+".txt")
            if page.status_code == requests.codes.ok:
                f = open(scanfile,"wb+")
                f.write(page.content)
            else:
                f = open(scanfile,"w")              
                f.write("")            
            f.close()

            print("scan complete - "+catagory+" tier "+tier)
            print("code "+str(page.status_code))

    currenttime = str(datetime.now().replace(microsecond=0))
    timestampfile = os.path.join(scriptpath, "scan", "timestamp.txt")
    t = open(timestampfile,"w")
    t.write(currenttime)
    t.close()

    print("SCAN COMPLETE!")
    return currenttime
