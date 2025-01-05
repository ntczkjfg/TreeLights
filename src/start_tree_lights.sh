#!/bin/bash
export DISPLAY=:0
while ! xset q &>/dev/null; do
	sleep 1
done
cd /home/user/Desktop/TreeLights/src/
lxterminal -e "sudo /usr/bin/python3 /home/user/Desktop/TreeLights/src/effect_control.py"
