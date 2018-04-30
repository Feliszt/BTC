# libraries to produce data
import random
# libraries for sending data
import argparse
from pythonosc import dispatcher
from pythonosc import osc_server
import serial

# clamp input variable between 2 variables
def clamp(val, min_, max_):
    return min_ if val < min_ else max_ if val > max_ else val

def mapValue(x, a, b, c, d):
   y = (x - a) / (b - a) * (d - c) + c
   return y

def send_transaction(unused_addr):
    global ser
    global maxStep
    global motorSpeedMax
    global motorSpeedMin
    global counterTrans
    counterTrans += 1
    if ser != None:
        # get step number
        numSteps = int(random.random() * maxStep) + 1

        # map to motor speed
        motorSpeed = int(mapValue(numSteps, 1, maxStep, motorSpeedMin, motorSpeedMax))
        motorSpeed = clamp(motorSpeed, motorSpeedMax, motorSpeedMin)

        # write message and send it
        string = "<" + str(numSteps) + "-" + str(motorSpeed) + ">"
        ser.write(string.encode())

        print(str(counterTrans) + '\t' + str(numSteps) + '\t' + str(motorSpeed))
    else:
        print("Serial port not set up.")


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
    parser.add_argument("--ip", default=ip, help="The ip to listen on")
    parser.add_argument("--port", type=int, default=port, help="The port to listen on")
    args = parser.parse_args()

    dis = dispatcher.Dispatcher()
    dis.map("/sendTrans", send_transaction)

    server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dis)
    return server

## -- MAIN PROGRAM
# init variables
motorSpeedMax = 500     # micro seconds
motorSpeedMin = 2000    # micro seconds
maxStep = 150
counterTrans = 0

# connect serial port
ser = connect_serial(115200)

# connect osc
oscServer = connect_osc("192.168.0.12", 5005)

oscServer.serve_forever()
## -----------------
