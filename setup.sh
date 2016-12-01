#!/bin/bash

echo "Welcome to DigitalOcean-Tools!"

if [ -f "/etc/debian_version" ];
  debian=1
else
  debian=0
fi

if [ $debian -eq 1 ]
then

sudo apt-get update
sudo apt-get install git
sudo apt-get install python

fi
