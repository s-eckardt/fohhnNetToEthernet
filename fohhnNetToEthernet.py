#!/bin/python
import serial
import socket
from collections import deque
import threading
import time

def udp_server():
 while True:
  udp_que.appendleft(sock.recvfrom(100))

tty = serial.Serial('/dev/ttyUSB0', timeout=2, baudrate=19200, stopbits=serial.STOPBITS_ONE)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", 2101))
udp_que = deque()
#print udp_que #Debug output
udp_que.append(sock.recvfrom(100))
tty_que = deque()
addr, data = udp_que.pop() 

rcv_thread = threading.Thread(target=udp_server)
rcv_thread.deamon = True
rcv_thread.start()

while True:
 if tty.inWaiting():
  tty_data = tty.read()
  tty_que.appendleft(tty_data)
  tty_hex_data = tty_data.encode('hex')
#  print tty_hex_data #Debug output
#  print tty_que #Debug output
  if tty_hex_data[len(tty_hex_data) - 2:] == "f0":
   data_string = ""
   while(len(tty_que)):
    data_string = data_string + tty_que.pop()
   sock.sendto(data_string, addr)
 if len(udp_que):
  data, addr = udp_que.pop()
  tty.write(data)
  tty.flush()
 #time.sleep(0.004)

sock.close()
