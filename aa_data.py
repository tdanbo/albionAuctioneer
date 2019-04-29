def data(cityfromcap, citytocap, catagories, tiers, cities, hourcap, margincaplow, margincaphigh):
    import os
    import json
    import time
    from datetime import datetime
    import pytz
    from operator import itemgetter, attrgetter

    scriptpath = str(os.path.dirname(os.path.realpath(__file__)))
    datapath = str(os.path.join(scriptpath, "dataset"))
    scandatapath = str(os.path.join(scriptpath, "scan"))

    allids = []
    allauctions = []
    
    print(catagories)

    for category in catagories:
        for tier in tiers:
            path = os.path.join(scandatapath,str(category)+"_"+str(tier)+".txt")
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
                                diffdays = (currenttime-datatime).days
                                if diffdays > 0:
                                    pass
                                else:
                                    if difference < int(hourcap):
                                        if i["city"] in cities:
                                            allids.append(i["item_id"])
                                            allauctions.append((i["item_id"],category,i["city"],i["sell_price_min"],i["sell_price_min_date"]))
                                    else:
                                        pass
                            else:
                                pass
            else:
                pass

    completeauctionlist = []
    for itemid in set(allids):
        idauctions = []
        for auction in allauctions:
            if auction[0] == itemid:
                idauctions.append(auction)

        if len(idauctions) > 1: 

            print(idauctions)

            fromdata = sorted(idauctions, key=itemgetter(3))[0]
            todata = sorted(idauctions, key=itemgetter(3))[-1]

            fromcity = fromdata[2]
            fromvalue = fromdata[3]
            fromvaluedata = fromdata[4].replace("T"," ")

            tocity = todata[2]
            tovalue = todata[3]
            tovaluedata = todata[4].replace("T"," ")

            margin = todata[3]-fromdata[3]
            marginp = round(float(margin)/float(todata[3])*100,2)

            # - getting name - #
            categoryfile = os.path.join(scriptpath, "dataset", str(idauctions[0][1])+".txt")
            file = open(categoryfile, "r+")
            lines = file.readlines()
            itemlist = [line.rstrip('\n') for line in lines]

            for item in itemlist:
                if item.split(":")[3] == idauctions[0][0]:
                    itemname = item.split(":")[0]
                    if marginp < float(margincaphigh):
                        if marginp > float(margincaplow):
                            if cityfromcap+" "+citytocap == "any any":
                                completeauctionlist.append((fromcity,fromvalue,tocity,tovalue,margin,marginp,itemname,itemid,tovaluedata,fromvaluedata))
                            elif cityfromcap+" "+citytocap == fromcity+" any":
                                completeauctionlist.append((fromcity,fromvalue,tocity,tovalue,margin,marginp,itemname,itemid,tovaluedata,fromvaluedata))
                            elif cityfromcap+" "+citytocap == "any "+tocity:
                                completeauctionlist.append((fromcity,fromvalue,tocity,tovalue,margin,marginp,itemname,itemid,tovaluedata,fromvaluedata))
                            elif cityfromcap+" "+citytocap == fromcity+" "+tocity:
                                completeauctionlist.append((fromcity,fromvalue,tocity,tovalue,margin,marginp,itemname,itemid,tovaluedata,fromvaluedata))
                            else:
                                pass
                        else:                   
                            pass
                    else:                   
                        pass
                else:
                    pass

    return completeauctionlist
