# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import socket
import time

def sendmsg(send_msg):
    host = '127.0.0.1'
    port = 3794
    serversock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Type message...")
#    send_msg = raw_input()
    serversock.sendto(send_msg, (host, port))


if __name__ == "__main__":
    i = 0
    for i in range(100):
        j = i +100
        print(j)
        sendmsg(j.to_bytes(1,"big"))
        time.sleep(0.5)
    
