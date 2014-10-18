#!/bin/python

from optparse import OptionParser
import os
import ctypes

LOCALDIR = "local"
FILEPATTERN = "wall%d.bmp"

# set windows background
def set_wallpaper(walldir, screenid):
	filepath = os.path.join(walldir, FILEPATTERN % int(screenid))
	print "Setting wallpaper %s" % filepath
	SPI_SETDESKWALLPAPER = 20 
	ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, filepath , 0)

if __name__=='__main__':
	parser = OptionParser()
	parser.add_option("-i", "--screen-id", dest="screenid", default="0", help="Id of screen in screen list")
	parser.add_option("-d", "--wallpaper-directory", dest="walldir", default=LOCALDIR, help="Path of directory where wallpaper shall be found")
	
	(options, args) = parser.parse_args()
	set_wallpaper(options.walldir, options.screenid)
