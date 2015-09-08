#!/usr/bin/python

import sys
import os
import urllib2
import unicodedata
from bs4 import BeautifulSoup

if len(sys.argv) != 2:
	print "Usage: ./dlop.py [url to download one piece from]"
	sys.exit()
url = sys.argv[1]
#Chomp extra text after chapter number
chapterNumStr = url[:url.rfind("/")]
#Now get chapter number
chapterNumStr = chapterNumStr[chapterNumStr.rfind("/")+1:]
print "Downloading one piece chapter at: " + url


#Download initial url
print "Loading info from given url..."
response = urllib2.urlopen(url)
content = response.read();

#Get set of all pages from dropdown list
print "Finding url from pages dropdown..."
urlsToDownload = set()
soup = BeautifulSoup(content, 'html.parser')
for a in soup.find_all('a', href=True):
	if url in a['href']:
		urlsToDownload.add(a['href'])

#Loop and download each url
print "Finding image urls to download..."
urlToImageMap = {}
imageurls = set()
for url in urlsToDownload:
	response = urllib2.urlopen(url)
	content = response.readlines()
	#Get the png link from the webpage, and download that
	foundpng = False
	for line in content:
		if ".png" in line:
			foundpng = True
			choppedline = line[line.index("src")+5:]
			choppedline = choppedline[:choppedline.index('"')]
			imageurls.add(choppedline)
			urlToImageMap[choppedline] = url
	if not foundpng:
		print "Skipping (possibly an ad) " + url


#Make directory for images
if len(imageurls) > 0:
	if not os.path.exists(chapterNumStr):
		print "Creating directory for chapter " + str(chapterNumStr)
		os.makedirs(chapterNumStr)
	for imageurl in imageurls:
		pageNumber = imageurl[imageurl.rfind('/'):]
		fileName = urlToImageMap[imageurl]
		fileName = fileName[fileName.rfind('/')+1:]
		if int(fileName) < 10:
			fileName = "0" + fileName
		fileName = chapterNumStr + "/" + fileName + ".png"
		print "Downloading " + imageurl + " -> " + fileName
		imgRequest = urllib2.Request(imageurl)
		imgData = urllib2.urlopen(imgRequest).read()
		f = open(fileName, 'w+')
		f.write(imgData)
		f.close()
	print "Finished downloading images"
else:
	print "No images to download"
