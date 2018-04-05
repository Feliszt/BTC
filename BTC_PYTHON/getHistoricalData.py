#!/usr/bin/env python

# libraries to fetch data
from urllib.request import Request, urlopen
import json
from collections import OrderedDict
import datetime

# init variables
today = datetime.date.today()
today = today.strftime('%Y-%m-%d')
link = 'https://api.coindesk.com/v1/bpi/historical/close.json?start=2011-01-01&end=' + today
coindeskURL = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
outputData = {}

# fetch data
dataRes = urlopen(coindeskURL).read().decode('utf8')
data = json.loads(dataRes, object_pairs_hook=OrderedDict)

i = 0
for key, value in data["bpi"].items() :
    outputData[str(i)] = value
    #print(key, value)
    i += 1

#print(outputData)

#
#print(data)
with open('/home/felix/Projets/TOAST/BTC/BTC_CODE/BTC_PROCESSING/data/JSONs/historicalData.json', 'w') as outfile:
    json.dump(outputData, outfile)
