#!/bin/python

from optparse import OptionParser
from ftplib import FTP
import os
import ctypes


CURRENTDIR = "current"
LOCALDIR = "local"
REMOTEDIR = "wall"
FILEPATTERN = "wall%d.bmp"

# set windows background
def set_wallpaper(filepath):
	print "Setting wallpaper %s" % filepath
	SPI_SETDESKWALLPAPER = 20 
	ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, filepath , 0)

	
def ftp_transfer(options):
	ftp = FTP(options.host)
	ftp.login()
	ftp.cwd(REMOTEDIR)
	print ftp.retrlines('LIST')
	if (options.serve == True):
		print "Serving wallpapers..."
		for filename in os.listdir(CURRENTDIR):
			print "Put %s on FTP %s" % (filename, options.host)
			f = open(os.path.join(CURRENTDIR, filename), "rb")
			ftp.storbinary("STOR %s" % filename, f)
			f.close()
	else:
		print "Getting wallpaper..."
		filename = os.path.join(LOCALDIR, FILEPATTERN % int(options.screenid))
		print "get %s from FTP %s" % (filename, options.host)
		f = open(filename, 'wb')
		ftp.retrbinary("RETR %s" % os.path.basename(filename), f.write)
		f.close()
	ftp.quit()

if __name__=='__main__':
	parser = OptionParser()
	parser.add_option("-i", "--screen-id", dest="screenid", default="0", help="Id of screen in screen list")
	parser.add_option("-s", "--serve-wallpaper", dest="serve", action="store_true", default=False, help="Upload wallpapers if set, else download proper one")
	parser.add_option("-H", "--hostname", dest="host", default="localhost", help="Server URL & credentials")
	parser.add_option("-D", "--dry-run", dest="dry", action="store_true", default=False, help="Do not set wallpaper, just download/upload it")
	
	(options, args) = parser.parse_args()
	
	if (False == os.path.isdir(LOCALDIR)):
		os.makedirs(LOCALDIR)
		
	ftp_transfer(options)
	
	if (options.dry == False):
		if (options.serve == True):
			set_wallpaper(os.path.join(CURRENTDIR, FILEPATTERN % int(options.screenid)))
		else:
			set_wallpaper(os.path.join(LOCALDIR, FILEPATTERN % int(options.screenid)))
