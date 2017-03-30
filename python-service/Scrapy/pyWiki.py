import wikipedia
# -*- coding: utf-8 -*-
wikipedia.set_lang("es")

def getPage(search):
    return wikipedia.page(search) 

def doSearch(search):
	return wikipedia.search(search)	
	
def getCategories(page):
    return page.categories #Get the categories of a page from Wikipedia