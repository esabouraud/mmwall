#!/bin/python
# Download wallpapers from Dead End Thrills random feed

from optparse import OptionParser
from PIL import Image
import os
import glob
import shutil
import random
from decimal import *

INPUTDIR = "wallpapers"
OUTPUTDIR = "data"

def save_image(imgpath):
	#print "%s_%s" % (m.group(1), m.group(2))
	filepath = os.path.join("data", os.path.basename(imgpath))
	"""if os.path.exists(filepath):
		print "Deleting %s" % filepath
		os.remove(filepath)"""
	print "Copying %s to %s..." % (imgpath, filepath)
	shutil.copyfile(imgpath, filepath)


def get_wallpaper(singledl, minratio):
	if (False == os.path.isdir(OUTPUTDIR)):
		os.makedirs(OUTPUTDIR)

	imglist = [i for i in glob.iglob(os.path.join(INPUTDIR, "*.*"))]
	random.shuffle(imglist)
	for img in imglist:
		#print img
		im = Image.open(img)
		(imgwidth, imgheight) = im.size
		imgratio = round(Decimal(imgwidth) / Decimal(imgheight), 1)
		if (imgratio >= minratio):
			save_image(img)
			if (singledl == True):
				break

if __name__=='__main__':
	parser = OptionParser()
	parser.add_option("-s", "--single-download", dest="singledl", action="store_true", default=False, help="Download a single image if set, instead of all found")
	parser.add_option("-r", "--img-ratio", dest="minratio", default=2.0, help="Minimum Width/Height ratio of images candidates for download")

	(options, args) = parser.parse_args()
	get_wallpaper(options.singledl, options.minratio)
