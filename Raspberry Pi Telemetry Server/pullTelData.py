import time
import random
from influxdb import InfluxDBClient
import struct
import signal
import sys
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import json
import threading

loadStatus = True

#set up web driver
#driver = webdriver.Chrome(executable_path='/usr/lib/chromium-browser/chromedriver')
#driver.set_page_load_timeout(30)

#set up thread to stop page loading if it takes too long
def timeoutThread():
	loadStatus = True
	time.sleep(15)
	if loadStatus:
		print("stopping window")
		driver.execute_script("return window.stop")

host = "127.0.1.1"
port = 8086
user = "rpi3"
password = "pineapple" 
dbname = "test"
interval = 5

# set up SIGINT handler so that the socket is closed if the program is ended
def signal_handler(sig, frame):
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# influx client
client = InfluxDBClient(host, port, user, password, dbname)

# name table
measurement = "test_data"

#driver.get('http://192.168.0.120:80')

#time.sleep(10)

try:
	while True:
		print("accessing web page")
		#try:
		#	threading.Thread(target=timeoutThread).start()
		#	driver.get('http://192.168.0.120:80')
		#	loadStatus = False
		#except:
		#	print("connection error")

		print("parsing webpage")
		#content = driver.page_source
		content = ''
		with open('/home/pi/Downloads/telemetry2.html', "r") as f:
			content = f.read()
		soup = bs(content, features="html.parser")
		data = []
		classNames = ['temperature', 'voltage', 'current', 'soc', 'flags', 'motor', 'mppt']
		for className in classNames:
			for p in soup.findAll('p', class_ = className):
				parsedString = p.contents[0].split(' | ')
				dataPoint = {}
				dataPoint['measurement'] = className
				dataPoint['time'] = time.ctime()
				if len(parsedString) == 1:
					value = {'value': float(p.contents[0])}
					dataPoint['fields'] = value
				else:
					IDPairs = {}
					for string in parsedString:
						if (len(string) > 1):
							splitStr = string.split(': ')
							for i in range(len(splitStr)):
								splitStr[i] = splitStr[i].strip('\n')
							IDPairs[splitStr[0].strip(' ')] = float(splitStr[1].strip(' '))
							if className == 'temperature' or className == 'voltage':
								values = IDPairs.values()
								mean = 0
								for val in values:
									mean += val
								mean = mean/len(IDPairs)
								IDPairs['mean'] = mean
					dataPoint['fields'] = IDPairs
					
				data.append(dataPoint)
			
		print(json.dumps(data))
		client.write_points(data)
		time.sleep(interval)

except KeyboardInterrupt:
	pass
