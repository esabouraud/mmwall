#!/bin/python
# deprecated file !


import set_wallpaper
import set_wallpaper_logon
import ftpsync_wallpaper
import synergy_wallpaper
import randomdownload_wallpaper

if __name__=='__main__':
	randomdownload_wallpaper.get_wallpaper(True, 2.0)
	#synergy_wallpaper.make_wallpapers(True, [(2646,1024,0,0)])
	synergy_wallpaper.make_wallpapers(True, [(1366, 768, 593, 0), (1280, 1024, 0, 0)])
	#ftpsync_wallpaper.ftp_transfer("localhost", True, 0)
	set_wallpaper.set_wallpaper("current", 0)
	#set_wallpaper_logon.set_wallpaper_logon("current", 0, (1366, 768))
