import enumProc
import re
import time
import sys
from googlesearch.googlesearch import GoogleSearch
from myprints import *



def getSpotifyWindowName():
	pids = enumProc.search('Spotify.exe')
	for pid in pids:
		name = enumProc.enumProcWnds(pid)
	name = re.sub('- live$', '', name)
	name = re.sub('- Live$', '', name)
	name = re.sub('- Edit$', '', name)
	name = re.sub('- edit$', '', name)
	name = re.sub('on Vimeo', '', name)
	name = re.sub('\(With Sample\)', '', name)
	return name


def getGoogleSearchResult(phrase):	
	ucPrint("Google search phrase: "+phrase)	
	return GoogleSearch().search(phrase)

def getLine(text):
	return iter(text.splitlines())
	
def getSongName(windowName):
	a = windowName.split(' - ')
	return a[1].rstrip()

def getSongLyrics_AZLyrics(content, wName):
	lirycs = []
	title = "\""+getSongName(wName)+"\""
	#print title
	startFound = False
	for line in getLine(content):
		if " Submit Corrections" in line:
			#print "Found Submit Corrections"
			break;
		if startFound and not re.match(r'^\s*$', line):
			lirycs.append(line)
		if re.search(title, line, re.IGNORECASE):
			#print "1st", line 
			if "lyrics" not in line:
				#print "2st", line 
				startFound = True
	return lirycs

def getSongLyrics_Tekstowo (content, wName):
	lirycs = []
	startFound = False
	#ucPrint(content)
	for line in getLine(content):
		#ucPrint(line)
		if re.search("Poznaj histori. zmian tego tekstu", line):
			#print "end:" + line 
			break;
		if startFound and not re.match(r'^\s*$', line):
			lirycs.append(line.lstrip())
		if re.search("Tekst piosenki:", line):
			#print "Tekst piosenki" + line
			startFound = True
	return lirycs

	
webParsers = [["AZLyrics", getSongLyrics_AZLyrics],["tekst piosenki,", getSongLyrics_Tekstowo]]
			 
def parseGoogleOutput(response, wName):
	i = 0 
	print("Results:")
	for result in response.results:
		ucPrint(result.title)
		for parser in webParsers:
			if parser[0] in result.title:
				return parser[1](result.getText(),wName)
		if i > 5:
			break
		i = i + 1
	print "No lyrics were found"
	return None
	
if __name__ == "__main__":
	lastName = "HopfulyNonExistingSongTitle"
	while (True):
		wName = getSpotifyWindowName()
		if lastName != wName:
			if wName == "Spotify":
				print "Currently no song is playing!"
			else:
				ucPrint(wName)
				content = getGoogleSearchResult(wName)
				#ucPrint(content)
				if content:
					lirycs = parseGoogleOutput(content, wName)
					print 
					if lirycs:
						for ln in lirycs:
							ucPrint(ln)
				print 
			lastName = wName
		time.sleep(5)