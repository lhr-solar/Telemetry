echo "Enter Date and time, ex: Sep 20 15:45:00"
read dateTime
tokens=( $dateTime )
IFS=':' times=( ${tokens[2]} )
timeUpdate=$((${times[0]} + 5))
times[0]=$(($timeUpdate % 24))
IFS=' '
dateTime="${tokens[0]} ${tokens[1]} ${times[0]}:${times[1]}:${times[2]}"
sudo date -s "$dateTime"
echo "Date and time are set ahead 5 hours so that UTC time aligns with central standard time"
sudo service hostapd stop
sudo ifconfig wlan0 down
echo "Stopped hostadp and shutdown wlan0"
sleep 5
sudo ifconfig wlan0 192.168.1.1 up
sudo ifconfig eth0 192.168.4.2 up
echo "Restarted wlan0"
sudo service dnsmasq start
echo "Launched dnsmasq"
sudo service hostapd start
echo "Launched hostapd"
sudo service grafana-server start
echo "Launched grafana-server"
lxterminal -e influx
echo "Launched influx server"
lxterminal -e python ~/Documents/datagen.py
echo "Launched python upd socket"
echo "Settings files are located in /etc/dnsmasq.conf and /etc/hostapd/hostapd.conf"

