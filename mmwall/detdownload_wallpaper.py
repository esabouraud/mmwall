#!/bin/python
# Download wallpapers from Dead End Thrills random feed

from optparse import OptionParser
from bs4 import BeautifulSoup
import urllib2
from decimal import Decimal
import re
import os
import random

URL = "http://deadendthrills.com/random/"
OUTPUTDIR = "data"

def save_image(imgurl):
	m = re.match("^.*/(\\w*)/large/([\\w\\.]*$)", imgurl)
	if (m == None):
		print "No regexp match for %s" % imgurl
		return
	#print "%s_%s" % (m.group(1), m.group(2))
	filepath = os.path.join("data", "DET_%s_%s" % (m.group(1), m.group(2)))
	print "Downloading %s as %s..." % (imgurl, filepath)
	try:
		response = urllib2.urlopen(imgurl)
		f = open(filepath, "wb")
		f.write(response.read())
		print "Download completed"
	except urllib2.HTTPError as e:
		print "Download aborted"
		raise e

def get_wallpaper(singledl, minratio):
	if (False == os.path.isdir(OUTPUTDIR)):
		os.makedirs(OUTPUTDIR)

	response = urllib2.urlopen(URL)
	html = response.read()
	
	soup = BeautifulSoup(html)
	#divs = soup.find_all("div", class_="jig-imageContainer")
	div = soup.find("div", {"id": "content"}, {"role":"main"})
	noscript = div.find("noscript")
	aimgs = noscript.find_all("a")
	random.shuffle(aimgs)
	for a in aimgs:
		img = a.find("img")
		imgwidth = int(img.get("width"))
		imgheight = int(img.get("height"))
		imgratio = round(Decimal(imgwidth) / Decimal(imgheight), 1)
		# Only get images suitable for multiscreen wallpapers
		if (imgratio >= minratio):
			try:
				save_image(a.get("href"))
				if (singledl == True):
					break
			except urllib2.HTTPError as e:
				print e.read()
		#print "%s (%d, %d) %f" % (img.get('alt'), imgwidth, imgheight, imgratio)

		
if __name__=='__main__':
	parser = OptionParser()
	parser.add_option("-s", "--single-download", dest="singledl", action="store_true", default=False, help="Download a single image if set, instead of all found")
	parser.add_option("-r", "--img-ratio", dest="minratio", default=2.0, help="Minimum Width/Height ratio of images candidates for download")

	(options, args) = parser.parse_args()
	get_wallpaper(options.singledl, options.minratio)
