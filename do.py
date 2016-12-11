#!/usr/bin/python

import os

# Determines if the operating system is debian
def isDebian():
	return  os.path.isfile("/etc/debian_version")

def generateVirtualHost(strDomain):
	strTemplate = """
<VirtualHost *:80>
	ServerName %domain%
	DocumentRoot /var/www/html/%domain%

	ErrorLog ${APACHE_LOG_DIR}/error.log
	CustomLog ${APACHE_LOG_DIR}/access.log combined
	<Directory /var/www/html/%domain% >
		RewriteEngine On
		Options FollowSymlinks
		AllowOverride All
		Order allow,deny
		Allow from all
	</Directory>
</VirtualHost>
	"""
	strOut = strTemplate.replace("%domain%", strDomain)
	return strOut

if __name__ == "__main__":
	print "Welcome to Digital Ocean Tools  "

	if isDebian():
		print "You are using debian"
	else:
		print "You are using redhat"

	print generateVirtualHost("mydomain.com")


