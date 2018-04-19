import sys
import time
import serial
import keyboard

motorSpeed = 800      # FAST : 100 - SLOW : 1800

def send_serial(val, id):
	msg = ""
	msg = str(chr(id))+str(chr(val))
	if(ser):
        print(msg)
		try:
			ser.write(msg.encode())
		except Exception as e:
			print(e)

def main():

    # Serial connect
    try:
    	global ser
    	if sys.platform.startswith('darwin'):
    		ser = serial.Serial('/dev/tty.usbmodem1a151',115200)
    		print("Serial connected")
    	elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
    		try:
    			ser = serial.Serial('/dev/ttyACM0',115200)
    			print("ACM0")
    		except :
    			ser = serial.Serial('/dev/ttyACM1', 115200)
    			print("ACM1")

    	else:
    		ser = None
    except :
    	print("Impossible to connect to Serial")
    	ser = None

    # Setting up variables

    while True:
        time.sleep(0.05)

        send_serial(motorSpeed, 1)

if __name__ == "__main__":
    main()
