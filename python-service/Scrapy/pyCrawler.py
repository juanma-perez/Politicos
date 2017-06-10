import wikipedia 
import pyScraper
wikipedia.set_lang("es")
def busqueda(valor, limit):
	lista = []
	page = wikipedia.page(valor)
	busquedas = set(page.links)
	cont = 1
	while  cont < limit:
		result = obtenerPaginas(busquedas,cont,limit)
		cont = result["cont"]
		busquedas = result["newlinks"]
def obtenerPaginas(links,num,limit):
	result = {"cont":num,"newlinks":set(links)}
	dic = {}
	for link in links:
		try:
			tempPage = wikipedia.page(link)
			dic["id"] = result["cont"]
			dic["title"] = tempPage.title
			dic["url"] = tempPage.url
			if result["cont"] > limit:
				break
			result["cont"]+=1			
			result["newlinks"] = result["newlinks"].union(tempPage.links)
			print dic
		except Exception as errorSearch:
			print errorSearch
	return result
#a = set([1,2,3])
#b = set([3,4,5])
#print a.union(b)
#busqueda("Juan Manuel Santos",10)

def buscarRelacionPersona(persona):
	print persona.encode("utf-8")
	page = wikipedia.page(persona)
	print page
	info =  pyScraper.politic_scrapeTable(page.url,"NA")
	if info.has_key("Familia"):
		for familiar in info["Familia"]:
			for key in info["Familia"][familiar]:
				buscarRelacionPersona(key)

buscarRelacionPersona("Juan Manuel Santos Calderon")