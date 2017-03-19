from pySearcher import Searcher
from pyJSONManager import JSONManager
"""
search = Searcher()
for item in search.doSearch("German Lopez"):
	print (item.encode("utf8"))
"""
busqueda = "Donald trump"
jsonFile = JSONManager(busqueda)
print jsonFile
import pdb; pdb.set_trace()
#jsonFile.writeJSON(busqueda, jsonFile.scrapeTable())
