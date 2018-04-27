#!/usr/bin/env python

# libraries to fetch data
from websocket import create_connection
from urllib.request import Request, urlopen
import json
# libraries to process data
import time
import datetime
import locale

def main():
    # init websocket
    try:
        ws = create_connection("wss://ws.blockchain.info/inv")
        ws.send('{"op" : "unconfirmed_sub"}')
        print("Connection to blockchain.info successful")
    except:
        print("Could not connect to blockchain.info")

    # init variable
    satoshi = 100000000
    ind = 0

    # main loop
    while True:
        # a transaction has taken place
        try:
            result =  ws.recv()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            result = None

        if result != None:
            #
            print("Received transaction")

            # parse the data
            data = json.loads(result)

            # init variables
            ind = ind + 1
            value = 0

            # get time
            transTime = data["x"]["time"]
            officialTime =int(time.time())

            # loop through all sub transactions and add up their values
            for subdata in data["x"]["out"] :
                value += subdata["value"]

            # compute values of transaction
            valueBTCfloat = value / satoshi

            # compute human readable time
            transTimestr = datetime.datetime.fromtimestamp(transTime).strftime('%H:%M:%S')

            # print to console for good measure
            print(str(ind) + '\t' + transTimestr + '\t' + str(officialTime - transTime) + '\t' + str(value))

            # test sleep
            time.sleep(0.5)

            print("Finished processing transaction")

    ws.close()

if __name__ == '__main__':
    main()
