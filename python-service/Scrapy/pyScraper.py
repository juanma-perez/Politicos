#!/usr/bin/python
import pyWiki
from bs4 import BeautifulSoup
import urllib
import urllib2
import time
#from pyScraper import Scraper
import Libraries.FileManager as fm
import Libraries.JSONProcessor as jsonp
from pyWiki import getPageData
# -*- coding: utf-8 -*-

#"https://es.wikipedia.org/wiki/Santos"
def getSoup(url):
	response = urllib2.urlopen(url) #Load the URL
	return BeautifulSoup(response.read(),"html.parser")  #Load the structure html to the library     

def getTitle(soup):
	return soup.title.string

def getTable(soup): 
	return soup.find('table', 'infobox')

def politic_scrapeTable(url):
	soup = getSoup(url)
	table = getTable(soup)
	dic={}
	try:
		if soup is not None:
			dic = jsonp.addValue(dic,"Fecha de registro", time.strftime("%x") + " " + time.strftime("%X"))
			dic = jsonp.addValue(dic,"Nombre",getTitle(soup))
			dic = jsonp.addValue(dic,"url",url)			
			filas = table.find_all('tr')[2:]
			parent = ""
			for fil in filas:
				if len(fil.find_all('th'))>0 and len(fil.find_all('td'))<1:
					parent = jsonp.clearValue(fil.find_all('th')[0].text)
					dic = jsonp.addValue(dic,jsonp.eliminateCharacters(parent),{})
				elif len(fil.find_all('th')) >= 1  and len(fil.find_all('td')) > 0:
					if parent != "":
						temp = {}
						temp = jsonp.addValue(temp,fil.find_all('th')[0].text, jsonp.clearValue(fil.find_all('td')[0].text))
						dic = jsonp.addValue(dic,jsonp.eliminateCharacters(parent),temp)
					else:
						dic = jsonp.addValue(dic,fil.find_all('th')[0].text, fil.find_all('td')[0].text)		
	except Exception as error:
	   	fm.registerError(error)
	return dic 

print politic_scrapeTable("https://es.wikipedia.org/wiki/Juan_Manuel_Santos")