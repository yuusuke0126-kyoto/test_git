# -*- coding: utf-8 -*-
"""
This is UDP program for Rpi

@author: Swarm Control 1
"""
import socket
import time


if __name__ == "__main__":
    hostopstn = '10.249.255.194'
#    hostrpi = '10.249.255.194'
    hostrpi = '10.249.255.147'
    port = 9999
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.bind((hostrpi, 9999))
    
        print("Now sending...")
        
        for i in range(256):
            print(i)
            sock.sendto(i.to_bytes(1,"big"), (hostopstn, port))
            time.sleep(0.01)
            
#            print("waiting...")
#            recv_msg, addr = sock.recvfrom(1024)
#            print("Received ->", int.from_bytes(recv_msg, "big"))
#            time.sleep(0.05)
    finally:
        sock.close()
