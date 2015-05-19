#!/bin/python
# Download wallpapers from Triple Monitor Backgrounds random feed

from optparse import OptionParser
from bs4 import BeautifulSoup
import urllib2
import re
import os

BASEURL = "http://www.triplemonitorbackgrounds.com"
URL = BASEURL + "/random/"
OUTPUTDIR = "data"

def save_image(imgurl):
	m = re.match("^.*/albums/([\\w\\-_]*)/([\\w\\.\\-_]*$)", imgurl)
	if (m == None):
		print "No regexp match for %s" % imgurl
		return
	#print "%s_%s" % (m.group(1), m.group(2))
	filepath = os.path.join("data", "TMB_%s_%s" % (m.group(1), m.group(2)))
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
	div = soup.find("div", {"id":"random"})
	aimgs = div.find_all("a", {"title":True}, {"href":True})
	for a in aimgs:
		if (a.find("img") == None):
			continue

		responseimg = urllib2.urlopen(BASEURL + a.get("href"))
		htmlimg = responseimg.read()

		soupimg = BeautifulSoup(htmlimg)
		divmain = soupimg.find("div", {"id":"main"})
		divimg = divmain.find("div", {"id":"SingleImageContainer"})
		aimg = divimg.find("a", {"title":True}, {"href":True})
		#print aimg
		try:
			save_image(BASEURL + aimg.get("href"))
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
