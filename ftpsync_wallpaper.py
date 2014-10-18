#!/bin/python

from optparse import OptionParser
from ftplib import FTP
import os

CURRENTDIR = "current"
LOCALDIR = "local"
REMOTEDIR = "wall"
FILEPATTERN = "wall%d.bmp"

	
def ftp_transfer(host, serve, screenid):
	if (False == os.path.isdir(LOCALDIR)):
		os.makedirs(LOCALDIR)
		
	ftp = FTP(host)
	ftp.login()
	ftp.cwd(REMOTEDIR)
	print ftp.retrlines('LIST')
	if (serve == True):
		print "Serving wallpapers..."
		for filename in os.listdir(CURRENTDIR):
			print "Put %s on FTP %s" % (filename, host)
			f = open(os.path.join(CURRENTDIR, filename), "rb")
			ftp.storbinary("STOR %s" % filename, f)
			f.close()
	else:
		print "Getting wallpaper..."
		filename = os.path.join(LOCALDIR, FILEPATTERN % int(screenid))
		print "get %s from FTP %s" % (filename, host)
		f = open(filename, 'wb')
		ftp.retrbinary("RETR %s" % os.path.basename(filename), f.write)
		f.close()
	ftp.quit()


if __name__=='__main__':
	parser = OptionParser()
	parser.add_option("-i", "--screen-id", dest="screenid", default="0", help="Id of screen in screen list")
	parser.add_option("-s", "--serve-wallpaper", dest="serve", action="store_true", default=False, help="Upload wallpapers if set, else download proper one")
	parser.add_option("-H", "--hostname", dest="host", default="localhost", help="Server URL & credentials")
	
	(options, args) = parser.parse_args()
	ftp_transfer(options.host, options.serve, options.screenid)
