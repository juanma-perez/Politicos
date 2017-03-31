import pyWiki

class Searcher:       

    def doSearch(self,search):
        dic = {}
        cont = 1
        cont2 = 1
        for item in pyWiki.doSearch(search):
            cont2 +=1
            try:
                dic[cont] = pyWiki.getPageData(item)
                cont+=1
            except Exception as error:
                print ".................................................."
                print item.encode('utf-8').strip()
                print ".................................................."
            
        print cont
        print cont2
        return dic

a = Searcher()
print a.doSearch("Juan Manuel Santos")