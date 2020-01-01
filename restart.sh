#!/bin/bash

echo "Starte Flask Webserver..."

cd /home/pi/plantmonitor_v2

nohup sudo python app.py >/dev/null 2>&1 &

echo "Fertig:  $(date)"
