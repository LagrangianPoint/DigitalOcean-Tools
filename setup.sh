#!/bin/bash

echo "Welcome to DigitalOcean-Tools!"

if [ -f "/etc/debian_version" ];
  debian=1
else
  debian=0
fi

