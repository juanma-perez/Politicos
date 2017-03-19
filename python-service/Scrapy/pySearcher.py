import pyWiki

class Searcher:
    def doSearch(self,search):
        temp = []
        for person in pyWiki.doSearch(search):
            categories = pyWiki.getCategories(pyWiki.getPage(person))
            for item in categories:
                if self.categories().has_key(item):
                    temp += [person]
        return temp
    
    def categories(self):
        return {u"Categor\u00eda:Hombres":""}