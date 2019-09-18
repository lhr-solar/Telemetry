# Telemetry Demo
This program / instructions make a simple system for presenting dummy speed data. Basically a proof of concept for the InfluxDB and Grafana combo c:

---
## First Time Set Up 
*assuming you're starting with a brand new raspberry pi, if not just skip this*
* Download a copy of Raspbian Stretch from [their website](https://www.raspberrypi.org/downloads/raspbian/)
* Throw it onto your SD card with [Etcher](https://www.balena.io/etcher/)
* Connect your peripherals to the Pi and power it up
* If you want, you can clear out some bloatware with [these commands](https://github.com/raspberrycoulis/remove-bloat/blob/master/remove-bloat.sh):
```
sudo apt-get remove --purge wolfram-engine libreoffice* scratch* minecraft-pi sonic-pi dillo gpicview oracle-java8-jdk openjdk-7-jre oracle-java7-jdk openjdk-8-jre -y
sudo apt-get autoremove -y
sudo apt-get autoclean -y
sudo apt-get update
```

**Also ensure that your Pi is on UTC time.** Influx runs on UTC for standardizing reasons, but if your Pi is in a different timezone your data will be logged at random hours

## Installing and Configuring Software
### InfluxDB
Install InfluxDB with these commands:
```
sudo apt install apt-transport-https
echo "deb https://repos.influxdata.com/debian jessie stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
sudo apt update
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
* `CREATE DATABASE test` - creates the test database
* `USE test` - swaps to this database
* `CREATE USER "admin" WITH PASSWORD "pineapple"` - makes admin account
* `GRANT ALL ON "test" to "admin"` - gives admin all rights
* `CREATE USER "grafana" WITH PASSWORD "tape"` - grafana needs an account too
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

Click "Add a Data Source" and change to these settings:

<img src="https://github.com/crmontminy/solar_car/blob/master/grafana_settings.png" alt="settings" width="70%" height="70%">

Hit test on the bottom, all you should see is just a cute lil green box saying everything is successful

### Running the Program
Download the `datagen.py` program to your favorite folder and navigate to it in your terminal. Run the command `python datagen.py` to get him going. You should see a time stamp with random numbers populate the terminal, along with sent confirmations

Go back to Grafana and create a new dashboard. Follow these settings:

<img src="https://github.com/crmontminy/solar_car/blob/master/grafana-dash.png" alt="dash" width="70%" height="70%">

You should now have a cute lil graph running across your screen <3
