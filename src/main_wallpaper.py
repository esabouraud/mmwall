#!/bin/python


import set_wallpaper
import ftpsync_wallpaper
import synergy_wallpaper
import detdownload_wallpaper

if __name__=='__main__':
	detdownload_wallpaper.get_wallpaper(True, 2.0)
	synergy_wallpaper.make_wallpapers(True, [(1280,1024,0)])
	ftpsync_wallpaper.ftp_transfer("localhost", True, 0)
	set_wallpaper.set_wallpaper("current", 0)
