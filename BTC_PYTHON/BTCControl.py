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
from pythonosc import dispatcher
from pythonosc import osc_server
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
            log("Connection to " + serialName + " successful")
            break
        except:
            ser = None
            log("Can't connect to" + serialName + " trying next.")

    return ser

# process and send command through serial communication
def sendMotorCommand(message) :
    global toggleMotor
    global ser
    global numBytes
    if(toggleMotor) :
        if ser.in_waiting > 1000 :
            ser.reset_input_buffer()
        try :
            numBytes = ser.write(message.encode())
        except :
            log("Couldn't send serial port message.")
        return
    #else :
        #log("Serial communication deactivated.")


# connect to osc
def connect_oscClient(ip, port):
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default=ip)
    parser.add_argument("--port", type=int, default=port)
    args = parser.parse_args()
    return udp_client.SimpleUDPClient(args.ip, args.port)

# function that answers to /startSocket OSC address
# starts websocket
def launch_websocket_thread(unused_addr):
    global ws
    global websocketOpen
    if websocketOpen :
        log("launch_websocket_thread : Websocket already open.")
    else :        
        threading.Thread(target=ws.run_forever).start()
        websocketOpen = True

# unction that answers to /closeSocket OSC address
# closes websocket. NOT TO BE USED ! DOESN'T WORK
def stop_websocket(unused_addr):
    global ws
    global websocketOpen
    if websocketOpen :
        websocketOpen = False
        ws.close()
    else :
        log("stop_websocket : Websocket already closed")

# function that answers to /toggleMotors OSC address
# toggles variable that enable the spinning of the motors
def toggle_motor(unused_addr):
    global toggleMotor
    toggleMotor = not toggleMotor
    log("toggle_motor : state = " + str(toggleMotor))

# function that answers to /vibrate OSC address
# sends a message to arduino that tells the vibration motor to spin 50 steps
def launch_vibration(unused_addr) :
    global motorSpeedMin
    sendMotorCommand("0-" + str(motorSpeedMin) + "-50>")

# launch osc server
def connect_oscServer(ip, port):
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default=ip, help="The ip to listen on")
    parser.add_argument("--port", type=int, default=port, help="The port to listen on")
    args = parser.parse_args()

    global ws
    global toggleMotor
    dis = dispatcher.Dispatcher()
    dis.map("/closeSocket", stop_websocket)
    dis.map("/startSocket", launch_websocket_thread)
    dis.map("/toggleMotors", toggle_motor)
    dis.map("/vibrate", launch_vibration)

    server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dis)
    return server

# function that process 1 block from websocket
def process_block(data):
    # play sound
    #soundInd = int(random.random() * 11 + 1)
    #soundName = '/home/felix/Music/Samples/Vocal_Eliot_5_V2'
    #commandName = 'aplay -q ' + soundName + '.wav &'
    #print(commandName)
    #os.system(commandName)

    # send osc message
    msg = osc_message_builder.OscMessageBuilder(address = "/block")
    msg = msg.build()
    oscClient.send(msg)

    # debug
    log("Received a block")

# log to screen and to file
def log(logString) :
    print(logString)
    with open('data/log.txt', 'a') as f :
        f.write(logString + "\n")

# function that process 1 message from websocket
def process_trans(data):
    # play sound
    #soundInd = int(random.random() * 11 + 1)
    #soundName = '/home/felix/Music/Samples/Breath_Eliot_1_V' + str(soundInd)
    #commandName = 'aplay -q ' + soundName + '.wav &'
    #print(commandName)
    #os.system(commandName)

    # get time
    transTime = data["x"]["time"]
    officialTime =int(time.time())
    diffTime = officialTime - transTime

    if diffTime > 4 :
        log("Transaction too old\t"
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
    coinsReleased = int(counterStep / 360)
    coinReleased0 = coinsReleased % 4 == 0
    if(coinReleased0 and not prevCoinReleased0):
        vibrationMotorStep = 0
    else :
        vibrationMotorStep = 0
    prevCoinReleased0 = coinReleased0

    # map to motor speed
    motorSpeed = int(mapValue(numSteps, 1, maxStep, motorSpeedMin, motorSpeedMax))
    motorSpeed = clamp(motorSpeed, motorSpeedMax, motorSpeedMin)

    global ser
    global counterBytes
    # write message and send it
    serialPortMessage = str(numSteps) + "-" + str(motorSpeed) + "-" + str(vibrationMotorStep) + ">"
    sendMotorCommand(serialPortMessage)

    # send counter
    global oscClient
    msg = osc_message_builder.OscMessageBuilder(address = "/trans")
    msg.add_arg(transTimestr)
    #msg.add_arg(numSteps)
    msg.add_arg(valueBTCstr)
    msg = msg.build()
    oscClient.send(msg)

    # print to console for good measure
    global toggleMotor
    app = ""
    if not toggleMotor :
        app = "///"
    log(app
    + str(counterTrans) + '\t'
    + transTimestr + '\t'
    + str(diffTime) + '\t'
    + valueBTCstr + '\t'
    + str(threading.activeCount()) + '\t'
    + serialPortMessage + '\t'
    + str(coinsReleased) + '\t'
    )

# happens everytime websocket receives something
def on_message(ws, message):
    # parse the data
    try:
        data = json.loads(message)
    except:
        log("Couldn't load json from websocket message.")
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
        log("Unknown message type.")

# display websocket error
def on_error(ws, error):
    log(error)

# display message when websocket closed
def on_close(ws):
    global websocketOpen
    websocketOpen = False
    log("Websocket closed.")
    #time.sleep(1)
    #launch_websocket_thread(ws)


# happens on websocket creation
# send message to blockchain websocket in order to subscribe to unconfirmed
# transactions
def on_open(ws):
    ws.send('{"op" : "unconfirmed_sub"}')
    ws.send('{"op" : "blocks_sub"}')
    log("Websocket opened.")

## ------ MAIN PROGRAM
# start log
with open('data/log.txt', 'a') as f :
    f.write("\n############## STARTING LOG ##############\n")

# init debug variables
counterTrans = 0
counterStep = 0
counterBytes = 0

# set locale
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')

# vibration motor variables
toggleMotor = True
coinReleased0 = False
prevCoinReleased0 = False

# motor variables
maxStep = 15
motorSpeedMax = 1000     # micro seconds
motorSpeedMin = 2000    # micro seconds

# step calculation variables
curveA = -0.096167 * maxStep
curveB = 0.4952864
curveC = 0.06150178
curveD = 1.00857 * maxStep

# connect serial port
ser = connect_serial(9600)
time.sleep(0.5)

# launch osc client
oscClient = connect_oscClient("127.0.0.1", 8000)

# launch websocket
#websocket.enableTrace(True)
websocketOpen = False
ws = websocket.WebSocketApp("wss://ws.blockchain.info/inv",
                          on_open = on_open,
                          on_message = on_message,
                          on_error = on_error,
                          on_close = on_close)
launch_websocket_thread([])

# launch osc server
oscServer = connect_oscServer("192.168.0.15", 9000)
oscServer.serve_forever()
## -----------------------
