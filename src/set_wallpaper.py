#!/bin/python

from optparse import OptionParser
import os
import platform
import ctypes
import subprocess

LOCALDIR = "local"
FILEPATTERN = "wall%d.bmp"
SRC_PATH = os.path.dirname(os.path.abspath(__file__))
CURRENT_SYSTEM = platform.system()

# set Linux (CentOS6 with gnome) background
def set_wallpaper_linux(walldir, screenid):
	subprocess.call(['gconftool-2', '--set', '/desktop/gnome/background/picture_filename', '--type', 'string',  '%s/wall%d.bmp' % (os.path.abspath(walldir), screenid)])

# set Windows (>= XP) background
def set_wallpaper_windows(walldir, screenid):
	filepath = os.path.abspath(os.path.join(walldir, FILEPATTERN % int(screenid)))
	print "Setting wallpaper %s" % filepath
	SPI_SETDESKWALLPAPER = 0x0014
	SPI_GETDESKWALLPAPER = 0x0073
	SPIF_UPDATEINIFILE = 0x01
	SPIF_SENDWININICHANGE = 0x02
	
	s = ctypes.create_string_buffer(512)
	ctypes.windll.user32.SystemParametersInfoA(SPI_GETDESKWALLPAPER, 512, s, 0)
	print s.raw
	
	ret = ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, filepath, SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE)
	if ret == 0:
		error = ctypes.WinError()
		print 'SystemParametersInfoA error=%s' % (ret, error)

def set_wallpaper(walldir, screenid):
	if CURRENT_SYSTEM == "Windows":
		set_wallpaper_windows(walldir, screenid)
	elif CURRENT_SYSTEM == "Linux":
		set_wallpaper_linux(walldir, screenid)
	else:
		print "Platform %s is not supported, wallpaper not set." % CURRENT_SYSTEM

if __name__=='__main__':
	parser = OptionParser()
	parser.add_option("-i", "--screen-id", dest="screenid", default="0", help="Id of screen in screen list")
	parser.add_option("-d", "--wallpaper-directory", dest="walldir", default=LOCALDIR, help="Path of directory where wallpaper shall be found")
	
	(options, args) = parser.parse_args()
	set_wallpaper(options.walldir, options.screenid)
