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
	return name

def getGoogleSearchResult(phrase):	
	ucPrint("Google search phrase: "+phrase)	
	response = GoogleSearch().search(phrase)
	i = 0 
	print("Results:")
	for result in response.results:
		ucPrint(result.title)
		if "AZLyrics" in result.title:
			return response.results[i].getText()
		if i > 10:
			break
		i = i + 1
	print "No lyrics were found"
	return None

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
	

if __name__ == "__main__":
	lastName = "HopfulyNonExistingSongTitle"
	while (True):
		wName = getSpotifyWindowName()
		if lastName != wName:
			if wName == "Spotify":
				print "Currently no song is playing!"
			else:
				print 
				print wName
				content = getGoogleSearchResult(wName)
				#ucPrint(content)
				if content:
					print 
					lirycs = getSongLyrics_AZLyrics(content, wName)
					for ln in lirycs:
						print ln
				print 
			lastName = wName
		time.sleep(5)