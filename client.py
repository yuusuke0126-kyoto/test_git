# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 23:05:35 2015

@author: Swarm Control 1
"""

import socket
import time

host = '10.249.255.147'
port = 9999
clientsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientsock.bind((host, port))
print("waiting...")

for i in range(10):
    recv_msg, addr = clientsock.recvfrom(1024)
    print("Received ->", int.from_bytes(recv_msg, "big"))
    time.sleep(1)
