import json
import time
from pyScraper import Scraper
from pyWiki import getPageData
from FileManager import FileManager
# -*- coding: utf-8 -*-

class JSONManager:
    def __init__(self, search):
        self.fileManager = FileManager()
        self.page = None
        self.search=search
        try:
            self.page = Scraper(search)            
            self.table =self.page.getTable()
            #self.dict_photo= pyWiki.getPageData(search)
        except Exception as error:
            self.fileManager.recordError(str(error))
        

    def clearValue(self,sentence):
        temp = sentence.split("\n")
        if len(temp)==1:
            return temp[0]
        else:
            if "" in temp:
                return self.clearValue(''.join(filter(lambda a: a != "", temp)))
            else:
                return temp

    def eliminateCharacters(self, cadena):
        d={'.':'',';':''}
        return ''.join(d[s] if s in d else s for s in cadena)

    def addValue(self,dictionary,name,value):
        name = self.eliminateCharacters(name)
    	dictionary[name]=value
    	return dictionary #Return the dictionary with a new value
    
    def scrapeTable(self):
        dic={}
        try:
            if self.page is not None:
                dic = self.addValue(dic,"Fecha de registro", time.strftime("%x") + " " + time.strftime("%X"))
                dic = self.addValue(dic,"Nombre",self.page.getTitle())
                
                dic = self.addValue(dic,"Foto", getPageData(self.search).get('Imagen'))
                
                filas = self.table.find_all('tr')[2:]
                parent = ""
                for fil in filas:
                    if len(fil.find_all('th'))>0 and len(fil.find_all('td'))<1:
                        parent = self.clearValue(fil.find_all('th')[0].text)
                        dic=self.addValue(dic,parent,{})
                    elif len(fil.find_all('th'))>0 and len(fil.find_all('td'))>0:
                        if parent != "":
                            temp = dic[self.eliminateCharacters(parent)]
                            temp = self.addValue(temp,fil.find_all('th')[0].text, self.clearValue(fil.find_all('td')[0].text))
                            dic[self.eliminateCharacters(parent)] = temp
                        else:
                             self.addValue(dic,fil.find_all('th')[0].text, fil.find_all('td')[0].text)    	
        except Exception as error:
                self.fileManager.recordError(str(error))
        return dic

a = JSONManager("asdkasdj")
aaa = a.scrapeTable()
print(aaa)