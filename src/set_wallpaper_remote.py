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
	open(REMOTE_PATH + '\\mmwallcli.bat', 'w').write('python set_wallpaper.py -i %d\npython set_wallpaper_logon.py -i %d -s "%s"\n' % (idx, idx, (logonscreensize, )))
	
	CMD = 'psexec \\\\%s' % WALLHOST
	if WALLUSER != None and WALLPASS != None:
		CMD += ' -u "%s" -p "%s"' % (WALLUSER, WALLPASS)
	CMD +=' -i -w "C:\\Temp\\.mmwall" "C:\\Temp\\.mmwall\\mmwallcli.bat"'
	subprocess.call(CMD)
	
	CMD = 'net use t: /d'
	if WALLUSER != None and WALLPASS != None:
		CMD += ' /user:"%s" "%s"' % (WALLUSER, WALLPASS)
	subprocess.call(CMD)

def setremotewallwin_linux(WALLHOST, WALLUSER, WALLPASS, idx, logonscreensize):
	wincmd = []
	wincmd.append('rd /s /q C:\\Temp\\.mmwall.del')
	wincmd.append('cd C:\\Temp\\.mmwall')
	wincmd.append('python set_wallpaper.py -i %d' % idx)
	wincmd.append('python set_wallpaper_logon.py -i %d -s "%s"' % (idx, logonscreensize))
	wincmd.append('')
	open('mmwallcli.bat', 'wb').write('\r\n'.join(wincmd))

	smbcmd = []
	smbcmd.append('cd Temp')
	smbcmd.append('rename .mmwall .mmwall.del')
	smbcmd.append('md .mmwall')
	smbcmd.append('cd .mmwall')
	smbcmd.append('recurse')
	smbcmd.append('prompt')
	smbcmd.append('mput current')
	smbcmd.append('rename current local')
	smbcmd.append('put %s %s' % (os.path.join(SRC_PATH, 'set_wallpaper.py'), 'set_wallpaper.py'))
	smbcmd.append('put %s %s' % (os.path.join(SRC_PATH, 'set_wallpaper_logon.py'), 'set_wallpaper_logon.py'))
	smbcmd.append('mput mmwallcli.bat')
	
	CMD = 'smbclient'
	if WALLUSER != None and WALLPASS != None:
		CMD += ' -U"%s%%%s"' % (WALLUSER, WALLPASS)
	CMD += ' -c "%s"' % ";".join(smbcmd)
	CMD += ' "//%s/C$"' % WALLHOST
	#print CMD
	subprocess.call(CMD, shell=True)
	
	CMD = 'winexe'
	if WALLUSER != None and WALLPASS != None:
		CMD += ' -U"%s%%%s"' % (WALLUSER, WALLPASS)
	CMD += ' "//%s"' % WALLHOST
	CMD += ' "C:\\Temp\\.mmwall\\mmwallcli.bat"'
	#print CMD
	subprocess.call(CMD, shell=True)

	"""CMD = 'psexec \\\\%s' % WALLHOST
	if WALLUSER != None and WALLPASS != None:
		CMD += '  -u "%s" -p "%s"' % (WALLUSER, WALLPASS)
	CMD +=' -i -w "C:\\Temp\\.mmwall" "C:\\Temp\\.mmwall\\mmwallcli.bat"'
	subprocess.call(CMD)"""


def buildsshscript(idx):
	remotesh = open(os.path.join(SRC_PATH, 'mmwallcli.sh'), 'w')
	remoteshlines = []
	remoteshlines.append("#!/bin/bash")
	remoteshlines.append("rm -rf /tmp/.mmwall.del")
	remoteshlines.append("eval `strings /proc/$(pgrep -u $(whoami) gnome-session)/environ | egrep '(DBUS_SESSION_BUS_ADDRESS|DISPLAY)'`")
	remoteshlines.append("export DBUS_SESSION_BUS_ADDRESS DISPLAY")
	remoteshlines.append("gconftool-2 --set /desktop/gnome/background/picture_filename --type string /tmp/.mmwall/local/wall%d.bmp" % idx)
	remotesh.write("\n".join(remoteshlines))
	remotesh.close()

def buildpsftpscript():
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
	
	return psftpbatch.name

def buildsftpscript():
	psftpbatch = open(os.path.join(SRC_PATH, 'mmwallpsftp'),'w')
	psftpbatchlines = []
	psftpbatchlines.append('cd /tmp')
	psftpbatchlines.append('-rename .mmwall .mmwall.del')
	psftpbatchlines.append('mkdir .mmwall')
	psftpbatchlines.append('cd .mmwall')
	psftpbatchlines.append('put mmwallcli.sh')
	psftpbatchlines.append('chmod 744 mmwallcli.sh')
	psftpbatchlines.append('mkdir local')
	psftpbatchlines.append('put current/* local/')
	psftpbatch.write("\n".join(psftpbatchlines))
	psftpbatch.close()
	
	return psftpbatch.name

def setremotewallgnome_windows(WALLHOST, WALLUSER, WALLPASS, idx, logonscreensize):
	buildsshscript(idx)
	psftpbatchname = buildpsftpscript()

	CMD = 'psftp %s -b %s -be' % (WALLHOST, psftpbatchname)
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

def setremotewallgnome_linux(WALLHOST, WALLUSER, WALLPASS, idx, logonscreensize):
	buildsshscript(idx)
	psftpbatchname = buildsftpscript()

	CMD = ''
	if WALLPASS != None:
		CMD += 'sshpass -p %s ' % WALLPASS
	CMD += 'sftp -oBatchMode=no -b %s ' % psftpbatchname
	if WALLUSER != None:
		CMD += '%s@' % WALLUSER
	CMD += '%s ' % WALLHOST
	print CMD
	subprocess.call(CMD, shell=True)
	
	CMD = ''
	if WALLPASS != None:
		CMD += 'sshpass -p %s ' % WALLPASS
	CMD += 'ssh '
	if WALLUSER != None:
		CMD += '%s@' % WALLUSER
	CMD += '%s /tmp/.mmwall/mmwallcli.sh' % WALLHOST
	print CMD
	subprocess.check_call(CMD, shell=True)

def setremotewallwin(WALLHOST, WALLUSER, WALLPASS, idx, logonscreensize):
	if CURRENT_SYSTEM == "Windows":
		setremotewallwin_windows(WALLHOST, WALLUSER, WALLPASS, idx, logonscreensize)
	elif CURRENT_SYSTEM == "Linux":
		setremotewallwin_linux(WALLHOST, WALLUSER, WALLPASS, idx, logonscreensize)
	else:
		print "Setting Windows wallpaper remotely on platform %s is not supported." % CURRENT_SYSTEM


def setremotewallgnome(WALLHOST, WALLUSER, WALLPASS, idx, logonscreensize):
	if CURRENT_SYSTEM == "Windows":
		setremotewallgnome_windows(WALLHOST, WALLUSER, WALLPASS, idx, logonscreensize)
	elif CURRENT_SYSTEM == "Linux":
		setremotewallgnome_linux(WALLHOST, WALLUSER, WALLPASS, idx, logonscreensize)
	else:
		print "Setting Linux wallpaper remotely on platform %s is not supported." % CURRENT_SYSTEM
	
