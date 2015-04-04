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
        
    Returns
    -------
    data : bytes
        The last received message, or None if the socket was not ready.
    size : int
        The number of bytes to read at a time.
    
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
    test()