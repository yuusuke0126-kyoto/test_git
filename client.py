# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 23:05:35 2015

@author: Swarm Control 1
"""

import socket
import time

host = '127.0.0.1'
port = 3794
clientsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientsock.bind((host, port))
print("wait...")
time.sleep(1)

for i in range(10):
    recv_msg, addr = clientsock.recvfrom(1024)
    print("Received ->", int.from_bytes(recv_msg, "big"))