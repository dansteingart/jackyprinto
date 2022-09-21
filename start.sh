EPORT=$(/bin/bash find_usb.sh | grep USB_S | awk '{split($0,a,":"); print a[2]}')
/home/pi/.nvm/versions/node/v16.17.0/bin/node server.js 3000 $EPORT 115200 10000 9001

