#!/usr/bin/env python

# libraries to fetch data
from websocket import create_connection
from urllib.request import Request, urlopen
import json

def main():
    # init websocket
    try:
        ws = create_connection("wss://ws.blockchain.info/inv")
        ws.send('{"op" : "unconfirmed_sub"}')
        print("Connection to blockchain.info successful")
    except:
        print("Could not connect to blockchain.info")

    # init counter
    counter = 0
    
    # open file
    dataFile = open('data/analytics02.txt', 'a')
    
    # main loop
    while True:
        # a transaction has taken placec
        try:
            result =  ws.recv()
        except (KeyboardInterrupt, SystemExit):
            dataFile.close()
            raise
        except:
            print("Error with receiving from websocket")
            result = None


        if result != None:
            # parse the data
            try:
                data = json.loads(result)
            except:
                print("Error with loading json data")
                data = None
                
            if data != None:    
                counter = counter + 1

                # init variables
                value = 0

                # get time
                transTime = data["x"]["time"]

                # loop through all sub transactions and add up their values
                for subdata in data["x"]["out"] :
                    value += subdata["value"]

                # print to console for good measure
                print(str(counter) + "\t" + str(transTime) + '\t' + str(value))
                
                # write to file
                dataFile.write(str(counter) + "-" + str(transTime) + "-" + str(value) + "\n")

    ws.close()

if __name__ == '__main__':
    main()

