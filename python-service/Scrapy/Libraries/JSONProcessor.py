import json
# -*- coding: utf-8 -*-
        
#Returns a array or a string without empty values 
def clearValue(sentence):
    temp = sentence.split("\n")
    if len(temp)==1:
        return temp[0]
    else:
        if "" in temp:
            return clearValue(''.join(filter(lambda a: a != "", temp)))
        else:
            return temp

#Eliminates characters that generate conflicts with json structure
def eliminateCharacters(cadena):
    d={'.':'',';':''}
    return ''.join(d[s] if s in d else s for s in cadena)

#Adds Values to a dictionary
def addValue(dictionary,name,value):
    name = eliminateCharacters(name)
    dictionary[name]=value
    return dictionary #Return the dictionary with a new value