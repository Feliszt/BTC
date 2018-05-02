#!/usr/bin/env python

# libraries to receive data
import websocket
# libraries to process data
import threading
import json
import time
import datetime
import locale
import os
import random
# libraries to send and receive messages
import argparse
from pythonosc import osc_message_builder
from pythonosc import udp_client
import sys
import serial

# clamp input variable between 2 variables
def clamp(val, min_, max_):
    return min_ if val < min_ else max_ if val > max_ else val

def mapValue(x, a, b, c, d):
   y = (x - a) / (b - a) * (d - c) + c
   return y

# connect to serial port
def connect_serial(serialBaud):
    for i in range(0,5):
        serialName = '/dev/ttyACM' + str(i)
        try:
            ser = serial.Serial(serialName,serialBaud, write_timeout = 0)
            print("Connection to " + serialName + " successful")
            break
        except:
            ser = None
            print("Can't connect to" + serialName + " trying next.")

    return ser

# connect to osc
def connect_osc(ip, port):
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default=ip)
    parser.add_argument("--port", type=int, default=port)
    args = parser.parse_args()
    return udp_client.SimpleUDPClient(args.ip, args.port)

# function that process 1 block from websocket
def process_block(data):
    # play sound
    soundInd = int(random.random() * 11 + 1)
    soundName = '/home/felix/Music/Samples/Vocal_Eliot_5_V2'
    commandName = 'aplay -q ' + soundName + '.wav &'
    #print(commandName)
    os.system(commandName)

    # send osc message
    msg = osc_message_builder.OscMessageBuilder(address = "/block")
    msg = msg.build()
    oscClient.send(msg)

    # debug
    print("Received a block")

# function that process 1 message from websocket
def process_trans(data):
    # test
    if random.random() < 0.0 :
        print("Fuck this transaction.")
        return
    
    # play sound
    soundInd = int(random.random() * 11 + 1)
    soundName = '/home/felix/Music/Samples/Breath_Eliot_1_V' + str(soundInd)
    commandName = 'aplay -q ' + soundName + '.wav &'
    #print(commandName)
    #os.system(commandName)

    # get time
    transTime = data["x"]["time"]
    officialTime =int(time.time())
    diffTime = officialTime - transTime

    if diffTime > 4 :
        print("Transaction too old\t"
              + str(diffTime) + "\t"
              + str(threading.activeCount()) + '\t'
              )
        return

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

    # compute steps
    global curveA
    global curveB
    global curveC
    global curveD
    global maxStep
    global counterStep
    global coinReleased0
    global prevCoinReleased0
    numSteps = curveD + (curveA - curveD) / (1 + (valueBTCfloat / curveC) ** curveB )
    numSteps = int(numSteps)
    numSteps = clamp(numSteps, 1, maxStep)
    counterStep += numSteps
    coinsReleased = int(counterStep / 178)
    coinReleased0 = coinsReleased % 15 == 0
    if(coinReleased0 and not prevCoinReleased0):
        vibrationMotorStep = 50
    else :
        vibrationMotorStep = 50
    prevCoinReleased0 = coinReleased0

    # map to motor speed
    motorSpeed = int(mapValue(numSteps, 1, maxStep, motorSpeedMin, motorSpeedMax))
    motorSpeed = clamp(motorSpeed, motorSpeedMax, motorSpeedMin)

    global ser
    global counterBytes
    # write message and send it
    serialPortMessage = str(numSteps) + "-" + str(motorSpeed) + "-" + str(vibrationMotorStep) + ">"
    #string = "1>"
    if ser.in_waiting > 1000 :
        ser.reset_input_buffer()
    try :
        numBytes = ser.write(serialPortMessage.encode())
    except :
        print("Couldn't send serial port message.")
        return

    # send counter
    global oscClient
    msg = osc_message_builder.OscMessageBuilder(address = "/trans")
    msg.add_arg(transTimestr)
    msg.add_arg(numSteps)
    #msg.add_arg(valueBTCstr)
    msg = msg.build()
    oscClient.send(msg)

    # print to console for good measure
    print(str(counterTrans) + '\t'
    + transTimestr + '\t'
    + str(diffTime) + '\t'
    #+ valueBTCstr + '\t'
    + str(threading.activeCount()) + '\t'
    + serialPortMessage + '\t'
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
counterStep = 0
counterBytes = 0

# set locale
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')

# connect serial port
ser = connect_serial(9600)
time.sleep(0.5)

# connect osc
oscClient = connect_osc("127.0.0.1", 8000)

# vibration motor variables
coinReleased0 = False
prevCoinReleased0 = False

# motor variables
maxStep = 200
motorSpeedMax = 500     # micro seconds
motorSpeedMin = 2500    # micro seconds

# step calculation variables
curveA = -0.096167 * maxStep
curveB = 0.4952864
curveC = 0.06150178
curveD = 1.00857 * maxStep

# launch websocket
#websocket.enableTrace(True)
ws = websocket.WebSocketApp("wss://ws.blockchain.info/inv",
                          on_message = on_message,
                          on_error = on_error,
                          on_close = on_close)
ws.on_open = on_open
ws.run_forever()
## -----------------------
