#!/bin/python
# Download wallpapers from Dead End Thrills random feed

from optparse import OptionParser
from bs4 import BeautifulSoup
import urllib2
import re
import os
import random

URL = "https://interfacelift.com/wallpaper/downloads/random/3_screens/4096x1024/"
OUTPUTDIR = "data"

def save_image(imgurl):
	m = re.match("^.*/(.*)$", imgurl)
	if (m == None):
		print "No regexp match for %s" % imgurl
		return
	filepath = os.path.join("data", "IFL_%s" % (m.group(1)))
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
	divs = soup.find_all("div", {"class":"download"})
	random.shuffle(divs)
	for d in divs:
		aimg = d.find("a")
		try:
			save_image("https://interfacelift.com" + aimg.get("href"))
			if (singledl == True):
				break
		except urllib2.HTTPError as e:
			print e.read()
		
if __name__=='__main__':
	parser = OptionParser()
	parser.add_option("-s", "--single-download", dest="singledl", action="store_true", default=False, help="Download a single image if set, instead of all found")
	parser.add_option("-r", "--img-ratio", dest="minratio", default=2.0, help="Minimum Width/Height ratio of images candidates for download")

	(options, args) = parser.parse_args()
	get_wallpaper(options.singledl, options.minratio)
