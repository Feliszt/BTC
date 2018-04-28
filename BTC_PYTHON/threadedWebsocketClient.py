# libraries to receive data
import websocket
# libraries to process data
import threading
import json
import time
import datetime
import locale
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
            ser = serial.Serial(serialName,serialBaud)
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

# function that process 1 message from websocket
def process_message(message):
    # parse the data
    try:
        data = json.loads(message)
    except:
        data = None
        print("Couldn't load json from websocket message.")
        return

    # get time
    transTime = data["x"]["time"]
    officialTime =int(time.time())
    diffTime = officialTime - transTime

    if diffTime > 4 :
        print("Transaction too old")
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

    # send counter
    global oscClient
    msg = osc_message_builder.OscMessageBuilder(address = "/trans")
    msg.add_arg(transTimestr)
    msg.add_arg(valueBTCstr)
    msg = msg.build()
    oscClient.send(msg)

    # send through serial port
    global ser
    if ser != None:
        # compute steps
        global curveA
        global curveB
        global curveC
        global curveD
        global maxStep
        global counterStep
        numSteps = curveD + (curveA - curveD) / (1 + (valueBTCfloat / curveC) ** curveB )
        numSteps = int(numSteps)
        numSteps = clamp(numSteps, 1, maxStep)
        counterStep += numSteps

        # map to motor speed
        motorSpeed = int(mapValue(numSteps, 1, maxStep, motorSpeedMin, motorSpeedMax))
        motorSpeed = clamp(motorSpeed, motorSpeedMax, motorSpeedMin)

        # write message and send it
        string = "<" + str(numSteps) + "-" + str(motorSpeed) + ">"
        ser.write(string.encode())
    else:
        numsteps = 0

    # print to console for good measure
    print(str(counterTrans) + '\t' + transTimestr + '\t' + str(officialTime - transTime) + '\t' + valueBTCstr + '\t' + str(threading.activeCount()) + '\t' + str(numSteps))

# happens everytime websocket receives something
def on_message(ws, message):
    thread = threading.Thread(target=process_message, args=(message,))
    thread.start()

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
    print("Websocket opened.")

## ------ MAIN PROGRAM
# init debug variables
counterTrans = 0
counterStep = 0
# set locale
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')

# connect serial port
ser = connect_serial(9600)

# connect osc
oscClient = connect_osc("127.0.0.1", 8000)

# motor variables
maxStep = 150
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
