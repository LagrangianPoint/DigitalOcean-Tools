#!/usr/bin/python

from dolib import *

listOptions = ['domains add']

if __name__ == "__main__":
	print "Welcome to Digital Ocean Tools  "

	if isDebian():
		print "You are using debian"
	else:
		print "You are using redhat"

	print generateVirtualHost("mydomain.com")

	backupFile("/etc/mysql/mysql.conf.d/mysqld.cnf")

