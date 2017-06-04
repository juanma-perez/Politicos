import wikipedia 
import pyScraper

wikipedia.set_lang("es")
def obtenerPaginas(persona):
	page = wikipedia.page(persona)
	imprimirLinks(page.url,persona)
	
visitadas = set()

def imprimirLinks(url,persona):
	
	info = pyScraper.politic_scrapeTable(url, "")
	if info.has_key("Familia"):
		for item in info["Familia"]:
			if "links" in item:
				for link in info["Familia"][item]:
					if item.strip(" - links").encode("utf-8")+ link["url"].encode("utf-8") not in visitadas:
						if "#cite" not in link["url"]:
							print persona.encode("utf-8")+" "+ item.strip(" - links").encode("utf-8")+" "+link["title"].encode("utf-8")+" "+link["url"].encode("utf-8")
							visitadas.add(item.strip(" - links").encode("utf-8")+ link["url"].encode("utf-8"))
							imprimirLinks(link["url"] ,link["title"])
		


obtenerPaginas("Juan Manuel Santos")