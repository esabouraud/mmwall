#!/bin/python

# mmwall launcher
# mmwall currently only works on windows, for wallpaper local and remote setting (uses Win32 API, network drive mount and psexec)

import subprocess
import shutil
import json
import optparse
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
	open(REMOTE_PATH + '\\mmwallcli.bat', 'w').write('python set_wallpaper.py -i %d\npython set_wallpaper_logon.py -i %d -s %s\n' % (idx, idx, (logonscreensize, )))
	
	CMD = 'psexec \\\\%s' % WALLHOST
	if WALLUSER != None and WALLPASS != None:
		CMD += '  -u "%s" -p "%s"' % (WALLUSER, WALLPASS)
	CMD +=' -i -w "C:\\Temp\\.mmwall" "C:\\Temp\\.mmwall\\mmwallcli.bat"'
	subprocess.call(CMD)
	
	CMD = 'net use t: /d'
	if WALLUSER != None and WALLPASS != None:
		CMD += ' /user:"%s" "%s"' % (WALLUSER, WALLPASS)
	subprocess.call(CMD)


def setremotewallgnome(WALLHOST, WALLUSER, WALLPASS, idx, logonscreensize):
	remotesh = open(os.path.join(SRC_PATH, 'mmwallcli.sh'), 'w')
	remoteshlines = []
	remoteshlines.append("rm -rf /tmp/.mmwall.del")
	remoteshlines.append("eval `strings /proc/$(pgrep -u $(whoami) gnome-session)/environ | egrep '(DBUS_SESSION_BUS_ADDRESS|DISPLAY)'`")
	remoteshlines.append("export DBUS_SESSION_BUS_ADDRESS DISPLAY")
	remoteshlines.append("gconftool-2 --set /desktop/gnome/background/picture_filename --type string /tmp/.mmwall/local/wall%d.bmp" % idx)
	remotesh.write("\n".join(remoteshlines))
	remotesh.close()
	
	psftpbatch = open(os.path.join(SRC_PATH, 'mmwallpsftp'),'w')
	psftpbatchlines = []
	psftpbatchlines.append('cd /tmp')
	psftpbatchlines.append('mv .mmwall .mmwall.del')
	psftpbatchlines.append('mkdir .mmwall')
	psftpbatchlines.append('cd .mmwall')
	psftpbatchlines.append('put mmwallcli.sh')
	psftpbatchlines.append('chmod u+x mmwallcli.sh')
	psftpbatchlines.append('put -r current local')
	psftpbatch.write("\n".join(psftpbatchlines))
	psftpbatch.close()
	
	CMD = 'psftp %s -b %s -be' % (WALLHOST, psftpbatch.name)
	if WALLUSER != None and WALLPASS != None:
		CMD += ' -l %s -pw %s' % (WALLUSER, WALLPASS)
	subprocess.check_call(CMD)
	
	puttycmd = open(os.path.join(SRC_PATH, 'mmwallputty'),'w')
	puttycmd.write("/tmp/.mmwall/mmwallcli.sh")
	puttycmd.close()
	
	CMD = 'putty -ssh %s -m %s' % (WALLHOST, puttycmd.name)
	if WALLUSER != None and WALLPASS != None:
		CMD += ' -l %s -pw %s' % (WALLUSER, WALLPASS)
	subprocess.check_call(CMD)


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
			remotelogin = host.get('login')
			remotepw = host.get('password')
			if host.get('remoteos') == None or host.get('remoteos') == 'Windows':
				setremotewallwin(host['remotehost'], remotelogin, remotepw, idx, logonscreensize)
			elif host.get('remoteos') == 'Linux':
				setremotewallgnome(host['remotehost'], remotelogin, remotepw, idx, logonscreensize)
			else:
				print 'Remote host os "%s" unsupported.' % host['remoteos']
		else:
			set_wallpaper.set_wallpaper('current', idx)
			set_wallpaper_logon.set_wallpaper_logon('current', idx, logonscreensize)


if __name__=='__main__':
	parser = optparse.OptionParser(description='mmwall: multi-machine background wallpaper changer')
	parser.add_option('-c', '--configuration', dest='cfgfile', default='mmwallcfg.json', metavar='FILEPATH', help='mmwall configuration file path')
	args = parser.parse_args()

	run_mmwall(args.cfgfile)
