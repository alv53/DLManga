#!/usr/bin/python

import sys
import os
import urllib2
import unicodedata
from bs4 import BeautifulSoup

if len(sys.argv) != 2:
    print "Usage: ./dlop.py [url to download from]"
    sys.exit()
url = sys.argv[1]

#Chomp extra text after chapter number and page number
chapterNumStr = url[:url.rfind("/")]
chapterNumStr = chapterNumStr[:chapterNumStr.rfind("/")]

#Now get manga name
chomped = chapterNumStr[:chapterNumStr.rfind("/")]
mangaName = chomped[chomped.rfind("/")+1:]

#Get chapter number
chapterNumStr = chapterNumStr[chapterNumStr.rfind("/")+1:]
print "Downloading chapter at: " + url

#Make directory for images
dirName = mangaName + "/" + chapterNumStr
if not os.path.exists(dirName):
    print "Creating directory for chapter " + dirName
    os.makedirs(dirName)

#Explore the chapter by using the "next" button while it is enabled
lastPage = False
currentUrl = url
while not lastPage and chapterNumStr in currentUrl and 'end' not in currentUrl:
    print "Exploring " + currentUrl
    response = urllib2.urlopen(currentUrl)
    content = response.read()
    #Find image url
    foundpng = False
    foundjpg = False
    for line in urllib2.urlopen(currentUrl):
        if ".png" in line:
            foundpng = True
            choppedline = line[line.index("src")+5:]
            imageurl = choppedline[:choppedline.index('"')]

            #Download from imageurl
            pageNumber = imageurl[imageurl.rfind('/'):]
            fileName = currentUrl
            fileName = fileName[fileName.rfind('/')+1:]
            if int(fileName) < 10:
                fileName = "0" + fileName
            fileName = dirName +  "/" + fileName + ".png"
            print "\tSaving " + imageurl + " -> " + fileName
            imgRequest = urllib2.Request(imageurl)
            imgData = urllib2.urlopen(imgRequest).read()
            f = open(fileName, 'w+')
            f.write(imgData)
            f.close()
    if not foundpng:
        print "\tSkipping (possibly an ad) " + currentUrl

    #Find next url
    soup = BeautifulSoup(content, 'html.parser')
    nextLi = soup.find('li', 'next')
    if next == None:
        break
    currentUrl = nextLi.contents[0]['href']
