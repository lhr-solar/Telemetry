import time
import random
from influxdb import InfluxDBClient

host = "127.0.1.1"
port = 8086
user = "rpi3"
password = "tape" 
dbname = "test"
interval = 6 #seconds

# influx client
client = InfluxDBClient(host, port, user, password, dbname)

# name table
measurement = "test_data"

try:
    while True:
        # randomly generate a number for speed and get time stamp
        speed = random.randint(30,50)
        timing = time.ctime()
        
        # bugbug
        print("[%s] Speed: %s" % (timing, speed)) 

        # make JSON data packet
        data = [ {
          "measurement": measurement,
            "time": timing,
            "fields": {
                "speed" : speed
              }
        } ]

        # write JSON to influx and make sure he got it
        client.write_points(data)
        print("sent")

        # pause program
        time.sleep(interval)
 
except KeyboardInterrupt:
    pass