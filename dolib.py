#!/usr/bin/python

import os
import shutil
import time
import datetime
import MySQLdb



# Determines if the operating system is debian
def isDebian():
	return  os.path.isfile("/etc/debian_version")

# Generates a VirtualHost configuration file for apache
def generateVirtualHost(strDomain):
	strTemplate = """
<VirtualHost *:80>
	ServerName %domain%
	ServerAlias www.%domain%
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
	#os.system("sudo /etc/init.d/mysql restart")
	os.system("sudo /usr/sbin/service mysql restart")

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

# Allows all folders inside a folder to have 777 permissions to enable file uploading
def enable_folder_writing(strPath):
	os.chmod(strPath, 0o777)
	for dirpath, dirnames, filenames in os.walk(strPath):
		for strDir in dirnames:  
			path = os.path.join(dirpath, strDir)
			os.chmod(path, 0o777) # for example

# Updates and removes old Wordpress versions  
def upgrade_wp_plugins(strPath):
	strOriginalDir = os.getcwd()
	os.chdir(strPath)
	for dirpath, dirnames, filenames in os.walk(strPath):
		for strDir in dirnames:
			strGetPluginFile = "https://downloads.wordpress.org/plugin/%s.zip" % (strDir)
			listParts = strGetPluginFile.split("/")
			strFileName = listParts.pop()
			os.system("wget " + strGetPluginFile)
			if os.path.isfile(strFileName):
				shutil.rmtree(strDir)
				os.system(  "unzip " + strFileName  )
				os.remove(strFileName)
			else:
				print " * Unable to update: " + strDir + " .... File " + strFileName +  " does not exists" 
		break
	os.chdir(strOriginalDir)

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

class DBMysql(object):
	# Initializes database with root information
	def __init__(self, host, username, password):
		self.host = host
		self.root_username = username
		self.root_password = password
		#self.cnx = mysql.connector.connect(host=host, user=username, password=password)
		self.db = MySQLdb.connect(host, username, password)
		self.cursor = self.db.cursor()

	# Selects database
	def selectDb(self, strDBName):
		self.db.select_db(strDBName)
	
	# Creates a new database 
	def create_db(self, strDBName):
		self.cursor.execute("CREATE DATABASE IF NOT EXISTS %s" % (strDBName))
		self.db.commit()

	# Adds a new user to a specified database
	def add_user(self, database, username, password, host='localhost'):
		self.cursor.execute("CREATE USER '%s'@'%s' IDENTIFIED BY '%s'" % (username, host,password))
		self.cursor.execute("GRANT ALL PRIVILEGES ON %s . * TO '%s'@'%s'" % (database, username, host))
		self.cursor.execute("FLUSH PRIVILEGES")
		self.db.commit()


	# Loads a database within database_dumps folder using mysql client.
	def load_db(self, database, dumpfile):
		strCommand = "mysql -h%s -u%s -p'%s' %s < database_dumps/%s" % (self.host, self.root_username, self.root_password, database, dumpfile)
		os.system(strCommand)





