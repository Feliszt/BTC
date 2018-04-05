import socket
from websocket import create_connection, WebSocket
class MyWebSocket(WebSocket):
    def recv_frame(self):
        frame = super().recv_frame()
        print('yay! I got this frame: ', frame)
        return frame

ws = create_connection("wss://ws.blockchain.info/inv",
                        sockopt=((socket.IPPROTO_TCP, socket.TCP_NODELAY, 1),), class_=MyWebSocket)
ws.send('{"op" : "unconfirmed_sub"}')
