import pyWiki

class Searcher:       

    def doSearch(self,search):
        dic = {}
        cont = 1
        cont2 = 1
        for item in pyWiki.doSearch(search):
            cont2 +=1
            try:
                dic[str(cont)] = pyWiki.getPageData(item)
                cont+=1
            except Exception as error:
                pass        
        print cont
        print cont2
        return dic

a = Searcher()
print a.doSearch("Alvaro Uribe Velez")