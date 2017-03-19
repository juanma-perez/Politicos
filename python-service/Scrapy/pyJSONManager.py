import json
from pyScraper import Scraper
import pyWiki
# -*- coding: utf-8 -*-

class JSONManager:
    def __init__(self, search):
        self.page = Scraper(search)
        self.table =self.page.getTable()

    def clearValue(self,sentence):
        temp = sentence.split("\n")
        if len(temp)==1:
            return temp[0]
        else:
            if "" in temp:
                return self.clearValue(''.join(filter(lambda a: a != "", temp)))
            else:
                return temp

    def addValue(self,dictionary,name,value):
    	dictionary[name]=value
    	return dictionary #Return the dictionary with a new value

   
    
    def scrapeTable(self):
        dic={}
        dic = self.addValue(dic,"Nombre",self.page.getTitle())
        if  len(self.table.find_all('a'))>0:
            dic = self.addValue(dic,"Foto","https://es.wikipedia.org" + self.table.find_all('a')[0].get('href'))
        else:
            dic = self.addValue(dic,"Foto","Imagen no encontrada")
        filas = self.table.find_all('tr')[2:]
        parent = ""
        for fil in filas:
            if len(fil.find_all('th'))>0 and len(fil.find_all('td'))<1:
                parent = self.clearValue(fil.find_all('th')[0].text)
                dic=self.addValue(dic,parent,{})
            elif len(fil.find_all('th'))>0 and len(fil.find_all('td'))>0:
                if parent != "":
                    temp = dic[parent]
                    temp = self.addValue(temp,fil.find_all('th')[0].text, self.clearValue(fil.find_all('td')[0].text))
                    dic[parent] = temp
                else:
                     self.addValue(dic,fil.find_all('th')[0].text, fil.find_all('td')[0].text)    	
        return dic

    def writeJSON(self,name, linea):
    	name += ".json" 
    	try:      
    		with open(name,'a') as g:
    			json.dump(linea, g) 
    			g.write("\n")
    	except IOError:
    		open(name,'w')
    		escribirArchivo(name, linea)