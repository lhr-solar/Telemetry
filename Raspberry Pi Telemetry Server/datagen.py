import time
import random
from influxdb import InfluxDBClient
import socket
import struct
import signal
import sys

host = "127.0.1.1"
port = 8086
user = "rpi3"
password = "tape" 
dbname = "test"
interval = 5

# set up SIGINT handler so that the socket is closed if the program is ended
def signal_handler(sig, frame):
        sock.close()
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# influx client
client = InfluxDBClient(host, port, user, password, dbname)

# set up socket stuff
UDP_IP = "192.168.4.2"
UDP_PORT = 6969

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

# name table
measurement = "test_data"

try:
    while True:
        # randomly generate a number for speed and get time stamp
        #speed = random.randint(30,50)
        speed = int(sock.recv(4).strip('\0'))
        print(speed)
        timing = time.ctime()
        
        # print and make data packet
        print("[%s] Speed: %s" % (timing, speed)) 
        # make JSON data packet
        data = [ {
          "measurement": measurement,
            "time": timing,
            "fields": {
                "speed" : speed
              }
        } ]

        # write JSON to influx
        client.write_points(data)
        print("sent")
        # pause program
        time.sleep(interval)
 
except KeyboardInterrupt:
    pass

