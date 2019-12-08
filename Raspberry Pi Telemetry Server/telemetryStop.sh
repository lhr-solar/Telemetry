sudo service grafana-server stop
echo "stopped grafana server"
sudo service dnsmasq stop
echo "stopped dnsmasq"
sudo service hostapd stop
echo "stopped hostapd"
sudo pkill "python"
echo "stopped python web scraper"
sudo killall -SIGKILL influx
echo "stopped influxdb"
