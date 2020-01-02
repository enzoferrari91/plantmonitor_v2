echo "PLANTMONITOR_v2"
echo "Installiere erforderliche Pakete..."
echo "----------------------------------------------------"
sudo apt-get update
sudo apt-get install python-pip -y
sudo apt-get install sqlite3 -y
sudo pip install flask
echo "Erstelle Verzeichnisse und Log-Files..."
echo "----------------------------------------------------"
echo "DATENBANK"
cd
cd /home/pi
mkdir plantmonitor_v2-db
echo "LOG-FILES"
cd
cd /home/pi
mkdir plantmonitor_v2-logs
cd /home/pi/plantmonitor_v2-logs
echo "-" > "log_test.txt"
echo "-" > "log_data.txt"
echo "-" > "log_dataplicity.txt"
echo "-" > "log_reboot.txt"
echo "-" > "log_restart.txt"

echo "ALARM-FILE"
cd
cd /home/pi
echo "-" > "alarm.txt"
echo "----------------------------------------------------"
echo "Erstelle sqlite3 Datenbank..."
echo "----------------------------------------------------"
cd /home/pi/plantmonitor_v2
sudo python create-db.py
echo "----------------------------------------------------"
echo "Erstelle erforderliche Crontab-Liste..."
echo "----------------------------------------------------"
# write out current crontab
crontab -l > mycron
# echo new cron into cron file
# Periodischer cron Test
echo "*/1	*	*	*	*	sudo python plantmonitor_v2/cron-test.py > plantmonitor_v2-logs/log_test.txt" >> mycron
# Periodische Abfrage Daten
echo "*/5	*	*	*	*	sudo python plantmonitor_v2/data-crawler.py > plantmonitor_v2-logs/log_data.txt" >> mycron
# Restart DP-Agent jeden Tag um 08:01 und 18:01
echo "1	8,18	*	*	*	plantmonitor_v2/restartDP.sh > plantmonitor_v2-logs/log_dataplicity.txt" >> mycron
# Reboot jeden 5. Tag um 09:01
echo "1	9	*/5	*	*	plantmonitor_v2/reboot.sh > plantmonitor_v2-logs/log_reboot.txt" >> mycron
# Nach Reboot starte Webserver Flask um 09:06
echo "6	9	*/5	*	*	plantmonitor_v2/restart.sh > plantmonitor_v2-logs/log_restart.txt" >> mycron
#install new cron file
crontab mycron
rm mycron
echo "----------------------------------------------------"
echo "Restart..."
sudo reboot