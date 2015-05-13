#!/bin/python

import subprocess
import shutil
import os

import set_wallpaper
import set_wallpaper_logon
import synergy_wallpaper
import randomdownload_wallpaper

REMOTE_PATH = 't:\\.mmwall'

if __name__=='__main__':
	print 'mmwall: multi-machine background wallpaper changer'
	
	WALLHOST = os.getenv('WALLHOST')
	WALLUSER = os.getenv('WALLUSER')
	WALLPASS = os.getenv('WALLPASS')
	
	#print 'remote host:%s\nremote host user: %s' % (WALLHOST, WALLUSER)
	
	randomdownload_wallpaper.get_wallpaper(True, 2.0)
	synergy_wallpaper.make_wallpapers(True, [(1280, 1024, 0, 0), (2560, 1024, 0, 1)])
	
	set_wallpaper.set_wallpaper('current', 1)
	set_wallpaper_logon.set_wallpaper_logon('current', 1, (1280, 1024))
	
	CMD = 'net use t: \\\\%s\\C$\\Temp' % WALLHOST
	if WALLUSER != None and WALLPASS != None:
		CMD += ' /user:"%s" "%s"' % (WALLUSER, WALLPASS)
	subprocess.call(CMD)
	shutil.rmtree(REMOTE_PATH, True)
	shutil.copytree('current', REMOTE_PATH + '\\local')
	shutil.copy('set_wallpaper.py', REMOTE_PATH)
	open(REMOTE_PATH + '\\wallcli.bat', 'w').write('python set_wallpaper.py -i 0\n')
	
	CMD = 'psexec \\\\%s' % WALLHOST
	if WALLUSER != None and WALLPASS != None:
		CMD += '  -u "%s" -p "%s"' % (WALLUSER, WALLPASS)
	CMD +=' -i -w "C:\\Temp\\.mmwall" "C:\\Temp\\.mmwall\\wallcli.bat"'
	subprocess.call(CMD)
	
	CMD = 'net use t: /d'
	if WALLUSER != None and WALLPASS != None:
		CMD += ' /user:"%s" "%s"' % (WALLUSER, WALLPASS)
	subprocess.call(CMD)
