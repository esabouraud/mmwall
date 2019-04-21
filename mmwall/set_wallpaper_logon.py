#!/bin/python

from optparse import OptionParser
import os
import ast
import sys
import platform
from PIL import Image

LOCALDIR = "local"
FILEPATTERN = "wall%d.bmp"
CURRENT_SYSTEM = platform.system()

def set_wallpaper_logon_windows(walldir, screenid, size):
	if sys.getwindowsversion().major < 6:
		return

	# Check HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Authentication\LogonUI\Background\OEMBackground == 1
	inputimagepath = os.path.abspath(os.path.join(walldir, FILEPATTERN % int(screenid)))
	print "Setting wallpaper logon from %s" % inputimagepath
	im = Image.open(inputimagepath)
	bg = im.crop((0, 0, size[0], size[1]))
	LOGONBG_DIR = os.path.expandvars("%WinDir%\\Sysnative\\oobe\\Info\\backgrounds")
	if (os.path.exists(LOGONBG_DIR) == False):
		os.makedirs(LOGONBG_DIR)
	bg.save(LOGONBG_DIR + "\\backgroundDefault.jpg", "JPEG", quality=75)

def set_wallpaper_logon(walldir, screenid, size):
	if CURRENT_SYSTEM == "Windows":
		set_wallpaper_logon_windows(walldir, screenid, size)
	else:
		print "Setting logon wallpaper on platform %s is not supported." % CURRENT_SYSTEM


if __name__=='__main__':
	parser = OptionParser()
	parser.add_option("-i", "--screen-id", dest="screenid", default="0", help="Id of screen in screen list")
	parser.add_option("-s", "--screen-size", dest="size", default="(1280, 1024)", help="Size of screen for single screen wallpaper")
	parser.add_option("-d", "--wallpaper-directory", dest="walldir", default=LOCALDIR, help="Path of directory where wallpaper shall be found")
	
	(options, args) = parser.parse_args()
	set_wallpaper_logon(options.walldir, options.screenid, ast.literal_eval(options.size))
