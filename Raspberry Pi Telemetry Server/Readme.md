# Raspberry Pi Telemetry System Code
This file contains all code related to UTSVT's Telemetry System that runs on a Raspberry Pi 3

# Latests web scraping method instructions:
These instructions will outline how to use the web scraping method to get data from the telemetry nucleo on the solar vehicle. This is the current prefered method to receive the data.

## Quick setup
Go to the SVT Google drive and go to the Bevolt folder in the Telemetry section. Download the `RaspberryPiWebscrapingImage.zip`, extract it, and etch it onto an SD card using [Etcher](https://www.balena.io/etcher/). Now, connect a mouse, keyboawrd, usb wifi dongle, and monitor, and boot the raspberry pi. Once the pi has booted, go to the wifi options in the upper right. If either wlan0 or wlan1 is connected to a network, then disconnect it before proceeding. Now select wlan1, and connect it to the wifi hotspot that the nucleo in the car is broadcasting on. Then go to ```/home/pi/Documents/Telemetry/Raspberry Pi Telemetry Server``` and run the ```startTelemetry.sh``` script by typing ```./startTelemetry.sh```. This should start everything automatically.

To view the data, connect to the wifi hotspot broadcast by the raspberry pi. The network is named TelemetryServer and the password is telemetry. Once connected, open a web browser and type the following in the url bar: "192.168.1.1:3000" (without quotes). The grafana server should come up. If a login is requested, then use admin for both password and username.

## Full setup
To do a full setup, install a fresh rasbian stretch os on an sd card for your raspberry pi. Follow the old instructions below for setting up Grafana, InfluxDB, hostapd, and dnsmasq. Then, just clone this github and run the startTelemetry.sh file. The setup instructions for setting up the grafana graphs is for our old udp system, so you will need to set up the graphs based on the data that is being pulled by the raspberry pi.







# Old UDP streaming instructions
These inscruction are old and may not be up to date. They outline how to set up the nucleo to receive and display data streamed via udp from the telemetry nucleo on the car.

## Running the telemetry system
If you are using the telemtry system that has already been set up then start here

Once everything has been set up properly, all you need to do is run the startTelemetry.sh script. This will automatically start all the required services. Then, plug the telemtry nucleo into the raspberry pi's ethernet port. To view the data, connect to the wifi hotspot broadcast by the raspberry pi. The network is named TelemetryServer and the password is telemetry. Once connected, open a web browser and type the following in the url bar: "192.168.1.1:3000" (without quotes). The grafana server should come up. If a login is requested, then use admin for both password and username. Now, go to dashboards, and manage. Open "test" and you should see a graph of the data. If you do not see any data, try zooming out. 

# Quick Time Set Up
Go to the SVT Google drive and go to the Bevolt folder in the Telemetry section. Download the `Telemetry_Pi_Image.img` and etch it onto an SD card using [Etcher](https://www.balena.io/etcher/).

# Slow Time Set Up
## Installing required software

Software requiered for raspberry pi:
1. grafana
2. influxDB
3. dnsmasq
4. hostapd

### Installing dnsmasq and hostapd:

To set up the raspberry pi to work with this code you need to install dnsmasq and hostapd. Use the following command to download these: 
```
sudo apt install dnsmasq hostapd
```
Next, replace the default config file for dnsmasq ```/etc/dnsmasq.conf``` with the dnsmasq.conf file from this github folder file. Next, replace the file ```/etc/hostapd/hostapd.conf``` with the hostapd.conf file in this github folder. If this file does not exist, just put the hostapd.conf from this github repo into the /etc/hostapd folder. Then, open up ```/etc/default/hostapd``` with a text editor and find the line with DAEMON_CONF and replace it with ```DAEMON_CONF="/etc/hostapd/hostapd.conf"```. Make sure you uncomment the line, i.e. remove the #. Finally you need to unmask and enable hostapd. Run the following commands:
```
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
```


### InfluxDB
Install InfluxDB with these commands:
```
sudo apt install apt-transport-https
echo "deb https://repos.influxdata.com/debian stretch stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
sudo apt-get update && sudo apt-get install influxdb
sudo service influxdb start
```
Use `sudo nano -c /etc/influxdb/influxdb.conf` to edit the Influx configuration file. Scroll down to the [http] section and uncomment these things:
* `enabled: false` and change it to `true`
* `bind-address: ":8086"`
* `auth-enabled = true`

Start Influx with:
```
sudo systemctl enable influxdb
sudo systemctl start influxdb
influx
```
Time to type in a whole lot of Influx terminal commands:
* `CREATE USER admin WITH PASSWORD 'pineapple' WITH ALL PRIVILEGES` - makes admin account
* `CREATE DATABASE test` - creates the test database
* `USE test` - swaps to this database
* `GRANT ALL ON "test" to "admin"` - gives admin all rights
* `CREATE USER grafana WITH PASSWORD 'pineapple'` - grafana needs an account too
* `GRANT READ ON "test" TO "grafana"` - gives only reading access
* `CREATE USER rpi3 WITH PASSWORD 'pineapple' WITH ALL PRIVILAGES` - make user for python client

### Grafana
Install Grafana with these commands:

*make sure that you're downloading the most recent version by checking [their website](https://grafana.com/grafana/download?platform=arm)*
```
wget https://dl.grafana.com/oss/release/grafana-rpi_6.1.4_armhf.deb 
sudo dpkg -i grafana-rpi_6.1.4_armhf.deb 
```
Start Grafana with:
```
sudo service grafana-server start
```
Open up a browser and go to `localhost:3000`. This should pull up the Grafana log in page. The default username and password are both `admin`
For consistency, change the default password of Grafana to `pineapple`

Click "Add a Data Source" and change to these settings:

<img src="https://github.com/crmontminy/solar_car/blob/master/grafana_settings.png" alt="settings" width="70%" height="70%">

Hit test on the bottom, all you should see is just a cute lil green box saying everything is successful

### Scripts

To set up the scripts (startTelemetry-old.sh and telemetryStop.sh) just leave them in this folder. Also, just leave the datagen.py script in this folder.

### Nucleo setup

Finally, you will need to upload the telemetry ode to a nucleo microcontroller that has an ethernet port (we used the Nucleo-F429ZI).

To do this, find the file called ```mbed-os-example-udp-sockets.NUCLEO_F429ZI.bin``` in this gihub project. Next, plug the nucleo board into your computer. It should show up as a device in you file explorer, similar to a usb flash drive. Drag the file mentioned earlier into the nuclue device. Now the nuclueo is programmed!

Plug the ethernet port of the nucleo into the raspberry pi.

### After everything has been installed
Once everything has been set up properly, reboot the Raspberry Pi. Then all you need to do is run the startTelemetry.sh script. This will automatically start all the required services.
```
cd ~/bin
./startTelemetry.sh
```

Now go back to Grafana and create a new dashboard. Follow these settings:

<img src="https://github.com/crmontminy/solar_car/blob/master/grafana-dash.png" alt="dash" width="70%" height="70%">

You should now have a cute lil graph running across your screen <3
