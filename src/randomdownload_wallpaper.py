#!/bin/python

from optparse import OptionParser
import random
import detdownload_wallpaper
import tmbdownload_wallpaper
import localdownload_wallpaper
import wpfdownload_wallpaper
import ifldownload_wallpaper

def get_wallpaper(singledl, minratio):
	downloaders = [detdownload_wallpaper, tmbdownload_wallpaper, localdownload_wallpaper, wpfdownload_wallpaper, ifldownload_wallpaper]
	random.choice(downloaders).get_wallpaper(singledl, minratio)

if __name__=='__main__':
	parser = OptionParser()
	parser.add_option("-s", "--single-download", dest="singledl", action="store_true", default=False, help="Download a single image if set, instead of all found")
	parser.add_option("-r", "--img-ratio", dest="minratio", default=2.0, help="Minimum Width/Height ratio of images candidates for download")

	(options, args) = parser.parse_args()
	get_wallpaper(options.singledl, options.minratio)
