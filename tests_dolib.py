
import unittest
import dolib
import glob
import os
import shutil

# DoLib module tests 
class DoLibTests(unittest.TestCase):
	
	# Checks if backupFile() works
	def test_backupFile(self):
		if os.path.exists("config_backups"):
			os.rename("config_backups", "config_backups_original")
		os.makedirs("config_backups")
		dolib.backupFile("/etc/issue")
		listFiles = glob.glob("config_backups/issue*")
		bResult =  len(listFiles) > 0
		shutil.rmtree("config_backups")
		os.rename("config_backups_original", "config_backups")
		self.assertEqual(bResult , True, " There should be a copy of /etc/issue in config_backups/")
	

		
	


unittest.main()

