#!/bin/python
# Download wallpapers from Dead End Thrills random feed

from optparse import OptionParser
from bs4 import BeautifulSoup
import urllib2
from decimal import *
import re
import os
import random

URL = "http://www.wallpaperfusion.com/RSS/?TagShow=videogames|&Monitors=3"
OUTPUTDIR = "data"

def save_image(imgurl):
	m = re.match("^.*/Download/(\\w*)/\?.*$", imgurl)
	if (m == None):
		print "No regexp match for %s" % imgurl
		return
	filepath = os.path.join("data", "WPF_%s.jpg" % (m.group(1)))
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
	rss = response.read()
	
	souprss = BeautifulSoup(rss, 'xml')
	guids = souprss.find_all("guid")
	random.shuffle(guids)
	for g in guids:
		responseimg = urllib2.urlopen(guids[0].contents[0])
		htmlimg = responseimg.read()
		soup = BeautifulSoup(htmlimg)
		orig = soup.find("div", {"class":"MonOrig"})
		aimg = orig.find("a", {"class":"MonBorder"})
		try:
			save_image(aimg.get("href"))
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
