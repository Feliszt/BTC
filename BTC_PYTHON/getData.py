#!/usr/bin/env python

# libraries to fetch data
from websocket import create_connection
from urllib.request import Request, urlopen
import json
# libraries to process data
import datetime
import locale
# libraries to send and receive messages
import argparse
from pythonosc import osc_message_builder
from pythonosc import udp_client

# init websocket
ws = create_connection("wss://ws.blockchain.info/inv")
ws.send('{"op" : "unconfirmed_sub"}')

# connect OSC
parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="127.0.0.1")
parser.add_argument("--port", type=int, default=8000)
args = parser.parse_args()
oscClient = udp_client.SimpleUDPClient(args.ip, args.port)

# init variables
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
coindeskCurrPrice = Request('https://api.coindesk.com/v1/bpi/currentprice.json', headers={'User-Agent': 'your bot 0.1'})
coindeskLastPrice = Request('https://api.coindesk.com/v1/bpi/historical/close.json?currency=EUR', headers={'User-Agent': 'your bot 0.1'})
ind = 0
satoshi = 100000000
currTime = 0
timePrev = currTime
btcPriceEUR = 0
btcCounter = 0
btcCounterLimit = 1000

# get today's open BTC price and send it
coindeskLastPrice = urlopen(coindeskLastPrice).read().decode('utf8')
coindeskLastPriceData = json.loads(coindeskLastPrice)
btcLastPriceEURlist = coindeskLastPriceData['bpi']
yesterday = datetime.date.today() - datetime.timedelta(1)
yesterday = yesterday.strftime('%Y-%m-%d')
btcLastPriceEURfloat = btcLastPriceEURlist[yesterday]
btcLastPriceEURstr = locale.format("%.2f", btcLastPriceEURfloat, grouping=True)

# main loop
while True:
    # a transaction has taken place
    result =  ws.recv()

    # parse the data
    data = json.loads(result)

    # init variables
    ind = ind + 1
    value = 0

    # get time
    transTime = data["x"]["time"]

    # every ten seconds, fetch bitcoin to euro value
    if transTime - currTime > 59 :
        currTime = transTime

    # this happens every minutes
    if currTime != timePrev :
        bitstampRes = urlopen(coindeskCurrPrice).read().decode('utf8')
        bitstampData = json.loads(bitstampRes)
        btcPriceEURfloat = bitstampData["bpi"]["EUR"]["rate_float"]
        btcPriceEURstr = locale.format("%.2f", btcPriceEURfloat, grouping=True)
        variation = (btcPriceEURfloat - btcLastPriceEURfloat) / btcLastPriceEURfloat * 100
        variationstr = locale.format("%.2f", variation, grouping=True)
        print("Price update : ", btcPriceEURstr)

        # send BTC value message
        msg = osc_message_builder.OscMessageBuilder(address = "/priceEUR")
        msg.add_arg(btcPriceEURstr)
        msg.add_arg(btcLastPriceEURstr)
        msg.add_arg(variationstr)
        msg = msg.build()
        oscClient.send(msg)

    # loop through all sub transactions and add up their values
    for subdata in data["x"]["out"] :
        value += subdata["value"]

    # compute values of transaction
    valueBTCfloat = value / satoshi
    valueBTCstr = locale.format("%14.8f", valueBTCfloat, grouping=True)
    valueEURfloat = valueBTCfloat * btcPriceEURfloat
    valueEURstr = locale.format("%12.2f", valueEURfloat, grouping=True)

    # update bitcoin counter
    btcCounter += valueBTCfloat
    btcCounterRatiofloat = btcCounter / btcCounterLimit

    # we release a coin and restart
    if(btcCounter >= btcCounterLimit) :
        btcCounter = 0

    # send counter
    msg = osc_message_builder.OscMessageBuilder(address = "/btcCounter")
    msg.add_arg(btcCounterRatiofloat)
    msg = msg.build()
    oscClient.send(msg)

    # compute human readable time
    transTimestr = datetime.datetime.fromtimestamp(transTime).strftime('%H:%M:%S')

    # send OSC message
    msg = osc_message_builder.OscMessageBuilder(address = "/trans")
    msg.add_arg(transTimestr)
    msg.add_arg(valueBTCstr)
    msg.add_arg(valueEURstr)
    msg = msg.build()
    oscClient.send(msg)

    # print to console for good measure
    print(transTimestr + '\t' + valueBTCstr + '\t' + valueEURstr + '\t' + str(btcCounter))
    #print(data)

    # update values
    timePrev = currTime

ws.close()
