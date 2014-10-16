#!/bin/python
# Download wallpapers from Dead End Thrills random feed

from bs4 import BeautifulSoup
import urllib2
from decimal import *
import re
import os

URL = "http://deadendthrills.com/random/"
OUTPUTDIR = "data"

def save_image(imgurl):
	m = re.match("^.*/(\\w*)/large/([\\w\\.]*$)", imgurl)
	if (m == None):
		print "No regexp match for %s" % imgurl
		return
	#print "%s_%s" % (m.group(1), m.group(2))
	filepath = os.path.join("data", "%s_%s" % (m.group(1), m.group(2)))
	print "Downloading %s as %s..." % (imgurl, filepath)
	try:
		response = urllib2.urlopen(imgurl)
		f = open(filepath, "wb")
		f.write(response.read())
		print "Download completed"
	except urllib2.HTTPError as e:
		print e.read()
		print "Download aborted"
		return

def get_wallpaper():
	response = urllib2.urlopen(URL)
	html = response.read()
	
	soup = BeautifulSoup(html)
	#divs = soup.find_all("div", class_="jig-imageContainer")
	div = soup.find("div", {"id": "content"}, {"role":"main"})
	noscript = div.find("noscript")
	aimgs = noscript.find_all("a")
	for a in aimgs:
		img = a.find("img")
		imgwidth = int(img.get("width"))
		imgheight = int(img.get("height"))
		imgratio = round(Decimal(imgwidth) / Decimal(imgheight), 1)
		# Only get images suitable for multiscreen wallpapers
		if (imgratio >= 2.0):
			save_image(a.get("href"))
		#print "%s (%d, %d) %f" % (img.get('alt'), imgwidth, imgheight, imgratio)
	
if __name__=='__main__':
	if (False == os.path.isdir(OUTPUTDIR)):
		os.makedirs(OUTPUTDIR)
	get_wallpaper()
