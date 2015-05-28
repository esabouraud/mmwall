#!/bin/python

# mmwall launcher
# mmwall currently only works on windows, for wallpaper local and remote setting (uses Win32 API, network drive mount and psexec)

import json
import optparse

import set_wallpaper
import set_wallpaper_logon
import set_wallpaper_remote
import synergy_wallpaper
import randomdownload_wallpaper


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
				set_wallpaper_remote.setremotewallwin(host['remotehost'], remotelogin, remotepw, idx, logonscreensize)
			elif host.get('remoteos') == 'Linux':
				set_wallpaper_remote.setremotewallgnome(host['remotehost'], remotelogin, remotepw, idx, logonscreensize)
			else:
				print 'Remote host os "%s" unsupported.' % host['remoteos']
		else:
			set_wallpaper.set_wallpaper('current', idx)
			set_wallpaper_logon.set_wallpaper_logon('current', idx, logonscreensize)


if __name__=='__main__':
	parser = optparse.OptionParser(description='mmwall: multi-machine background wallpaper changer')
	parser.add_option('-c', '--configuration', dest='cfgfile', default='mmwallcfg.json', metavar='FILEPATH', help='mmwall configuration file path')
	(options, args) = parser.parse_args()

	run_mmwall(options.cfgfile)
