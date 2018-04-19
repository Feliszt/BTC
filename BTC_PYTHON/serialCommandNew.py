import sys
import time
import serial
import keyboard


serialNumber = 9600
motorSpeedMAX = 1600
motorSpeedMIN = 100

def send_serial(val, id):
    msg = ""
    msg = str(chr(id))+str(chr(val))
    if(ser):
    	try:
    		ser.write(msg.encode())
    	except Exception as e:
    		print(e)

def main():

    # Serial connect
    try:
        global ser
        if sys.platform.startswith('darwin'):
        	ser = serial.Serial('/dev/tty.usbmodem1a151',serialNumber)
        	print("Serial connected")
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        	try:
        		ser = serial.Serial('/dev/ttyACM0',serialNumber)
        		print("ACM0")
        	except :
        		ser = serial.Serial('/dev/ttyACM1', serialNumber)
        		print("ACM1")

        else:
        	ser = None
    except :
        print("Impossible to connect to Serial")
        ser = None

    # Setting up variables
    motorSpeed = 800      # FAST : 100 - SLOW : 1800

    while True:
        time.sleep(0.05)

        if(keyboard.is_pressed('a')):
            ser.write('<'.encode())

        if(keyboard.is_pressed('s')):
            ser.write('>'.encode())

if __name__ == "__main__":
    main()
