# Raspberry Pi Telemetry System Code
This file contains all code related to UTSVT's Telemetry System that runs on a raspberry pi

## Running the telemetry system
If you are using the telemtry system that has already been set up then start here

Once everything has been set up properly, all you need to do is run the startTelemetry.sh script. This will automatically start all the required services. Then, plug the telemtry nucleo into the raspberry pi's ethernet port. To view the data, connect to the wifi hotspot broadcast by the raspberry pi. The network is named TelemetryServer and the password is telemetry. Once connected, open a web browser and type the following in the url bar: "192.168.1.1:3000" (without quotes). The grafana server should come up. If a login is requested, then use admin for both password and username. Now, go to dashboards, and manage. Open "test" and you should see a graph of the data. If you do not see any data, try zooming out. 

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
Next, replace the default config file for dnsmasq ```/etc/dnsmasq.conf``` with the dnsmasq.conf file from this github folder file. Next, replace the file ```/etc/hostapd/hostapd.conf``` with the hostapd.conf file in this github folder. If this file does not exist, just put the hostapd.conf from this github repo into the /etc/hostapd folder. Then, open up ```/etc/default/hostapd``` with a text editor and find the line with DAEMON_CONF and replace it with ```DAEMON_CONF="/etc/hostapd/hostapd.conf"```. Make sure you uncomment the line, i.e. remove the #.


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

To set up the scripts (startTelemetry.sh and telemetryStop.sh) in this folder, place them in ```~/bin``` on the raspberry pi (you may need to create a bin directory). Also, place the datagen.py script in ```~/Documents``` on the raspberry pi.

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
