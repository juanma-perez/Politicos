import wikipedia
from wptools import wptools 
import urllib
import urllib2

# -*- coding: utf-8 -*-
wikipedia.set_lang("es")

def getPage(search):
    return wikipedia.page(search) 

def doSearch(search):
	return wikipedia.search(search)	
	
def getCategories(page):
    return page.categories #Get the categories of a page from Wikipedia

def getPageData(search):
	dic ={}
	try:
		page = wptools.page(search).get_query()
		dic["Title"]= page.title
		dic["Url"]= page.url
		dic["Imagen"]= page.image('page')['url']
		print "----->Categorias:"
		page 
	except Exception as error:
		dic["Title"]=search
		page =  getPage(search)
		dic["Url"]=page.url		
		dic["Imagen"]= "Imagen no disponible"
		dic["Categorias"] = getCategories(page)
	page = wptools.page(search).get_query()
	dic["Title"]= page.title
	dic["Url"]= page.url
	try:
		dic["Imagen"]= page.image('page')['url']

	except Exception as error:
		dic["Imagen"]='No_Disponible'
	return dic
		
