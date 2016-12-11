#!/bin/bash

echo "Welcome to DigitalOcean-Tools!"

if [ -f "/etc/debian_version" ]
then
  debian=1
else
  debian=0
fi

wget https://raw.githubusercontent.com/LagrangianPoint/DigitalOcean-Tools/master/do.py
chmod +x do.py

if [ $debian -eq 1 ]
then

	# Installing Git and Python for using do.py
	sudo apt-get update
	sudo apt-get install git
	sudo apt-get install python
	sudo apt-get install python-mysqldb

	# Installing LAMP stack
	sudo apt-get install php libapache2-mod-php
	sudo apt-get install mysql-server
	sudo apt-get install apache2
	sudo a2enmod rewrite
	sudo /etc/init.d/apache2 restart


else
	# Installing Git and Python for using do.py
	sudo yum install git
	sudo yum install python
fi


