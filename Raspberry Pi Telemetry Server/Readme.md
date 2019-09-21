# Raspberry Pi Telemetry System Code
This file contains all code related to UTSVT's Telemetry System that runs on a raspberry pi

## Running the telemetry system
If you are using the telemtry system that has already been set up then start here

Once everything has been set up properly, all you need to do is run the startTelemetry.sh script. This will automatically start all the required services. Then, plug the telemtry nucleo into the raspberry pi's ethernet port. To view the data, connect to the wifi hotspot broadcast by the raspberry pi. The network is named TelemetryServer and the password is telemetry. Once connected, open a web browser and type the following in the url bar: "192.168.1.1:3000" (without quotes). The grafana server should come up. If a login is requested, then use admin for both password and username. Now, go to dashboards, and manage. Open "test" and you should see a graph of the data. If you do not see any data, try zooming out. 

## Installing required software
To set up the raspberry pi to work with this code you need to install dnsmasq and hostapd. Use the following command to download these: sudo apt install dnsmasq hostapd. Next, replace the default config file for dnsmasq (located in /etc/dnsmasq/conf) with the dnsmasq.conf file in this file. Next, replace the file /etc/hostapd/hostapd.conf with the hostapd.conf file in this file. Then, open up /etc/default/hostapd with a text editor and file the line with DAEMON_CONF and replace it with DAEMON_CONF="/etc/hostapd/hostapd.conf".

You will also need to install Grafana and Influxdb for this project to work.

To set up the scripts (startTelemetry.sh and telemetryStop.sh) in this folder, place them in ~/bin on the raspberry pi (you may need to create a bin directory). Also, place the datagen.py script in ~/Documents on the raspberry pi.

Finally, you will need to compile the code in the mbed-os file using the online mbed compiler. Then upload this code to a nucleo microcontroll that has an ethernet port (we used the Nucleo-F429ZI). Now connect the nucleo to the raspberry pi using an ethernet cable