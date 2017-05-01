import pyWiki

class Searcher:       

    def doSearch(self,search):
        list = []
        for item in pyWiki.doSearch(search):            
            try:
            	page=pyWiki.getPage(item)
            	print page
                list.append({'Title': page.title, 'url': page.url})                
            except Exception as error:
                pass                
                
        return list


a = Searcher()
print a.doSearch("Alvaro Uribe Velez")