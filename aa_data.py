def data(catagories, tiers, cities, hourcap, margincap):
    import os
    import json
    import time
    from datetime import datetime, timezone
    import pytz

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

                                if difference < int(hourcap):
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

    completeauctionlist = []
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


            if marginp > float(margincap):
                pass
            else:
                completeauctionlist.append((fromcity,fromvalue,tocity,tovalue,margin,marginp,itemid,tovaluedata,fromvaluedata))
        else:
            pass

    return completeauctionlist