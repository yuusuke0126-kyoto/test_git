# -*- coding: utf-8 -*-
"""
This is UDP program for recv

@author: Swarm Control 1
"""
import socket
import time


if __name__ == "__main__":
    ipmbed = "127.0.0.1"
    ipopstn = "127.0.0.1"
#    host = "192.168.1.90"
#    hostopstn = '10.249.255.194'
#    hostrpi = '10.249.255.194'
#    hostrpi = '10.249.255.147'
    portmbed = 9999
    portopstn = 9998
    hostmbed = (ipmbed, portmbed)
    hostopstn = (ipopstn, portopstn)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.bind(hostmbed)
        print("Now waiting...")
        
        for i in range(256):
            recv_msg = sock.recv(1024)
            recv_data = int.from_bytes(recv_msg, "little")
            print("Received ->", recv_data, bin(recv_data))
            time.sleep(0.1)
            
            if i % 3 is not 0:
                print("Send data")
                data_list = [str(j/2) for j in range(50)]
                data_str = " ".join(data_list)
                #print(data_str)
                send_data = data_str.encode()
                sock.sendto(send_data, hostopstn)
                time.sleep(0.1)
            else:
                print("Not send data")
            
    finally:
        sock.close()
