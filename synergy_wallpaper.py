#!/bin/python
# Resize an image and split it to be used as wallpapers on adjacent desktop (for use with synergy KM switch for example)

from optparse import OptionParser
from PIL import Image
import ctypes
import os
import random
from decimal import *
import glob

INPUTDIR = "data"
OUTPUTDIR = "current"
#OUTPUT_SCREENS = [(1280, 1024, 0), (2560, 1024, 0)]
#OUTPUT_SCREENS = [(1366, 768, 550), (1280, 1024, 0)]
OUTPUT_SCREENS = [(1280, 1024, 0)]

# compute total virtual screen size
def compute_screens_resolutions(screens):
	totalwidth = sum([s[0] for s in screens])
	totalheight = max([s[1] for s in screens])
	totalheightoffset = sum([abs(s[2]) for s in screens])
	totalheight += totalheightoffset

	return (totalwidth, totalheight)

# increase size of image so that screen is filled, while keeping original ratio
def compute_resize_resolution(imagewidth, imageheight, screenwidth, screenheight):
	resizewidth = imagewidth
	resizeheight = imageheight

	if (screenwidth > resizewidth):
		resizewidth = screenwidth
		resizeheight *= screenwidth
		resizeheight /= imagewidth
	if (screenheight > resizeheight):
		resizewidth *= screenheight
		resizewidth /= resizeheight
		resizeheight = screenheight

	return (resizewidth, resizeheight)

# crop center of image so that it matches screen dimensions
def compute_crop_coordinates(imagewidth, imageheight, screenwidth, screenheight):
	x1 = 0
	y1 = 0
	x2 = imagewidth
	y2 = imageheight

	# todo: improve rouding, there is often a 1px error
	if (screenwidth < imagewidth):
		x1 = int(round(Decimal(imagewidth - screenwidth) / 2))
		x2 -= x1
	
	if (screenheight < imageheight):
		y1 = int(round(Decimal(imageheight - screenheight) / 2))
		y2 -= y1
	
	return (x1, y1, x2, y2)

def generate_wallpaper(inputimagepath, outputdir, screenresolutions):
	print "Source image: %s" % inputimagepath
	(screenwidth, screenheight) = compute_screens_resolutions(screenresolutions)
	print "Output screen resolution is: (%d,%d)" % (screenwidth, screenheight)
	
	im = Image.open(inputimagepath)
	(imagewidth, imageheight) = im.size
	print "Source image resolution is: (%d,%d)" % (imagewidth, imageheight)
	
	(resizewidth, resizeheight) = compute_resize_resolution(imagewidth, imageheight, screenwidth, screenheight)
	if (imagewidth != resizewidth or imageheight != resizeheight):
		print "Upscaled image resolution is: (%d,%d)" % (resizewidth, resizeheight)
		im = im.resize((resizewidth, resizeheight), Image.BICUBIC)
	
	if (screenwidth != resizewidth or screenheight != resizeheight):
		(x1, y1, x2, y2) = compute_crop_coordinates(resizewidth, resizeheight, screenwidth, screenheight)
		print "Cropped image coordinates are: (%d,%d),(%d,%d))" % (x1, y1, x2, y2)
		im = im.crop((x1, y1, x2, y2))
	
	im.save("im.bmp")
	
	x = 0
	i = 0
	for s in screenresolutions:
		wall = im.crop((x, s[2], x + s[0], s[1] + s[2]))
		wall.load()
		wall.save(os.path.join(outputdir, "wall%d.bmp" % i))
		x += s[0]
		i += 1


def make_wallpapers(uselatest):
	if (False == os.path.isdir(OUTPUTDIR)):
		os.makedirs(OUTPUTDIR)
	
	inputimagepath = ""
	if (uselatest == True):
		inputimagepath = max(glob.iglob(os.path.join(INPUTDIR, "*.*")), key=os.path.getctime)
	else:
		inputimagepath = os.path.join(INPUTDIR, random.choice(os.listdir(INPUTDIR)))
	generate_wallpaper(inputimagepath, OUTPUTDIR, OUTPUT_SCREENS)

		
if __name__=='__main__':
	parser = OptionParser()
	parser.add_option("-L", "--use-latest-image", dest="latest", action="store_true", default=False, help="Use the most recent image found in images directory if true, otherwise pick one at random")
	
	(options, args) = parser.parse_args()
	make_wallpapers(options.latest)
