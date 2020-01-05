echo "PLANTMONITOR_v2 -- SETUP"
echo "Installiere erforderliche Pakete..."
echo "----------------------------------------------------"
sudo apt-get update
sudo apt-get install python-pip -y
sudo apt-get install sqlite3 -y
sudo pip install flask
clear
echo "Erstelle Verzeichnisse und Log-Files..."
echo "----------------------------------------------------"
echo "DATENBANK"
cd
cd /home/pi
sudo mkdir plantmonitor_v2-db
echo "LOG-FILES"
cd
cd /home/pi
sudo mkdir plantmonitor_v2-logs
cd /home/pi/plantmonitor_v2-logs
echo "-" | sudo tee "log_test.txt"
echo "-" | sudo tee "log_data.txt"
echo "-" | sudo tee "log_dataplicity.txt"
echo "-" | sudo tee "log_reboot.txt"
echo "-" | sudo tee "log_restart.txt"
echo "ALARM-FILE"
cd
cd /home/pi
echo "-" | sudo tee "alarm.txt"
echo "----------------------------------------------------"
echo "Erstelle sqlite3 Datenbank..."
echo "----------------------------------------------------"
cd /home/pi/plantmonitor_v2
sudo python create-db.py
echo "----------------------------------------------------"
echo "Erstelle erforderliche Crontab-Liste..."
echo "----------------------------------------------------"
crontab -r
# Periodischer cron Test
(crontab -l 2>/dev/null; echo "*/1	*	*	*	*	sudo python plantmonitor_v2/cron-test.py > plantmonitor_v2-logs/log_test.txt") | crontab -
# Periodische Abfrage Daten
(crontab -l 2>/dev/null; echo "*/5	*	*	*	*	sudo python plantmonitor_v2/data-crawler.py > plantmonitor_v2-logs/log_data.txt") | crontab -
# Restart DP-Agent jeden Tag um 08:01 und 18:01
(crontab -l 2>/dev/null; echo "1	8,18	*	*	*	plantmonitor_v2/restartDP.sh > plantmonitor_v2-logs/log_dataplicity.txt") | crontab -
# Reboot jeden 5. Tag um 09:01
(crontab -l 2>/dev/null; echo "1	9	*/5	*	*	plantmonitor_v2/reboot.sh > plantmonitor_v2-logs/log_reboot.txt") | crontab -
# Nach Reboot starte Webserver Flask um 09:06
(crontab -l 2>/dev/null; echo "6	9	*/5	*	*	plantmonitor_v2/restart.sh > plantmonitor_v2-logs/log_restart.txt") | crontab -
echo "Setup abgeschlossen."
echo "----------------------------------------------------"
#echo "Restart..."
#sudo reboot