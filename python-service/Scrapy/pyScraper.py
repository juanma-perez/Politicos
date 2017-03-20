#!/usr/bin/python
import pyWiki
from bs4 import BeautifulSoup
import urllib
import urllib2

class Scraper():
	def __init__(self, search):
		response = urllib2.urlopen(pyWiki.getPage(search).url) #Load the URL
		self.soup = BeautifulSoup(response.read(),"html.parser")  #Load the structure html to the library 
    
	def getTitle(self):
		return self.soup.title.string

	def getTable(self): 
		return self.soup.find('table', 'infobox')  #Get the table of information in wikipedia
	
	