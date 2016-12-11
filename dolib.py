#!/usr/bin/python

import os
import shutil
import time
import datetime

# Determines if the operating system is debian
def isDebian():
	return  os.path.isfile("/etc/debian_version")

# Generates a VirtualHost configuration file for apache
def generateVirtualHost(strDomain):
	strTemplate = """
<VirtualHost *:80>
	ServerName %domain%
	DocumentRoot /var/www/%domain%

	ErrorLog ${APACHE_LOG_DIR}/error.log
	CustomLog ${APACHE_LOG_DIR}/access.log combined
	<Directory /var/www/%domain% >
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

# Backups a system file in the config_backups folder
def backupFile(strFile):
	listParts = strFile.split("/")
	strFileName = listParts.pop()
	nTimestamp = int(time.time())
	now = datetime.datetime.now()
	strPrefix = str(now.year) + str(now.month) + str(now.day)
	strNewFile = "config_backups/" + strFileName + "." + strPrefix + "_" + str(nTimestamp)

	shutil.copy(strFile, strNewFile)	


# Replaces a system files, but keeps a backup of it automatically
def replaceFile(strOldFile, strNewFile):
	backupFile(strOldFile)
	shutil.copy(strNewFile, strOldFile)

# Restarts MySQL
def restart_mysql():
	os.system("sudo /etc/init.d/mysql restart")

# Restarts Apache
def restart_apache():
	os.system("sudo sudo /etc/init.d/apache2 restart")

# Adds a new domain/subdomain, enables it, and restarts apache
def add_domain(strDomain):
	strVirtualHost = generateVirtualHost(strDomain)
	strFile = "/etc/apache2/sites-available/" + strDomain + ".conf"
	strFileSymlink = "/etc/apache2/sites-enabled/" + strDomain + ".conf"

	# Creating project directory
	strProjectDir = "/var/www/%s" % (strDomain)
	if not os.path.exists(strProjectDir):
		os.makedirs(strProjectDir)

	print ">>> " + strFile
	if os.path.isfile(strFile):
		return False
	else:
		fh = open(strFile, 'w' )
		fh.write(strVirtualHost)
		fh.close()
		os.symlink(strFile, strFileSymlink)
		restart_apache()

# Automatically configs MySQL in one of three modes
# low :  Low resource VM
# mid : mid resource VM  - TODO
# high : high resource VM  - TODO
def config_mysql(mode):
	if mode in ['low', 'mid', 'high']:
		strFile = "my.cnf." + mode
		strTarget = "/etc/mysql/mysql.conf.d/mysqld.cnf"
		replaceFile(strTarget, strFile)
		restart_mysql()		
	else:
		return False

# /etc/mysql/mysql.conf.d/mysqld.cnf


