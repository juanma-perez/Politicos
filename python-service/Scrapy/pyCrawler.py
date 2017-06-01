import wikipedia 


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
busqueda("Juan Manuel Santos",10)