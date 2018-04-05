# import stuff
import pysher
import time
import json
import argparse
from pythonosc import osc_message_builder
from pythonosc import udp_client
import sys
import logging

# Add a logging handler so we can see the raw communication data
root = logging.getLogger()
root.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
root.addHandler(ch)

# connect OSC
parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="127.0.0.1")
parser.add_argument("--port", type=int, default=8000)
args = parser.parse_args()
oscClient = udp_client.SimpleUDPClient(args.ip, args.port)

# create pusher to get live trade data
pusher = pysher.Pusher('de504dc5763aeef9ff52')
# process data whenever we receive it
def callback(*args, **kwargs):
    temp = json.loads(json.dumps(args))
    data = json.loads(temp[0])
    price = data["price"]
    print(price)
    print(data["amount"])
    oscClient.send_message("/price", price)

# connect to channel
def connect_handler(data):
    channel = pusher.subscribe('live_trades')
    channel.bind('trade', callback)
pusher.connection.bind('pusher:connection_established', connect_handler)
pusher.connect()

while True:
    time.sleep(1)
