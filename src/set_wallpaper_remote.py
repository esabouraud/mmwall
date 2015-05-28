#!/bin/python


import subprocess
import shutil
import optparse
import os
import platform

import set_wallpaper

REMOTE_PATH = 't:\\.mmwall'
SRC_PATH = os.path.dirname(os.path.abspath(__file__))
CURRENT_SYSTEM = platform.system()


def setremotewallwin_windows(WALLHOST, WALLUSER, WALLPASS, idx, logonscreensize):
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


def setremotewallgnome_windows(WALLHOST, WALLUSER, WALLPASS, idx, logonscreensize):
	set_wallpaper.create_linux_script()
	
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

def setremotewallwin(WALLHOST, WALLUSER, WALLPASS, idx, logonscreensize):
	setremotewallwin_windows(WALLHOST, WALLUSER, WALLPASS, idx, logonscreensize)
	
def setremotewallgnome(WALLHOST, WALLUSER, WALLPASS, idx, logonscreensize):
	setremotewallgnome_windows(WALLHOST, WALLUSER, WALLPASS, idx, logonscreensize)
	
