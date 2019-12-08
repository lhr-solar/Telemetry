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
driver = webdriver.Chrome(executable_path='./chromedriver')
driver.set_page_load_timeout(10)

host = "127.0.1.1"
port = 8086
user = "rpi3"
password = "pineapple" 
dbname = "test"
interval = 5

# set up SIGINT handler so that the program is properly closed if it is interrupted
def signal_handler(sig, frame):
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# influx client
client = InfluxDBClient(host, port, user, password, dbname)

# name table
measurement = "test_data"

def startDriver():
	driver.get('http://192.168.0.120:80')

try:
	#Main while loop that will continuously scrape the web page
	while True:
		loadStatus = True
		fail_count = 0
		#this while loop handles loading the web page and retrying if loading fails
		while loadStatus:
			try:
				if fail_count > 5:
					driver.close()
					driver = webdriver.Chrome(executable_path='./chromedriver')
					driver.set_page_load_timeout(10)
					fail_count = 0
					print('failed to access webpage 5 times in a row, restarting browser')
				print('accessing web page')
				startDriver()
				loadStatus = False
			except:
				print('retrying webpage')
				loadStatus = True
				fail_count += 1
				#If we get past 5 fails we know the web browser has been closed so we exit
				if fail_count > 6:
					print('web browser has been closed, ending python web scraper process')
					sys.exit()

		print("parsing webpage")
		content = driver.page_source
		soup = bs(content, features="html.parser")
		data = []
		classNames = ['temperature', 'voltage', 'current', 'soc', 'flags', 'motor', 'mppt']
		#This for loop handles parsing the information displayed in the web page
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
		#here we write the parsed data to the database
		client.write_points(data)
		time.sleep(interval)

except KeyboardInterrupt:
	pass

