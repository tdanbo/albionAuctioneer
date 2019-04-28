def scan():
    import os
    import requests
    from pathlib import Path

    catagories = ["accessories","armor","artefacts","cityresources","consumables","farmables","furniture","gatherergear","luxurygoods","magic","materials","melee","mounts","offhand","products","ranged","resources","token","tools","trophies"]
    tiers = ["1","2","3","4","5","6","7","8"]

    scriptpath = os.path.dirname(os.path.realpath(__file__))
    datapath = os.path.join(scriptpath, "dataset")
    scandatapath = os.path.join(scriptpath, "scan")

    print(datapath)

    # - dataset - #
    for catagory in catagories:
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

            f = open(scanfile,"wb+")
            f.write(page.content)
            f.close()

            print("scan complete - "+catagory+" tier "+tier)

    print("SCAN COMPLETE!")