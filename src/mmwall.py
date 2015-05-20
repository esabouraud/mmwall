#!/bin/python

# mmwall launcher
# mmwall currently only works on windows, for wallpaper local and remote setting (uses Win32 API, network drive mount and psexec)

import subprocess
import shutil
import json
import argparse
import os

import set_wallpaper
import set_wallpaper_logon
import synergy_wallpaper
import randomdownload_wallpaper


REMOTE_PATH = 't:\\.mmwall'
SRC_PATH = os.path.dirname(os.path.abspath(__file__))


def setremotewallwin(WALLHOST, WALLUSER, WALLPASS, idx, logonscreensize):
	CMD = 'net use t: \\\\%s\\C$\\Temp' % WALLHOST
	if WALLUSER != None and WALLPASS != None:
		CMD += ' /user:"%s" "%s"' % (WALLUSER, WALLPASS)
	subprocess.call(CMD)
	shutil.rmtree(REMOTE_PATH, True)
	shutil.copytree('current', REMOTE_PATH + '\\local')
	shutil.copy(os.path.join(SRC_PATH, 'set_wallpaper.py'), REMOTE_PATH)
	shutil.copy(os.path.join(SRC_PATH, 'set_wallpaper_logon.py'), REMOTE_PATH)
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
	cfg = json.load(open(cfgfile))
	screenratio = cfg['general']['screenratio']
	imgsrc = cfg['general'].get('imgsrc')
	#print screenratio

	screenconf = []
	for host in cfg['hosts']:
		idx = host['id']
		for screen in host['screens']:
			screenconf.append((screen['screenwidth'], screen['screenheight'], screen['screenvoffset'], idx))	
	#print screenconf
	
	randomdownload_wallpaper.get_wallpaper(True, screenratio, imgsrc)
	synergy_wallpaper.make_wallpapers(True, screenconf)
	
	for host in cfg['hosts']:
		idx = host['id']
		if host.get('logonscreenwidth') and host.get('logonscreenheight'):
			logonscreensize = (host['logonscreenwidth'], host['logonscreenheight'])
		else:
			logonscreensize = (host['screens'][0]['screenwidth'], host['screens'][0]['screenheight'])
		
		if host.get('remotehost'):
			if host.get('remoteos') == None or host.get('remoteos') == 'Windows':
				setremotewallwin(host['remotehost'], None, None, idx, logonscreensize)
			else:
				print 'Remote host os "%s" unsupported.' % host['remoteos']
		else:
			set_wallpaper.set_wallpaper('current', idx)
			set_wallpaper_logon.set_wallpaper_logon('current', idx, logonscreensize)


if __name__=='__main__':
	parser = argparse.ArgumentParser(description='mmwall: multi-machine background wallpaper changer')
	parser.add_argument('-c', '--configuration', dest='cfgfile', default='mmwallcfg.json', metavar='FILEPATH', help='mmwall configuration file path')
	args = parser.parse_args()

	run_mmwall(args.cfgfile)
