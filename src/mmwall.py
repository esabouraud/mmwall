#!/bin/python


import subprocess
import shutil
import ConfigParser
import re
import argparse

import set_wallpaper
import set_wallpaper_logon
import synergy_wallpaper
import randomdownload_wallpaper


REMOTE_PATH = 't:\\.mmwall'


def setremotewall(WALLHOST, WALLUSER, WALLPASS, idx, logonscreensize):
	CMD = 'net use t: \\\\%s\\C$\\Temp' % WALLHOST
	if WALLUSER != None and WALLPASS != None:
		CMD += ' /user:"%s" "%s"' % (WALLUSER, WALLPASS)
	subprocess.call(CMD)
	shutil.rmtree(REMOTE_PATH, True)
	shutil.copytree('current', REMOTE_PATH + '\\local')
	shutil.copy('set_wallpaper.py', REMOTE_PATH)
	shutil.copy('set_wallpaper_logon.py', REMOTE_PATH)
	open(REMOTE_PATH + '\\wallcli.bat', 'w').write('python set_wallpaper.py -i %d\npython set_wallpaper_logon.py -i %d -s %s\n' % (idx, idx, (logonscreensize, )))
	
	CMD = 'psexec \\\\%s' % WALLHOST
	if WALLUSER != None and WALLPASS != None:
		CMD += '  -u "%s" -p "%s"' % (WALLUSER, WALLPASS)
	CMD +=' -i -w "C:\\Temp\\.mmwall" "C:\\Temp\\.mmwall\\wallcli.bat"'
	subprocess.call(CMD)
	
	CMD = 'net use t: /d'
	if WALLUSER != None and WALLPASS != None:
		CMD += ' /user:"%s" "%s"' % (WALLUSER, WALLPASS)
	subprocess.call(CMD)


def run_mmwall(cfgfile):
	config = ConfigParser.ConfigParser()
	config.read(cfgfile)
	screenratio = config.getfloat('general', 'screenratio')
	print screenratio

	screenconf = []
	for sec in config.sections():
		matchsec = re.match('^host-(\d+)$', sec)
		if matchsec != None:
			idx = int(matchsec.group(1))
			screenconf.append((config.getint(sec, 'screenwidth'), config.getint(sec, 'screenheight'), config.getint(sec, 'screenvoffset'), idx))	
	print screenconf
	
	randomdownload_wallpaper.get_wallpaper(True, screenratio)
	synergy_wallpaper.make_wallpapers(True, screenconf)
	
	for sec in config.sections():
		matchsec = re.match('^host-(\d+)$', sec)
		if matchsec != None:
			idx = int(matchsec.group(1))
			
			if config.has_option(sec, 'logonscreenwidth') and config.has_option(sec, 'logonscreenheight'):
				logonscreensize = (config.getint(sec, 'logonscreenwidth'), config.getint(sec, 'logonscreenheight'))
			else:
				logonscreensize = (config.getint(sec, 'screenwidth'), config.getint(sec, 'screenheight'))
			
			if config.has_option(sec, 'remotehost'):
				setremotewall(config.get(sec, 'remotehost'), None, None, idx, logonscreensize)
			else:
				set_wallpaper.set_wallpaper('current', idx)
				set_wallpaper_logon.set_wallpaper_logon('current', idx, logonscreensize)

if __name__=='__main__':
	parser = argparse.ArgumentParser(description='mmwall: multi-machine background wallpaper changer')
	parser.add_argument('-c', '--configuration', dest='cfgfile', default='mmwall.cfg', metavar='FILEPATH', help='mmwall configuration file path')
	args = parser.parse_args()

	run_mmwall(args.cfgfile)
