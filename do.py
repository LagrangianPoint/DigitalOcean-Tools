#!/usr/bin/python

import os

# Determines if the operating system is debian
def isDebian():
	return  os.path.isfile("/etc/debian_version")


if __name__ == "__main__":
	print "Welcome to Digital Ocean Tools  "

	if isDebian():
		print "You are using debian"
	else:
		print "You are using redhat"
