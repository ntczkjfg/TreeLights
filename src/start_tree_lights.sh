#!/bin/bash
export DISPLAY=:0
while ! xset q &>/dev/null; do
	sleep 1
done
cd /home/pi/Desktop/TreeLights/src/
lxterminal -e "sudo /usr/bin/python3 /home/pi/Desktop/TreeLights/src/Effect_Control.py"
