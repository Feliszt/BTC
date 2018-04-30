#!/usr/bin/env python

# libraries to fetch data
import websocket
import json
# libraries to process data
import threading
import time
import datetime
import locale

# function that process 1 block from websocket
def process_block(data):
    # play sound
    soundInd = int(random.random() * 11 + 1)
    soundName = '/home/felix/Music/Samples/Vocal_Eliot_5_V2'
    commandName = 'aplay -q ' + soundName + '.wav &'
    #print(commandName)
    os.system(commandName)

    # debug
    print("Received a block")

# function that process 1 message from websocket
def process_trans(data):
    # get time
    transTime = data["x"]["time"]
    officialTime =int(time.time())
    diffTime = officialTime - transTime

    # init variables
    global counterTrans
    counterTrans += 1
    value = 0

    # loop through all sub transactions and add up their values
    for subdata in data["x"]["out"] :
        value += subdata["value"]

    # compute values of transaction
    valueBTCfloat = value / 100000000
    valueBTCstr = locale.format("%14.8f", valueBTCfloat, grouping=True)

    # compute human readable time
    transTimestr = datetime.datetime.fromtimestamp(transTime).strftime('%H:%M:%S')

    # print to console for good measure
    print(
    str(counterTrans) + '\t'
    + transTimestr + '\t'
    + str(diffTime) + '\t'
    + valueBTCstr + '\t'
    + str(threading.activeCount()) + '\t'
    )

# happens everytime websocket receives something
def on_message(ws, message):
    # parse the data
    try:
        data = json.loads(message)
    except:
        print("Couldn't load json from websocket message.")
        return

    # get type of message and takes decision
    messageType = data["op"]
    if (messageType == "utx") :
        thread = threading.Thread(target=process_trans, args=(data,))
        thread.start()
    elif (messageType == "block") :
        thread = threading.Thread(target=process_block, args=(data,))
        thread.start()
    else :
        print("Unknown message type.")

# display websocket error
def on_error(ws, error):
    print(error)

# display message when websocket closed
def on_close(ws):
    print("Websocket closed.")

# happens on websocket creation
# send message to blockchain websocket in order to subscribe to unconfirmed
# transactions
def on_open(ws):
    ws.send('{"op" : "unconfirmed_sub"}')
    ws.send('{"op" : "blocks_sub"}')
    print("Websocket opened.")

## ------ MAIN PROGRAM
# init debug variables
counterTrans = 0

# set locale
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')

# launch websocket
#websocket.enableTrace(True)
ws = websocket.WebSocketApp("wss://ws.blockchain.info/inv",
                          on_message = on_message,
                          on_error = on_error,
                          on_close = on_close)
ws.on_open = on_open
ws.run_forever()
## -----------------------
