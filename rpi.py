# -*- coding: utf-8 -*-
"""
This is UDP program for Rpi

@author: Swarm Control 1
"""

import socket
import time

def sendmsg(send_msg, host, port):
    sendsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Send message...")
    sendsock.sendto(send_msg, (host, port))


if __name__ == "__main__":
    hostopstn = '10.249.255.194'
    hostrpi = '10.249.255.194'
#    hostrpi = '10.249.255.147'
    port = 9999
    Recvsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    Recvsock.bind((hostrpi, 9998))
    
    print("Now sending...")
    
    for i in range(20):
        j = i +100
        print(j)
        sendmsg(j.to_bytes(1,"big"), hostopstn, port)
        time.sleep(0.05)
        
        print("waiting...")
        recv_msg, addr = Recvsock.recvfrom(1024)
        print("Received ->", int.from_bytes(recv_msg, "big"))
        time.sleep(0.05)