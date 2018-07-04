import sys
import os 
#from time import sleep

RED   = "color 4"  
BLUE  = "color 1"
YELLOW  = "color 6"
GREEN = "color 2"
RESET = "color 7"
REVERSE = "color 0"


def ucPrint(text):
	#print unicode(text, "utf-8").encode(sys.stdout.encoding, errors='replace')
	print text.encode(sys.stdout.encoding, errors='replace')

def applyColor(color):
	os.system(color)

def infoPrint(text):
	applyColor(BLUE)
	print text 
	applyColor(RESET)

def warrnPrint(text):
	applyColor(YELLOW)
	print text 
	applyColor(RESET)
	
def grenPrint(text):
	applyColor(GREEN)
	print text 
	applyColor(RESET)
	
def errorPrint(text):
	applyColor(RED)
	print text 
	applyColor(RESET)
	
def infoUcPrint(text):
	applyColor(BLUE)
	#print unicode(text, "utf-8").encode(sys.stdout.encoding, errors='replace')
	print text.encode(sys.stdout.encoding, errors='replace')
	applyColor(RESET)