import pyWiki

class Searcher:       

    def doSearch(self,search):
        list = []
        for item in pyWiki.search(search):   
            print item.encode('utf-8')
            print pyWiki.getPageData(item)         
            list.append(pyWiki.getPageData(item))                
        return list


#a = Searcher()

#print a.doSearch("Alvaro Uribe Velez")

# for a in pyWiki.search("Juan Manuel Santos Calderon"):
#     print a.encode('utf-8')