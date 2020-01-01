echo "Install..."

apt-get update
apt-get install git -y
apt-get install python-pip -y
apt-get install sqlite3 -y

pip install flask

echo "Arduino IDE..."
apt-get install picocom -y
apt-get install arduino-core arduino-mk -y

sudo usermod -a -G dialout pi

echo "Erstelle Verzeichnisse und Log-Files..."

echo "PLANTMONITOR-VERZEICHNIS:"
cd
cd /home/pi
mkdir plantmonitor

echo "DATENBANK-VERZEICHNIS:"
cd
cd /home/pi
mkdir plantmonitor-db

echo "LOG-FILES:"
cd
cd /home/pi
mkdir plantmonitor-logs
cd /home/pi/plantmonitor-logs
echo "-" > "log_data.txt"

echo "ALARM-FILE:"
cd
cd /home/pi
echo "-" > "alarm.txt"

cd /home/pi

echo "Restart..."
sudo reboot