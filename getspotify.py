import enumProc
import re
import time 

def getSpotifyWindowName():
	pids = enumProc.search('Spotify.exe')
	for pid in pids:
		name = enumProc.enumProcWnds(pid)
	name = re.sub('- live$', '', name)
	name = re.sub('- Live$', '', name)
	name = re.sub('- Edit$', '', name)
	name = re.sub('- edit$', '', name)
	return name

def getGoogleSearchResult(phrase):		
	from googlesearch.googlesearch import GoogleSearch
	response = GoogleSearch().search(phrase)
	#print response.results[0].title
	return response.results[0].getText()

def getLine(text):
	return iter(text.splitlines())
	
def getSongName(windowName):
	a = windowName.split(' - ')
	return a[1].rstrip()

	
def getSongLirycs(content, wName):
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
		if title in line:
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
				print 
				lirycs = getSongLirycs(content, wName)
				for ln in lirycs:
					print ln
			lastName = wName
		time.sleep(5)