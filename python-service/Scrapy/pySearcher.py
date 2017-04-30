import pyWiki

class Searcher:       

    def doSearch(self,search):
        list = []
        for item in pyWiki.doSearch(search):            
            try:
                list.append(pyWiki.getPageData(item))                
            except Exception as error:
                pass                
        return list

a = Searcher()
print a.doSearch("Alvaro Uribe Velez")