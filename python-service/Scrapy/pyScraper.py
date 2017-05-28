#!/usr/bin/python
from bs4 import BeautifulSoup
import urllib
import urllib2
import time
import Libraries.FileManager as fm
import Libraries.JSONProcessor as jsonp
# -*- coding: utf-8 -*-

#Returns a Beutiful object
def getSoup(url):
	response = urllib2.urlopen(url) #Load the URL
	return BeautifulSoup(response.read(),"html.parser")  #Load the structure html to the library     

#Get the title of the page
def getTitle(soup):
	return soup.title.string

#Returns a element with infobox table
def getTable(soup): 
	return soup.find('table', 'infobox')

#Scrapy of the imge in the infobix table
def getTableImage(url):
	return "https:" + getTable(getSoup(url)).find_all('tr')[1].find_all('img')[0]['src']
		
#Scrapy infobox (Proven for politicians) into json structure
def politic_scrapeTable(url,image):
	soup = getSoup(url)
	table = soup.find('table', 'infobox')
	table = getTable(soup)
	dic={}
	try:
		if soup is not None:
			dic = jsonp.addValue(dic,"Fecha de registro", time.strftime("%x") + " " + time.strftime("%X"))
			dic = jsonp.addValue(dic,"Nombre",getTitle(soup).replace(' - Wikipedia, la enciclopedia libre',''))
			dic = jsonp.addValue(dic,"Url",url)
			dic = jsonp.addValue(dic,"Imagen",url)			
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
	   	fm.registerError(str(error))
	return dic 

#politic_scrapeTable("https://es.wikipedia.org/wiki/Juan_Manuel_Santos","")
#fm.writeFileJSON("prueba",politic_scrapeTable("https://es.wikipedia.org/wiki/Juan_Manuel_Santos"))