cd
echo "WELCOME TO PLANTMONITOR V2!"
echo "QUICKSTART"
sudo apt-get update
sudo apt-get install git -y
sudo rm -rv plantmonitor_v2
sudo rm -rv plantmonitor_v2-logs
sudo rm -rv plantmonitor_v2-db
sudo rm "alarm.txt"
sudo git clone https://github.com/enzoferrari91/plantmonitor_v2.git
cd plantmonitor_v2
clear
sudo ./setup.sh