# -*- coding: utf-8 -*-
"""
This is UDP program for Opstn
@author: Swarm Control 1
"""
import select
import signal
import socket
import time


def sigalrm_handler(signum, frame):
    """The handler for SIGALRM."""
    raise TimeoutError


def get_latest(sock, size=1):
    """
    Get the latest input.
    
    This function automatically empties the given socket.
    
    Parameters
    ----------
    sock : socket
        The socket to be emptied.
    size : int
        The number of bytes to read at a time.
        
    Returns
    -------
    data : bytes
        The last received message, or None if the socket was not ready.
    
    """
    data = None
    input_ready, o, e = select.select([sock], [], [], 0.0)  # Check if ready.
    
    while input_ready:
        data = input_ready[0].recv(size)  # Read everything
        input_ready, o, e = select.select([sock], [], [], 0.0)
        
    return data


def receive_data(sock, delay=0.01, size=32):
    """
    Receive UDP data without blocking.
    
    Parameters
    ----------
    sock : socket
        The socket to use.
    delay : float, optional
        The timeout within which to read the socket, in seconds.
    size : int
        The number of bytes to read.
    
    Returns
    -------
    recv_msg : bytes
        The received message, or None if the buffer was empty.
        
    """
    recv_msg = None
    
    try:
        signal.setitimer(signal.ITIMER_REAL, delay, 0)  # Set up interrupt.
        recv_msg = get_latest(sock, size=size)
    except (BlockingIOError, TimeoutError):
        pass
    finally:
        signal.alarm(0)  # Cancel interrupt.

    return recv_msg

def get_input():
    mode = linear = pitch = yaw = 0
    key = input("Press 'wasd' for roll/pitch or 'jk' for linear or 'QRS' for quit/reset/startpos: ")
    if key == "w":
        pitch = 1
    elif key == "s":
        pitch = 2
    elif key == "a":
        yaw = 1
    elif key == "d":
        yaw = 2
    elif key == "j":
        linear = 1
    elif key == "k":
        linear = 2
    elif key == "Q":
        mode = 3
    elif key == "R":
        mode = 2
    elif key == "S":
        mode = 1
    
    return mode, linear, pitch, yaw

class Arm:
    
    def __init__(self, hostopstn, hostmbed):
        self.hostopsnt = hostopstn
        self.hostmbed = hostmbed
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self.sock.bind(hostopstn)
        
        signal.signal(signal.SIGALRM, sigalrm_handler)
        
        mode = 1
        self.sock.sendto(mode.to_bytes(1,"little"), self.hostmbed)
    
    def send_arm(self, mode, linear, pitch, yaw):
        senddata = 0
        if max(mode, linear, pitch, yaw) > 3:
            raise ValueError
        elif mode is not 0:
            senddata = mode
        else:
            senddata += (linear<<2) + (pitch<<4) + (yaw<<6)
        print("Send data is '{}' '{}'".format(senddata, bin(senddata)))
        self.sock.sendto(senddata.to_bytes(1, "little"), self.hostmbed)
    
    def recv_sensor(self):
        recv_msg = receive_data(self.sock, size=1024)
        return recv_msg
#        if recv_msg is not None:
#            return recv_msg
#        else:
#            raise ValueError
                



def test():
    hostopstn = '10.249.255.194'
#    hostrpi = '10.249.255.194'
#    hostrpi = '10.249.255.147'

    signal.signal(signal.SIGALRM, sigalrm_handler)
    
    successful_count = 0
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    sock.bind((hostopstn, 9999))
    
    try:
        for i in range(255):
            recv_msg = receive_data(sock, delay=2)
            if recv_msg is not None:
                print("Received -> {data}".format(
                    data=int.from_bytes(recv_msg, "big")))
                successful_count += 1
            time.sleep(1)

    finally:
        sock.close()
        print("Got {n} messages in total.".format(n=successful_count))


if __name__ == "__main__":
    ipopstn = "127.0.0.1"
#    ipopstn = "192.168.1.90"
    ipmbed = "127.0.0.1"
#    ipmbed = "192.168.1.100"
    portopstn = 9998
    portmbed = 9999
    hostopstn = (ipopstn, portopstn)
    hostmbed = (ipmbed, portmbed)
    
    arm = Arm(hostopstn, hostmbed)
    time.sleep(1)
    
    try:
        while True:
            mode, linear, pitch, yaw = get_input()
            print(mode, linear, pitch, yaw)
            arm.send_arm(mode, linear, pitch, yaw)
            time.sleep(0.5)
            sensor_data = arm.recv_sensor()
            if sensor_data is not None:
                #print("Received -> " + sensor_data.decode())
                print("Reception success!")
            else:
                print("Reception failure!")

    finally:
        arm.sock.close()
